# REPORT_CHANGES.md

## Phạm vi cập nhật
- File chính: `scripts/upload_to_drive_from_local.py`
- File cấu hình: `config/.env`
- Tầng tri thức: `docs/knowledge/GEM_CODE_MAP.md`, `docs/knowledge/GEM_ERROR_CONTEXT.md`

## Nội dung thay đổi

### 1) Bỏ nhập tham số runtime qua argparse
- Đã loại bỏ toàn bộ `argparse` trong script upload local.
- Script chuyển sang đọc cấu hình cố định từ `config/.env`.

### 2) Chuẩn hóa 3 biến cấu hình trong `config/.env`
- `GDRIVE_CREDENTIALS_FILE=config/etl-nano-project-v2-22b521dbed64.json`
- `GDRIVE_FOLDER_ID=YOUR_DRIVE_FOLDER_ID`
- `GDRIVE_ROOT_DIR=.`

### 3) Bổ sung cơ chế đọc và kiểm tra cấu hình
- Thêm `load_env_file()` để đọc `.env` không cần thư viện ngoài.
- Thêm `load_runtime_config()` để:
  - Kiểm tra đủ 3 biến bắt buộc.
  - Kiểm tra tồn tại file credentials.

### 4) Sửa lỗi không tìm thấy file `.md`
- Thêm `resolve_root_dir()` để xử lý đúng các case cấu hình root phổ biến.
- Thêm validate `root.exists()` và `root.is_dir()` trước khi quét.
- In log rõ ràng:
  - Thư mục đang quét
  - Số lượng file `.md` tìm thấy
- Giữ nguyên quét đệ quy `rglob('*.md')`, loại trừ `.git`.

## Lý do gốc của lỗi đã xử lý
- Root directory truyền vào trước đây dễ bị resolve sai khi người dùng nhập trùng tên repo, gây quét sai thư mục nên không thấy `.md`.
- Script cũ thiếu bước validate và debug path trước khi quét.

## Cách dùng sau cập nhật
1. Mở `config/.env` và điền `GDRIVE_FOLDER_ID` thật.
2. Chạy script:
   - `python scripts/upload_to_drive_from_local.py`

## Kết quả mong đợi
- Không cần nhập tham số mỗi lần chạy.
- Script quét đúng file `.md` tại root project và `docs/knowledge`.
- Nếu cấu hình sai, script báo lỗi rõ ràng thay vì báo rỗng khó hiểu.