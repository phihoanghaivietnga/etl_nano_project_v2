
# YÊU CẦU CỦA MASTER

**Bắt buộc đọc:**

* `GEM_TECHNICAL_STANDARDS.md` (Để thiết lập tiêu chuẩn xác thực mới).
* `GEM_ERROR_CONTEXT.md` (Để ghi nhận việc loại bỏ lỗi E-ID liên quan đến Quota Service Account).
* Tệp mã nguồn `scripts/upload_to_drive_from_local.py`.

**Yêu cầu chi tiết:**

1. **Thay thế thư viện xác thực:** Loại bỏ `google.oauth2.service_account`. Thay thế bằng `google.auth.transport.requests`, `google.oauth2.credentials`, và `google_auth_oauthlib.flow`.
2. **Cấu hình tệp tin:** Sử dụng tệp credentials tại đường dẫn `config/etl-nano-project-v2-oauth-credentials.json`.
3. **Triển khai luồng OAuth2 Desktop:** - Viết lại hàm `authenticate`.
* Luồng xử lý: Kiểm tra tệp `config/token.json`. Nếu tồn tại và còn hạn, sử dụng nó. Nếu không, khởi chạy `InstalledAppFlow` để mở trình duyệt cho Master đăng nhập.
* Sau khi đăng nhập thành công, phải tự động lưu token mới vào `config/token.json` để tái sử dụng.


4. **Dọn dẹp mã nguồn:** - Xóa bỏ toàn bộ logic kiểm tra Quota (`get_drive_quota`, `bytes_to_gb`, `MIN_FREE_QUOTA_GB`). Khi chạy dưới danh nghĩa Master, việc này là thừa thãi và gây chậm hệ thống.
* Giữ nguyên logic chuyển đổi Markdown sang Google Docs trong hàm `upload_file`.


5. **Xử lý thư mục:** Đảm bảo script vẫn quét toàn bộ file `.md` trong thư mục gốc dự án (trừ `.git`) như cũ.

**Kết quả đối soát:**

* Codex phải chạy thử và trả về log xác nhận đã tạo được tệp `config/token.json`.
* Thực hiện upload thử 1 file và trả về File ID để AI Test kiểm tra quyền sở hữu trên Drive.

**Cập nhật tri thức:**

* Cập nhật `GEM_TECHNICAL_STANDARDS.md`: Ghi đè phần hướng dẫn xác thực từ Service Account sang OAuth 2.0 Desktop App.
* Cập nhật `GEM_ERROR_CONTEXT.md`: Đánh dấu lỗi Quota (E-ID cũ) đã được giải quyết triệt để bằng cách chuyển đổi thực thể xác thực.

**Kết xuất báo cáo:**

* Cập nhật tệp `REPORT_CHANGES.md` mô tả các hàm đã thay đổi và danh sách thư viện mới cần cài đặt qua `uv`.

Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.

# BÁO CÁO CỦA THỢ CODE

## 1) Kết quả thực hiện theo chỉ thị

- Đã thay thế xác thực từ `google.oauth2.service_account` sang OAuth2 Desktop App.
- Đã sử dụng credentials tại: `config/etl-nano-project-v2-oauth-credentials.json`.
- Đã viết lại hàm `authenticate` theo luồng:
  - Đọc `config/token.json` nếu có và còn hợp lệ.
  - Refresh token nếu hết hạn và có `refresh_token`.
  - Nếu chưa hợp lệ thì mở trình duyệt qua `InstalledAppFlow` để đăng nhập.
  - Tự động lưu token mới về `config/token.json`.

## 2) Dọn dẹp mã nguồn

- Đã xóa toàn bộ logic quota:
  - `MIN_FREE_QUOTA_GB`
  - `bytes_to_gb`
  - `get_drive_quota`
  - Các nhánh điều kiện chặn upload theo quota.
- Giữ nguyên logic chuyển đổi Markdown sang Google Docs trong `upload_file`.

## 3) Quét thư mục

- Script vẫn quét toàn bộ file `.md` từ thư mục gốc dự án (trừ `.git`) bằng `rglob('*.md')` như yêu cầu.

## 4) Cập nhật tri thức

- Đã cập nhật `docs/knowledge/GEM_CODE_MAP.md` theo hàm mới OAuth2.
- Đã tạo `docs/knowledge/GEM_TECHNICAL_STANDARDS.md` để chuẩn hóa tiêu chuẩn OAuth2 Desktop.
- Đã cập nhật `docs/knowledge/GEM_ERROR_CONTEXT.md` và đánh dấu nhóm lỗi quota service account là đã được xử lý triệt để trong luồng mới.

## 5) Cập nhật bảo mật và báo cáo

- Đã thêm `config/token.json` vào `.gitignore` để tránh lộ token.
- Đã cập nhật `REPORT_CHANGES.md` mô tả đầy đủ hàm thay đổi và danh sách thư viện cần qua `uv`.

## 6) Đối soát chạy thật

- Đã chạy xác thực thực tế thành công và tạo token:
  - `Đã lưu token OAuth tại: D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\config\token.json`
  - `TOKEN_EXISTS=True`
- Đã upload thử 1 file `.md` thành công:
  - `SELECTED_FILE=D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\0_yeu_cau_khoi_tao_ban_dau.md`
  - `FILE_ID=1S7cC1wa2em6Gar7QSRgi9zM5ClDwuTBvHTd6v9aDuRs`