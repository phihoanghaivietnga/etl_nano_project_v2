# REPORT_CHANGES.md

## Phạm vi cập nhật theo yêu cầu 20260511_1425_change_group_file_v3
- Cấu hình: `config/.env`
- Script chính: `scripts/upload_to_drive_from_local.py`
- Nhật ký dự án: `PROJECT_CHRONICLE.md`
- File yêu cầu cần ghi báo cáo: `docs/prompts/20260511_1425_change_group_file_v3.md`

## Nội dung đã thực hiện

### 1) Trả lại phạm vi quét toàn dự án
- Cập nhật `config/.env`:
  - `GDRIVE_ROOT_DIR=etl_nano_project_v2`
- Xác minh script chạy từ root project và quét toàn bộ cây thư mục.

### 2) Viết lại hàm phân loại theo path vật lý
- Cập nhật `classify_group_by_path` trong `scripts/upload_to_drive_from_local.py`:
  - `/src/core/`, `/config/`, `.env` -> `CORE_LOGIC`
  - `/src/jobs/`, `/src/db/templates/sql/` -> `ETL_PROCESS`
  - `/src/ui/`, `/scripts/`, `main.py` -> `INTERFACE`
  - `/docs/knowledge/` + file chiến lược root -> `KNOWLEDGE_BASE`
- Loại bỏ logic phụ thuộc root hẹp `docs/knowledge`.

### 3) Chuẩn hóa mục lục Master theo yêu cầu v3
- Cập nhật format mục lục trong file Master thành:
  - `### [PATH] - [DESCRIPTION]`

### 4) Chạy script và đối soát kết quả
- Đã chạy `python scripts/upload_to_drive_from_local.py` với root project.
- Kết quả chính:
  - Tổng file trước lọc: `2262`
  - Tổng file xử lý: `2266`
  - Created: `3`, Updated: `7`, Up-to-date: `33`, Skipped: `2223`, Error: `0`
- Trích xuất mục lục mẫu từ:
  - `temp_merged/MASTER_CORE_LOGIC.md`
  - `temp_merged/MASTER_KNOWLEDGE_BASE.md`

### 5) Cập nhật tài liệu nhật ký và báo cáo yêu cầu
- `PROJECT_CHRONICLE.md`: ghi lại sai lầm thu hẹp phạm vi quét về `docs/knowledge`, tác động, cách khắc phục.
- `docs/prompts/20260511_1425_change_group_file_v3.md`:
  - Bổ sung đầy đủ mục **Mô tả các việc đã làm**.
  - Dán log thực thi và trích mục lục Master theo yêu cầu.

## Ghi chú kỹ thuật
- `CORE_LOGIC`/`ETL_PROCESS` vẫn có thể bằng 0 ở snapshot hiện tại nếu không có file nguồn hợp lệ sau lọc.
- Trong lần chạy này:
  - `src/core`, `src/jobs`, `src/ui` không có source nghiệp vụ đáng kể.
  - `.env` và file nhạy cảm trong `config/` bị loại do quy tắc `.gitignore`/forced-exclude.

## Phạm vi cập nhật theo yêu cầu 20260514_1420_tao_man_hinh_dashboard_doi_chieu_v1
- Tạo mới `src/core/base_ui.py`
- Tạo mới `src/core/base_loader.py`
- Tạo mới `src/ui/dashboard_app.py`
- Tạo mới `src/db/templates/sql/dashboard_doichieu/ho_so_kham_benh_ngoai_tru_doi_chieu.sql`
- Cập nhật `docs/knowledge/GEM_CODE_MAP.md`
- Cập nhật `docs/prompts/20260514_1420_tao_man_hinh_dashboard_doi_chieu_v1.md`

## Nội dung đã thực hiện

### 1) Khởi tạo BaseUI theo Native OOP cho NiceGUI
- Tạo lớp `BaseUI` với các năng lực lõi:
  - Dựng layout chung gồm Header và Navigation Drawer.
  - DB helper dạng context manager `get_db_context()` để cấp phát kết nối `pyodbc` độc lập cho từng truy vấn, không dùng connection dùng chung vĩnh cửu.
  - Chuẩn hóa prepend `SET NOCOUNT ON;` trước SQL runtime.
  - Bọc truy vấn giao diện bằng `await nicegui.run.io_bound(...)` để bảo đảm non-blocking Main Event Loop.

