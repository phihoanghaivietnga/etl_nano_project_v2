# GEM_SYNC_WORKFLOW.md

## Mục tiêu
- Chuẩn hóa quy trình đồng bộ sai khác (Diff Sync) từ local lên Google Drive.
- Giảm thời gian vận hành bằng cách chỉ cập nhật file có thay đổi.

## Phạm vi áp dụng
- Script: `scripts/upload_to_drive_from_local.py`
- Kiểu tệp: `.md`
- Đích: Google Drive (chuyển đổi sang Google Docs)

## Luồng đồng bộ chuẩn

### Bước 1: Quét dữ liệu local
- Quét đệ quy tất cả `.md` từ `GDRIVE_ROOT_DIR`.
- Loại trừ `.git`.
- Loại trừ toàn bộ `config/` để tránh đẩy nhầm token/credentials.

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
- Nếu có file:
  - So sánh MD5 local và `md5Checksum` remote.
  - Nếu giống nhau: bỏ qua upload, trạng thái `Up-to-date`.
  - Nếu khác nhau: cập nhật (`update`), trạng thái `Updated`.

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