# MASTER_KNOWLEDGE_BASE.md

## NHÓM: KNOWLEDGE_BASE

## MỤC LỤC NGUỒN
  [DESCRIPTION]: Project documentation and knowledge base

### PROJECT_CHRONICLE.md - Nhật ký thay đổi hạ tầng, sự cố và quyết định kỹ thuật theo mốc thời gian
### README.md - Tổng quan dự án, kiến trúc thư mục và hướng dẫn sử dụng nhanh
### agents.md - Định nghĩa cấu hình và chiến lược điều phối các AI Agent trong hệ thống
### docs/knowledge/GEM_AUTO_PIPELINE.md - Mô tả cơ chế vận hành pipeline tự động
### docs/knowledge/GEM_CODE_MAP.md - Bản đồ cấu trúc mã nguồn và quy tắc ánh xạ nhóm
### docs/knowledge/GEM_CODE_SNIPPETS.md - Thư viện mẫu code chuẩn dùng trong các tình huống phổ biến
### docs/knowledge/GEM_DATA_FLOW.md - Mô tả luồng dữ liệu từ Production qua Staging tới Datamart
### docs/knowledge/GEM_DB_SCHEMAS.md - Đặc tả schema và cấu trúc bảng dữ liệu
### docs/knowledge/GEM_DEPENDENCY_GRAPH.md - Đồ thị phụ thuộc giữa module, lớp và quy trình
### docs/knowledge/GEM_ERROR_CONTEXT.md - Ngữ cảnh lỗi chuẩn hóa và hướng xử lý theo mã lỗi
### docs/knowledge/GEM_GUIDE.md - Thứ tự ưu tiên đọc tài liệu cho từng loại tác vụ
### docs/knowledge/GEM_NAVIGATION.md - Chỉ dẫn điều hướng và tra cứu nhanh các tài liệu tri thức
### docs/knowledge/GEM_SYNC_WORKFLOW.md - Quy trình đồng bộ sai khác và cơ chế Enhanced Merge
### docs/knowledge/GEM_TECHNICAL_STANDARDS.md - Tiêu chuẩn kỹ thuật, bảo mật và xác thực tích hợp
### docs/knowledge/loop_Gem_Github_GoogleDrive_NotebookLM.md - Vòng lặp cộng tác tri thức giữa Gemini, GitHub, Drive và NotebookLM

## NỘI DUNG GỘP

