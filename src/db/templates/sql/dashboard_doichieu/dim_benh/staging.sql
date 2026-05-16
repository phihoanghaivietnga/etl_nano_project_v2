SET NOCOUNT ON;

DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM {staging_schema}.DMBenh WITH (NOLOCK);
