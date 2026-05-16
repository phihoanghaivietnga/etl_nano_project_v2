# MASTER_INTERFACE.md

## NHÓM: INTERFACE

## MỤC LỤC NGUỒN
  [DESCRIPTION]: User interface and automation scripts

### main.py - Thành phần giao diện, tiện ích và script vận hành hệ thống
### scripts/upload_to_drive.py - Thành phần giao diện, tiện ích và script vận hành hệ thống
### scripts/upload_to_drive_from_local.py - Thành phần giao diện, tiện ích và script vận hành hệ thống
### src/ui/dashboard_app.py - Thành phần giao diện, tiện ích và script vận hành hệ thống
### src/ui/main_app.py - Thành phần giao diện, tiện ích và script vận hành hệ thống
### src/ui/pages/__init__.py - Thành phần giao diện, tiện ích và script vận hành hệ thống
### src/ui/pages/bao_cao_page.py - Thành phần giao diện, tiện ích và script vận hành hệ thống
### src/ui/pages/common.py - Thành phần giao diện, tiện ích và script vận hành hệ thống
### src/ui/pages/doi_chieu_page.py - Thành phần giao diện, tiện ích và script vận hành hệ thống
### src/ui/pages/job_history_page.py - Thành phần giao diện, tiện ích và script vận hành hệ thống
### src/ui/pages/manual_runner_page.py - Thành phần giao diện, tiện ích và script vận hành hệ thống

## NỘI DUNG GỘP

### SOURCE: main.py
```py
def main():
    print("Hello from etl-nano-project-v2!")


if __name__ == "__main__":
    main()
```

### SOURCE: scripts/upload_to_drive.py
```py
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Cấu hình
SCOPES = ['https://www.googleapis.com/auth/drive.file']
FOLDER_ID = os.environ.get('GDRIVE_FOLDER_ID')
CREDENTIALS_JSON = os.environ.get('GDRIVE_CREDENTIALS')

def authenticate():
	creds_dict = json.loads(CREDENTIALS_JSON)
	return service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)

def upload_files():
	creds = authenticate()
	service = build('drive', 'v3', credentials=creds)

	# Lấy danh sách các file .md trong commit mới nhất (ví dụ đơn giản)
	# Trong thực tế, bạn có thể lọc file dựa trên git log
	files = [f for f in os.listdir('.') if f.endswith('.md')]
	
	for file_name in files:
		file_metadata = {
			'name': file_name,
			'parents': [FOLDER_ID],
			'mimeType': 'application/vnd.google-apps.document'
		}
		media = MediaFileUpload(file_name, mimetype='text/markdown')
		
		file = service.files().create(body=file_metadata, media_body=media).execute()
		print(f'Đã upload thành công: {file_name} với ID: {file.get("id")}')

if __name__ == '__main__':
	upload_files()
```

