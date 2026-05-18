--
-- FILE: merge_fact_thuphichvu_3in1.sql
-- AUTHOR: GitHub Copilot (Builder)
-- CREATED: 2026-03-17
-- MODIFIED: 2026-03-27
-- VERSION: 1.9.1
-- PURPOSE: MERGE 3-in-1 doanh thu vào dm.FactThuPhiDichVu từ 3 nguồn:
--          1. ThuPhiDichVu (Dịch vụ) → LoaiHinh = 'DV'
--          2. ThuPhiBaoHiem (Bảo hiểm) → LoaiHinh = 'BH'
--          3. ThuPhiTangGiam → JOIN để tính TongTienSauTangGiam cho nguồn DV
--
--          Logic:
--          - ThuPhiDichVu LEFT JOIN ThuPhiTangGiam để tính TongTienSauTangGiam
--          - ThuPhiBaoHiem: TongTienSauTangGiam = TongTien + TienChenhLech
--          - DateKey = YEAR * 10000 + MONTH * 100 + DAY (từ NgayDoanhThu)
--          - LuotKhamKey, BenhNhanKey, DichVuKey: lookup từ DimLuotKham, DimDichVu
--          - MaChiTieuBK: Business Key bất biến = NguonDuLieuKey + ':' + MaChiTieu
--            (FIX E018 v1.7.3: Dung separator ':' thay vi '_' de dong nhat voi CLAUDE.md Section 7.1)
--
-- PARAMETERS (placeholders de thay the trong _substitute_params):
--     {nguon_dulieu_key} INT     - Key của nguồn dữ liệu (vd: 1 cho hanoi)
--     {coso_key}         INT     - Key của cơ sở (vd: 1 cho hanoi)
--     {ma_co_so}         NVARCHAR(50) - Ma co so (vd: 'hanoi')
--     {date_from}        DATE    - Ngày bắt đầu (inclusive)
--     {date_to}          DATE    - Ngày kết thúc (inclusive)
--     {staging_schema}   NVARCHAR(128) - Schema staging của facility
--
-- HISTORY:
--     - v1.0.0 [2026-03-17]: Tạo mới - MERGE 3-in-1 từ chỉ thị Opus Architect
--     - v1.1.0 [2026-03-17]: Sửa MERGE key: thay MaThuPhi bằng MaChiTieu + MaPhieuDichVu
--     - v1.2.0 [2026-03-18]: Thay hardcode bang placeholder facility va keys
--     - v1.4.0 [2026-03-24]: Bo sung MaDotThuPhi vao khoa MERGE
--     - v1.5.0 [2026-03-24]: Go MaDotThuPhi (khong ton tai trong schema thuc te)
--     - v1.6.0 [2026-03-25]: FIX E010 - Loai bo DECLARE @DateFrom/@DateTo, thay bang embedded
--                            string ({date_from}/{date_to}) de tranh GO batch scope loi
--     - v1.7.1 [2026-03-26]: LOAI BO MaChiTieuBK khoi ON clause (gay NULL comparison loi)
--                            MaChiTieuBK chi la data column, khong phai identity key
--     - v1.7.0 [2026-03-26]: [FEATURE] Them MaChiTieuBK (Business Key bat bien) vao MERGE
--                            + Toi uu cong thuc TongTienSauTangGiam (khong con CASE WHEN)
--                            + LOOKUP DichVuKey qua MaChiTieuBK thay vi MaChiTieu
--     - v1.8.0 [2026-03-27]: [FIX E020] LEFT JOIN -> tg_agg subquery (SUM aggregation)
--                            trong Nguon 1 ThuPhiDichVu de tranh nhan ban dong
--                            khi ThuPhiTangGiam co nhieu record cung khoa.
--                            Cong thuc: TongTienSauTangGiam = TongTien - TongGiam + TongTang
--     - v1.9.1 [2026-04-03]: [FIX E021] Them date filter vao tg_agg subquery.
--                            Root cause: Khong co date filter -> tg_agg SUM toan bo lich su,
--                            ngay cuoi cung nhan TatCaTangGiam = SUM TatCa -> bi sai thanh 0.
--                            Fix: Loc tg_agg theo {date_from}/{date_to} giong nhu dv/bh.
--     - v1.7.3 [2026-03-27]: [FIX E018] Doi separator MaChiTieuBK tu '_' thanh ':'
--                            de dong nhat voi CLAUDE.md Section 7.1 va MaBenhNhanBK
--


