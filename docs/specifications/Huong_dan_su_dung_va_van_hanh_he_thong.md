# HƯỚNG DẪN SỬ DỤNG VÀ VẬN HÀNH HỆ THỐNG

## 1. Chuẩn bị môi trường
- Cài đặt Python theo phiên bản dự án.
- Thiết lập biến cấu hình trong `config/.env`.
- Bảo đảm có file OAuth credentials trong `config/`.

## 2. Chạy quy trình ETL
- Chạy theo lệnh vận hành đã quy định trong dự án.
- Theo dõi log để kiểm tra trạng thái từng bước.
- Đối soát số bản ghi giữa nguồn, Staging và Datamart.

## 3. Đồng bộ tri thức lên Google Drive
- Sử dụng script `scripts/upload_to_drive_from_local.py`.
- Script sẽ tự:
  - Quét file trong phạm vi cấu hình.
  - Lọc `.gitignore` và các mục loại trừ cứng.
  - Ánh xạ nhóm và tạo file Master trong `temp_merged/`.
  - So sánh MD5 để chỉ upload phần thay đổi.

## 4. Xử lý lỗi thường gặp
- Lỗi cấu hình: kiểm tra `GDRIVE_FOLDER_ID` và `GDRIVE_ROOT_DIR`.
- Lỗi xác thực: kiểm tra file OAuth credentials và `config/token.json`.
- Lỗi đồng bộ: đọc log trạng thái `Error` để xác định file gây lỗi.

## 5. Quy tắc vận hành an toàn
- Không chỉnh sửa trực tiếp token khi hệ thống đang chạy.
- Không đẩy file nhạy cảm lên kho mã nguồn hoặc Drive dùng chung.
- Sau mỗi thay đổi kỹ thuật, cập nhật tài liệu tri thức và báo cáo thay đổi.