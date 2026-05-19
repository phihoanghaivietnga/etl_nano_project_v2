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
   - Nạp delta theo cửa sổ trượt `Lookback = from_date - lookback_days` bằng `bcp -w`.
   - Dynamic SELECT phải đọc metadata cột từ `INFORMATION_SCHEMA.COLUMNS` và loại cột theo `exclude_datatypes` trước khi extract.
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

## Mapping cột ngày cho incremental_tables
- `ThuPhiDichVu` -> `NgayDenKham`
- `ThuPhiBaoHiem` -> `NgayDenKham`
- `ThuPhiTangGiam` -> `NgayDenKham`
- `ThuPhiGoi` -> `NgayThu`
- `DoThiLuc` -> `NgayDo`
- `HoSoKhamBenhNgoaiTru` -> `NgayVaoKham`

## Quy tắc an toàn Landing dùng chung
- Luôn TRUNCATE Landing ở đầu luồng.
- Sau TRUNCATE Landing phải commit ngay để giải phóng lock trước khi BCP IN bằng session khác.
- Luồng hiện tại chạy tuần tự từng bảng fact trong cùng facility, không dùng TRUNCATE ở tầng Facility Historical Staging.