-- ============================================================
-- KHAI BAO THAM SỐ (chỉnh sửa theo môi trường thực tế)
-- ============================================================
DECLARE @NguonDuLieuKey INT     = {nguon_dulieu_key};
DECLARE @CoSoKey        INT     = {coso_key};
DECLARE @MaCoSo         NVARCHAR(50) = '{ma_co_so}';

-- FIX E010 v1.6.0: {date_from} va {date_to} la string placeholder
-- duoc thay the truc tiep trong Python _substitute_params() truoc khi tach GO batch
-- Vi du: {date_from} = '2026-03-10', {date_to} = '2026-03-10'
-- KHONG dung @DateFrom/@DateTo vi no bi mat scope khi GO tach batch

-- ============================================================
-- MERGE 3-IN-1: ThuPhiDichVu (DV) + ThuPhiBaoHiem (BH) + ThuPhiTangGiam (điều chỉnh)
-- ============================================================
MERGE [dm].[FactThuPhiDichVu] AS target
USING (

    -- --------------------------------------------------------
    -- NGUỒN 1: ThuPhiDichVu (Dịch vụ) - LEFT JOIN với ThuPhiTangGiam
    -- LoaiHinh = 'DV'
    -- FIX v1.7.2: Doc NguonDuLieuKey/CoSoKey tu staging (da enriched),
    --              khong dung gia tri tham so (vi enrichment da xay ra o Step 2)
    -- --------------------------------------------------------
    SELECT
        ISNULL(dv.NguonDuLieuKey, @NguonDuLieuKey) AS NguonDuLieuKey,
        ISNULL(dv.CoSoKey, @CoSoKey)                AS CoSoKey,
        ISNULL(dv.MaCoSo, @MaCoSo)                 AS MaCoSo,
        dv.MaThuPhi,
        dv.MaPhieuDichVu,
        dv.MaHoSo,
        dv.MaChiTieu,
        -- FIX v1.7.3 E018: MaChiTieuBK = NguonDuLieuKey (da enriched) + ':' + MaChiTieu
        -- (Doi tu '_' thanh ':' de dong nhat voi CLAUDE.md Section 7.1)
        CAST(ISNULL(dv.NguonDuLieuKey, @NguonDuLieuKey) AS VARCHAR(10)) + ':' + dv.MaChiTieu AS MaChiTieuBK,
        dv.NgayDenKham,
        dv.NgayVaoMay                               AS NgayDoanhThu,

        -- DateKey: tính từ NgayDoanhThu theo công thức YYYYMMDD
        ISNULL(
            CAST(YEAR(dv.NgayVaoMay) * 10000
                 + MONTH(dv.NgayVaoMay) * 100
                 + DAY(dv.NgayVaoMay) AS INT),
            CAST(YEAR(dv.NgayDenKham) * 10000
                 + MONTH(dv.NgayDenKham) * 100
                 + DAY(dv.NgayDenKham) AS INT)
        )                                           AS DateKey,

        -- SoLuongChuan: ưu tiên SoLuongThucHien, fallback SoLuong, default 1
        COALESCE(dv.SoLuongThucHien, dv.SoLuong, 1) AS SoLuongChuan,

        -- TongTien: giá trị gốc từ ThuPhiDichVu
        dv.TongTien                                 AS TongTien,

        -- FIX v1.8.0 E020: TongTienSauTangGiam - dung tg_agg (SUM aggregation)
        -- ThuPhiTangGiam co the co nhieu dong cung khoa -> aggregate SUM truoc khi JOIN
        -- Cong thuc: TongTien - TongGiam + TongTang
        dv.TongTien - ISNULL(tg_agg.TongGiam, 0) + ISNULL(tg_agg.TongTang, 0) AS TongTienSauTangGiam,

        -- LoaiHinh = 'DV' cho dịch vụ thường
        'DV'                                        AS LoaiHinh,

        dv.SoHoaDon,
        dv.DaThucHien,
        dv.TrangThaiPhieu

    -- FIX v1.8.0 E020: Pre-aggregate ThuPhiTangGiam bang subquery de tranh nhan ban
    -- Nếu cùng MaHoSo+MaChiTieu+MaPhieuDichVu có N dòng TG -> SUM(N) = TongGiam
    -- FIX E021 v1.9.1: THEM date filter vao tg_agg de chi aggregate dung ngay.
    -- Root cause: Khong co date filter -> tg_agg tong hop NHIEU THANG, khi merge
    -- ngay cuoi cung (01/04), TatCaTangGiam = SUM TatCa -> bi sai thanh 0.
    FROM [{staging_schema}].[ThuPhiDichVu] dv WITH (NOLOCK)
    LEFT JOIN (
        SELECT
            MaHoSo,
            MaChiTieu,
            MaPhieuDichVu,
            SUM(SoTienGiam) AS TongGiam,
            SUM(SoTienTang) AS TongTang
        FROM [{staging_schema}].[ThuPhiTangGiam] WITH (NOLOCK)
        WHERE DaDongTien = 1
          -- E021: LOC THEO NGAY - chi aggregate nhung dong trong date range hien tai
          AND CAST(NgayDenKham AS DATE) >= CAST('{date_from}' AS DATE)
          AND CAST(NgayDenKham AS DATE) <= CAST('{date_to}' AS DATE)
        GROUP BY MaHoSo, MaChiTieu, MaPhieuDichVu
    ) AS tg_agg
        ON dv.MaHoSo         = tg_agg.MaHoSo
        AND dv.MaChiTieu     = tg_agg.MaChiTieu
        AND dv.MaPhieuDichVu = tg_agg.MaPhieuDichVu
    WHERE dv.DaDongTien = 1
        AND dv.MaChiTieu IS NOT NULL
        AND LTRIM(RTRIM(dv.MaChiTieu)) <> ''
        -- FIX E010 v1.6.0: Dung embedded string thay vi @DateFrom/@DateTo (bi mat scope)
        AND CAST(dv.NgayDenKham AS DATE) >= CAST('{date_from}' AS DATE)
        AND CAST(dv.NgayDenKham AS DATE) <= CAST('{date_to}' AS DATE)

    UNION ALL

    -- --------------------------------------------------------
    -- NGUỒN 2: ThuPhiBaoHiem (Bảo hiểm)
    -- LoaiHinh = 'BH'
    -- FIX v1.7.2: Doc NguonDuLieuKey/CoSoKey tu staging (da enriched)
    -- --------------------------------------------------------
    SELECT
        ISNULL(bh.NguonDuLieuKey, @NguonDuLieuKey) AS NguonDuLieuKey,
        ISNULL(bh.CoSoKey, @CoSoKey)                AS CoSoKey,
        ISNULL(bh.MaCoSo, @MaCoSo)                AS MaCoSo,
        bh.MaThuPhi,
        bh.MaPhieuDichVu,
        bh.MaHoSo,
        bh.MaChiTieu,
        -- MaChiTieuBK = NguonDuLieuKey (da enriched) + ':' + MaChiTieu
        -- FIX E018 v1.7.3: Doi tu '_' thanh ':'
        CAST(ISNULL(bh.NguonDuLieuKey, @NguonDuLieuKey) AS VARCHAR(10)) + ':' + bh.MaChiTieu AS MaChiTieuBK,
        bh.NgayDenKham,
        bh.NgayVaoMay                               AS NgayDoanhThu,

        -- DateKey: tính từ NgayDoanhThu
        ISNULL(
            CAST(YEAR(bh.NgayVaoMay) * 10000
                 + MONTH(bh.NgayVaoMay) * 100
                 + DAY(bh.NgayVaoMay) AS INT),
            CAST(YEAR(bh.NgayDenKham) * 10000
                 + MONTH(bh.NgayDenKham) * 100
                 + DAY(bh.NgayDenKham) AS INT)
        )                                           AS DateKey,

        -- SoLuongChuan
        COALESCE(bh.SoLuongThucHien, bh.SoLuong, 1) AS SoLuongChuan,

        -- TongTien: giá trị gốc từ ThuPhiBaoHiem
        bh.TongTien                                 AS TongTien,

        -- FIX v1.7.0: TongTienSauTangGiam - cong thuc truc tiep
        -- BH khong co bang ThuPhiTangGiam -> TienChenhLech la adjustments
        bh.TongTien + ISNULL(bh.TienChenhLech, 0)  AS TongTienSauTangGiam,

        -- LoaiHinh = 'BH' cho bảo hiểm
        'BH'                                        AS LoaiHinh,

        bh.SoHoaDon,
        NULL                                        AS DaThucHien,   -- BH không có cột này
        bh.TrangThaiPhieu

    FROM [{staging_schema}].[ThuPhiBaoHiem] bh WITH (NOLOCK)
    WHERE bh.DaDongTien = 1
        AND bh.MaChiTieu IS NOT NULL
        AND LTRIM(RTRIM(bh.MaChiTieu)) <> ''
        -- FIX E010 v1.6.0: Dung embedded string thay vi @DateFrom/@DateTo (bi mat scope)
        AND CAST(bh.NgayDenKham AS DATE) >= CAST('{date_from}' AS DATE)
        AND CAST(bh.NgayDenKham AS DATE) <= CAST('{date_to}' AS DATE)

) AS source

