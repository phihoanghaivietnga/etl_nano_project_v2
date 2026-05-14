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