### SOURCE: PROJECT_CHRONICLE.md
```md
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

### ADR-10: Điều chỉnh FULL_LOAD danh mục theo chỉ thị 20260518_1040
- **Quyết định**: Chuẩn hóa `DimensionLoader` chỉ xử lý đúng 4 dimension full-load: `DimBenhNhan`, `DimBenh`, `DimLoaiGoiDichVu`, `DimDichVu` và chỉ dùng lại 4 SQL merge có sẵn (`DimBenhNhan_merge.sql`, `DimBenh_merge.sql`, `DimLoaiGoiDichVu_merge.sql`, `dim_dich_vu_merge.sql`).
- **Điểm bắt buộc đã thực thi**:
  - Gỡ hoàn toàn `DimLuotKham` khỏi `DimensionLoader` để tránh rủi ro `TRUNCATE` sai vào bảng có bản chất incremental.
  - Với `DimDichVu`, pipeline phải chạy Bước 1 liên tiếp cho cả 3 bảng `DMLoaiDichVu`, `DMDichVu`, `DMDichVuChiTiet` vào ODS cơ sở; chỉ sau khi hoàn tất mới chạy Bước 2 gọi `dim_dich_vu_merge.sql`.
  - Luồng cho từng cơ sở vẫn giữ thứ tự tuần tự: chạy xong Dimension mới đến Fact trong `SyncOrchestrator`.

### ADR-11: Thiết lập quân luật kết nối DB để bảo vệ Production
- **Quyết định**: Cập nhật `agents.md` với điều luật cứng:
  - Staging/Datamart được phép chạy lệnh thay đổi dữ liệu và cấu trúc.
  - Production tuyệt đối chỉ được đọc (`SELECT`) hoặc trích xuất (`BCP OUT`), cấm toàn bộ lệnh thay đổi dữ liệu.
- **Áp dụng vào code**:
  - Trong `DimensionLoader`, `TRUNCATE`/`MERGE` chỉ chạy trên connection Datamart/ODS.
  - `production_connection` chỉ dùng cho `bcp queryout` với câu lệnh `SELECT`.

### ADR-12: Nâng cấp giám sát real-time cho FULL_LOAD Dimension
- **Quyết định**: Chuyển cơ chế thực thi BCP trong `DimensionLoader` từ `subprocess.run` sang `subprocess.Popen` để stream log theo thời gian thực, tránh hiện tượng nuốt log khi xử lý bảng lớn (đặc biệt `DimBenhNhan`).
- **Thực thi kỹ thuật**:
  - Override `_log` theo chuẩn timestamp mili-giây và `flush=True` để log ra terminal ngay lập tức.
  - Hai hàm `_run_bcp_queryout` và `_run_bcp_in` đọc `stdout` từng dòng và in trực tiếp trong lúc tiến trình còn chạy.
  - Bổ sung cặp log trạng thái MERGE ở `_execute_dimension_spec`:
    - `[START] Đang thực thi MERGE ODS -> Datamart cho <dimension_name>...`
    - `[SUCCESS] Hoàn thành MERGE <dimension_name>`
- **Ràng buộc an toàn giữ nguyên**:
  - Guard Production ở `_run_bcp_queryout` không thay đổi: chỉ chấp nhận câu lệnh bắt đầu bằng `SELECT`.
  - `TRUNCATE` và `MERGE` tiếp tục chạy trên connection Datamart/ODS.

### ADR-13: Hotfix lỗi kế thừa `_log` do mất đồng bộ chữ ký hàm
- **Sự cố**: Khi chạy Orchestrator phát sinh lỗi `TypeError: DimensionLoader._log() got an unexpected keyword argument 'queue'`.
- **Nguyên nhân**: `BaseLoader.execute_load()` gọi `_log(..., queue=..., loop=...)`, nhưng `DimensionLoader._log` override không có tham số để hứng keyword arguments, vi phạm tính đa hình.
- **Bản vá**:
  - Cập nhật chữ ký hàm thành `def _log(self, message: str, **kwargs) -> None`.
  - Giữ nguyên cơ chế log timestamp mili-giây và `flush=True`.
- **Bài học kinh nghiệm**:
  - Khi override method từ lớp cha có khả năng mở rộng tham số, cần bổ sung `**kwargs` để đảm bảo tương thích ngược và tránh gãy luồng runtime.

### ADR-14: Hotfix Deadlock do Table Lock giữa `pyodbc` và `bcp` subprocess
- **Sự cố**: Pipeline bị treo khi bắt đầu `BCP IN` vào ODS.
- **Nguyên nhân gốc**:
  - `TRUNCATE TABLE` chạy qua `pyodbc` nhưng chưa `commit()` ngay.
  - Session Python giữ table lock, khiến tiến trình `bcp` subprocess không thể ghi vào cùng bảng.
  - Hệ quả là luồng tự chặn lẫn nhau (deadlock/hang) trong cùng pipeline.
- **Bản vá bắt buộc**:
  - Thêm `connection.commit()` ngay sau `self.execute_sql_sync(connection, sql)` trong `_truncate_table` để giải phóng khóa trước khi gọi `BCP IN`.
  - Thêm `connection.commit()` ngay sau `self.execute_sql_sync(connection, merge_sql)` trong `_execute_dimension_spec` để chốt transaction MERGE Datamart.
- **Bài học kinh nghiệm**:
  - Khi phối hợp DDL/DML qua `pyodbc` với tiến trình ngoài (`bcp`), mọi thay đổi có lock phải được commit sớm theo từng bước để tránh lock leak và treo pipeline.

### ADR-15: Hotfix bảo mật log BCP và chuẩn hóa tham số chống lỗi cast
- **Sự cố bảo mật**:
  - Log runtime từng in trực tiếp toàn bộ `command` BCP, có thể lộ thông tin nhạy cảm như server/database/user/password.
- **Sự cố dữ liệu**:
  - `bcp in` thiếu cờ `-k` làm SQL Server dễ phát sinh lỗi `Invalid character value for cast specification` khi gặp chuỗi rỗng cho cột số/ngày.
  - Dấu phân tách cột mặc định không đủ an toàn với dữ liệu y tế chứa ký tự đặc biệt.
- **Bản vá bắt buộc**:
  - Cấm log chi tiết `command` trong `_run_bcp_queryout` và `_run_bcp_in`; chỉ log trung tính (`Đang thực thi BCP OUT...`, `Đang thực thi BCP IN...`).
  - Chuẩn hóa tham số BCP:
    - `BCP OUT`: bắt buộc `-w` và `-t "<|>"`.
    - `BCP IN`: bắt buộc `-w`, `-t "<|>"`, và `-k` (Keep Nulls).
- **Bài học kinh nghiệm**:
  - Bảo mật vận hành phải xem log command như dữ liệu nhạy cảm.
  - Bộ cờ `-w -t "<|>" -k` là cấu hình sống còn để giảm lỗi ép kiểu và xô lệch cột khi nạp dữ liệu Unicode y tế.

### ADR-16: Hotfix cú pháp tham số BCP và che giấu traceback command
- **Sự cố**:
  - Vẫn có nguy cơ lộ thông tin kết nối khi raise `subprocess.CalledProcessError(..., command)` làm traceback in ra full command.
  - Cấu hình tham số BCP dạng tách rời (`-t`, `<|>`) và định dạng kết thúc dòng không chuẩn dễ gây lỗi `Text column data incomplete`/cast sai kiểu.
- **Bản vá bắt buộc**:
  - Chuẩn hóa mảng `command`:
    - `queryout`: `"-w", "-t<|>", "-r\\n", "-q"`
    - `in`: `"-w", "-t<|>", "-k", "-r\\n", "-q"`
  - Thay raise lỗi subprocess bằng lỗi chung:
    - `RuntimeError("Tiến trình BCP thất bại ... Đã ẩn chi tiết command để bảo mật.")`
- **Bài học kinh nghiệm**:
  - Khi dùng `subprocess` cho BCP, cấu trúc list tham số phải đúng cú pháp từng cờ để tránh parser lỗi ngầm.
  - Exception vận hành không được đính kèm command raw nếu command có thể chứa credentials.

### ADR-17: Khai tử BCP CLI, chuyển sang ODBC Bulk Copy (`pyodbc.fast_executemany`)
- **Nguyên nhân gốc rễ**:
  - Dữ liệu HIS Production chứa ký tự ẩn trong text tự do (`\n`, `\r`, `\t`) làm vỡ cấu trúc file `.txt` khi đi qua `bcp queryout`.
  - Khi `bcp in` đọc lại, các dòng bị xô lệch cột, dẫn đến ép kiểu sai (`Invalid character value for cast specification`) vào cột `INT/DATETIME`.
- **Quyết định kiến trúc**:
  - Loại bỏ hoàn toàn đường ống BCP CLI qua `subprocess` và file trung gian `.txt`.
  - Chuyển sang nạp trực tiếp bằng `pyodbc` theo cơ chế parameterized `executemany` để bảo toàn dữ liệu text bẩn.
  - Bật `fast_executemany = True` và chạy chunking 10,000 dòng/lô để tối ưu tốc độ và tránh tràn RAM.
- **Thực thi**:
  - Xóa hai hàm `_run_bcp_queryout` và `_run_bcp_in` khỏi `DimensionLoader`.
  - Viết lại `_copy_prod_to_ods` theo luồng: `SELECT Prod -> fetchmany(10000) -> executemany ODS -> commit theo lô`.
  - Giữ quân luật bảo vệ Production: kết nối Production chỉ dùng cho truy vấn `SELECT`.
- **Bài học kinh nghiệm**:
  - Với dữ liệu y tế giàu text tự do, cơ chế text-file ingestion (BCP OUT/IN) kém bền vững hơn parameterized bulk insert.
  - Kiến trúc ingest native ODBC giúp giảm rủi ro cast/xô cột và giảm bề mặt rò rỉ thông tin vận hành.

### ADR-18: Hotfix MemoryError khi dùng `fast_executemany` với cột MAX
- **Sự cố**:
  - Khi chạy `_copy_prod_to_ods` cho bảng lớn (đặc biệt `DMBenhNhan`), tiến trình văng `MemoryError` ngay từ pha nạp dữ liệu.
- **Nguyên nhân gốc rễ**:
  - Bảng có cột `NVARCHAR(MAX)/VARCHAR(MAX)` khiến ODBC ước lượng bộ nhớ theo kích thước lý thuyết cực đại khi `fast_executemany=True`.
  - Với `chunk_size` lớn (10,000), lượng RAM yêu cầu vượt ngưỡng hệ điều hành.
- **Quyết định kỹ thuật**:
  - Ưu tiên ổn định thay vì tốc độ: tắt `fast_executemany` trong `_copy_prod_to_ods`.
  - Hạ `chunk_size` từ `10000` xuống `1000` để kiểm soát bộ nhớ theo lô.
- **Bài học kinh nghiệm**:
  - Với schema có cột MAX, cần xem `fast_executemany` là tính năng có điều kiện, không bật mặc định.
  - Chunking nhỏ hơn là chi phí hiệu năng cần chấp nhận để đảm bảo an toàn bộ nhớ tuyệt đối.

### ADR-19: Chuyển ma trận vận hành Multi-tenant sang `config/tables.yaml`
- **Bối cảnh**:
  - Quản trị danh sách cơ sở chạy và tham số chunk bằng `.env` trở nên rời rạc, khó mở rộng khi vận hành đa cơ sở.
- **Quyết định**:
  - Chuyển cấu hình vận hành sang `config/tables.yaml` theo 2 khối:
    - `etl_settings`: chứa `odbc_chunk_size`, `active_facilities`.
    - `facilities`: chứa ma trận định danh và schema theo từng `facility_code`.
- **Triển khai**:
  - `SyncOrchestrator` bỏ đọc `ACTIVE_FACILITIES` từ môi trường, chuyển sang đọc `etl_settings.active_facilities` từ YAML.
  - Registry facility được build động từ node `facilities` trong YAML.

### ADR-20: Tenant Injection trong `DimensionLoader` để chống NULL định danh cơ sở
- **Sự cố nghiệp vụ**:
  - Dữ liệu Production mang tính single-tenant, thiếu cột định danh cơ sở khi đẩy lên cấu trúc multi-tenant ở ODS/Datamart.
  - Hệ thống phát sinh lỗi kiểu `Cannot insert the value NULL` cho các cột định danh.
- **Quyết định kỹ thuật**:
  - Tại `_copy_prod_to_ods`, đọc `nguon_dulieu_key` và `co_so_key` từ `config/tables.yaml` theo `facility_code`.
  - Tiêm thêm 3 cột tenant vào payload insert:
    - `NguonDuLieuKey`
    - `CoSoKey`
    - `MaCoSo`
- **Thực thi**:
  - Mở rộng danh sách cột đích: `target_columns = prod_columns + [NguonDuLieuKey, CoSoKey, MaCoSo]`.
  - Mở rộng dữ liệu mỗi dòng trên RAM: `tuple(row) + tenant_values`.
  - Đồng thời đọc `odbc_chunk_size` trực tiếp từ YAML để đồng bộ tham số vận hành.

## 2026-05-19: Tái cấu trúc Incremental động cho Fact theo YAML

### ADR-21: Tách lớp lõi Extractor và chuyển incremental sang cấu hình động
- **Bối cảnh**:
  - Luồng incremental trước đó hardcode danh sách bảng/cột ngày và thiếu cơ chế loại cột theo kiểu dữ liệu.
  - Yêu cầu vận hành mới cần mở rộng bảng incremental theo cấu hình, không chỉnh sửa code lõi mỗi lần thêm bảng.
- **Quyết định kỹ thuật**:
  - Tạo mới `src/core/base_extractor.py` với class `BaseExtractor` và DTO `ExtractPlan`.
  - Chuẩn hóa xử lý ngày theo công thức:
    - `effective_from_date = from_date - lookback_days`.
  - Áp dụng Dynamic SELECT dựa trên `INFORMATION_SCHEMA.COLUMNS` và `exclude_datatypes` từ YAML.
  - Refactor `FactLoader` để đọc toàn bộ `incremental_tables` trong `config/tables.yaml` thành `FactTableSpec`.
  - Giữ nguyên nguyên tắc Datamart:
    - chỉ render placeholder và thực thi SQL template có sẵn,
    - không chỉnh sửa nội dung file SQL template.
- **Module bị ảnh hưởng**:
  - `config/tables.yaml`
  - `src/core/base_extractor.py` (mới)
  - `src/jobs/fact_loader.py`
  - `src/jobs/sync_orchestrator.py`
  - `docs/knowledge/GEM_CODE_MAP.md`
  - `docs/knowledge/GEM_DATA_FLOW.md`
  - `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`

### ADR-22: Hotfix chống treo lock ở tầng Landing khi phối hợp pyodbc và BCP
- **Sự cố**:
  - Có nguy cơ treo dài khi `TRUNCATE` Landing xong nhưng transaction chưa commit, trong khi BCP IN chạy ở session khác.
- **Nguyên nhân gốc**:
  - Lock từ câu lệnh `TRUNCATE` còn giữ trên session `pyodbc`, khiến tiến trình BCP chờ lock.
- **Bản vá**:
  - Trong `FactLoader._truncate_table(...)`, thêm `connection.commit()` ngay sau khi thực thi `TRUNCATE`.
- **Kết quả**:
  - Giải phóng lock sớm giữa các chặng, giảm nguy cơ treo pipeline incremental khi nạp qua BCP.

## 2026-05-20: Hotfix khẩn lỗi lệch schema BCP 22005 và chuẩn hóa bảo mật log kết nối

### ADR-23: Vá lệch schema BCP bằng Masking NULL trong Dynamic SELECT
- **Sự cố**:
  - Pipeline incremental có nguy cơ lỗi `BCP 22005` do danh sách cột extract bị lệch so với bảng Landing/Staging đích.
- **Nguyên nhân gốc**:
  - Logic cũ trong `BaseExtractor` loại bỏ hẳn cột thuộc `exclude_datatypes`, làm thay đổi số lượng và vị trí cột.
- **Quyết định kỹ thuật**:
  - Không loại cột khỏi projection.
  - Với cột thuộc `exclude_datatypes`, mask bằng `CAST(NULL AS VARCHAR(1)) AS [TenCot]`.
  - Giữ nguyên thứ tự cột theo `INFORMATION_SCHEMA.COLUMNS.ORDINAL_POSITION`.
- **Triển khai**:
  - Cập nhật `src/core/base_extractor.py`:
    - Thêm DTO `DynamicColumnProjection`.
    - Mở rộng `ExtractPlan` với `projected_columns`.
    - Refactor `build_dynamic_select_columns(...)` và `build_select_sql(...)` theo cơ chế masking NULL.

### ADR-24: Bịt lỗ hổng rò rỉ thông tin nhạy cảm qua log ETL
- **Sự cố**:
  - Log BCP trước đây có khả năng lộ query/command vận hành, kéo theo rủi ro lộ thông tin kết nối.
- **Quyết định kỹ thuật**:
  - Chuẩn hóa sanitize logging: không log `connection_string`, `PWD/password`, token/secret hoặc raw command nhạy cảm.
- **Triển khai**:
  - Cập nhật `src/core/base_loader.py`:
    - Đổi log BCP sang thông điệp an toàn: ẩn nội dung query/command.

### ADR-25: Củng cố guard doanh thu SMI-3 bằng Regex validator
- **Bối cảnh**:
  - Yêu cầu bắt buộc duy trì cơ chế kiểm duyệt fallback doanh thu `COALESCE/ISNULL` để tránh sai lệch số liệu khi merge Datamart.
- **Quyết định kỹ thuật**:
  - Bổ sung hàm `validate_sql_revenue_rules(...)` trong `FactLoader`.
  - Áp dụng guard theo whitelist template doanh thu:
    - `merge_fact_thuphichvu_3in1.sql`
    - `FactThuPhiDichVu_ThuPhiGoi_merge.sql`
- **Triển khai**:
  - Cập nhật `src/jobs/fact_loader.py` để chạy regex check trước khi `execute_sql_sync(...)`.

### Module bị ảnh hưởng trong đợt thay đổi 2026-05-20
- `src/core/base_extractor.py`
- `src/core/base_loader.py`
- `src/jobs/fact_loader.py`
- `docs/knowledge/GEM_ERROR_CONTEXT.md`
- `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`
- `docs/knowledge/GEM_CODE_MAP.md`
- `PROJECT_CHRONICLE.md`
- `REPORT_CHANGES.md`
- `docs/prompts/20260519_1710_sync_incremental_v2.md`

## 2026-05-20: Điều chỉnh khẩn v3 cho lỗi BCP 22005 (Unicode Masking)

### ADR-26: Chuyển masking NULL sang NVARCHAR(MAX) để tương thích tuyệt đối BCP -w
- **Bối cảnh**:
  - Sau bản vá v2, vẫn ghi nhận tình huống `BCP copy in failed (22005)` khi kiểu che cột chưa đồng nhất tuyệt đối với luồng Unicode rộng.
- **Quyết định kỹ thuật**:
  - Loại bỏ biểu thức `CAST(NULL AS VARCHAR(1))` khỏi Dynamic SELECT.
  - Chuẩn bắt buộc mới: `CAST(NULL AS NVARCHAR(MAX)) AS [TenCot]` cho mọi cột thuộc `exclude_datatypes`.
  - Giữ đối sánh cột 1:1 giữa `physical_columns` và `select_projections` để tránh lệch vị trí khi BCP IN.

### ADR-27: Ghi nhận khoản nợ kỹ thuật theo chỉ thị Master
- Cảnh báo rủi ro (Nợ kỹ thuật): Đã gỡ bỏ cơ chế Validate SQL Fallback Doanh Thu bằng Python theo quyết định của Master. Luồng ETL hiện tại hoàn toàn tin tưởng vào các file SQL Template. Nếu file SQL bị sửa sai, hệ thống sẽ không thể tự động chặn lỗi.

## 2026-05-20: Hotfix khẩn BCP v4 cho luồng Incremental Tầng 1

### ADR-28: Chuẩn hóa parse connection BCP bằng Regex và tách kết nối nguồn/đích
- **Sự cố**:
  - BCP OUT/IN có thời điểm thiếu tham số kết nối, gây thất bại runtime.
  - Luồng trước đó có nguy cơ dùng sai ngữ cảnh kết nối giữa nguồn Production và đích Staging.
- **Quyết định kỹ thuật**:
  - `BaseLoader.parse_connection_string(...)` dùng Regex `re.IGNORECASE` để bóc tách key-value connection string.
  - `run_bcp_utf16le(...)` bắt buộc nhận `source_connection_string` để BCP OUT luôn đi vào DB nguồn.
  - Bổ sung `run_bcp_in(...)` và chuẩn hóa đầy đủ cờ `-w -k -E -t\t -r\n`.
  - Log command BCP IN dạng mask mật khẩu để đối soát mà không lộ `PWD`.

### ADR-29: Chuẩn hóa transaction biên chống deadlock ở Tầng 1
- **Sự cố**:
  - Nếu giữ connection xuyên suốt khi phối hợp `TRUNCATE` và `BCP IN`, pipeline có nguy cơ treo lock.
- **Quyết định kỹ thuật**:
  - Luồng cứng tại `FactLoader`:
    1. BCP OUT thành công.
    2. Mở connection A, `TRUNCATE` landing, `commit()`, đóng connection A ngay.
    3. Gọi BCP IN bằng subprocess session riêng.
    4. Mở connection B mới để chạy các MERGE tầng sau.

### ADR-30: Sửa nhiễu metadata do trailing spaces từ pyodbc
- **Sự cố**:
  - Metadata cột trả về từ `pyodbc` có thể chứa khoảng trắng ở đầu/cuối làm lệch nhận diện datatype.
- **Quyết định kỹ thuật**:
  - Cố định chuẩn tại `BaseExtractor.build_dynamic_select_columns(...)`:
    - `column_name = str(row[0]).strip()`
    - `data_type = str(row[1]).strip().lower()`

## 2026-05-20: Tái cấu trúc Incremental v5 sang Whitelist cột

### ADR-31: Khai tử Black-list `exclude_datatypes`, chuyển sang Whitelist `selected_columns`
- **Bối cảnh**:
  - Cơ chế cũ dựa vào quét metadata và loại trừ theo datatype làm tăng độ phức tạp vận hành và khó kiểm soát hình học cột khi BCP.
- **Quyết định kỹ thuật**:
  - Loại bỏ hoàn toàn `exclude_datatypes` khỏi `config/tables.yaml`.
  - Mỗi bảng incremental bắt buộc khai báo `selected_columns` do quản trị tự kiểm soát.
  - `BaseExtractor` không còn truy vấn `INFORMATION_SCHEMA.COLUMNS`.

### ADR-32: Chuẩn hóa Dynamic SELECT từ Whitelist + enrichment keys
- **Quyết định kỹ thuật**:
  - Dynamic SELECT đọc trực tiếp `selected_columns` theo đúng thứ tự khai báo.
  - Bắt buộc ghép thêm 3 cột enrichment ở cuối projection:
    - `{co_so_key} AS [CoSoKey]`
    - `{nguon_du_lieu_key} AS [NguonDuLieuKey]`
    - `'{ma_co_so}' AS [MaCoSo]`
  - Mục tiêu: giữ đối sánh 100% số lượng/vị trí cột với Landing để chống lệch schema BCP.

### ADR-33: Cô lập transaction biên Tầng 1 chống deadlock
- **Quyết định kỹ thuật**:
  - Chuỗi thao tác bắt buộc:
    1. BCP OUT hoàn tất.
    2. Mở Connection A (đích) -> `TRUNCATE` -> `commit()`.
    3. Đóng Connection A ngay để giải phóng Sch-M lock.
    4. BCP IN bằng subprocess, chờ `exit code == 0`.
    5. Mở Connection B mới để MERGE tầng sau.
  - Đồng thời giữ chuẩn cờ BCP:
    - OUT: `-w -t\t -r\n`
    - IN: `-w -k -E -t\t -r\n`

## 2026-05-20: Tái cấu trúc Incremental v6 quay về PyODBC

### ADR-34: Quyết định chiến lược bỏ BCP cho Incremental
- **Bối cảnh**:
  - Luồng incremental BCP phát sinh nhiều điểm nhạy cảm liên quan hình học cột, transaction boundary và lỗi ép kiểu khi dữ liệu thay đổi.
- **Quyết định kỹ thuật**:
  - Hủy hoàn toàn BCP cho luồng incremental.
  - Quay về kiến trúc nạp dữ liệu bằng PyODBC để tăng độ ổn định implicit casting.
  - Chấp nhận đánh đổi một phần tốc độ bulk, bù bằng Whitelist `selected_columns` để giảm tải bộ nhớ.

### ADR-35: Chuẩn Tầng 1 bằng PyODBC chunking + INSERT tường minh
- **Quyết định kỹ thuật**:
  - Tầng 1 chạy theo chuỗi bắt buộc:
    1. `SELECT` từ Production bằng `cursor.execute(...)`.
    2. `TRUNCATE stg_nano_v2.[TenBang]` đúng 1 lần trước vòng nạp.
    3. Nạp theo chunk `fetchmany(batch_size)` + `executemany(...)`.
    4. `commit()` sau khi nạp xong.
  - Bắt buộc build INSERT động tường minh theo `selected_columns`:
    - `INSERT INTO [stg_nano_v2].[TenBang] ([Col1], [Col2], ...) VALUES (?, ?, ...)`.
  - Cột hệ thống (`MaCoSo`, `CoSoKey`, `NguonDuLieuKey`) không truyền ở Tầng 1, để DB nhận default/NULL hoặc xử lý downstream.

### ADR-36: Bổ sung script đồng bộ Whitelist từ Staging schema
- **Quyết định kỹ thuật**:
  - Thêm script `scripts/sync_selected_columns_from_staging.py` để chuẩn hóa `selected_columns` từ schema `stg_nano_v2`.
  - Script dùng `STAGING_CONNECTION_STRING`, quét `INFORMATION_SCHEMA.COLUMNS` theo `ORDINAL_POSITION`, `.strip()` tên cột, loại `MaCoSo/CoSoKey/NguonDuLieuKey`.
  - Hỗ trợ 2 chế độ:
    - Preview YAML ra terminal.
    - Ghi trực tiếp vào `config/tables.yaml` bằng cờ `--write`.

## 2026-05-20: Hotfix Incremental v7 cho lỗi IDENTITY_INSERT 544

### ADR-37: Mô phỏng cờ BCP `-E` bằng Identity Insert động trong PyODBC
- **Sự cố**:
  - Luồng nạp Tầng 1 bằng PyODBC phát sinh lỗi SQL Server 544 (`IDENTITY_INSERT is set to OFF`) khi bảng Landing có cột IDENTITY.
- **Quyết định kỹ thuật**:
  - Trước vòng nạp chunking, bắt buộc kiểm tra metadata động:
    - `SELECT OBJECTPROPERTY(OBJECT_ID('stg_nano_v2.[TenBang]'), 'TableHasIdentity')`.
  - Nếu bảng có identity (`TableHasIdentity = 1`):
    - Bật `SET IDENTITY_INSERT stg_nano_v2.[TenBang] ON` trước vòng `executemany`.
    - Bọc toàn bộ vòng nạp trong khối `try...finally`.
    - Trong `finally`, bắt buộc tắt lại `SET IDENTITY_INSERT ... OFF` để trả trạng thái an toàn, tránh treo session.
- **Phạm vi áp dụng**:
  - `src/jobs/fact_loader.py`, trong Tầng 1 `SELECT -> TRUNCATE -> executemany` của incremental pipeline.

## 2026-05-21: Quyết định kiến trúc tối hậu cho Incremental Tầng 1

### ADR-38: Tắt hoàn toàn `fast_executemany` để bảo vệ bộ nhớ tuyệt đối
- **Bối cảnh**:
  - Luồng Incremental Tầng 1 có nguy cơ `MemoryError` khi bảng chứa cột `NVARCHAR(MAX)/VARCHAR(MAX)` do cơ chế cấp phát bộ nhớ tĩnh lớn của ODBC khi bật `fast_executemany`.
- **Quyết định kiến trúc tối hậu**:
  - Tắt vĩnh viễn `fast_executemany` trong `_load_to_global_staging` của `FactLoader`.
  - Chấp nhận tốc độ nạp Row-by-Row ngầm của PyODBC để đổi lấy an toàn bộ nhớ 100%.
  - Khai tử cơ chế fallback tăng/giảm `fast_executemany` trong runtime để giảm độ phức tạp và tránh hành vi khó dự đoán.
- **Ràng buộc bắt buộc giữ nguyên**:
  - `TRUNCATE` Landing vẫn nằm ngoài vòng lặp chunking.
  - `INSERT INTO ... VALUES ...` động theo danh sách `selected_columns` vẫn giữ nguyên.
  - Kiểm tra động `TableHasIdentity` và khối `try...finally` bật/tắt `IDENTITY_INSERT` vẫn giữ nguyên.

## 2026-05-21: Tái cấu trúc Manual Runner theo pipeline đa chặng từ Production

### ADR-39: Manual Runner điều phối động theo bảng chọn, cô lập chạy đơn đối tượng
- **Bối cảnh**:
  - Màn hình Manual Runner trước đây dùng `GenericTableLoader`, chủ yếu chạy MERGE chặng cuối Datamart.
  - Nhu cầu nghiệp vụ yêu cầu bấm Run từ UI phải kích hoạt đầy đủ luồng ETL theo bảng chọn, đi từ Production xuyên qua các tầng trung gian.
- **Quyết định kỹ thuật**:
  - Loại bỏ `GenericTableLoader` khỏi `src/ui/pages/manual_runner_page.py`.
  - Điều phối động theo `config/tables.yaml`:
    - Nếu bảng thuộc `incremental_tables`: khởi tạo `FactLoader` và truyền `from_date/to_date` từ UI.
    - Nếu thuộc danh mục full-load: khởi tạo `DimensionLoader` để chạy full theo dimension mục tiêu.
  - Mở rộng loader để cô lập tiến trình chạy đơn đối tượng:
    - `FactLoader(..., target_table_name=...)` chỉ chạy đúng 1 `FactTableSpec`.
    - `DimensionLoader(..., target_dimension_name=...)` chỉ chạy đúng 1 `DimensionTableSpec`.
- **Ràng buộc an toàn tiếp tục giữ nguyên**:
  - Chặng nạp global landing của Fact vẫn giữ `fast_executemany = False`.
  - Không thay đổi thuật ngữ nghiệp vụ tiếng Việt gốc và không làm sai lệch quy tắc fallback doanh thu hiện hành trong SQL template.

## 2026-05-21

### Dấu mốc: Đóng gói cụm bảng doanh thu 3-in-1 trên Manual Runner
- **Vấn đề**: Dữ liệu tài chính trên màn hình Manual Runner bị phân mảnh do 3 bảng ThuPhiBaoHiem, ThuPhiTangGiam, ThuPhiDichVu hiển thị độc lập, dễ gây nhầm lẫn người dùng khi chỉ chạy 1 bảng mà thiếu 2 bảng còn lại.
- **Quyết định kỹ thuật**:
  - Gom 3 bảng doanh thu thành một thực thể đồng bộ hợp nhất mang tên `ThuPhiDichVu` trên UI.
  - `src/ui/pages/manual_runner_page.py`: Xóa `ThuPhiBaoHiem` và `ThuPhiTangGiam` khỏi combobox.
  - `src/jobs/fact_loader.py`: Khi `target_table_name == "ThuPhiDichVu"`, thiết lập ma trận `CLUSTER = {"ThuPhiBaoHiem", "ThuPhiTangGiam", "ThuPhiDichVu"}` và duyệt nạp tuần tự.
- **Luồng dữ liệu cho cụm ThuPhiDichVu**:
  1. Prod -> Landing transient cho từng bảng trong cụm.
  2. Landing -> ODS cơ sở cho từng bảng.
  3. ODS -> Datamart qua template `merge_fact_thuphichvu_3in1.sql`.
- **Tác động tài liệu**:
  - `docs/knowledge/GEM_CODE_MAP.md`: Bổ sung mục v2 trong nhóm INTERFACE.
  - `docs/knowledge/GEM_DATA_FLOW.md`: Cập nhật ma trận xử lý Manual Pipeline cho cụm 3 bảng.
  - `PROJECT_CHRONICLE.md`: Mô tả dấu mốc này.
  - `REPORT_CHANGES.md`: Ghi nhận thay đổi files và lý do.
```

