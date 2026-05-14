--
-- FILE: FactThuPhiDichVu_ThuPhiGoi_merge.sql
-- AUTHOR: Claude Sonnet 4.6 (Builder)
-- CREATED: 2026-04-17
-- MODIFIED: 2026-04-17
-- VERSION: 1.0.0
-- PURPOSE: Template MERGE ThuPhiGoi vao dm.FactThuPhiDichVu voi LoaiHinh='TPG'.
--          Mapping: MaPhieuThu -> MaPhieuDichVu, TongTien, ThanhTien -> TongTienSauTangGiam.
-- HISTORY:
--     - v1.0.0 [2026-04-17]: Tao moi — dong bo ThuPhiGoi (LoaiHinh=TPG)
--

MERGE [{dm_schema}].[FactThuPhiDichVu] AS Target
USING (
    SELECT
        {co_so_key}        AS CoSoKey,
        {nguon_dulieu_key} AS NguonDuLieuKey,
        '{ma_co_so}' AS MaCoSo,
        s.MaHoSo,
        s.MaPhieuThu       AS MaPhieuDichVu,
        'TPG'              AS LoaiHinh,
        s.TongTien,
        s.ThanhTien        AS TongTienSauTangGiam,
        s.NgayThu          AS NgayDenKham,
        s.MaLoaiGoi        AS MaChiTieu,
        ISNULL(
            CAST(YEAR(s.NgayThu) * 10000
                 + MONTH(s.NgayThu) * 100
                 + DAY(s.NgayThu) AS INT),
            CAST(YEAR(s.NgayThu) * 10000
                 + MONTH(s.NgayThu) * 100
                 + DAY(s.NgayThu) AS INT)
        ) AS DateKey,
        CAST({nguon_dulieu_key} AS VARCHAR(10)) + ':' + s.MaLoaiGoi AS MaChiTieuBK,
        s.MaPhieuThu       AS SoHoaDon,
        NEWID() AS MaThuPhi,
        0 AS SoLuong,
        NULL AS DoanhThu,
        NULL AS DaThucHien,
        NULL AS TrangThaiPhieu
    FROM [{staging_schema}].[ThuPhiGoi] s WITH (NOLOCK)
    WHERE s.NgayThu IS NOT NULL AND s.MaPhieuThu IS NOT NULL
        AND CAST(s.NgayThu AS DATE) >= CAST('{date_from}' AS DATE)
        AND CAST(s.NgayThu AS DATE) <= CAST('{date_to}' AS DATE)
) AS Source
ON Target.NguonDuLieuKey = Source.NguonDuLieuKey
   AND Target.MaHoSo = Source.MaHoSo
   AND Target.MaPhieuDichVu = Source.MaPhieuDichVu
   AND Target.LoaiHinh = 'TPG'
WHEN MATCHED THEN
    UPDATE SET
        Target.TongTien = Source.TongTien,
        Target.TongTienSauTangGiam = Source.TongTienSauTangGiam,
        Target.NgayDenKham = Source.NgayDenKham
WHEN NOT MATCHED BY TARGET THEN
    /*
    INSERT (CoSoKey, NguonDuLieuKey, MaCoSo, MaHoSo, MaPhieuDichVu,
            LoaiHinh, TongTien, TongTienSauTangGiam, NgayDenKham, MaChiTieu, MaChiTieuBK, DateKey)
    VALUES (Source.CoSoKey, Source.NguonDuLieuKey, Source.MaCoSo,
            Source.MaHoSo, Source.MaPhieuDichVu, Source.LoaiHinh,
            Source.TongTien, Source.TongTienSauTangGiam, Source.NgayDenKham, 
            Source.MaChiTieu, Source.MaChiTieuBK, Source.DateKey);
    */
     INSERT (
        NguonDuLieuKey,
        CoSoKey,
        DateKey,
        LuotKhamKey,
        BenhNhanKey,
        DichVuKey,
        MaCoSo,
        MaThuPhi,
        MaPhieuDichVu,
        MaHoSo,
        MaChiTieu,
        MaChiTieuBK,
        NgayDenKham,
        SoLuong,
        TongTien,
        TongTienSauTangGiam,
        LoaiHinh,
        SoHoaDon,
        DoanhThu,
        DaThucHien,
        TrangThaiPhieu
    )
    VALUES (
        source.NguonDuLieuKey,
        source.CoSoKey,
        -- DateKey: YYYYMMDD
        source.DateKey,
        -- LuotKhamKey: lookup từ dm.DimLuotKham theo MaHoSo + NguonDuLieuKey
        ISNULL((
            SELECT TOP 1 lk.LuotKhamKey
            FROM dm.DimLuotKham lk WITH (NOLOCK)
            WHERE lk.NguonDuLieuKey = source.NguonDuLieuKey
              AND lk.MaHoSo         = source.MaHoSo
        ), 0),

        -- BenhNhanKey: lookup từ dm.DimLuotKham (nullable)
        (
            SELECT TOP 1 lk.BenhNhanKey
            FROM dm.DimLuotKham lk WITH (NOLOCK)
            WHERE lk.NguonDuLieuKey = source.NguonDuLieuKey
              AND lk.MaHoSo         = source.MaHoSo
        ),
        -- FIX v1.7.0: DichVuKey - lookup qua MaChiTieuBK (Business Key bat bien)
        -- Neu DimDichVu chua co MaChiTieuBK, fallback ve lookup qua MaChiTieu
        ISNULL((
            SELECT TOP 1 dv2.DichVuKey
            FROM dm.DimDichVu dv2 WITH (NOLOCK)
            WHERE dv2.MaChiTieuBK = source.MaChiTieuBK
        ), ISNULL((
            SELECT TOP 1 dv3.DichVuKey
            FROM dm.DimDichVu dv3 WITH (NOLOCK)
            WHERE dv3.NguonDuLieuKey = source.NguonDuLieuKey
              AND dv3.MaChiTieu      = source.MaChiTieu
        ), 0)),

        source.MaCoSo,
        source.MaThuPhi,
        source.MaPhieuDichVu,
        source.MaHoSo,
        source.MaChiTieu,
        source.MaChiTieuBK,
        source.NgayDenKham,
        source.SoLuong,
        source.TongTien,
        source.TongTienSauTangGiam,
        source.LoaiHinh,
        source.SoHoaDon,
        ISNULL(CAST(source.TongTienSauTangGiam AS FLOAT), 0),  -- DoanhThu = TongTienSauTangGiam
        source.DaThucHien,
        source.TrangThaiPhieu
    );