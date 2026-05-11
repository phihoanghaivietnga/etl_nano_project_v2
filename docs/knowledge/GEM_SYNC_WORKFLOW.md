# GEM_SYNC_WORKFLOW.md

## Mục tiêu
- Chuẩn hóa luồng đồng bộ tri thức từ local lên Google Drive theo cơ chế sai khác.
- Tạo bộ file Master theo nhóm để phục vụ tạo tri thức cho NotebookLM.

## Phạm vi áp dụng
- Script: `scripts/upload_to_drive_from_local.py`
- Nguồn dữ liệu: toàn bộ file trong `GDRIVE_ROOT_DIR` sau khi lọc hợp lệ.
- Đích: Google Drive, trong đó mọi file `.md` được chuyển thành Google Docs.

## Luồng tự động hóa chuẩn

### Bước 1: Quét file
- Quét đệ quy tất cả file từ thư mục gốc cấu hình `GDRIVE_ROOT_DIR`.
- Thu tập file thô ban đầu để chuẩn bị lọc.

### Bước 2: Lọc tệp
- Áp dụng `pathspec` với quy tắc `.gitignore` tại root dự án.
- Loại trừ cứng các mục:
  - File: `.gitignore`, `credentials.json`, `token.json`
  - Thư mục: `.git`, `.venv`, `__pycache__`
- Chỉ giữ các file hợp lệ cho các bước tiếp theo.

### Bước 3: Ánh xạ nhóm
- Ánh xạ file vào 4 nhóm quy chuẩn:
  - `CORE_LOGIC`
  - `ETL_PROCESS`
  - `INTERFACE`
  - `KNOWLEDGE_BASE`
- Ánh xạ này là cơ sở để tạo file Master theo ngữ cảnh chức năng.

### Bước 4: Gộp nội dung (Enhanced Merge với Metadata)
- Tạo thư mục tạm `temp_merged/` tại root.
- Với mỗi nhóm, tạo một file Master `.md`.
- Cấu trúc bắt buộc của file Master:
  - **Mục lục nguồn ở đầu file**: Liệt kê đầy đủ tệp nguồn với metadata mô tả.
    - Dòng đầu: `[DESCRIPTION]: <Mô tả chung của nhóm>`
    - Mỗi tệp: `### <đường dẫn tệp> - <Mô tả chức năng thực tế của tệp>`
  - **Gán nhãn mô tả tệp (File Description Tagging)**:
    - Mỗi tệp nguồn phải có mô tả ngắn gọn theo ý nghĩa nghiệp vụ/vận hành thực tế.
    - Không dùng mô tả lặp lại tên file đơn thuần.
  - **Các khối nội dung**: Mỗi tệp nguồn được ghi theo header `### SOURCE: <đường dẫn tệp>`.
  - **Nội dung gốc**: Bọc trong code block Markdown theo loại tệp (md, py, sql, etc.).
- Cách thức này bảo tồn ngữ cảnh và cung cấp định hướng cho NotebookLM:

### Bước 5: Đối soát MD5
- Tính MD5 local bằng `hashlib` cho file cần upload (bao gồm file Master).
- Tìm file tương ứng trên Drive theo `name + parent`.
- Lấy `md5Checksum` trên Drive để so sánh.
- Nếu thiếu `md5Checksum` thì fallback `appProperties.local_md5`.
- Chỉ `update` khi mã MD5 sai khác, nếu chưa có file thì `create`.

### Bước 6: Upload
- Xác thực OAuth2 Desktop App và lưu `token.json`.
- Upload file lên đúng thư mục Drive theo đường dẫn tương đối.
- Tất cả file `.md` (kể cả file Master) dùng:
  - `mimeType='application/vnd.google-apps.document'`

## Kết quả và đối soát
- Log chi tiết theo trạng thái: `Created`, `Updated`, `Up-to-date`, `Skipped`, `Error`.
- In tổng kết cuối phiên và danh sách thư mục Drive đã tạo.

## Quy tắc an toàn
- Không đồng bộ file nhạy cảm và file hệ thống.
- Không ghi log nội dung token hoặc thông tin bí mật.