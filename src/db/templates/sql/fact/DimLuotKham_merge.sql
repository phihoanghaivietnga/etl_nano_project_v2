--
-- FILE: DimLuotKham_merge.sql
-- AUTHOR: GitHub Copilot
-- CREATED: 2026-03-14
-- MODIFIED: 2026-03-14
-- VERSION: 1.0.2
-- PURPOSE: Template MERGE DimLuotKham truc tiep tu HoSoKhamBenhNgoaiTru.
-- HISTORY:
--     - v1.0.0 [2026-03-14]: Tao moi template MERGE theo logic toi uu
--     - v1.0.1 [2026-03-14]: Map cot ThoiGianVaoKham va DaDongTien theo nguon thuc te
--     - v1.0.2 [2026-03-14]: Fallback NguonDuLieuKey, CoSoKey, MaCoSo neu nguon NULL
--

MERGE [{dm_schema}].[DimLuotKham] AS target
USING (
    SELECT
        COALESCE(s.NguonDuLieuKey, {nguon_dulieu_key}) AS NguonDuLieuKey,
        COALESCE(s.CoSoKey, {co_so_key}) AS CoSoKey,
        COALESCE(s.MaCoSo, '{ma_co_so}') AS MaCoSo,
        s.MaHoSo,
        CONCAT(COALESCE(s.NguonDuLieuKey, {nguon_dulieu_key}), ':', s.MaHoSo) AS MaHoSoBK,
        s.MaBenhNhan,
        bnh.MaBenhNhanBK,
        s.NgayVaoKham,
        CASE WHEN s.NgayVaoKham IS NULL THEN NULL
             ELSE (YEAR(CAST(s.NgayVaoKham AS DATE)) * 10000
                 + MONTH(CAST(s.NgayVaoKham AS DATE)) * 100
                 + DAY(CAST(s.NgayVaoKham AS DATE))) END AS NgayVaoKhamDateKey,
        s.NgayVaoKhamDP AS ThoiGianVaoKham,
        s.TrangThaiPhieu,
        NULL AS DaDongTien,
        s.TrangThaiThanhToan,
        s.NgayThanhToan,
        bnh.BenhNhanKey,
        CASE
            WHEN s.MaHoSo IS NULL OR LTRIM(RTRIM(s.MaHoSo)) = '' THEN 0
            WHEN s.MaBenhNhan IS NULL OR LTRIM(RTRIM(s.MaBenhNhan)) = '' THEN 0
            WHEN s.NgayVaoKham IS NULL THEN 0
            ELSE 1
        END AS DQ_HopLe,
        CASE
            WHEN s.MaHoSo IS NULL OR LTRIM(RTRIM(s.MaHoSo)) = '' THEN N'Thieu MaHoSo'
            WHEN s.MaBenhNhan IS NULL OR LTRIM(RTRIM(s.MaBenhNhan)) = '' THEN N'Thieu MaBenhNhan'
            WHEN s.NgayVaoKham IS NULL THEN N'Thieu NgayVaoKham'
            WHEN bnh.BenhNhanKey IS NULL THEN N'Khong map duoc sang dm.DimBenhNhan'
            ELSE NULL
        END AS DQ_GhiChu
    FROM [{source_schema}].[HoSoKhamBenhNgoaiTru] s
    LEFT JOIN [{dm_schema}].[DimBenhNhan] bnh
        ON bnh.MaBenhNhanBK = CONCAT(COALESCE(s.NguonDuLieuKey, {nguon_dulieu_key}), ':', s.MaBenhNhan)
) src
ON target.MaHoSoBK = src.MaHoSoBK
WHEN MATCHED THEN
    UPDATE SET
        NguonDuLieuKey = src.NguonDuLieuKey,
        CoSoKey = src.CoSoKey,
        MaCoSo = src.MaCoSo,
        MaHoSo = src.MaHoSo,
        MaBenhNhan = src.MaBenhNhan,
        MaBenhNhanBK = src.MaBenhNhanBK,
        BenhNhanKey = src.BenhNhanKey,
        NgayVaoKham = src.NgayVaoKham,
        NgayVaoKhamDateKey = src.NgayVaoKhamDateKey,
        ThoiGianVaoKham = src.ThoiGianVaoKham,
        TrangThaiPhieu = src.TrangThaiPhieu,
        DaDongTien = src.DaDongTien,
        TrangThaiThanhToan = src.TrangThaiThanhToan,
        NgayThanhToan = src.NgayThanhToan,
        DQ_HopLe = src.DQ_HopLe,
        DQ_GhiChu = src.DQ_GhiChu,
        NgayCapNhat = GETDATE()
WHEN NOT MATCHED THEN
    INSERT (
        NguonDuLieuKey, CoSoKey, MaCoSo, MaHoSo, MaHoSoBK,
        MaBenhNhan, MaBenhNhanBK, BenhNhanKey,
        NgayVaoKham, NgayVaoKhamDateKey, ThoiGianVaoKham,
        TrangThaiPhieu, DaDongTien, TrangThaiThanhToan, NgayThanhToan,
        DQ_HopLe, DQ_GhiChu
    )
    VALUES (
        src.NguonDuLieuKey, src.CoSoKey, src.MaCoSo, src.MaHoSo, src.MaHoSoBK,
        src.MaBenhNhan, src.MaBenhNhanBK, src.BenhNhanKey,
        src.NgayVaoKham, src.NgayVaoKhamDateKey, src.ThoiGianVaoKham,
        src.TrangThaiPhieu, src.DaDongTien, src.TrangThaiThanhToan, src.NgayThanhToan,
        src.DQ_HopLe, src.DQ_GhiChu
    );