### 2) Khởi tạo BaseLoader dùng chung Auto/Manual
- Tạo lớp `BaseLoader` với:
  - `execute_load()` quản lý transaction cấp Python: `autocommit=False`, success thì commit, lỗi thì rollback toàn cục.
  - Chuẩn prepend `SET NOCOUNT ON;` cho SQL thực thi.
  - Hàm `run_bcp_utf16le(...)` dùng BCP cờ `-w` (UTF-16-LE).
- Tạo `GenericTableLoader` kế thừa `BaseLoader` để UI Manual Runner có thể import và chạy trực tiếp, không dùng subprocess độc lập.

### 3) Tạo ứng dụng Dashboard NiceGUI 4 màn hình theo OOP
- Tạo `src/ui/dashboard_app.py` gồm các class màn hình kế thừa từ `BaseUI`:
  - Màn hình 1: Đối chiếu kết quả từ SQL template, dùng marker `?` và gọi DB qua `run.io_bound`.
  - Màn hình 2: Manual Runner chọn bảng và thời gian, chạy loader bằng `await run.io_bound(loader.execute_load)`.
  - Màn hình 3: Lịch sử chạy job, hiển thị trạng thái Success/Failed theo màu.
  - Màn hình 4: Trang báo cáo khung trắng để dọn đường tích hợp logic V1.
- Tích hợp `ui.log` + `asyncio.Queue` để streaming log thời gian thực từ loader lên UI.

### 4) Tạo SQL template đối chiếu mẫu
- Tạo file `src/db/templates/sql/dashboard_doichieu/ho_so_kham_benh_ngoai_tru_doi_chieu.sql`:
  - Có `SET NOCOUNT ON;`
  - Dùng marker `?` cho `@TuNgay`, `@DenNgay`
  - Đối chiếu RowCount/SUM giữa `dbo` -> `hanoi_hisnano_v2` -> `dm`
  - Có fallback doanh thu đúng chuẩn: `SUM(ISNULL(TongTienSauTangGiam, TongTien))`

### 5) Cập nhật tri thức
- `docs/knowledge/GEM_CODE_MAP.md` đã bổ sung danh sách file UI/lõi/SQL template mới theo yêu cầu task.

## Phụ thuộc hệ thống
- `pyproject.toml` hiện đã có đủ dependency cần thiết cho hạng mục này:
  - `nicegui>=3.12.0`
  - `pyodbc>=5.3.0`

## Phạm vi cập nhật theo yêu cầu 20260515_0835_tao_man_hinh_dashboard_doi_chieu_v2
- Cập nhật `pyproject.toml` để thêm `python-dotenv`
- Cập nhật `src/core/base_ui.py`
- Cập nhật `src/core/base_loader.py`
- Cập nhật `src/ui/dashboard_app.py`
- Tạo mới `src/ui/main_app.py`
- Tạo mới `src/ui/pages/__init__.py`
- Tạo mới `src/ui/pages/common.py`
- Tạo mới `src/ui/pages/doi_chieu_page.py`
- Tạo mới `src/ui/pages/manual_runner_page.py`
- Tạo mới `src/ui/pages/job_history_page.py`
- Tạo mới `src/ui/pages/bao_cao_page.py`
- Tạo mới `src/db/templates/sql/dashboard_doichieu/dim_luot_kham/production.sql`
- Tạo mới `src/db/templates/sql/dashboard_doichieu/dim_luot_kham/staging.sql`
- Tạo mới `src/db/templates/sql/dashboard_doichieu/dim_luot_kham/datamart.sql`
- Tạo mới `src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/production.sql`
- Tạo mới `src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/staging.sql`
- Tạo mới `src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/datamart.sql`
- Cập nhật `docs/knowledge/GEM_CODE_MAP.md`
- Cập nhật `docs/prompts/20260515_0835_tao_man_hinh_dashboard_doi_chieu_v2.md`

## Nội dung đã thực hiện

### 1) Chuẩn hóa BaseUI theo quy tắc Context Manager + Semaphore toàn cục
- `BaseUI` nạp `.env` bằng `python-dotenv`, đọc `MAX_CONCURRENT_CONNECTIONS` với fallback mặc định `5`.
- Khởi tạo `asyncio.Semaphore` một lần duy nhất ở cấp class để giới hạn kết nối đồng thời.
- DB helper `get_db_context(connection_string_var)` lấy chuỗi kết nối theo biến môi trường và tự đóng kết nối sau truy vấn.
- Mọi truy vấn UI đều chạy qua `await nicegui.run.io_bound(...)` và prepend `SET NOCOUNT ON;`.

