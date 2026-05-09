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