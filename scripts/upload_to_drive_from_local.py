#!/usr/bin/env python3
import hashlib
import mimetypes
from pathlib import Path

import pathspec
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Quản lý Drive: chỉ tạo/ghi mới từ app (không full-access toàn Drive)
SCOPES = ['https://www.googleapis.com/auth/drive.file']
ENV_FILE = 'config/.env'
OAUTH_CREDENTIALS_FILE = 'config/etl-nano-project-v2-oauth-credentials.json'
TOKEN_FILE = 'config/token.json'
GITIGNORE_FILE = '.gitignore'

FORCED_EXCLUDED_FILES = {
    'credentials.json',
    'token.json',
    '.gitignore',
    '.gitattributes',
    '.python-version',
}
FORCED_EXCLUDED_DIRS = {'.git', '.venv', '__pycache__'}


def load_env_file(env_path: Path) -> dict:
    """Đọc file .env theo định dạng KEY=VALUE (không phụ thuộc thư viện ngoài)."""
    values = {}
    if not env_path.exists() or not env_path.is_file():
        raise FileNotFoundError(f"Không tìm thấy file cấu hình: {env_path}")

    for raw_line in env_path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue

        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")

        if key:
            values[key] = value

    return values


def resolve_root_dir(root_dir_value: str, project_root: Path) -> Path:
    """Chuẩn hóa ROOT_DIR, xử lý cả đường dẫn tương đối/tuyệt đối và cấu hình dễ nhầm."""
    raw_value = (root_dir_value or '').strip()
    if not raw_value:
        raise ValueError('Biến GDRIVE_ROOT_DIR đang rỗng trong config/.env')

    if raw_value in {'.', './', project_root.name}:
        return project_root

    candidate = Path(raw_value).expanduser()
    if candidate.is_absolute():
        return candidate.resolve()

    resolved = (project_root / candidate).resolve()
    if resolved.exists():
        return resolved

    # Trường hợp phổ biến: cấu hình trùng tên repo và chạy tại root repo
    if candidate.name == project_root.name:
        return project_root

    return resolved


def load_runtime_config(project_root: Path) -> tuple[str, Path]:
    env_path = project_root / ENV_FILE
    env_values = load_env_file(env_path)

    folder_id = env_values.get('GDRIVE_FOLDER_ID', '').strip()
    root_dir_raw = env_values.get('GDRIVE_ROOT_DIR', '').strip()

    missing_keys = []
    if not folder_id:
        missing_keys.append('GDRIVE_FOLDER_ID')
    if not root_dir_raw:
        missing_keys.append('GDRIVE_ROOT_DIR')

    if missing_keys:
        raise ValueError(
            f"Thiếu cấu hình trong {env_path}: {', '.join(missing_keys)}"
        )

    root_dir = resolve_root_dir(root_dir_raw, project_root)
    return folder_id, root_dir


def authenticate(project_root: Path):
    oauth_credentials_path = (project_root / OAUTH_CREDENTIALS_FILE).resolve()
    token_path = (project_root / TOKEN_FILE).resolve()

    if not oauth_credentials_path.exists() or not oauth_credentials_path.is_file():
        raise FileNotFoundError(
            f"Không tìm thấy OAuth credentials file: {oauth_credentials_path}"
        )

    creds = None
    token_saved = False

    if token_path.exists() and token_path.is_file():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_saved = True

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(oauth_credentials_path),
            SCOPES,
        )
        creds = flow.run_local_server(port=0)
        token_saved = True

    if token_saved:
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json(), encoding='utf-8')
        print(f"Đã lưu token OAuth tại: {token_path}")
    else:
        print(f"Sử dụng token OAuth hiện có tại: {token_path}")

    return build('drive', 'v3', credentials=creds)



def load_gitignore_spec(project_root: Path):
    gitignore_path = project_root / GITIGNORE_FILE
    if not gitignore_path.exists() or not gitignore_path.is_file():
        return pathspec.PathSpec.from_lines('gitwildmatch', [])

    lines = gitignore_path.read_text(encoding='utf-8').splitlines()
    return pathspec.PathSpec.from_lines('gitwildmatch', lines)


