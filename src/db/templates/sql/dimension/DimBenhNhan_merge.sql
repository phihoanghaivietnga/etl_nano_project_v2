--
-- FILE: DimBenhNhan_merge.sql
-- AUTHOR: GitHub Copilot
-- CREATED: 2026-03-14
-- MODIFIED: 2026-03-14
-- VERSION: 1.0.0
-- PURPOSE: Template MERGE DimBenhNhan tu staging sang dm voi enrichment.
-- HISTORY:
--     - v1.0.0 [2026-03-14]: Tao moi template tu bulk_loader va schema cu
--

DECLARE @NguonDuLieuKey INT = {nguon_dulieu_key};
DECLARE @MaCoSo        VARCHAR(50) = '{ma_co_so}';
DECLARE @CoSoKey       INT = {co_so_key};

;WITH Src AS (
    SELECT
        @NguonDuLieuKey AS NguonDuLieuKey,
        @MaCoSo         AS MaCoSo,
        CAST(bn.MaBenhNhan AS VARCHAR(50)) AS MaBenhNhan,
        bn.TenBenhNhan         AS HoTenRaw,
        bn.DiaChiBenhNhan      AS DiaChiRaw,
        bn.NgayThang + '/' + CAST(bn.NamSinh AS VARCHAR) AS NgaySinhRaw,
        bn.NamSinh             AS NamSinhRaw,
        REPLACE(bn.SoDienThoai, '***',dbo.Decode_Hex(bn.SoDienThoaiEnabled)) As SoDienThoaiRaw,
        -- bn.SoDienThoai         AS SoDienThoaiRaw,
        bn.MaTinhThanh         AS MaTinhThanhRaw,
        dmTinh.TenTinhThanh    AS TinhThanhRaw,
        bn.MaXa                AS MaXaPhuongRaw,
        dmPhuong.TenXa         AS XaPhuongRaw,
        CASE
            WHEN LTRIM(RTRIM(bn.MaGioiTinh)) = '0' THEN 'NAM'
            WHEN LTRIM(RTRIM(bn.MaGioiTinh)) = '1' THEN 'NU'
            ELSE 'KXD'
        END AS MaGioiTinhChuan,
        bn.sysdate AS SysDateNguon,
        CAST(COALESCE(
            TRY_CONVERT(DATE, (bn.NgayThang + '/' + CAST(bn.NamSinh AS VARCHAR)), 103),
            TRY_CONVERT(DATE, (bn.NgayThang + '/' + CAST(bn.NamSinh AS VARCHAR)), 120)
        ) AS DATE) AS NgaySinhChuan,
        bn.NamSinh AS NamSinhChuan
    FROM [{staging_schema}].[DMBenhNhan] bn WITH (NOLOCK)
    LEFT JOIN [{staging_schema}].[DMTinhThanh] dmTinh
        ON bn.MaTinhThanh = dmTinh.MaTinhThanh
    LEFT JOIN [{staging_schema}].[DMXaPhuong] dmPhuong
        ON bn.MaXa = dmPhuong.MaXa
),
Enriched AS (
    SELECT
        s.*,        
        COALESCE(dcs.CoSoKey, @CoSoKey) AS CoSoKey,
        dc_tinh.MaChuan  AS MaTinhThanhChuan,
        dc_tinh.TenChuan AS TinhThanhChuan,
        NULL             AS MaPhuongChuan,
        NULL             AS PhuongChuan,
        gt.GioiTinhKey,
        gt.MaGioiTinh    AS MaGioiTinhRef,
        gt.TenGioiTinh,
        C.SoDienThoaiChuan20 AS SoDienThoaiChuan,
        C.DQ_SDT_QuaDai
    FROM Src s
    LEFT JOIN [{dm_schema}].[DimCoSo] dcs
        ON dcs.MaCoSo = s.MaCoSo
    LEFT JOIN [ref].[MapDiaLy] m_tinh
        ON  m_tinh.NguonDuLieuKey = s.NguonDuLieuKey
        AND m_tinh.CoSoKey = COALESCE(dcs.CoSoKey, @CoSoKey)
        AND m_tinh.Cap     = 'TINH'
        AND m_tinh.MaNguon = s.MaTinhThanhRaw
    LEFT JOIN [ref].[DiaLyChuan] dc_tinh
        ON dc_tinh.DiaLyChuanKey = m_tinh.DiaLyChuanKey
    LEFT JOIN [ref].[GioiTinh] gt
        ON gt.MaGioiTinh = s.MaGioiTinhChuan
    CROSS APPLY (
        SELECT REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
            LTRIM(RTRIM(ISNULL(s.SoDienThoaiRaw, N''))),
            '/',''),'-',''),' ',''),'.',''),'+','') AS sdt0
    ) A
    CROSS APPLY (
        SELECT CASE
            WHEN LEFT(A.sdt0, 2) = '84' THEN '0' + SUBSTRING(A.sdt0, 3, 200)
            ELSE A.sdt0
        END AS sdt1
    ) B
    CROSS APPLY (
        SELECT
            CASE WHEN LEN(B.sdt1) > 20 THEN 1 ELSE 0 END AS DQ_SDT_QuaDai,
            LEFT(B.sdt1, 20) AS SoDienThoaiChuan20
    ) C
)
MERGE [{dm_schema}].[DimBenhNhan] AS tgt
USING (
    SELECT
        e.NguonDuLieuKey,
        e.CoSoKey,
        e.MaCoSo,
        e.MaBenhNhan,
        CAST(e.NguonDuLieuKey AS VARCHAR(10)) + ':' + CAST(e.MaBenhNhan AS VARCHAR(50)) AS MaBenhNhanBK,
        e.HoTenRaw,
        e.DiaChiRaw,
        e.NgaySinhRaw,
        e.NamSinhRaw,
        e.SoDienThoaiRaw,
        e.MaTinhThanhRaw,
        e.TinhThanhRaw,
        e.MaXaPhuongRaw AS MaXaPhuongRaw,
        e.XaPhuongRaw   AS PhuongRaw,
        e.HoTenRaw      AS HoTenChuan,
        e.DiaChiRaw     AS DiaChiChuan,
        e.NgaySinhChuan,
        e.NamSinhChuan,
        e.MaTinhThanhChuan,
        e.TinhThanhChuan,
        e.MaPhuongChuan,
        e.PhuongChuan,
        e.SoDienThoaiChuan,
        e.GioiTinhKey,
        e.MaGioiTinhRef AS MaGioiTinhChuan,
        e.SysDateNguon,
        CASE WHEN NULLIF(LTRIM(RTRIM(e.HoTenRaw)), '') IS NULL THEN 0 ELSE 1 END
            AS DQ_HoTenHopLe,
        CASE WHEN NULLIF(LTRIM(RTRIM(e.DiaChiRaw)), '') IS NULL THEN 0 ELSE 1 END
            AS DQ_DiaChiHopLe,
        CASE WHEN e.NgaySinhChuan IS NULL AND e.NamSinhChuan IS NULL THEN 0 ELSE 1 END
            AS DQ_NgaySinhHopLe,
        CASE WHEN e.TinhThanhChuan IS NULL THEN 0 ELSE 1 END
            AS DQ_TinhThanhHopLe,
        CASE WHEN e.PhuongChuan IS NULL THEN 0 ELSE 1 END
            AS DQ_PhuongHopLe,
        CASE
            WHEN e.SoDienThoaiChuan IS NULL OR e.SoDienThoaiChuan = '' THEN 0
            WHEN e.SoDienThoaiChuan LIKE '%[^0-9]%'                    THEN 0
            WHEN LEN(e.SoDienThoaiChuan) < 9                           THEN 0
            WHEN e.DQ_SDT_QuaDai = 1                                   THEN 0
            ELSE 1
        END AS DQ_SoDienThoaiHopLe,
        CASE
            WHEN e.DQ_SDT_QuaDai = 1
                THEN N'SDT > 20 ky tu: da cat 20 ky tu de luu, can kiem tra'
            WHEN e.TinhThanhChuan IS NULL OR e.PhuongChuan IS NULL
                THEN N'Chua map du dia ly (TINH/XA) qua ref.MapDiaLy'
            WHEN e.GioiTinhKey IS NULL
                THEN N'Chua map duoc gioi tinh ve ref.GioiTinh (NAM/NU/KXD)'
            ELSE NULL
        END AS DQ_GhiChu
    FROM Enriched e
) AS src
ON tgt.MaBenhNhanBK = src.MaBenhNhanBK
WHEN MATCHED THEN
    UPDATE SET
        tgt.NguonDuLieuKey      = src.NguonDuLieuKey,
        tgt.CoSoKey             = src.CoSoKey,
        tgt.MaCoSo              = src.MaCoSo,
        tgt.HoTenRaw            = src.HoTenRaw,
        tgt.DiaChiRaw           = src.DiaChiRaw,
        tgt.NgaySinhRaw         = src.NgaySinhRaw,
        tgt.NamSinhRaw          = src.NamSinhRaw,
        tgt.SoDienThoaiRaw      = src.SoDienThoaiRaw,
        tgt.MaTinhThanhRaw      = src.MaTinhThanhRaw,
        tgt.TinhThanhRaw        = src.TinhThanhRaw,
        tgt.MaPhuongRaw         = src.MaXaPhuongRaw,
        tgt.PhuongRaw           = src.PhuongRaw,
        tgt.HoTenChuan          = src.HoTenChuan,
        tgt.DiaChiChuan         = src.DiaChiChuan,
        tgt.NgaySinhChuan       = src.NgaySinhChuan,
        tgt.NamSinhChuan        = src.NamSinhChuan,
        tgt.MaTinhThanhChuan    = src.MaTinhThanhChuan,
        tgt.TinhThanhChuan      = src.TinhThanhChuan,
        tgt.MaPhuongChuan       = src.MaPhuongChuan,
        tgt.PhuongChuan         = src.PhuongChuan,
        tgt.SoDienThoaiChuan    = src.SoDienThoaiChuan,
        tgt.GioiTinhKey         = src.GioiTinhKey,
        tgt.MaGioiTinhChuan     = src.MaGioiTinhChuan,
        tgt.DQ_HoTenHopLe       = src.DQ_HoTenHopLe,
        tgt.DQ_DiaChiHopLe      = src.DQ_DiaChiHopLe,
        tgt.DQ_NgaySinhHopLe    = src.DQ_NgaySinhHopLe,
        tgt.DQ_TinhThanhHopLe   = src.DQ_TinhThanhHopLe,
        tgt.DQ_PhuongHopLe      = src.DQ_PhuongHopLe,
        tgt.DQ_SoDienThoaiHopLe = src.DQ_SoDienThoaiHopLe,
        tgt.DQ_GhiChu           = src.DQ_GhiChu,
        tgt.SysDateNguon        = src.SysDateNguon,
        tgt.NgayCapNhat         = GETDATE()
