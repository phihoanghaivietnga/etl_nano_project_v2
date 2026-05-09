# REPORT_CHANGES.md

## Phạm vi cập nhật mới (Blacklist v2 cho all-file sync)
- File chính: `scripts/upload_to_drive_from_local.py`
- Tri thức: `docs/knowledge/GEM_SYNC_WORKFLOW.md`, `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`
- Prompt báo cáo: `docs/prompts/20260508_1540_change_upload_all_from_local_v2.md`

## Nội dung thay đổi chính

### 1) Tái cấu trúc đồng bộ thư mục trên Drive
- Bổ sung các hàm:
  - `find_folder_in_drive()`
  - `create_folder_in_drive()`
  - `ensure_drive_folder_path()`
- Cơ chế:
  - Kiểm tra thư mục đã tồn tại thì tái sử dụng ID.
  - Nếu chưa tồn tại thì tạo mới.
  - Dùng cache folder ID để giảm query lặp và tăng hiệu năng.

### 2) Triển khai lọc `.gitignore` + loại trừ cứng
- Bổ sung `pathspec` để đọc và áp dụng `.gitignore` tại root dự án.
- Bổ sung hàm:
  - `load_gitignore_spec()`
  - `normalize_relative_posix()`
  - `classify_skip_reason()`
- Loại trừ bắt buộc (dù có/không có trong `.gitignore`):
  - File: `credentials.json`, `token.json`, `.gitignore`, `.gitattributes`, `.python-version`, các tệp `.env`
  - Thư mục: `.git`, `.venv`, `__pycache__`
- Log bỏ qua theo định dạng: `[Excluded][reason] <relative_path>`.

### 2.1) Lọc ngay từ vòng quét ban đầu
- Điều chỉnh luồng quét từ `candidate_files` thành:
  - `all_files`: tập file thô trước lọc
  - `candidate_files`: tập file còn lại sau khi blacklist theo tên + `pathspec`
- File blacklist bị chặn ngay ở vòng quét đầu, không đi vào bước tính MD5.
- Bổ sung log số lượng:
  - `Tìm thấy <N> file (trước khi lọc)`
  - `Số file sau lọc ban đầu: <M>`

### 3) Smart Sync MD5 cho cả Markdown và file gốc
- Đổi `sync_markdown_file()` thành `sync_file()` để xử lý đa định dạng.
- Tính MD5 local bằng `hashlib` cho mọi file.
- Cơ chế so sánh checksum:
  - Ưu tiên `appProperties.local_md5`
  - Fallback sang `md5Checksum` của Drive
- Chỉ `update` khi checksum sai khác, nếu trùng thì `Up-to-date`.

### 4) Xử lý định dạng upload
- `.md`: giữ convert sang Google Docs (`mimeType='application/vnd.google-apps.document'`).
- Các tệp khác (`.py`, `.sql`, `.yml`, `.yaml`, ...): upload dạng tệp gốc với `MediaFileUpload`.

### 5) Tối ưu log và đối soát
- In `ROOT_FOLDER_ID=<folder_id>` ngay đầu phiên chạy để AI Test đối chiếu.
- In tổng số file trước lọc và kết quả theo trạng thái `Created/Updated/Up-to-date/Skipped/Error`.
- Log rõ ràng trạng thái `Excluded` khi tệp bị loại bởi blacklist theo tên hoặc `.gitignore`.

## Cập nhật tri thức và tài liệu
- Cập nhật `GEM_SYNC_WORKFLOW.md`:
  - Bổ sung quy trình lọc `.gitignore` và loại trừ cứng.
  - Bổ sung mục "Danh sách các tệp không đồng bộ" và lý do không upload tệp cấu hình hệ thống.
  - Bổ sung cơ chế MD5 cho `.md` và file gốc.
- Cập nhật `GEM_TECHNICAL_STANDARDS.md`:
  - Bổ sung thư viện chuẩn `pathspec` và `hashlib`.