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