### SOURCE: scripts/upload_to_drive_from_local.py
```py
#!/usr/bin/env python3
import hashlib
import mimetypes
import shutil
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
TEMP_MERGED_DIR = 'temp_merged'

MASTER_FILE_BY_GROUP = {
    'CORE_LOGIC': 'MASTER_CORE_LOGIC.md',
    'ETL_PROCESS': 'MASTER_ETL_PROCESS.md',
    'INTERFACE': 'MASTER_INTERFACE.md',
    'KNOWLEDGE_BASE': 'MASTER_KNOWLEDGE_BASE.md',
}

# Metadata mô tả ngắn cho từng nhóm
GROUP_DESCRIPTIONS = {
    'CORE_LOGIC': 'Core logic, configuration, and environment settings',
    'ETL_PROCESS': 'ETL job scripts and SQL templates',
    'INTERFACE': 'User interface and automation scripts',
    'KNOWLEDGE_BASE': 'Project documentation and knowledge base',
}

FORCED_EXCLUDED_FILES = {
    'credentials.json',
    'token.json',
    '.gitignore',
}
FORCED_EXCLUDED_DIRS = {'.git', '.venv', '__pycache__'}

# Các tệp chiến lược luôn thuộc KNOWLEDGE_BASE dù nằm ở root
STRATEGIC_FILES = {'agents.md', 'README.md', 'PROJECT_CHRONICLE.md'}

FILE_DESCRIPTION_MAP = {
    'agents.md': 'Định nghĩa cấu hình và chiến lược điều phối các AI Agent trong hệ thống',
    'README.md': 'Tổng quan dự án, kiến trúc thư mục và hướng dẫn sử dụng nhanh',
    'PROJECT_CHRONICLE.md': 'Nhật ký thay đổi hạ tầng, sự cố và quyết định kỹ thuật theo mốc thời gian',
    'docs/knowledge/GEM_NAVIGATION.md': 'Chỉ dẫn điều hướng và tra cứu nhanh các tài liệu tri thức',
    'docs/knowledge/GEM_GUIDE.md': 'Thứ tự ưu tiên đọc tài liệu cho từng loại tác vụ',
    'docs/knowledge/GEM_CODE_MAP.md': 'Bản đồ cấu trúc mã nguồn và quy tắc ánh xạ nhóm',
    'docs/knowledge/GEM_CODE_SNIPPETS.md': 'Thư viện mẫu code chuẩn dùng trong các tình huống phổ biến',
    'docs/knowledge/GEM_DATA_FLOW.md': 'Mô tả luồng dữ liệu từ Production qua Staging tới Datamart',
    'docs/knowledge/GEM_DB_SCHEMAS.md': 'Đặc tả schema và cấu trúc bảng dữ liệu',
    'docs/knowledge/GEM_AUTO_PIPELINE.md': 'Mô tả cơ chế vận hành pipeline tự động',
    'docs/knowledge/GEM_DEPENDENCY_GRAPH.md': 'Đồ thị phụ thuộc giữa module, lớp và quy trình',
    'docs/knowledge/GEM_ERROR_CONTEXT.md': 'Ngữ cảnh lỗi chuẩn hóa và hướng xử lý theo mã lỗi',
    'docs/knowledge/GEM_TECHNICAL_STANDARDS.md': 'Tiêu chuẩn kỹ thuật, bảo mật và xác thực tích hợp',
    'docs/knowledge/GEM_SYNC_WORKFLOW.md': 'Quy trình đồng bộ sai khác và cơ chế Enhanced Merge',
    'docs/knowledge/loop_Gem_Github_GoogleDrive_NotebookLM.md': 'Vòng lặp cộng tác tri thức giữa Gemini, GitHub, Drive và NotebookLM',
}


def load_env_file(env_path: Path) -> dict:
    values = {}
    if not env_path.exists() or not env_path.is_file():
        raise FileNotFoundError(f'Không tìm thấy file cấu hình: {env_path}')

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
        raise ValueError(f"Thiếu cấu hình trong {env_path}: {', '.join(missing_keys)}")

    root_dir = resolve_root_dir(root_dir_raw, project_root)
    return folder_id, root_dir


def authenticate(project_root: Path):
    oauth_credentials_path = (project_root / OAUTH_CREDENTIALS_FILE).resolve()
    token_path = (project_root / TOKEN_FILE).resolve()

    if not oauth_credentials_path.exists() or not oauth_credentials_path.is_file():
        raise FileNotFoundError(f'Không tìm thấy OAuth credentials file: {oauth_credentials_path}')

    creds = None
    token_saved = False

    if token_path.exists() and token_path.is_file():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token_saved = True

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(str(oauth_credentials_path), SCOPES)
        creds = flow.run_local_server(port=0)
        token_saved = True

    if token_saved:
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json(), encoding='utf-8')
        print(f'Đã lưu token OAuth tại: {token_path}')
    else:
        print(f'Sử dụng token OAuth hiện có tại: {token_path}')

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

    normalized_posix = normalize_relative_posix(project_root, file_path)
    path_parts = set(Path(normalized_posix).parts)

    for excluded_dir in FORCED_EXCLUDED_DIRS:
        if excluded_dir in path_parts:
            return f'forced-dir:{excluded_dir}'

    if ignore_spec.match_file(normalized_posix):
        return 'gitignore'

    return None


def escape_drive_query_value(value: str) -> str:
    return value.replace('\\', '\\\\').replace("'", "\\'")


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
            print(f'[Folder Created] {cache_key} -> {folder_id}')
        else:
            print(f'[Folder Exists] {cache_key} -> {folder_id}')

        folder_cache[cache_key] = folder_id
        current_parent_id = folder_id

    return current_parent_id


def find_file_in_drive(service, file_name: str, parent_id: str) -> dict | None:
    escaped_name = escape_drive_query_value(file_name)
    query = f"name='{escaped_name}' and '{parent_id}' in parents and trashed=false"
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


def get_markdown_language(file_path: Path) -> str:
    suffix = file_path.suffix.lower().lstrip('.')
    if suffix in {'py', 'sql', 'md', 'json', 'yml', 'yaml', 'toml', 'txt', 'env', 'sh', 'bat'}:
        return suffix
    return 'text'


def describe_source_file(relative_posix_path: str, group_name: str) -> str:
    normalized = relative_posix_path.strip('/')
    if normalized in FILE_DESCRIPTION_MAP:
        return FILE_DESCRIPTION_MAP[normalized]

    if group_name == 'CORE_LOGIC':
        return 'Thành phần lõi và cấu hình nền tảng của hệ thống ETL'
    if group_name == 'ETL_PROCESS':
        return 'Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ'
    if group_name == 'INTERFACE':
        return 'Thành phần giao diện, tiện ích và script vận hành hệ thống'
    if group_name == 'KNOWLEDGE_BASE':
        return 'Tài liệu tri thức và quy trình vận hành phục vụ cộng tác AI'

    return 'Tệp thành phần của nhóm tri thức'


def classify_group_by_path(relative_posix_path: str) -> str | None:
    """Phân loại file vào nhóm dựa trên đường dẫn vật lý từ root project."""
    normalized = relative_posix_path.strip('/')
    normalized_with_slash = f'/{normalized}/'

    # CORE_LOGIC
    if '/src/core/' in normalized_with_slash or '/config/' in normalized_with_slash or normalized == '.env':
        return 'CORE_LOGIC'

    # ETL_PROCESS
    if '/src/jobs/' in normalized_with_slash or '/src/db/templates/sql/' in normalized_with_slash:
        return 'ETL_PROCESS'

    # INTERFACE
    if '/src/ui/' in normalized_with_slash or '/scripts/' in normalized_with_slash or normalized == 'main.py':
        return 'INTERFACE'

    # KNOWLEDGE_BASE
    if '/docs/knowledge/' in normalized_with_slash or normalized in STRATEGIC_FILES:
        return 'KNOWLEDGE_BASE'

    return None


def build_grouped_file_map(project_root: Path, candidate_files: list[Path]) -> dict[str, list[Path]]:
    grouped: dict[str, list[Path]] = {group: [] for group in MASTER_FILE_BY_GROUP}
    for file_path in candidate_files:
        relative_posix = normalize_relative_posix(project_root, file_path)
        group_name = classify_group_by_path(relative_posix)
        if group_name:
            grouped[group_name].append(file_path)
    return grouped


def build_master_content(project_root: Path, group_name: str, source_files: list[Path]) -> str:
    lines: list[str] = [
        f'# {MASTER_FILE_BY_GROUP[group_name]}',
        '',
        f'## NHÓM: {group_name}',
        '',
        f'## MỤC LỤC NGUỒN',
        f'  [DESCRIPTION]: {GROUP_DESCRIPTIONS.get(group_name, "N/A")}',
        '',
    ]

    if not source_files:
        lines.extend([
            '- Không có tệp nguồn thuộc nhóm này ở lần chạy hiện tại.',
            '',
            '## NỘI DUNG GỘP',
            '',
            'Không có nội dung để gộp.',
        ])
        return '\n'.join(lines) + '\n'

    for source in source_files:
        rel = normalize_relative_posix(project_root, source)
        file_desc = describe_source_file(rel, group_name)
        lines.append(f'### {rel} - {file_desc}')

    lines.extend(['', '## NỘI DUNG GỘP', ''])

    for source in source_files:
        rel = normalize_relative_posix(project_root, source)
        language = get_markdown_language(source)
        try:
            source_content = source.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            source_content = source.read_text(encoding='utf-8', errors='replace')

        lines.extend([
            f'### SOURCE: {rel}',
            f'```{language}',
            source_content.rstrip(),
            '```',
            '',
        ])

    return '\n'.join(lines).rstrip() + '\n'


