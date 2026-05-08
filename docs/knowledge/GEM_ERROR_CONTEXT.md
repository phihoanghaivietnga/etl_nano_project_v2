# GEM_ERROR_CONTEXT.md

## E-UPLOAD-001: Không tìm thấy file `.md` để upload

### Triệu chứng
- Script in ra: `Không tìm thấy file .md để upload.`

### Nguyên nhân gốc
- `GDRIVE_ROOT_DIR` cấu hình sai, thường gặp khi đặt giá trị trùng tên repo và chạy tại root repo, dẫn đến resolve thành đường dẫn lồng sai.
- Thiếu kiểm tra tồn tại thư mục gốc trước khi quét.

### Cách xử lý chuẩn
- Dùng `resolve_root_dir()` để chuẩn hóa `GDRIVE_ROOT_DIR`.
- Thêm kiểm tra `root.exists()` và `root.is_dir()` trước khi `rglob`.
- In debug path: `Đang quét file .md trong thư mục: ...` và số lượng file tìm được.

## E-UPLOAD-002: Thiếu cấu hình runtime trong `config/.env`

### Triệu chứng
- Script dừng với thông báo thiếu biến môi trường cấu hình.

### Biến bắt buộc
- `GDRIVE_CREDENTIALS_FILE`
- `GDRIVE_FOLDER_ID`
- `GDRIVE_ROOT_DIR`

### Cách xử lý chuẩn
- Điền đầy đủ 3 biến trong `config/.env`.
- Đảm bảo file credentials tồn tại đúng đường dẫn đã khai báo.