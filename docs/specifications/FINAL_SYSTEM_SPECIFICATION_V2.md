# FINAL SYSTEM SPECIFICATION V2 — ETL_NANO_PROJECT

## Phạm vi và Mục tiêu
Tài liệu này đặc tả bắt buộc cho 3 nhóm luồng ETL (Dimension, Fact Core, Revenue Group) và ánh xạ chi tiết 8 bảng nghiệp vụ theo ranh giới thực thi hiện hành của hệ thống ETL_Nano_Project V2.

Các quy ước xuyên suốt:
- Đọc nguồn từ `dbo` với `NOLOCK`.
- Enrichment Keys gồm: `NguonDuLieuKey`, `CoSoKey`, `MaCoSo`.
- Chuẩn Business Key: `NguonDuLieuKey:natural_key`.
- Dimension Full Load bỏ qua `stg_nano_v2`.
- Fact Incremental bắt buộc đi qua `stg_nano_v2`.
- Revenue Group xử lý theo cơ chế Group Sync.

---

## 1) NHÓM 1 — DIMENSION TABLES (FULL LOAD, BỎ QUA `stg_nano_v2`)

### 1.1. Bảng `DMBenhNhan`
- **Lược đồ Di chuyển (Schema Path):** `dbo.DMBenhNhan` -> `hanoi_hisnano_v2.DMBenhNhan` (TRUNCATE + INSERT) -> `dm.DimBenhNhan` (MERGE SCD Type 1).
- **Cơ chế Đồng bộ (Sync Mode):** Full Load; không dùng cột mốc thời gian incremental.
- **Quy tắc Khóa (Key Mapping):** Khóa tự nhiên `MaBenhNhan`; Business Key đích `NguonDuLieuKey:MaBenhNhan`; Enrichment Keys được tiêm trong bước MERGE từ staging sang đích.
- **File T-SQL MERGE:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\src\db\templates\sql\dimension\DimBenhNhan_merge.sql`.
- **Ràng buộc Toàn vẹn (Constraints/Anomalies):** Chuẩn hóa dữ liệu dân cư, số điện thoại, map giới tính/địa lý, SCD Type 1 overwrite khi `WHEN MATCHED`.
- **Tên file và đường dẫn lưu file:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\FINAL_SYSTEM_SPECIFICATION_V2.md`.

### 1.2. Bảng `DMBenh`
- **Lược đồ Di chuyển (Schema Path):** `dbo.DMBenh` -> `hanoi_hisnano_v2.DMBenh` (TRUNCATE + INSERT) -> `dm.DimBenh` (MERGE SCD Type 1).
- **Cơ chế Đồng bộ (Sync Mode):** Full Load; không dùng cột mốc thời gian incremental.
- **Quy tắc Khóa (Key Mapping):** Khóa tự nhiên `MaBenh`; Business Key đích `NguonDuLieuKey:MaBenh`; Enrichment Keys tiêm khi MERGE từ staging cơ sở sang Datamart.
- **File T-SQL MERGE:** ưu tiên thiết kế `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\schemas\dimension\DimBenh_merge.sql`; hiện trạng thực thi tương ứng nằm trong mã nguồn loader tại `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\src\auto_runner\loader.py` (luồng `_merge_dimbenh_direct`).
- **Ràng buộc Toàn vẹn (Constraints/Anomalies):** Tuân thủ SCD Type 1; chỉ cập nhật/cấy dữ liệu danh mục bệnh, không thay đổi DDL đích.
- **Tên file và đường dẫn lưu file:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\FINAL_SYSTEM_SPECIFICATION_V2.md`.

### 1.3. Bảng `LoaiGoiDichVuNT`
- **Lược đồ Di chuyển (Schema Path):** `dbo.LoaiGoiDichVuNT` -> `hanoi_hisnano_v2.LoaiGoiDichVuNT` (TRUNCATE + INSERT) -> `dm.DimLoaiGoiDichVu` (MERGE).
- **Cơ chế Đồng bộ (Sync Mode):** Full Load; không dùng cột mốc thời gian incremental.
- **Quy tắc Khóa (Key Mapping):** Khóa tự nhiên `MaLoaiGoi`; Business Key chuẩn hóa `NguonDuLieuKey:MaLoaiGoi` (`MaLoaiGoiBK`); Enrichment Keys được tiêm tại MERGE.
- **File T-SQL MERGE:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\src\db\templates\sql\dimension\DimLoaiGoiDichVu_merge.sql`.
- **Ràng buộc Toàn vẹn (Constraints/Anomalies):** `MaCoSo`, `CoSoKey`, `NguonDuLieuKey` bắt buộc đồng bộ nhất quán với facility config; MERGE cập nhật `NgayDongBo`.
- **Tên file và đường dẫn lưu file:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\FINAL_SYSTEM_SPECIFICATION_V2.md`.

### 1.4. Bảng `DMLoaiDichVu` (và cụm Dịch vụ)
- **Lược đồ Di chuyển (Schema Path):** `dbo.DMLoaiDichVu` -> `hanoi_hisnano_v2.DMLoaiDichVu` (TRUNCATE + INSERT) -> `stg.DMLoaiDichVu`; cụm dịch vụ hợp nhất cuối vào `dm.DimDichVu`.
- **Cơ chế Đồng bộ (Sync Mode):** Full Load cho danh mục dịch vụ; không dùng mốc incremental.
- **Quy tắc Khóa (Key Mapping):** `DMLoaiDichVu` theo khóa tự nhiên `MaLoaiDichVu`; `DimDichVu` chuẩn BK `NguonDuLieuKey:MaChiTieu`; Enrichment Keys tiêm khi MERGE.
- **File T-SQL MERGE:** logic chuẩn thiết kế tham chiếu `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\schemas\dim_dich_vu_merge.sql`; hiện trạng codebase đang vận hành gộp 3-in-1 tương ứng qua loader (`_merge_dimdichvu_3in1`).
- **Ràng buộc Toàn vẹn (Constraints/Anomalies):** `DMDichVu` và `DMDichVuChiTiet` đang `enabled: false` trong `config/tables.yaml`, được xử lý theo luồng gộp tự động để tạo `dm.DimDichVu`.
- **Tên file và đường dẫn lưu file:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\FINAL_SYSTEM_SPECIFICATION_V2.md`.