### SOURCE: README.md
```md
# ETL NANO PROJECT V2

## 1. Mục đích hệ thống
Hệ thống ETL phiên bản v2 được thiết kế để chuẩn hóa luồng dữ liệu từ Production sang Datamart theo kiến trúc Modular và lập trình hướng đối tượng (OOP). Hệ thống đảm bảo tính thống nhất giữa chế độ chạy Tự động (Auto) và Thủ công (Manual).
Hy vọng test lần cuối
Lần cuối 2
Lần cuối 3

## 2. Cấu trúc thư mục
ETL_Nano_Project_V2/
├── agents.md               # File chiến lược điều phối hệ thống
├── README.md               # Hướng dẫn tổng quan dự án
├── .env                    # Lưu trữ biến môi trường và kết nối DB
├── config/                 # Cấu hình hệ thống và danh sách bảng
├── docs/
│   ├── knowledge/       # Tầng tri thức GEM
		├── GEM_NAVIGATION.md: Chỉ dẫn tìm kiếm tri thức.
		├── GEM_GUIDE.md: Thứ tự ưu tiên đọc tài liệu.
		├── GEM_CODE_MAP.md: Sơ đồ các lớp và hàm trong mã nguồn.
		├── GEM_CODE_SNIPPETS.md: Thư viện mã mẫu chuẩn.
		├── GEM_DATA_FLOW.md: Mô tả luồng dữ liệu Production -> Staging -> Datamart.
		├── GEM_DB_SCHEMAS.md: Chi tiết cấu trúc bảng và schema database.
		├── GEM_AUTO_PIPELINE.md: Chi tiết vận hành engine chạy tự động.
		├── GEM_DEPENDENCY_GRAPH.md: Đồ thị mối quan hệ giữa các module.
		├── GEM_ERROR_CONTEXT.md: Bối cảnh và cách xử lý các mã lỗi (E-ID).
		├── GEM_TECHNICAL_STANDARDS.md: Tiêu chuẩn kỹ thuật và xác thực Google Drive.
		├── GEM_SYNC_WORKFLOW.md: Quy trình đồng bộ sai khác (Diff Sync) giữa local và Google Drive.
│   └── archive/            # Lưu trữ tài liệu phiên bản cũ
├── scripts/                # CÁC SCRIPT VẬN HÀNH VÀ TỰ ĐỘNG HÓA
│   └── upload_to_drive.py  # Script đồng bộ tri thức lên Google Drive
├── src/                    # Mã nguồn chính của ứng dụng, phân tách giữa Core logic và Job thực thi.
│   ├── core/               # Lớp cha, Logger, Database Connection
│   ├── jobs/               # Logic đồng bộ các bảng cụ thể
│   ├── ui/                 # Giao diện Streamlit (Runner & Verify)
│   └── db/
│       └── templates/sql/  # Nguồn SQL MERGE duy nhất
├── tests/                  # Script kiểm thử độc lập
└── .github/
    └── workflows/
        └── sync_to_drive.yml # File cấu hình Trigger GitHub Actions

## 3. Ý nghĩa các file GEM tri thức (docs/knowledge/)
- GEM_NAVIGATION.md: Chỉ dẫn tìm kiếm tri thức.
- GEM_GUIDE.md: Thứ tự ưu tiên đọc tài liệu.
- GEM_CODE_MAP.md: Sơ đồ các lớp và hàm trong mã nguồn.
- GEM_CODE_SNIPPETS.md: Thư viện mã mẫu chuẩn.
- GEM_DATA_FLOW.md: Mô tả luồng dữ liệu Production -> Staging -> Datamart.
- GEM_DB_SCHEMAS.md: Chi tiết cấu trúc bảng và schema database.
- GEM_AUTO_PIPELINE.md: Chi tiết vận hành engine chạy tự động.
- GEM_DEPENDENCY_GRAPH.md: Đồ thị mối quan hệ giữa các module.
- GEM_ERROR_CONTEXT.md: Bối cảnh và cách xử lý các mã lỗi (E-ID).
- GEM_TECHNICAL_STANDARDS.md: Tiêu chuẩn kỹ thuật và xác thực Google Drive.
- GEM_SYNC_WORKFLOW.md: Quy trình đồng bộ sai khác (Diff Sync) giữa local và Google Drive.
```

