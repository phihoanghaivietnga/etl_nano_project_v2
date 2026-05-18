# PROJECT_CHRONICLE.md

## 2026-05-09

### Dấu mốc: Xây dựng hệ thống gộp tri thức đa tầng cho NotebookLM
- Thiết lập quy tắc ánh xạ tệp theo 4 nhóm chuẩn: `CORE_LOGIC`, `ETL_PROCESS`, `INTERFACE`, `KNOWLEDGE_BASE`.
- Nâng cấp script `scripts/upload_to_drive_from_local.py` để:
  - Lọc tệp theo `.gitignore` và blacklist cứng.
  - Gộp nội dung theo nhóm vào các file Master trong `temp_merged/`.
  - Bảo tồn ngữ cảnh bằng mục lục nguồn và header `### SOURCE: <đường dẫn tệp>`.
  - Đối soát MD5 trước khi create/update trên Google Drive.
  - Đồng bộ mọi file `.md` dưới dạng Google Docs.
- Cập nhật tài liệu tri thức vận hành để phản ánh luồng mới:
  - Quét file -> Lọc tệp -> Ánh xạ nhóm -> Gộp nội dung -> Đối soát MD5 -> Upload.

### Ý nghĩa kỹ thuật
- Chuẩn hóa đầu vào tri thức cho NotebookLM theo ngữ cảnh chức năng.
- Giảm thời gian đồng bộ nhờ chỉ upload phần sai khác.
- Nâng tính truy vết và khả năng bảo trì tài liệu kỹ thuật theo thời gian.

## 2026-05-11

### Sự cố: Thư mục `tmp_diffsync_demo` đặt sai vị trí trong `docs/knowledge/`
- **Vấn đề**: Thư mục demo `tmp_diffsync_demo/` nằm trong `docs/knowledge/`, gây nhiễu cho bộ não AI (NotebookLM) khi quét tri thức.
- **Nguyên nhân**: Trong lần triển khai trước, thư mục demo được tạo trực tiếp trong `docs/knowledge/` thay vì thư mục gốc project.
- **Cách khắc phục**:
  1. Di chuyển `docs/knowledge/tmp_diffsync_demo/` ra thư mục gốc project (`/tmp_diffsync_demo/`).
  2. Cập nhật `GEM_CODE_MAP.md`: Thay `/docs/v2_knowledge/` bằng `/docs/knowledge/` cho đúng cấu trúc thực tế.
  3. Cập nhật `config/.env`: Đổi `GDRIVE_ROOT_DIR=etl_nano_project_v2` thành `GDRIVE_ROOT_DIR=docs/knowledge` để script quét đúng phạm vi.
  4. Nâng cấp script `upload_to_drive_from_local.py`:
     - Sửa hàm `classify_group_by_path` để xử lý đúng khi `GDRIVE_ROOT_DIR` trỏ đến thư mục con.
     - Thêm `[DESCRIPTION]` metadata vào mục lục mỗi file Master.
     - Bổ sung log chi tiết: lọc file, đối soát MD5, upload/create/update.
- **Bài học kinh nghiệm**:
  - Không bao giờ đặt thư mục demo hay tệp tạm trong `docs/knowledge/` vì đây là nguồn dữ liệu tri thức cho NotebookLM.
  - Mọi thay đổi cấu trúc thư mục cần được ghi nhận ngay vào `PROJECT_CHRONICLE.md` để tránh mất dấu.
  - Script cần có khả năng xử lý cả hai chế độ: root = project root hoặc root = thư mục con (subdirectory).

### Sự cố khẩn cấp: Thu hẹp sai phạm vi quét về `docs/knowledge`
- **Vấn đề**: `GDRIVE_ROOT_DIR` đã bị thu hẹp về `docs/knowledge`, làm mất khả năng quét toàn bộ layer từ gốc dự án.
- **Tác động**:
  - Hàm phân loại theo path không phản ánh đúng kiến trúc tổng thể.
  - Các nhóm Master ngoài `KNOWLEDGE_BASE` có nguy cơ thiếu dữ liệu.
