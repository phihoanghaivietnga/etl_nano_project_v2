SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT
    COUNT(1) AS [RowCount]
FROM dm.DimLuotKham WITH (NOLOCK)
WHERE NgayVaoKham >= @TuNgay AND NgayVaoKham < DATEADD(DAY, 1, @DenNgay);