### SOURCE: agents.md
```md
# CHIẾN LƯỢC ĐIỀU PHỐI HỆ THỐNG AGENTS

## 1. Vai trò
- Gem (Kiến trúc sư): Điều phối, ra lệnh và giám sát dựa trên Tầng tri thức.
- Codex (Thợ code): Thực thi lập trình, sửa lỗi và cập nhật tài liệu.

## 2. Giao thức làm việc
- Bước 1: Trước khi sửa code, Codex bắt buộc phải đọc các tệp GEM_xxx.md liên quan để nắm ngữ cảnh.
- Bước 2: Thực hiện sửa đổi mã nguồn.
- Bước 3: Cập nhật đúng và đủ các thay đổi vào Tầng tri thức (GEM_xxx.md) để đảm bảo tính nhất quán.
- Bước 4: Kết xuất báo cáo vào tệp REPORT_CHANGES.md tại thư mục gốc.

## 3. Quy tắc bắt buộc
- Ngôn ngữ: Tiếng Việt rõ ràng, ngắn gọn, cô đọng.
- Hình thức: Không sử dụng icon trong mọi tệp tài liệu .md.
- Kỹ thuật: Mọi mã nguồn phải theo hướng đối tượng (OOP), kế thừa từ Base Class tại src/core.

## 3.1. Điều luật kết nối cơ sở dữ liệu
- KẾT NỐI STAGING & DATAMART: Được phép thực thi các câu lệnh thay đổi dữ liệu và cấu trúc (TRUNCATE, INSERT, UPDATE, DELETE, MERGE, ALTER, CREATE).
- KẾT NỐI PRODUCTION: TUYỆT ĐỐI CẤM mọi câu lệnh làm thay đổi dữ liệu (CREATE, UPDATE, DELETE, TRUNCATE, ALTER, DROP, INSERT). Kết nối đến Production CHỈ ĐƯỢC PHÉP sử dụng để ĐỌC (SELECT) hoặc dùng cho công cụ trích xuất (BCP OUT).

## 4. Cấu trúc thư mục
ETL_Nano_Project_V2/
├── agents.md               # File chiến lược điều phối hệ thống
├── README.md               # Hướng dẫn tổng quan dự án
├── PROJECT_CHRONICLE.md    # Nhật ký tiến hóa của dự án
├── .env                    # Lưu trữ biến môi trường và kết nối DB
├── config/                 # Cấu hình hệ thống và danh sách bảng
├── docs/
│   ├── knowledge/       # Tầng tri thức GEM
		├── GEM_NAVIGATION.md: Chỉ dẫn tìm kiếm tri thức.
		├── GEM_GUIDE.md: Thứ tự ưu tiên đọc tài liệu.
		├── GEM_CODE_MAP.md: Sơ đồ các lớp và hàm trong mã nguồn.
		├── GEM_CODE_SNIPPETS.md: Thư viện mã mẫu chuẩn.
		├── GEM_DATA_FLOW.md: Mô tả luồng dữ liệu Production -> Staging -> Datamart.
		├── GEM_DB_SCHEMAS.md: Chi tiết cấu trúc bảng và schema database.
		├── GEM_AUTO_PIPELINE.md: Chi tiết vận hành engine chạy tự động.
		├── GEM_DEPENDENCY_GRAPH.md: Đồ thị mối quan hệ giữa các module.
		├── GEM_ERROR_CONTEXT.md: Bối cảnh và cách xử lý các mã lỗi (E-ID).
		├── GEM_TECHNICAL_STANDARDS.md: Tiêu chuẩn kỹ thuật và xác thực Google Drive.
		├── GEM_SYNC_WORKFLOW.md: Quy trình đồng bộ sai khác (Diff Sync) giữa local và Google Drive.
│   └── archive/            # Lưu trữ tài liệu phiên bản cũ
├── scripts/                # CÁC SCRIPT VẬN HÀNH VÀ TỰ ĐỘNG HÓA
│   └── upload_to_drive.py  # Script đồng bộ tri thức lên Google Drive
├── src/                    # Mã nguồn chính của ứng dụng
│   ├── core/               # Lớp cha, Logger, Database Connection
│   ├── jobs/               # Logic đồng bộ các bảng cụ thể
│   ├── ui/                 # Giao diện Streamlit (Runner & Verify)
│   └── db/
│       └── templates/sql/  # Nguồn SQL MERGE duy nhất
├── tests/                  # Script kiểm thử độc lập
└── .github/
    └── workflows/
        └── sync_to_drive.yml # File cấu hình Trigger GitHub Actions
```

### SOURCE: docs/knowledge/GEM_AUTO_PIPELINE.md
```md
# GEM_AUTO_PIPELINE.md

## Mục tiêu
- Chuẩn hóa engine tự động chạy ETL theo chiến lược tuần tự an toàn Landing.
- Hỗ trợ vận hành chọn lọc cơ sở để phục vụ deploy theo pha.

## Module điều phối
- Tệp: `src/jobs/sync_orchestrator.py`
- Lớp: `SyncOrchestrator`

## Quy tắc điều phối bắt buộc
1. Chạy tuần tự từng cơ sở, không chạy song song giữa các cơ sở.
2. Cơ sở hiện tại phải hoàn tất toàn bộ Dimension + Fact + cleanup Landing trước khi sang cơ sở kế tiếp.
3. Nếu có lỗi tại một cơ sở thì dừng luồng tuần tự để tránh lan lỗi.

## Selective Sync
- Hỗ trợ 2 cách chọn cơ sở chạy:
  - Cấu hình YAML: `config/tables.yaml` -> `etl_settings.active_facilities`
  - Tham số hàm: `run(target_facilities=['hanoi'])`
- Nếu không truyền hoặc nhận `ALL` thì chạy toàn bộ facility đã định nghĩa.
- Facility ngoài scope không được khởi tạo connection.

## Cấu hình vận hành tập trung (YAML)
- File chuẩn: `config/tables.yaml`
- Khối `etl_settings`:
  - `odbc_chunk_size`: kích thước lô nạp ODBC cho DimensionLoader.
  - `active_facilities`: danh sách cơ sở mặc định cho orchestrator.
- Khối `facilities.<facility_code>`:
  - `nguon_dulieu_key`, `co_so_key`, `staging_schema`.
- Quy tắc: ưu tiên YAML làm nguồn cấu hình chính cho matrix multi-tenant; `.env` chỉ giữ chuỗi kết nối.

## Input connection chuẩn
- Datamart: `DATAMART_CONNECTION_STRING`
- Production theo cơ sở:
  - `PROD_CONNECTION_HANOI`
  - `PROD_CONNECTION_HCM`
  - `PROD_CONNECTION_HALONG`
  - `PROD_CONNECTION_HAIPHONG`

## Luồng gọi loader
- Dimension: `src/jobs/dimension_loader.py`
- Fact: `src/jobs/fact_loader.py`
- Trình tự gọi trong mỗi facility:
  1. `DimensionLoader.execute_load(...)`
  2. `FactLoader.execute_load(...)`

## Chốt chặn vận hành
- FactLoader luôn dọn Landing ở đầu và cuối luồng.
- Hard delete incremental chỉ được áp dụng trong cửa sổ D-3 và đúng phạm vi cơ sở.
- MERGE Fact lên Datamart bắt buộc cô lập theo `NguonDuLieuKey`.

## Cơ chế Giám sát (Monitoring)
- Áp dụng tại `DimensionLoader`:
  - Log runtime dùng timestamp đến mili-giây theo format `YYYY-MM-DD HH:MM:SS.mmm` và `flush=True`.
  - Luồng ODBC copy log tiến độ theo tổng số dòng đã nạp từng lô.
  - Trạng thái MERGE ODS -> Datamart có log rõ ràng theo cặp:
    - `[START] Đang thực thi MERGE ODS -> Datamart cho <dimension_name>...`
    - `[SUCCESS] Hoàn thành MERGE <dimension_name>`
```