- **Khắc phục đã thực hiện**:
  1. Khôi phục `GDRIVE_ROOT_DIR=etl_nano_project_v2` trong `config/.env`.
  2. Viết lại `classify_group_by_path` theo path vật lý từ root project:
     - `/src/core/` hoặc `/config/` hoặc `.env` -> `CORE_LOGIC`
     - `/src/jobs/` hoặc `/src/db/templates/sql/` -> `ETL_PROCESS`
     - `/src/ui/` hoặc `/scripts/` hoặc `main.py` -> `INTERFACE`
     - `/docs/knowledge/` hoặc file chiến lược root -> `KNOWLEDGE_BASE`
  3. Chuẩn hóa mục lục Master theo dạng `### [PATH] - [DESCRIPTION]`.
  4. Chạy lại đồng bộ toàn dự án để xác thực log và số lượng file theo nhóm.
- **Kết quả**:
  - Script quét từ root project thành công (`ROOT_DIR=.../etl_nano_project_v2`).
  - Group `KNOWLEDGE_BASE` có dữ liệu rõ ràng; mục lục Master đã hiển thị theo format mới.
  - Group `CORE_LOGIC` trong lần chạy hiện tại chưa có nguồn hợp lệ sau lọc vì `src/core` rỗng và các file nhạy cảm trong `config/` bị loại theo chính sách `.gitignore`/forced-exclude.

### Hoàn tất giai đoạn hạ tầng đồng bộ đa nền tảng
- **Mốc thời gian**: 2026-05-11
- **Trạng thái**: Hoàn thành giai đoạn Infrastructure Phase cho luồng tri thức Gemini - Codex - GitHub - Drive - NotebookLM.
- **Giải trình số lượng file bị loại lớn (>2200 file)**:
  - Phần lớn file bị loại nằm trong thư mục môi trường ảo `.venv` và thư mục hệ thống `.git`.
  - Đây là hành vi đúng theo quy tắc lọc `pathspec` + forced exclude để tránh đồng bộ file không phục vụ tri thức nghiệp vụ.
- **Xác nhận cấu trúc `/src/` đang trống**:
  - `src/core/` và `src/jobs/` trống là đúng chủ đích hiện tại.
  - Dự án đang ưu tiên xây dựng pipeline trao đổi tri thức và cơ chế đồng bộ trước khi nạp code nghiệp vụ ETL chi tiết.

## 2026-05-15: Giai đoạn Kiến trúc Dashboard V2

### ADR-01: Kiến trúc Native OOP thay thế Client-Server (API)
- **Quyết định**: Loại bỏ mô hình gọi API HTTP nội bộ qua `API_URL`, chuyển sang gọi trực tiếp logic Python bằng `nicegui.run.io_bound` trong cùng tiến trình.
- **Lý do kiến trúc**: Giảm độ trễ mạng nội bộ, cải thiện phản hồi thời gian thực cho dashboard, đồng thời đơn giản hóa vận hành khi hợp nhất FastAPI và NiceGUI trong kiến trúc single process.

### ADR-02: Quản trị kết nối CSDL bằng DB Context Manager
- **Quyết định**: Chấm dứt kết nối DB vĩnh cửu; mọi truy vấn phải đi qua `get_db_context` và nạp chuỗi kết nối động từ `.env`.
- **Lý do kiến trúc**: Tránh rò rỉ tài nguyên kết nối, giảm nguy cơ treo session kéo dài trên Production, và tăng tính an toàn khi mở rộng số lượng luồng truy vấn đồng thời.

### ADR-03: Bảo vệ CSDL bằng Semaphore toàn cục
- **Quyết định**: Bọc toàn bộ luồng truy vấn song song `asyncio.gather` dưới cơ chế giới hạn đồng thời `MAX_CONCURRENT_CONNECTIONS`.
- **Lý do kiến trúc**: Ngăn tình trạng bắn đồng loạt truy vấn gây quá tải máy chủ nguồn, duy trì khả năng phục vụ ổn định khi UI chạy đối chiếu nhiều bảng hoặc nhiều cơ sở cùng lúc.

### ADR-04: Cách ly trạng thái giao diện (Anti-State Leakage)
- **Quyết định**: Chuẩn hóa pattern wrapper function dưới `@ui.page` để khởi tạo instance class UI mới cho từng request/client.
- **Lý do kiến trúc**: Loại trừ rò rỉ trạng thái giữa các tab hoặc người dùng khác nhau, đảm bảo mỗi phiên giao diện có vòng đời độc lập và an toàn dữ liệu hiển thị.

