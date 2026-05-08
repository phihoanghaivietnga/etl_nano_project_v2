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

## E-UPLOAD-003: Quota Drive đã đầy hoặc dưới ngưỡng an toàn

### Triệu chứng
- Console luôn in dung lượng quota còn lại, sau đó báo bỏ qua upload.
- Ví dụ: `Quota còn lại: 0.12 GB ...` và `Bỏ qua upload vì quota còn lại thấp hơn ngưỡng an toàn 0.50 GB.`

### Nguyên nhân gốc
- Dung lượng còn lại của Drive service account nhỏ hơn ngưỡng tối thiểu `0.5 GB`.
- Hoặc quota đã đầy (`remaining = 0`).

### Cách xử lý chuẩn
- Giải phóng bớt dung lượng trên Drive đích của service account.
- Tăng ngưỡng hoặc điều chỉnh chiến lược upload theo batch nếu phù hợp nghiệp vụ.

## E-UPLOAD-004: Không xác định được quota Drive

### Triệu chứng
- Console in thông báo không xác định được tổng quota hoặc lỗi gọi API quota.
- Script chủ động bỏ qua upload để an toàn.

### Nguyên nhân gốc
- API `about.storageQuota` không trả về `limit` hợp lệ.
- Hoặc lỗi quyền/API khi truy vấn quota.

### Cách xử lý chuẩn
- Kiểm tra quyền của service account với Drive API.
- Kiểm tra cấu hình project GCP và trạng thái Drive API.
- Chạy lại sau khi xác nhận quyền và quota có thể truy vấn.

## E-UPLOAD-003, E-UPLOAD-004: Trạng thái sau khi chuyển sang OAuth2 Desktop

### Trạng thái
- Hai lỗi liên quan quota service account (`E-UPLOAD-003`, `E-UPLOAD-004`) được đánh dấu giải quyết triệt để trong luồng upload local.
- Nguyên nhân: script đã chuyển mô hình xác thực từ Service Account sang OAuth2 Desktop App (danh nghĩa Master), đồng thời loại bỏ hoàn toàn logic kiểm tra quota trước upload.

### Ghi chú vận hành
- Phiên bản OAuth2 Desktop không còn dùng các hàm quota cũ (`bytes_to_gb`, `get_drive_quota`) và ngưỡng `MIN_FREE_QUOTA_GB`.
- Nếu phát sinh lỗi upload, ưu tiên kiểm tra token OAuth, quyền thư mục đích và trạng thái chia sẻ trên Drive.