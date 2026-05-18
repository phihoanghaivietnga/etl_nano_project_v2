# MASTER_ETL_PROCESS.md

## NHÓM: ETL_PROCESS

## MỤC LỤC NGUỒN
  [DESCRIPTION]: ETL job scripts and SQL templates

### src/db/templates/sql/dashboard_doichieu/dim_benh/datamart.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_benh/production.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_benh/staging.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_benh_nhan/datamart.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_benh_nhan/production.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_benh_nhan/staging.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_dich_vu/datamart.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_dich_vu/production.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_dich_vu/staging.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_loai_goi_dich_vu/datamart.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_loai_goi_dich_vu/production.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_loai_goi_dich_vu/staging.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_luot_kham/datamart.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_luot_kham/production.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/dim_luot_kham/staging.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/datamart.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/production.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/staging.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dashboard_doichieu/ho_so_kham_benh_ngoai_tru_doi_chieu.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dimension/DimBenhNhan_merge.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dimension/DimBenh_merge.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dimension/DimLoaiGoiDichVu_merge.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/dimension/dim_dich_vu_merge.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/fact/DimLuotKham_merge.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/fact/FactDoThiLuc_merge.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/fact/FactThuPhiDichVu_ThuPhiGoi_merge.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/db/templates/sql/fact/merge_fact_thuphichvu_3in1.sql - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/jobs/__init__.py - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/jobs/dimension_loader.py - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/jobs/fact_loader.py - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ
### src/jobs/sync_orchestrator.py - Tác vụ ETL và logic xử lý dữ liệu theo bảng/miền nghiệp vụ

## NỘI DUNG GỘP

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_benh/datamart.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM dm.DimBenh WITH (NOLOCK)
WHERE NguonDuLieuKey = 2;
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_benh/production.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM dbo.DMBenh WITH (NOLOCK);
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_benh/staging.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM {staging_schema}.DMBenh WITH (NOLOCK);
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_benh_nhan/datamart.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM dm.DimBenhNhan WITH (NOLOCK)
WHERE NguonDuLieuKey = 2;
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_benh_nhan/production.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM dbo.DMBenhNhan WITH (NOLOCK);
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_benh_nhan/staging.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM {staging_schema}.DMBenhNhan WITH (NOLOCK);
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_dich_vu/datamart.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM dm.DimDichVu WITH (NOLOCK)
WHERE NguonDuLieuKey = 2;
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_dich_vu/production.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM dbo.DMDichVuChiTiet WITH (NOLOCK);
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_dich_vu/staging.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM {staging_schema}.DMDichVuChiTiet WITH (NOLOCK);
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_loai_goi_dich_vu/datamart.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount] 
FROM dm.DimLoaiGoiDichVu WITH (NOLOCK)
WHERE NguonDuLieuKey = 2;
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_loai_goi_dich_vu/production.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM dbo.LoaiGoiDichVuNT WITH (NOLOCK);
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_loai_goi_dich_vu/staging.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM {staging_schema}.LoaiGoiDichVuNT WITH (NOLOCK);
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_luot_kham/datamart.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT
    COUNT(1) AS [RowCount]
FROM dm.DimLuotKham WITH (NOLOCK)
WHERE NgayVaoKham >= @TuNgay AND NgayVaoKham < DATEADD(DAY, 1, @DenNgay);
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_luot_kham/production.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM dbo.HoSoKhamBenhNgoaiTru WITH (NOLOCK)
WHERE NgayVaoKham >= @TuNgay AND NgayVaoKham < DATEADD(DAY, 1, @DenNgay);
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/dim_luot_kham/staging.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT
    COUNT(1) AS [RowCount]
FROM {staging_schema}.HoSoKhamBenhNgoaiTru WITH (NOLOCK)
WHERE NgayVaoKham >= @TuNgay AND NgayVaoKham < DATEADD(DAY, 1, @DenNgay);
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/datamart.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT SUM(TongTien_DV + TongTien_BH) TongTien, SUM(TongTienSauTangGiam_DV + TongTienSauTangGiam_BH) TongTienSauTangGiam
FROM
(
	SELECT NgayDenKham, SUM(TongTien_DV) TongTien_DV, SUM(TongTienSauTangGiam_DV) TongTienSauTangGiam_DV
		, SUM(TongTien_BH) TongTien_BH, SUM(TongTienSauTangGiam_BH) TongTienSauTangGiam_BH
	FROM
	(
	select DateKey NgayDenKham, sum(TongTien) TongTien_DV, sum(TongTienSauTangGiam) TongTienSauTangGiam_DV
		, 0 TongTien_BH, 0 TongTienSauTangGiam_BH from dm.FactThuPhiDichVu 
	where CoSoKey = 1 and NguonDuLieuKey = 2 and LoaiHinh = 'DV'
		and datekey >= YEAR(@TuNgay) * 10000 + MONTH(@TuNgay) * 100 + DAY(@TuNgay) and datekey <= YEAR(@DenNgay) * 10000 + MONTH(@DenNgay) * 100 + DAY(@DenNgay)
	group by DateKey
	union
	select DateKey NgayDenKham, 0 TongTien_DV, 0 TongTienSauTangGiam_DV
		, SUM(TongTien) TongTien_BH, SUM(TongTienSauTangGiam) TongTienSauTangGiam_BH from dm.FactThuPhiDichVu 
	where CoSoKey = 1 and NguonDuLieuKey = 2 and LoaiHinh = 'BH'
		and datekey >= YEAR(@TuNgay) * 10000 + MONTH(@TuNgay) * 100 + DAY(@TuNgay) and datekey <= YEAR(@DenNgay) * 10000 + MONTH(@DenNgay) * 100 + DAY(@DenNgay)
	group by DateKey
	) as temp
	group by NgayDenKham
) as tblTemp;
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/production.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT SUM(TongTien_DV + TongTien_BH) TongTien, SUM(TongTienSauTangGiam_DV + TongTienSauTangGiam_BH) TongTienSauTangGiam
FROM
(
	SELECT NgayDenKham, SUM(TongTien_DV) TongTien_DV, SUM(TongTienSauTangGiam_DV) TongTienSauTangGiam_DV
		, SUM(TongTien_BH) TongTien_BH, SUM(TongTienSauTangGiam_BH) TongTienSauTangGiam_BH
	FROM
	(
	select cast(a.ngaydenkham as date) AS NgayDenKham, sum(a.Tongtien) TongTien_DV,  sum(a.Tongtien - ISNULL(b.sotiengiam, 0) + ISNULL(b.sotientang, 0)) TongTienSauTangGiam_DV, 0 TongTien_BH, 0 TongTienSauTangGiam_BH 
	from  ThuPhiDichVu a
		left join (SELECT
					MaHoSo,
					MaChiTieu,
					MaPhieuDichVu,
					SUM(SoTienGiam) AS SoTienGiam,
					SUM(SoTienTang) AS SoTienTang
				FROM ThuPhiTangGiam
				WHERE DaDongTien = 1
				  AND CAST(NgayDenKham AS DATE) >= @TuNgay
				  AND CAST(NgayDenKham AS DATE) <= @DenNgay
				GROUP BY MaHoSo, MaChiTieu, MaPhieuDichVu) b on a.MaHoSo = b.MaHoSo and a.MaChiTieu = b.MaChiTieu and a.MaPhieuDichVu = b.MaPhieuDichVu
	where a.NgayDenKham >= @TuNgay and a.ngaydenkham < DATEADD(DAY, 1, @DenNgay)
		and a.DaDongTien = 1
	group by cast(a.ngaydenkham as date)
	UNION
	select cast(ngaydenkham as date) AS NgayDenKham, 0 TongTien_DV, 0 TongTienSauTangGiam_DV, sum(a.TongTien) TongTien_BH, sum(a.TongTien + a.TienChenhLech) TongTienSauTangGiam_BH
	from ThuPhiBaoHiem a
	where a.NgayDenKham >= @TuNgay and a.ngaydenkham < DATEADD(DAY, 1, @DenNgay)
		and a.DaDongTien = 1
	group by cast(ngaydenkham as date)
	) as temp
	GROUP BY NgayDenKham
) as tbltemp
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/staging.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT SUM(TongTien_DV + TongTien_BH) TongTien, SUM(TongTienSauTangGiam_DV + TongTienSauTangGiam_BH) TongTienSauTangGiam
FROM
(
	SELECT NgayDenKham, SUM(TongTien_DV) TongTien_DV, SUM(TongTienSauTangGiam_DV) TongTienSauTangGiam_DV
		, SUM(TongTien_BH) TongTien_BH, SUM(TongTienSauTangGiam_BH) TongTienSauTangGiam_BH
	FROM
	(
	select cast(a.ngaydenkham as date) AS NgayDenKham, sum(a.Tongtien) TongTien_DV,  sum(a.Tongtien - ISNULL(b.sotiengiam, 0) + ISNULL(b.sotientang, 0)) TongTienSauTangGiam_DV, 0 TongTien_BH, 0 TongTienSauTangGiam_BH 
	from  {staging_schema}.ThuPhiDichVu a
		left join (SELECT
					MaHoSo,
					MaChiTieu,
					MaPhieuDichVu,
					SUM(SoTienGiam) AS SoTienGiam,
					SUM(SoTienTang) AS SoTienTang
				FROM {staging_schema}.ThuPhiTangGiam
				WHERE DaDongTien = 1
				  AND CAST(NgayDenKham AS DATE) >= @TuNgay
				  AND CAST(NgayDenKham AS DATE) < DATEADD(DAY, 1, @DenNgay)
				GROUP BY MaHoSo, MaChiTieu, MaPhieuDichVu) b on a.MaHoSo = b.MaHoSo and a.MaChiTieu = b.MaChiTieu and a.MaPhieuDichVu = b.MaPhieuDichVu
	where a.NgayDenKham >= @TuNgay and a.ngaydenkham < DATEADD(DAY, 1, @DenNgay)
		and a.DaDongTien = 1
	group by cast(a.ngaydenkham as date)
	UNION
	select cast(ngaydenkham as date) AS NgayDenKham, 0 TongTien_DV, 0 TongTienSauTangGiam_DV, sum(a.TongTien) TongTien_BH, sum(a.TongTien + a.TienChenhLech) TongTienSauTangGiam_BH
	from {staging_schema}.ThuPhiBaoHiem a
	where a.NgayDenKham >= @TuNgay and a.ngaydenkham < DATEADD(DAY, 1, @DenNgay)
		and a.DaDongTien = 1
	group by cast(ngaydenkham as date)
	) as temp
	GROUP BY NgayDenKham
) as tbltemp
```

### SOURCE: src/db/templates/sql/dashboard_doichieu/ho_so_kham_benh_ngoai_tru_doi_chieu.sql
```sql
SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

WITH ProdHoSo AS (
    SELECT
        COUNT(1) AS RowCount,
        SUM(CAST(ISNULL(MaBenhNhan, '') <> '' AS INT)) AS SumLuotKhamHopLe
    FROM dbo.HoSoKhamBenhNgoaiTru WITH (NOLOCK)
    WHERE CAST(NgayVaoKham AS DATE) BETWEEN @TuNgay AND @DenNgay
),
StgHoSo AS (
    SELECT
        COUNT(1) AS RowCount,
        SUM(CAST(ISNULL(MaBenhNhan, '') <> '' AS INT)) AS SumLuotKhamHopLe
    FROM hanoi_hisnano_v2.HoSoKhamBenhNgoaiTru WITH (NOLOCK)
    WHERE CAST(NgayVaoKham AS DATE) BETWEEN @TuNgay AND @DenNgay
),
DmHoSo AS (
    SELECT
        COUNT(1) AS RowCount,
        SUM(CAST(ISNULL(MaBenhNhan, '') <> '' AS INT)) AS SumLuotKhamHopLe
    FROM dm.DimLuotKham WITH (NOLOCK)
    WHERE CAST(NgayVaoKham AS DATE) BETWEEN @TuNgay AND @DenNgay
),
ProdRevenue AS (
    SELECT
        SUM(ISNULL(TongTienSauTangGiam, TongTien)) AS SumDoanhThu
    FROM dbo.ThuPhiDichVu WITH (NOLOCK)
    WHERE CAST(NgayDenKham AS DATE) BETWEEN @TuNgay AND @DenNgay
),
StgRevenue AS (
    SELECT
        SUM(ISNULL(TongTienSauTangGiam, TongTien)) AS SumDoanhThu
    FROM hanoi_hisnano_v2.ThuPhiDichVu WITH (NOLOCK)
    WHERE CAST(NgayDenKham AS DATE) BETWEEN @TuNgay AND @DenNgay
),
DmRevenue AS (
    SELECT
        SUM(ISNULL(TongTienSauTangGiam, TongTien)) AS SumDoanhThu
    FROM dm.FactThuPhiDichVu WITH (NOLOCK)
    WHERE CAST(NgayDenKham AS DATE) BETWEEN @TuNgay AND @DenNgay
)
SELECT
    N'HoSoKhamBenhNgoaiTru' AS TenBang,
    p.RowCount AS RowCount_Production,
    s.RowCount AS RowCount_Staging,
    d.RowCount AS RowCount_DataMart,
    p.SumLuotKhamHopLe AS Sum_Production,
    s.SumLuotKhamHopLe AS Sum_Staging,
    d.SumLuotKhamHopLe AS Sum_DataMart
FROM ProdHoSo p
CROSS JOIN StgHoSo s
CROSS JOIN DmHoSo d

UNION ALL

SELECT
    N'FactThuPhiDichVu' AS TenBang,
    NULL AS RowCount_Production,
    NULL AS RowCount_Staging,
    NULL AS RowCount_DataMart,
    p.SumDoanhThu AS Sum_Production,
    s.SumDoanhThu AS Sum_Staging,
    d.SumDoanhThu AS Sum_DataMart
FROM ProdRevenue p
CROSS JOIN StgRevenue s
CROSS JOIN DmRevenue d;
```

### SOURCE: src/db/templates/sql/dimension/DimBenhNhan_merge.sql
```sql
--
-- FILE: DimBenhNhan_merge.sql
-- AUTHOR: GitHub Copilot
-- CREATED: 2026-03-14
-- MODIFIED: 2026-03-14
-- VERSION: 1.0.0
-- PURPOSE: Template MERGE DimBenhNhan tu staging sang dm voi enrichment.
-- HISTORY:
--     - v1.0.0 [2026-03-14]: Tao moi template tu bulk_loader va schema cu
--

DECLARE @NguonDuLieuKey INT = {nguon_dulieu_key};
DECLARE @MaCoSo        VARCHAR(50) = '{ma_co_so}';
DECLARE @CoSoKey       INT = {co_so_key};