### ADR-05: Giao diện Multi-Grid All-in-one
- **Quyết định**: Loại bỏ dropdown chọn từng bảng, chuyển sang hiển thị toàn bộ lưới đối chiếu động trên một màn hình theo thứ tự Dim trước, Fact sau.
- **Lý do kiến trúc**: Tách bạch bản chất dữ liệu full-load của dimension và dữ liệu có lọc ngày của transactional/fact, đồng thời giữ tính đúng đắn của cột động theo từng domain mà không trộn nhiễu cấu trúc hiển thị.

## 2026-05-18: Xây dựng khung đồng bộ ETL v1 (Sequential + Selective Sync)

### ADR-06: Chuẩn hóa module điều phối tuần tự có chọn lọc cơ sở
- **Quyết định**: Tạo `src/jobs/sync_orchestrator.py` với class `SyncOrchestrator` chạy tuần tự từng cơ sở, hỗ trợ lọc cơ sở chạy bằng `ACTIVE_FACILITIES` hoặc tham số `run(target_facilities=...)`.
- **Lý do kiến trúc**: Tránh hardcode chạy chết toàn bộ cơ sở trong mọi phiên deploy, cho phép vận hành rollout theo từng cơ sở mục tiêu nhưng vẫn giữ nguyên nguyên tắc tuần tự để bảo vệ Landing dùng chung.

### ADR-07: Chuẩn hóa luồng 2-Hop cho Dimension Full Load
- **Quyết định**: Tạo `src/jobs/dimension_loader.py` (kế thừa `BaseLoader`) để chạy full-load theo 2 chặng:
  1. Production -> ODS cơ sở (TRUNCATE + BCP `-w`).
  2. ODS cơ sở -> Datamart (MERGE template theo domain).
- **Lý do kiến trúc**: Tách rõ luồng danh mục với luồng phát sinh, giữ ODS theo từng cơ sở làm vùng ổn định trước khi đẩy Datamart.

### ADR-08: Chuẩn hóa luồng 3-Hop cho Fact Incremental với Hard Delete an toàn
- **Quyết định**: Tạo `src/jobs/fact_loader.py` (kế thừa `BaseLoader`) với luồng:
  1. Prod -> Landing `stg_nano_v2` (TRUNCATE + BCP delta D-3).
  2. Landing -> ODS cơ sở bằng MERGE có hard delete giới hạn thời gian D-3.
  3. ODS cơ sở -> Datamart bằng MERGE batching `TOP (10000)`.
- **Chốt chặn an toàn đã áp dụng**:
  - Hard delete ở ODS có điều kiện thời gian: chỉ xóa trong cửa sổ `Lookback D-3` đến `to_date`.
  - Hard delete ở Datamart có điều kiện kép: giới hạn D-3 và cô lập theo `NguonDuLieuKey` + `MaCoSo` để không xóa nhầm dữ liệu cơ sở khác.
  - Điều kiện `ON` MERGE Datamart bắt buộc có `Target.NguonDuLieuKey = Source.NguonDuLieuKey` để cô lập business key đa cơ sở.
  - Bảo vệ Landing: TRUNCATE ở đầu và cuối luồng (`finally`) để tránh rò rỉ dữ liệu giữa các phiên cơ sở.

### ADR-09: Chuẩn hóa nghiệp vụ FactThuPhiDichVu 3-in-1 và Seed Data
- **Quyết định**:
  - Công thức DV: `TongTienSauTangGiam = TongTien - ISNULL(TongGiam, 0) + ISNULL(TongTang, 0)`.
  - Công thức BH: `TongTienSauTangGiam = TongTien + ISNULL(TienChenhLech, 0)`.
  - Early arriving facts dùng fallback seed key `-1` cho các khóa dimension (`LuotKhamKey`, `BenhNhanKey`, `DichVuKey`).
- **Lý do kiến trúc**: Giữ tính nhất quán tài chính giữa ODS và Datamart, đồng thời bảo đảm fact không bị rớt bản ghi khi dimension đến trễ.