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