;WITH Src AS (
    SELECT
        @NguonDuLieuKey AS NguonDuLieuKey,
        @MaCoSo         AS MaCoSo,
        CAST(bn.MaBenhNhan AS VARCHAR(50)) AS MaBenhNhan,
        bn.TenBenhNhan         AS HoTenRaw,
        bn.DiaChiBenhNhan      AS DiaChiRaw,
        bn.NgayThang + '/' + CAST(bn.NamSinh AS VARCHAR) AS NgaySinhRaw,
        bn.NamSinh             AS NamSinhRaw,
        REPLACE(bn.SoDienThoai, '***',dbo.Decode_Hex(bn.SoDienThoaiEnabled)) As SoDienThoaiRaw,
        -- bn.SoDienThoai         AS SoDienThoaiRaw,
        bn.MaTinhThanh         AS MaTinhThanhRaw,
        dmTinh.TenTinhThanh    AS TinhThanhRaw,
        bn.MaXa                AS MaXaPhuongRaw,
        dmPhuong.TenXa         AS XaPhuongRaw,
        CASE
            WHEN LTRIM(RTRIM(bn.MaGioiTinh)) = '0' THEN 'NAM'
            WHEN LTRIM(RTRIM(bn.MaGioiTinh)) = '1' THEN 'NU'
            ELSE 'KXD'
        END AS MaGioiTinhChuan,
        bn.sysdate AS SysDateNguon,
        CAST(COALESCE(
            TRY_CONVERT(DATE, (bn.NgayThang + '/' + CAST(bn.NamSinh AS VARCHAR)), 103),
            TRY_CONVERT(DATE, (bn.NgayThang + '/' + CAST(bn.NamSinh AS VARCHAR)), 120)
        ) AS DATE) AS NgaySinhChuan,
        bn.NamSinh AS NamSinhChuan
    FROM [{staging_schema}].[DMBenhNhan] bn WITH (NOLOCK)
    LEFT JOIN [{staging_schema}].[DMTinhThanh] dmTinh
        ON bn.MaTinhThanh = dmTinh.MaTinhThanh
    LEFT JOIN [{staging_schema}].[DMXaPhuong] dmPhuong
        ON bn.MaXa = dmPhuong.MaXa
),
Enriched AS (
    SELECT
        s.*,        
        COALESCE(dcs.CoSoKey, @CoSoKey) AS CoSoKey,
        dc_tinh.MaChuan  AS MaTinhThanhChuan,
        dc_tinh.TenChuan AS TinhThanhChuan,
        NULL             AS MaPhuongChuan,
        NULL             AS PhuongChuan,
        gt.GioiTinhKey,
        gt.MaGioiTinh    AS MaGioiTinhRef,
        gt.TenGioiTinh,
        C.SoDienThoaiChuan20 AS SoDienThoaiChuan,
        C.DQ_SDT_QuaDai
    FROM Src s
    LEFT JOIN [{dm_schema}].[DimCoSo] dcs
        ON dcs.MaCoSo = s.MaCoSo
    LEFT JOIN [ref].[MapDiaLy] m_tinh
        ON  m_tinh.NguonDuLieuKey = s.NguonDuLieuKey
        AND m_tinh.CoSoKey = COALESCE(dcs.CoSoKey, @CoSoKey)
        AND m_tinh.Cap     = 'TINH'
        AND m_tinh.MaNguon = s.MaTinhThanhRaw
    LEFT JOIN [ref].[DiaLyChuan] dc_tinh
        ON dc_tinh.DiaLyChuanKey = m_tinh.DiaLyChuanKey
    LEFT JOIN [ref].[GioiTinh] gt
        ON gt.MaGioiTinh = s.MaGioiTinhChuan
    CROSS APPLY (
        SELECT REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
            LTRIM(RTRIM(ISNULL(s.SoDienThoaiRaw, N''))),
            '/',''),'-',''),' ',''),'.',''),'+','') AS sdt0
    ) A
    CROSS APPLY (
        SELECT CASE
            WHEN LEFT(A.sdt0, 2) = '84' THEN '0' + SUBSTRING(A.sdt0, 3, 200)
            ELSE A.sdt0
        END AS sdt1
    ) B
    CROSS APPLY (
        SELECT
            CASE WHEN LEN(B.sdt1) > 20 THEN 1 ELSE 0 END AS DQ_SDT_QuaDai,
            LEFT(B.sdt1, 20) AS SoDienThoaiChuan20
    ) C
)
MERGE [{dm_schema}].[DimBenhNhan] AS tgt
USING (
    SELECT
        e.NguonDuLieuKey,
        e.CoSoKey,
        e.MaCoSo,
        e.MaBenhNhan,
        CAST(e.NguonDuLieuKey AS VARCHAR(10)) + ':' + CAST(e.MaBenhNhan AS VARCHAR(50)) AS MaBenhNhanBK,
        e.HoTenRaw,
        e.DiaChiRaw,
        e.NgaySinhRaw,
        e.NamSinhRaw,
        e.SoDienThoaiRaw,
        e.MaTinhThanhRaw,
        e.TinhThanhRaw,
        e.MaXaPhuongRaw AS MaXaPhuongRaw,
        e.XaPhuongRaw   AS PhuongRaw,
        e.HoTenRaw      AS HoTenChuan,
        e.DiaChiRaw     AS DiaChiChuan,
        e.NgaySinhChuan,
        e.NamSinhChuan,
        e.MaTinhThanhChuan,
        e.TinhThanhChuan,
        e.MaPhuongChuan,
        e.PhuongChuan,
        e.SoDienThoaiChuan,
        e.GioiTinhKey,
        e.MaGioiTinhRef AS MaGioiTinhChuan,
        e.SysDateNguon,
        CASE WHEN NULLIF(LTRIM(RTRIM(e.HoTenRaw)), '') IS NULL THEN 0 ELSE 1 END
            AS DQ_HoTenHopLe,
        CASE WHEN NULLIF(LTRIM(RTRIM(e.DiaChiRaw)), '') IS NULL THEN 0 ELSE 1 END
            AS DQ_DiaChiHopLe,
        CASE WHEN e.NgaySinhChuan IS NULL AND e.NamSinhChuan IS NULL THEN 0 ELSE 1 END
            AS DQ_NgaySinhHopLe,
        CASE WHEN e.TinhThanhChuan IS NULL THEN 0 ELSE 1 END
            AS DQ_TinhThanhHopLe,
        CASE WHEN e.PhuongChuan IS NULL THEN 0 ELSE 1 END
            AS DQ_PhuongHopLe,
        CASE
            WHEN e.SoDienThoaiChuan IS NULL OR e.SoDienThoaiChuan = '' THEN 0
            WHEN e.SoDienThoaiChuan LIKE '%[^0-9]%'                    THEN 0
            WHEN LEN(e.SoDienThoaiChuan) < 9                           THEN 0
            WHEN e.DQ_SDT_QuaDai = 1                                   THEN 0
            ELSE 1
        END AS DQ_SoDienThoaiHopLe,
        CASE
            WHEN e.DQ_SDT_QuaDai = 1
                THEN N'SDT > 20 ky tu: da cat 20 ky tu de luu, can kiem tra'
            WHEN e.TinhThanhChuan IS NULL OR e.PhuongChuan IS NULL
                THEN N'Chua map du dia ly (TINH/XA) qua ref.MapDiaLy'
            WHEN e.GioiTinhKey IS NULL
                THEN N'Chua map duoc gioi tinh ve ref.GioiTinh (NAM/NU/KXD)'
            ELSE NULL
        END AS DQ_GhiChu
    FROM Enriched e
) AS src
ON tgt.MaBenhNhanBK = src.MaBenhNhanBK
WHEN MATCHED THEN
    UPDATE SET
        tgt.NguonDuLieuKey      = src.NguonDuLieuKey,
        tgt.CoSoKey             = src.CoSoKey,
        tgt.MaCoSo              = src.MaCoSo,
        tgt.HoTenRaw            = src.HoTenRaw,
        tgt.DiaChiRaw           = src.DiaChiRaw,
        tgt.NgaySinhRaw         = src.NgaySinhRaw,
        tgt.NamSinhRaw          = src.NamSinhRaw,
        tgt.SoDienThoaiRaw      = src.SoDienThoaiRaw,
        tgt.MaTinhThanhRaw      = src.MaTinhThanhRaw,
        tgt.TinhThanhRaw        = src.TinhThanhRaw,
        tgt.MaPhuongRaw         = src.MaXaPhuongRaw,
        tgt.PhuongRaw           = src.PhuongRaw,
        tgt.HoTenChuan          = src.HoTenChuan,
        tgt.DiaChiChuan         = src.DiaChiChuan,
        tgt.NgaySinhChuan       = src.NgaySinhChuan,
        tgt.NamSinhChuan        = src.NamSinhChuan,
        tgt.MaTinhThanhChuan    = src.MaTinhThanhChuan,
        tgt.TinhThanhChuan      = src.TinhThanhChuan,
        tgt.MaPhuongChuan       = src.MaPhuongChuan,
        tgt.PhuongChuan         = src.PhuongChuan,
        tgt.SoDienThoaiChuan    = src.SoDienThoaiChuan,
        tgt.GioiTinhKey         = src.GioiTinhKey,
        tgt.MaGioiTinhChuan     = src.MaGioiTinhChuan,
        tgt.DQ_HoTenHopLe       = src.DQ_HoTenHopLe,
        tgt.DQ_DiaChiHopLe      = src.DQ_DiaChiHopLe,
        tgt.DQ_NgaySinhHopLe    = src.DQ_NgaySinhHopLe,
        tgt.DQ_TinhThanhHopLe   = src.DQ_TinhThanhHopLe,
        tgt.DQ_PhuongHopLe      = src.DQ_PhuongHopLe,
        tgt.DQ_SoDienThoaiHopLe = src.DQ_SoDienThoaiHopLe,
        tgt.DQ_GhiChu           = src.DQ_GhiChu,
        tgt.SysDateNguon        = src.SysDateNguon,
        tgt.NgayCapNhat         = GETDATE()
WHEN NOT MATCHED THEN
    INSERT (
        NguonDuLieuKey, CoSoKey, MaCoSo,
        MaBenhNhan, MaBenhNhanBK,
        HoTenRaw, DiaChiRaw, NgaySinhRaw, NamSinhRaw,
        MaTinhThanhRaw, TinhThanhRaw, MaPhuongRaw, PhuongRaw, SoDienThoaiRaw,
        HoTenChuan, DiaChiChuan, NgaySinhChuan, NamSinhChuan,
        MaTinhThanhChuan, TinhThanhChuan, MaPhuongChuan, PhuongChuan, SoDienThoaiChuan,
        GioiTinhKey, MaGioiTinhChuan,
        DQ_HoTenHopLe, DQ_DiaChiHopLe, DQ_NgaySinhHopLe, DQ_TinhThanhHopLe,
        DQ_PhuongHopLe, DQ_SoDienThoaiHopLe, DQ_GhiChu,
        SysDateNguon
    )
    VALUES (
        src.NguonDuLieuKey, src.CoSoKey, src.MaCoSo,
        src.MaBenhNhan, src.MaBenhNhanBK,
        src.HoTenRaw, src.DiaChiRaw, src.NgaySinhRaw, src.NamSinhRaw,
        src.MaTinhThanhRaw, src.TinhThanhRaw, src.MaXaPhuongRaw, src.PhuongRaw, src.SoDienThoaiRaw,
        src.HoTenChuan, src.DiaChiChuan, src.NgaySinhChuan, src.NamSinhChuan,
        src.MaTinhThanhChuan, src.TinhThanhChuan, src.MaPhuongChuan, src.PhuongChuan, src.SoDienThoaiChuan,
        src.GioiTinhKey, src.MaGioiTinhChuan,
        src.DQ_HoTenHopLe, src.DQ_DiaChiHopLe, src.DQ_NgaySinhHopLe, src.DQ_TinhThanhHopLe,
        src.DQ_PhuongHopLe, src.DQ_SoDienThoaiHopLe, src.DQ_GhiChu,
        src.SysDateNguon
    );
```

### SOURCE: src/db/templates/sql/dimension/DimBenh_merge.sql
```sql
-- =============================================================================
-- FILE: DimBenh_merge.sql
-- SOURCE: src/auto_runner/loader.py::_merge_dimbenh_direct
-- PURPOSE: MERGE [{staging_schema}].[DMBenh] -> [{dm_schema}].[DimBenh]
-- NOTE:
--   - Script da duoc chuyen truc tiep tu logic MERGE trong Auto Loader.
--   - BK su dung separator ':' theo logic hien tai.
-- =============================================================================

MERGE INTO [{dm_schema}].[DimBenh] AS target
USING (
    SELECT
        b.NguonDuLieuKey,
        b.CoSoKey,
        b.MaCoSo,
        b.MaBenh,
        b.TenBenhTiengViet,
        b.TenBenhTiengAnh,
        b.GhiChu,
        b.MaNhomBenh
    FROM [{staging_schema}].[DMBenh] b WITH (NOLOCK)
) src
ON target.MaBenhBK = CAST(src.NguonDuLieuKey AS VARCHAR(10)) + ':' + src.MaBenh
WHEN MATCHED THEN
    UPDATE SET
        target.NguonDuLieuKey    = src.NguonDuLieuKey,
        target.CoSoKey           = src.CoSoKey,
        target.MaCoSo            = src.MaCoSo,
        target.TenBenhTiengViet  = src.TenBenhTiengViet,
        target.TenBenhTiengAnh   = src.TenBenhTiengAnh,
        target.GhiChu            = src.GhiChu,
        target.MaNhomBenh        = src.MaNhomBenh,
        target.NgayCapNhat       = GETDATE()
WHEN NOT MATCHED THEN
    INSERT (
        NguonDuLieuKey, CoSoKey, MaCoSo,
        MaBenh,
        TenBenhTiengViet, TenBenhTiengAnh,
        GhiChu, MaNhomBenh,
        NgayTao
    )
    VALUES (
        src.NguonDuLieuKey, src.CoSoKey, src.MaCoSo,
        src.MaBenh,
        src.TenBenhTiengViet, src.TenBenhTiengAnh,
        src.GhiChu, src.MaNhomBenh,
        GETDATE()
    );
```

### SOURCE: src/db/templates/sql/dimension/DimLoaiGoiDichVu_merge.sql
```sql
--
-- FILE: DimLoaiGoiDichVu_merge.sql
-- AUTHOR: Claude Sonnet 4.6 (Builder)
-- CREATED: 2026-04-17
-- MODIFIED: 2026-04-17
-- VERSION: 1.1.0
-- PURPOSE: Template MERGE DimLoaiGoiDichVu tu staging sang dm.
-- HISTORY:
--     - v1.0.0 [2026-04-17]: Tao moi — dong bo LoaiGoiDichVuNT
--     - v1.1.0 [2026-04-17]: Fix mapping — them MaLoaiGoi (goc),
--                             CONCAT cho MaLoaiGoiBK, them MaCoSo vao INSERT/UPDATE
--                             (chi thi 20260417_1750)
--


MERGE [{dm_schema}].[DimLoaiGoiDichVu] AS Target
USING (
    SELECT
        {co_so_key}        AS CoSoKey,
        {nguon_dulieu_key} AS NguonDuLieuKey,
        '{ma_co_so}'       AS MaCoSo,
        s.MaLoaiGoi        AS MaLoaiGoi,
        -- Khoi tao MaLoaiGoiBK theo dinh dang NguonDuLieuKey:MaLoaiGoi
        CONCAT(CAST({nguon_dulieu_key} AS VARCHAR), ':', s.MaLoaiGoi) AS MaLoaiGoiBK,
        s.TenLoaiGoi
    FROM [{staging_schema}].[LoaiGoiDichVuNT] s WITH (NOLOCK)
) AS Source
ON Target.NguonDuLieuKey = Source.NguonDuLieuKey
   AND Target.MaLoaiGoiBK = Source.MaLoaiGoiBK
WHEN MATCHED THEN
    UPDATE SET
        Target.TenLoaiGoi = Source.TenLoaiGoi,
        Target.MaCoSo = Source.MaCoSo,
        Target.NgayDongBo = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    INSERT (MaLoaiGoi, CoSoKey, NguonDuLieuKey, MaCoSo, MaLoaiGoiBK, TenLoaiGoi, NgayDongBo)
    VALUES (Source.MaLoaiGoi, Source.CoSoKey, Source.NguonDuLieuKey, Source.MaCoSo, Source.MaLoaiGoiBK, Source.TenLoaiGoi, GETDATE());
```

### SOURCE: src/db/templates/sql/dimension/dim_dich_vu_merge.sql
```sql
-- =============================================================================
-- FILE: dim_dich_vu_merge.sql
-- SOURCE: src/auto_runner/loader.py::_merge_dimdichvu_3in1
-- PURPOSE: MERGE 3-in-1 DMLoaiDichVu + DMDichVu + DMDichVuChiTiet -> dm.DimDichVu
-- NOTE:
--   - Thay cac gia tri bien o dau script cho phu hop facility truoc khi chay.
--   - BK su dung separator ':' theo logic hien tai.
-- =============================================================================

DECLARE @NguonDuLieuKey INT = {nguon_dulieu_key};
DECLARE @MaCoSo VARCHAR(50) = '{ma_co_so}';
DECLARE @CoSoKey INT = {co_so_key};

MERGE [{dm_schema}].[DimDichVu] AS tgt
USING (
    SELECT
        @NguonDuLieuKey             AS NguonDuLieuKey,
        @CoSoKey                    AS CoSoKey,
        @MaCoSo                     AS MaCoSo,
        ct.MaChiTieu,
        CAST(@NguonDuLieuKey AS VARCHAR(10)) + ':' + ct.MaChiTieu AS BK_Src,
        ct.TenChiTieu,
        dv.MaDichVu,
        dv.TenDichVu,
        ldv.MaLoaiDichVu,
        ldv.TenLoaiDichVu,
        ct.MaNhomDMDichVuChiTiet,
        ct.MaDichVuBaoCao,
        CAST(ct.TrangThaiSuDung  AS INT) AS TrangThaiSuDung,
        CAST(ct.TrangThaiHienThi AS INT) AS TrangThaiHienThi,
        CAST(ct.GDNgoaiBH        AS INT) AS GDNgoaiBH,
        CAST(ct.BHKhongThanhToan AS INT) AS BHKhongThanhToan,
        CASE
            WHEN ct.MaChiTieu IS NOT NULL
                 AND ct.TenChiTieu IS NOT NULL
                 AND ct.TenChiTieu <> ''
            THEN CAST(1 AS BIT)
            ELSE CAST(0 AS BIT)
        END AS DQ_HopLe,
        NULL AS DQ_GhiChu
    FROM [{staging_schema}].[DMDichVuChiTiet] ct WITH (NOLOCK)
    LEFT JOIN [{staging_schema}].[DMDichVu] dv
        ON ct.MaDichVu = dv.MaDichVu
    LEFT JOIN [{staging_schema}].[DMLoaiDichVu] ldv
        ON dv.MaLoaiDichVu = ldv.MaLoaiDichVu
) AS src ON tgt.NguonDuLieuKey = src.NguonDuLieuKey
        AND tgt.MaCoSo = src.MaCoSo
        AND tgt.MaChiTieu = src.MaChiTieu
WHEN MATCHED THEN UPDATE SET
    tgt.NguonDuLieuKey          = src.NguonDuLieuKey,
    tgt.CoSoKey                 = src.CoSoKey,
    tgt.MaCoSo                  = src.MaCoSo,
    tgt.TenChiTieu              = src.TenChiTieu,
    tgt.MaDichVu                = src.MaDichVu,
    tgt.TenDichVu               = src.TenDichVu,
    tgt.MaLoaiDichVu            = src.MaLoaiDichVu,
    tgt.TenLoaiDichVu           = src.TenLoaiDichVu,
    tgt.MaNhomDMDichVuChiTiet   = src.MaNhomDMDichVuChiTiet,
    tgt.MaDichVuBaoCao          = src.MaDichVuBaoCao,
    tgt.TrangThaiSuDung         = src.TrangThaiSuDung,
    tgt.TrangThaiHienThi        = src.TrangThaiHienThi,
    tgt.GDNgoaiBH               = src.GDNgoaiBH,
    tgt.BHKhongThanhToan        = src.BHKhongThanhToan,
    tgt.DQ_HopLe                = src.DQ_HopLe,
    tgt.DQ_GhiChu               = src.DQ_GhiChu,
    tgt.NgayCapNhat             = GETDATE()