### 2) Chuẩn hóa BaseLoader cho Manual Runner/Auto Runner
- `execute_load(*args, **kwargs)` hỗ trợ nhận tham số động `from_date`, `to_date`.
- Quản lý transaction Python-level (`autocommit=False`, commit/rollback toàn cục).
- BCP vẫn dùng UTF-16-LE với cờ `-w`.
- Queue log an toàn luồng: dùng `loop.call_soon_threadsafe(queue.put_nowait, msg)`.
- Luôn đẩy Poison Pill `[DONE]` ở khối `finally` để UI ngắt vòng đọc log an toàn.

### 3) Tách kiến trúc UI theo mô hình Pages
- Tạo entry chính `src/ui/main_app.py` có block:
  - `if __name__ in {"__main__", "__mp_main__"}:`
  - `ui.run(title=..., port=...)`
- Tách 4 màn hình riêng trong `src/ui/pages/`:
  - `doi_chieu_page.py`
  - `manual_runner_page.py`
  - `job_history_page.py`
  - `bao_cao_page.py`
- Các class đều kế thừa `BaseUI` và route bằng decorator `@ui.page`.

### 4) Backend đối chiếu bất đồng bộ chống chết chùm
- `src/ui/dashboard_app.py` hiện là backend class `DashboardCompareBackend`.
- Chạy đồng thời 3 nhánh `production`, `staging`, `datamart` bằng `asyncio.gather(..., return_exceptions=True)`.
- Production multi-tenant:
  - Quét tất cả biến `PROD_CONNECTION_*`.
  - Chạy cùng `production.sql` trên nhiều nguồn.
  - Tổng hợp số liệu bằng Python.
- Staging dynamic schema:
  - Dùng template `{staging_schema}` trong `staging.sql`.
  - Render bằng `.format(staging_schema=...)`.
  - Chạy song song, gom lỗi theo từng schema.
- Validate cứng consistency marker `?` giữa 3 file SQL cùng domain.

### 5) SQL template theo domain tách biệt
- Tạo đầy đủ 3 file cho `dim_luot_kham`:
  - `production.sql`, `staging.sql`, `datamart.sql` (chỉ RowCount).
- Tạo đầy đủ 3 file cho `fact_thu_phi_dich_vu`:
  - `production.sql`, `staging.sql`, `datamart.sql`.
- Logic doanh thu fallback đúng chuẩn:
  - `SUM(ISNULL(TongTienSauTangGiam, TongTien))` chỉ nằm trong domain doanh thu.

### 6) Manual Runner theo tiêu chuẩn an toàn luồng
- Lấy loop tường minh `loop = asyncio.get_running_loop()` trước `run.io_bound`.
- Gọi loader đúng mẫu:
  - `await nicegui.run.io_bound(loader.execute_load, from_date, to_date, queue=log_queue, loop=loop)`.
- Truyền `datetime.date` native cho pyodbc bind marker `?`.
- Nút Run Job được `.disable()` khi bắt đầu và `.enable()` ở `finally` để chống spam.
- Vòng đọc `asyncio.Queue` dừng bằng `break` khi nhận `[DONE]`.

### 7) Cập nhật tri thức
- Đã đăng ký toàn bộ file UI/Base Class/SQL template mới vào nhóm `INTERFACE` trong `GEM_CODE_MAP.md`.

## Phạm vi cập nhật theo yêu cầu 20260515_1315_tao_man_hinh_dashboard_doi_chieu_v3
- Cập nhật `src/ui/main_app.py`
- Cập nhật `src/ui/pages/common.py`
- Cập nhật `src/ui/pages/doi_chieu_page.py`
- Cập nhật `src/ui/pages/manual_runner_page.py`
- Cập nhật `src/ui/pages/job_history_page.py`
- Cập nhật `src/ui/pages/bao_cao_page.py`
- Cập nhật `src/ui/pages/__init__.py`
- Cập nhật `docs/prompts/20260515_1315_tao_man_hinh_dashboard_doi_chieu_v3.md`

## Nội dung đã thực hiện

