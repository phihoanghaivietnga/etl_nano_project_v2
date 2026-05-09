# ĐẶC TẢ YÊU CẦU NGHIỆP VỤ Y TẾ

## 1. Mục tiêu
- Chuẩn hóa quy trình ETL dữ liệu y tế từ nguồn vận hành vào kho phân tích.
- Bảo đảm dữ liệu đầy đủ, nhất quán, truy vết được theo từng lần chạy.

## 2. Phạm vi nghiệp vụ
- Thu nhận dữ liệu từ hệ thống nguồn theo danh mục bảng cấu hình.
- Làm sạch, chuẩn hóa và đồng bộ vào tầng Staging.
- Nạp dữ liệu sang Datamart phục vụ báo cáo và đối soát.

## 3. Vai trò người dùng
- Quản trị hệ thống: cấu hình kết nối, vận hành lịch chạy, theo dõi log.
- Người vận hành ETL: chạy thủ công, kiểm tra trạng thái, xử lý lỗi.
- Người khai thác báo cáo: xác nhận dữ liệu đầu ra theo kỳ.

## 4. Yêu cầu chức năng chính
- Cho phép chạy ETL theo nhóm bảng hoặc toàn bộ bảng.
- Kiểm soát sai khác theo cơ chế checksum/điều kiện đồng bộ.
- Ghi nhận log đầy đủ: thời gian chạy, số bản ghi, trạng thái thành công/thất bại.
- Hỗ trợ đồng bộ tri thức vận hành lên Google Drive.

## 5. Yêu cầu phi chức năng
- Tính tin cậy: có cơ chế retry và báo lỗi rõ ràng.
- Tính an toàn: không công khai thông tin nhạy cảm (token, credentials, biến môi trường).
- Hiệu năng: chỉ đồng bộ phần thay đổi để giảm thời gian chạy.

## 6. Tiêu chí nghiệm thu
- Luồng ETL chạy ổn định theo cấu hình hiện hành.
- Kết quả dữ liệu tại Datamart khớp quy tắc nghiệp vụ đã định nghĩa.
- Tài liệu vận hành và tri thức kỹ thuật được cập nhật đồng bộ.