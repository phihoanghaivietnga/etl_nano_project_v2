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