def normalize_relative_posix(project_root: Path, file_path: Path) -> str:
    try:
        return file_path.resolve().relative_to(project_root.resolve()).as_posix()
    except ValueError:
        return file_path.name


def classify_skip_reason(project_root: Path, file_path: Path, ignore_spec) -> str | None:
    file_name_lower = file_path.name.lower()
    if file_name_lower in FORCED_EXCLUDED_FILES:
        return f'forced-file:{file_path.name}'

    # Chặn cứng các file .env ngay từ vòng quét đầu tiên
    if file_name_lower == '.env' or file_name_lower.startswith('.env') or file_name_lower.endswith('.env'):
        return f'forced-file:{file_path.name}'

    normalized_posix = normalize_relative_posix(project_root, file_path)
    path_parts = set(Path(normalized_posix).parts)

    for excluded_dir in FORCED_EXCLUDED_DIRS:
        if excluded_dir in path_parts:
            return f'forced-dir:{excluded_dir}'

    if ignore_spec.match_file(normalized_posix):
        return 'gitignore'

    return None


def escape_drive_query_value(value: str) -> str:
    return value.replace("\\", "\\\\").replace("'", "\\'")


def compute_md5(file_path: Path) -> str:
    md5_hash = hashlib.md5()
    with file_path.open('rb') as file_obj:
        while chunk := file_obj.read(8192):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def find_folder_in_drive(service, folder_name: str, parent_id: str) -> str | None:
    escaped_name = escape_drive_query_value(folder_name)
    query = (
        "mimeType='application/vnd.google-apps.folder' "
        f"and name='{escaped_name}' "
        f"and '{parent_id}' in parents and trashed=false"
    )
    result = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id,name)',
        pageSize=1,
    ).execute()
    files = result.get('files', [])
    if not files:
        return None
    return files[0]['id']


def create_folder_in_drive(service, folder_name: str, parent_id: str) -> str:
    metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_id],
    }
    folder = service.files().create(body=metadata, fields='id,name').execute()
    return folder['id']


def ensure_drive_folder_path(
    service,
    root_folder_id: str,
    relative_parent: Path,
    folder_cache: dict[str, str],
    created_folders: list[str],
) -> str:
    if str(relative_parent) in {'.', ''}:
        return root_folder_id

    current_parent_id = root_folder_id
    current_path = Path('.')

    for part in relative_parent.parts:
        current_path = current_path / part
        cache_key = str(current_path)
        if cache_key in folder_cache:
            current_parent_id = folder_cache[cache_key]
            continue

        folder_id = find_folder_in_drive(service, part, current_parent_id)
        if folder_id is None:
            folder_id = create_folder_in_drive(service, part, current_parent_id)
            created_folders.append(cache_key)
            print(f"[Folder Created] {cache_key} -> {folder_id}")
        else:
            print(f"[Folder Exists] {cache_key} -> {folder_id}")

        folder_cache[cache_key] = folder_id
        current_parent_id = folder_id

    return current_parent_id


def find_file_in_drive(service, file_name: str, parent_id: str) -> dict | None:
    escaped_name = escape_drive_query_value(file_name)
    query = (
        f"name='{escaped_name}' and '{parent_id}' in parents and trashed=false"
    )
    result = service.files().list(
        q=query,
        spaces='drive',
        fields='files(id,name,mimeType,md5Checksum,modifiedTime,appProperties)',
        pageSize=1,
    ).execute()
    files = result.get('files', [])
    if not files:
        return None
    return files[0]