### 1) Ghi nhận lỗi gốc UI tàng hình
- Khi chạy `uv run python -m src.ui.main_app`, root trả JSON API thay vì giao diện.
- Nguyên nhân chính:
  - Route trang đối chiếu chưa được cố định theo URL chuyên biệt `/doi-chieu`.
  - Cơ chế route đặt trong hàm đăng ký khiến việc nạp route không tường minh ở entry point.
  - Thiếu route gốc điều hướng từ `/` sang trang giao diện.

### 2) Khắc phục tại entry point `src/ui/main_app.py`
- Import tường minh các module pages để decorators `@ui.page` được nạp ngay khi khởi chạy.
- Tạo route gốc:
  - `@ui.page("/")`
  - `ui.navigate.to("/doi-chieu")`
- Giữ chuẩn block chạy cuối file với `if __name__ in {"__main__", "__mp_main__"}:` và `ui.run(...)`.

### 3) Chuẩn hóa định tuyến pages theo tiêu chuẩn an toàn scope
- Áp dụng wrapper function module-level cho từng route, mỗi request khởi tạo object mới:
  - `@ui.page('/doi-chieu')` -> tạo mới `DoiChieuPage()` trong hàm route.
  - `@ui.page('/manual-runner')` -> tạo mới `ManualRunnerPage()`.
  - `@ui.page('/job-history')` -> tạo mới `JobHistoryPage()`.
  - `@ui.page('/bao-cao')` -> tạo mới `BaoCaoPage()`.
- Không dùng instance toàn cục, tránh State Leakage giữa các client/tab.

### 4) Đồng bộ điều hướng nội bộ
- Cập nhật menu trong `src/ui/pages/common.py`:
  - Đổi route đối chiếu từ `/` sang `/doi-chieu`.
- Cập nhật `active_route` tương ứng trong `DoiChieuPage`.

### 5) Cập nhật mô-đun pages
- `src/ui/pages/__init__.py` chuyển sang import module-level để nạp route decorators tự động.
- Loại bỏ phụ thuộc vào hàm đăng ký route thủ công.

## Phạm vi cập nhật theo yêu cầu 20260515_1340_tao_man_hinh_dashboard_doi_chieu_v4
- Cập nhật `src/ui/main_app.py`
- Cập nhật `config/.env`
- Cập nhật `docs/prompts/20260515_1340_tao_man_hinh_dashboard_doi_chieu_v4.md`

## Nội dung đã thực hiện

### 1) Khóa xung đột route giữa API và UI
- Rà soát toàn bộ mã nguồn không còn định nghĩa `@app.get('/')`.
- Bổ sung endpoint API riêng tại `@app.get('/api/health')` trong `src/ui/main_app.py` để tách biệt hoàn toàn khỏi route giao diện.
- Giữ route UI gốc `@ui.page('/')` và điều hướng về `/doi-chieu`.

### 2) Chuẩn hóa nạp biến môi trường trước khi đọc port
- `src/ui/main_app.py` đã nạp `.env` bằng:
  - `from dotenv import load_dotenv`
  - `load_dotenv('config/.env', override=False)`
- Chỉ sau đó mới đọc biến môi trường để chạy UI.

### 3) Đổi sang cấu hình port động UI
- `ui.run()` chuyển sang dùng `UI_PORT` với fallback cứng theo yêu cầu:
  - `port=int(os.getenv('UI_PORT', '9005'))`
- Đã thêm biến cấu hình trong `config/.env`:
  - `UI_PORT=9005`

### 4) Đảm bảo an toàn scope trang UI
- Các trang trong `src/ui/pages/` giữ mô hình wrapper function với `@ui.page(...)`.
- Mỗi request đều khởi tạo instance class mới trong wrapper, không dùng instance toàn cục.

## Phạm vi cập nhật theo yêu cầu 20260515_1610_bo_sung_bang_doi_chieu_v1
- Tạo mới 12 SQL template cho 4 domain dimension:
  - `src/db/templates/sql/dashboard_doichieu/dim_benh_nhan/{production.sql,staging.sql,datamart.sql}`
  - `src/db/templates/sql/dashboard_doichieu/dim_benh/{production.sql,staging.sql,datamart.sql}`
  - `src/db/templates/sql/dashboard_doichieu/dim_dich_vu/{production.sql,staging.sql,datamart.sql}`
  - `src/db/templates/sql/dashboard_doichieu/dim_loai_goi_dich_vu/{production.sql,staging.sql,datamart.sql}`
