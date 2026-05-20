# GEM_TECHNICAL_STANDARDS.md

## Tiêu chuẩn xác thực Google Drive cho script upload local

### Chuẩn bắt buộc
- Cơ chế xác thực phải dùng OAuth 2.0 Desktop App cho tài khoản Master.
- Không sử dụng `google.oauth2.service_account` cho luồng upload local.

### Thư viện chuẩn
- `google.auth.transport.requests`
- `google.oauth2.credentials`
- `google_auth_oauthlib.flow`
- `googleapiclient.discovery`
- `pathspec` (đọc và áp dụng quy tắc `.gitignore`)
- `hashlib` (tính checksum MD5 cho Smart Sync)

### Tệp cấu hình chuẩn
- OAuth client credentials: `config/etl-nano-project-v2-oauth-credentials.json`
- Token tái sử dụng: `config/token.json`
- Cấu hình runtime trong `config/.env`:
  - `GDRIVE_FOLDER_ID`
  - `GDRIVE_ROOT_DIR`

### Luồng xác thực chuẩn
1. Kiểm tra `config/token.json`:
   - Nếu tồn tại và hợp lệ: sử dụng trực tiếp.
   - Nếu hết hạn và có `refresh_token`: refresh token.
2. Nếu chưa có token hợp lệ:
   - Khởi chạy `InstalledAppFlow` để Master đăng nhập qua trình duyệt.
3. Sau khi xác thực thành công:
   - Lưu token mới về `config/token.json` để dùng cho các lần chạy sau.

### Yêu cầu bảo mật
- Không in nội dung token, refresh token, client secret ra console.
- Không commit `config/token.json` vào hệ thống quản lý mã nguồn.
- Chỉ log thông tin trạng thái xác thực ở mức cần thiết.

### Yêu cầu vận hành
- Script phải quét đệ quy toàn bộ tệp trong `GDRIVE_ROOT_DIR`, sau đó lọc theo `.gitignore`.
- Bắt buộc loại trừ cứng: `credentials.json`, `token.json`, `.git`, `.venv`, `__pycache__`.
- Với `.md`: giữ cơ chế chuyển đổi sang Google Docs.
- Với tệp khác (`.py`, `.sql`, `.yml`, `.yaml`, ...): upload dưới dạng tệp gốc.
- Trước khi `update`, bắt buộc đối soát checksum MD5 và chỉ cập nhật khi sai khác.

## Tiêu chuẩn kỹ thuật cho Incremental ETL động (Fact)

### Chuẩn cấu hình `incremental_tables` trong `config/tables.yaml`
- Mỗi bảng phải khai báo đầy đủ:
  - `type: fact`
  - `date_column`
  - `merge_script`
  - `lookback_days`
  - `exclude_datatypes`
- Bắt buộc viết block comment ngay phía trên biến `lookback_days` và `exclude_datatypes`.

### Chuẩn xử lý ngày và cửa sổ incremental
- `from_date` và `to_date` phải được chuẩn hóa về `date` trước khi sinh câu lệnh extract.
- Cửa sổ lọc thực tế phải dùng:
  - `effective_from_date = from_date - lookback_days`
- `lookback_days` bắt buộc là số nguyên `>= 0`; nếu âm phải raise lỗi cấu hình.

### Chuẩn Dynamic SELECT theo metadata cột
- Phải truy vấn `INFORMATION_SCHEMA.COLUMNS` tại nguồn để lấy danh sách cột theo thứ tự `ORDINAL_POSITION`.
- Nếu có `exclude_datatypes`, tuyệt đối không được loại cột khỏi projection.
- Với cột thuộc `exclude_datatypes`, phải mask bằng biểu thức an toàn schema:
  - `CAST(NULL AS VARCHAR(1)) AS [TenCot]` (ưu tiên)
  - hoặc `NULL AS [TenCot]` nếu phù hợp ngữ cảnh.
- Với cột không bị loại trừ, giữ nguyên `[TenCot]`.
- Mục tiêu bắt buộc: số lượng và vị trí cột trong Dynamic SELECT phải khớp 100% với bảng đích để tránh `BCP Error 22005 (Schema Shift)`.

### Chuẩn thực thi Staging 3 tầng
- Tầng 1 Global Landing (`stg_nano_v2`):
  - Cho phép `TRUNCATE` + BCP IN/OUT.
  - Sau `TRUNCATE` phải `commit` ngay để tránh lock chờ khi BCP chạy ở session khác.
- Tầng 2 Facility Historical Staging:
  - Chỉ cho phép UPSERT/MERGE.
  - Nghiêm cấm `TRUNCATE`.
- Tầng 3 Datamart (`dm`):
  - Chỉ đọc và thực thi SQL template có sẵn trong `src/db/templates/sql/fact/` và `src/db/templates/sql/dimension/`.
  - Không chỉnh sửa nội dung SQL template trong task incremental.

### Chuẩn giao tiếp cơ sở dữ liệu và bảo toàn dữ liệu tiếng Việt
- Khi dùng BCP bắt buộc cờ `-w` (UTF-16-LE).
- Giữ nguyên nội dung Unicode tiếng Việt trong dữ liệu y tế, không chuyển mã thủ công.

### Chuẩn bảo mật logging kết nối
- Nghiêm cấm log trực tiếp `connection_string`, password (`PWD`), token, secret hoặc full command có chứa thông tin xác thực.
- Chỉ log thông điệp an toàn dạng ngữ cảnh vận hành, ví dụ:
  - `Connected to Database [Ten_DB] at Server [Ten_Server] successfully`.
- Với BCP/subprocess, phải ẩn nội dung query/command nếu có khả năng mang thông tin nhạy cảm.