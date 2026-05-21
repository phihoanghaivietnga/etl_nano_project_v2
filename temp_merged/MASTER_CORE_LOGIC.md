# MASTER_CORE_LOGIC.md

## NHÓM: CORE_LOGIC

## MỤC LỤC NGUỒN
  [DESCRIPTION]: Core logic, configuration, and environment settings

### config/.env.example - Thành phần lõi và cấu hình nền tảng của hệ thống ETL
### config/tables.yaml - Thành phần lõi và cấu hình nền tảng của hệ thống ETL
### src/core/base_extractor.py - Thành phần lõi và cấu hình nền tảng của hệ thống ETL
### src/core/base_loader.py - Thành phần lõi và cấu hình nền tảng của hệ thống ETL
### src/core/base_ui.py - Thành phần lõi và cấu hình nền tảng của hệ thống ETL

## NỘI DUNG GỘP

### SOURCE: config/.env.example
```text
# =============================================================================
# ETL Nano V2 - Environment Configuration Template
# =============================================================================
# Lưu ý: Đổi tên file thành .env và điền các giá trị thực
# =============================================================================

# -----------------------------------------------------------------------------
# Database Connections
# -----------------------------------------------------------------------------

# Chuỗi kết nối đến SQL Server Production (Source - Chỉ đọc)
# Sử dụng ODBC Driver 17 for SQL Server
PROD_CONNECTION_STRING=DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.100;DATABASE=HIS_NANO_V2;UID=etl_read;PWD=your_password_here;TrustServerCertificate=yes

# Chuỗi kết nối đến SQL Server Datamart (Target - Đọc/Ghi)
DATAMART_CONNECTION_STRING=DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.101;DATABASE=ETL_DATAMART;UID=etl_write;PWD=your_password_here;TrustServerCertificate=yes

# -----------------------------------------------------------------------------
# Database Connection Settings
# -----------------------------------------------------------------------------

# Thời gian chờ kết nối (giây)
CONNECTION_TIMEOUT=30

# Số lần thử kết nối lại khi thất bại
MAX_RETRIES=3

# Thời gian chờ giữa các lần retry (giây)
RETRY_DELAY=5

# -----------------------------------------------------------------------------
# ETL Settings
# -----------------------------------------------------------------------------

# Kích thước batch khi bulk insert (số dòng mỗi batch)
BATCH_SIZE=10000

# Số lần thử lại khi một bảng lỗi
TABLE_MAX_RETRIES=3

# Khoảng thời gian đồng bộ fact tables (phút)
FACT_SYNC_INTERVAL_MINUTES=30

# Thời gian chạy rebuild index hàng ngày (giờ:phút)
INDEX_REBUILD_TIME=02:00

# -----------------------------------------------------------------------------
# Email Alert Settings
# -----------------------------------------------------------------------------

# SMTP Server
SMTP_SERVER=smtp.company.local
SMTP_PORT=587
SMTP_USERNAME=etl@company.local
SMTP_PASSWORD=your_email_password_here

# Danh sách email nhận cảnh báo (phân cách bằng dấu phẩy)
ALERT_EMAIL_TO=operator@company.local,admin@company.local

# -----------------------------------------------------------------------------
# Logging Settings
# -----------------------------------------------------------------------------

# Thư mục lưu log
LOG_DIR=./logs

# Mức độ log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Số ngày lưu log
LOG_RETENTION_DAYS=90

# -----------------------------------------------------------------------------
# Application Settings
# -----------------------------------------------------------------------------

# Môi trường (development, production)
APP_ENV=development

# API Host
API_HOST=0.0.0.0

# API Port
API_PORT=9001

# API URL (duong dan day du cho UI goi toi)
API_URL=http://localhost:9001
```

