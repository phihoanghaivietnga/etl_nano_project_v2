--
-- FILE: DimLoaiGoiDichVu_merge.sql
-- AUTHOR: Claude Sonnet 4.6 (Builder)
-- CREATED: 2026-04-17
-- MODIFIED: 2026-04-17
-- VERSION: 1.1.0
-- PURPOSE: Template MERGE DimLoaiGoiDichVu tu staging sang dm.
-- HISTORY:
--     - v1.0.0 [2026-04-17]: Tao moi — dong bo LoaiGoiDichVuNT
--     - v1.1.0 [2026-04-17]: Fix mapping — them MaLoaiGoi (goc),
--                             CONCAT cho MaLoaiGoiBK, them MaCoSo vao INSERT/UPDATE
--                             (chi thi 20260417_1750)
--


MERGE [{dm_schema}].[DimLoaiGoiDichVu] AS Target
USING (
    SELECT
        {co_so_key}        AS CoSoKey,
        {nguon_dulieu_key} AS NguonDuLieuKey,
        '{ma_co_so}'       AS MaCoSo,
        s.MaLoaiGoi        AS MaLoaiGoi,
        -- Khoi tao MaLoaiGoiBK theo dinh dang NguonDuLieuKey:MaLoaiGoi
        CONCAT(CAST({nguon_dulieu_key} AS VARCHAR), ':', s.MaLoaiGoi) AS MaLoaiGoiBK,
        s.TenLoaiGoi
    FROM [{staging_schema}].[LoaiGoiDichVuNT] s WITH (NOLOCK)
) AS Source
ON Target.NguonDuLieuKey = Source.NguonDuLieuKey
   AND Target.MaLoaiGoiBK = Source.MaLoaiGoiBK
WHEN MATCHED THEN
    UPDATE SET
        Target.TenLoaiGoi = Source.TenLoaiGoi,
        Target.MaCoSo = Source.MaCoSo,
        Target.NgayDongBo = GETDATE()
WHEN NOT MATCHED BY TARGET THEN
    INSERT (MaLoaiGoi, CoSoKey, NguonDuLieuKey, MaCoSo, MaLoaiGoiBK, TenLoaiGoi, NgayDongBo)
    VALUES (Source.MaLoaiGoi, Source.CoSoKey, Source.NguonDuLieuKey, Source.MaCoSo, Source.MaLoaiGoiBK, Source.TenLoaiGoi, GETDATE());