### SOURCE: docs/knowledge/GEM_CODE_MAP.md
```md
# GEM_CODE_MAP.md

## Mục tiêu cập nhật
- Chuẩn hóa quy tắc ánh xạ tệp theo nhóm tri thức để phục vụ điều phối lâu dài.
- Làm cơ sở gộp file Master cho quy trình tạo tri thức đưa vào NotebookLM.

## Bảng quy tắc ánh xạ nhóm

### Nhóm CORE_LOGIC
- Phạm vi:
  - `/src/core/`
  - `/config/`
  - Tệp `.env` tại root
- File Master tương ứng: `MASTER_CORE_LOGIC.md`

### Nhóm ETL_PROCESS
- Phạm vi:
  - `/src/jobs/`
  - `/src/db/templates/sql/`
- File Master tương ứng: `MASTER_ETL_PROCESS.md`

#### Bổ sung theo yêu cầu 20260518_0900_xay_dung_khung_dong_bo_v1
- Module điều phối ETL tuần tự có hỗ trợ Selective Sync:
  - `src/jobs/sync_orchestrator.py`
  - Chức năng chính:
    - Class `SyncOrchestrator` điều phối tuần tự theo facility.
    - Hỗ trợ lọc cơ sở chạy bằng `etl_settings.active_facilities` trong `config/tables.yaml` hoặc tham số `run(target_facilities=...)`.
    - Chỉ map/khởi tạo connection theo facility được chọn, bỏ qua facility ngoài scope.
- Module nạp Dimension full load 2-Hop:
  - `src/jobs/dimension_loader.py`
  - Chức năng chính:
    - Class `DimensionLoader` kế thừa `BaseLoader`.
    - Luồng Production -> ODS cơ sở bằng ODBC Bulk Copy native (`pyodbc.executemany`).
    - Luồng ODS cơ sở -> Datamart bằng MERGE SQL template có sẵn.
    - Logging real-time cho full-load:
      - Hàm `_log(self, message: str, **kwargs)` in timestamp đến mili-giây và `flush=True`.
      - `**kwargs` được dùng để tương thích đa hình với `BaseLoader._log(..., queue=..., loop=...)` trong luồng orchestrator.
      - Hàm `_copy_prod_to_ods(...)` đọc `odbc_chunk_size` từ `config/tables.yaml`.
      - Hàm `_copy_prod_to_ods(...)` đọc cấu hình facility từ YAML để lấy `nguon_dulieu_key` và `co_so_key` theo `facility_code`.
      - Hàm `_copy_prod_to_ods(...)` tự động Tenant Injection bằng cách nối thêm 3 cột `NguonDuLieuKey`, `CoSoKey`, `MaCoSo` vào payload insert ODS.
      - Chunking theo tham số YAML + commit theo lô để cân bằng hiệu năng và an toàn bộ nhớ.
      - Guard an toàn Production giữ nguyên: connection Production chỉ dùng truy vấn `SELECT`.
      - Trạng thái MERGE có cặp log `[START]` và `[SUCCESS]` trong `_execute_dimension_spec`.

#### Bổ sung theo yêu cầu 20260518_1040_xay_dung_luong_full_load_v1
- Chuẩn hóa phạm vi FULL_LOAD trong `DimensionLoader` chỉ còn đúng 4 dimension:
  - `DimBenhNhan`: `DMBenhNhan` -> `DimBenhNhan_merge.sql`
  - `DimBenh`: `DMBenh` -> `DimBenh_merge.sql`
  - `DimLoaiGoiDichVu`: `LoaiGoiDichVuNT` -> `DimLoaiGoiDichVu_merge.sql`
  - `DimDichVu`: (`DMLoaiDichVu`, `DMDichVu`, `DMDichVuChiTiet`) -> `dim_dich_vu_merge.sql`
- Quy tắc đặc biệt DimDichVu:
  - Bắt buộc chạy BCP đủ 3 bảng vào ODS trước khi gọi MERGE Datamart.
- Nợ kỹ thuật đã xử lý:
  - Gỡ `DimLuotKham` khỏi `DimensionLoader` để tránh `TRUNCATE` nhầm lên bảng có bản chất incremental.
  - Trạng thái theo dõi ở luồng Fact: `FactLoader.PENDING_INCREMENTAL_DIMENSIONS = ("DimLuotKham",)`.
- Quân luật an toàn DB trong `DimensionLoader`:
  - `production_connection` chỉ dùng cho `SELECT`/`BCP OUT`.
  - `TRUNCATE` và `MERGE` chỉ thực thi bằng connection Datamart/ODS.
- Module nạp Fact incremental 3-Hop:
  - `src/jobs/fact_loader.py`
  - Chức năng chính:
    - Class `FactLoader` kế thừa `BaseLoader`.
    - Luồng Prod -> Landing `stg_nano_v2` theo cửa sổ trượt D-3.
    - Luồng Landing -> ODS bằng MERGE có hard delete giới hạn D-3.
    - Luồng ODS -> Datamart bằng MERGE batching `TOP (10000)`.
    - Áp dụng fallback seed key `-1` cho early arriving facts.
    - Dọn Landing ở đầu và cuối luồng để chống rò rỉ dữ liệu giữa facilities.

#### Bổ sung theo yêu cầu 20260519_1315_sync_incremental_v1
- Cấu phần lõi mới cho incremental động:
  - `src/core/base_extractor.py`
  - Chức năng chính:
    - `ExtractPlan`: DTO mô tả kế hoạch extract (`table_name`, `date_column`, `effective_from_date`, `to_date`, `select_sql`, `selected_columns`, `projected_columns`).
    - `DynamicColumnProjection`: DTO cột động gồm `column_name`, `data_type`, `select_expression`, `is_masked`.
    - `BaseExtractor.normalize_date(...)`: chuẩn hóa input ngày (`date`, `datetime`, `YYYY-MM-DD`).
    - `BaseExtractor.compute_effective_from_date(...)`: áp dụng lookback động `from_date - lookback_days`.
    - `BaseExtractor.build_dynamic_select_columns(...)`: đọc metadata từ `INFORMATION_SCHEMA.COLUMNS`, giữ đủ thứ tự cột theo `ORDINAL_POSITION` và mask cột thuộc `exclude_datatypes` bằng `CAST(NULL AS VARCHAR(1)) AS [TenCot]`.
    - `BaseExtractor.build_select_sql(...)`: sinh Dynamic SELECT theo projection expressions đã mask để chống lệch schema BCP (`22005`).
- Tái cấu trúc `src/jobs/fact_loader.py` theo ma trận YAML:
  - Đọc node `incremental_tables` từ `config/tables.yaml` thành `FactTableSpec`.
  - Bỏ hardcode danh sách bảng fact, chuyển sang cấu hình động theo từng bảng.
  - Bổ sung guard `validate_sql_revenue_rules(...)` (Regex) để bảo vệ logic fallback doanh thu `COALESCE/ISNULL` trên các template doanh thu.
  - Luồng 3 tầng chuẩn hóa:
    1. Tầng 1: `TRUNCATE` global landing `stg_nano_v2` + BCP `-w`.
    2. Tầng 2: MERGE từ landing sang facility staging, không dùng `TRUNCATE`.
    3. Tầng 3: thực thi SQL template có sẵn qua `merge_script`, không sửa file SQL template.
  - Bổ sung chốt chống treo lock:
    - Sau `TRUNCATE` landing có `connection.commit()` ngay để tránh lock chờ giữa `pyodbc` session và tiến trình BCP IN.
  - Bổ sung chốt sanitize logging:
    - `src/core/base_loader.py` ẩn nội dung query/command khi log BCP UTF-16-LE để tránh rò rỉ thông tin nhạy cảm.
- Cập nhật điều phối:
  - `src/jobs/sync_orchestrator.py` truyền `tables_config_path` vào `FactLoader` để đồng bộ cùng một nguồn cấu hình YAML.
- Mở rộng cấu hình:
  - `config/tables.yaml` có node `incremental_tables` cho các bảng:
    - `ThuPhiDichVu`, `ThuPhiBaoHiem`, `ThuPhiTangGiam` (date: `NgayDenKham`)
    - `ThuPhiGoi` (date: `NgayThu`)
    - `DoThiLuc` (date: `NgayDo`)
    - `HoSoKhamBenhNgoaiTru` (date: `NgayVaoKham`, type `fact`, merge `DimLuotKham_merge.sql`)

#### Bổ sung theo yêu cầu 20260520_1110_sync_incremental_v4
- Chuẩn hóa xử lý metadata cột ở `src/core/base_extractor.py`:
  - Trong `BaseExtractor.build_dynamic_select_columns(...)`, bắt buộc `.strip()` ngay tại điểm đọc metadata từ `pyodbc`:
    - `column_name = str(row[0]).strip()`
    - `data_type = str(row[1]).strip().lower()`
- Bổ sung năng lực BCP chuẩn ở `src/core/base_loader.py`:
  - `BaseLoader.parse_connection_string(...)` dùng Regex `re.IGNORECASE` để bóc tách connection string.
  - `BaseLoader._build_bcp_connection_args(...)` map tham số kết nối cho BCP: `-S`, `-d`, và auth `-U/-P` hoặc `-T`.
  - `BaseLoader.run_bcp_utf16le(...)` nhận thêm `source_connection_string` để bắt buộc BCP OUT dùng kết nối nguồn Production.
  - `BaseLoader.run_bcp_in(...)` mới cho BCP IN, bắt buộc đủ cờ: `-w`, `-k`, `-E`, `-t\t`, `-r\n`.
  - `BaseLoader._mask_bcp_command(...)` dùng để log command BCP IN có che mật khẩu.
- Chuẩn hóa transaction biên trong `src/jobs/fact_loader.py`:
  - Tầng 1 chạy theo thứ tự cứng:
    1. BCP OUT từ Production.
    2. Mở connection A -> `TRUNCATE` Landing -> `commit()` -> đóng connection A.
    3. BCP IN vào Landing bằng session subprocess riêng.
    4. Mở connection B mới để chạy các bước MERGE tầng sau.

#### Bổ sung theo yêu cầu 20260520_1435_sync_incremental_v5
- Chuyển kiến trúc incremental từ Black-list sang Whitelist cột:
  - `config/tables.yaml`:
    - Xóa toàn bộ `exclude_datatypes`.
    - Mỗi bảng incremental bắt buộc khai báo `selected_columns`.
- Vai trò mới của `src/core/base_extractor.py`:
  - Không còn quét `INFORMATION_SCHEMA.COLUMNS`.
  - Không còn `DynamicColumnProjection` và logic masking datatype.
  - Sinh Dynamic SELECT trực tiếp từ `selected_columns`.
  - Tự ghép 3 cột enrichment vào projection:
    - `{co_so_key} AS [CoSoKey]`
    - `{nguon_du_lieu_key} AS [NguonDuLieuKey]`
    - `'{ma_co_so}' AS [MaCoSo]`
- Vai trò mới của `src/jobs/fact_loader.py`:
  - `FactTableSpec` đổi sang giữ `selected_columns`.
  - `build_extract_plan(...)` nhận trực tiếp `selected_columns` + 3 biến ngữ cảnh (`co_so_key`, `nguon_du_lieu_key`, `ma_co_so`).
  - Luồng Tầng 1 giữ biên giao dịch cô lập chống deadlock:
    1. BCP OUT hoàn tất.
    2. Connection A: `TRUNCATE` + `commit()` + đóng ngay.
    3. BCP IN bằng subprocess session riêng.
    4. Connection B mới để chạy MERGE tầng sau.

#### Bổ sung theo yêu cầu 20260520_1540_sync_incremental_v6
- Quyết định chiến lược mới cho Incremental:
  - Hủy hoàn toàn BCP trong luồng incremental.
  - Quay về pipeline PyODBC để ổn định ép kiểu ngầm (implicit casting).
- `src/core/base_extractor.py`:
  - `build_extract_plan(...)` chỉ còn nhận `selected_columns`.
  - Dynamic SELECT chỉ gồm các cột Whitelist, không ghép enrichment projection vào câu SELECT.
- `src/core/base_loader.py`:
  - Loại bỏ các hàm và tiện ích BCP:
    - `parse_connection_string(...)`
    - `_build_bcp_connection_args(...)`
    - `_mask_bcp_command(...)`
    - `run_bcp_utf16le(...)`
    - `run_bcp_in(...)`
- `src/jobs/fact_loader.py`:
  - Tầng 1 chuyển sang nạp PyODBC theo chunk:
    1. `cursor.execute(select_sql)` trên connection Production.
    2. `TRUNCATE stg_nano_v2.[TenBang]` đúng 1 lần trước vòng lặp.
    3. Dùng `fetchmany(batch_size)` + `executemany(...)` để nạp dữ liệu.
    4. `commit()` sau khi nạp xong Tầng 1.
  - Bắt buộc INSERT động tường minh:
    - `INSERT INTO [stg_nano_v2].[TenBang] ([Col1], [Col2], ...) VALUES (?, ?, ...)`.
  - Vẫn giữ kiến trúc Staging 3 tầng:
    - Tầng 1: Landing transient.
    - Tầng 2: MERGE landing -> facility staging.
    - Tầng 3: MERGE facility staging -> datamart.
- Script vận hành mới:
  - `scripts/sync_selected_columns_from_staging.py`:
    - Kết nối bằng `STAGING_CONNECTION_STRING`.
    - Quét `INFORMATION_SCHEMA.COLUMNS` theo `ORDINAL_POSITION` cho 6 bảng incremental.
    - `.strip()` tên cột, loại `MaCoSo/CoSoKey/NguonDuLieuKey`.
    - In preview YAML hoặc ghi trực tiếp `selected_columns` vào `config/tables.yaml` (`--write`).

### Nhóm INTERFACE
- Phạm vi:
  - `/src/ui/`
  - `/scripts/`
  - `main.py` tại root
- File Master tương ứng: `MASTER_INTERFACE.md`

#### Bổ sung theo yêu cầu 20260514_1420_tao_man_hinh_dashboard_doi_chieu_v1
- File UI mới:
  - `src/ui/dashboard_app.py`
- File lõi dùng chung phục vụ UI Manual Runner:
  - `src/core/base_ui.py`
  - `src/core/base_loader.py`
- SQL template đối chiếu dùng cho màn hình giao diện:
  - `src/db/templates/sql/dashboard_doichieu/ho_so_kham_benh_ngoai_tru_doi_chieu.sql`

#### Bổ sung theo yêu cầu 20260515_0835_tao_man_hinh_dashboard_doi_chieu_v2
- Entry UI mới theo mô hình phân trang:
  - `src/ui/main_app.py`
- Trang giao diện tách file độc lập:
  - `src/ui/pages/__init__.py`
  - `src/ui/pages/common.py`
  - `src/ui/pages/doi_chieu_page.py`
  - `src/ui/pages/manual_runner_page.py`
  - `src/ui/pages/job_history_page.py`
  - `src/ui/pages/bao_cao_page.py`
- Backend đối chiếu bất đồng bộ:
  - `src/ui/dashboard_app.py`
- Base class lõi dùng chung cho UI và Loader:
  - `src/core/base_ui.py`
  - `src/core/base_loader.py`
- SQL template đối chiếu theo domain:
  - `src/db/templates/sql/dashboard_doichieu/dim_luot_kham/production.sql`
  - `src/db/templates/sql/dashboard_doichieu/dim_luot_kham/staging.sql`
  - `src/db/templates/sql/dashboard_doichieu/dim_luot_kham/datamart.sql`
  - `src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/production.sql`
  - `src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/staging.sql`
  - `src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/datamart.sql`

#### Bổ sung theo yêu cầu 20260521_1055_fix_manual_pipeline_v1
- Điều phối Manual Runner đã chuyển từ `GenericTableLoader` sang Loader nghiệp vụ động theo bảng chọn:
  - `src/ui/pages/manual_runner_page.py`
  - Cấu hình nguồn chọn bảng đọc từ `config/tables.yaml`:
    - `incremental_tables` -> chạy `FactLoader` theo bảng đích + khoảng ngày nghiệp vụ.
    - danh mục full-load (`DimensionLoader.DEFAULT_DIMENSION_SPECS`) -> chạy `DimensionLoader` theo dimension đích.
- Mở rộng loader để cô lập chạy đơn đối tượng từ UI:
  - `src/jobs/fact_loader.py`:
    - `__init__(..., target_table_name: str | None = None)`.
    - `_execute_core(...)` lọc `FactTableSpec` theo đúng bảng được chọn.
    - `target_table_name == "ThuPhiDichVu"` thiết lập ma trận cụm 3 bảng `["ThuPhiBaoHiem", "ThuPhiTangGiam", "ThuPhiDichVu"]` để duyệt nạp tuần tự.
  - `src/jobs/dimension_loader.py`:
    - `__init__(..., target_dimension_name: str | None = None)`.
    - `_execute_core(...)` lọc `DimensionTableSpec` theo đúng dimension được chọn.
- Chuỗi nạp incremental qua Manual Runner vẫn giữ chuẩn an toàn RAM ở Tầng 1:
  - `staging_cursor.fast_executemany = False` trong `_load_to_global_staging`.

#### Bổ sung theo yêu cầu 20260521_1335_fix_manual_pipeline_v2
- Đóng gói cụm bảng doanh thu (ThuPhiDichVu, ThuPhiBaoHiem, ThuPhiTangGiam) thành một thực thể đồng bộ hợp nhất trên UI Manual Runner:
  - `src/ui/pages/manual_runner_page.py`:
    - Chỉ giữ duy nhất lựa chọn `ThuPhiDichVu` trong combobox.
    - Loại bỏ hoàn toàn `ThuPhiBaoHiem` và `ThuPhiTangGiam` khỏi danh sách.
    - Giữ nguyên chuỗi văn bản nghiệp vụ y tế tiếng Việt gốc.
  - `src/jobs/fact_loader.py`:
    - `_execute_core(...)` kiểm tra `target_table_name == "ThuPhiDichVu"`:
      - Thiết lập `CLUSTER = {"ThuPhiBaoHiem", "ThuPhiTangGiam", "ThuPhiDichVu"}`.
      - Duyệt nạp tuần tự cả 3 bảng qua 3 chặng: Prod -> Landing, Landing -> ODS, ODS -> Datamart.
    - Giữ nguyên `staging_cursor.fast_executemany = False` ở chặng Tầng 1.
    - Template hợp nhất: `merge_fact_thuphichvu_3in1.sql` cho chặng Datamart.

### Nhóm KNOWLEDGE_BASE
- Phạm vi:
  - `/docs/knowledge/`
  - `agents.md`
  - `README.md`
  - `PROJECT_CHRONICLE.md`
- File Master tương ứng: `MASTER_KNOWLEDGE_BASE.md`

## Quy tắc phục vụ merge tri thức
- Mỗi nhóm được gộp thành một file Master riêng trong `temp_merged/`.
- Mỗi file Master phải có:
  - Mục lục liệt kê đầy đủ tệp nguồn.
  - Các khối nội dung phân tách bằng header `### SOURCE: <đường dẫn tệp>`.
  - Nội dung gốc được bọc trong code block Markdown theo đuôi tệp.