WHEN NOT MATCHED THEN INSERT (
    NguonDuLieuKey, CoSoKey, MaCoSo,
    MaChiTieu, TenChiTieu,
    MaDichVu, TenDichVu,
    MaLoaiDichVu, TenLoaiDichVu,
    MaNhomDMDichVuChiTiet, MaDichVuBaoCao,
    TrangThaiSuDung, TrangThaiHienThi, GDNgoaiBH, BHKhongThanhToan,
    DQ_HopLe, DQ_GhiChu,
    NgayTao
) VALUES (
    src.NguonDuLieuKey, src.CoSoKey, src.MaCoSo,
    src.MaChiTieu, src.TenChiTieu,
    src.MaDichVu, src.TenDichVu,
    src.MaLoaiDichVu, src.TenLoaiDichVu,
    src.MaNhomDMDichVuChiTiet, src.MaDichVuBaoCao,
    src.TrangThaiSuDung, src.TrangThaiHienThi, src.GDNgoaiBH, src.BHKhongThanhToan,
    src.DQ_HopLe, src.DQ_GhiChu,
    GETDATE()
);
```

### SOURCE: src/db/templates/sql/fact/DimLuotKham_merge.sql
```sql
--
-- FILE: DimLuotKham_merge.sql
-- AUTHOR: GitHub Copilot
-- CREATED: 2026-03-14
-- MODIFIED: 2026-03-14
-- VERSION: 1.0.2
-- PURPOSE: Template MERGE DimLuotKham truc tiep tu HoSoKhamBenhNgoaiTru.
-- HISTORY:
--     - v1.0.0 [2026-03-14]: Tao moi template MERGE theo logic toi uu
--     - v1.0.1 [2026-03-14]: Map cot ThoiGianVaoKham va DaDongTien theo nguon thuc te
--     - v1.0.2 [2026-03-14]: Fallback NguonDuLieuKey, CoSoKey, MaCoSo neu nguon NULL
--

MERGE [{dm_schema}].[DimLuotKham] AS target
USING (
    SELECT
        COALESCE(s.NguonDuLieuKey, {nguon_dulieu_key}) AS NguonDuLieuKey,
        COALESCE(s.CoSoKey, {co_so_key}) AS CoSoKey,
        COALESCE(s.MaCoSo, '{ma_co_so}') AS MaCoSo,
        s.MaHoSo,
        CONCAT(COALESCE(s.NguonDuLieuKey, {nguon_dulieu_key}), ':', s.MaHoSo) AS MaHoSoBK,
        s.MaBenhNhan,
        bnh.MaBenhNhanBK,
        s.NgayVaoKham,
        CASE WHEN s.NgayVaoKham IS NULL THEN NULL
             ELSE (YEAR(CAST(s.NgayVaoKham AS DATE)) * 10000
                 + MONTH(CAST(s.NgayVaoKham AS DATE)) * 100
                 + DAY(CAST(s.NgayVaoKham AS DATE))) END AS NgayVaoKhamDateKey,
        s.NgayVaoKhamDP AS ThoiGianVaoKham,
        s.TrangThaiPhieu,
        NULL AS DaDongTien,
        s.TrangThaiThanhToan,
        s.NgayThanhToan,
        bnh.BenhNhanKey,
        CASE
            WHEN s.MaHoSo IS NULL OR LTRIM(RTRIM(s.MaHoSo)) = '' THEN 0
            WHEN s.MaBenhNhan IS NULL OR LTRIM(RTRIM(s.MaBenhNhan)) = '' THEN 0
            WHEN s.NgayVaoKham IS NULL THEN 0
            ELSE 1
        END AS DQ_HopLe,
        CASE
            WHEN s.MaHoSo IS NULL OR LTRIM(RTRIM(s.MaHoSo)) = '' THEN N'Thieu MaHoSo'
            WHEN s.MaBenhNhan IS NULL OR LTRIM(RTRIM(s.MaBenhNhan)) = '' THEN N'Thieu MaBenhNhan'
            WHEN s.NgayVaoKham IS NULL THEN N'Thieu NgayVaoKham'
            WHEN bnh.BenhNhanKey IS NULL THEN N'Khong map duoc sang dm.DimBenhNhan'
            ELSE NULL
        END AS DQ_GhiChu
    FROM [{source_schema}].[HoSoKhamBenhNgoaiTru] s
    LEFT JOIN [{dm_schema}].[DimBenhNhan] bnh
        ON bnh.MaBenhNhanBK = CONCAT(COALESCE(s.NguonDuLieuKey, {nguon_dulieu_key}), ':', s.MaBenhNhan)
) src
ON target.MaHoSoBK = src.MaHoSoBK
WHEN MATCHED THEN
    UPDATE SET
        NguonDuLieuKey = src.NguonDuLieuKey,
        CoSoKey = src.CoSoKey,
        MaCoSo = src.MaCoSo,
        MaHoSo = src.MaHoSo,
        MaBenhNhan = src.MaBenhNhan,
        MaBenhNhanBK = src.MaBenhNhanBK,
        BenhNhanKey = src.BenhNhanKey,
        NgayVaoKham = src.NgayVaoKham,
        NgayVaoKhamDateKey = src.NgayVaoKhamDateKey,
        ThoiGianVaoKham = src.ThoiGianVaoKham,
        TrangThaiPhieu = src.TrangThaiPhieu,
        DaDongTien = src.DaDongTien,
        TrangThaiThanhToan = src.TrangThaiThanhToan,
        NgayThanhToan = src.NgayThanhToan,
        DQ_HopLe = src.DQ_HopLe,
        DQ_GhiChu = src.DQ_GhiChu,
        NgayCapNhat = GETDATE()
WHEN NOT MATCHED THEN
    INSERT (
        NguonDuLieuKey, CoSoKey, MaCoSo, MaHoSo, MaHoSoBK,
        MaBenhNhan, MaBenhNhanBK, BenhNhanKey,
        NgayVaoKham, NgayVaoKhamDateKey, ThoiGianVaoKham,
        TrangThaiPhieu, DaDongTien, TrangThaiThanhToan, NgayThanhToan,
        DQ_HopLe, DQ_GhiChu
    )
    VALUES (
        src.NguonDuLieuKey, src.CoSoKey, src.MaCoSo, src.MaHoSo, src.MaHoSoBK,
        src.MaBenhNhan, src.MaBenhNhanBK, src.BenhNhanKey,
        src.NgayVaoKham, src.NgayVaoKhamDateKey, src.ThoiGianVaoKham,
        src.TrangThaiPhieu, src.DaDongTien, src.TrangThaiThanhToan, src.NgayThanhToan,
        src.DQ_HopLe, src.DQ_GhiChu
    );
```

### SOURCE: src/db/templates/sql/fact/FactDoThiLuc_merge.sql
```sql
--
-- FILE: FactDoThiLuc_merge.sql
-- AUTHOR: Claude Sonnet 4.6 (Builder)
-- CREATED: 2026-04-17
-- MODIFIED: 2026-04-22
-- VERSION: 1.1.0
-- PURPOSE: Template MERGE FactDoThiLuc tu staging sang dm.
--          Map truc tiep enrichment keys tu staging (KHONG COALESCE).
-- HISTORY:
--     - v1.0.0 [2026-04-17]: Tao moi — dong bo DoThiLuc
--     - v1.1.0 [2026-04-22]: Fix incremental key va map enriched keys truc tiep
--

MERGE [{dm_schema}].[FactDoThiLuc] AS Target
USING (
    SELECT
        s.CoSoKey,
        s.NguonDuLieuKey,
        s.MaCoSo,
        s.MaHoSo,
        s.NgayDo
       ,[KXM_Cau_MP]
      ,[KXM_Cau_MT]
      ,[KXM_Tru_MP]
      ,[KXM_Tru_MT]
      ,[KXM_Truc_MP]
      ,[KXM_Truc_MT]
      ,[KXM_KCDT]
      ,[KC_Cau_MP]
      ,[KC_Cau_MT]
      ,[KC_Tru_MP]
      ,[KC_Tru_MT]
      ,[KC_Truc_MP]
      ,[KC_Truc_MT]
      ,[KC_CK_MP]
      ,[KC_CK_MT]
      ,[KC_Add_MP]
      ,[KC_Add_MT]
      ,[KC_KCDT]
      ,[KXHT_KK_MP]
      ,[KXHT_KK_MT]
      ,[KXHT_Cau_MP]
      ,[KXHT_Cau_MT]
      ,[KXHT_Tru_MP]
      ,[KXHT_Tru_MT]
      ,[KXHT_Truc_MP]
      ,[KXHT_Truc_MT]
      ,[KXHT_CK_MP]
      ,[KXHT_CK_MT]
      ,[KXHT_Add_MP]
      ,[KXHT_Add_MT]
      ,[KXHT_KCDT]
      ,[KXSLDT_KK_MP]
      ,[KXSLDT_KK_MT]
      ,[KXSLDT_Cau_MP]
      ,[KXSLDT_Cau_MT]
      ,[KXSLDT_Tru_MP]
      ,[KXSLDT_Tru_MT]
      ,[KXSLDT_Truc_MP]
      ,[KXSLDT_Truc_MT]
      ,[KXSLDT_CK_MP]
      ,[KXSLDT_CK_MT]
      ,[KXSLDT_Add_MP]
      ,[KXSLDT_Add_MT]
      ,[KXSLDT_KCDT]
      ,[Skiascopy_MP]
      ,[Skiascopy_MT]
      ,[NhanAp_MP]
      ,[NhanAp_MT]
      ,[BeDayGiacMac_MP]
      ,[BeDayGiacMac_MT]
      ,[DuongKinhDongTu_MP]
      ,[DuongKinhDongTu_MT]
      ,[K1_MP]
      ,[K1_MT]
      ,[K2_MP]
      ,[K2_MT]
      ,[ThiTruongVaoVien_MP]
      ,[ThiTruongVaoVien_MT]
      ,[LeDao_MP]
      ,[LeDao_MT]
      ,[MiMat_MP]
      ,[MiMat_MT]
      ,[KetMac_MP]
      ,[KetMac_MT]
      ,[TinhHinhMatHot_MP]
      ,[TinhHinhMatHot_MT]
      ,[GiacMac_MP]
      ,[GiacMac_MT]
      ,[CungMac_MP]
      ,[CungMac_MT]
      ,[TienPhong_MP]
      ,[TienPhong_MT]
      ,[MongMat_MP]
      ,[MongMat_MT]
      ,[DongTuPhanXa_MP]
      ,[DongTuPhanXa_MT]
      ,[ThuyTinhThe_MP]
      ,[ThuyTinhThe_MT]
      ,[DichKinh_MP]
      ,[DichKinh_MT]
      ,[VongMac_MP]
      ,[VongMac_MT]
      ,[GaiThi_MP]
      ,[GaiThi_MT]
      ,[HoangDiem_MP]
      ,[HoangDiem_MT]
      ,[SoiAnhDongTu_MP]
      ,[SoiAnhDongTu_MT]
      ,[TinhHinhNhanCau_MP]
      ,[TinhHinhNhanCau_MT]
      ,[HoMat_MP]
      ,[HoMat_MT]
      ,[ThiLuc_MP]
      ,[ThiLuc_MT]
      ,[ThiLucLoKinh_MP]
      ,[ThiLucLoKinh_MT]
      ,[ChieuDaiTrucNhanCau_MP]
      ,[ChieuDaiTrucNhanCau_MT]
      ,[NhinXa_KK_MP]
      ,[NhinXa_KK_MT]
      ,[NhinXa_Cau_MP]
      ,[NhinXa_Cau_MT]
      ,[NhinXa_Tru_MP]
      ,[NhinXa_Tru_MT]
      ,[NhinXa_Truc_MP]
      ,[NhinXa_Truc_MT]
      ,[NhinXa_CK_MP]
      ,[NhinXa_CK_MT]
      ,[NhinXa_Add_MP]
      ,[NhinXa_Add_MT]
      ,[NhinXa_KCDT]
      ,[NhinGan_KK_MP]
      ,[NhinGan_KK_MT]
      ,[NhinGan_Cau_MP]
      ,[NhinGan_Cau_MT]
      ,[NhinGan_Tru_MP]
      ,[NhinGan_Tru_MT]
      ,[NhinGan_Truc_MP]
      ,[NhinGan_Truc_MT]
      ,[NhinGan_CK_MP]
      ,[NhinGan_CK_MT]
      ,[NhinGan_Add_MP]
      ,[NhinGan_Add_MT]
      ,[NhinGan_KCDT]
      ,[LoiDan]
      ,[NguoiThucHien]
      ,[KC_KK_MP]
      ,[KC_KK_MT]
      ,[TrangThai]
      ,[MaPhongKham]
      ,[GhiChu]
      ,[KXHT_ChuaChinh_MP]
      ,[KXHT_ChuaChinh_MT]
      ,[KXHT_DaChinh_MT]
      ,[KXHT_DaChinh_MP]
      ,[KhoangCachDongTuXa]
      ,[KhoangCachDongTuGan]
      ,[CongNhinGan]
      ,[ThiLucCongNhinGan]
      ,[KinhApTrong]
      ,[KinhDaTrong]
      ,[KinhDoiMau]
      ,[KinhHaiTrong]
      ,[KinhNhinGan]
      ,[KinhPoly]
      ,[KinhNhinXa]
      ,[TinhTrangKinh]
      ,[ThoiGianSuDung]
      ,[SoLuong]
      ,[KXHT_KK_MP_Xa]
      ,[KXHT_KK_MT_Xa]
      ,[KXHT_Cau_MP_Xa]
      ,[KXHT_Cau_MT_Xa]
      ,[KXHT_Tru_MP_Xa]
      ,[KXHT_Tru_MT_Xa]
      ,[KXHT_Truc_MP_Xa]
      ,[KXHT_Truc_MT_Xa]
      ,[KXHT_CK_MP_Xa]
      ,[KXHT_CK_MT_Xa]
      ,[KXHT_Add_MP_Xa]
      ,[KXHT_Add_MT_Xa]
      ,[KXHT_KCDT_Xa]
      ,[KXSLDT_KK_MP_Xa]
      ,[KXSLDT_KK_MT_Xa]
      ,[KXSLDT_Cau_MP_Xa]
      ,[KXSLDT_Cau_MT_Xa]
      ,[KXSLDT_Tru_MP_Xa]
      ,[KXSLDT_Tru_MT_Xa]
      ,[KXSLDT_Truc_MP_Xa]
      ,[KXSLDT_Truc_MT_Xa]
      ,[KXSLDT_CK_MP_Xa]
      ,[KXSLDT_CK_MT_Xa]
      ,[KXSLDT_Add_MP_Xa]
      ,[KXSLDT_Add_MT_Xa]
      ,[KXSLDT_KCDT_Xa]
      ,[ThiLucLoKinh_MP_Xa]
      ,[ThiLucLoKinh_MT_Xa]
      ,[Skiascopy_SauLiet_MP]
      ,[Skiascopy_SauLiet_MT]
      ,[ThoiGianTraThuoc]
      ,[NhanAp_Maklakov_MP]
      ,[NhanAp_Maklakov_MT]
      ,[KXSLDT_ThiLucLoKinh_MP]
      ,[KXSLDT_ThiLucLoKinh_MT]
    FROM [{staging_schema}].[DoThiLuc] s WITH (NOLOCK)
	WHERE s.NgayDo >= '{date_from}' AND s.NgayDo < DATEADD(DAY, 1, '{date_to}')
) AS Source
ON Target.NgayDo = Source.NgayDo
   AND Target.MaHoSo = Source.MaHoSo
   AND Target.NguonDuLieuKey = Source.NguonDuLieuKey
