-- =============================================================================
-- FILE: DimBenh_merge.sql
-- SOURCE: src/auto_runner/loader.py::_merge_dimbenh_direct
-- PURPOSE: MERGE [{staging_schema}].[DMBenh] -> [{dm_schema}].[DimBenh]
-- NOTE:
--   - Script da duoc chuyen truc tiep tu logic MERGE trong Auto Loader.
--   - BK su dung separator ':' theo logic hien tai.
-- =============================================================================

MERGE INTO [{dm_schema}].[DimBenh] AS target
USING (
    SELECT
        b.NguonDuLieuKey,
        b.CoSoKey,
        b.MaCoSo,
        b.MaBenh,
        b.TenBenhTiengViet,
        b.TenBenhTiengAnh,
        b.GhiChu,
        b.MaNhomBenh
    FROM [{staging_schema}].[DMBenh] b WITH (NOLOCK)
) src
ON target.MaBenhBK = CAST(src.NguonDuLieuKey AS VARCHAR(10)) + ':' + src.MaBenh
WHEN MATCHED THEN
    UPDATE SET
        target.NguonDuLieuKey    = src.NguonDuLieuKey,
        target.CoSoKey           = src.CoSoKey,
        target.MaCoSo            = src.MaCoSo,
        target.TenBenhTiengViet  = src.TenBenhTiengViet,
        target.TenBenhTiengAnh   = src.TenBenhTiengAnh,
        target.GhiChu            = src.GhiChu,
        target.MaNhomBenh        = src.MaNhomBenh,
        target.NgayCapNhat       = GETDATE()
WHEN NOT MATCHED THEN
    INSERT (
        NguonDuLieuKey, CoSoKey, MaCoSo,
        MaBenh,
        TenBenhTiengViet, TenBenhTiengAnh,
        GhiChu, MaNhomBenh,
        NgayTao
    )
    VALUES (
        src.NguonDuLieuKey, src.CoSoKey, src.MaCoSo,
        src.MaBenh,
        src.TenBenhTiengViet, src.TenBenhTiengAnh,
        src.GhiChu, src.MaNhomBenh,
        GETDATE()
    );
