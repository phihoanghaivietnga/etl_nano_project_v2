#!/usr/bin/env python3
from pathlib import Path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Quản lý Drive: chỉ tạo/ghi mới từ app (không full-access toàn Drive)
SCOPES = ['https://www.googleapis.com/auth/drive.file']
ENV_FILE = 'config/.env'


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


def load_runtime_config(project_root: Path) -> tuple[str, str, Path]:
    env_path = project_root / ENV_FILE
    env_values = load_env_file(env_path)

    credentials_file = env_values.get('GDRIVE_CREDENTIALS_FILE', '').strip()
    folder_id = env_values.get('GDRIVE_FOLDER_ID', '').strip()
    root_dir_raw = env_values.get('GDRIVE_ROOT_DIR', '').strip()

    missing_keys = []
    if not credentials_file:
        missing_keys.append('GDRIVE_CREDENTIALS_FILE')
    if not folder_id:
        missing_keys.append('GDRIVE_FOLDER_ID')
    if not root_dir_raw:
        missing_keys.append('GDRIVE_ROOT_DIR')

    if missing_keys:
        raise ValueError(
            f"Thiếu cấu hình trong {env_path}: {', '.join(missing_keys)}"
        )

    credentials_path = Path(credentials_file).expanduser()
    if not credentials_path.is_absolute():
        credentials_path = (project_root / credentials_path).resolve()
    else:
        credentials_path = credentials_path.resolve()

    if not credentials_path.exists() or not credentials_path.is_file():
        raise FileNotFoundError(
            f"Không tìm thấy file credentials: {credentials_path}"
        )

    root_dir = resolve_root_dir(root_dir_raw, project_root)
    return str(credentials_path), folder_id, root_dir

def authenticate(creds_file: str):
    creds = service_account.Credentials.from_service_account_file(creds_file, scopes=SCOPES)
    return build('drive', 'v3', credentials=creds)

def upload_file(service, file_path: Path, folder_id: str) -> str:
    file_name = file_path.name
    file_metadata = {
        'name': file_name,
        'parents': [folder_id],
        'mimeType': 'application/vnd.google-apps.document'
    }
    media = MediaFileUpload(str(file_path), mimetype='text/markdown')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

def main():
    project_root = Path(__file__).resolve().parents[1]

    try:
        credentials_file, folder_id, root = load_runtime_config(project_root)
    except Exception as exc:
        print(f"Lỗi cấu hình: {exc}")
        return

    if not root.exists() or not root.is_dir():
        print(f"ROOT_DIR không hợp lệ hoặc không tồn tại: {root}")
        return

    print(f"Đang quét file .md trong thư mục: {root}")

    service = authenticate(credentials_file)

    # Thu thập tất cả file .md trong root và các thư mục con, bỏ qua thư mục .git
    md_files = [
        p for p in root.rglob('*.md')
        if p.is_file() and '.git' not in p.parts
    ]

    print(f"Tìm thấy {len(md_files)} file .md")

    if not md_files:
        print("Không tìm thấy file .md để upload.")
        return

    for file_path in sorted(md_files):
        try:
            file_id = upload_file(service, file_path, folder_id)
            print(f"Uploaded: {file_path} -> ID: {file_id}")
        except Exception as e:
            print(f"ERROR uploading {file_path}: {e}")

if __name__ == '__main__':
    main()