### SOURCE: config/tables.yaml
```yaml
etl_settings:
  odbc_chunk_size: 5000
  active_facilities:
  - hanoi
incremental_tables:
  ThuPhiDichVu:
    type: fact
    date_column: NgayDenKham
    merge_script: src/db/templates/sql/fact/merge_fact_thuphichvu_3in1.sql
    lookback_days: 1
    selected_columns:
    - MaThuPhi
    - MaPhieuDichVu
    - MaHoSo
    - NgayDenKham
    - MaDichVu
    - MaChiTieu
    - TongTien
    - DaDongTien
    - MaNguoiDung
    - MaKhoaKham
    - MaPhongKham
    - MaKhoaCanLamSang
    - MaPhongCanLamSang
    - DaThucHien
    - SoHoaDon
    - NgayVaoMay
    - NgayBaoCaoDoanhThu
    - TrangThaiPhieu
    - SoLuong
    - SoLuongThucHien
    - GhiChu
    - IDKeys
    - NgayGioYLenh
    - NgayTraKetQua
    - MaBacSyCD
    - HanhChinhOrTruc
    - DichVuOrTuNguyen
    - sysdate
    - TongTienSauTangGiam
    - BHNTChiTra
    - MaBacSyTH
    - StateThanhToanNoiTru
    - LOCK
    - STTThuPhi
    - MaNguoiDungCD
    - MaGoiDichVu
  ThuPhiBaoHiem:
    type: fact
    date_column: NgayDenKham
    merge_script: src/db/templates/sql/fact/merge_fact_thuphichvu_3in1.sql
    lookback_days: 1
    selected_columns:
    - MaThuPhi
    - MaHoSo
    - MaPhieuDichVu
    - NgayDenKham
    - MaDichVu
    - MaChiTieu
    - TongTien
    - BHChiTra
    - ThanhTien
    - DaDongTien
    - MaNguoiDung
    - PhanTramBaoHiem
    - MaKhoaKham
    - MaPhongKham
    - MaKhoaCanLamSang
    - MaPhongCanLamSang
    - DuyetBaoHiem
    - StateThanhToanNoiTru
    - SoHoaDon
    - TienChenhLech
    - NgayVaoMay
    - TrangThaiPhieu
    - SoLuong
    - SoLuongThucHien
    - GhiChu
    - IDKeys
    - NgayGioYLenh
    - NgayTraKetQua
    - MaBacSyCD
    - HanhChinhOrTruc
    - DichVuKyThuatCao
    - TrongNgoai_DT
    - LOCK
    - sysdate
    - DaThuChenh
    - SoHoaDonThuChenh
    - MaNguoiThuChenh
    - NgayThuChenh
    - MaNguoiDuyet
    - NgayDuyet
    - MaNguoiThanhToan
    - NgayThanhToan
    - MaBacSyTH
    - LOCKTHUCHENH
    - STTThuPhi
    - MaNguoiDungCD
    - MaLoai
    - DonGiaBH
    - DonGiaDV
    - bChuyenDoiTuong
    - NgayGioThucHienYL
    - MaGoiDichVu
    - DonGiaGoiDichVu
  ThuPhiTangGiam:
    type: fact
    date_column: NgayDenKham
    merge_script: src/db/templates/sql/fact/merge_fact_thuphichvu_3in1.sql
    lookback_days: 1
    selected_columns:
    - MaPhieuTangGiam
    - MaPhieuDichVu
    - MaHoSo
    - NgayDenKham
    - MaDichVu
    - MaChiTieu
    - SoTienGoc
    - SoTienTang
    - SoTienGiam
    - MaNguoiDung
    - MaLyDo
    - IDKeys
    - NgayTangGiam
    - DaDongTien
    - SoHoaDon
    - PhanTramTang
    - PhanTramGiam
    - MaDoiTuongTangGiam
    - MaPhongKham
    - MaBacSyCD
    - MaPhongCanLamSang
    - MaBacSyTH
    - NgayGioYLenh
    - MaGoiDichVu
  ThuPhiGoi:
    type: fact
    date_column: NgayThu
    merge_script: src/db/templates/sql/fact/FactThuPhiDichVu_ThuPhiGoi_merge.sql
    lookback_days: 1
    selected_columns:
    - ID
    - MaHoSo
    - MaLoaiGoi
    - NgayThu
    - SoTien
    - GiamGia
    - TongTien
    - HinhThucThanhToan
    - GhiChuHinhThucThanhToan
    - MaNguoiDung
    - HoanTat
    - TrangThaiHuy
    - MaPhieuThu
    - LyDoGiam
    - ThanhTien
    - bTiemChung
    - GiamGiaBHYT
    - GiamGiaKhac
  DoThiLuc:
    type: fact
    date_column: NgayDo
    merge_script: src/db/templates/sql/fact/FactDoThiLuc_merge.sql
    lookback_days: 1
    selected_columns:
    - MaHoSo
    - KXM_Cau_MP
    - KXM_Cau_MT
    - KXM_Tru_MP
    - KXM_Tru_MT
    - KXM_Truc_MP
    - KXM_Truc_MT
    - KXM_KCDT
    - KC_Cau_MP
    - KC_Cau_MT
    - KC_Tru_MP
    - KC_Tru_MT
    - KC_Truc_MP
    - KC_Truc_MT
    - KC_CK_MP
    - KC_CK_MT
    - KC_Add_MP
    - KC_Add_MT
    - KC_KCDT
    - KXHT_KK_MP
    - KXHT_KK_MT
    - KXHT_Cau_MP
    - KXHT_Cau_MT
    - KXHT_Tru_MP
    - KXHT_Tru_MT
    - KXHT_Truc_MP
    - KXHT_Truc_MT
    - KXHT_CK_MP
    - KXHT_CK_MT
    - KXHT_Add_MP
    - KXHT_Add_MT
    - KXHT_KCDT
    - KXSLDT_KK_MP
    - KXSLDT_KK_MT
    - KXSLDT_Cau_MP
    - KXSLDT_Cau_MT
    - KXSLDT_Tru_MP
    - KXSLDT_Tru_MT
    - KXSLDT_Truc_MP
    - KXSLDT_Truc_MT
    - KXSLDT_CK_MP
    - KXSLDT_CK_MT
    - KXSLDT_Add_MP
    - KXSLDT_Add_MT
    - KXSLDT_KCDT
    - Skiascopy_MP
    - Skiascopy_MT
    - NhanAp_MP
    - NhanAp_MT
    - BeDayGiacMac_MP
    - BeDayGiacMac_MT
    - DuongKinhDongTu_MP
    - DuongKinhDongTu_MT
    - K1_MP
    - K1_MT
    - K2_MP
    - K2_MT
    - ThiTruongVaoVien_MP
    - ThiTruongVaoVien_MT
    - LeDao_MP
    - LeDao_MT
    - MiMat_MP
    - MiMat_MT
    - KetMac_MP
    - KetMac_MT
    - TinhHinhMatHot_MP
    - TinhHinhMatHot_MT
    - GiacMac_MP
    - GiacMac_MT
    - CungMac_MP
    - CungMac_MT
    - TienPhong_MP
    - TienPhong_MT
    - MongMat_MP
    - MongMat_MT
    - DongTuPhanXa_MP
    - DongTuPhanXa_MT
    - ThuyTinhThe_MP
    - ThuyTinhThe_MT
    - DichKinh_MP
    - DichKinh_MT
    - VongMac_MP
    - VongMac_MT
    - GaiThi_MP
    - GaiThi_MT
    - HoangDiem_MP
    - HoangDiem_MT
    - SoiAnhDongTu_MP
    - SoiAnhDongTu_MT
    - TinhHinhNhanCau_MP
    - TinhHinhNhanCau_MT
    - HoMat_MP
    - HoMat_MT
    - ThiLuc_MP
    - ThiLuc_MT
    - ThiLucLoKinh_MP
    - ThiLucLoKinh_MT
    - ChieuDaiTrucNhanCau_MP
    - ChieuDaiTrucNhanCau_MT
    - NhinXa_KK_MP
    - NhinXa_KK_MT
    - NhinXa_Cau_MP
    - NhinXa_Cau_MT
    - NhinXa_Tru_MP
    - NhinXa_Tru_MT
    - NhinXa_Truc_MP
    - NhinXa_Truc_MT
    - NhinXa_CK_MP
    - NhinXa_CK_MT
    - NhinXa_Add_MP
    - NhinXa_Add_MT
    - NhinXa_KCDT
    - NhinGan_KK_MP
    - NhinGan_KK_MT
    - NhinGan_Cau_MP
    - NhinGan_Cau_MT
    - NhinGan_Tru_MP
    - NhinGan_Tru_MT
    - NhinGan_Truc_MP
    - NhinGan_Truc_MT
    - NhinGan_CK_MP
    - NhinGan_CK_MT
    - NhinGan_Add_MP
    - NhinGan_Add_MT
    - NhinGan_KCDT
    - LoiDan
    - NguoiThucHien
    - KC_KK_MP
    - KC_KK_MT
    - TrangThai
    - MaPhongKham
    - GhiChu
    - KXHT_ChuaChinh_MP
    - KXHT_ChuaChinh_MT
    - KXHT_DaChinh_MT
    - KXHT_DaChinh_MP
    - KhoangCachDongTuXa
    - KhoangCachDongTuGan
    - STTKetThuc
    - NgayDo
    - CongNhinGan
    - ThiLucCongNhinGan
    - KinhApTrong
    - KinhDaTrong
    - KinhDoiMau
    - KinhHaiTrong
    - KinhNhinGan
    - KinhPoly
    - KinhNhinXa
    - TinhTrangKinh
    - ThoiGianSuDung
    - SoLuong
    - bKinhXuoc
    - KXHT_KK_MP_Xa
    - KXHT_KK_MT_Xa
    - KXHT_Cau_MP_Xa
    - KXHT_Cau_MT_Xa
    - KXHT_Tru_MP_Xa
    - KXHT_Tru_MT_Xa
    - KXHT_Truc_MP_Xa
    - KXHT_Truc_MT_Xa
    - KXHT_CK_MP_Xa
    - KXHT_CK_MT_Xa
    - KXHT_Add_MP_Xa
    - KXHT_Add_MT_Xa
    - KXHT_KCDT_Xa
    - KXSLDT_KK_MP_Xa
    - KXSLDT_KK_MT_Xa
    - KXSLDT_Cau_MP_Xa
    - KXSLDT_Cau_MT_Xa
    - KXSLDT_Tru_MP_Xa
    - KXSLDT_Tru_MT_Xa
    - KXSLDT_Truc_MP_Xa
    - KXSLDT_Truc_MT_Xa
    - KXSLDT_CK_MP_Xa
    - KXSLDT_CK_MT_Xa
    - KXSLDT_Add_MP_Xa
    - KXSLDT_Add_MT_Xa
    - KXSLDT_KCDT_Xa
    - ThiLucLoKinh_MP_Xa
    - ThiLucLoKinh_MT_Xa
    - Skiascopy_SauLiet_MP
    - Skiascopy_SauLiet_MT
    - ThoiGianTraThuoc
    - Anh1
    - Anh2
    - Anh3
    - Anh4
    - Anh5
    - Anh6
    - Anh7
    - Anh8
    - iKhucXaMay
    - iDoSoKinhBangmay
    - iKhucXaHienTai
    - iKhucXaSauLietDieuTiet
    - iDoNhanAp
    - iDoDoDayGiacMac
    - iChieuDaiTrucNhanCau
    - iDonKinh
    - NhanAp_Maklakov_MP
    - NhanAp_Maklakov_MT
    - KXSLDT_ThiLucLoKinh_MP
    - KXSLDT_ThiLucLoKinh_MT
  HoSoKhamBenhNgoaiTru:
    type: fact
    date_column: NgayVaoKham
    merge_script: src/db/templates/sql/fact/DimLuotKham_merge.sql
    lookback_days: 1
    selected_columns:
    - MaHoSo
    - SoVaoVien
    - STT
    - MaBenhNhan
    - NgayVaoKham
    - TrangThaiPhieu
    - GhiChu
    - MaDoiTuongBenhNhan
    - LyDoVaoKham
    - ChanDoan
    - KetLuan
    - MaBenh1
    - MaBenh2
    - MaBenh3
    - SoTheBHYT
    - NgayBatDau
    - NgayHetHan
    - MaDoiTuongBaoHiem
    - MaLoaiBaoHiem
    - MaNoiDangKyKCBBD
    - MaXuTri
    - MaBacSy
    - MaHoSoTuSinh
    - ThuongOrCapCuu
    - DungTraiTuyen
    - NgayVaoKhamDP
    - DuyetBHLai
    - TongSoNgayDT
    - NgayVaoKhamDP2
    - bBenhNhanAo
    - TrangThaiThanhToan
    - bNhapVien
    - NgayChuyen
    - TrangThaiCapThuoc
    - SoChuyenVien
    - ChuyenVienNoiTinh
    - bUuTien
    - DTMienPhi
    - bDieuTriNgoaiTru
    - bDaDieuTriXong
    - CDNoiGioiThieu_MaBenh_CDPhongKham_MaBenh_KeDon_ChuyenVien_VaoKhoa_DTNgT
    - NoiChuyenDen
    - MaLoaiKham
    - TenLoaiKham
    - MaKhamBenhSan
    - TenKhamBenhSan
    - Mach
    - NhietDo
    - HuyetAp
    - NhipTho
    - ChieuCao
    - CanNang
    - MaDonThuoc
    - MaDonThuocDY
    - NgayDuyetBaoHiem
    - PhanTramBaoHiem
    - QuaTrinhBenhLy
    - TienSuBenhBanThan
    - TienSuBenhGiaDinh
    - MaNguoiDuyet
    - GhiChuMaBenh1
    - GhiChuMaBenh2
    - GhiChuMaBenh3
    - iChanDoanKhoaPHCN
    - iCapCuuNoiOrNgoai
    - bThuGiayChuyenVien
    - MaKhoaVaoVien
    - TongTienDuyet
    - HanhChinhOrTruc
    - MaKhuVuc
    - MaNhomTaiNan
    - MaNoiChuyenDen
    - NgayRaVien
    - NgayThanhToan
    - SoChuyenDen
    - MaNguoiTiepNhan
    - MaDoiTuongBenhNhanChuan
    - bBNManTinh
    - SoBAManTinh
    - MaBenhYHCT1
    - MaBenhYHCT2
    - GhiChuMaBenhYHCT1
    - GhiChuMaBenhYHCT2
    - SoLuuTruRaVien
    - NgayCapSoLuuTruRaVien
    - MaNguoiLuuTru
    - LOCK
    - NgayDu5Nam
    - bGiayChungNhanKhongCungChiTra
    - GiamDinh
    - MaBenhChinh
    - sysdate
    - MaBacSyChuyen
    - MaGoiKhamTheoDoan
    - TrangThaiChiDinhDoan
    - TrangThaiHoSoDoanDenKham
    - TrangThaiPhatSo
    - STT_Doan
    - Barcode_Doan
    - NgayPhatSo
    - DiaChiTheBHYT
    - BoPhan
    - ChucVu
    - MaNguoiThanhToan
    - TrieuChungLamSang
    - ToanThan
    - CacBoPhan
    - CachXuLy
    - TuMayChu
    - MaLienKet
    - MaNguonKhach
    - TuanHoan
    - HoHap
    - TieuHoa
    - Than_TietNieu
    - NoiTiet
    - Co_Xuong_Khop
    - ThanKinh
    - TamThan
    - ThongTuyen
    - SoTheAo
    - StateXuatXML
    - SoNghiBHXH
    - HoSoVip
    - NgayDieuTriNgoaiTru
    - VongBung
    - NgoaiMat
    - TrongMieng
    - NgayMienCCT
    - HoTenCha
    - HoTenMe
    - TuNgayNghiBHXH
    - DenNgayNghiBHXH
    - NgayLapPhieuBHXH
    - MaHoSoHienThi
    - DaInMau01
    - SoTienTamThuDuKien
    - MaTiepNhan_KBYT
    - MaTiepNhan_GTHH
    - MaLichHen_CRM
    - bitGuiSMS
    - PhanLoaiTheLuc
    - TaiPhai1000Hz
    - TaiPhai4000Hz
    - TaiTrai1000Hz
    - TaiTrai4000Hz
    - MaMP_CoKinh
    - MaMP_KhongKinh
    - MaMT_CoKinh
    - MaMT_KhongKinh
    - LoaiSucKhoe
    - TieuSuBenhNhan
    - DuBaoSucKhoe
    - PhongNgua
    - KetLuanVaTuVan
    - KetQuaDieuTri
    - ChanDoanMP
    - ChanDoanMT
    - ChanDoan2Mat
    - MaBenhMP
    - MaBenhMT
    - MaBenh2Mat
    - LinkMaBenh
    - ChanDoanSoBoMat
    - ChanDoanXacDinhMat
    - MaXuTriMat
    - PhanTruoc_MP
    - PhanTruoc_MT
    - DayMat_MP
    - DayMat_MT
    - VanNhan_MP
    - VanNhan_MT
    - TinhTrangRaVien
    - MaSoBHXH
    - MaBenhKemMat
    - TenBenhKemMat
    - LinhThuocTheoHen
    - ThuHoiDeNghiTT
    - KTKeDon
    - HuongDieuTri
    - CodeTraKQ
    - StateCheckIn
    - StateXuatXML130
    - IDLichHen
    - SoTheBHYTNghiBHXH
facilities:
  hanoi:
    nguon_dulieu_key: 2
    co_so_key: 1
    staging_schema: hanoi_hisnano_v2
```

