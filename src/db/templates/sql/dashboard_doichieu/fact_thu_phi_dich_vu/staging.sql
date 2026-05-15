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
				  AND CAST(NgayDenKham AS DATE) <= DATEADD(DAY, 1, @DenNgay)
				GROUP BY MaHoSo, MaChiTieu, MaPhieuDichVu) b on a.MaHoSo = b.MaHoSo and a.MaChiTieu = b.MaChiTieu and a.MaPhieuDichVu = b.MaPhieuDichVu
	where a.NgayDenKham >= @TuNgay and a.ngaydenkham < @DenNgay
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
