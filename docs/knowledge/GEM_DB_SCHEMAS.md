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

## Cấu trúc bảng Datamart `dm`

### Bảng `dm.FactThuPhiDichVu`
Bảng fact tổng hợp doanh thu từ 3 nguồn (Dịch vụ, Bảo hiểm, Tang/Giam) phục vụ phân tích doanh thu và khách hàng.

#### Schema (các cột):
| Tên cột | Kiểu dữ liệu | Mô tả |
|---------|--------------|-------|
| NguonDuLieuKey | INT | Key nguồn dữ liệu (multi-tenant) |
| CoSoKey | INT | Key cơ sở |
| DateKey | INT | Khóa ngày dạng YYYYMMDD |
| LuotKhamKey | INT | Key lượt khám (lookup từ DimLuotKham) |
| BenhNhanKey | INT | Key bệnh nhân (lookup từ DimLuotKham) |
| DichVuKey | INT | Key dịch vụ (lookup từ DimDichVu) |
| MaCoSo | NVARCHAR(50) | Mã cơ sở |
| MaThuPhi | NVARCHAR(100) | Mã thu phí |
| MaPhieuDichVu | NVARCHAR(100) | Mã phiếu dịch vụ |
| MaHoSo | NVARCHAR(100) | Mã hồ sơ |
| MaChiTieu | NVARCHAR(100) | Mã chi tiêu |
| MaChiTieuBK | VARCHAR(255) | Business Key bất biến = NguonDuLieuKey + ':' + MaChiTieu |
| NgayDenKham | DATE | Ngày đến khám |
| NgayDoanhThu | DATE | Ngày doanh thu |
| DateKey | INT | Khóa ngày dạng YYYYMMDD |
| SoLuong | INT | Số lượng |
| TongTien | DECIMAL | Tổng tiền |
| TongTienSauTangGiam | DECIMAL | Tổng tiền sau điều chỉnh (Tang/Giam) |
| LoaiHinh | CHAR(2) | Loại hình ('DV' = Dịch vụ, 'BH' = Bảo hiểm) |
| SoHoaDon | NVARCHAR(100) | Số hóa đơn |
| DoanhThu | FLOAT | Doanh thu tính toán |
| DaThucHien | BIT | Đã thực hiện |
| TrangThaiPhieu | NVARCHAR(50) | Trạng thái phiếu |
| **MaGoiDichVu** | **VARCHAR(50)** | **Mã gói dịch vụ - Dùng để phân cụm và định danh bệnh nhân theo Gói Dịch Vụ, phục vụ báo cáo phân khúc khách hàng** |

#### Ghi chú:
- Trường `MaGoiDichVu` là trường mới được bổ sung để phục vụ logic phân tích khách hàng theo gói dịch vụ.
- Dữ liệu được đồng bộ từ tầng 2 qua SQL Template `merge_fact_thuphichvu_3in1.sql`.