### SOURCE: src/core/base_extractor.py
```py
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta


@dataclass(frozen=True)
class ExtractPlan:
    table_name: str
    date_column: str
    effective_from_date: date
    to_date: date
    select_sql: str
    selected_columns: tuple[str, ...]
    projected_columns: tuple[str, ...]


class BaseExtractor:
    """
    Lớp nền chỉ chịu trách nhiệm EXTRACT.
    Không chứa logic TRUNCATE/BCP IN/MERGE.
    """

    def __init__(self, production_connection: str) -> None:
        self.production_connection = production_connection

    @staticmethod
    def _sanitize_identifier(name: str) -> str:
        clean = str(name).strip()
        if not clean:
            raise ValueError("Tên cột whitelist không được rỗng")
        return clean

    @classmethod
    def _build_whitelist_projections(cls, selected_columns: list[str] | tuple[str, ...]) -> list[str]:
        if not selected_columns:
            raise ValueError("selected_columns bắt buộc có ít nhất 1 cột")
        projections: list[str] = []
        for column in selected_columns:
            column_name = cls._sanitize_identifier(column)
            projections.append(f"[{column_name}]")
        return projections

    @staticmethod
    def normalize_date(value: object | None, fallback: date) -> date:
        if value is None:
            return fallback
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        raise ValueError(f"Không parse được ngày: {value}")

    @staticmethod
    def compute_effective_from_date(from_date: date, lookback_days: int) -> date:
        if lookback_days < 0:
            raise ValueError("lookback_days phải >= 0")
        return from_date - timedelta(days=lookback_days)

    @staticmethod
    def build_select_sql(table_name: str, date_column: str, projections: list[str], from_date: date, to_date: date) -> str:
        projected = ", ".join(projections)
        return (
            f"SELECT {projected} FROM dbo.[{table_name}] WITH (NOLOCK) "
            f"WHERE CAST([{date_column}] AS DATE) >= '{from_date:%Y-%m-%d}' "
            f"AND CAST([{date_column}] AS DATE) <= '{to_date:%Y-%m-%d}'"
        )

    def build_extract_plan(
        self,
        table_name: str,
        date_column: str,
        from_date: date,
        to_date: date,
        lookback_days: int,
        selected_columns: list[str] | tuple[str, ...],
    ) -> ExtractPlan:
        effective_from_date = self.compute_effective_from_date(from_date=from_date, lookback_days=lookback_days)
        physical_columns = [self._sanitize_identifier(column) for column in selected_columns]

        if not physical_columns:
            raise ValueError(f"selected_columns rỗng cho bảng {table_name}")

        select_projections = self._build_whitelist_projections(selected_columns)
        final_projections = [*select_projections]
        final_columns = [*physical_columns]

        if len(final_columns) != len(final_projections):
            raise ValueError(
                f"Lệch schema projection cho bảng {table_name}: "
                f"physical_columns={len(final_columns)} != select_projections={len(final_projections)}"
            )

        select_sql = self.build_select_sql(
            table_name=table_name,
            date_column=date_column,
            projections=final_projections,
            from_date=effective_from_date,
            to_date=to_date,
        )
        return ExtractPlan(
            table_name=table_name,
            date_column=date_column,
            effective_from_date=effective_from_date,
            to_date=to_date,
            select_sql=select_sql,
            selected_columns=tuple(final_columns),
            projected_columns=tuple(final_projections),
        )
```