def generate_master_files(project_root: Path, grouped_files: dict[str, list[Path]]) -> list[Path]:
    temp_merged_path = project_root / TEMP_MERGED_DIR
    if temp_merged_path.exists() and temp_merged_path.is_dir():
        shutil.rmtree(temp_merged_path)
    temp_merged_path.mkdir(parents=True, exist_ok=True)

    master_files: list[Path] = []
    for group_name, master_name in MASTER_FILE_BY_GROUP.items():
        group_sources = sorted(
            grouped_files[group_name],
            key=lambda path: normalize_relative_posix(project_root, path),
        )
        content = build_master_content(project_root, group_name, group_sources)
        master_path = temp_merged_path / master_name
        master_path.write_text(content, encoding='utf-8')
        master_files.append(master_path)
        print(f'[Master Built] {master_path}')

    return master_files


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

    remote_md5 = existing_file.get('md5Checksum')
    if not remote_md5:
        remote_md5 = existing_file.get('appProperties', {}).get('local_md5')

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


def is_in_temp_merged(project_root: Path, file_path: Path) -> bool:
    temp_root = (project_root / TEMP_MERGED_DIR).resolve()
    try:
        file_path.resolve().relative_to(temp_root)
        return True
    except ValueError:
        return False


def main():
    project_root = Path(__file__).resolve().parents[1]

    try:
        folder_id, root = load_runtime_config(project_root)
    except Exception as exc:
        print(f'Lỗi cấu hình: {exc}')
        return

    if not root.exists() or not root.is_dir():
        print(f'ROOT_DIR không hợp lệ hoặc không tồn tại: {root}')
        return

    print(f'\n=== KHỞI ĐỘNG ĐỒNG BỘ ===')
    print(f'ROOT_FOLDER_ID={folder_id}')
    print(f'ROOT_DIR={root}')
    print(f'Đang quét file trong thư mục: {root}')

    try:
        service = authenticate(project_root)
        print(f'Xác thực OAuth2 thành công')
    except Exception as exc:
        print(f'Lỗi xác thực OAuth2: {type(exc).__name__}')
        return

    ignore_spec = load_gitignore_spec(project_root)
    print(f'Đã tải quy tắc .gitignore')

    all_files = [p for p in root.rglob('*') if p.is_file()]
    print(f'Tìm thấy {len(all_files)} file (trước khi lọc)')

    if not all_files:
        print('Không tìm thấy file nào để upload.')
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

    candidate_files: list[Path] = []
    for file_path in sorted(all_files):
        skip_reason = classify_skip_reason(project_root, file_path, ignore_spec)
        relative_path = file_path.relative_to(root)
        if skip_reason:
            sync_results['Skipped'] += 1
            if skip_reason.startswith('forced-file:') or skip_reason.startswith('forced-dir:'):
                print(f'[Excluded][{skip_reason}] {relative_path}')
            elif skip_reason == 'gitignore':
                print(f'[Excluded][gitignore: matched in .gitignore] {relative_path}')
            continue
        candidate_files.append(file_path)

    print(f'\n=== KẾT QUẢ LỌC TỆP ===')
    print(f'Số file sau lọc ban đầu: {len(candidate_files)}')
    print(f'Số file bị loại: {sync_results["Skipped"]}')

    grouped_files = build_grouped_file_map(project_root, candidate_files)
    for group_name, files in grouped_files.items():
        if group_name == 'CORE_LOGIC' and len(files) == 0:
            print(f'[Group CORE_LOGIC]: 0 files (Correct for Infra Phase)')
        else:
            print(f'[Group {group_name}]: {len(files)} file(s)')
    master_files = generate_master_files(project_root, grouped_files)
    upload_files = sorted(candidate_files) + master_files

    master_component_counts = {
        'MASTER_CORE_LOGIC.md': len(grouped_files['CORE_LOGIC']),
        'MASTER_ETL_PROCESS.md': len(grouped_files['ETL_PROCESS']),
        'MASTER_INTERFACE.md': len(grouped_files['INTERFACE']),
        'MASTER_KNOWLEDGE_BASE.md': len(grouped_files['KNOWLEDGE_BASE']),
    }

    print(f'\n=== BẮTĐẦU ĐỐI SOÁT VÀ UPLOAD ===')
    for file_path in upload_files:
        try:
            if is_in_temp_merged(project_root, file_path):
                relative_path = Path(TEMP_MERGED_DIR) / file_path.name
            else:
                relative_path = file_path.relative_to(root)

            parent_relative = relative_path.parent
            parent_folder_id = ensure_drive_folder_path(
                service,
                folder_id,
                parent_relative,
                folder_cache,
                created_folders,
            )

            # Enhanced logging for MD5 check
            local_md5 = compute_md5(file_path)
            existing_file = find_file_in_drive(service, file_path.name, parent_folder_id)

            if existing_file:
                remote_md5 = existing_file.get('md5Checksum')
                if not remote_md5:
                    remote_md5 = existing_file.get('appProperties', {}).get('local_md5')
                if remote_md5 and remote_md5 == local_md5:
                    if relative_path.name == 'MASTER_KNOWLEDGE_BASE.md':
                        comp_count = master_component_counts.get('MASTER_KNOWLEDGE_BASE.md', 0)
                        print(f'[MD5 Match] {relative_path}: Local MD5={local_md5[:8]}..., Remote MD5={remote_md5[:8]}... -> Skipping (aggregated from {comp_count} source files)')
                    else:
                        print(f'[MD5 Match] {relative_path}: Local MD5={local_md5[:8]}..., Remote MD5={remote_md5[:8]}... -> Skipping')
                    sync_results['Up-to-date'] += 1
                    continue
                else:
                    remote_md5_display = remote_md5[:8] if remote_md5 else 'N/A'
                    if relative_path.name == 'MASTER_KNOWLEDGE_BASE.md':
                        comp_count = master_component_counts.get('MASTER_KNOWLEDGE_BASE.md', 0)
                        print(f'[MD5 Mismatch] {relative_path}: Local MD5={local_md5[:8]}..., Remote MD5={remote_md5_display}... -> Updating (aggregated from {comp_count} source files)')
                    else:
                        print(f'[MD5 Mismatch] {relative_path}: Local MD5={local_md5[:8]}..., Remote MD5={remote_md5_display}... -> Updating')
            else:
                print(f'[MD5 New] {relative_path}: New file (Local MD5={local_md5[:8]}...) -> Creating')

            status, file_id = sync_file(service, file_path, parent_folder_id)
            sync_results[status] += 1
            print(f'[{status}] {relative_path} -> ID: {file_id}')
        except Exception as exc:
            sync_results['Error'] += 1
            print(f'[Error] {file_path}: {exc}')

    print('\n=== TỔNG KẾT ĐỒNG BỘ ===')
    total_processed = sum(sync_results.values())
    print(f'Tổng file xử lý: {total_processed}')
    print(f'  - Created: {sync_results["Created"]}')
    print(f'  - Updated: {sync_results["Updated"]}')
    print(f'  - Up-to-date (MD5 match): {sync_results["Up-to-date"]}')
    print(f'  - Skipped (filter): {sync_results["Skipped"]}')
    print(f'  - Error: {sync_results["Error"]}')

    print('\n=== DANH SÁCH THƯ MỤC DRIVE ĐÃ TẠO ===')
    if created_folders:
        for folder in created_folders:
            print(f'- {folder}')
    else:
        print('- Không tạo mới thư mục nào (đã tồn tại hoặc không có thư mục con).')

    print(f'\n=== KẾT THÚC ĐỒNG BỘ ===')
    print(f'Pathspec .gitignore: Áp dụng thành công')


