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