### SOURCE: src/core/base_loader.py
```py
from __future__ import annotations

import asyncio
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

import pyodbc


class BaseLoader:
    def __init__(
        self,
        connection_string: str,
        table_name: str,
    ) -> None:
        self.connection_string = connection_string
        self.table_name = table_name
        self._active_queue: asyncio.Queue[str] | None = None
        self._active_loop: asyncio.AbstractEventLoop | None = None

    def _log(
        self,
        message: str,
        queue: asyncio.Queue[str] | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        text = f"[{self.table_name}] {message}"
        target_queue = queue or self._active_queue
        target_loop = loop or self._active_loop
        if target_queue is not None and target_loop is not None:
            target_loop.call_soon_threadsafe(target_queue.put_nowait, text)
        else:
            print(text)

    def _emit_done(
        self,
        queue: asyncio.Queue[str] | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        target_queue = queue or self._active_queue
        target_loop = loop or self._active_loop
        if target_queue is not None and target_loop is not None:
            target_loop.call_soon_threadsafe(target_queue.put_nowait, "[DONE]")

    @staticmethod
    def _prepend_nocount(sql_text: str) -> str:
        normalized = sql_text.lstrip().upper()
        if normalized.startswith("SET NOCOUNT ON;"):
            return sql_text
        return f"SET NOCOUNT ON;\n{sql_text}"

    @contextmanager
    def get_db_context(self) -> Iterable[pyodbc.Connection]:
        connection = pyodbc.connect(self.connection_string, autocommit=False)
        try:
            yield connection
        finally:
            connection.close()

    def execute_sql_sync(
        self,
        connection: pyodbc.Connection,
        sql_text: str,
        params: tuple[Any, ...] | None = None,
    ) -> None:
        safe_sql = self._prepend_nocount(sql_text)
        cursor = connection.cursor()
        cursor.execute(safe_sql, params or ())

    def _execute_core(self, connection: pyodbc.Connection) -> None:
        raise NotImplementedError("Loader con phải override _execute_core")

    def execute_load(
        self,
        *args: Any,
        queue: asyncio.Queue[str] | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
        **kwargs: Any,
    ) -> None:
        self._active_queue = queue
        self._active_loop = loop
        self._log("Bắt đầu execute_load", queue=queue, loop=loop)
        with self.get_db_context() as connection:
            try:
                self._execute_core(connection, *args, **kwargs)
                connection.commit()
                self._log("Hoàn tất thành công, đã commit", queue=queue, loop=loop)
            except Exception as exc:
                connection.rollback()
                self._log(f"Thất bại, đã rollback toàn cục: {exc}", queue=queue, loop=loop)
                raise
            finally:
                self._emit_done(queue=queue, loop=loop)
                self._active_queue = None
                self._active_loop = None


class GenericTableLoader(BaseLoader):
    def __init__(
        self,
        connection_string: str,
        table_name: str,
        merge_sql_path: str | None = None,
    ) -> None:
        super().__init__(connection_string=connection_string, table_name=table_name)
        self.merge_sql_path = merge_sql_path

    @staticmethod
    def _resolve_date(value: Any) -> date | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        return None

    @staticmethod
    def _build_incremental_params(sql_text: str, from_date: date | None, to_date: date | None) -> tuple[Any, ...]:
        marker_count = sql_text.count("?")
        if marker_count == 0:
            return tuple()
        if from_date is None or to_date is None:
            raise ValueError("Thiếu from_date hoặc to_date để bind marker '?' cho SQL incremental")

        pair = (from_date, to_date)
        params: list[Any] = []
        while len(params) < marker_count:
            params.extend(pair)
        return tuple(params[:marker_count])

    def _execute_core(self, connection: pyodbc.Connection, *args: Any, **kwargs: Any) -> None:
        from_date = self._resolve_date(args[0] if len(args) > 0 else kwargs.get("from_date"))
        to_date = self._resolve_date(args[1] if len(args) > 1 else kwargs.get("to_date"))

        if from_date and to_date:
            self._log(f"Khoảng thời gian: {from_date} -> {to_date}")
        else:
            self._log("Không có tham số ngày, chuyển sang chế độ kiểm tra cơ bản")

        if self.merge_sql_path:
            sql_path = Path(self.merge_sql_path)
            sql_text = sql_path.read_text(encoding="utf-8")
            params = self._build_incremental_params(sql_text, from_date, to_date)
            self._log(f"Thực thi MERGE template: {sql_path}")
            self.execute_sql_sync(connection, sql_text, params)
            return

        health_check_sql = "SELECT GETDATE() AS ThoiGianHeThong;"
        self._log("Không có template cụ thể, chạy health-check SQL")
        self.execute_sql_sync(connection, health_check_sql)
```

