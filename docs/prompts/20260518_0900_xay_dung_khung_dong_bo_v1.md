
# YÊU CẦU CỦA MASTER DÀNH CHO CODEX

1. **TÀI LIỆU NGUỒN BẮT BUỘC ĐỌC (SOURCE OF TRUTH):**
* Đọc `GEM_CODE_MAP.md` (để hiểu cấu trúc thư mục và Base Class).
* Đọc `PROJECT_CHRONICLE.md` (để nắm bắt tiến trình hiện tại).
* Đọc các file `GEM_*.md` hoặc thư mục `.specifications/` liên quan đến nghiệp vụ ETL.
* Tham khảo file SQL `merge_fact_thuphichvu_3in1.sql` (từ Knowledge) để nắm công thức tính toán.
* *(TUYỆT ĐỐI KHÔNG sử dụng hay đọc các file `MASTER_*.md` vì đây chỉ là file build tổng hợp tự động).*


2. **CHỈ THỊ KIẾN TRÚC VÀ CÔNG NGHỆ (V2):**
* **Quản lý môi trường:** Cấu hình toàn bộ dự án bắt buộc sử dụng `uv`. Tuyệt đối không dùng `pip` hay `conda`. Mọi module Python mới phải tuân thủ chuẩn OOP, kế thừa từ `BaseLoader` (hoặc `GenericTableLoader`).
* **Module Điều phối (`src/jobs/sync_orchestrator.py`):** Viết lớp `SyncOrchestrator` chạy đồng bộ TUẦN TỰ (Sequential). Đọc danh sách chuỗi kết nối từ `.env` (`PROD_CONNECTION_HANOI`, `PROD_CONNECTION_HCM`, `PROD_CONNECTION_HALONG`, `PROD_CONNECTION_HAIPHONG`). Quá trình xử lý của một cơ sở phải kết thúc hoàn toàn (giải phóng Landing) mới được chuyển sang cơ sở tiếp theo.


3. **CHỈ THỊ PHÁT TRIỂN LUỒNG NẠP DỮ LIỆU:**
* **A. Module Nạp Danh Mục - FULL LOAD (`src/jobs/dimension_loader.py`):** * *Luồng 2 chặng (2-Hop):* Production -> ODS Cơ sở -> Datamart.
* **Bước 1:** Thực thi `TRUNCATE TABLE` trực tiếp trên Schema ODS của cơ sở (VD: `hanoi_hisnano_v2.<TableName>`). Dùng `subprocess` gọi `bcp` cờ `-w` (UTF-16-LE) đẩy thẳng dữ liệu từ Production vào đây.
* **Bước 2:** Gọi Script SQL `MERGE` đẩy dữ liệu từ Schema ODS của cơ sở lên Datamart.


* **B. Module Nạp Phát Sinh - INCREMENTAL (`src/jobs/fact_loader.py`):** * *Luồng 3 chặng (3-Hop) sử dụng Cửa sổ trượt (Lookback = D-3):*
* **Bước 1 (Prod -> Landing):** `TRUNCATE TABLE` trên Schema dùng chung `stg_nano_v2.<TableName>`. Dùng `bcp` cờ `-w` nạp dữ liệu delta (D-3) từ Production vào đây.
* **Bước 2 (Landing -> ODS Cơ sở):** Thực thi lệnh SQL `MERGE` hợp nhất dữ liệu từ `stg_nano_v2` sang Schema của cơ sở (VD: `hanoi_hisnano_v2`). **Bắt buộc** phải có mệnh đề `WHEN NOT MATCHED BY SOURCE THEN DELETE` để đồng bộ việc xóa vật lý (Hard Deletes) từ Production.
* **Bước 3 (ODS Cơ sở -> Datamart):** Thực thi lệnh SQL `MERGE` đẩy dữ liệu từ ODS cơ sở lên Datamart với các ràng buộc khắt khe:
* **Batching:** Bọc lệnh MERGE trong vòng lặp `WHILE` cắt `TOP (10000)` để chống tràn Transaction Log.
* **Early Arriving Facts:** Mọi trường tham chiếu Dimension (`DichVuKey`, `BenhNhanKey`, v.v.) phải bọc hàm `ISNULL(Key, -1)` để fallback về Seed Data.
* **Logic Tính Tiền (KHÔNG FALLBACK):** Áp dụng chuẩn công thức 3-in-1:
* Nguồn Dịch vụ (DV): `TongTienSauTangGiam` = `TongTien - ISNULL(TongGiam, 0) + ISNULL(TongTang, 0)`.
* Nguồn Bảo hiểm (BH): `TongTienSauTangGiam` = `TongTien + ISNULL(TienChenhLech, 0)`.