WHEN MATCHED THEN
    UPDATE SET
        Target.CoSoKey = Source.CoSoKey,
        Target.NguonDuLieuKey = Source.NguonDuLieuKey,
        Target.MaCoSo = Source.MaCoSo,
        Target.KXM_Cau_MP = Source.KXM_Cau_MP ,
        Target.KXM_Cau_MT = Source.KXM_Cau_MT ,
        Target.KXM_Tru_MP = Source.KXM_Tru_MP ,
        Target.KXM_Tru_MT = Source.KXM_Tru_MT ,
        Target.KXM_Truc_MP = Source.KXM_Truc_MP ,
        Target.KXM_Truc_MT = Source.KXM_Truc_MT 
      ,Target.KXM_KCDT = Source.KXM_KCDT
      ,Target.KC_Cau_MP = Source.KC_Cau_MP
      ,Target.KC_Cau_MT = Source.KC_Cau_MT
      ,Target.KC_Tru_MP = Source.KC_Tru_MP
      ,Target.KC_Tru_MT = Source.KC_Tru_MT
      ,Target.KC_Truc_MP = Source.KC_Truc_MP
      ,Target.KC_Truc_MT = Source.KC_Truc_MT
      ,Target.KC_CK_MP = Source.KC_CK_MP
      ,Target.KC_CK_MT = Source.KC_CK_MT
      ,Target.KC_Add_MP = Source.KC_Add_MP
      ,Target.KC_Add_MT = Source.KC_Add_MT
      ,Target.KC_KCDT = Source.KC_KCDT
      ,Target.KXHT_KK_MP = Source.KXHT_KK_MP
      ,Target.KXHT_KK_MT = Source.KXHT_KK_MT
      ,Target.KXHT_Cau_MP = Source.KXHT_Cau_MP
      ,Target.KXHT_Cau_MT = Source.KXHT_Cau_MT
      ,Target.KXHT_Tru_MP = Source.KXHT_Tru_MP
      ,Target.KXHT_Tru_MT = Source.KXHT_Tru_MT
      ,Target.KXHT_Truc_MP = Source.KXHT_Truc_MP
      ,Target.KXHT_Truc_MT = Source.KXHT_Truc_MT
      ,Target.KXHT_CK_MP = Source.KXHT_CK_MP
      ,Target.KXHT_CK_MT = Source.KXHT_CK_MT
      ,Target.KXHT_Add_MP = Source.KXHT_Add_MP
      ,Target.KXHT_Add_MT = Source.KXHT_Add_MT
      ,Target.KXHT_KCDT = Source.KXHT_KCDT
      ,Target.KXSLDT_KK_MP = Source.KXSLDT_KK_MP
      ,Target.KXSLDT_KK_MT = Source.KXSLDT_KK_MT
      ,Target.KXSLDT_Cau_MP = Source.KXSLDT_Cau_MP
      ,Target.KXSLDT_Cau_MT = Source.KXSLDT_Cau_MT
      ,Target.KXSLDT_Tru_MP = Source.KXSLDT_Tru_MP
      ,Target.KXSLDT_Tru_MT = Source.KXSLDT_Tru_MT
      ,Target.KXSLDT_Truc_MP = Source.KXSLDT_Truc_MP
      ,Target.KXSLDT_Truc_MT = Source.KXSLDT_Truc_MT
      ,Target.KXSLDT_CK_MP = Source.KXSLDT_CK_MP
      ,Target.KXSLDT_CK_MT = Source.KXSLDT_CK_MT
      ,Target.KXSLDT_Add_MP = Source.KXSLDT_Add_MP
      ,Target.KXSLDT_Add_MT = Source.KXSLDT_Add_MT
      ,Target.KXSLDT_KCDT = Source.KXSLDT_KCDT
      ,Target.Skiascopy_MP = Source.Skiascopy_MP
      ,Target.Skiascopy_MT = Source.Skiascopy_MT
      ,Target.NhanAp_MP = Source.NhanAp_MP
      ,Target.NhanAp_MT = Source.NhanAp_MT
      ,Target.BeDayGiacMac_MP = Source.BeDayGiacMac_MP
      ,Target.BeDayGiacMac_MT = Source.BeDayGiacMac_MT
      ,Target.DuongKinhDongTu_MP = Source.DuongKinhDongTu_MP
      ,Target.DuongKinhDongTu_MT = Source.DuongKinhDongTu_MT
      ,Target.K1_MP = Source.K1_MP
      ,Target.K1_MT = Source.K1_MT
      ,Target.K2_MP = Source.K2_MP
      ,Target.K2_MT = Source.K2_MT
      ,Target.ThiTruongVaoVien_MP = Source.ThiTruongVaoVien_MP
      ,Target.ThiTruongVaoVien_MT = Source.ThiTruongVaoVien_MT
      ,Target.LeDao_MP = Source.LeDao_MP
      ,Target.LeDao_MT = Source.LeDao_MT
      ,Target.MiMat_MP = Source.MiMat_MP
      ,Target.MiMat_MT = Source.MiMat_MT
      ,Target.KetMac_MP = Source.KetMac_MP
      ,Target.KetMac_MT = Source.KetMac_MT
      ,Target.TinhHinhMatHot_MP = Source.TinhHinhMatHot_MP
      ,Target.TinhHinhMatHot_MT = Source.TinhHinhMatHot_MT
      ,Target.GiacMac_MP = Source.GiacMac_MP
      ,Target.GiacMac_MT = Source.GiacMac_MT
      ,Target.CungMac_MP = Source.CungMac_MP
      ,Target.CungMac_MT = Source.CungMac_MT
      ,Target.TienPhong_MP = Source.TienPhong_MP
      ,Target.TienPhong_MT = Source.TienPhong_MT
      ,Target.MongMat_MP = Source.MongMat_MP
      ,Target.MongMat_MT = Source.MongMat_MT
      ,Target.DongTuPhanXa_MP = Source.DongTuPhanXa_MP
      ,Target.DongTuPhanXa_MT = Source.DongTuPhanXa_MT
      ,Target.ThuyTinhThe_MP = Source.ThuyTinhThe_MP
      ,Target.ThuyTinhThe_MT = Source.ThuyTinhThe_MT
      ,Target.DichKinh_MP = Source.DichKinh_MP
      ,Target.DichKinh_MT = Source.DichKinh_MT
      ,Target.VongMac_MP = Source.VongMac_MP
      ,Target.VongMac_MT = Source.VongMac_MT
      ,Target.GaiThi_MP = Source.GaiThi_MP
      ,Target.GaiThi_MT = Source.GaiThi_MT
      ,Target.HoangDiem_MP = Source.HoangDiem_MP
      ,Target.HoangDiem_MT = Source.HoangDiem_MT
      ,Target.SoiAnhDongTu_MP = Source.SoiAnhDongTu_MP
      ,Target.SoiAnhDongTu_MT = Source.SoiAnhDongTu_MT
      ,Target.TinhHinhNhanCau_MP = Source.TinhHinhNhanCau_MP
      ,Target.TinhHinhNhanCau_MT = Source.TinhHinhNhanCau_MT
      ,Target.HoMat_MP = Source.HoMat_MP
      ,Target.HoMat_MT = Source.HoMat_MT
      ,Target.ThiLuc_MP = Source.ThiLuc_MP
      ,Target.ThiLuc_MT = Source.ThiLuc_MT
      ,Target.ThiLucLoKinh_MP = Source.ThiLucLoKinh_MP
      ,Target.ThiLucLoKinh_MT = Source.ThiLucLoKinh_MT
      ,Target.ChieuDaiTrucNhanCau_MP = Source.ChieuDaiTrucNhanCau_MP
      ,Target.ChieuDaiTrucNhanCau_MT = Source.ChieuDaiTrucNhanCau_MT
      ,Target.NhinXa_KK_MP = Source.NhinXa_KK_MP
      ,Target.NhinXa_KK_MT = Source.NhinXa_KK_MT
      ,Target.NhinXa_Cau_MP = Source.NhinXa_Cau_MP
      ,Target.NhinXa_Cau_MT = Source.NhinXa_Cau_MT
      ,Target.NhinXa_Tru_MP = Source.NhinXa_Tru_MP
      ,Target.NhinXa_Tru_MT = Source.NhinXa_Tru_MT
      ,Target.NhinXa_Truc_MP = Source.NhinXa_Truc_MP
      ,Target.NhinXa_Truc_MT = Source.NhinXa_Truc_MT
      ,Target.NhinXa_CK_MP = Source.NhinXa_CK_MP
      ,Target.NhinXa_CK_MT = Source.NhinXa_CK_MT
      ,Target.NhinXa_Add_MP = Source.NhinXa_Add_MP
      ,Target.NhinXa_Add_MT = Source.NhinXa_Add_MT
      ,Target.NhinXa_KCDT = Source.NhinXa_KCDT
      ,Target.NhinGan_KK_MP = Source.NhinGan_KK_MP
      ,Target.NhinGan_KK_MT = Source.NhinGan_KK_MT
      ,Target.NhinGan_Cau_MP = Source.NhinGan_Cau_MP
      ,Target.NhinGan_Cau_MT = Source.NhinGan_Cau_MT
      ,Target.NhinGan_Tru_MP = Source.NhinGan_Tru_MP
      ,Target.NhinGan_Tru_MT = Source.NhinGan_Tru_MT
      ,Target.NhinGan_Truc_MP = Source.NhinGan_Truc_MP
      ,Target.NhinGan_Truc_MT = Source.NhinGan_Truc_MT
      ,Target.NhinGan_CK_MP = Source.NhinGan_CK_MP
      ,Target.NhinGan_CK_MT = Source.NhinGan_CK_MT
      ,Target.NhinGan_Add_MP = Source.NhinGan_Add_MP
      ,Target.NhinGan_Add_MT = Source.NhinGan_Add_MT
      ,Target.NhinGan_KCDT = Source.NhinGan_KCDT
      ,Target.LoiDan = Source.LoiDan
      ,Target.NguoiThucHien = Source.NguoiThucHien
      ,Target.KC_KK_MP = Source.KC_KK_MP
      ,Target.KC_KK_MT = Source.KC_KK_MT
      ,Target.TrangThai = Source.TrangThai
      ,Target.MaPhongKham = Source.MaPhongKham
      ,Target.GhiChu = Source.GhiChu
      ,Target.KXHT_ChuaChinh_MP = Source.KXHT_ChuaChinh_MP
      ,Target.KXHT_ChuaChinh_MT = Source.KXHT_ChuaChinh_MT
      ,Target.KXHT_DaChinh_MT = Source.KXHT_DaChinh_MT
      ,Target.KXHT_DaChinh_MP = Source.KXHT_DaChinh_MP
      ,Target.KhoangCachDongTuXa = Source.KhoangCachDongTuXa
      ,Target.KhoangCachDongTuGan = Source.KhoangCachDongTuGan
      ,Target.CongNhinGan = Source.CongNhinGan
      ,Target.ThiLucCongNhinGan = Source.ThiLucCongNhinGan
      ,Target.KinhApTrong = Source.KinhApTrong
      ,Target.KinhDaTrong = Source.KinhDaTrong
      ,Target.KinhDoiMau = Source.KinhDoiMau
      ,Target.KinhHaiTrong = Source.KinhHaiTrong
      ,Target.KinhNhinGan = Source.KinhNhinGan
      ,Target.KinhPoly = Source.KinhPoly
      ,Target.KinhNhinXa = Source.KinhNhinXa
      ,Target.TinhTrangKinh = Source.TinhTrangKinh
      ,Target.ThoiGianSuDung = Source.ThoiGianSuDung
      ,Target.SoLuong = Source.SoLuong
      ,Target.KXHT_KK_MP_Xa = Source.KXHT_KK_MP_Xa
      ,Target.KXHT_KK_MT_Xa = Source.KXHT_KK_MT_Xa
      ,Target.KXHT_Cau_MP_Xa = Source.KXHT_Cau_MP_Xa
      ,Target.KXHT_Cau_MT_Xa = Source.KXHT_Cau_MT_Xa
      ,Target.KXHT_Tru_MP_Xa = Source.KXHT_Tru_MP_Xa
      ,Target.KXHT_Tru_MT_Xa = Source.KXHT_Tru_MT_Xa
      ,Target.KXHT_Truc_MP_Xa = Source.KXHT_Truc_MP_Xa
      ,Target.KXHT_Truc_MT_Xa = Source.KXHT_Truc_MT_Xa
      ,Target.KXHT_CK_MP_Xa = Source.KXHT_CK_MP_Xa
      ,Target.KXHT_CK_MT_Xa = Source.KXHT_CK_MT_Xa
      ,Target.KXHT_Add_MP_Xa = Source.KXHT_Add_MP_Xa
      ,Target.KXHT_Add_MT_Xa = Source.KXHT_Add_MT_Xa
      ,Target.KXHT_KCDT_Xa = Source.KXHT_KCDT_Xa
      ,Target.KXSLDT_KK_MP_Xa = Source.KXSLDT_KK_MP_Xa
      ,Target.KXSLDT_KK_MT_Xa = Source.KXSLDT_KK_MT_Xa
      ,Target.KXSLDT_Cau_MP_Xa = Source.KXSLDT_Cau_MP_Xa
      ,Target.KXSLDT_Cau_MT_Xa = Source.KXSLDT_Cau_MT_Xa
      ,Target.KXSLDT_Tru_MP_Xa = Source.KXSLDT_Tru_MP_Xa
      ,Target.KXSLDT_Tru_MT_Xa = Source.KXSLDT_Tru_MT_Xa
      ,Target.KXSLDT_Truc_MP_Xa = Source.KXSLDT_Truc_MP_Xa
      ,Target.KXSLDT_Truc_MT_Xa = Source.KXSLDT_Truc_MT_Xa
      ,Target.KXSLDT_CK_MP_Xa = Source.KXSLDT_CK_MP_Xa
      ,Target.KXSLDT_CK_MT_Xa = Source.KXSLDT_CK_MT_Xa
      ,Target.KXSLDT_Add_MP_Xa = Source.KXSLDT_Add_MP_Xa
      ,Target.KXSLDT_Add_MT_Xa = Source.KXSLDT_Add_MT_Xa
      ,Target.KXSLDT_KCDT_Xa = Source.KXSLDT_KCDT_Xa
      ,Target.ThiLucLoKinh_MP_Xa = Source.ThiLucLoKinh_MP_Xa
      ,Target.ThiLucLoKinh_MT_Xa = Source.ThiLucLoKinh_MT_Xa
      ,Target.Skiascopy_SauLiet_MP = Source.Skiascopy_SauLiet_MP
      ,Target.Skiascopy_SauLiet_MT = Source.Skiascopy_SauLiet_MT
      ,Target.ThoiGianTraThuoc = Source.ThoiGianTraThuoc
      ,Target.NhanAp_Maklakov_MP = Source.NhanAp_Maklakov_MP
      ,Target.NhanAp_Maklakov_MT = Source.NhanAp_Maklakov_MT
      ,Target.KXSLDT_ThiLucLoKinh_MP = Source.KXSLDT_ThiLucLoKinh_MP
      ,Target.KXSLDT_ThiLucLoKinh_MT = Source.KXSLDT_ThiLucLoKinh_MT
    , Target.NgayDongBo = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    INSERT (CoSoKey, NguonDuLieuKey, MaCoSo, MaHoSo, NgayDo
           ,KXM_Cau_MP
      ,KXM_Cau_MT
      ,KXM_Tru_MP
      ,KXM_Tru_MT
      ,KXM_Truc_MP
      ,KXM_Truc_MT
      ,KXM_KCDT
      ,KC_Cau_MP
      ,KC_Cau_MT
      ,KC_Tru_MP
      ,KC_Tru_MT
      ,KC_Truc_MP
      ,KC_Truc_MT
      ,KC_CK_MP
      ,KC_CK_MT
      ,KC_Add_MP
      ,KC_Add_MT
      ,KC_KCDT
      ,KXHT_KK_MP
      ,KXHT_KK_MT
      ,KXHT_Cau_MP
      ,KXHT_Cau_MT
      ,KXHT_Tru_MP
      ,KXHT_Tru_MT
      ,KXHT_Truc_MP
      ,KXHT_Truc_MT
      ,KXHT_CK_MP
      ,KXHT_CK_MT
      ,KXHT_Add_MP
      ,KXHT_Add_MT
      ,KXHT_KCDT
      ,KXSLDT_KK_MP
      ,KXSLDT_KK_MT
      ,KXSLDT_Cau_MP
      ,KXSLDT_Cau_MT
      ,KXSLDT_Tru_MP
      ,KXSLDT_Tru_MT
      ,KXSLDT_Truc_MP
      ,KXSLDT_Truc_MT
      ,KXSLDT_CK_MP
      ,KXSLDT_CK_MT
      ,KXSLDT_Add_MP
      ,KXSLDT_Add_MT
      ,KXSLDT_KCDT
      ,Skiascopy_MP
      ,Skiascopy_MT
      ,NhanAp_MP
      ,NhanAp_MT
      ,BeDayGiacMac_MP
      ,BeDayGiacMac_MT
      ,DuongKinhDongTu_MP
      ,DuongKinhDongTu_MT
      ,K1_MP
      ,K1_MT
      ,K2_MP
      ,K2_MT
      ,ThiTruongVaoVien_MP
      ,ThiTruongVaoVien_MT
      ,LeDao_MP
      ,LeDao_MT
      ,MiMat_MP
      ,MiMat_MT
      ,KetMac_MP
      ,KetMac_MT
      ,TinhHinhMatHot_MP
      ,TinhHinhMatHot_MT
      ,GiacMac_MP
      ,GiacMac_MT
      ,CungMac_MP
      ,CungMac_MT
      ,TienPhong_MP
      ,TienPhong_MT
      ,MongMat_MP
      ,MongMat_MT
      ,DongTuPhanXa_MP
      ,DongTuPhanXa_MT
      ,ThuyTinhThe_MP
      ,ThuyTinhThe_MT
      ,DichKinh_MP
      ,DichKinh_MT
      ,VongMac_MP
      ,VongMac_MT
      ,GaiThi_MP
      ,GaiThi_MT
      ,HoangDiem_MP
      ,HoangDiem_MT
      ,SoiAnhDongTu_MP
      ,SoiAnhDongTu_MT
      ,TinhHinhNhanCau_MP
      ,TinhHinhNhanCau_MT
      ,HoMat_MP
      ,HoMat_MT
      ,ThiLuc_MP
      ,ThiLuc_MT
      ,ThiLucLoKinh_MP
      ,ThiLucLoKinh_MT
      ,ChieuDaiTrucNhanCau_MP
      ,ChieuDaiTrucNhanCau_MT
      ,NhinXa_KK_MP
      ,NhinXa_KK_MT
      ,NhinXa_Cau_MP
      ,NhinXa_Cau_MT
      ,NhinXa_Tru_MP
      ,NhinXa_Tru_MT
      ,NhinXa_Truc_MP
      ,NhinXa_Truc_MT
      ,NhinXa_CK_MP
      ,NhinXa_CK_MT
      ,NhinXa_Add_MP
      ,NhinXa_Add_MT
      ,NhinXa_KCDT
      ,NhinGan_KK_MP
      ,NhinGan_KK_MT
      ,NhinGan_Cau_MP
      ,NhinGan_Cau_MT
      ,NhinGan_Tru_MP
      ,NhinGan_Tru_MT
      ,NhinGan_Truc_MP
      ,NhinGan_Truc_MT
      ,NhinGan_CK_MP
      ,NhinGan_CK_MT
      ,NhinGan_Add_MP
      ,NhinGan_Add_MT
      ,NhinGan_KCDT
      ,LoiDan
      ,NguoiThucHien
      ,KC_KK_MP
      ,KC_KK_MT
      ,TrangThai
      ,MaPhongKham
      ,GhiChu
      ,KXHT_ChuaChinh_MP
      ,KXHT_ChuaChinh_MT
      ,KXHT_DaChinh_MT
      ,KXHT_DaChinh_MP
      ,KhoangCachDongTuXa
      ,KhoangCachDongTuGan
      ,CongNhinGan
      ,ThiLucCongNhinGan
      ,KinhApTrong
      ,KinhDaTrong
      ,KinhDoiMau
      ,KinhHaiTrong
      ,KinhNhinGan
      ,KinhPoly
      ,KinhNhinXa
      ,TinhTrangKinh
      ,ThoiGianSuDung
      ,SoLuong
      ,KXHT_KK_MP_Xa
      ,KXHT_KK_MT_Xa
      ,KXHT_Cau_MP_Xa
      ,KXHT_Cau_MT_Xa
      ,KXHT_Tru_MP_Xa
      ,KXHT_Tru_MT_Xa
      ,KXHT_Truc_MP_Xa
      ,KXHT_Truc_MT_Xa
      ,KXHT_CK_MP_Xa
      ,KXHT_CK_MT_Xa
      ,KXHT_Add_MP_Xa
      ,KXHT_Add_MT_Xa
      ,KXHT_KCDT_Xa
      ,KXSLDT_KK_MP_Xa
      ,KXSLDT_KK_MT_Xa
      ,KXSLDT_Cau_MP_Xa
      ,KXSLDT_Cau_MT_Xa
      ,KXSLDT_Tru_MP_Xa
      ,KXSLDT_Tru_MT_Xa
      ,KXSLDT_Truc_MP_Xa
      ,KXSLDT_Truc_MT_Xa
      ,KXSLDT_CK_MP_Xa
      ,KXSLDT_CK_MT_Xa
      ,KXSLDT_Add_MP_Xa
      ,KXSLDT_Add_MT_Xa
      ,KXSLDT_KCDT_Xa
      ,ThiLucLoKinh_MP_Xa
      ,ThiLucLoKinh_MT_Xa
      ,Skiascopy_SauLiet_MP
      ,Skiascopy_SauLiet_MT
      ,ThoiGianTraThuoc
      ,NhanAp_Maklakov_MP
      ,NhanAp_Maklakov_MT
      ,KXSLDT_ThiLucLoKinh_MP
      ,KXSLDT_ThiLucLoKinh_MT
      , NgayDongBo)
    VALUES (Source.CoSoKey, Source.NguonDuLieuKey, Source.MaCoSo, Source.MaHoSo, Source.NgayDo
            ,Source.KXM_Cau_MP
      ,Source.KXM_Cau_MT
      ,Source.KXM_Tru_MP
      ,Source.KXM_Tru_MT
      ,Source.KXM_Truc_MP
      ,Source.KXM_Truc_MT
      ,Source.KXM_KCDT
      ,Source.KC_Cau_MP
      ,Source.KC_Cau_MT
      ,Source.KC_Tru_MP
      ,Source.KC_Tru_MT
      ,Source.KC_Truc_MP
      ,Source.KC_Truc_MT
      ,Source.KC_CK_MP
      ,Source.KC_CK_MT
      ,Source.KC_Add_MP
      ,Source.KC_Add_MT
      ,Source.KC_KCDT
      ,Source.KXHT_KK_MP
      ,Source.KXHT_KK_MT
      ,Source.KXHT_Cau_MP
      ,Source.KXHT_Cau_MT
      ,Source.KXHT_Tru_MP
      ,Source.KXHT_Tru_MT
      ,Source.KXHT_Truc_MP
      ,Source.KXHT_Truc_MT
      ,Source.KXHT_CK_MP
      ,Source.KXHT_CK_MT
      ,Source.KXHT_Add_MP
      ,Source.KXHT_Add_MT
      ,Source.KXHT_KCDT
      ,Source.KXSLDT_KK_MP
      ,Source.KXSLDT_KK_MT
      ,Source.KXSLDT_Cau_MP
      ,Source.KXSLDT_Cau_MT
      ,Source.KXSLDT_Tru_MP
      ,Source.KXSLDT_Tru_MT
      ,Source.KXSLDT_Truc_MP
      ,Source.KXSLDT_Truc_MT
      ,Source.KXSLDT_CK_MP
      ,Source.KXSLDT_CK_MT
      ,Source.KXSLDT_Add_MP
      ,Source.KXSLDT_Add_MT
      ,Source.KXSLDT_KCDT
      ,Source.Skiascopy_MP
      ,Source.Skiascopy_MT
      ,Source.NhanAp_MP
      ,Source.NhanAp_MT
      ,Source.BeDayGiacMac_MP
      ,Source.BeDayGiacMac_MT
      ,Source.DuongKinhDongTu_MP
      ,Source.DuongKinhDongTu_MT
      ,Source.K1_MP
      ,Source.K1_MT
      ,Source.K2_MP
      ,Source.K2_MT
      ,Source.ThiTruongVaoVien_MP
      ,Source.ThiTruongVaoVien_MT
      ,Source.LeDao_MP
      ,Source.LeDao_MT
      ,Source.MiMat_MP
      ,Source.MiMat_MT
      ,Source.KetMac_MP
      ,Source.KetMac_MT
      ,Source.TinhHinhMatHot_MP
      ,Source.TinhHinhMatHot_MT
      ,Source.GiacMac_MP
      ,Source.GiacMac_MT
      ,Source.CungMac_MP
      ,Source.CungMac_MT
      ,Source.TienPhong_MP
      ,Source.TienPhong_MT
      ,Source.MongMat_MP
      ,Source.MongMat_MT
      ,Source.DongTuPhanXa_MP
      ,Source.DongTuPhanXa_MT
      ,Source.ThuyTinhThe_MP
      ,Source.ThuyTinhThe_MT
      ,Source.DichKinh_MP
      ,Source.DichKinh_MT
      ,Source.VongMac_MP
      ,Source.VongMac_MT
      ,Source.GaiThi_MP
      ,Source.GaiThi_MT
      ,Source.HoangDiem_MP
      ,Source.HoangDiem_MT
      ,Source.SoiAnhDongTu_MP
      ,Source.SoiAnhDongTu_MT
      ,Source.TinhHinhNhanCau_MP
      ,Source.TinhHinhNhanCau_MT
      ,Source.HoMat_MP
      ,Source.HoMat_MT
      ,Source.ThiLuc_MP
      ,Source.ThiLuc_MT
      ,Source.ThiLucLoKinh_MP
      ,Source.ThiLucLoKinh_MT
      ,Source.ChieuDaiTrucNhanCau_MP
      ,Source.ChieuDaiTrucNhanCau_MT
      ,Source.NhinXa_KK_MP
      ,Source.NhinXa_KK_MT
      ,Source.NhinXa_Cau_MP
      ,Source.NhinXa_Cau_MT
      ,Source.NhinXa_Tru_MP
      ,Source.NhinXa_Tru_MT
      ,Source.NhinXa_Truc_MP
      ,Source.NhinXa_Truc_MT
      ,Source.NhinXa_CK_MP
      ,Source.NhinXa_CK_MT
      ,Source.NhinXa_Add_MP
      ,Source.NhinXa_Add_MT
      ,Source.NhinXa_KCDT
      ,Source.NhinGan_KK_MP
      ,Source.NhinGan_KK_MT
      ,Source.NhinGan_Cau_MP
      ,Source.NhinGan_Cau_MT
      ,Source.NhinGan_Tru_MP
      ,Source.NhinGan_Tru_MT
      ,Source.NhinGan_Truc_MP
      ,Source.NhinGan_Truc_MT
      ,Source.NhinGan_CK_MP
      ,Source.NhinGan_CK_MT
      ,Source.NhinGan_Add_MP
      ,Source.NhinGan_Add_MT
      ,Source.NhinGan_KCDT
      ,Source.LoiDan
      ,Source.NguoiThucHien
      ,Source.KC_KK_MP
      ,Source.KC_KK_MT
      ,Source.TrangThai
      ,Source.MaPhongKham
      ,Source.GhiChu
      ,Source.KXHT_ChuaChinh_MP
      ,Source.KXHT_ChuaChinh_MT
      ,Source.KXHT_DaChinh_MT
      ,Source.KXHT_DaChinh_MP
      ,Source.KhoangCachDongTuXa
      ,Source.KhoangCachDongTuGan
      ,Source.CongNhinGan
      ,Source.ThiLucCongNhinGan
      ,Source.KinhApTrong
      ,Source.KinhDaTrong
      ,Source.KinhDoiMau
      ,Source.KinhHaiTrong
      ,Source.KinhNhinGan
      ,Source.KinhPoly
      ,Source.KinhNhinXa
      ,Source.TinhTrangKinh
      ,Source.ThoiGianSuDung
      ,Source.SoLuong
      ,Source.KXHT_KK_MP_Xa
      ,Source.KXHT_KK_MT_Xa
      ,Source.KXHT_Cau_MP_Xa
      ,Source.KXHT_Cau_MT_Xa
      ,Source.KXHT_Tru_MP_Xa
      ,Source.KXHT_Tru_MT_Xa
      ,Source.KXHT_Truc_MP_Xa
      ,Source.KXHT_Truc_MT_Xa
      ,Source.KXHT_CK_MP_Xa
      ,Source.KXHT_CK_MT_Xa
      ,Source.KXHT_Add_MP_Xa
      ,Source.KXHT_Add_MT_Xa
      ,Source.KXHT_KCDT_Xa
      ,Source.KXSLDT_KK_MP_Xa
      ,Source.KXSLDT_KK_MT_Xa
      ,Source.KXSLDT_Cau_MP_Xa
      ,Source.KXSLDT_Cau_MT_Xa
      ,Source.KXSLDT_Tru_MP_Xa
      ,Source.KXSLDT_Tru_MT_Xa
      ,Source.KXSLDT_Truc_MP_Xa
      ,Source.KXSLDT_Truc_MT_Xa
      ,Source.KXSLDT_CK_MP_Xa
      ,Source.KXSLDT_CK_MT_Xa
      ,Source.KXSLDT_Add_MP_Xa
      ,Source.KXSLDT_Add_MT_Xa
      ,Source.KXSLDT_KCDT_Xa
      ,Source.ThiLucLoKinh_MP_Xa
      ,Source.ThiLucLoKinh_MT_Xa
      ,Source.Skiascopy_SauLiet_MP
      ,Source.Skiascopy_SauLiet_MT
      ,Source.ThoiGianTraThuoc
      ,Source.NhanAp_Maklakov_MP
      ,Source.NhanAp_Maklakov_MT
      ,Source.KXSLDT_ThiLucLoKinh_MP
      ,Source.KXSLDT_ThiLucLoKinh_MT , GETDATE());
