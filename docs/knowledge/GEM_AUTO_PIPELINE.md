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