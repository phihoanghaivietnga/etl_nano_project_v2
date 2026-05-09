
# YÊU CẦU CỦA MASTER

**Bắt buộc đọc:** - `GEM_CODE_MAP.md` (Để đối soát cấu trúc thư mục dự án).

* `GEM_TECHNICAL_STANDARDS.md` (Để áp dụng quy chuẩn về OAuth2 đã thiết lập).
* `GEM_SYNC_WORKFLOW.md` (Để cập nhật luồng đồng bộ mới).

**Yêu cầu chi tiết:**

1. **Quản lý cấu trúc thư mục (Recursive Directory Mapping):**
* Sửa script `scripts/upload_to_drive.py` để tái lập chính xác cấu trúc thư mục local lên Google Drive.
* Script phải tự động kiểm tra sự tồn tại của thư mục cha trước khi tạo thư mục con. Lưu trữ ID của các thư mục đã ánh xạ để tối ưu tốc độ.


2. **Lọc file theo `.gitignore`:**
* Sử dụng thư viện `pathspec` (hoặc logic tương đương) để đọc tệp `.gitignore` tại thư mục gốc (Master đã chạy lệnh `uv add pathspec` để add thư viện vào môi trường chạy rồi)
* TUYỆT ĐỐI KHÔNG upload các tệp hoặc thư mục bị cấm trong `.gitignore`.
* BẮT BUỘC loại trừ thêm các tệp: `credentials.json`, `token.json`, và toàn bộ thư mục `.git`, `.venv`, `__pycache__` dù có trong `.gitignore` hay không.


3. **Cơ chế so sánh MD5 (Smart Sync):**
* Trước khi upload, phải lấy `md5Checksum` của file hiện có trên Drive (nếu có).
* Tính toán MD5 của file local bằng thư viện `hashlib`.
* Chỉ thực hiện `service.files().update` nếu MD5 có sự sai khác. Nếu giống nhau, ghi log "Up-to-date" và bỏ qua để tiết kiệm băng thông.


4. **Xử lý định dạng:**
* Riêng đối với các tệp `.md`, vẫn giữ nguyên logic convert sang Google Docs (`mimeType='application/vnd.google-apps.document'`).
* Các tệp khác (Python, SQL, YAML) upload dưới dạng tệp gốc (Media Upload).


5. **Giao thức phản hồi:** - Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.

**Kết quả đối soát:**

* Codex phải cung cấp đoạn mã log thực thi chứng minh script đã bỏ qua các file trong `.gitignore`.
* Trả về ID của thư mục gốc trên Drive chứa toàn bộ cấu trúc đã đồng bộ.

**Cập nhật tri thức:**

* Cập nhật `GEM_SYNC_WORKFLOW.md`: Ghi lại quy trình lọc dữ liệu theo `.gitignore` và cơ chế đối soát MD5.
* Cập nhật `GEM_TECHNICAL_STANDARDS.md`: Bổ sung thư viện `pathspec` và `hashlib` vào danh sách yêu cầu hệ thống.

**Kết xuất báo cáo:**

* Cập nhật tệp `REPORT_CHANGES.md` liệt kê logic đệ quy thư mục và cách thức xử lý file sai khác.

# BÁO CÁO CỦA THỢ CODE

## 1) Phạm vi thực hiện
- Theo chỉ đạo mới của Master, mình triển khai trực tiếp trên file:
  - `scripts/upload_to_drive_from_local.py`
- Không sửa `scripts/upload_to_drive.py`.

## 2) Quản lý cấu trúc thư mục (Recursive Directory Mapping)
- Đã triển khai mapping đệ quy local -> Drive qua các hàm:
  - `find_folder_in_drive()`
  - `create_folder_in_drive()`
  - `ensure_drive_folder_path()`
- Cơ chế:
  - Kiểm tra tồn tại thư mục cha trước khi tạo thư mục con.
  - Dùng cache folder ID theo path để tăng tốc.

## 3) Lọc file theo `.gitignore`
- Đã dùng `pathspec` đọc và áp dụng `.gitignore` tại root project.
- Đã thêm loại trừ cứng (không phụ thuộc `.gitignore`):
  - File: `credentials.json`, `token.json`
  - Thư mục: `.git`, `.venv`, `__pycache__`
- Đã log theo định dạng:
  - `[Skipped][gitignore] ...`
  - `[Skipped][forced-dir:...] ...`
  - `[Skipped][forced-file:...] ...`

## 4) Smart Sync theo MD5
- Đã tính MD5 local bằng `hashlib` cho mọi file.
- Đã truy vấn file hiện có trên Drive theo `name + parent folder id`.
- Cơ chế so sánh:
  - Ưu tiên `appProperties.local_md5`
  - Fallback `md5Checksum`
- Chỉ `update` khi sai khác; nếu trùng sẽ log `Up-to-date`.

## 5) Xử lý định dạng upload
- `.md`: giữ convert sang Google Docs (`application/vnd.google-apps.document`).
- File khác (`.py`, `.sql`, `.yml`, `.yaml`, ...) upload dạng tệp gốc.

## 6) Kết quả đối soát thực tế

### 6.1 Log chứng minh bỏ qua theo chính sách lọc
- `ROOT_FOLDER_ID=1sN7YercGtTYh63yKCUab40v9IAM7_fHC`
- `Tìm thấy 2217 file (trước khi lọc)`
- Ví dụ log skip:
  - `[Skipped][forced-dir:.git] .git\\config`
  - `[Skipped][forced-dir:.venv] .venv\\Lib\\site-packages\\...`
  - `[Skipped][forced-dir:__pycache__] scripts\\__pycache__\\upload_to_drive_from_local.cpython-312.pyc`

### 6.2 Log Smart Sync
- `Updated`: `docs\\knowledge\\GEM_SYNC_WORKFLOW.md`
- `Up-to-date`: `docs\\prompts\\20260508_1125_change_upload_from_oauth2.md`
- `Created`: `docs\\prompts\\20260508_1510_change_upload_all_from_local_v1.md`

### 6.3 Tổng kết thực thi
- `Created: 9`
- `Updated: 3`
- `Up-to-date: 15`
- `Skipped: 2190`
- `Error: 0`

### 6.4 ID thư mục gốc Drive
- `ROOT_FOLDER_ID=1sN7YercGtTYh63yKCUab40v9IAM7_fHC`

## 7) Cập nhật tri thức và báo cáo
- Đã cập nhật `GEM_SYNC_WORKFLOW.md`: thêm luồng lọc `.gitignore` và cơ chế MD5.
- Đã cập nhật `GEM_TECHNICAL_STANDARDS.md`: bổ sung `pathspec`, `hashlib`.
- Đã cập nhật `REPORT_CHANGES.md`: liệt kê logic đệ quy thư mục + xử lý file sai khác.
