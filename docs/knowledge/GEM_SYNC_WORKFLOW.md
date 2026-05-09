# GEM_SYNC_WORKFLOW.md

## Mục tiêu
- Chuẩn hóa quy trình đồng bộ sai khác (Diff Sync) từ local lên Google Drive.
- Giảm thời gian vận hành bằng cách chỉ cập nhật file có thay đổi.

## Phạm vi áp dụng
- Script: `scripts/upload_to_drive_from_local.py`
- Kiểu tệp: toàn bộ file hợp lệ theo quy tắc lọc
- Đích: Google Drive (Markdown chuyển Google Docs, các tệp khác giữ định dạng gốc)

## Luồng đồng bộ chuẩn

### Bước 1: Quét dữ liệu local
- Quét đệ quy tất cả file từ `GDRIVE_ROOT_DIR`.
- Áp dụng lọc `.gitignore` bằng `pathspec`.
- Loại trừ bắt buộc (dù có/không có trong `.gitignore`):
  - File: `credentials.json`, `token.json`
  - Thư mục: `.git`, `.venv`, `__pycache__`
- Log file bị loại trừ theo dạng `[Skipped][reason]`.

## Danh sách các tệp không đồng bộ

### Nhóm loại trừ theo tên (blacklist cứng)
- `.gitignore`
- `.gitattributes`
- `.python-version`
- `credentials.json`
- `token.json`
- Các tệp `.env` (ví dụ: `.env`, `.env.local`, `prod.env`)

### Nhóm loại trừ theo thư mục
- `.git`
- `.venv`
- `__pycache__`

### Nhóm loại trừ theo quy tắc `.gitignore`
- Mọi tệp/thư mục khớp mẫu trong `.gitignore` tại root dự án.

### Lý do không đồng bộ các tệp cấu hình hệ thống
- Tránh lộ thông tin nhạy cảm (token, credentials, biến môi trường).
- Tránh đồng bộ các tệp phục vụ môi trường cục bộ hoặc kiểm soát phiên bản.
- Giảm nhiễu dữ liệu trên Drive và tăng tốc độ đồng bộ.

### Bước 2: Đồng bộ cấu trúc thư mục
- Từ đường dẫn tương đối của mỗi file, dựng cây thư mục trên Drive.
- Với từng cấp thư mục:
  - Nếu đã tồn tại trong parent: tái sử dụng folder ID.
  - Nếu chưa tồn tại: tạo mới và lưu lại folder ID.
- Dùng cache folder để giảm số lần query API.

### Bước 3: Diff Sync cho từng file
- Tìm file trên Drive theo `name + parent folder id`.
- Nếu không có file:
  - Tạo mới (`create`) và trạng thái `Created`.
  - Với `.md`: tạo dưới dạng Google Docs (`mimeType='application/vnd.google-apps.document'`).
  - Với tệp khác: upload dạng tệp gốc (Media Upload).
- Nếu có file:
  - Tính MD5 local bằng `hashlib`.
  - So sánh theo thứ tự:
    - `appProperties.local_md5` (ưu tiên)
    - `md5Checksum` của file Drive (fallback)
  - Nếu giống nhau: bỏ qua upload, trạng thái `Up-to-date`.
  - Nếu khác nhau: cập nhật (`update`), trạng thái `Updated`.

### Bước 3.1: Chính sách checksum theo định dạng
- `.md` (Google Docs): dùng `appProperties.local_md5` để đối soát ổn định.
- File gốc (py/sql/yml/yaml/...): ưu tiên `md5Checksum` của Drive, đồng thời lưu `appProperties.local_md5` để thống nhất cơ chế.

### Bước 4: Ghi log đối soát
- Log theo từng file với 1 trong các trạng thái:
  - `Created`
  - `Updated`
  - `Up-to-date`
  - `Skipped`
  - `Error`
- In tổng kết cuối phiên đồng bộ.
- In danh sách thư mục Drive đã tạo mới để kiểm tra tính thống nhất với local.

## Quy tắc bảo mật
- Token OAuth và credentials phải nằm trong `config/`.
- Không đồng bộ file nhạy cảm:
  - `config/token.json`
  - `config/etl-nano-project-v2-oauth-credentials.json`
  - `config/.env`
- Không log nội dung token/secret.

## Tiêu chí hoàn thành
- Script nhận diện đúng file không đổi (`Up-to-date`).
- Script chỉ `update` file thay đổi và `create` file mới.
- Cấu trúc thư mục trên Drive khớp với local theo đường dẫn tương đối.