```

### SOURCE: src/db/templates/sql/fact/FactThuPhiDichVu_ThuPhiGoi_merge.sql
```sql
--
-- FILE: FactThuPhiDichVu_ThuPhiGoi_merge.sql
-- AUTHOR: Claude Sonnet 4.6 (Builder)
-- CREATED: 2026-04-17
-- MODIFIED: 2026-04-17
-- VERSION: 1.0.0
-- PURPOSE: Template MERGE ThuPhiGoi vao dm.FactThuPhiDichVu voi LoaiHinh='TPG'.
--          Mapping: MaPhieuThu -> MaPhieuDichVu, TongTien, ThanhTien -> TongTienSauTangGiam.
-- HISTORY:
--     - v1.0.0 [2026-04-17]: Tao moi — dong bo ThuPhiGoi (LoaiHinh=TPG)
--

MERGE [{dm_schema}].[FactThuPhiDichVu] AS Target
USING (
    SELECT
        {co_so_key}        AS CoSoKey,
        {nguon_dulieu_key} AS NguonDuLieuKey,
        '{ma_co_so}' AS MaCoSo,
        s.MaHoSo,
        s.MaPhieuThu       AS MaPhieuDichVu,
        'TPG'              AS LoaiHinh,
        s.TongTien,
        s.ThanhTien        AS TongTienSauTangGiam,
        s.NgayThu          AS NgayDenKham,
        s.MaLoaiGoi        AS MaChiTieu,
        ISNULL(
            CAST(YEAR(s.NgayThu) * 10000
                 + MONTH(s.NgayThu) * 100
                 + DAY(s.NgayThu) AS INT),
            CAST(YEAR(s.NgayThu) * 10000
                 + MONTH(s.NgayThu) * 100
                 + DAY(s.NgayThu) AS INT)
        ) AS DateKey,
        CAST({nguon_dulieu_key} AS VARCHAR(10)) + ':' + s.MaLoaiGoi AS MaChiTieuBK,
        s.MaPhieuThu       AS SoHoaDon,
        NEWID() AS MaThuPhi,
        0 AS SoLuong,
        NULL AS DoanhThu,
        NULL AS DaThucHien,
        NULL AS TrangThaiPhieu
    FROM [{staging_schema}].[ThuPhiGoi] s WITH (NOLOCK)
    WHERE s.NgayThu IS NOT NULL AND s.MaPhieuThu IS NOT NULL
        AND CAST(s.NgayThu AS DATE) >= CAST('{date_from}' AS DATE)
        AND CAST(s.NgayThu AS DATE) <= CAST('{date_to}' AS DATE)
) AS Source
ON Target.NguonDuLieuKey = Source.NguonDuLieuKey
   AND Target.MaHoSo = Source.MaHoSo
   AND Target.MaPhieuDichVu = Source.MaPhieuDichVu
   AND Target.LoaiHinh = 'TPG'
WHEN MATCHED THEN
    UPDATE SET
        Target.TongTien = Source.TongTien,
        Target.TongTienSauTangGiam = Source.TongTienSauTangGiam,
        Target.NgayDenKham = Source.NgayDenKham
WHEN NOT MATCHED BY TARGET THEN
    /*
    INSERT (CoSoKey, NguonDuLieuKey, MaCoSo, MaHoSo, MaPhieuDichVu,
            LoaiHinh, TongTien, TongTienSauTangGiam, NgayDenKham, MaChiTieu, MaChiTieuBK, DateKey)
    VALUES (Source.CoSoKey, Source.NguonDuLieuKey, Source.MaCoSo,
            Source.MaHoSo, Source.MaPhieuDichVu, Source.LoaiHinh,
            Source.TongTien, Source.TongTienSauTangGiam, Source.NgayDenKham, 
            Source.MaChiTieu, Source.MaChiTieuBK, Source.DateKey);
    */
     INSERT (
        NguonDuLieuKey,
        CoSoKey,
        DateKey,
        LuotKhamKey,
        BenhNhanKey,
        DichVuKey,
        MaCoSo,
        MaThuPhi,
        MaPhieuDichVu,
        MaHoSo,
        MaChiTieu,
        MaChiTieuBK,
        NgayDenKham,
        SoLuong,
        TongTien,
        TongTienSauTangGiam,
        LoaiHinh,
        SoHoaDon,
        DoanhThu,
        DaThucHien,
        TrangThaiPhieu
    )
    VALUES (
        source.NguonDuLieuKey,
        source.CoSoKey,
        -- DateKey: YYYYMMDD
        source.DateKey,
        -- LuotKhamKey: lookup từ dm.DimLuotKham theo MaHoSo + NguonDuLieuKey
        ISNULL((
            SELECT TOP 1 lk.LuotKhamKey
            FROM dm.DimLuotKham lk WITH (NOLOCK)
            WHERE lk.NguonDuLieuKey = source.NguonDuLieuKey
              AND lk.MaHoSo         = source.MaHoSo
        ), 0),

        -- BenhNhanKey: lookup từ dm.DimLuotKham (nullable)
        (
            SELECT TOP 1 lk.BenhNhanKey
            FROM dm.DimLuotKham lk WITH (NOLOCK)
            WHERE lk.NguonDuLieuKey = source.NguonDuLieuKey
              AND lk.MaHoSo         = source.MaHoSo
        ),
        -- FIX v1.7.0: DichVuKey - lookup qua MaChiTieuBK (Business Key bat bien)
        -- Neu DimDichVu chua co MaChiTieuBK, fallback ve lookup qua MaChiTieu
        ISNULL((
            SELECT TOP 1 dv2.DichVuKey
            FROM dm.DimDichVu dv2 WITH (NOLOCK)
            WHERE dv2.MaChiTieuBK = source.MaChiTieuBK
        ), ISNULL((
            SELECT TOP 1 dv3.DichVuKey
            FROM dm.DimDichVu dv3 WITH (NOLOCK)
            WHERE dv3.NguonDuLieuKey = source.NguonDuLieuKey
              AND dv3.MaChiTieu      = source.MaChiTieu
        ), 0)),

        source.MaCoSo,
        source.MaThuPhi,
        source.MaPhieuDichVu,
        source.MaHoSo,
        source.MaChiTieu,
        source.MaChiTieuBK,
        source.NgayDenKham,
        source.SoLuong,
        source.TongTien,
        source.TongTienSauTangGiam,
        source.LoaiHinh,
        source.SoHoaDon,
        ISNULL(CAST(source.TongTienSauTangGiam AS FLOAT), 0),  -- DoanhThu = TongTienSauTangGiam
        source.DaThucHien,
        source.TrangThaiPhieu
    );
