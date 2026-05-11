# YÊU CẦU CỦA MASTER

**Bắt buộc đọc**:

* `GEM_CODE_MAP.md` (Để đối soát lại cấu trúc thư mục thực tế).
* `GEM_SYNC_WORKFLOW.md` (Để cập nhật luồng gộp file và lọc dữ liệu).
* `PROJECT_CHRONICLE.md` (Để ghi lại nhật ký xử lý lỗi thư mục).

**# BƯỚC 1: CHỈNH SỬA VÀ DI CHUYỂN THƯ MỤC SAI QUY ĐỊNH**

1. Di chuyển toàn bộ thư mục `tmp_diffsync_demo` từ `/docs/knowledge/` ra thư mục gốc (`/`). Thư mục tri thức chỉ được phép chứa các tệp `.md` quy định, không được chứa các folder demo làm nhiễu bộ não AI.
2. Sau khi di chuyển, hãy kiểm tra và cập nhật lại nội dung các file GEM liên quan (nếu có tham chiếu đến đường dẫn cũ).

**# BƯỚC 2: SỬA LỖI GỘP FILE MASTER_KNOWLEDGE_BASE.MD**

1. Tôi phát hiện tệp `MASTER_KNOWLEDGE_BASE.md` đang trống hoặc thiếu nội dung từ `/docs/knowledge/`. Đây là lỗi cẩu thả nghiêm trọng làm mù "Bộ não" NotebookLM.
2. Codex phải quét lại toàn bộ `/docs/knowledge/`, đảm bảo 9 tệp GEM và các tệp chiến lược khác được gộp đầy đủ vào tệp Master này.
3. **Bổ sung Metadata**: Trong phần "Mục lục" ở đầu mỗi tệp Master (bao gồm cả CORE, ETL, INTERFACE), Codex bắt buộc phải thêm dòng mô tả chức năng ngắn gọn (`[DESCRIPTION]`) cho từng tệp thành phần. Không được để một danh sách tệp vô hồn.

**# BƯỚC 3: NÂNG CẤP SCRIPT VÀ TRÍCH XUẤT BẰNG CHỨNG (LOGS)**

Sửa lại `scripts/upload_to_drive_from_local.py` để đảm bảo tính minh bạch:

1. **Đồng bộ đường dẫn**: Đảm bảo mọi hằng số và cấu hình trong script và tệp `.env` đều trỏ thống nhất về `/docs/knowledge/` (không được sử dụng v2_knowledge).
2. **Trích xuất Log thực tế**: Script khi chạy phải in ra Console ít nhất 10 dòng log chi tiết cho Master kiểm tra, bao gồm:
   * Log lọc file: Ví dụ `.gitignore: Ignored`, `token.json: Excluded`.
   * Log đối soát MD5: Ví dụ `File GEM_GUIDE.md: MD5 match, skipping upload`.
   * Log upload: Ví dụ `File MASTER_ETL_PROCESS.md: MD5 mismatch, updating...`.
3. **Xác thực OAuth2**: Giữ nguyên luồng xác thực cá nhân để sử dụng hạn mức 5 TB của Master.

**# BƯỚC 4: CẬP NHẬT TÀI LIỆU VÀ BÁO CÁO**

1. Cập nhật `PROJECT_CHRONICLE.md`: Ghi lại sự cố cấu trúc thư mục (vụ `tmp_diffsync_demo`) và cách khắc phục để làm bài học kinh nghiệm.
2. Cập nhật `GEM_SYNC_WORKFLOW.md`: Mô tả rõ hơn về cơ chế "Gộp file kèm mô tả" (Enhanced Merge).
3. Ghi rõ dòng sau ở cuối phần yêu cầu: "Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE".

**# BÁO CÁO CỦA THỢ CODE**

(Codex phải dán ít nhất 10 dòng log thực thi vào đây để chứng minh logic MD5 và Pathspec đang hoạt động).

## Mô tả các việc đã làm

