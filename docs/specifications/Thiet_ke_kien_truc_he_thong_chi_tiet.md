# THIẾT KẾ KIẾN TRÚC HỆ THỐNG CHI TIẾT

## 1. Tổng quan kiến trúc
- Hệ thống tổ chức theo các lớp: cấu hình, lõi xử lý, tác vụ ETL, giao diện vận hành và tầng tri thức.
- Luồng dữ liệu chính: Nguồn vận hành -> Staging -> Datamart.

## 2. Thành phần chính
- `config/`: quản lý biến môi trường, danh mục bảng và tham số vận hành.
- `src/core/`: lớp nền cho logging, kết nối, tiện ích dùng chung.
- `src/jobs/`: xử lý ETL theo từng nhóm bảng hoặc phiên chạy.
- `src/db/templates/sql/`: mẫu SQL chuẩn hóa cho nạp và đối soát dữ liệu.
- `src/ui/`: giao diện vận hành, giám sát và xác thực kết quả.
- `scripts/`: các tiện ích đồng bộ tri thức và tự động hóa ngoài luồng ETL chính.

## 3. Cơ chế đồng bộ tri thức
- Quét file từ thư mục gốc cấu hình.
- Lọc file theo `.gitignore` và blacklist cứng.
- Ánh xạ file vào nhóm tri thức nghiệp vụ.
- Gộp nội dung theo nhóm thành các file Master để phục vụ NotebookLM.
- Đối soát MD5 trước khi upload lên Google Drive.

## 4. Cơ chế bảo mật
- Dùng OAuth2 Desktop App cho Google Drive API.
- Token và credentials đặt trong `config/`, không đồng bộ lên Drive.
- Không ghi log giá trị nhạy cảm.

## 5. Nguyên tắc mở rộng
- Tách riêng cấu hình và logic xử lý.
- Mọi thay đổi luồng đồng bộ phải cập nhật đồng thời tài liệu tri thức.
- Ưu tiên đồng bộ sai khác để giảm chi phí vận hành.