-- ============================================================
-- ĐIỀU KIỆN MATCH: khóa tự nhiên của Fact (4 cột gốc)
-- FIX v1.7.1: LOẠI BỎ MaChiTieuBK khỏi ON clause
--             MaChiTieuBK chỉ là data column, không phải business key.
--             Dùng MaChiTieuBK trong INSERT để populate cho record mới.
--             Lookup DichVuKey dùng MaChiTieuBK để đảm bảo consistency.
-- ============================================================
ON  target.NguonDuLieuKey = source.NguonDuLieuKey
AND target.CoSoKey        = source.CoSoKey
AND target.MaHoSo         = source.MaHoSo
AND target.MaChiTieu      = source.MaChiTieu
AND target.MaPhieuDichVu  = source.MaPhieuDichVu
-- MaChiTieuBK: KHÔNG đưa vào ON vì:
--   1. Target NULL + Source NOT NULL = không match → INSERT thất bại vì duplicate
--   2. MaChiTieuBK chỉ là computed data, không phải identity key

-- ============================================================
-- WHEN MATCHED: Cập nhật các cột dữ liệu
-- ============================================================
WHEN MATCHED THEN
    UPDATE SET
        target.TongTien             = source.TongTien,
        target.TongTienSauTangGiam  = source.TongTienSauTangGiam,
        target.LoaiHinh             = source.LoaiHinh,
        target.SoHoaDon             = source.SoHoaDon,
        target.SoLuong              = source.SoLuongChuan,
        target.DoanhThu             = ISNULL(CAST(source.TongTienSauTangGiam AS FLOAT), 0),
        target.DaThucHien           = source.DaThucHien,
        target.TrangThaiPhieu       = source.TrangThaiPhieu,
        target.NgayDenKham          = source.NgayDenKham