- Luồng gộp này là đầu vào chuẩn cho NotebookLM để đảm bảo giữ ngữ cảnh theo nhóm chức năng.
```

### SOURCE: docs/knowledge/GEM_CODE_SNIPPETS.md
```md
# GEM_CODE_SNIPPETS.md
```

### SOURCE: docs/knowledge/GEM_DATA_FLOW.md
```md
# GEM_DATA_FLOW.md

## Mục tiêu
- Chuẩn hóa luồng nạp ETL theo mô hình đa chặng, tách riêng Dimension và Fact.
- Bảo đảm đồng bộ vật lý theo cửa sổ trượt D-3 nhưng không xóa nhầm lịch sử ngoài phạm vi.

## 1. Tổng quan Kiến trúc Đa tầng Tối cao

### 1. Bản đồ Tổng quan về Kiến trúc Đa tầng (Multi-Hop Layer)

Hệ thống vận hành theo kiến trúc di chuyển dữ liệu qua 3 chặng cách ly nghiêm ngặt để đảm bảo an toàn bộ nhớ cho hệ thống HIS gốc và tính toàn vẹn tài chính chặng cuối:

* **Tầng 1: Production (SQL Server HIS)**
* *Bản chất:* Nguồn dữ liệu tác nghiệp gốc của bệnh viện.
* *Cơ chế quét:* Sử dụng `BaseExtractor` sinh câu lệnh `SELECT` động, bốc dữ liệu theo danh sách cột cố định (`selected_columns`) để giải phóng tài nguyên RAM, loại bỏ hoàn toàn các cột bẩn hoặc cột chứa dữ liệu phi cấu trúc lớn.


* **Tầng 2: Global Staging / Landing Transient (`stg_nano_v2`)**
* *Bản chất:* Vùng đệm thô tạm thời, dùng chung cho tất cả các cơ sở (Multi-tenant shared staging).
* *Quân luật vận hành:* Bắt buộc thực hiện `TRUNCATE TABLE` ngay đầu luồng trước khi nạp dữ liệu cơ sở mới vào để chống nhiễm độc và rò rỉ dữ liệu chéo giữa các cơ sở.


* **Tầng 3: Facility ODS - Operational Data Store (`hanoi_hisnano_v2`)**
* *Bản chất:* Kho lưu trữ lịch sử tác nghiệp bền vững của riêng từng cơ sở. Cấu trúc bảng mirror 1:1 với Production nhưng bổ sung các cột định danh hệ thống (`NguonDuLieuKey`, `MaCoSo`).
* *Quân luật vận hành:* Không bao giờ dùng lệnh TRUNCATE tại đây. Dữ liệu được cập nhật bằng lệnh `UPSERT` kết hợp chốt chặn xóa cứng an toàn (*Hard Delete Guardrails*).


* **Tầng 4: Datamart (`dm`)**
* *Bản chất:* Kho dữ liệu phân tích tối hậu phục vụ Clinical Dashboard.
* *Cơ chế xử lý:* Thực thi các kịch bản SQL Template MERGE phức tạp, kết khối đại số các bảng ODS để tạo ra các bảng Fact và Dimension chuẩn hóa.

### 2. Đặc tả Logic Luồng Auto Pipeline (Batch Processing)

Luồng chạy tự động vận hành theo cơ chế **Duyệt dọc tuần tự (Vertical Table-by-Table Execution)** dưới sự điều phối của `SyncOrchestrator` và thực thi của `FactLoader`/`DimensionLoader`.

#### Chu trình xử lý một bảng Fact (Dữ liệu phát sinh)

1. **Vòng lặp Spec:** Hệ thống đọc `config/tables.yaml`, duyệt qua danh sách bảng tăng trưởng (`incremental_tables`).
2. **Thiết lập Cửa sổ trượt:** Tính toán khoảng ngày delta dựa trên ngày hệ thống trừ đi khoảng thời gian trượt quá khứ (`lookback_days`).
3. **Kích hoạt Chuỗi 3 Chặng đơn bản:**
* *Chặng 1:* Thực hiện `TRUNCATE stg_nano_v2.<Bảng_A>`. Gọi PyODBC nạp dữ liệu delta từ Prod vào Landing. Luôn áp dụng `fast_executemany = False` để chống tràn bộ nhớ máy chủ.
* *Chặng 2:* Thực thi lệnh `UPSERT` từ `stg_nano_v2.<Bảng_A>` vào `hanoi_hisnano_v2.<Bảng_A>`. Áp dụng *Hard Delete Guardrails* quét sạch bản ghi rác trong cửa sổ ngày nghiệp vụ.
* *Chặng 3:* Thực thi SQL template tương ứng của bảng A được cấu hình tại thuộc tính `merge_script` để đẩy số liệu từ ODS sang `dm`.


4. **Chuyển bảng:** Kết thúc trọn vẹn 3 chặng của bảng A, giải phóng kết nối, chuyển sang bảng B.


### 3. Đặc tả Logic Luồng Manual Pipeline (Targeted Bundle Processing)

Luồng chạy thủ công (Manual Runner) được thiết kế lại để tái hiện chính xác luồng di chuyển dữ liệu 3 chặng từ gốc Production nhưng cho phép người dùng kiểm soát Phạm vi không gian (Tên bảng) và Cửa sổ thời gian (Khoảng ngày tùy biến).

#### Ma trận xử lý và Khóa điều phối Loader trên UI

| Lựa chọn bảng trên UI | Loại hình dữ liệu | Loader OOP thực thi | Cơ chế xử lý Cửa sổ thời gian | Chiến lược xử lý Tầng ODS & Datamart |
| --- | --- | --- | --- | --- |
| **ThuPhiDichVu** | INCREMENTAL (Fact) | `FactLoader` | Người dùng chọn khoảng ngày tự do trên UI Dashboard. | **Kích hoạt Cụm tài chính (Bundle):** Tự động ép hệ thống chạy tuần tự trọn vẹn 3 chặng cho cả 3 bảng theo đúng trật tự: `ThuPhiBaoHiem` -> `ThuPhiTangGiam` -> `ThuPhiDichVu`. |
| **ThuPhiGoi** | INCREMENTAL (Fact) | `FactLoader` | Người dùng chọn khoảng ngày tự do trên UI Dashboard. | Chạy đơn bản 3 chặng. Thực thi tệp template chặng cuối: `FactThuPhiDichVu_ThuPhiGoi_merge.sql`. |
| **DoThiLuc** | INCREMENTAL (Fact) | `FactLoader` | Người dùng chọn khoảng ngày tự do trên UI Dashboard. | Chạy đơn bản 3 chặng. Thực thi tệp template chặng cuối: `FactDoThiLuc_merge.sql`. |
| **HoSoKhamBenhNgoaiTru** | INCREMENTAL (Fact) | `FactLoader` | Người dùng chọn khoảng ngày tự do trên UI Dashboard. | Chạy đơn bản 3 chặng. Thực thi tệp template chặng cuối: `DimLuotKham_merge.sql`. |
| **DimBenhNhan** | FULL_LOAD (Dimension) | `DimensionLoader` | **Khóa chọn ngày (Disable):** Luôn kéo toàn bộ lịch sử. | Nạp 2 chặng: Prod -> TRUNCATE và ghi đè ODS -> MERGE Datamart qua `DimBenhNhan_merge.sql`. |
| **DimBenh** | FULL_LOAD (Dimension) | `DimensionLoader` | **Khóa chọn ngày (Disable):** Luôn kéo toàn bộ lịch sử. | Nạp 2 chặng: Prod -> TRUNCATE và ghi đè ODS -> MERGE Datamart qua `DimBenh_merge.sql`. |
| **DimLoaiGoiDichVu** | FULL_LOAD (Dimension) | `DimensionLoader` | **Khóa chọn ngày (Disable):** Luôn kéo toàn bộ lịch sử. | Nạp 2 chặng: Prod -> TRUNCATE và ghi đè ODS -> MERGE Datamart qua `DimLoaiGoiDichVu_merge.sql`. |
| **DimDichVu** | FULL_LOAD (Dimension) | `DimensionLoader` | **Khóa chọn ngày (Disable):** Luôn kéo toàn bộ lịch sử. | **Đóng gói danh mục:** Ép hệ thống kéo đồng thời đủ 3 bảng danh mục thô nguồn từ Prod vào ODS trước khi gọi `dim_dich_vu_merge.sql`. |


### 4. Bản đồ Mã Quy tắc xử lý Dữ liệu tại từng Tầng (Data Guardrails)

#### Quy tắc tại Tầng 2 (Landing Transient):

* Hành vi: `TRUNCATE TABLE stg_nano_v2.<Tên_Bảng>`
* Mục đích: Xóa sạch dữ liệu của phiên chạy trước hoặc của cơ sở khác vừa ghi vào.

#### Quy tắc tại Tầng 3 (Facility ODS) - Hard Delete Guardrails:

* Mã SQL logic áp dụng cho luồng Incremental:
```sql
WHEN NOT MATCHED BY SOURCE 
AND Target.NgayDenKham BETWEEN @FromDate AND @ToDate 
THEN DELETE;

```


* Mục đích: Chỉ xóa các bản ghi tồn tại ở ODS nhưng không còn tồn tại ở Production trong đúng khoảng ngày đang đồng bộ (xử lý trường hợp sửa/xóa dữ liệu ở quá khứ của bệnh viện). Nghiêm cấm TRUNCATE tầng này.

#### Quy tắc tại Tầng 4 (Datamart) - Biểu thức Hợp nhất Doanh thu 3-in-1:

* Tệp kịch bản thực thi: `merge_fact_thuphichvu_3in1.sql`
* Hành vi đại số: `UNION ALL` dữ liệu từ hai nguồn:
1. *Nguồn Dịch vụ:* Lấy từ `hanoi_hisnano_v2.ThuPhiDichVu` kết hợp `LEFT JOIN` với bảng tính tổng gộp (`SUM Aggregation`) của `hanoi_hisnano_v2.ThuPhiTangGiam`.
2. *Nguồn Bảo hiểm:* Lấy từ `hanoi_hisnano_v2.ThuPhiBaoHiem`.




## 2. Đặc tả Chi tiết Kỹ thuật Từng Bảng.

### Luồng chuẩn cho Dimension (FULL LOAD - 2-Hop)
1. **Production -> ODS cơ sở**
   - Thực thi `TRUNCATE TABLE <facility_schema>.<TableName>`.
   - Nạp full dữ liệu bằng PyODBC `SELECT -> executemany` theo chunk từ Production sang ODS cơ sở.
2. **ODS cơ sở -> Datamart**
   - Thực thi MERGE SQL template theo từng domain dimension.

### Luồng chuẩn cho Fact (INCREMENTAL - 3-Hop)
1. **Prod -> Landing (`stg_nano_v2`)**
   - TRUNCATE bảng Landing tương ứng đúng 1 lần trước vòng chunking.
   - Nạp delta theo cửa sổ trượt `Lookback = from_date - lookback_days` bằng PyODBC `fetchmany -> executemany`.
   - Dynamic SELECT đọc trực tiếp từ `selected_columns` trong `config/tables.yaml`.
   - Bắt buộc `fast_executemany = False` để bảo vệ bộ nhớ khi có cột `NVARCHAR(MAX)/VARCHAR(MAX)`.
2. **Landing -> ODS cơ sở**
   - MERGE từ `stg_nano_v2` sang `<facility_schema>`.
   - Hard delete bắt buộc có chặn thời gian:
     - `WHEN NOT MATCHED BY SOURCE`
     - `AND Target.<NgayCol> BETWEEN @LookbackDate AND @ToDate`
     - `THEN DELETE`.