def sync_file(service, file_path: Path, parent_folder_id: str) -> tuple[str, str]:
    file_name = file_path.name
    local_md5 = compute_md5(file_path)
    existing_file = find_file_in_drive(service, file_name, parent_folder_id)
    is_markdown = file_path.suffix.lower() == '.md'

    upload_mimetype = 'text/markdown' if is_markdown else (mimetypes.guess_type(str(file_path))[0] or 'application/octet-stream')

    file_metadata = {
        'name': file_name,
        'parents': [parent_folder_id],
        'appProperties': {'local_md5': local_md5},
    }
    if is_markdown:
        file_metadata['mimeType'] = 'application/vnd.google-apps.document'

    media = MediaFileUpload(str(file_path), mimetype=upload_mimetype)

    if existing_file is None:
        created = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id',
        ).execute()
        return 'Created', created['id']

    remote_md5 = existing_file.get('appProperties', {}).get('local_md5')
    if not remote_md5:
        remote_md5 = existing_file.get('md5Checksum')

    if remote_md5 and remote_md5 == local_md5:
        return 'Up-to-date', existing_file['id']

    update_body = {
        'name': file_name,
        'appProperties': {'local_md5': local_md5},
    }
    if is_markdown:
        update_body['mimeType'] = 'application/vnd.google-apps.document'

    updated = service.files().update(
        fileId=existing_file['id'],
        body=update_body,
        media_body=media,
        fields='id',
    ).execute()
    return 'Updated', updated['id']


def main():
    project_root = Path(__file__).resolve().parents[1]

    try:
        folder_id, root = load_runtime_config(project_root)
    except Exception as exc:
        print(f"Lỗi cấu hình: {exc}")
        return

    if not root.exists() or not root.is_dir():
        print(f"ROOT_DIR không hợp lệ hoặc không tồn tại: {root}")
        return

    print(f"ROOT_FOLDER_ID={folder_id}")
    print(f"Đang quét file trong thư mục: {root}")

    try:
        service = authenticate(project_root)
    except Exception as exc:
        print(f"Lỗi xác thực OAuth2: {type(exc).__name__}")
        return

    ignore_spec = load_gitignore_spec(project_root)

    all_files = [
        p for p in root.rglob('*')
        if p.is_file()
    ]

    print(f"Tìm thấy {len(all_files)} file (trước khi lọc)")

    if not all_files:
        print("Không tìm thấy file nào để upload.")
        return

    folder_cache: dict[str, str] = {}
    created_folders: list[str] = []
    sync_results = {
        'Created': 0,
        'Updated': 0,
        'Up-to-date': 0,
        'Skipped': 0,
        'Error': 0,
    }

    # Lọc từ vòng quét ban đầu: chặn ngay file blacklist theo tên + quy tắc .gitignore
    candidate_files: list[Path] = []
    for file_path in sorted(all_files):
        skip_reason = classify_skip_reason(project_root, file_path, ignore_spec)
        relative_path = file_path.relative_to(root)
        if skip_reason:
            sync_results['Skipped'] += 1
            print(f"[Excluded][{skip_reason}] {relative_path}")
            continue
        candidate_files.append(file_path)

    print(f"Số file sau lọc ban đầu: {len(candidate_files)}")

    for file_path in sorted(candidate_files):
        try:
            relative_path = file_path.relative_to(root)

            parent_relative = relative_path.parent
            parent_folder_id = ensure_drive_folder_path(
                service,
                folder_id,
                parent_relative,
                folder_cache,
                created_folders,
            )

            status, file_id = sync_file(service, file_path, parent_folder_id)
            sync_results[status] += 1
            print(f"[{status}] {relative_path} -> ID: {file_id}")
        except Exception as e:
            sync_results['Error'] += 1
            print(f"[Error] {file_path}: {e}")

    print("\n=== TỔNG KẾT ĐỒNG BỘ ===")
    print(f"Created: {sync_results['Created']}")
    print(f"Updated: {sync_results['Updated']}")
    print(f"Up-to-date: {sync_results['Up-to-date']}")
    print(f"Skipped: {sync_results['Skipped']}")
    print(f"Error: {sync_results['Error']}")

    print("\n=== DANH SÁCH THƯ MỤC DRIVE ĐÃ TẠO ===")
    if created_folders:
        for folder in created_folders:
            print(f"- {folder}")
    else:
        print("- Không tạo mới thư mục nào (đã tồn tại hoặc không có thư mục con).")

if __name__ == '__main__':
    main()