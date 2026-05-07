# ETL NANO PROJECT V2

## 1. Mục đích hệ thống
Hệ thống ETL phiên bản v2 được thiết kế để chuẩn hóa luồng dữ liệu từ Production sang Datamart theo kiến trúc Modular và lập trình hướng đối tượng (OOP). Hệ thống đảm bảo tính thống nhất giữa chế độ chạy Tự động (Auto) và Thủ công (Manual).
Hy vọng test lần cuối

## 2. Cấu trúc thư mục
ETL_Nano_Project_V2/
├── agents.md               # File chiến lược điều phối hệ thống
├── README.md               # Hướng dẫn tổng quan dự án
├── .env                    # Lưu trữ biến môi trường và kết nối DB
├── config/                 # Cấu hình hệ thống và danh sách bảng
├── docs/
│   ├── knowledge/       # Tầng tri thức GEM (9 file GEM_xxx.md)
		├── GEM_NAVIGATION.md: Chỉ dẫn tìm kiếm tri thức.
		├── GEM_GUIDE.md: Thứ tự ưu tiên đọc tài liệu.
		├── GEM_CODE_MAP.md: Sơ đồ các lớp và hàm trong mã nguồn.
		├── GEM_CODE_SNIPPETS.md: Thư viện mã mẫu chuẩn.
		├── GEM_DATA_FLOW.md: Mô tả luồng dữ liệu Production -> Staging -> Datamart.
		├── GEM_DB_SCHEMAS.md: Chi tiết cấu trúc bảng và schema database.
		├── GEM_AUTO_PIPELINE.md: Chi tiết vận hành engine chạy tự động.
		├── GEM_DEPENDENCY_GRAPH.md: Đồ thị mối quan hệ giữa các module.
		├── GEM_ERROR_CONTEXT.md: Bối cảnh và cách xử lý các mã lỗi (E-ID).
│   └── archive/            # Lưu trữ tài liệu phiên bản cũ
├── scripts/                # CÁC SCRIPT VẬN HÀNH VÀ TỰ ĐỘNG HÓA
│   └── upload_to_drive.py  # Script đồng bộ tri thức lên Google Drive
├── src/                    # Mã nguồn chính của ứng dụng, phân tách giữa Core logic và Job thực thi.
│   ├── core/               # Lớp cha, Logger, Database Connection
│   ├── jobs/               # Logic đồng bộ các bảng cụ thể
│   ├── ui/                 # Giao diện Streamlit (Runner & Verify)
│   └── db/
│       └── templates/sql/  # Nguồn SQL MERGE duy nhất
├── tests/                  # Script kiểm thử độc lập
└── .github/
    └── workflows/
        └── sync_to_drive.yml # File cấu hình Trigger GitHub Actions

## 3. Ý nghĩa các file GEM tri thức (docs/knowledge/)
- GEM_NAVIGATION.md: Chỉ dẫn tìm kiếm tri thức.
- GEM_GUIDE.md: Thứ tự ưu tiên đọc tài liệu.
- GEM_CODE_MAP.md: Sơ đồ các lớp và hàm trong mã nguồn.
- GEM_CODE_SNIPPETS.md: Thư viện mã mẫu chuẩn.
- GEM_DATA_FLOW.md: Mô tả luồng dữ liệu Production -> Staging -> Datamart.
- GEM_DB_SCHEMAS.md: Chi tiết cấu trúc bảng và schema database.
- GEM_AUTO_PIPELINE.md: Chi tiết vận hành engine chạy tự động.
- GEM_DEPENDENCY_GRAPH.md: Đồ thị mối quan hệ giữa các module.
- GEM_ERROR_CONTEXT.md: Bối cảnh và cách xử lý các mã lỗi (E-ID).