---

## 2) NHÓM 2 — FACT CORE TABLES (INCREMENTAL, QUA `stg_nano_v2`)

### 2.1. Bảng `HoSoKhamBenhNgoaiTru` (đích `dm.DimLuotKham`)
- **Lược đồ Di chuyển (Schema Path):** `dbo.HoSoKhamBenhNgoaiTru` -> `stg_nano_v2.HoSoKhamBenhNgoaiTru` -> `hanoi_hisnano_v2.HoSoKhamBenhNgoaiTru` -> `dm.DimLuotKham`.
- **Cơ chế Đồng bộ (Sync Mode):** Incremental theo `NgayVaoKham`, lọc khép kín theo khoảng ngày; truy vấn extract bắt buộc để `columns=None` nhằm tránh kéo nhầm cột enrichment từ Production.
- **Quy tắc Khóa (Key Mapping):** Khóa nghiệp vụ `MaHoSo + NgayVaoKham`; BK luồng `MaHoSoBK = NguonDuLieuKey:MaHoSo`; Enrichment Keys chỉ được tiêm ở bước MERGE trung gian.
- **File T-SQL MERGE:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\src\db\templates\sql\fact\DimLuotKham_merge.sql`.
- **Ràng buộc Toàn vẹn (Constraints/Anomalies):** Bảo toàn ngầm định 20 cột chẩn đoán mở rộng tại `dm.DimLuotKham` (`ChanDoan1-10`, `ChanDoan1_2-10_2`), không thay đổi DDL; date filter phải nằm đúng vị trí WHERE/MERGE để tránh GAP 100%.
- **Tên file và đường dẫn lưu file:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\FINAL_SYSTEM_SPECIFICATION_V2.md`.

### 2.2. Bảng `DoThiLuc`
- **Lược đồ Di chuyển (Schema Path):** `dbo.DoThiLuc` -> `stg_nano_v2.DoThiLuc` -> `dm.FactDoThiLuc` (qua MERGE theo template fact).
- **Cơ chế Đồng bộ (Sync Mode):** Incremental theo `NgayDo`.
- **Quy tắc Khóa (Key Mapping):** Khóa chính thực thi theo luồng `MaHoSo` + `NgayDo` + `NguonDuLieuKey` (điều kiện MERGE); Enrichment Keys lấy trực tiếp từ staging đã enrich.
- **File T-SQL MERGE:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\src\db\templates\sql\fact\FactDoThiLuc_merge.sql`.
- **Ràng buộc Toàn vẹn (Constraints/Anomalies):** Không COALESCE enrichment keys ở lớp merge chính để tránh drift định danh cơ sở; phải giữ điều kiện lọc ngày trong source subquery.
- **Tên file và đường dẫn lưu file:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\FINAL_SYSTEM_SPECIFICATION_V2.md`.

