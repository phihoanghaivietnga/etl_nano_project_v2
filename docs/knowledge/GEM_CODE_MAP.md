# GEM_CODE_MAP.md

## scripts/upload_to_drive_from_local.py

### Mục tiêu
- Đồng bộ toàn bộ file Markdown từ máy local lên Google Drive (định dạng Google Docs).

### Cấu trúc hàm chính
- `load_env_file(env_path: Path) -> dict`
  - Đọc cấu hình từ `config/.env` theo định dạng `KEY=VALUE`.
  - Bỏ qua dòng rỗng, comment và giá trị không hợp lệ.

- `resolve_root_dir(root_dir_value: str, project_root: Path) -> Path`
  - Chuẩn hóa thư mục gốc quét `.md`.
  - Hỗ trợ các trường hợp cấu hình `.` / `./` / trùng tên repo.
  - Tránh lỗi resolve sai thành đường dẫn lồng `.../etl_nano_project_v2/etl_nano_project_v2`.

- `load_runtime_config(project_root: Path) -> tuple[str, str, Path]`
  - Nạp 3 biến bắt buộc từ `config/.env`:
    - `GDRIVE_CREDENTIALS_FILE`
    - `GDRIVE_FOLDER_ID`
    - `GDRIVE_ROOT_DIR`
  - Kiểm tra thiếu biến và tồn tại file credentials.

- `authenticate(creds_file: str)`
  - Xác thực Google Service Account với scope `drive.file`.

- `upload_file(service, file_path: Path, folder_id: str) -> str`
  - Upload một file `.md` lên Drive và chuyển đổi thành Google Docs.

- `main()`
  - Xác định `project_root` theo vị trí file script.
  - Nạp cấu hình từ `config/.env`.
  - Kiểm tra hợp lệ thư mục gốc quét.
  - Quét toàn bộ `.md` bằng `rglob('*.md')`, loại trừ `.git`.
  - In số lượng file tìm thấy và upload tuần tự.