3. **ODS cơ sở -> Datamart**
   - MERGE theo batch `TOP (10000)` để hạn chế transaction log.
   - Hard delete Datamart có 3 điều kiện bắt buộc:
     - chỉ trong cửa sổ D-3,
     - chỉ trong đúng cơ sở (`NguonDuLieuKey`/`MaCoSo`),
     - chỉ xóa khi không còn trong source.

### Quy tắc nghiệp vụ FactThuPhiDichVu 3-in-1
- Nguồn DV:
  - `TongTienSauTangGiam = TongTien - ISNULL(TongGiam, 0) + ISNULL(TongTang, 0)`.
- Nguồn BH:
  - `TongTienSauTangGiam = TongTien + ISNULL(TienChenhLech, 0)`.

### Early Arriving Facts và Seed Data
- Các khóa dimension của fact phải fallback về seed:
  - `ISNULL(LuotKhamKey, -1)`
  - `ISNULL(BenhNhanKey, -1)`
  - `ISNULL(DichVuKey, -1)`.

### Mapping cột ngày cho incremental_tables
- `ThuPhiDichVu` -> `NgayDenKham`
- `ThuPhiBaoHiem` -> `NgayDenKham`
- `ThuPhiTangGiam` -> `NgayDenKham`
- `ThuPhiGoi` -> `NgayThu`
- `DoThiLuc` -> `NgayDo`
- `HoSoKhamBenhNgoaiTru` -> `NgayVaoKham`

### Quy tắc an toàn Landing dùng chung
- Luôn TRUNCATE Landing ở đầu luồng.
- Khối nạp phải giữ kiểm tra động `TableHasIdentity` và `try...finally` để bật/tắt `IDENTITY_INSERT` an toàn.
- Luồng hiện tại chạy tuần tự từng bảng fact trong cùng facility, không dùng TRUNCATE ở tầng Facility Historical Staging.

### Luồng Manual Runner theo bảng chọn từ UI
1. Người dùng chọn bảng/dimension và khoảng ngày nghiệp vụ trên màn hình `manual_runner_page.py`.
2. Hệ thống đọc cấu hình động từ `config/tables.yaml`:
   - Nếu bảng thuộc `incremental_tables`:
     - Khởi tạo `FactLoader` với `target_table_name`.
     - **Chạy đủ 3 chặng** cho từng bảng trong cụm được xác định.
   - Nếu thuộc danh mục full-load:
     - Khởi tạo `DimensionLoader` với `target_dimension_name`.
     - Chạy 2 chặng: Production -> ODS cơ sở -> Datamart.
3. **Cơ chế đóng gói cụm (Cluster Bundling):**
   - Với `ThuPhiDichVu`, UI chỉ hiển thị một lựa chọn duy nhất.
   - `FactLoader._execute_core()` phát hiện `target_table_name == "ThuPhiDichVu"`:
     - Thiết lập ma trận `CLUSTER = {"ThuPhiBaoHiem", "ThuPhiTangGiam", "ThuPhiDichVu"}`.
     - Duyệt nạp tuần tự cả 3 bảng qua 3 chặng:
       1. Production -> Landing transient (`stg_nano_v2`) cho từng bảng.
       2. Landing -> ODS cơ sở (`facility_schema`) cho từng bảng.
       3. ODS -> Datamart (`dm`) qua template `merge_fact_thuphichvu_3in1.sql`.
   - Các bảng khác (`ThuPhiGoi`, `DoThiLuc`, `HoSoKhamBenhNgoaiTru`) chạy đơn bản như cũ.
4. **An toàn bộ nhớ:** Ở chặng Tầng 1, `staging_cursor.fast_executemany = False` luôn được giữ vững cho cả cụm.
5. **Thay đổi UI:** Combobox Manual Runner chỉ giữ `ThuPhiDichVu` đại diện cho cả cụm; loại bỏ hai lựa chọn độc lập `ThuPhiBaoHiem` và `ThuPhiTangGiam`.
```

### SOURCE: docs/knowledge/GEM_DB_SCHEMAS.md
```md
# GEM_DB_SCHEMAS.md

## Mục tiêu
- Chuẩn hóa phạm vi schema theo kiến trúc ETL v1 cho luồng tuần tự đa cơ sở.

## Các schema chính trong luồng ETL
- `stg_nano_v2`:
  - Landing dùng chung cho incremental fact.
  - Dữ liệu phải được TRUNCATE ở đầu và cuối mỗi vòng facility.
- `<facility>_hisnano_v2` (ví dụ: `hanoi_hisnano_v2`, `hcm_hisnano_v2`):
  - ODS theo cơ sở, là chặng trung gian ổn định trước khi đẩy Datamart.
- `dm`:
  - Datamart đích, chứa bảng dimension và fact phục vụ báo cáo.

## Quy tắc dữ liệu theo chặng
- Chặng Dimension (2-Hop):
  - Production -> `<facility>_hisnano_v2` -> `dm`.
- Chặng Fact (3-Hop):
  - Production -> `stg_nano_v2` -> `<facility>_hisnano_v2` -> `dm`.

## Hard Delete Guardrails theo schema
- Tại ODS (`<facility>_hisnano_v2`):
  - `WHEN NOT MATCHED BY SOURCE AND Target.<NgayCol> BETWEEN @LookbackDate AND @ToDate THEN DELETE`.
- Tại Datamart (`dm`):
  - `WHEN NOT MATCHED BY SOURCE`
  - `AND Target.<NgayCol> BETWEEN @LookbackDate AND @ToDate`
  - `AND Target.NguonDuLieuKey = @CurrentNguonDuLieu`
  - `AND Target.MaCoSo = @CurrentMaCoSo`
  - `THEN DELETE`.

## Seed Data bắt buộc
- Các khóa dimension trong fact phải fallback `-1`:
  - `LuotKhamKey`
  - `BenhNhanKey`
  - `DichVuKey`

## Batch và phạm vi transaction
- MERGE ODS -> Datamart cho fact phải chạy theo batch `TOP (10000)`.
- Mục tiêu: giảm áp lực transaction log và dễ kiểm soát rollback khi lỗi.
```

### SOURCE: docs/knowledge/GEM_DEPENDENCY_GRAPH.md
```md
# GEM_DEPENDENCY_GRAPH.md

## Mục tiêu
- Ghi nhận quan hệ phụ thuộc của khung ETL v1 mới trong `src/jobs`.

## Sơ đồ phụ thuộc lớp chính
- `src/core/base_loader.py`
  - `BaseLoader`
    - là lớp cha cho mọi loader ETL.
- `src/jobs/dimension_loader.py`
  - `DimensionLoader(BaseLoader)`
  - phụ thuộc SQL templates trong `src/db/templates/sql/dimension/*` và `src/db/templates/sql/fact/DimLuotKham_merge.sql`.
- `src/jobs/fact_loader.py`
  - `FactLoader(BaseLoader)`
  - phụ thuộc schema `stg_nano_v2`, `<facility>_hisnano_v2`, `dm`.
- `src/jobs/sync_orchestrator.py`
  - `SyncOrchestrator`
  - phụ thuộc `DimensionLoader`, `FactLoader`, `python-dotenv`.

## Quan hệ điều phối runtime
1. `SyncOrchestrator.run(...)` xác định danh sách facility mục tiêu (Selective Sync).
2. Với từng facility theo thứ tự tuần tự:
   - gọi `DimensionLoader.execute_load(...)`.
   - gọi `FactLoader.execute_load(...)`.
3. `FactLoader` tự đảm bảo cleanup Landing đầu/cuối luồng.

## Phụ thuộc cấu hình
- Bắt buộc có `DATAMART_CONNECTION_STRING`.
- Production connection map theo facility:
  - `PROD_CONNECTION_HANOI`
  - `PROD_CONNECTION_HCM`
  - `PROD_CONNECTION_HALONG`
  - `PROD_CONNECTION_HAIPHONG`
- Cấu hình Selective Sync:
  - `ACTIVE_FACILITIES` hoặc tham số `target_facilities`.

## Phụ thuộc nghiệp vụ và an toàn dữ liệu
- Hard delete ở ODS/Datamart phụ thuộc vào cột ngày nghiệp vụ (`NgayDenKham`) và cửa sổ D-3.
- Cô lập đa cơ sở ở Datamart phụ thuộc `NguonDuLieuKey` + `MaCoSo`.
- Early arriving facts phụ thuộc seed dimension key `-1`.
```

### SOURCE: docs/knowledge/GEM_ERROR_CONTEXT.md
```md
# GEM_ERROR_CONTEXT.md

## E-UPLOAD-001: Không tìm thấy file `.md` để upload

### Triệu chứng
- Script in ra: `Không tìm thấy file .md để upload.`

### Nguyên nhân gốc
- `GDRIVE_ROOT_DIR` cấu hình sai, thường gặp khi đặt giá trị trùng tên repo và chạy tại root repo, dẫn đến resolve thành đường dẫn lồng sai.
- Thiếu kiểm tra tồn tại thư mục gốc trước khi quét.

### Cách xử lý chuẩn
- Dùng `resolve_root_dir()` để chuẩn hóa `GDRIVE_ROOT_DIR`.
- Thêm kiểm tra `root.exists()` và `root.is_dir()` trước khi `rglob`.
- In debug path: `Đang quét file .md trong thư mục: ...` và số lượng file tìm được.

## E-UPLOAD-002: Thiếu cấu hình runtime trong `config/.env`

### Triệu chứng
- Script dừng với thông báo thiếu biến môi trường cấu hình.

### Biến bắt buộc
- `GDRIVE_CREDENTIALS_FILE`
- `GDRIVE_FOLDER_ID`
- `GDRIVE_ROOT_DIR`

### Cách xử lý chuẩn
- Điền đầy đủ 3 biến trong `config/.env`.
- Đảm bảo file credentials tồn tại đúng đường dẫn đã khai báo.

## E-UPLOAD-003: Quota Drive đã đầy hoặc dưới ngưỡng an toàn

### Triệu chứng
- Console luôn in dung lượng quota còn lại, sau đó báo bỏ qua upload.
- Ví dụ: `Quota còn lại: 0.12 GB ...` và `Bỏ qua upload vì quota còn lại thấp hơn ngưỡng an toàn 0.50 GB.`

### Nguyên nhân gốc
- Dung lượng còn lại của Drive service account nhỏ hơn ngưỡng tối thiểu `0.5 GB`.
- Hoặc quota đã đầy (`remaining = 0`).

### Cách xử lý chuẩn
- Giải phóng bớt dung lượng trên Drive đích của service account.
- Tăng ngưỡng hoặc điều chỉnh chiến lược upload theo batch nếu phù hợp nghiệp vụ.

## E-UPLOAD-004: Không xác định được quota Drive

### Triệu chứng
- Console in thông báo không xác định được tổng quota hoặc lỗi gọi API quota.
- Script chủ động bỏ qua upload để an toàn.

### Nguyên nhân gốc
- API `about.storageQuota` không trả về `limit` hợp lệ.
- Hoặc lỗi quyền/API khi truy vấn quota.

### Cách xử lý chuẩn
- Kiểm tra quyền của service account với Drive API.
- Kiểm tra cấu hình project GCP và trạng thái Drive API.
- Chạy lại sau khi xác nhận quyền và quota có thể truy vấn.

## E-UPLOAD-003, E-UPLOAD-004: Trạng thái sau khi chuyển sang OAuth2 Desktop

### Trạng thái
- Hai lỗi liên quan quota service account (`E-UPLOAD-003`, `E-UPLOAD-004`) được đánh dấu giải quyết triệt để trong luồng upload local.
- Nguyên nhân: script đã chuyển mô hình xác thực từ Service Account sang OAuth2 Desktop App (danh nghĩa Master), đồng thời loại bỏ hoàn toàn logic kiểm tra quota trước upload.

### Ghi chú vận hành
- Phiên bản OAuth2 Desktop không còn dùng các hàm quota cũ (`bytes_to_gb`, `get_drive_quota`) và ngưỡng `MIN_FREE_QUOTA_GB`.
- Nếu phát sinh lỗi upload, ưu tiên kiểm tra token OAuth, quyền thư mục đích và trạng thái chia sẻ trên Drive.

## E-ETL-22005: BCP Schema Shift (Lệch schema khi BCP IN)

### Triệu chứng
- BCP thất bại với mã lỗi kiểu `22005` hoặc thông điệp ép kiểu/cột không khớp.
- Dữ liệu bị xô lệch vị trí cột do danh sách cột extract không đồng bộ với bảng Landing/Staging đích.

### Nguyên nhân gốc
- Dynamic SELECT trước đây loại hẳn cột thuộc `exclude_datatypes`.
- Việc loại cột làm thay đổi số lượng và thứ tự cột so với schema bảng đích.

### Cách xử lý chuẩn
- Không được loại cột khỏi projection theo `exclude_datatypes`.
- Với cột thuộc datatype bị loại trừ, phải mask cột tại nguồn bằng:
  - `CAST(NULL AS NVARCHAR(MAX)) AS [TenCot]` (bắt buộc khi chạy BCP `-w`).