```

### SOURCE: src/db/templates/sql/fact/merge_fact_thuphichvu_3in1.sql
```sql
--
-- FILE: merge_fact_thuphichvu_3in1.sql
-- AUTHOR: GitHub Copilot (Builder)
-- CREATED: 2026-03-17
-- MODIFIED: 2026-03-27
-- VERSION: 1.9.1
-- PURPOSE: MERGE 3-in-1 doanh thu vào dm.FactThuPhiDichVu từ 3 nguồn:
--          1. ThuPhiDichVu (Dịch vụ) → LoaiHinh = 'DV'
--          2. ThuPhiBaoHiem (Bảo hiểm) → LoaiHinh = 'BH'
--          3. ThuPhiTangGiam → JOIN để tính TongTienSauTangGiam cho nguồn DV
--
--          Logic:
--          - ThuPhiDichVu LEFT JOIN ThuPhiTangGiam để tính TongTienSauTangGiam
--          - ThuPhiBaoHiem: TongTienSauTangGiam = TongTien + TienChenhLech
--          - DateKey = YEAR * 10000 + MONTH * 100 + DAY (từ NgayDoanhThu)
--          - LuotKhamKey, BenhNhanKey, DichVuKey: lookup từ DimLuotKham, DimDichVu
--          - MaChiTieuBK: Business Key bất biến = NguonDuLieuKey + ':' + MaChiTieu
--            (FIX E018 v1.7.3: Dung separator ':' thay vi '_' de dong nhat voi CLAUDE.md Section 7.1)
--
-- PARAMETERS (placeholders de thay the trong _substitute_params):
--     {nguon_dulieu_key} INT     - Key của nguồn dữ liệu (vd: 1 cho hanoi)
--     {coso_key}         INT     - Key của cơ sở (vd: 1 cho hanoi)
--     {ma_co_so}         NVARCHAR(50) - Ma co so (vd: 'hanoi')
--     {date_from}        DATE    - Ngày bắt đầu (inclusive)
--     {date_to}          DATE    - Ngày kết thúc (inclusive)
--     {staging_schema}   NVARCHAR(128) - Schema staging của facility
--
-- HISTORY:
--     - v1.0.0 [2026-03-17]: Tạo mới - MERGE 3-in-1 từ chỉ thị Opus Architect
--     - v1.1.0 [2026-03-17]: Sửa MERGE key: thay MaThuPhi bằng MaChiTieu + MaPhieuDichVu
--     - v1.2.0 [2026-03-18]: Thay hardcode bang placeholder facility va keys
--     - v1.4.0 [2026-03-24]: Bo sung MaDotThuPhi vao khoa MERGE
--     - v1.5.0 [2026-03-24]: Go MaDotThuPhi (khong ton tai trong schema thuc te)
--     - v1.6.0 [2026-03-25]: FIX E010 - Loai bo DECLARE @DateFrom/@DateTo, thay bang embedded
--                            string ({date_from}/{date_to}) de tranh GO batch scope loi
--     - v1.7.1 [2026-03-26]: LOAI BO MaChiTieuBK khoi ON clause (gay NULL comparison loi)
--                            MaChiTieuBK chi la data column, khong phai identity key
--     - v1.7.0 [2026-03-26]: [FEATURE] Them MaChiTieuBK (Business Key bat bien) vao MERGE
--                            + Toi uu cong thuc TongTienSauTangGiam (khong con CASE WHEN)
--                            + LOOKUP DichVuKey qua MaChiTieuBK thay vi MaChiTieu
--     - v1.8.0 [2026-03-27]: [FIX E020] LEFT JOIN -> tg_agg subquery (SUM aggregation)
--                            trong Nguon 1 ThuPhiDichVu de tranh nhan ban dong
--                            khi ThuPhiTangGiam co nhieu record cung khoa.
--                            Cong thuc: TongTienSauTangGiam = TongTien - TongGiam + TongTang
--     - v1.9.1 [2026-04-03]: [FIX E021] Them date filter vao tg_agg subquery.
--                            Root cause: Khong co date filter -> tg_agg SUM toan bo lich su,
--                            ngay cuoi cung nhan TatCaTangGiam = SUM TatCa -> bi sai thanh 0.
--                            Fix: Loc tg_agg theo {date_from}/{date_to} giong nhu dv/bh.
--     - v1.7.3 [2026-03-27]: [FIX E018] Doi separator MaChiTieuBK tu '_' thanh ':'
--                            de dong nhat voi CLAUDE.md Section 7.1 va MaBenhNhanBK
--


-- ============================================================
-- KHAI BAO THAM SỐ (chỉnh sửa theo môi trường thực tế)
-- ============================================================
DECLARE @NguonDuLieuKey INT     = {nguon_dulieu_key};
DECLARE @CoSoKey        INT     = {coso_key};
DECLARE @MaCoSo         NVARCHAR(50) = '{ma_co_so}';

-- FIX E010 v1.6.0: {date_from} va {date_to} la string placeholder
-- duoc thay the truc tiep trong Python _substitute_params() truoc khi tach GO batch
-- Vi du: {date_from} = '2026-03-10', {date_to} = '2026-03-10'
-- KHONG dung @DateFrom/@DateTo vi no bi mat scope khi GO tach batch

-- ============================================================
-- MERGE 3-IN-1: ThuPhiDichVu (DV) + ThuPhiBaoHiem (BH) + ThuPhiTangGiam (điều chỉnh)
-- ============================================================
MERGE [dm].[FactThuPhiDichVu] AS target
USING (

    -- --------------------------------------------------------
    -- NGUỒN 1: ThuPhiDichVu (Dịch vụ) - LEFT JOIN với ThuPhiTangGiam
    -- LoaiHinh = 'DV'
    -- FIX v1.7.2: Doc NguonDuLieuKey/CoSoKey tu staging (da enriched),
    --              khong dung gia tri tham so (vi enrichment da xay ra o Step 2)
    -- --------------------------------------------------------
    SELECT
        ISNULL(dv.NguonDuLieuKey, @NguonDuLieuKey) AS NguonDuLieuKey,
        ISNULL(dv.CoSoKey, @CoSoKey)                AS CoSoKey,
        ISNULL(dv.MaCoSo, @MaCoSo)                 AS MaCoSo,
        dv.MaThuPhi,
        dv.MaPhieuDichVu,
        dv.MaHoSo,
        dv.MaChiTieu,
        -- FIX v1.7.3 E018: MaChiTieuBK = NguonDuLieuKey (da enriched) + ':' + MaChiTieu
        -- (Doi tu '_' thanh ':' de dong nhat voi CLAUDE.md Section 7.1)
        CAST(ISNULL(dv.NguonDuLieuKey, @NguonDuLieuKey) AS VARCHAR(10)) + ':' + dv.MaChiTieu AS MaChiTieuBK,
        dv.NgayDenKham,
        dv.NgayVaoMay                               AS NgayDoanhThu,

        -- DateKey: tính từ NgayDoanhThu theo công thức YYYYMMDD
        ISNULL(
            CAST(YEAR(dv.NgayVaoMay) * 10000
                 + MONTH(dv.NgayVaoMay) * 100
                 + DAY(dv.NgayVaoMay) AS INT),
            CAST(YEAR(dv.NgayDenKham) * 10000
                 + MONTH(dv.NgayDenKham) * 100
                 + DAY(dv.NgayDenKham) AS INT)
        )                                           AS DateKey,

        -- SoLuongChuan: ưu tiên SoLuongThucHien, fallback SoLuong, default 1
        COALESCE(dv.SoLuongThucHien, dv.SoLuong, 1) AS SoLuongChuan,

        -- TongTien: giá trị gốc từ ThuPhiDichVu
        dv.TongTien                                 AS TongTien,

        -- FIX v1.8.0 E020: TongTienSauTangGiam - dung tg_agg (SUM aggregation)
        -- ThuPhiTangGiam co the co nhieu dong cung khoa -> aggregate SUM truoc khi JOIN
        -- Cong thuc: TongTien - TongGiam + TongTang
        dv.TongTien - ISNULL(tg_agg.TongGiam, 0) + ISNULL(tg_agg.TongTang, 0) AS TongTienSauTangGiam,

        -- LoaiHinh = 'DV' cho dịch vụ thường
        'DV'                                        AS LoaiHinh,

        dv.SoHoaDon,
        dv.DaThucHien,
        dv.TrangThaiPhieu

    -- FIX v1.8.0 E020: Pre-aggregate ThuPhiTangGiam bang subquery de tranh nhan ban
    -- Nếu cùng MaHoSo+MaChiTieu+MaPhieuDichVu có N dòng TG -> SUM(N) = TongGiam
    -- FIX E021 v1.9.1: THEM date filter vao tg_agg de chi aggregate dung ngay.
    -- Root cause: Khong co date filter -> tg_agg tong hop NHIEU THANG, khi merge
    -- ngay cuoi cung (01/04), TatCaTangGiam = SUM TatCa -> bi sai thanh 0.
    FROM [{staging_schema}].[ThuPhiDichVu] dv WITH (NOLOCK)
    LEFT JOIN (
        SELECT
            MaHoSo,
            MaChiTieu,
            MaPhieuDichVu,
            SUM(SoTienGiam) AS TongGiam,
            SUM(SoTienTang) AS TongTang
        FROM [{staging_schema}].[ThuPhiTangGiam] WITH (NOLOCK)
        WHERE DaDongTien = 1
          -- E021: LOC THEO NGAY - chi aggregate nhung dong trong date range hien tai
          AND CAST(NgayDenKham AS DATE) >= CAST('{date_from}' AS DATE)
          AND CAST(NgayDenKham AS DATE) <= CAST('{date_to}' AS DATE)
        GROUP BY MaHoSo, MaChiTieu, MaPhieuDichVu
    ) AS tg_agg
        ON dv.MaHoSo         = tg_agg.MaHoSo
        AND dv.MaChiTieu     = tg_agg.MaChiTieu
        AND dv.MaPhieuDichVu = tg_agg.MaPhieuDichVu
    WHERE dv.DaDongTien = 1
        AND dv.MaChiTieu IS NOT NULL
        AND LTRIM(RTRIM(dv.MaChiTieu)) <> ''
        -- FIX E010 v1.6.0: Dung embedded string thay vi @DateFrom/@DateTo (bi mat scope)
        AND CAST(dv.NgayDenKham AS DATE) >= CAST('{date_from}' AS DATE)
        AND CAST(dv.NgayDenKham AS DATE) <= CAST('{date_to}' AS DATE)

    UNION ALL

    -- --------------------------------------------------------
    -- NGUỒN 2: ThuPhiBaoHiem (Bảo hiểm)
    -- LoaiHinh = 'BH'
    -- FIX v1.7.2: Doc NguonDuLieuKey/CoSoKey tu staging (da enriched)
    -- --------------------------------------------------------
    SELECT
        ISNULL(bh.NguonDuLieuKey, @NguonDuLieuKey) AS NguonDuLieuKey,
        ISNULL(bh.CoSoKey, @CoSoKey)                AS CoSoKey,
        ISNULL(bh.MaCoSo, @MaCoSo)                AS MaCoSo,
        bh.MaThuPhi,
        bh.MaPhieuDichVu,
        bh.MaHoSo,
        bh.MaChiTieu,
        -- MaChiTieuBK = NguonDuLieuKey (da enriched) + ':' + MaChiTieu
        -- FIX E018 v1.7.3: Doi tu '_' thanh ':'
        CAST(ISNULL(bh.NguonDuLieuKey, @NguonDuLieuKey) AS VARCHAR(10)) + ':' + bh.MaChiTieu AS MaChiTieuBK,
        bh.NgayDenKham,
        bh.NgayVaoMay                               AS NgayDoanhThu,

        -- DateKey: tính từ NgayDoanhThu
        ISNULL(
            CAST(YEAR(bh.NgayVaoMay) * 10000
                 + MONTH(bh.NgayVaoMay) * 100
                 + DAY(bh.NgayVaoMay) AS INT),
            CAST(YEAR(bh.NgayDenKham) * 10000
                 + MONTH(bh.NgayDenKham) * 100
                 + DAY(bh.NgayDenKham) AS INT)
        )                                           AS DateKey,

        -- SoLuongChuan
        COALESCE(bh.SoLuongThucHien, bh.SoLuong, 1) AS SoLuongChuan,

        -- TongTien: giá trị gốc từ ThuPhiBaoHiem
        bh.TongTien                                 AS TongTien,

        -- FIX v1.7.0: TongTienSauTangGiam - cong thuc truc tiep
        -- BH khong co bang ThuPhiTangGiam -> TienChenhLech la adjustments
        bh.TongTien + ISNULL(bh.TienChenhLech, 0)  AS TongTienSauTangGiam,

        -- LoaiHinh = 'BH' cho bảo hiểm
        'BH'                                        AS LoaiHinh,

        bh.SoHoaDon,
        NULL                                        AS DaThucHien,   -- BH không có cột này
        bh.TrangThaiPhieu

    FROM [{staging_schema}].[ThuPhiBaoHiem] bh WITH (NOLOCK)
    WHERE bh.DaDongTien = 1
        AND bh.MaChiTieu IS NOT NULL
        AND LTRIM(RTRIM(bh.MaChiTieu)) <> ''
        -- FIX E010 v1.6.0: Dung embedded string thay vi @DateFrom/@DateTo (bi mat scope)
        AND CAST(bh.NgayDenKham AS DATE) >= CAST('{date_from}' AS DATE)
        AND CAST(bh.NgayDenKham AS DATE) <= CAST('{date_to}' AS DATE)

) AS source

-- ============================================================
-- ĐIỀU KIỆN MATCH: khóa tự nhiên của Fact (4 cột gốc)
-- FIX v1.7.1: LOẠI BỎ MaChiTieuBK khỏi ON clause
--             MaChiTieuBK chỉ là data column, không phải business key.
--             Dùng MaChiTieuBK trong INSERT để populate cho record mới.
--             Lookup DichVuKey dùng MaChiTieuBK để đảm bảo consistency.
-- ============================================================
ON  target.NguonDuLieuKey = source.NguonDuLieuKey
AND target.CoSoKey        = source.CoSoKey
AND target.MaHoSo         = source.MaHoSo
AND target.MaChiTieu      = source.MaChiTieu
AND target.MaPhieuDichVu  = source.MaPhieuDichVu
-- MaChiTieuBK: KHÔNG đưa vào ON vì:
--   1. Target NULL + Source NOT NULL = không match → INSERT thất bại vì duplicate
--   2. MaChiTieuBK chỉ là computed data, không phải identity key

-- ============================================================
-- WHEN MATCHED: Cập nhật các cột dữ liệu
-- ============================================================
WHEN MATCHED THEN
    UPDATE SET
        target.TongTien             = source.TongTien,
        target.TongTienSauTangGiam  = source.TongTienSauTangGiam,
        target.LoaiHinh             = source.LoaiHinh,
        target.SoHoaDon             = source.SoHoaDon,
        target.SoLuong              = source.SoLuongChuan,
        target.DoanhThu             = ISNULL(CAST(source.TongTienSauTangGiam AS FLOAT), 0),
        target.DaThucHien           = source.DaThucHien,
        target.TrangThaiPhieu       = source.TrangThaiPhieu,
        target.NgayDenKham          = source.NgayDenKham

-- ============================================================
-- WHEN NOT MATCHED: Insert bản ghi mới
-- ============================================================
WHEN NOT MATCHED BY TARGET THEN
    INSERT (
        NguonDuLieuKey,
        CoSoKey,
        DateKey,
        LuotKhamKey,
        BenhNhanKey,
        DichVuKey,
        MaCoSo,
        MaThuPhi,
        MaPhieuDichVu,
        MaHoSo,
        MaChiTieu,
        MaChiTieuBK,
        NgayDenKham,
        SoLuong,
        TongTien,
        TongTienSauTangGiam,
        LoaiHinh,
        SoHoaDon,
        DoanhThu,
        DaThucHien,
        TrangThaiPhieu
    )
    VALUES (
        source.NguonDuLieuKey,
        source.CoSoKey,

        -- DateKey: YYYYMMDD
        source.DateKey,

        -- LuotKhamKey: lookup từ dm.DimLuotKham theo MaHoSo + NguonDuLieuKey
        ISNULL((
            SELECT TOP 1 lk.LuotKhamKey
            FROM dm.DimLuotKham lk WITH (NOLOCK)
            WHERE lk.NguonDuLieuKey = source.NguonDuLieuKey
              AND lk.MaHoSo         = source.MaHoSo
        ), 0),

        -- BenhNhanKey: lookup từ dm.DimLuotKham (nullable)
        (
            SELECT TOP 1 lk.BenhNhanKey
            FROM dm.DimLuotKham lk WITH (NOLOCK)
            WHERE lk.NguonDuLieuKey = source.NguonDuLieuKey
              AND lk.MaHoSo         = source.MaHoSo
        ),

        -- FIX v1.7.0: DichVuKey - lookup qua MaChiTieuBK (Business Key bat bien)
        -- Neu DimDichVu chua co MaChiTieuBK, fallback ve lookup qua MaChiTieu
        ISNULL((
            SELECT TOP 1 dv2.DichVuKey
            FROM dm.DimDichVu dv2 WITH (NOLOCK)
            WHERE dv2.MaChiTieuBK = source.MaChiTieuBK
        ), ISNULL((
            SELECT TOP 1 dv3.DichVuKey
            FROM dm.DimDichVu dv3 WITH (NOLOCK)
            WHERE dv3.NguonDuLieuKey = source.NguonDuLieuKey
              AND dv3.MaChiTieu      = source.MaChiTieu
        ), 0)),

        source.MaCoSo,
        source.MaThuPhi,
        source.MaPhieuDichVu,
        source.MaHoSo,
        source.MaChiTieu,
        source.MaChiTieuBK,
        source.NgayDenKham,
        source.SoLuongChuan,
        source.TongTien,
        source.TongTienSauTangGiam,
        source.LoaiHinh,
        source.SoHoaDon,
        ISNULL(CAST(source.TongTienSauTangGiam AS FLOAT), 0),  -- DoanhThu = TongTienSauTangGiam
        source.DaThucHien,
        source.TrangThaiPhieu
    );