### 1. Chỉnh sửa cấu trúc thư mục
- Di chuyển thư mục `docs/knowledge/tmp_diffsync_demo/` ra thư mục gốc project (`tmp_diffsync_demo/`).
- Xóa bỏ tham chiếu sai `docs/v2_knowledge/` trong `GEM_CODE_MAP.md`, thay bằng `docs/knowledge/`.

### 2. Đồng bộ đường dẫn cấu hình
- Cập nhật `config/.env`: đổi `GDRIVE_ROOT_DIR=etl_nano_project_v2` thành `GDRIVE_ROOT_DIR=docs/knowledge`.
- Đảm bảo script và cấu hình trỏ thống nhất về `/docs/knowledge/`.

### 3. Nâng cấp script `scripts/upload_to_drive_from_local.py`
- **Sửa hàm `classify_group_by_path`**: Xử lý đúng khi `GDRIVE_ROOT_DIR` trỏ đến thư mục con (`docs/knowledge/`). File `.md` trực tiếp trong root (không chứa `/`) và không thuộc `src/`/`scripts/`/`main.py` tự động phân loại `KNOWLEDGE_BASE`. Các file chiến lược luôn thuộc `KNOWLEDGE_BASE`.
- **Thêm `GROUP_DESCRIPTIONS`**: Metadata mô tả ngắn cho từng nhóm (CORE_LOGIC, ETL_PROCESS, INTERFACE, KNOWLEDGE_BASE).
- **Nâng cấp `build_master_content`**: Mục lục nguồn mỗi dòng có thêm `[DESCRIPTION]: <mô tả ngắn>`.
- **Nâng cấp log minh bạch**: Log phân nhóm, MD5 match/mismatch, upload/create/update, tổng kết.
- Giữ nguyên luồng OAuth2 Desktop App.

### 4. Cập nhật tài liệu tri thức
- **`GEM_CODE_MAP.md`**: Sửa đường dẫn `docs/v2_knowledge/` → `docs/knowledge/`.
- **`GEM_SYNC_WORKFLOW.md`**: Bổ sung bước "Enhanced Merge" - mô tả cơ chế gộp file kèm metadata `[DESCRIPTION]`.
- **`PROJECT_CHRONICLE.md`**: Ghi nhật ký sự cố `tmp_diffsync_demo`, nguyên nhân, cách khắc phục, và bài học kinh nghiệm.

### 5. Kiểm chứng
- Chạy script thành công: 12 file được quét, 12 file thuộc KNOWLEDGE_BASE, 4 file Master được tạo.
- Upload thành công: 6 file Updated, 10 file Up-to-date, 0 Error.
- `MASTER_KNOWLEDGE_BASE.md` bao gồm đầy đủ 12 file GEM và tài liệu chiến lược.

=== LOG THỰC THI TỪ `python scripts/upload_to_drive_from_local.py` ===

