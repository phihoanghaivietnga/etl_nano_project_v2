# GEM_CODE_MAP.md

## scripts/upload_to_drive_from_local.py

### Mục tiêu
- Đồng bộ file Markdown từ local lên Google Drive theo cơ chế Diff Sync.
- Đồng bộ cả cấu trúc thư mục local tương ứng trên Drive.

### Hàm chính
- `load_env_file(env_path: Path) -> dict`
  - Đọc cấu hình từ `config/.env`.

- `resolve_root_dir(root_dir_value: str, project_root: Path) -> Path`
  - Chuẩn hóa thư mục gốc quét `.md`.

- `load_runtime_config(project_root: Path) -> tuple[str, Path]`
  - Đọc `GDRIVE_FOLDER_ID`, `GDRIVE_ROOT_DIR`.

- `authenticate(project_root: Path)`
  - Xác thực OAuth2 Desktop.
  - Tái sử dụng/refresh token tại `config/token.json`.

- `escape_drive_query_value(value: str) -> str`
  - Escape query cho Drive API.

- `compute_md5(file_path: Path) -> str`
  - Tính checksum local để so sánh sai khác.

- `find_folder_in_drive(service, folder_name, parent_id) -> str | None`
  - Tìm folder con theo tên + folder cha.

- `create_folder_in_drive(service, folder_name, parent_id) -> str`
  - Tạo folder khi chưa tồn tại.

- `ensure_drive_folder_path(...) -> str`
  - Đảm bảo đường dẫn folder local đã tồn tại trên Drive.
  - Dùng cache giảm query lặp.

- `find_file_in_drive(service, file_name, parent_id) -> dict | None`
  - Tìm file theo tên trong folder cha.

- `sync_markdown_file(service, file_path, parent_folder_id) -> tuple[str, str]`
  - `Created`: file chưa tồn tại trên Drive.
  - `Up-to-date`: checksum giống nhau.
  - `Updated`: checksum khác nhau, thực hiện `update`.
  - Lưu `local_md5` vào `appProperties` để đối soát cho file Google Docs.

- `should_skip_file(project_root, file_path) -> bool`
  - Bỏ qua file nhạy cảm và thư mục không cần sync (`config`, `.venv`).

- `main()`
  - Quét file `.md` trong root (trừ `.git`).
  - Xác thực OAuth2.
  - Đồng bộ thư mục và file theo Diff Sync.
  - In log `Created/Updated/Up-to-date/Skipped/Error` và tổng kết cuối phiên.