- Cập nhật `src/ui/dashboard_app.py`
- Cập nhật `src/ui/pages/doi_chieu_page.py`
- Cập nhật `src/ui/main_app.py`
- Cập nhật `docs/prompts/20260515_1610_bo_sung_bang_doi_chieu_v1.md`

## Nội dung đã thực hiện

### 1) Mở rộng domain đối chiếu theo thứ tự ưu tiên mới
- Backend đối chiếu mở rộng danh sách domain theo đúng thứ tự hiển thị:
  1. `dim_benh_nhan`
  2. `dim_benh`
  3. `dim_dich_vu`
  4. `dim_loai_goi_dich_vu`
  5. `dim_luot_kham`
  6. `fact_thu_phi_dich_vu`

### 2) Tạo SQL template full-load count cho 4 dimension mới
- Mỗi file đều có:
  - `SET NOCOUNT ON;`
  - `DECLARE @TuNgay DATE = ?;`
  - `DECLARE @DenNgay DATE = ?;`
  - `SELECT COUNT(1) AS [RowCount]`
- Không dùng `@TuNgay/@DenNgay` trong `WHERE` cho 4 bảng dim mới.
- Không chỉnh sửa bất kỳ SQL nào thuộc `dim_luot_kham` và `fact_thu_phi_dich_vu`.

### 3) Refactor DoiChieuPage sang Multi-Grid All-in-one
- Giao diện bỏ dropdown chọn bảng.
- Header chỉ giữ:
  - `Từ ngày`
  - `Đến ngày`
  - nút `Chạy đối chiếu toàn bộ`
- Kết quả render trong `ui.scroll_area`, mỗi domain là một `ui.card()` + `ui.table()` riêng.
- Container kết quả được `clear()` trước mỗi lần chạy.

### 4) Dynamic columns và chuẩn hóa None -> 0
- Backend chuẩn hóa toàn bộ số liệu `None` về `0.0` trước khi trả về UI.
- Bảng kết quả sinh cột động theo keys metric.
- Với dimension: chỉ hiển thị metric `RowCount`.
- Với `fact_thu_phi_dich_vu`: bảo đảm hiển thị tập metric gồm `RowCount`, `TongTien`, `TongTienSauTangGiam` (nếu thiếu từ SQL sẽ mặc định 0).

### 5) Chốt chặn kỹ thuật UI_PORT
- `src/ui/main_app.py` bổ sung hàm `resolve_ui_port()` dùng `try/except` khi ép kiểu port.
- Fallback cứng `9005` khi biến môi trường rỗng/sai định dạng/<=0.

## Phạm vi cập nhật theo yêu cầu 20260516_1105_sua_loi_dashboard_doi_chieu_v1
- Cập nhật `src/ui/dashboard_app.py`
- Cập nhật `REPORT_CHANGES.md`
- Cập nhật `docs/prompts/20260516_1105_sua_loi_dashboard_doi_chieu_v1.md`

## Nội dung đã thực hiện

### 1) Khắc phục lỗi gộp số liệu Decimal gây hiển thị 0
- Nguyên nhân gốc: hàm gộp chỉ nhận `int/float`, trong khi giá trị `SUM` từ pyodbc thường trả về `decimal.Decimal`, dẫn tới bị loại khỏi phép cộng.
- Đã sửa:
  - `from decimal import Decimal`
  - `_merge_numeric` nhận `(int, float, Decimal)`
  - `_normalize_metric_map` nhận `(int, float, Decimal)`
- Kết quả: số liệu `TongTien`, `TongTienSauTangGiam` được cộng dồn đúng thay vì rơi về 0.

### 2) Cố định mapping đa nguồn đúng cấu trúc dữ liệu
- Giữ chuẩn:
  - `prod_result`/`stg_result` đọc từ dict `['values']`.
  - `dm_result` đọc từ list dòng đầu tiên.
- Bổ sung chống crash khi Datamart trả rỗng:
  - `dm_data = dm_result[0] if dm_result else {}`
- Rà soát và xác nhận không còn tàn dư `TotalRevenue`; mapping chỉ dùng key đúng chuẩn:
  - `TongTien`
  - `TongTienSauTangGiam`