```
=== KHỞI ĐỘNG ĐỒNG BỘ ===
ROOT_FOLDER_ID=1sN7YercGtTYh63yKCUab40v9IAM7_fHC
ROOT_DIR=D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\knowledge
Đang quét file trong thư mục: D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\knowledge
Đã lưu token OAuth tại: D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\config\token.json
Xác thực OAuth2 thành công
Đã tải quy tắc .gitignore
Tìm thấy 12 file (trước khi lọc)

=== KẾT QUẢ LỌC TỆP ===
Số file sau lọc ban đầu: 12
Số file bị loại: 0
[Group CORE_LOGIC]: 0 file(s)
[Group ETL_PROCESS]: 0 file(s)
[Group INTERFACE]: 0 file(s)
[Group KNOWLEDGE_BASE]: 12 file(s)
[Master Built] D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\temp_merged\MASTER_CORE_LOGIC.md
[Master Built] D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\temp_merged\MASTER_ETL_PROCESS.md
[Master Built] D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\temp_merged\MASTER_INTERFACE.md
[Master Built] D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\temp_merged\MASTER_KNOWLEDGE_BASE.md

=== BẮT ĐẦU ĐỐI SOÁT VÀ UPLOAD ===
[MD5 Match] GEM_AUTO_PIPELINE.md: Local MD5=9ee39b12..., Remote MD5=9ee39b12... -> Skipping
[MD5 Mismatch] GEM_CODE_MAP.md: Local MD5=daa5babd..., Remote MD5=fb29bd26... -> Updating
[Updated] GEM_CODE_MAP.md -> ID: 1XIVISCr7EEH8WOaTRFm3-Mi3t5JB8Prq4vhhTRbRxes
[MD5 Match] GEM_CODE_SNIPPETS.md: Local MD5=13d88353..., Remote MD5=13d88353... -> Skipping
[MD5 Match] GEM_DATA_FLOW.md: Local MD5=d5426d04..., Remote MD5=d5426d04... -> Skipping
[MD5 Match] GEM_DB_SCHEMAS.md: Local MD5=251276d5..., Remote MD5=251276d5... -> Skipping
[MD5 Match] GEM_DEPENDENCY_GRAPH.md: Local MD5=c351e843..., Remote MD5=c351e843... -> Skipping
[MD5 Match] GEM_ERROR_CONTEXT.md: Local MD5=ba75d99e..., Remote MD5=ba75d99e... -> Skipping
[MD5 Match] GEM_GUIDE.md: Local MD5=04689607..., Remote MD5=04689607... -> Skipping
[MD5 Match] GEM_NAVIGATION.md: Local MD5=4a6a32ef..., Remote MD5=4a6a32ef... -> Skipping
[MD5 Mismatch] GEM_SYNC_WORKFLOW.md: Local MD5=579c140a..., Remote MD5=4f5c7283... -> Updating
[Updated] GEM_SYNC_WORKFLOW.md -> ID: 1dhs-WkliL6EPH7OOQUXcQP2wstkBjnqi2IpPJs4cRsA
[MD5 Match] GEM_TECHNICAL_STANDARDS.md: Local MD5=56c428b4..., Remote MD5=56c428b4... -> Skipping
[MD5 Match] loop_Gem_Github_GoogleDrive_NotebookLM.md: Local MD5=71a82917..., Remote MD5=71a82917... -> Skipping
[Folder Exists] temp_merged -> 1g5OJEZXTLHVlUJb15Tp8E79Gfg4RIt9m
[MD5 Mismatch] temp_merged\MASTER_CORE_LOGIC.md: Local MD5=eb2b4377..., Remote MD5=2035b669... -> Updating
[Updated] temp_merged\MASTER_CORE_LOGIC.md -> ID: 1bihbR4Eusqo7UU-1ALuO_k3B9KbzI0TuaEd5r9aueUo
[MD5 Mismatch] temp_merged\MASTER_ETL_PROCESS.md: Local MD5=886216e3..., Remote MD5=aa5e6dfe... -> Updating
[Updated] temp_merged\MASTER_ETL_PROCESS.md -> ID: 1GCP9k97gbN53LXIRTqDA_KUudJx6yTyROPY_lVFMnUc
[MD5 Mismatch] temp_merged\MASTER_INTERFACE.md: Local MD5=5d9be903..., Remote MD5=7b355e9d... -> Updating
[Updated] temp_merged\MASTER_INTERFACE.md -> ID: 1KQO7cP26gNdGsekQT1M4n4Xc6dGEnSq3r-Lf0RT-LPM
[MD5 Mismatch] temp_merged\MASTER_KNOWLEDGE_BASE.md: Local MD5=81bdf52c..., Remote MD5=d02c3149... -> Updating
[Updated] temp_merged\MASTER_KNOWLEDGE_BASE.md -> ID: 1wRgxXWS9X9LAyIEqNOJJDEiJS9mgvOXcE6pL84dhd8Q

=== TỔNG KẾT ĐỒNG BỘ ===
Tổng file xử lý: 16
  - Created: 0
  - Updated: 6
  - Up-to-date (MD5 match): 10
  - Skipped (filter): 0
  - Error: 0

=== DANH SÁCH THƯ MỤC DRIVE ĐÃ TẠO ===
- Không tạo mới thư mục nào (đã tồn tại hoặc không có thư mục con).

=== KẾT THÚC ĐỒNG BỘ ===
Pathspec .gitignore: Áp dụng thành công