---

## 3) NHÓM 3 — REVENUE GROUP & PHỤ TRỢ

### 3.1. Cụm 3-in-1: `ThuPhiDichVu` (Lead), `ThuPhiBaoHiem`, `ThuPhiTangGiam`
- **Lược đồ Di chuyển (Schema Path):** `dbo.ThuPhiDichVu` + `dbo.ThuPhiBaoHiem` + `dbo.ThuPhiTangGiam` -> `stg_nano_v2.(3 bảng tương ứng)` -> MERGE gộp chung vào `dm.FactThuPhiDichVu`.
- **Cơ chế Đồng bộ (Sync Mode):** Incremental theo `NgayDenKham` với Group Sync cho toàn cụm doanh thu.
- **Quy tắc Khóa (Key Mapping):** JOIN/MERGE keys: `MaHoSo + MaChiTieu + MaPhieuDichVu`; Business Key dịch vụ: `MaChiTieuBK = NguonDuLieuKey:MaChiTieu`; Enrichment Keys inject trước khi vào bước merge gộp.
- **File T-SQL MERGE:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\schemas\merge_fact_thuphichvu_3in1.sql` (kèm template phụ nếu tách luồng: `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\schemas\FactThuPhiDichVu_merge_template.sql`, `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\schemas\FactThuPhiBaoHiem_merge_template.sql`, `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\schemas\FactThuPhiTangGiam_merge_template.sql`).
- **Ràng buộc Toàn vẹn (Constraints/Anomalies):** Bắt buộc công thức chống NULL doanh thu sau điều chỉnh theo chuẩn nghiệp vụ: `ISNULL(TongTienSauTangGiam, TongTien)`; kiểm soát không nhân bản dòng khi tổng hợp tăng/giảm (pre-aggregate trước join).
- **Tên file và đường dẫn lưu file:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\FINAL_SYSTEM_SPECIFICATION_V2.md`.

### 3.2. Bảng `ThuPhiGoi`
- **Lược đồ Di chuyển (Schema Path):** `dbo.ThuPhiGoi` (custom extract) -> `stg_nano_v2.ThuPhiGoi` -> ghi gộp vào `dm.FactThuPhiDichVu` với `LoaiHinh='TPG'`.
- **Cơ chế Đồng bộ (Sync Mode):** Incremental theo `NgayThu`, dùng truy vấn đặc thù.
- **Quy tắc Khóa (Key Mapping):** Khóa theo `MaPhieuThu + MaHoSo`; map `MaPhieuThu -> MaPhieuDichVu`, `MaLoaiGoi -> MaChiTieu`, `MaChiTieuBK = NguonDuLieuKey:MaLoaiGoi`; Enrichment Keys inject trước MERGE.
- **File T-SQL MERGE:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\src\db\templates\sql\fact\FactThuPhiDichVu_ThuPhiGoi_merge.sql`.
- **Ràng buộc Toàn vẹn (Constraints/Anomalies):** `custom_extract_query` bắt buộc: `SELECT * FROM dbo.ThuPhiGoi WHERE NgayThu IS NOT NULL AND MaPhieuThu IS NOT NULL`; dữ liệu vào fact tổng hợp phải gắn cờ phân loại `LoaiHinh='TPG'`.
- **Tên file và đường dẫn lưu file:** `D:\projects\vietnga\database\etl_nano\etl_nano_project_v2\docs\FINAL_SYSTEM_SPECIFICATION_V2.md`.

---

## 4) RÀNG BUỘC TOÀN HỆ THỐNG ÁP DỤNG CHUNG CHO 8 BẢNG
- Giao dịch phải quản lý ở Python-level (`autocommit=False`, `commit/rollback` toàn cục), không nhúng transaction block cứng trong từng SQL template triển khai runtime.
- Trước khi execute SQL text, phải prepend `SET NOCOUNT ON;` để tránh kẹt kết nối pyodbc do result set trung gian.
- Không sửa cấu trúc vật lý Datamart/Staging trong tài liệu vận hành này; các yêu cầu mở rộng cột phải đi theo migration có kiểm soát.
- Lớp UI/BI giữ cơ chế Flat Fact View với cờ `1/0` (ví dụ `IsLuotKham`, `IsNhuocThi`) để tối ưu phép tổng hợp `SUM`/`COUNT DISTINCT`.
