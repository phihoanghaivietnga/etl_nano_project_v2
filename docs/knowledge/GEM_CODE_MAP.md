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