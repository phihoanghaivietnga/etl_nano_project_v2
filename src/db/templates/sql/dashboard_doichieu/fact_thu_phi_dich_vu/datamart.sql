SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT
    SUM(ISNULL(TongTienSauTangGiam, TongTien)) AS TotalRevenue
FROM dm.FactThuPhiDichVu WITH (NOLOCK)
WHERE CAST(NgayDenKham AS DATE) BETWEEN @TuNgay AND @DenNgay;