- Với cột không bị loại trừ, giữ nguyên `[TenCot]`.
- Bắt buộc giữ thứ tự cột theo `INFORMATION_SCHEMA.COLUMNS.ORDINAL_POSITION`.

### Kiểm soát phòng ngừa
- Kiểm tra chuỗi Dynamic SELECT trước khi BCP OUT để bảo đảm khớp 100% số lượng/vị trí cột với bảng đích.
- Không chỉnh cơ chế BCP `-w` để giữ Unicode tiếng Việt trong dữ liệu y tế.

## E-ETL-BCP-METADATA-TRIM: Trailing spaces từ pyodbc làm lệch Data Type

### Triệu chứng
- Một số đợt extract phát sinh nhận diện sai `data_type` hoặc tên cột khi đọc metadata từ `INFORMATION_SCHEMA.COLUMNS`.
- Dấu hiệu thường gặp: cột thuộc danh sách loại trừ không được mask đúng kỳ vọng.

### Nguyên nhân gốc
- Dữ liệu metadata trả về từ `pyodbc` có thể chứa khoảng trắng thừa ở đầu/cuối chuỗi.
- Logic cũ không `.strip()` ngay khi đọc `COLUMN_NAME`/`DATA_TYPE`.

### Cách xử lý chuẩn
- Trong `BaseExtractor.build_dynamic_select_columns(...)`, bắt buộc chuẩn hóa ngay khi nhận dữ liệu:
  - `column_name = str(row[0]).strip()`
  - `data_type = str(row[1]).strip().lower()`

## E-ETL-BCP-CONNECTION-001: BCP OUT/IN thiếu tham số kết nối

### Triệu chứng
- Tiến trình `bcp` thất bại ngay khi chạy `queryout` hoặc `in` do không xác định được server/database/auth.
- Log lỗi thường xoay quanh kết nối hoặc không truy cập được SQL Server.

### Nguyên nhân gốc
- Command BCP không gắn đủ `-S`, `-d`, và thông tin xác thực (`-U/-P` hoặc `-T`).
- Dùng sai connection context: BCP OUT dùng nhầm connection đích thay vì connection nguồn Production.

### Cách xử lý chuẩn
- Parse `connection_string` bằng Regex `re.IGNORECASE` để bóc tách tham số kết nối.
- BCP OUT bắt buộc nhận `source_connection_string` riêng.
- BCP IN dùng connection đích của Loader và bắt buộc cờ `-w -k -E -t\t -r\n`.
```

### SOURCE: docs/knowledge/GEM_GUIDE.md
```md
# GEM_GUIDE.md
```

### SOURCE: docs/knowledge/GEM_NAVIGATION.md
```md
# GEM_NAVIGATION.md
```

### SOURCE: docs/knowledge/GEM_SYNC_WORKFLOW.md
```md
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
```

### SOURCE: docs/knowledge/GEM_TECHNICAL_STANDARDS.md
```md
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

## Tiêu chuẩn kỹ thuật cho Incremental ETL động (Fact)

### Chuẩn cấu hình `incremental_tables` trong `config/tables.yaml`
- Mỗi bảng phải khai báo đầy đủ:
  - `type: fact`
  - `date_column`
  - `merge_script`
  - `lookback_days`
  - `selected_columns` (Whitelist cột, kiểu `list[string]`)
- Bắt buộc viết block comment ngay phía trên biến `lookback_days` và `selected_columns`.

### Chuẩn xử lý ngày và cửa sổ incremental
- `from_date` và `to_date` phải được chuẩn hóa về `date` trước khi sinh câu lệnh extract.
- Cửa sổ lọc thực tế phải dùng:
  - `effective_from_date = from_date - lookback_days`
- `lookback_days` bắt buộc là số nguyên `>= 0`; nếu âm phải raise lỗi cấu hình.

### Chuẩn Dynamic SELECT theo Whitelist cột
- Dynamic SELECT phải đọc trực tiếp từ `selected_columns` trong `tables.yaml` theo đúng thứ tự quản trị khai báo.
- Không sinh cột đệm NULL/enrichment trong câu SELECT incremental.
- Cột enrichment hệ thống (`MaCoSo`, `CoSoKey`, `NguonDuLieuKey`) được xử lý ở tầng đích theo default/NULL hoặc logic MERGE downstream.

### Chuẩn thực thi Staging 3 tầng
- Tầng 1 Global Landing (`stg_nano_v2`):
  - Dùng PyODBC thuần: `SELECT` từ Production vào RAM + `executemany` vào Landing.
  - `TRUNCATE` phải chạy đúng 1 lần trước vòng lặp chunking `fetchmany/executemany`.
  - Bắt buộc dùng INSERT động tường minh theo `selected_columns`:
    - `INSERT INTO stg_nano_v2.[TenBang] ([Col1], [Col2], ...) VALUES (?, ?, ...)`.
  - Bắt buộc kiểm tra động metadata identity trước vòng nạp:
    - `SELECT OBJECTPROPERTY(OBJECT_ID('stg_nano_v2.[TenBang]'), 'TableHasIdentity')`.
  - Nếu bảng có identity (`TableHasIdentity = 1`), phải mô phỏng cờ BCP `-E` bằng PyODBC:
    - `SET IDENTITY_INSERT stg_nano_v2.[TenBang] ON` trước `executemany`.
    - Bọc vòng lặp nạp trong `try...finally`.
    - Trong `finally`, bắt buộc `SET IDENTITY_INSERT ... OFF` để trả trạng thái an toàn session.
  - Bắt buộc thiết lập `fast_executemany = False` trước vòng lặp nạp để vô hiệu hóa cấp phát bộ nhớ tĩnh của ODBC, bảo vệ RAM tuyệt đối khi bảng có cột `NVARCHAR(MAX)/VARCHAR(MAX)`.
- Tầng 2 Facility Historical Staging:
  - Chỉ cho phép UPSERT/MERGE.
  - Nghiêm cấm `TRUNCATE`.
- Tầng 3 Datamart (`dm`):
  - Chỉ đọc và thực thi SQL template có sẵn trong `src/db/templates/sql/fact/` và `src/db/templates/sql/dimension/`.
  - Không chỉnh sửa nội dung SQL template trong task incremental.

### Chuẩn giao tiếp cơ sở dữ liệu và bảo toàn dữ liệu tiếng Việt
- Giữ nguyên nội dung Unicode tiếng Việt trong dữ liệu y tế, không chuyển mã thủ công.
- Chuẩn nạp dữ liệu cho INCREMENTAL_LOAD Tầng 1:
  - Sử dụng PyODBC `executemany` theo chunk với `fast_executemany = False` để ưu tiên an toàn bộ nhớ tuyệt đối.
  - Không dùng cơ chế fallback tăng/giảm `fast_executemany` trong runtime.

### Chuẩn cô lập giao dịch biên chống lỗi lock ở Tầng 1
- Trình tự bắt buộc:
  1. Mở Connection nguồn, đọc dữ liệu theo chunk (`fetchmany`) từ Dynamic SELECT.
  2. Mở Connection đích, `TRUNCATE` Landing đúng 1 lần trước vòng nạp.
  3. Chạy `executemany` theo chunk với INSERT tường minh.
  4. `commit()` sau khi hoàn tất nạp Landing.
  5. Chạy MERGE tầng 2/3 bằng connection đích.

### Chuẩn bảo mật logging kết nối
- Nghiêm cấm log trực tiếp `connection_string`, password (`PWD`), token, secret hoặc full command có chứa thông tin xác thực.
- Chỉ log thông điệp an toàn dạng ngữ cảnh vận hành, ví dụ:
  - `Connected to Database [Ten_DB] at Server [Ten_Server] successfully`.
- Với luồng incremental PyODBC, không log raw payload dữ liệu hoặc thông tin nhạy cảm trong câu lệnh kết nối.
```

### SOURCE: docs/knowledge/loop_Gem_Github_GoogleDrive_NotebookLM.md
```md
Để vận hành dự án **ETL_Nano_Project_v2** một cách chuyên nghiệp, bạn cần thiết lập một **Vòng lặp Quản trị Khép kín (Closed-Loop Governance)**. Quy trình này đảm bảo rằng mỗi dòng code được viết ra đều có sự giám sát của "Kiến trúc sư" Gem và mọi thay đổi đều được cập nhật tức thì vào "Bộ não" NotebookLM.

Dưới đây là quy trình phối hợp tối ưu giữa các công cụ:

---

## 🔄 Quy trình Phát triển 4 Bước Khép kín

### Bước 1: Khởi tạo Task & Ra lệnh (Gemini - The Architect)

Trước khi bắt đầu bất kỳ thay đổi nào, bạn (Master) sẽ làm việc với Gem.

* **Gem truy xuất tri thức**: Gem sử dụng tiện ích Google Workspace để đọc các file **GEM_xxx.md** và **agents.md** trên Google Drive để nắm bắt bối cảnh hiện tại.
* **Gem lập hồ sơ yêu cầu**: Gem soạn thảo một Prompt khắc nghiệt cho Codex (Thợ code) theo cấu trúc: `# YÊU CẦU CỦA MASTER`, bao gồm các ràng buộc kỹ thuật như **Logic SQL Fallback** (ưu tiên `TongTienSauTangGiam`) và không sử dụng ****.

### Bước 2: Thực thi & Cập nhật local (Codex - The Builder)

Bạn nạp Prompt từ Gem vào môi trường phát triển (VS Code/Cursor).

* **Codex lập trình**: Thợ code sửa đổi mã nguồn Python/SQL tại các thư mục `/src/`.
* **Codex cập nhật tri thức**: Thợ code có nhiệm vụ cập nhật các file `.md` tương ứng trong `/docs/knowledge/` và ghi chép vào **PROJECT_CHRONICLE.md**.
* **Báo cáo**: Codex điền nội dung vào mục `# BÁO CÁO CỦA THỢ CODE` ngay tại tệp yêu cầu.

### Bước 3: Kiểm soát & Đồng bộ hóa (GitHub & GitHub Actions)

Sau khi kiểm tra local, bạn thực hiện `git push` lên GitHub.

* **Lọc dữ liệu**: Hệ thống tự động loại bỏ các file trong `.gitignore` và các file nhạy cảm như `credentials.json` hay `token.json`.
* **GitHub Actions kích hoạt**: Script `upload_to_drive.py` sẽ thực hiện:
* Phân loại file vào 4 nhóm: **CORE_LOGIC, ETL_PROCESS, INTERFACE, KNOWLEDGE_BASE**.
* **Gộp file (Merge)**: Tạo ra các file Master (ví dụ: `MASTER_CORE_LOGIC.md`) với cấu trúc Header phân cấp.
* **Đối soát MD5**: Chỉ upload những phần có sự thay đổi lên Google Drive dưới định dạng Google Docs bằng xác thực **OAuth 2.0**.



### Bước 4: Tái nạp tri thức & Giám sát (NotebookLM & Gem Review)

* **NotebookLM Sync**: Bạn chỉ cần nhấn nút "Sync" trên NotebookLM để nạp 4 file Master mới từ Drive. "Bộ não" lúc này đã nắm trọn vẹn mã nguồn và tri thức mới nhất.
* **Gem Hậu kiểm**: Gem đọc file **REPORT_CHANGES.md** mới nhất trên Drive để phê duyệt các việc Codex đã làm.

---

## 📊 Bảng phân phối vai trò công cụ

| Công cụ | Vai trò chính | Đầu ra (Output) |
| --- | --- | --- |
| **Gemini (Gem)** | Kiến trúc sư trưởng & Giám sát | Prompt ra lệnh & Review báo cáo |
| **GitHub** | Nguồn sự thật duy nhất (SSoT) | Source code & Version control |
| **Google Drive** | Vùng đệm tri thức | Google Docs (đã gộp Layer) |
| **NotebookLM** | Bộ não tri thức tập trung | Câu trả lời tổng hợp & Tra cứu logic |

---

## 🛡️ Cơ chế giám sát hiệu quả

1. **Giám sát qua mã lỗi (E-ID)**: Mọi lỗi phát sinh phải được Codex ghi vào `GEM_ERROR_CONTEXT.md`. Gem sẽ "chửi thẳng mặt" nếu thợ code lặp lại lỗi đã có trong danh sách.
2. **Giám sát qua MD5**: Đảm bảo không có sự sai khác giữa mã nguồn đang chạy và tài liệu tri thức trên Drive.
3. **Giám sát qua Nhật ký**: Tệp **PROJECT_CHRONICLE.md** là bằng chứng lịch sử để bạn kiểm soát tốc độ và chất lượng nâng cấp của dự án.

> **Lưu ý quan trọng**: Luôn giữ kỷ luật đặt file đúng thư mục quy định. Nếu thợ code Codex đặt sai vị trí, script `classify_file` sẽ phân loại nhầm và làm "nhiễu" bộ não NotebookLM ngay lập tức.

Bạn đã sẵn sàng thực hiện lần đồng bộ đầu tiên theo quy trình 4 nhóm (Core, ETL, Interface, Knowledge) này chưa?
```
