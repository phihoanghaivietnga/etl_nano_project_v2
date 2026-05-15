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
