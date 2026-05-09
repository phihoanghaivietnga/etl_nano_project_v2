# REPORT_CHANGES.md

## Phạm vi cập nhật theo yêu cầu 20260509_1045_change_group_file_v1
- Script chính: `scripts/upload_to_drive_from_local.py`
- Tài liệu người dùng: `docs/specifications/`
- Tri thức kỹ thuật: `docs/knowledge/GEM_CODE_MAP.md`, `docs/knowledge/GEM_SYNC_WORKFLOW.md`
- Nhật ký dự án: `PROJECT_CHRONICLE.md`
- File yêu cầu cần ghi báo cáo: `docs/prompts/20260509_1045_change_group_file_v1.md`

## Nội dung đã thực hiện

### 1) Thiết lập bộ tài liệu người dùng
- Tạo thư mục `docs/specifications/`.
- Tạo 3 tài liệu:
  - `Dac_ta_yeu_cau_nghiep_vu_y_te.md`
  - `Thiet_ke_kien_truc_he_thong_chi_tiet.md`
  - `Huong_dan_su_dung_va_van_hanh_he_thong.md`

### 2) Cập nhật quy tắc ánh xạ nhóm tri thức
- Cập nhật `GEM_CODE_MAP.md` với 4 nhóm chuẩn:
  - `CORE_LOGIC`
  - `ETL_PROCESS`
  - `INTERFACE`
  - `KNOWLEDGE_BASE`
- Ghi rõ mục tiêu chia nhóm để tạo file Master phục vụ merge tri thức cho NotebookLM.

### 3) Nâng cấp script đồng bộ Drive từ local
- Bổ sung hằng số ánh xạ nhóm -> file Master:
  - `MASTER_CORE_LOGIC.md`
  - `MASTER_ETL_PROCESS.md`
  - `MASTER_INTERFACE.md`
  - `MASTER_KNOWLEDGE_BASE.md`
- Hoàn thiện lọc tệp:
  - Áp dụng `.gitignore` qua `pathspec`.
  - Loại trừ cứng: `.gitignore`, `credentials.json`, `token.json`, `.git`, `.venv`, `__pycache__`.
- Thêm merge logic:
  - Tạo thư mục tạm `temp_merged/`.
  - Tạo file Master theo từng nhóm.
  - Mỗi file Master có mục lục nguồn.
  - Mỗi nội dung nguồn tách bằng `### SOURCE: <đường dẫn>` và bọc code block theo đuôi file.
- Cập nhật đối soát MD5:
  - Tính MD5 local bằng `hashlib`.
  - So sánh với `md5Checksum` trên Drive, fallback `appProperties.local_md5`.
  - Chỉ update khi sai khác, create nếu chưa có.
- Giữ luồng OAuth2 Desktop App và lưu `token.json`.
- Bảo đảm mọi file `.md` upload dạng Google Docs.

### 4) Cập nhật tài liệu tri thức và nhật ký dự án
- Cập nhật `GEM_SYNC_WORKFLOW.md` với luồng:
  - Quét file -> Lọc tệp -> Ánh xạ nhóm -> Gộp nội dung -> Đối soát MD5 -> Upload.
- Tạo `PROJECT_CHRONICLE.md` và ghi dấu mốc xây dựng hệ thống gộp tri thức đa tầng cho NotebookLM.

### 5) Cập nhật báo cáo trong file yêu cầu
- Bổ sung đầy đủ phần `# BÁO CÁO CỦA THỢ CODE` trong:
  - `docs/prompts/20260509_1045_change_group_file_v1.md`
- Có ghi rõ dòng bắt buộc theo yêu cầu và mô tả chi tiết các việc đã làm.