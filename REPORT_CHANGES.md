# REPORT_CHANGES.md

## Phạm vi cập nhật mới (Diff Sync local -> Drive)
- File chính: `scripts/upload_to_drive_from_local.py`
- Tri thức: `docs/knowledge/GEM_SYNC_WORKFLOW.md`, `docs/knowledge/GEM_CODE_MAP.md`
- Tài liệu tổng quan: `agents.md`, `README.md`
- Prompt báo cáo: `docs/prompts/20260508_1330_change_upload_from_local_v1.md`

## Nội dung thay đổi chính

### 1) Tái cấu trúc đồng bộ thư mục trên Drive
- Bổ sung các hàm:
  - `find_folder_in_drive()`
  - `create_folder_in_drive()`
  - `ensure_drive_folder_path()`
- Cơ chế:
  - Kiểm tra thư mục đã tồn tại thì tái sử dụng ID.
  - Nếu chưa tồn tại thì tạo mới.
  - Dùng cache folder ID để giảm query lặp và tăng hiệu năng.

### 2) Triển khai Diff Sync thay vì upload create toàn bộ
- Thay thế logic upload cũ bằng hàm `sync_markdown_file()`:
  - Search file theo `name + parent folder id`.
  - Nếu chưa tồn tại: `create` -> trạng thái `Created`.
  - Nếu tồn tại: so sánh checksum local với checksum lưu trên Drive.
  - Nếu không đổi: `Up-to-date` (bỏ qua upload).
  - Nếu đổi: `update` -> trạng thái `Updated`.

### 3) Cơ chế checksum cho Google Docs
- Vì file Google Docs thường không có `md5Checksum` nguồn, script lưu `local_md5` vào `appProperties`.
- Lần chạy sau dùng `appProperties.local_md5` để xác định file có thay đổi hay không.

### 4) Tối ưu hiệu suất
- Chỉ upload khi file thay đổi (`Updated`) hoặc chưa tồn tại (`Created`).
- Bỏ qua file không đổi (`Up-to-date`).
- Giảm thời gian chạy nhờ cache folder và skip file không cần sync.

### 5) Bảo mật thông tin
- Loại trừ đồng bộ các file nhạy cảm:
  - `config/token.json`
  - `config/etl-nano-project-v2-oauth-credentials.json`
  - `config/.env`
- Loại trừ toàn bộ thư mục `config/` và `.venv/` khỏi luồng upload.

### 6) Log đối soát
- Script in log từng file theo trạng thái:
  - `Created`
  - `Updated`
  - `Up-to-date`
  - `Skipped`
  - `Error`
- In tổng kết cuối phiên và danh sách thư mục Drive đã tạo mới.

## Cập nhật tri thức và tài liệu
- Tạo mới `GEM_SYNC_WORKFLOW.md` mô tả quy trình Diff Sync.
- Cập nhật `GEM_CODE_MAP.md` theo cấu trúc hàm mới.
- Bổ sung mục đích `GEM_SYNC_WORKFLOW.md` vào:
  - `agents.md`
  - `README.md`
  (chỉ thêm, không xóa thông tin cũ theo yêu cầu).