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