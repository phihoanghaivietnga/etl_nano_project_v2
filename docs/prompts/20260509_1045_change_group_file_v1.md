
# YÊU CẦU CỦA MASTER

**Bắt buộc đọc:**

* `GEM_CODE_MAP.md` (Để đối soát và cập nhật quy tắc ánh xạ mới).
* `GEM_SYNC_WORKFLOW.md` (Để ghi lại quy trình gộp file).
* `PROJECT_CHRONICLE.md` (Để nắm bắt lịch sử phát triển dự án).

**# BƯỚC 1: THIẾT LẬP CẤU TRÚC VÀ TÀI LIỆU HƯỚNG DẪN NGƯỜI DÙNG**

1. Tạo thư mục `/docs/specifications/` tại thư mục gốc.
2. Khởi tạo 3 file tài liệu dành cho người dùng với tên gọi đầy đủ (không viết tắt):
* `Dac_ta_yeu_cau_nghiep_vu_y_te.md` (Thay thế cho SRS).
* `Thiet_ke_kien_truc_he_thong_chi_tiet.md` (Thay thế cho SDD).
* `Huong_dan_su_dung_va_van_hanh_he_thong.md` (Thay thế cho User Guide).


3. Nội dung trong các file này phải viết bằng tiếng Việt, ngắn gọn, cô đọng, không icon và không sử dụng thẻ dẫn nguồn.

**# BƯỚC 2: CẬP NHẬT QUY TẮC ÁNH XẠ VÀO TẦNG TRI THỨC**
Mở tệp `GEM_CODE_MAP.md` và ghi nhận bảng quy tắc ánh xạ bắt buộc sau đây để Gem có ngữ cảnh điều phối lâu dài, và cần ghi rõ việc chia nhóm này để phục vụ việc merge file tạo tri thức cho NotebookLM:

* **Nhóm CORE_LOGIC:** Bao gồm các tệp trong thư mục `/src/core/`, `/config/` và tệp `.env`.
* **Nhóm ETL_PROCESS:** Bao gồm các tệp trong thư mục `/src/jobs/` và `/src/db/templates/sql/`.
* **Nhóm INTERFACE:** Bao gồm các tệp trong thư mục `/src/ui/`, `/scripts/` và tệp `main.py` tại root.
* **Nhóm KNOWLEDGE_BASE:** Bao gồm các tệp trong thư mục `/docs/v2_knowledge/`, tệp `agents.md`, `README.md` và `PROJECT_CHRONICLE.md`.

**# BƯỚC 3: NÂNG CẤP SCRIPT upload_to_drive_from_local.py (CHI TIẾT KỸ THUẬT)**
Thực hiện sửa đổi tệp `scripts/upload_to_drive_from_local.py` theo các bước sau:

1. **Khai báo hằng số:** Tạo một Dictionary chứa quy tắc ánh xạ từ đường dẫn thư mục sang tên file Master tương ứng (ví dụ: `MASTER_CORE_LOGIC.md`).
2. **Xây dựng hàm lọc tệp:** Sử dụng `pathspec` để lọc bỏ hoàn toàn các tệp trong `.gitignore`. Bổ sung logic loại trừ cứng các tệp: `.gitignore`, `credentials.json`, `token.json`, thư mục `.git`, `.venv`, `__pycache__`.
3. **Xây dựng hàm gộp nội dung (Merge Logic):**
* Tạo thư mục tạm `temp_merged/` tại thư mục gốc.
* Đối với mỗi nhóm, tạo một tệp `.md` Master.
* **Bảo tồn ngữ cảnh:** Tại đầu mỗi file Master, tạo một "Mục lục" liệt kê danh sách các tệp gốc có trong nhóm đó.
* **Cấu trúc Header:** Mỗi đoạn nội dung của tệp gốc phải được phân tách bằng Header cấp 3 dạng: `### SOURCE: [Đường dẫn đầy đủ của file]`. Sau đó bọc toàn bộ code/nội dung vào trong Markdown code block tương ứng.


