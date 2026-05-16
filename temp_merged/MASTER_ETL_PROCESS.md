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
