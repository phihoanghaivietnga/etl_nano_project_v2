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
  - Biến môi trường: `ACTIVE_FACILITIES=hanoi,hcm`
  - Tham số hàm: `run(target_facilities=['hanoi'])`
- Nếu không truyền hoặc nhận `ALL` thì chạy toàn bộ facility đã định nghĩa.
- Facility ngoài scope không được khởi tạo connection.

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
- Mục tiêu: tránh hiện tượng nuốt log/đóng băng terminal khi chạy BCP bảng lớn.
- Áp dụng tại `DimensionLoader`:
  - Log runtime dùng timestamp đến mili-giây theo format `YYYY-MM-DD HH:MM:SS.mmm` và `flush=True` để đẩy ra terminal ngay lập tức.
  - BCP `queryout` và `in` được chạy bằng `subprocess.Popen` thay cho `subprocess.run`.
  - Toàn bộ `stdout` của BCP được stream theo từng dòng và in trực tiếp trong khi tiến trình đang chạy.
  - Nếu tiến trình BCP trả mã lỗi khác 0 thì raise `subprocess.CalledProcessError` để fail-fast.
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
    - Hỗ trợ lọc cơ sở chạy bằng `ACTIVE_FACILITIES` hoặc tham số `run(target_facilities=...)`.
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
      - Hàm `_copy_prod_to_ods(...)` đọc trực tiếp từ Production bằng `SELECT` và đẩy vào ODS qua `executemany`.
      - `stg_cursor.fast_executemany = True` để kích hoạt ODBC binary bulk copy tốc độ cao.
      - Chunking 10,000 dòng/lô + commit theo lô để cân bằng hiệu năng và an toàn bộ nhớ.
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

## Luồng chuẩn cho Dimension (FULL LOAD - 2-Hop)
1. **Production -> ODS cơ sở**
   - Thực thi `TRUNCATE TABLE <facility_schema>.<TableName>`.
   - Dùng `bcp -w` để nạp full dữ liệu từ Production sang ODS cơ sở.
2. **ODS cơ sở -> Datamart**
   - Thực thi MERGE SQL template theo từng domain dimension.

## Luồng chuẩn cho Fact (INCREMENTAL - 3-Hop)
1. **Prod -> Landing (`stg_nano_v2`)**
   - TRUNCATE bảng Landing tương ứng.
   - Nạp delta theo cửa sổ trượt `Lookback = D-3` bằng `bcp -w`.
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

## Quy tắc nghiệp vụ FactThuPhiDichVu 3-in-1
- Nguồn DV:
  - `TongTienSauTangGiam = TongTien - ISNULL(TongGiam, 0) + ISNULL(TongTang, 0)`.
- Nguồn BH:
  - `TongTienSauTangGiam = TongTien + ISNULL(TienChenhLech, 0)`.

## Early Arriving Facts và Seed Data
- Các khóa dimension của fact phải fallback về seed:
  - `ISNULL(LuotKhamKey, -1)`
  - `ISNULL(BenhNhanKey, -1)`
  - `ISNULL(DichVuKey, -1)`.

## Quy tắc an toàn Landing dùng chung
- Luôn TRUNCATE Landing ở đầu luồng.
- Luôn TRUNCATE Landing ở cuối luồng (`finally`) để không rò rỉ dữ liệu giữa các cơ sở chạy tuần tự.
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