WHEN NOT MATCHED THEN
    INSERT (
        NguonDuLieuKey, CoSoKey, MaCoSo,
        MaBenhNhan, MaBenhNhanBK,
        HoTenRaw, DiaChiRaw, NgaySinhRaw, NamSinhRaw,
        MaTinhThanhRaw, TinhThanhRaw, MaPhuongRaw, PhuongRaw, SoDienThoaiRaw,
        HoTenChuan, DiaChiChuan, NgaySinhChuan, NamSinhChuan,
        MaTinhThanhChuan, TinhThanhChuan, MaPhuongChuan, PhuongChuan, SoDienThoaiChuan,
        GioiTinhKey, MaGioiTinhChuan,
        DQ_HoTenHopLe, DQ_DiaChiHopLe, DQ_NgaySinhHopLe, DQ_TinhThanhHopLe,
        DQ_PhuongHopLe, DQ_SoDienThoaiHopLe, DQ_GhiChu,
        SysDateNguon
    )
    VALUES (
        src.NguonDuLieuKey, src.CoSoKey, src.MaCoSo,
        src.MaBenhNhan, src.MaBenhNhanBK,
        src.HoTenRaw, src.DiaChiRaw, src.NgaySinhRaw, src.NamSinhRaw,
        src.MaTinhThanhRaw, src.TinhThanhRaw, src.MaXaPhuongRaw, src.PhuongRaw, src.SoDienThoaiRaw,
        src.HoTenChuan, src.DiaChiChuan, src.NgaySinhChuan, src.NamSinhChuan,
        src.MaTinhThanhChuan, src.TinhThanhChuan, src.MaPhuongChuan, src.PhuongChuan, src.SoDienThoaiChuan,
        src.GioiTinhKey, src.MaGioiTinhChuan,
        src.DQ_HoTenHopLe, src.DQ_DiaChiHopLe, src.DQ_NgaySinhHopLe, src.DQ_TinhThanhHopLe,
        src.DQ_PhuongHopLe, src.DQ_SoDienThoaiHopLe, src.DQ_GhiChu,
        src.SysDateNguon
    );
