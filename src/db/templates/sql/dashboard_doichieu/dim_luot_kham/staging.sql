SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT
    COUNT(1) AS [RowCount]
FROM {staging_schema}.HoSoKhamBenhNgoaiTru WITH (NOLOCK)
WHERE NgayVaoKham >= @TuNgay AND NgayVaoKham < DATEADD(DAY, 1, @DenNgay);