GO

-- ============================================================
-- THỐNG KÊ SAU KHI MERGE
-- ============================================================
-- FIX E010 v1.6.0: Dung embedded string thay vi @DateFrom/@DateTo (bi mat scope)
SELECT
    LoaiHinh,
    COUNT(*)                    AS SoBanGhi,
    SUM(TongTien)               AS TongTien,
    SUM(TongTienSauTangGiam)    AS TongTienSauTangGiam,
    SUM(DoanhThu)               AS TongDoanhThu
FROM [dm].[FactThuPhiDichVu]
WHERE NgayDenKham >= CAST('{date_from}' AS DATE)
  AND NgayDenKham <  DATEADD(DAY, 1, CAST('{date_to}' AS DATE))
GROUP BY LoaiHinh
ORDER BY LoaiHinh;
GO
```

### SOURCE: src/jobs/__init__.py
```py
from src.jobs.dimension_loader import DimensionLoader
from src.jobs.fact_loader import FactLoader
from src.jobs.sync_orchestrator import SyncOrchestrator

__all__ = [
    "DimensionLoader",
    "FactLoader",
    "SyncOrchestrator",
]
```

### SOURCE: src/jobs/dimension_loader.py
```py
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import pyodbc

from src.core.base_loader import BaseLoader


@dataclass(frozen=True)
class DimensionTableSpec:
    dimension_name: str
    source_tables: tuple[str, ...]
    merge_sql_path: str


class DimensionLoader(BaseLoader):
    DEFAULT_DIMENSION_SPECS: tuple[DimensionTableSpec, ...] = (
        DimensionTableSpec(
            dimension_name="DimBenhNhan",
            source_tables=("DMBenhNhan",),
            merge_sql_path="src/db/templates/sql/dimension/DimBenhNhan_merge.sql",
        ),
        DimensionTableSpec(
            dimension_name="DimBenh",
            source_tables=("DMBenh",),
            merge_sql_path="src/db/templates/sql/dimension/DimBenh_merge.sql",
        ),
        DimensionTableSpec(
            dimension_name="DimLoaiGoiDichVu",
            source_tables=("LoaiGoiDichVuNT",),
            merge_sql_path="src/db/templates/sql/dimension/DimLoaiGoiDichVu_merge.sql",
        ),
        DimensionTableSpec(
            dimension_name="DimDichVu",
            source_tables=("DMLoaiDichVu", "DMDichVu", "DMDichVuChiTiet"),
            merge_sql_path="src/db/templates/sql/dimension/dim_dich_vu_merge.sql",
        ),
    )

    def __init__(
        self,
        datamart_connection: str,
        production_connection: str,
        facility_code: str,
        facility_schema: str,
        nguon_dulieu_key: int,
        co_so_key: int,
        dimension_specs: tuple[DimensionTableSpec, ...] | None = None,
    ) -> None:
        super().__init__(connection_string=datamart_connection, table_name=f"DimensionLoader:{facility_code}")
        self.production_connection = production_connection
        self.prod_env_key = "production"
        self.connection_strings: dict[str, str] = {self.prod_env_key: production_connection}
        self.facility_code = facility_code
        self.facility_schema = facility_schema
        self.nguon_dulieu_key = nguon_dulieu_key
        self.co_so_key = co_so_key
        self.dimension_specs = dimension_specs or self.DEFAULT_DIMENSION_SPECS

    def _log(self, message: str, **kwargs) -> None:
        _ = kwargs
        from datetime import datetime

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] {message}", flush=True)

    def _truncate_table(self, connection: pyodbc.Connection, schema_name: str, table_name: str) -> None:
        # Lệnh thay đổi dữ liệu chỉ chạy trên connection Datamart/ODS, không dùng Production.
        sql = f"TRUNCATE TABLE [{schema_name}].[{table_name}];"
        self._log(f"TRUNCATE {schema_name}.{table_name}")
        self.execute_sql_sync(connection, sql)
        connection.commit()

    def _copy_prod_to_ods(self, connection: pyodbc.Connection, table_name: str) -> None:
        self._log(f"Đang kéo dữ liệu {table_name} từ Prod -> ODS bằng ODBC Bulk Copy...")

        # 1. Kết nối Production (Chỉ được SELECT)
        prod_conn_str = self.connection_strings[self.prod_env_key]
        prod_conn = pyodbc.connect(prod_conn_str, autocommit=True)
        prod_cursor = prod_conn.cursor()

        try:
            # 2. Truy vấn dữ liệu gốc
            query = f"SELECT * FROM dbo.[{table_name}] WITH (NOLOCK)"
            prod_cursor.execute(query)

            # Lấy danh sách cột để sinh câu lệnh INSERT động
            columns = [column[0] for column in prod_cursor.description]
            col_names_str = ", ".join([f"[{c}]" for c in columns])
            placeholders = ", ".join(["?"] * len(columns))
            insert_sql = f"INSERT INTO [{self.facility_schema}].[{table_name}] ({col_names_str}) VALUES ({placeholders})"

            # 3. Chuẩn bị Cursor cho Staging với fast_executemany
            stg_cursor = connection.cursor()
            # Hotfix MemoryError: vô hiệu hóa fast_executemany với bảng có cột VARCHAR/NVARCHAR(MAX).
            stg_cursor.fast_executemany = False

            # 4. Đẩy dữ liệu theo lô (Chunking) để không tràn RAM
            chunk_size = 1000
            total_rows = 0

            while True:
                rows = prod_cursor.fetchmany(chunk_size)
                if not rows:
                    break

                # Chuyển đổi pyodbc.Row thành tuple để executemany có thể xử lý
                data_chunk = [tuple(row) for row in rows]
                stg_cursor.executemany(insert_sql, data_chunk)
                connection.commit()

                total_rows += len(data_chunk)
                self._log(f"Đã copy {total_rows} dòng vào ODS...")

            self._log(f"[SUCCESS] Hoàn tất kéo {total_rows} dòng cho {table_name}.")
        finally:
            prod_cursor.close()
            prod_conn.close()

    def _render_merge_sql(self, merge_sql_path: str) -> str:
        template = Path(merge_sql_path).read_text(encoding="utf-8")
        return template.format(
            dm_schema="dm",
            staging_schema=self.facility_schema,
            nguon_dulieu_key=self.nguon_dulieu_key,
            ma_co_so=self.facility_code,
            co_so_key=self.co_so_key,
        )

    def _execute_dimension_spec(self, connection: pyodbc.Connection, spec: DimensionTableSpec) -> None:
        self._log(f"Bắt đầu FULL LOAD dimension: {spec.dimension_name}")

        for source_table in spec.source_tables:
            self._truncate_table(connection, self.facility_schema, source_table)
            self._copy_prod_to_ods(connection, source_table)

        merge_sql = self._render_merge_sql(spec.merge_sql_path)
        self._log(f"[START] Đang thực thi MERGE ODS -> Datamart cho {spec.dimension_name}...")
        # Lệnh MERGE chỉ chạy trên connection Datamart/ODS, không dùng Production.
        self.execute_sql_sync(connection, merge_sql)
        connection.commit()
        self._log(f"[SUCCESS] Hoàn thành MERGE {spec.dimension_name}")

    def _execute_core(self, connection: pyodbc.Connection, *args: Any, **kwargs: Any) -> None:
        _ = args
        _ = kwargs
        for spec in self.dimension_specs:
            self._execute_dimension_spec(connection, spec)
```

### SOURCE: src/jobs/fact_loader.py
```py
from __future__ import annotations

import os
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any

import pyodbc

from src.core.base_loader import BaseLoader


@dataclass(frozen=True)
class FactTableSpec:
    table_name: str
    key_columns: tuple[str, ...]
    date_column: str