-- ============================================================
-- WHEN NOT MATCHED: Insert bản ghi mới
-- ============================================================
WHEN NOT MATCHED BY TARGET THEN
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
        source.SoLuongChuan,
        source.TongTien,
        source.TongTienSauTangGiam,
        source.LoaiHinh,
        source.SoHoaDon,
        ISNULL(CAST(source.TongTienSauTangGiam AS FLOAT), 0),  -- DoanhThu = TongTienSauTangGiam
        source.DaThucHien,
        source.TrangThaiPhieu
    );
GO

-- ============================================================
-- THỐNG KÊ SAU KHI MERGE
-- ============================================================
-- FIX E010 v1.6.0: Dung embedded string thay vi @DateFrom/@DateTo (bi mat scope)
SELECT
    LoaiHinh,
    COUNT(*)                    AS SoBanGhi,
    SUM(TongTien)               AS TongTien,
    SUM(TongTienSauTangGiam)    AS TongTienSauTangGiam,
    SUM(DoanhThu)               AS TongDoanhThu
FROM [dm].[FactThuPhiDichVu]
WHERE NgayDenKham >= CAST('{date_from}' AS DATE)
  AND NgayDenKham <  DATEADD(DAY, 1, CAST('{date_to}' AS DATE))
GROUP BY LoaiHinh
ORDER BY LoaiHinh;
GO