### 3) Bổ sung traceback bắt buộc cho mọi nhánh lỗi
- Đã thêm `import traceback`.
- Tại các nhánh exception của Production, Staging, Datamart và lỗi tổng hợp domain, đều in đầy đủ stack trace bằng `traceback.print_exc()` trước khi trả trạng thái lỗi về UI.
- Mục tiêu: không còn hiện tượng nuốt lỗi làm khó truy vết trên terminal Master.

## Phạm vi cập nhật theo yêu cầu 20260518_0900_xay_dung_khung_dong_bo_v1
- Tạo mới `src/jobs/__init__.py`
- Tạo mới `src/jobs/dimension_loader.py`
- Tạo mới `src/jobs/fact_loader.py`
- Tạo mới `src/jobs/sync_orchestrator.py`
- Cập nhật `PROJECT_CHRONICLE.md`
- Cập nhật `docs/knowledge/GEM_CODE_MAP.md`
- Cập nhật `docs/knowledge/GEM_DATA_FLOW.md`
- Cập nhật `docs/knowledge/GEM_AUTO_PIPELINE.md`
- Cập nhật `docs/knowledge/GEM_DB_SCHEMAS.md`
- Cập nhật `docs/knowledge/GEM_DEPENDENCY_GRAPH.md`
- Cập nhật `docs/prompts/20260518_0900_xay_dung_khung_dong_bo_v1.md`

## Nội dung đã thực hiện

### 1) Xây dựng khung jobs theo OOP, kế thừa BaseLoader
- `DimensionLoader(BaseLoader)`:
  - Full-load 2-Hop: Production -> ODS cơ sở -> Datamart.
  - Chặng 1 dùng `TRUNCATE` + `bcp -w` theo từng bảng nguồn dimension.
  - Chặng 2 chạy MERGE template theo domain.
- `FactLoader(BaseLoader)`:
  - Incremental 3-Hop với Lookback D-3.
  - Prod -> Landing: `TRUNCATE stg_nano_v2` + `bcp -w`.
  - Landing -> ODS: MERGE có hard delete giới hạn thời gian D-3.
  - ODS -> Datamart: MERGE batch `TOP (10000)`.
  - Áp dụng fallback seed `-1` cho `LuotKhamKey`, `BenhNhanKey`, `DichVuKey`.
  - Cleanup Landing ở đầu và cuối luồng (`finally`).
- `SyncOrchestrator`:
  - Chạy tuần tự từng facility.
  - Hỗ trợ Selective Sync qua `ACTIVE_FACILITIES` hoặc `run(target_facilities=...)`.
  - Nếu không truyền hoặc `ALL` thì chạy toàn bộ facility đã định nghĩa.

### 2) Chốt chặn an toàn dữ liệu Hard Delete
- ODS hard delete chỉ trong cửa sổ D-3 (`Target.<NgayCol> BETWEEN @LookbackDate AND @ToDate`).
- Datamart hard delete có đủ 3 chốt:
  - cửa sổ D-3,
  - `Target.NguonDuLieuKey = @CurrentNguonDuLieu`,
  - `Target.MaCoSo = @CurrentMaCoSo`.
- Điều kiện ON MERGE Datamart cô lập business key đa cơ sở bằng `Target.NguonDuLieuKey = Source.NguonDuLieuKey`.

### 3) Cập nhật tri thức bắt buộc
- `PROJECT_CHRONICLE.md`: thêm cụm ADR-06..ADR-09 cho đợt ETL v1.
- `GEM_CODE_MAP.md`: khai báo 3 module jobs mới và chức năng.
- `GEM_DATA_FLOW.md`: đặc tả 2-Hop/3-Hop, D-3, seed `-1`, hard delete guardrails.
- `GEM_AUTO_PIPELINE.md`: quy tắc điều phối tuần tự + selective sync.
- `GEM_DB_SCHEMAS.md`: chuẩn hóa vai trò schema `stg_nano_v2`, `<facility>_hisnano_v2`, `dm`.
- `GEM_DEPENDENCY_GRAPH.md`: đồ thị phụ thuộc module mới.

### 4) Kiểm tra kỹ thuật
- Đã chạy kiểm tra cú pháp:
  - `python -m py_compile src/jobs/dimension_loader.py src/jobs/fact_loader.py src/jobs/sync_orchestrator.py src/jobs/__init__.py`
- Kết quả: pass, không có lỗi syntax.