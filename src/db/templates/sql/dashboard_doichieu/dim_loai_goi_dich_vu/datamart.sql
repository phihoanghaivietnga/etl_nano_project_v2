SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount] 
FROM dm.DimLoaiGoiDichVu WITH (NOLOCK)
WHERE NguonDuLieuKey = 2;