4. **Xây dựng hàm đối soát MD5:**
* Sử dụng `hashlib` để tính MD5 của file Master tại local.
* Gọi API Drive để lấy `md5Checksum` của file tương ứng trên Drive.
* Chỉ thực hiện lệnh `update` (hoặc `create` nếu chưa có) nếu mã MD5 sai khác.


5. **Xây dựng luồng xác thực:** Sử dụng OAuth2 Desktop App để lấy `token.json`, đảm bảo quyền upload sử dụng hạn mức của tài khoản Master (5 TB).
6. **Xử lý định dạng:** Mọi tệp có đuôi `.md` (bao gồm cả các file Master gộp) khi upload lên Drive phải được cấu hình `mimeType='application/vnd.google-apps.document'`.

**# BƯỚC 4: CẬP NHẬT TÀI LIỆU VÀ BÁO CÁO**

1. Cập nhật `GEM_SYNC_WORKFLOW.md`: Mô tả chi tiết luồng tự động hóa từ việc quét file -> Lọc tệp -> Ánh xạ nhóm -> Gộp nội dung -> Đối soát MD5 -> Upload.
2. Cập nhật `PROJECT_CHRONICLE.md`: Ghi lại dấu mốc quan trọng về việc xây dựng hệ thống gộp tri thức đa tầng cho NotebookLM.
3. Ghi rõ dòng sau ở cuối phần yêu cầu: "Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE".

# BÁO CÁO CỦA THỢ CODE

Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.

## Kết quả thực hiện

### 1) Thiết lập cấu trúc và tài liệu người dùng
- Đã tạo thư mục `docs/specifications/`.
- Đã tạo 3 tài liệu:
  - `docs/specifications/Dac_ta_yeu_cau_nghiep_vu_y_te.md`
  - `docs/specifications/Thiet_ke_kien_truc_he_thong_chi_tiet.md`
  - `docs/specifications/Huong_dan_su_dung_va_van_hanh_he_thong.md`

### 2) Cập nhật quy tắc ánh xạ tầng tri thức
- Đã cập nhật `docs/knowledge/GEM_CODE_MAP.md` với 4 nhóm bắt buộc:
  - `CORE_LOGIC`
  - `ETL_PROCESS`
  - `INTERFACE`
  - `KNOWLEDGE_BASE`
- Đã ghi rõ mục đích chia nhóm để gộp file Master phục vụ NotebookLM.

### 3) Nâng cấp script upload_to_drive_from_local.py
- Đã bổ sung hằng số ánh xạ nhóm -> file Master:
  - `MASTER_CORE_LOGIC.md`
  - `MASTER_ETL_PROCESS.md`
  - `MASTER_INTERFACE.md`
  - `MASTER_KNOWLEDGE_BASE.md`
- Đã triển khai lọc bằng `pathspec` theo `.gitignore` và loại trừ cứng:
  - File: `.gitignore`, `credentials.json`, `token.json`
  - Thư mục: `.git`, `.venv`, `__pycache__`
- Đã triển khai cơ chế gộp nội dung:
  - Tạo thư mục `temp_merged/`
  - Tạo file Master theo nhóm
  - Có mục lục nguồn ở đầu file
  - Mỗi block theo chuẩn `### SOURCE: <đường dẫn>` + code block theo đuôi file
- Đã triển khai đối soát MD5 trước khi upload:
  - Tính MD5 local bằng `hashlib`
  - Lấy `md5Checksum` từ Drive API để so sánh
  - Chỉ `update` khi sai khác, `create` nếu chưa có
- Đã giữ luồng xác thực OAuth2 Desktop App với `token.json`.
- Đã đảm bảo tất cả tệp `.md` (bao gồm file Master) upload dưới dạng Google Docs.

### 4) Cập nhật tài liệu và báo cáo
- Đã cập nhật `docs/knowledge/GEM_SYNC_WORKFLOW.md` theo luồng:
  - Quét file -> Lọc tệp -> Ánh xạ nhóm -> Gộp nội dung -> Đối soát MD5 -> Upload.
- Đã tạo `PROJECT_CHRONICLE.md` và ghi lại dấu mốc xây dựng hệ thống gộp tri thức đa tầng cho NotebookLM.
- Đã cập nhật `REPORT_CHANGES.md` cho đợt thay đổi này.