class FactLoader(BaseLoader):
    LANDING_SCHEMA = "stg_nano_v2"
    # Nợ kỹ thuật đã tách khỏi luồng FULL_LOAD Dimension:
    # DimLuotKham có bản chất incremental và sẽ được xử lý trong phạm vi Fact pipeline.
    PENDING_INCREMENTAL_DIMENSIONS: tuple[str, ...] = ("DimLuotKham",)

    FACT_SPECS: tuple[FactTableSpec, ...] = (
        FactTableSpec(
            table_name="ThuPhiDichVu",
            key_columns=("MaHoSo", "MaChiTieu", "MaPhieuDichVu"),
            date_column="NgayDenKham",
        ),
        FactTableSpec(
            table_name="ThuPhiBaoHiem",
            key_columns=("MaHoSo", "MaChiTieu", "MaPhieuDichVu"),
            date_column="NgayDenKham",
        ),
        FactTableSpec(
            table_name="ThuPhiTangGiam",
            key_columns=("MaHoSo", "MaChiTieu", "MaPhieuDichVu"),
            date_column="NgayDenKham",
        ),
    )

    def __init__(
        self,
        datamart_connection: str,
        production_connection: str,
        facility_code: str,
        facility_schema: str,
        nguon_dulieu_key: int,
        co_so_key: int,
        lookback_days: int = 3,
        batch_size: int = 10000,
    ) -> None:
        super().__init__(connection_string=datamart_connection, table_name=f"FactLoader:{facility_code}")
        self.production_connection = production_connection
        self.facility_code = facility_code
        self.facility_schema = facility_schema
        self.nguon_dulieu_key = nguon_dulieu_key
        self.co_so_key = co_so_key
        self.lookback_days = lookback_days
        self.batch_size = batch_size

    @staticmethod
    def _parse_connection_string(connection_string: str) -> dict[str, str]:
        parsed: dict[str, str] = {}
        for item in connection_string.split(";"):
            if not item or "=" not in item:
                continue
            key, value = item.split("=", 1)
            parsed[key.strip().upper()] = value.strip()
        return parsed

    @staticmethod
    def _build_bcp_auth_args(conn_parts: dict[str, str]) -> list[str]:
        if conn_parts.get("UID") and conn_parts.get("PWD"):
            return ["-U", conn_parts["UID"], "-P", conn_parts["PWD"]]
        return ["-T"]

    @staticmethod
    def _normalize_date(value: Any, fallback: date) -> date:
        if value is None:
            return fallback
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        raise ValueError(f"Không parse được ngày từ giá trị: {value}")

    def _truncate_table(self, connection: pyodbc.Connection, schema_name: str, table_name: str) -> None:
        sql = f"TRUNCATE TABLE [{schema_name}].[{table_name}];"
        self._log(f"TRUNCATE {schema_name}.{table_name}")
        self.execute_sql_sync(connection, sql)

    def _landing_cleanup(self, connection: pyodbc.Connection) -> None:
        for spec in self.FACT_SPECS:
            self._truncate_table(connection, self.LANDING_SCHEMA, spec.table_name)

    def _run_bcp_queryout(self, query: str, output_file: str, prod_parts: dict[str, str]) -> None:
        command = [
            "bcp",
            query,
            "queryout",
            output_file,
            "-S",
            prod_parts.get("SERVER", ""),
            "-d",
            prod_parts.get("DATABASE", ""),
            *self._build_bcp_auth_args(prod_parts),
            "-w",
            "-t\t",
            "-r\n",
            "-q",
        ]
        self._log(f"BCP queryout: {' '.join(command)}")
        subprocess.run(command, check=True, shell=False)

    def _run_bcp_in(self, full_table_name: str, input_file: str, dm_parts: dict[str, str]) -> None:
        command = [
            "bcp",
            full_table_name,
            "in",
            input_file,
            "-S",
            dm_parts.get("SERVER", ""),
            "-d",
            dm_parts.get("DATABASE", ""),
            *self._build_bcp_auth_args(dm_parts),
            "-w",
            "-t\t",
            "-r\n",
            "-q",
        ]
        self._log(f"BCP in: {' '.join(command)}")
        subprocess.run(command, check=True, shell=False)

    def _copy_delta_prod_to_landing(
        self,
        connection: pyodbc.Connection,
        spec: FactTableSpec,
        lookback_date: date,
        to_date: date,
    ) -> None:
        self._truncate_table(connection, self.LANDING_SCHEMA, spec.table_name)

        prod_parts = self._parse_connection_string(self.production_connection)
        dm_parts = self._parse_connection_string(self.connection_string)

        query = (
            f"SELECT * FROM dbo.{spec.table_name} WITH (NOLOCK) "
            f"WHERE CAST({spec.date_column} AS DATE) >= '{lookback_date:%Y-%m-%d}' "
            f"AND CAST({spec.date_column} AS DATE) <= '{to_date:%Y-%m-%d}'"
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            temp_path = tmp_file.name

        try:
            self._run_bcp_queryout(query=query, output_file=temp_path, prod_parts=prod_parts)
            self._run_bcp_in(
                full_table_name=f"{self.LANDING_SCHEMA}.{spec.table_name}",
                input_file=temp_path,
                dm_parts=dm_parts,
            )
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def _get_common_columns(
        self,
        connection: pyodbc.Connection,
        source_schema: str,
        source_table: str,
        target_schema: str,
        target_table: str,
    ) -> list[str]:
        sql = """
            SELECT s.COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS s
            INNER JOIN INFORMATION_SCHEMA.COLUMNS t
                ON s.COLUMN_NAME = t.COLUMN_NAME
               AND t.TABLE_SCHEMA = ?
               AND t.TABLE_NAME = ?
            WHERE s.TABLE_SCHEMA = ?
              AND s.TABLE_NAME = ?
            ORDER BY s.ORDINAL_POSITION;
        """
        cursor = connection.cursor()
        cursor.execute(sql, target_schema, target_table, source_schema, source_table)
        return [row[0] for row in cursor.fetchall()]

    def _build_ods_merge_sql(self, spec: FactTableSpec, common_columns: list[str], lookback_date: date, to_date: date) -> str:
        if not common_columns:
            raise ValueError(f"Không tìm thấy cột chung để MERGE ODS cho bảng {spec.table_name}")

        key_columns = [column for column in spec.key_columns if column in common_columns]
        if not key_columns:
            raise ValueError(f"Không đủ cột khóa cho MERGE ODS ở bảng {spec.table_name}")

        update_columns = [
            column
            for column in common_columns
            if column not in key_columns and column.lower() not in {"createdat", "created_at", "ngaytao"}
        ]

        on_clause = " AND ".join([f"Target.[{column}] = Source.[{column}]" for column in key_columns])
        update_clause = ",\n                ".join([f"Target.[{column}] = Source.[{column}]" for column in update_columns])
        insert_columns = ", ".join([f"[{column}]" for column in common_columns])
        insert_values = ", ".join([f"Source.[{column}]" for column in common_columns])

        return f"""
            MERGE [{self.facility_schema}].[{spec.table_name}] AS Target
            USING [{self.LANDING_SCHEMA}].[{spec.table_name}] AS Source
                ON {on_clause}
            WHEN MATCHED THEN
                UPDATE SET
                {update_clause}
            WHEN NOT MATCHED BY TARGET THEN
                INSERT ({insert_columns})
                VALUES ({insert_values})
            WHEN NOT MATCHED BY SOURCE
                 AND CAST(Target.[{spec.date_column}] AS DATE) >= CAST('{lookback_date:%Y-%m-%d}' AS DATE)
                 AND CAST(Target.[{spec.date_column}] AS DATE) <= CAST('{to_date:%Y-%m-%d}' AS DATE)
            THEN DELETE;
        """

    def _merge_landing_to_ods(self, connection: pyodbc.Connection, spec: FactTableSpec, lookback_date: date, to_date: date) -> None:
        common_columns = self._get_common_columns(
            connection=connection,
            source_schema=self.LANDING_SCHEMA,
            source_table=spec.table_name,
            target_schema=self.facility_schema,
            target_table=spec.table_name,
        )
        merge_sql = self._build_ods_merge_sql(spec, common_columns, lookback_date, to_date)
        self._log(f"MERGE Landing -> ODS cho {spec.table_name}")
        self.execute_sql_sync(connection, merge_sql)

    def _build_fact_merge_batch_sql(self, lookback_date: date, to_date: date) -> str:
        return f"""
            ;WITH src_full AS (
                SELECT
                    {self.nguon_dulieu_key} AS NguonDuLieuKey,
                    {self.co_so_key} AS CoSoKey,
                    '{self.facility_code}' AS MaCoSo,
                    dv.MaThuPhi,
                    dv.MaPhieuDichVu,
                    dv.MaHoSo,
                    dv.MaChiTieu,
                    CAST({self.nguon_dulieu_key} AS VARCHAR(10)) + ':' + dv.MaChiTieu AS MaChiTieuBK,
                    dv.NgayDenKham,
                    dv.NgayVaoMay AS NgayDoanhThu,
                    ISNULL(
                        CAST(YEAR(dv.NgayVaoMay) * 10000 + MONTH(dv.NgayVaoMay) * 100 + DAY(dv.NgayVaoMay) AS INT),
                        CAST(YEAR(dv.NgayDenKham) * 10000 + MONTH(dv.NgayDenKham) * 100 + DAY(dv.NgayDenKham) AS INT)
                    ) AS DateKey,
                    COALESCE(dv.SoLuongThucHien, dv.SoLuong, 1) AS SoLuongChuan,
                    dv.TongTien AS TongTien,
                    dv.TongTien - ISNULL(tg_agg.TongGiam, 0) + ISNULL(tg_agg.TongTang, 0) AS TongTienSauTangGiam,
                    'DV' AS LoaiHinh,
                    dv.SoHoaDon,
                    dv.DaThucHien,
                    dv.TrangThaiPhieu
                FROM [{self.facility_schema}].[ThuPhiDichVu] dv WITH (NOLOCK)
                LEFT JOIN (
                    SELECT
                        MaHoSo,
                        MaChiTieu,
                        MaPhieuDichVu,
                        SUM(SoTienGiam) AS TongGiam,
                        SUM(SoTienTang) AS TongTang
                    FROM [{self.facility_schema}].[ThuPhiTangGiam] WITH (NOLOCK)
                    WHERE DaDongTien = 1
                      AND CAST(NgayDenKham AS DATE) >= CAST('{lookback_date:%Y-%m-%d}' AS DATE)
                      AND CAST(NgayDenKham AS DATE) <= CAST('{to_date:%Y-%m-%d}' AS DATE)
                    GROUP BY MaHoSo, MaChiTieu, MaPhieuDichVu
                ) tg_agg
                    ON dv.MaHoSo = tg_agg.MaHoSo
                   AND dv.MaChiTieu = tg_agg.MaChiTieu
                   AND dv.MaPhieuDichVu = tg_agg.MaPhieuDichVu
                WHERE dv.DaDongTien = 1
                  AND dv.MaChiTieu IS NOT NULL
                  AND LTRIM(RTRIM(dv.MaChiTieu)) <> ''
                  AND CAST(dv.NgayDenKham AS DATE) >= CAST('{lookback_date:%Y-%m-%d}' AS DATE)
                  AND CAST(dv.NgayDenKham AS DATE) <= CAST('{to_date:%Y-%m-%d}' AS DATE)

                UNION ALL

                SELECT
                    {self.nguon_dulieu_key} AS NguonDuLieuKey,
                    {self.co_so_key} AS CoSoKey,
                    '{self.facility_code}' AS MaCoSo,
                    bh.MaThuPhi,
                    bh.MaPhieuDichVu,
                    bh.MaHoSo,
                    bh.MaChiTieu,
                    CAST({self.nguon_dulieu_key} AS VARCHAR(10)) + ':' + bh.MaChiTieu AS MaChiTieuBK,
                    bh.NgayDenKham,
                    bh.NgayVaoMay AS NgayDoanhThu,
                    ISNULL(
                        CAST(YEAR(bh.NgayVaoMay) * 10000 + MONTH(bh.NgayVaoMay) * 100 + DAY(bh.NgayVaoMay) AS INT),
                        CAST(YEAR(bh.NgayDenKham) * 10000 + MONTH(bh.NgayDenKham) * 100 + DAY(bh.NgayDenKham) AS INT)
                    ) AS DateKey,
                    COALESCE(bh.SoLuongThucHien, bh.SoLuong, 1) AS SoLuongChuan,
                    bh.TongTien AS TongTien,
                    bh.TongTien + ISNULL(bh.TienChenhLech, 0) AS TongTienSauTangGiam,
                    'BH' AS LoaiHinh,
                    bh.SoHoaDon,
                    NULL AS DaThucHien,
                    bh.TrangThaiPhieu
                FROM [{self.facility_schema}].[ThuPhiBaoHiem] bh WITH (NOLOCK)
                WHERE bh.DaDongTien = 1
                  AND bh.MaChiTieu IS NOT NULL
                  AND LTRIM(RTRIM(bh.MaChiTieu)) <> ''
                  AND CAST(bh.NgayDenKham AS DATE) >= CAST('{lookback_date:%Y-%m-%d}' AS DATE)
                  AND CAST(bh.NgayDenKham AS DATE) <= CAST('{to_date:%Y-%m-%d}' AS DATE)
            ),
            src_batch AS (
                SELECT TOP ({self.batch_size}) *
                FROM src_full
                ORDER BY DateKey, MaHoSo, MaChiTieu, MaPhieuDichVu
            )
            MERGE [dm].[FactThuPhiDichVu] AS Target
            USING src_batch AS Source
            ON  Target.NguonDuLieuKey = Source.NguonDuLieuKey
            AND Target.CoSoKey        = Source.CoSoKey
            AND Target.MaHoSo         = Source.MaHoSo
            AND Target.MaChiTieu      = Source.MaChiTieu
            AND Target.MaPhieuDichVu  = Source.MaPhieuDichVu
            WHEN MATCHED THEN
                UPDATE SET
                    Target.TongTien            = Source.TongTien,
                    Target.TongTienSauTangGiam = Source.TongTienSauTangGiam,
                    Target.LoaiHinh            = Source.LoaiHinh,
                    Target.SoHoaDon            = Source.SoHoaDon,
                    Target.SoLuong             = Source.SoLuongChuan,
                    Target.DoanhThu            = ISNULL(CAST(Source.TongTienSauTangGiam AS FLOAT), 0),
                    Target.DaThucHien          = Source.DaThucHien,
                    Target.TrangThaiPhieu      = Source.TrangThaiPhieu,
                    Target.NgayDenKham         = Source.NgayDenKham
            WHEN NOT MATCHED BY TARGET THEN
                INSERT (
                    NguonDuLieuKey,
                    CoSoKey,
                    DateKey,
                    LuotKhamKey,
                    BenhNhanKey,
                    DichVuKey,
                    MaCoSo,
                    MaThuPhi,
                    MaPhieuDichVu,
                    MaHoSo,
                    MaChiTieu,
                    MaChiTieuBK,
                    NgayDenKham,
                    SoLuong,
                    TongTien,
                    TongTienSauTangGiam,
                    LoaiHinh,
                    SoHoaDon,
                    DoanhThu,
                    DaThucHien,
                    TrangThaiPhieu
                )
                VALUES (
                    Source.NguonDuLieuKey,
                    Source.CoSoKey,
                    Source.DateKey,
                    ISNULL((
                        SELECT TOP 1 lk.LuotKhamKey
                        FROM dm.DimLuotKham lk WITH (NOLOCK)
                        WHERE lk.NguonDuLieuKey = Source.NguonDuLieuKey
                          AND lk.MaHoSo = Source.MaHoSo
                    ), -1),
                    ISNULL((
                        SELECT TOP 1 lk.BenhNhanKey
                        FROM dm.DimLuotKham lk WITH (NOLOCK)
                        WHERE lk.NguonDuLieuKey = Source.NguonDuLieuKey
                          AND lk.MaHoSo = Source.MaHoSo
                    ), -1),
                    ISNULL((
                        SELECT TOP 1 dv2.DichVuKey
                        FROM dm.DimDichVu dv2 WITH (NOLOCK)
                        WHERE dv2.MaChiTieuBK = Source.MaChiTieuBK
                    ), ISNULL((
                        SELECT TOP 1 dv3.DichVuKey
                        FROM dm.DimDichVu dv3 WITH (NOLOCK)
                        WHERE dv3.NguonDuLieuKey = Source.NguonDuLieuKey
                          AND dv3.MaChiTieu = Source.MaChiTieu
                    ), -1)),
                    Source.MaCoSo,
                    Source.MaThuPhi,
                    Source.MaPhieuDichVu,
                    Source.MaHoSo,
                    Source.MaChiTieu,
                    Source.MaChiTieuBK,
                    Source.NgayDenKham,
                    Source.SoLuongChuan,
                    Source.TongTien,
                    Source.TongTienSauTangGiam,
                    Source.LoaiHinh,
                    Source.SoHoaDon,
                    ISNULL(CAST(Source.TongTienSauTangGiam AS FLOAT), 0),
                    Source.DaThucHien,
                    Source.TrangThaiPhieu
                )
            WHEN NOT MATCHED BY SOURCE
                 AND CAST(Target.NgayDenKham AS DATE) >= CAST('{lookback_date:%Y-%m-%d}' AS DATE)
                 AND CAST(Target.NgayDenKham AS DATE) <= CAST('{to_date:%Y-%m-%d}' AS DATE)
                 AND Target.NguonDuLieuKey = {self.nguon_dulieu_key}
                 AND Target.MaCoSo = '{self.facility_code}'
            THEN DELETE;

            SELECT @@ROWCOUNT AS MergeAffectedRows;
        """

    def _merge_ods_to_datamart_batches(self, connection: pyodbc.Connection, lookback_date: date, to_date: date) -> None:
        self._log(
            "MERGE ODS -> Datamart theo batch TOP "
            f"{self.batch_size} cho khoảng {lookback_date} -> {to_date}"
        )

        max_loops = 500
        for loop_idx in range(1, max_loops + 1):
            sql = self._prepend_nocount(self._build_fact_merge_batch_sql(lookback_date, to_date))
            cursor = connection.cursor()
            cursor.execute(sql)
            row = cursor.fetchone()
            affected = int(row[0]) if row and row[0] is not None else 0
            self._log(f"Batch {loop_idx}: affected = {affected}")

            if affected == 0:
                break
            if affected < self.batch_size:
                break
        else:
            raise RuntimeError("Vượt quá số vòng lặp batch tối đa khi MERGE FactThuPhiDichVu")

    def _execute_core(self, connection: pyodbc.Connection, *args: Any, **kwargs: Any) -> None:
        from_date_input = args[0] if len(args) > 0 else kwargs.get("from_date")
        to_date_input = args[1] if len(args) > 1 else kwargs.get("to_date")

        today = date.today()
        to_date = self._normalize_date(to_date_input, fallback=today)
        lookback_date = to_date - timedelta(days=self.lookback_days)
        _from_date = self._normalize_date(from_date_input, fallback=lookback_date)

        self._log(
            f"Luồng incremental Fact theo Lookback D-{self.lookback_days}. "
            f"to_date={to_date}, lookback_date={lookback_date}, from_date_input={_from_date}"
        )

        try:
            self._log("Dọn Landing đầu luồng")
            self._landing_cleanup(connection)

            for spec in self.FACT_SPECS:
                self._copy_delta_prod_to_landing(connection, spec, lookback_date, to_date)
                self._merge_landing_to_ods(connection, spec, lookback_date, to_date)

            self._merge_ods_to_datamart_batches(connection, lookback_date, to_date)
        finally:
            self._log("Dọn Landing cuối luồng")
            self._landing_cleanup(connection)
```

### SOURCE: src/jobs/sync_orchestrator.py
```py
from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from datetime import date

from dotenv import load_dotenv

from src.jobs.dimension_loader import DimensionLoader
from src.jobs.fact_loader import FactLoader


@dataclass(frozen=True)
class FacilityDefinition:
    code: str
    prod_env_key: str
    schema_name: str
    nguon_dulieu_env_key: str
    co_so_env_key: str
    default_nguon_dulieu_key: int
    default_co_so_key: int


class SyncOrchestrator:
    def __init__(
        self,
        datamart_env_key: str = "DATAMART_CONNECTION_STRING",
        active_facilities_env_key: str = "ACTIVE_FACILITIES",
    ) -> None:
        load_dotenv("config/.env", override=False)
        self.datamart_env_key = datamart_env_key
        self.active_facilities_env_key = active_facilities_env_key

        self.facility_registry: dict[str, FacilityDefinition] = {
            "hanoi": FacilityDefinition(
                code="hanoi",
                prod_env_key="PROD_CONNECTION_HANOI",
                schema_name="hanoi_hisnano_v2",
                nguon_dulieu_env_key="NGUON_DULIEU_KEY_HANOI",
                co_so_env_key="CO_SO_KEY_HANOI",
                default_nguon_dulieu_key=2,
                default_co_so_key=1,
            ),
            "hcm": FacilityDefinition(
                code="hcm",
                prod_env_key="PROD_CONNECTION_HCM",
                schema_name="hcm_hisnano_v2",
                nguon_dulieu_env_key="NGUON_DULIEU_KEY_HCM",
                co_so_env_key="CO_SO_KEY_HCM",
                default_nguon_dulieu_key=3,
                default_co_so_key=2,
            ),
            "halong": FacilityDefinition(
                code="halong",
                prod_env_key="PROD_CONNECTION_HALONG",
                schema_name="halong_hisnano_v2",
                nguon_dulieu_env_key="NGUON_DULIEU_KEY_HALONG",
                co_so_env_key="CO_SO_KEY_HALONG",
                default_nguon_dulieu_key=4,
                default_co_so_key=3,
            ),
            "haiphong": FacilityDefinition(
                code="haiphong",
                prod_env_key="PROD_CONNECTION_HAIPHONG",
                schema_name="haiphong_hisnano_v2",
                nguon_dulieu_env_key="NGUON_DULIEU_KEY_HAIPHONG",
                co_so_env_key="CO_SO_KEY_HAIPHONG",
                default_nguon_dulieu_key=5,
                default_co_so_key=4,
            ),
        }

    @staticmethod
    def _parse_facility_tokens(raw_value: str) -> list[str]:
        return [token.strip().lower() for token in raw_value.split(",") if token.strip()]

    def _resolve_target_facilities(self, target_facilities: list[str] | None = None) -> list[str]:
        if target_facilities is not None:
            normalized = [facility.strip().lower() for facility in target_facilities if facility.strip()]
            if not normalized or "all" in normalized:
                return list(self.facility_registry.keys())
            return normalized

        env_value = os.getenv(self.active_facilities_env_key, "ALL").strip()
        if not env_value or env_value.upper() == "ALL":
            return list(self.facility_registry.keys())
        return self._parse_facility_tokens(env_value)

    def _validate_target_facilities(self, facilities: list[str]) -> None:
        unknown = [facility for facility in facilities if facility not in self.facility_registry]
        if unknown:
            valid = ", ".join(self.facility_registry.keys())
            raise ValueError(f"Facility không hợp lệ: {unknown}. Danh sách hợp lệ: {valid}")

    def _resolve_facility_key(self, env_key: str, fallback: int) -> int:
        raw = os.getenv(env_key, "").strip()
        if not raw:
            return fallback
        try:
            return int(raw)
        except ValueError as exc:
            raise ValueError(f"Biến {env_key} phải là số nguyên, đang nhận '{raw}'") from exc

    def _build_dimension_loader(
        self,
        datamart_connection: str,
        production_connection: str,
        facility: FacilityDefinition,
        nguon_dulieu_key: int,
        co_so_key: int,
    ) -> DimensionLoader:
        return DimensionLoader(
            datamart_connection=datamart_connection,
            production_connection=production_connection,
            facility_code=facility.code,
            facility_schema=facility.schema_name,
            nguon_dulieu_key=nguon_dulieu_key,
            co_so_key=co_so_key,
        )

    def _build_fact_loader(
        self,
        datamart_connection: str,
        production_connection: str,
        facility: FacilityDefinition,
        nguon_dulieu_key: int,
        co_so_key: int,
    ) -> FactLoader:
        return FactLoader(
            datamart_connection=datamart_connection,
            production_connection=production_connection,
            facility_code=facility.code,
            facility_schema=facility.schema_name,
            nguon_dulieu_key=nguon_dulieu_key,
            co_so_key=co_so_key,
        )

    def run(
        self,
        target_facilities: list[str] | None = None,
        run_dimension: bool = True,
        run_fact: bool = True,
        to_date: date | None = None,
    ) -> None:
        if not run_dimension and not run_fact:
            raise ValueError("Cần bật ít nhất một luồng: run_dimension hoặc run_fact")

        datamart_connection = os.getenv(self.datamart_env_key, "").strip()
        if not datamart_connection:
            raise ValueError(f"Thiếu biến môi trường {self.datamart_env_key}")

        selected_facilities = self._resolve_target_facilities(target_facilities)
        self._validate_target_facilities(selected_facilities)

        effective_to_date = to_date or date.today()
        print(f"[SyncOrchestrator] Danh sách facility cần chạy: {selected_facilities}")

        for facility_code in selected_facilities:
            facility = self.facility_registry[facility_code]
            production_connection = os.getenv(facility.prod_env_key, "").strip()
            if not production_connection:
                print(f"[SyncOrchestrator] Bỏ qua {facility.code} vì thiếu {facility.prod_env_key}")
                continue

            nguon_dulieu_key = self._resolve_facility_key(
                facility.nguon_dulieu_env_key,
                facility.default_nguon_dulieu_key,
            )
            co_so_key = self._resolve_facility_key(
                facility.co_so_env_key,
                facility.default_co_so_key,
            )

            print(f"[SyncOrchestrator] Bắt đầu facility={facility.code}")
            try:
                if run_dimension:
                    dimension_loader = self._build_dimension_loader(
                        datamart_connection=datamart_connection,
                        production_connection=production_connection,
                        facility=facility,
                        nguon_dulieu_key=nguon_dulieu_key,
                        co_so_key=co_so_key,
                    )
                    dimension_loader.execute_load(to_date=effective_to_date)

                if run_fact:
                    fact_loader = self._build_fact_loader(
                        datamart_connection=datamart_connection,
                        production_connection=production_connection,
                        facility=facility,
                        nguon_dulieu_key=nguon_dulieu_key,
                        co_so_key=co_so_key,
                    )
                    fact_loader.execute_load(to_date=effective_to_date)

                print(f"[SyncOrchestrator] Hoàn tất facility={facility.code}")
            except Exception:
                print(f"[SyncOrchestrator] Lỗi tại facility={facility.code}, dừng luồng tuần tự")
                raise


def _parse_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chạy đồng bộ ETL tuần tự theo facility")
    parser.add_argument(
        "--facilities",
        type=str,
        default="ALL",
        help="Danh sách facility phân tách bởi dấu phẩy, ví dụ: hanoi,hcm hoặc ALL",
    )
    parser.add_argument(
        "--only",
        type=str,
        choices=["dimension", "fact", "all"],
        default="all",
        help="Giới hạn luồng chạy",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_cli_args()
    orchestrator = SyncOrchestrator()

    run_dimension = args.only in {"dimension", "all"}
    run_fact = args.only in {"fact", "all"}
    target_facilities = None if args.facilities.upper() == "ALL" else [token.strip() for token in args.facilities.split(",")]

    orchestrator.run(
        target_facilities=target_facilities,
        run_dimension=run_dimension,
        run_fact=run_fact,
    )
```
