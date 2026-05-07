
**Tiêu đề: Thiết lập cấu trúc dự án ETL_Nano_Project_V2 và Tầng tri thức GEM**

**[VAI TRÒ]**
Bạn là một chuyên gia Data Engineer và Python Developer chịu trách nhiệm khởi tạo khung dự án (Boilerplate) cho hệ thống ETL phiên bản v2. Bạn phải làm việc dưới sự giám sát chặt chẽ của Tầng tri thức.

**[YÊU CẦU CẤU TRÚC THƯ MỤC]**
Hãy tạo cấu trúc thư mục sau tại thư mục gốc của dự án:
1. `/config`: Lưu các tệp cấu hình hệ thống (.yaml, .json).
2. `/docs/knowledge`: Lưu 9 tệp GEM tri thức.
3. `/docs/archive`: Lưu trữ tài liệu phiên bản cũ.
4. `/src/core`: Lưu mã nguồn lớp cha (Base Class), Database Connection, Logger.
5. `/src/jobs`: Lưu các logic đồng bộ bảng cụ thể kế thừa từ Core.
6. `/src/ui`: Lưu mã nguồn giao diện Streamlit (Runner và Verify).
7. `/src/db/templates/sql`: Nguồn duy nhất chứa các tệp .sql MERGE template.
8. `/tests`: Lưu các script kiểm thử độc lập.

**[YÊU CẦU TẠO TỆP TIN TRI THỨC]**
Hãy tạo các tệp .md sau với các quy định cụ thể:

**1. Tạo tệp `agents.md` tại thư mục gốc với nội dung đầy đủ sau:**
```markdown
# CHIẾN LƯỢC ĐIỀU PHỐI HỆ THỐNG AGENTS

## 1. Vai trò
- Gem (Kiến trúc sư): Điều phối, ra lệnh và giám sát dựa trên Tầng tri thức.
- Codex (Thợ code): Thực thi lập trình, sửa lỗi và cập nhật tài liệu.

## 2. Giao thức làm việc
- Bước 1: Trước khi sửa code, Codex bắt buộc phải đọc các tệp GEM_xxx.md liên quan để nắm ngữ cảnh.
- Bước 2: Thực hiện sửa đổi mã nguồn.
- Bước 3: Cập nhật đúng và đủ các thay đổi vào Tầng tri thức (GEM_xxx.md) để đảm bảo tính nhất quán.
- Bước 4: Kết xuất báo cáo vào tệp REPORT_CHANGES.md tại thư mục gốc.

## 3. Quy tắc bắt buộc
- Ngôn ngữ: Tiếng Việt rõ ràng, ngắn gọn, cô đọng.
- Hình thức: Không sử dụng icon trong mọi tệp tài liệu .md.
- Kỹ thuật: Mọi mã nguồn phải theo hướng đối tượng (OOP), kế thừa từ Base Class tại src/core.
```

**2. Tạo tệp `README.md` tại thư mục gốc với nội dung đầy đủ sau:**
```markdown
# ETL NANO PROJECT V2

## 1. Mục đích hệ thống
Hệ thống ETL phiên bản v2 được thiết kế để chuẩn hóa luồng dữ liệu từ Production sang Datamart theo kiến trúc Modular và lập trình hướng đối tượng (OOP). Hệ thống đảm bảo tính thống nhất giữa chế độ chạy Tự động (Auto) và Thủ công (Manual).

## 2. Cấu trúc thư mục
- /config: Chứa settings.yaml và tables.yaml để cấu hình hệ thống và danh sách bảng.
- /docs/knowledge: Tầng tri thức cốt lõi chứa 9 file GEM điều phối.
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
```

**3. Tạo 9 tệp GEM trong thư mục `/docs/knowledge/`:**
- Các tệp bao gồm: `GEM_NAVIGATION.md`, `GEM_GUIDE.md`, `GEM_CODE_MAP.md`, `GEM_CODE_SNIPPETS.md`, `GEM_DATA_FLOW.md`, `GEM_DB_SCHEMAS.md`, `GEM_AUTO_PIPELINE.md`, `GEM_DEPENDENCY_GRAPH.md`, `GEM_ERROR_CONTEXT.md`.
- **Yêu cầu:** Các tệp này khởi tạo là tệp trắng (chỉ có tiêu đề đầu trang), sẽ được bổ sung nội dung chi tiết trong quá trình thực thi các task tiếp theo.

**[HÀNH ĐỘNG]**
Hãy thực thi việc tạo thư mục và ghi nội dung vào các file nêu trên ngay bây giờ. Xác nhận sau khi hoàn thành.