### SOURCE: src/core/base_ui.py
```py
from __future__ import annotations

import asyncio
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable

import pyodbc
from dotenv import load_dotenv
from nicegui import run, ui


class BaseUI:
    ENV_PATH = Path("config/.env")
    _env_loaded = False
    _shared_semaphore: asyncio.Semaphore | None = None
    _max_concurrent_connections = 5

    def __init__(self, page_title: str, navigation_items: list[tuple[str, str]] | None = None) -> None:
        self._ensure_environment_loaded()
        self.page_title = page_title
        self.navigation_items = navigation_items or []
        if BaseUI._shared_semaphore is None:
            BaseUI._shared_semaphore = asyncio.Semaphore(BaseUI._max_concurrent_connections)

    @classmethod
    def _ensure_environment_loaded(cls) -> None:
        if cls._env_loaded:
            return
        load_dotenv(dotenv_path=cls.ENV_PATH, override=False)
        cls._max_concurrent_connections = cls._parse_int(
            os.getenv("MAX_CONCURRENT_CONNECTIONS"),
            default=5,
        )
        cls._env_loaded = True

    @staticmethod
    def _parse_int(value: str | None, default: int) -> int:
        try:
            parsed = int((value or "").strip())
            return parsed if parsed > 0 else default
        except (TypeError, ValueError):
            return default

    def build_layout(self, active_route: str) -> None:
        with ui.header().classes("items-center justify-between"):
            ui.label(self.page_title).classes("text-lg font-semibold")

        with ui.left_drawer(value=True).classes("bg-slate-50"):
            ui.label("Điều hướng Dashboard").classes("text-sm text-slate-700 font-medium")
            for route, label in self.navigation_items:
                style = "text-primary font-semibold" if route == active_route else ""
                ui.link(label, route).classes(f"block py-1 {style}")

    def get_env(self, key: str, default: str = "") -> str:
        return os.getenv(key, default)

    def get_production_connection_vars(self) -> list[str]:
        keys = [key for key in os.environ if key.startswith("PROD_CONNECTION_")]
        return sorted(keys)

    def get_staging_schemas(self) -> list[str]:
        raw = self.get_env("STAGING_SCHEMAS", "hanoi_hisnano_v2")
        schemas = [item.strip() for item in raw.split(",") if item.strip()]
        return schemas or ["hanoi_hisnano_v2"]

    @contextmanager
    def get_db_context(self, connection_string_var: str) -> Iterable[pyodbc.Connection]:
        connection_string = self.get_env(connection_string_var).strip()
        if not connection_string:
            raise ValueError(f"Thiếu cấu hình kết nối: {connection_string_var}")

        connection = pyodbc.connect(connection_string, autocommit=False)
        try:
            yield connection
        finally:
            connection.close()

    @staticmethod
    def _prepend_nocount(sql_text: str) -> str:
        normalized = sql_text.lstrip().upper()
        if normalized.startswith("SET NOCOUNT ON;"):
            return sql_text
        return f"SET NOCOUNT ON;\n{sql_text}"

    def _query_sync(
        self,
        connection_string_var: str,
        sql_text: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[dict[str, Any]]:
        safe_sql = self._prepend_nocount(sql_text)
        with self.get_db_context(connection_string_var) as connection:
            cursor = connection.cursor()
            cursor.execute(safe_sql, params or ())
            if cursor.description is None:
                connection.commit()
                return []

            columns = [item[0] for item in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    async def execute_query_async(
        self,
        connection_string_var: str,
        sql_text: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[dict[str, Any]]:
        if BaseUI._shared_semaphore is None:
            BaseUI._shared_semaphore = asyncio.Semaphore(BaseUI._max_concurrent_connections)
        async with BaseUI._shared_semaphore:
            return await run.io_bound(self._query_sync, connection_string_var, sql_text, params)

    def read_sql_template(self, sql_path: str | Path) -> str:
        path_obj = Path(sql_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Không tìm thấy SQL template: {path_obj}")
        return path_obj.read_text(encoding="utf-8")
```