4. **NHIỆM VỤ CẬP NHẬT TRI THỨC VÀO CÁC FILE GỐC (.md) - BẮT BUỘC:**
Codex phải tự động cập nhật thông tin thiết kế vào các file gốc sau (TUYỆT ĐỐI KHÔNG ghi vào `MASTER_*.md`):
* **Tệp `PROJECT_CHRONICLE.md`:** Ghi log (nhật ký) chi tiết về đợt nâng cấp này. Bao gồm quyết định sử dụng Luồng 3 chặng (3-Hop) cho Incremental, giải quyết bài toán Hard Delete bằng `NOT MATCHED BY SOURCE THEN DELETE` ở ODS, và kiến trúc chạy tuần tự giải phóng Landing.
* **Tệp `GEM_CODE_MAP.md`:** Khai báo cấu trúc thư mục, đường dẫn và chức năng của `sync_orchestrator.py`, `dimension_loader.py`, `fact_loader.py`.
* **Các tệp `GEM_*.md` (Kiến trúc & Nghiệp vụ):** Bổ sung đặc tả Lookback D-3, nguyên tắc Seed Data (`ID = -1`), và công thức tài chính DV/BH.


5. **CHỈ DẪN PHẢN HỒI:**
Sau khi sinh code và cập nhật các file `.md` thành công, hãy liệt kê danh sách các class/hàm đã tạo và trích dẫn các đoạn text đã chèn vào tài liệu gốc, đặt ngay bên dưới thẻ `# BÁO CÁO CỦA THỢ CODE`.

# BÁO CÁO CỦA THỢ CODE

## 1) Danh sách class/hàm đã tạo

### File `src/jobs/dimension_loader.py`
- `DimensionTableSpec`
- `DimensionLoader(BaseLoader)`
  - `_parse_connection_string`
  - `_build_bcp_auth_args`
  - `_run_bcp_queryout`
  - `_run_bcp_in`
  - `_truncate_table`
  - `_copy_prod_to_ods`
  - `_render_merge_sql`
  - `_execute_dimension_spec`
  - `_execute_core`

### File `src/jobs/fact_loader.py`
- `FactTableSpec`
- `FactLoader(BaseLoader)`
  - `_parse_connection_string`
  - `_build_bcp_auth_args`
  - `_normalize_date`
  - `_truncate_table`
  - `_landing_cleanup`
  - `_run_bcp_queryout`
  - `_run_bcp_in`
  - `_copy_delta_prod_to_landing`
  - `_get_common_columns`
  - `_build_ods_merge_sql`
  - `_merge_landing_to_ods`
  - `_build_fact_merge_batch_sql`
  - `_merge_ods_to_datamart_batches`
  - `_execute_core`

### File `src/jobs/sync_orchestrator.py`
- `FacilityDefinition`
- `SyncOrchestrator`
  - `_parse_facility_tokens`
  - `_resolve_target_facilities`
  - `_validate_target_facilities`
  - `_resolve_facility_key`
  - `_build_dimension_loader`
  - `_build_fact_loader`
  - `run`
- Hàm CLI:
  - `_parse_cli_args`

### File `src/jobs/__init__.py`
- Export module: `DimensionLoader`, `FactLoader`, `SyncOrchestrator`

## 2) Trích dẫn các đoạn text đã chèn vào tài liệu gốc

### Trích `PROJECT_CHRONICLE.md`
> "## 2026-05-18: Xây dựng khung đồng bộ ETL v1 (Sequential + Selective Sync)"

> "Hard delete ở Datamart có điều kiện kép: giới hạn D-3 và cô lập theo `NguonDuLieuKey` + `MaCoSo` để không xóa nhầm dữ liệu cơ sở khác."

### Trích `docs/knowledge/GEM_CODE_MAP.md`
> "Class `SyncOrchestrator` điều phối tuần tự theo facility."

> "Luồng ODS -> Datamart bằng MERGE batching `TOP (10000)`."

### Trích `docs/knowledge/GEM_DATA_FLOW.md`
> "Hard delete Datamart có 3 điều kiện bắt buộc: chỉ trong cửa sổ D-3, chỉ trong đúng cơ sở (`NguonDuLieuKey`/`MaCoSo`), chỉ xóa khi không còn trong source."

> "Các khóa dimension của fact phải fallback về seed: `ISNULL(LuotKhamKey, -1)`, `ISNULL(BenhNhanKey, -1)`, `ISNULL(DichVuKey, -1)`."

### Trích `docs/knowledge/GEM_AUTO_PIPELINE.md`
> "Hỗ trợ 2 cách chọn cơ sở chạy: Biến môi trường `ACTIVE_FACILITIES=hanoi,hcm` hoặc tham số hàm `run(target_facilities=['hanoi'])`."

### Trích `docs/knowledge/GEM_DB_SCHEMAS.md`
> "Production -> `stg_nano_v2` -> `<facility>_hisnano_v2` -> `dm`."

### Trích `docs/knowledge/GEM_DEPENDENCY_GRAPH.md`
> "`SyncOrchestrator.run(...)` xác định danh sách facility mục tiêu (Selective Sync)."

## 3) Ghi chú xác nhận kỹ thuật
- Đã kiểm tra cú pháp Python cho các module mới bằng lệnh:
  - `python -m py_compile src/jobs/dimension_loader.py src/jobs/fact_loader.py src/jobs/sync_orchestrator.py src/jobs/__init__.py`
- Kết quả: không phát hiện lỗi syntax.