# ETL NANO PROJECT V2

## 1. Mục đích hệ thống
Hệ thống ETL phiên bản v2 được thiết kế để chuẩn hóa luồng dữ liệu từ Production sang Datamart theo kiến trúc Modular và lập trình hướng đối tượng (OOP). Hệ thống đảm bảo tính thống nhất giữa chế độ chạy Tự động (Auto) và Thủ công (Manual).

## 2. Cấu trúc thư mục
- /config: Chứa settings.yaml và tables.yaml để cấu hình hệ thống và danh sách bảng.
- /docs/knowledge: Tầng tri thức cốt lõi chứa 9 file GEM điều phối.
  - GEM_NAVIGATION.md: Chỉ dẫn tìm kiếm tri thức.
  - GEM_GUIDE.md: Thứ tự ưu tiên đọc tài liệu.
  - GEM_CODE_MAP.md: Sơ đồ các lớp và hàm trong mã nguồn.
  - GEM_CODE_SNIPPETS.md: Thư viện mã mẫu chuẩn.
  - GEM_DATA_FLOW.md: Mô tả luồng dữ liệu Production -> Staging -> Datamart.
  - GEM_DB_SCHEMAS.md: Chi tiết cấu trúc bảng và schema database.
  - GEM_AUTO_PIPELINE.md: Chi tiết vận hành engine chạy tự động.
  - GEM_DEPENDENCY_GRAPH.md: Đồ thị mối quan hệ giữa các module.
  - GEM_ERROR_CONTEXT.md: Bối cảnh và cách xử lý các mã lỗi (E-ID).
- /src: Mã nguồn chính của hệ thống, phân tách giữa Core logic và Job thực thi.
- /src/db/templates/sql: Nơi lưu trữ duy nhất các script SQL, tránh viết cứng SQL trong code Python.

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