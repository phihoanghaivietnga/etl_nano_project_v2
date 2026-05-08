
# YÊU CẦU CỦA MASTER

**Bắt buộc đọc:**

* `GEM_CODE_MAP.md` (Để đối soát cấu trúc thư mục chuẩn).
* `GEM_TECHNICAL_STANDARDS.md` (Để áp dụng quy chuẩn tối ưu hóa code).
* Tệp mã nguồn `scripts/upload_to_drive_from_local.py`.

**Yêu cầu chi tiết:**

1. **Tái cấu trúc thư mục:** Sửa logic upload để tự động tạo thư mục con trên Google Drive tương ứng với cấu trúc thư mục tại máy local. Script phải kiểm tra nếu thư mục đã tồn tại thì lấy ID, nếu chưa thì mới tạo.
2. **Triển khai Diff Sync (Đồng bộ sai khác):** - Thay thế hàm `upload_file` bằng một logic thông minh hơn.
* Trước khi upload, script phải thực hiện truy vấn (Search) trên Drive theo tên file và Folder ID cha.
* Nếu file đã tồn tại: So sánh mã MD5 hoặc thời gian chỉnh sửa (`modifiedTime`). Chỉ thực hiện `service.files().update` nếu file local có sự thay đổi.
* Nếu file chưa tồn tại: Thực hiện `service.files().create`.


3. **Tối ưu hóa hiệu suất:** Loại bỏ việc quét và upload những tệp không thay đổi để rút ngắn thời gian vận hành xuống mức tối thiểu.
4. **Bảo mật thông tin:** Đảm bảo tệp `token.json` và `credentials.json` luôn nằm trong `config/` và không bị đẩy nhầm lên Drive.

**Kết quả đối soát:**

* Codex phải cung cấp đoạn log mẫu cho thấy script nhận diện được file nào "Up-to-date" (đã cập nhật) và file nào "Updated" (mới được sửa đổi).
* Trả về danh sách cấu trúc thư mục đã được tạo trên Drive để AI Test kiểm tra tính thống nhất với local.

**Cập nhật tri thức:**

* Cập nhật `GEM_SYNC_WORKFLOW.md`: Mô tả cơ chế đồng bộ sai khác (Diff Sync) để Master nắm quy trình.

**Kết xuất báo cáo:**

* Cập nhật tệp `REPORT_CHANGES.md` mô tả logic kiểm tra tệp tồn tại và cách xử lý `update` thay vì `create`.

Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.

# BÁO CÁO CỦA THỢ CODE

## 1) Tái cấu trúc đồng bộ thư mục local -> Drive
- Đã bổ sung logic đảm bảo cây thư mục Drive tương ứng local:
  - `find_folder_in_drive()`
  - `create_folder_in_drive()`
  - `ensure_drive_folder_path()`
- Cơ chế hoạt động:
  - Nếu thư mục đã tồn tại thì tái sử dụng ID.
  - Nếu chưa tồn tại thì tạo mới.
  - Có cache folder để giảm số lần truy vấn lặp.

## 2) Triển khai Diff Sync cho file Markdown
- Đã thay thế upload thô bằng hàm `sync_markdown_file()` theo luồng:
  - Tìm file theo `name + parent folder id`.
  - Chưa tồn tại: `create` => `Created`.
  - Đã tồn tại và thay đổi: `update` => `Updated`.
  - Đã tồn tại và không đổi: bỏ qua => `Up-to-date`.

## 3) Cơ chế đối soát thay đổi cho Google Docs
- Do file Google Docs không ổn định ở `md5Checksum` nguồn, script lưu `local_md5` vào `appProperties`.
- Lần chạy sau sẽ đối chiếu `appProperties.local_md5` với local để xác định có thay đổi hay không.

## 4) Tối ưu hiệu suất
- Chỉ update khi file thực sự thay đổi.
- Bỏ qua file `Up-to-date`.
- Dùng cache folder để tăng tốc đồng bộ cây thư mục.

## 5) Bảo mật thông tin
- Đã loại trừ file nhạy cảm khỏi đồng bộ:
  - `config/token.json`
  - `config/etl-nano-project-v2-oauth-credentials.json`
  - `config/.env`
- Đồng thời bỏ qua toàn bộ thư mục `config` và `.venv`.

## 6) Kết quả đối soát thực tế

### Log mẫu trạng thái file
- `RUN1_STATUS=Created`
- `RUN2_STATUS=Updated`
- `RUN3_STATUS=Up-to-date`

### Danh sách cấu trúc thư mục Drive đã tạo
- `docs`
- `docs\\knowledge`
- `docs\\knowledge\\tmp_diffsync_demo`

### File ID đối soát
- `RUN1_FILE_ID=11AOfxNFwhrw0XKlB2y5U8VVWoXQhFACwJSlsUoBa0S0`
- `RUN2_FILE_ID=11AOfxNFwhrw0XKlB2y5U8VVWoXQhFACwJSlsUoBa0S0`
- `RUN3_FILE_ID=11AOfxNFwhrw0XKlB2y5U8VVWoXQhFACwJSlsUoBa0S0`

## 7) Cập nhật tri thức và tài liệu liên quan
- Đã tạo `docs/knowledge/GEM_SYNC_WORKFLOW.md` mô tả quy trình Diff Sync.
- Đã cập nhật `docs/knowledge/GEM_CODE_MAP.md` theo hàm mới.
- Đã cập nhật `REPORT_CHANGES.md` mô tả rõ logic `update` thay vì `create` toàn bộ.
- Đã bổ sung mục đích sử dụng `GEM_SYNC_WORKFLOW.md` vào `agents.md` và `README.md` (không xóa nội dung cũ).