if __name__ == '__main__':
    main()
```

### SOURCE: src/ui/dashboard_app.py
```py
from __future__ import annotations

import asyncio
from decimal import Decimal
from datetime import date
from pathlib import Path
import traceback
from typing import Any

from src.core.base_ui import BaseUI


class DashboardCompareBackend(BaseUI):
    ORDERED_DOMAINS = [
        "dim_benh_nhan",
        "dim_benh",
        "dim_dich_vu",
        "dim_loai_goi_dich_vu",
        "dim_luot_kham",
        "fact_thu_phi_dich_vu",
    ]

    DOMAIN_TITLES = {
        "dim_benh_nhan": "BẢNG ĐỐI CHIẾU BỆNH NHÂN",
        "dim_benh": "BẢNG ĐỐI CHIẾU BỆNH",
        "dim_dich_vu": "BẢNG ĐỐI CHIẾU DỊCH VỤ",
        "dim_loai_goi_dich_vu": "BẢNG ĐỐI CHIẾU LOẠI GÓI DỊCH VỤ",
        "dim_luot_kham": "BẢNG ĐỐI CHIẾU LƯỢT KHÁM",
        "fact_thu_phi_dich_vu": "BẢNG ĐỐI CHIẾU DOANH THU",
    }

    FACT_REQUIRED_METRICS = ["RowCount", "TongTien", "TongTienSauTangGiam"]

    def __init__(self) -> None:
        super().__init__(page_title="", navigation_items=[])
        self.sql_root = Path("src/db/templates/sql/dashboard_doichieu")

    @staticmethod
    def _build_params(marker_count: int, from_date: date, to_date: date) -> tuple[Any, ...]:
        if marker_count == 0:
            return tuple()
        pair = (from_date, to_date)
        params: list[Any] = []
        while len(params) < marker_count:
            params.extend(pair)
        return tuple(params[:marker_count])

    @staticmethod
    def _ensure_marker_consistency(sql_list: list[str]) -> int:
        counts = {sql.count("?") for sql in sql_list}
        if len(counts) != 1:
            raise ValueError("Ba file SQL trong cùng domain phải có cùng số lượng marker '?'")
        return counts.pop()

    @staticmethod
    def _merge_numeric(total: dict[str, float], row: dict[str, Any]) -> dict[str, float]:
        for key, value in row.items():
            if value is None:
                total[key] = total.get(key, 0.0)
                continue
            if isinstance(value, (int, float, Decimal)):
                total[key] = total.get(key, 0.0) + float(value)
        return total

    @staticmethod
    def _normalize_metric_map(values: dict[str, Any]) -> dict[str, float]:
        normalized: dict[str, float] = {}
        for key, value in values.items():
            if value is None:
                normalized[key] = 0.0
            elif isinstance(value, (int, float, Decimal)):
                normalized[key] = float(value)
        return normalized

    @classmethod
    def _resolve_metrics(cls, domain_name: str, source_maps: list[dict[str, float]]) -> list[str]:
        metrics: list[str] = []
        for source_map in source_maps:
            for key in source_map:
                if key not in metrics:
                    metrics.append(key)

        if domain_name == "fact_thu_phi_dich_vu":
            for metric in cls.FACT_REQUIRED_METRICS:
                if metric not in metrics:
                    metrics.append(metric)
        else:
            metrics = ["RowCount"]

        return metrics

    @staticmethod
    def _build_rows_by_source(
        metrics: list[str],
        production_values: dict[str, float],
        staging_values: dict[str, float],
        datamart_values: dict[str, float],
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        source_items = [
            ("Production", production_values),
            ("Staging", staging_values),
            ("DataMart", datamart_values),
        ]
        for source_name, source_values in source_items:
            row: dict[str, Any] = {"Nguon": source_name}
            for metric in metrics:
                row[metric] = source_values.get(metric, 0.0)
            rows.append(row)
        return rows

    async def _aggregate_production(self, production_sql: str, params: tuple[Any, ...]) -> dict[str, Any]:
        prod_vars = self.get_production_connection_vars()
        if not prod_vars:
            raise ValueError("Không tìm thấy biến kết nối nào theo mẫu PROD_CONNECTION_*")

        tasks = [
            self.execute_query_async(prod_var, production_sql, params)
            for prod_var in prod_vars
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        errors: list[str] = []
        aggregated: dict[str, float] = {}
        for prod_var, result in zip(prod_vars, results, strict=False):
            if isinstance(result, Exception):
                try:
                    raise result
                except Exception:
                    traceback.print_exc()
                errors.append(f"{prod_var}: {result}")
                continue
            if result:
                self._merge_numeric(aggregated, result[0])

        return {"values": aggregated, "errors": errors}

    async def _aggregate_staging(self, staging_sql_template: str, params: tuple[Any, ...]) -> dict[str, Any]:
        staging_schemas = self.get_staging_schemas()
        tasks = [
            self.execute_query_async(
                "DATAMART_CONNECTION_STRING",
                staging_sql_template.format(staging_schema=schema),
                params,
            )
            for schema in staging_schemas
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        errors: list[str] = []
        aggregated: dict[str, float] = {}
        for schema, result in zip(staging_schemas, results, strict=False):
            if isinstance(result, Exception):
                try:
                    raise result
                except Exception:
                    traceback.print_exc()
                errors.append(f"{schema}: {result}")
                continue
            if result:
                self._merge_numeric(aggregated, result[0])

        return {"values": aggregated, "errors": errors}

    async def compare_domain(self, domain_name: str, from_date: date, to_date: date) -> dict[str, Any]:
        domain_path = self.sql_root / domain_name
        production_sql = self.read_sql_template(domain_path / "production.sql")
        staging_sql = self.read_sql_template(domain_path / "staging.sql")
        datamart_sql = self.read_sql_template(domain_path / "datamart.sql")

        marker_count = self._ensure_marker_consistency([production_sql, staging_sql, datamart_sql])
        params = self._build_params(marker_count, from_date, to_date)

        prod_task = self._aggregate_production(production_sql, params)
        stg_task = self._aggregate_staging(staging_sql, params)
        dm_task = self.execute_query_async("DATAMART_CONNECTION_STRING", datamart_sql, params)

        prod_result, stg_result, dm_result = await asyncio.gather(
            prod_task,
            stg_task,
            dm_task,
            return_exceptions=True,
        )

        production_values: dict[str, float] = {}
        staging_values: dict[str, float] = {}
        datamart_values: dict[str, float] = {}
        errors: dict[str, str] = {"Production": "", "Staging": "", "DataMart": ""}

        if isinstance(prod_result, Exception):
            try:
                raise prod_result
            except Exception:
                traceback.print_exc()
            errors["Production"] = str(prod_result)
        else:
            production_values = self._normalize_metric_map(prod_result.get("values", {}))
            errors["Production"] = "; ".join(prod_result.get("errors", []))

        if isinstance(stg_result, Exception):
            try:
                raise stg_result
            except Exception:
                traceback.print_exc()
            errors["Staging"] = str(stg_result)
        else:
            staging_values = self._normalize_metric_map(stg_result.get("values", {}))
            errors["Staging"] = "; ".join(stg_result.get("errors", []))

        if isinstance(dm_result, Exception):
            try:
                raise dm_result
            except Exception:
                traceback.print_exc()
            errors["DataMart"] = str(dm_result)
        else:
            dm_data = dm_result[0] if dm_result else {}
            datamart_values = self._normalize_metric_map(dm_data)

        metrics = self._resolve_metrics(
            domain_name,
            [production_values, staging_values, datamart_values],
        )
        rows = self._build_rows_by_source(metrics, production_values, staging_values, datamart_values)
        columns = ["Nguon", *metrics]

        return {
            "domain": domain_name,
            "title": self.DOMAIN_TITLES.get(domain_name, domain_name.upper()),
            "columns": columns,
            "rows": rows,
            "errors": errors,
        }

    async def compare_all(self, from_date: date, to_date: date) -> list[dict[str, Any]]:
        domains = self.ORDERED_DOMAINS
        tasks = [self.compare_domain(domain, from_date, to_date) for domain in domains]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        rows: list[dict[str, Any]] = []
        for domain, result in zip(domains, results, strict=False):
            if isinstance(result, Exception):
                try:
                    raise result
                except Exception:
                    traceback.print_exc()
                rows.append(
                    {
                        "domain": domain,
                        "title": self.DOMAIN_TITLES.get(domain, domain.upper()),
                        "columns": ["Nguon", "RowCount"],
                        "rows": [
                            {"Nguon": "Production", "RowCount": 0.0},
                            {"Nguon": "Staging", "RowCount": 0.0},
                            {"Nguon": "DataMart", "RowCount": 0.0},
                        ],
                        "errors": {"Production": str(result), "Staging": "", "DataMart": ""},
                    }
                )
            else:
                rows.append(result)
        return rows
```

### SOURCE: src/ui/main_app.py
```py
from __future__ import annotations

import os

from dotenv import load_dotenv
from nicegui import app, ui

from src.ui.pages import bao_cao_page, doi_chieu_page, job_history_page, manual_runner_page


load_dotenv("config/.env", override=False)


def resolve_ui_port() -> int:
    raw_port = os.getenv("UI_PORT", "9005")
    try:
        port = int(raw_port)
        return port if port > 0 else 9005
    except (TypeError, ValueError):
        return 9005


@app.get("/api/health")
def api_health() -> dict[str, str]:
    return {
        "name": "ETL Nano V2 API",
        "version": "1.0.0",
        "status": "running",
    }


@ui.page("/")
def index_page() -> None:
    ui.navigate.to("/doi-chieu")


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="ETL Dashboard Đối chiếu V2",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=resolve_ui_port(),
        reload=False,
    )
```

### SOURCE: src/ui/pages/__init__.py
```py
from src.ui.pages import bao_cao_page, doi_chieu_page, job_history_page, manual_runner_page

__all__ = [
    "bao_cao_page",
    "doi_chieu_page",
    "job_history_page",
    "manual_runner_page",
]
```

### SOURCE: src/ui/pages/bao_cao_page.py
```py
from __future__ import annotations

from nicegui import ui

from src.core.base_ui import BaseUI
from src.ui.pages.common import NAV_ITEMS


class BaoCaoPage(BaseUI):
    def __init__(self) -> None:
        super().__init__(page_title="Dashboard ETL - Báo cáo", navigation_items=NAV_ITEMS)

    def render(self) -> None:
        self.build_layout(active_route="/bao-cao")
        with ui.column().classes("w-full p-4 gap-3"):
            ui.label("Màn hình 4 - Báo cáo").classes("text-xl font-semibold")
            with ui.card().classes("w-full h-96 bg-white"):
                ui.label("Khung trắng chuẩn bị tích hợp logic báo cáo từ V1").classes("text-slate-500")


@ui.page("/bao-cao")
def bao_cao_route() -> None:
    page = BaoCaoPage()
    page.render()
```

### SOURCE: src/ui/pages/common.py
```py
from __future__ import annotations

from dataclasses import dataclass


NAV_ITEMS: list[tuple[str, str]] = [
    ("/doi-chieu", "Đối chiếu kết quả"),
    ("/manual-runner", "Chạy Job ETL thủ công"),
    ("/job-history", "Lịch sử chạy Job"),
    ("/bao-cao", "Báo cáo"),
]


@dataclass
class JobHistoryRecord:
    thoi_gian: str
    ten_bang: str
    tu_ngay: str
    den_ngay: str
    trang_thai: str
    chi_tiet: str


class JobHistoryStore:
    records: list[JobHistoryRecord] = []

    @classmethod
    def add_record(cls, record: JobHistoryRecord) -> None:
        cls.records.insert(0, record)
```

### SOURCE: src/ui/pages/doi_chieu_page.py
```py
from __future__ import annotations

from datetime import date, datetime
from typing import Any

from nicegui import ui

from src.core.base_ui import BaseUI
from src.ui.dashboard_app import DashboardCompareBackend
from src.ui.pages.common import NAV_ITEMS


class DoiChieuPage(BaseUI):
    def __init__(self) -> None:
        super().__init__(page_title="Dashboard ETL - Đối chiếu kết quả", navigation_items=NAV_ITEMS)
        self.from_date = date.today().replace(day=1)
        self.to_date = date.today()
        self.result_container: ui.column | None = None
        self.backend = DashboardCompareBackend()

    @staticmethod
    def _to_native_date(value: Any) -> date:
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            if "-" in value:
                return datetime.strptime(value, "%Y-%m-%d").date()
            return datetime.strptime(value, "%Y%m%d").date()
        raise ValueError(f"Không parse được ngày: {value}")

    def _on_from_date_change(self, value: Any) -> None:
        self.from_date = self._to_native_date(value)

    def _on_to_date_change(self, value: Any) -> None:
        self.to_date = self._to_native_date(value)

    @staticmethod
    def _build_table_columns(keys: list[str]) -> list[dict[str, Any]]:
        return [{"name": key, "label": key, "field": key, "align": "left"} for key in keys]

    def _render_domain_card(self, domain_result: dict[str, Any]) -> None:
        if self.result_container is None:
            return
        with self.result_container:
            with ui.card().classes("w-full"):
                ui.label(domain_result.get("title", "BẢNG ĐỐI CHIẾU")).classes("text-base font-semibold")
                table_columns = self._build_table_columns(domain_result.get("columns", []))
                table_rows = domain_result.get("rows", [])
                ui.table(columns=table_columns, rows=table_rows).classes("w-full")

                errors = domain_result.get("errors", {})
                for source in ["Production", "Staging", "DataMart"]:
                    error_text = (errors.get(source, "") or "").strip()
                    if error_text:
                        ui.label(f"{source}: {error_text}").classes("text-red-600 text-sm")

    async def run_compare_all(self) -> None:
        try:
            if self.result_container is not None:
                self.result_container.clear()

            results = await self.backend.compare_all(self.from_date, self.to_date)
            for domain_result in results:
                self._render_domain_card(domain_result)

            ui.notify("Đã chạy đối chiếu toàn bộ", color="positive")
        except Exception as exc:
            ui.notify(f"Lỗi đối chiếu: {exc}", color="negative")

    def render(self) -> None:
        self.build_layout(active_route="/doi-chieu")
        with ui.column().classes("w-full p-4 gap-4"):
            ui.label("Màn hình 1 - Đối chiếu kết quả").classes("text-xl font-semibold")
            with ui.row().classes("items-end gap-4"):
                ui.date(value=self.from_date.isoformat(), on_change=lambda e: self._on_from_date_change(e.value)).props(
                    "label=Từ ngày"
                )
                ui.date(value=self.to_date.isoformat(), on_change=lambda e: self._on_to_date_change(e.value)).props(
                    "label=Đến ngày"
                )
                ui.button("Chạy đối chiếu toàn bộ", on_click=self.run_compare_all, color="primary")

            with ui.scroll_area().classes("w-full h-[70vh]"):
                self.result_container = ui.column().classes("w-full gap-4")


@ui.page("/doi-chieu")
def doi_chieu_route() -> None:
    page = DoiChieuPage()
    page.render()
```

### SOURCE: src/ui/pages/job_history_page.py
```py
from __future__ import annotations

from nicegui import ui

from src.core.base_ui import BaseUI
from src.ui.pages.common import JobHistoryStore, NAV_ITEMS


class JobHistoryPage(BaseUI):
    def __init__(self) -> None:
        super().__init__(page_title="Dashboard ETL - Lịch sử chạy Job", navigation_items=NAV_ITEMS)

    def render(self) -> None:
        self.build_layout(active_route="/job-history")
        with ui.column().classes("w-full p-4 gap-3"):
            ui.label("Màn hình 3 - Lịch sử chạy Job").classes("text-xl font-semibold")
            with ui.card().classes("w-full"):
                with ui.column().classes("w-full gap-2"):
                    if not JobHistoryStore.records:
                        ui.label("Chưa có bản ghi lịch sử").classes("text-slate-500")
                    else:
                        for record in JobHistoryStore.records:
                            status_class = "text-green-600" if record.trang_thai == "Success" else "text-red-600"
                            with ui.row().classes("w-full justify-between border-b pb-2"):
                                ui.label(f"{record.thoi_gian} | {record.ten_bang} | {record.tu_ngay} -> {record.den_ngay}")
                                ui.label(record.trang_thai).classes(f"font-semibold {status_class}")
                            ui.label(record.chi_tiet).classes("text-xs text-slate-600")


@ui.page("/job-history")
def job_history_route() -> None:
    page = JobHistoryPage()
    page.render()
```

### SOURCE: src/ui/pages/manual_runner_page.py
```py
from __future__ import annotations

import asyncio
from datetime import date, datetime
from typing import Any

from nicegui import run, ui

from src.core.base_loader import GenericTableLoader
from src.core.base_ui import BaseUI
from src.ui.pages.common import JobHistoryRecord, JobHistoryStore, NAV_ITEMS


TABLE_MERGE_TEMPLATE: dict[str, str] = {
    "HoSoKhamBenhNgoaiTru": "src/db/templates/sql/fact/DimLuotKham_merge.sql",
    "DoThiLuc": "src/db/templates/sql/fact/FactDoThiLuc_merge.sql",
    "ThuPhiGoi": "src/db/templates/sql/fact/FactThuPhiDichVu_ThuPhiGoi_merge.sql",
}


class ManualRunnerPage(BaseUI):
    def __init__(self) -> None:
        super().__init__(page_title="Dashboard ETL - Chạy Job thủ công", navigation_items=NAV_ITEMS)
        self.from_date = date.today().replace(day=1)
        self.to_date = date.today()
        self.selected_table = "HoSoKhamBenhNgoaiTru"
        self.log_queue: asyncio.Queue[str] = asyncio.Queue()
        self.log_panel: ui.log | None = None
        self.run_button: ui.button | None = None

    @staticmethod
    def _to_native_date(value: Any) -> date:
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            if "-" in value:
                return datetime.strptime(value, "%Y-%m-%d").date()
            return datetime.strptime(value, "%Y%m%d").date()
        raise ValueError(f"Không parse được ngày: {value}")

    async def _consume_log_queue(self) -> None:
        while True:
            message = await self.log_queue.get()
            if self.log_panel is not None:
                self.log_panel.push(message)
            if message == "[DONE]":
                break

    def _on_from_date_change(self, value: Any) -> None:
        self.from_date = self._to_native_date(value)

    def _on_to_date_change(self, value: Any) -> None:
        self.to_date = self._to_native_date(value)

    async def run_job(self) -> None:
        loop = asyncio.get_running_loop()
        if self.run_button is not None:
            self.run_button.disable()

        connection_string = self.get_env("DATAMART_CONNECTION_STRING")
        merge_template = TABLE_MERGE_TEMPLATE.get(self.selected_table)
        if not connection_string:
            ui.notify("Thiếu DATAMART_CONNECTION_STRING, chưa thể chạy job", color="negative")
            if self.run_button is not None:
                self.run_button.enable()
            return

        self.log_queue = asyncio.Queue()
        consumer_task = asyncio.create_task(self._consume_log_queue())
        from_date_native = self._to_native_date(self.from_date)
        to_date_native = self._to_native_date(self.to_date)

        loader = GenericTableLoader(
            connection_string=connection_string,
            table_name=self.selected_table,
            merge_sql_path=merge_template,
        )

        try:
            await run.io_bound(
                loader.execute_load,
                from_date_native,
                to_date_native,
                queue=self.log_queue,
                loop=loop,
            )
            await consumer_task
            JobHistoryStore.add_record(
                JobHistoryRecord(
                    thoi_gian=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ten_bang=self.selected_table,
                    tu_ngay=from_date_native.strftime("%Y%m%d"),
                    den_ngay=to_date_native.strftime("%Y%m%d"),
                    trang_thai="Success",
                    chi_tiet="Job hoàn tất và commit thành công",
                )
            )
            ui.notify("Run Job thành công", color="positive")
        except Exception as exc:
            await consumer_task
            JobHistoryStore.add_record(
                JobHistoryRecord(
                    thoi_gian=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ten_bang=self.selected_table,
                    tu_ngay=from_date_native.strftime("%Y%m%d"),
                    den_ngay=to_date_native.strftime("%Y%m%d"),
                    trang_thai="Failed",
                    chi_tiet=str(exc),
                )
            )
            ui.notify(f"Run Job thất bại: {exc}", color="negative")
        finally:
            if self.run_button is not None:
                self.run_button.enable()

    def render(self) -> None:
        self.build_layout(active_route="/manual-runner")
        with ui.column().classes("w-full p-4 gap-4"):
            ui.label("Màn hình 2 - Chạy Job ETL thủ công").classes("text-xl font-semibold")
            with ui.row().classes("items-end gap-4"):
                ui.select(
                    list(TABLE_MERGE_TEMPLATE.keys()),
                    value=self.selected_table,
                    on_change=lambda e: setattr(self, "selected_table", e.value),
                    label="Chọn bảng lõi",
                )
                ui.date(value=self.from_date.isoformat(), on_change=lambda e: self._on_from_date_change(e.value)).props(
                    "label=Từ ngày"
                )
                ui.date(value=self.to_date.isoformat(), on_change=lambda e: self._on_to_date_change(e.value)).props(
                    "label=Đến ngày"
                )
                self.run_button = ui.button("Run Job", on_click=self.run_job, color="primary")
            self.log_panel = ui.log().classes("w-full h-72 bg-black text-green-400")


@ui.page("/manual-runner")
def manual_runner_route() -> None:
    page = ManualRunnerPage()
    page.render()
```
