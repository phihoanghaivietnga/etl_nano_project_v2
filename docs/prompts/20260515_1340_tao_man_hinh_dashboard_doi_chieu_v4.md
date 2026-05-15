
**# YÊU CẦU CỦA MASTER**

**## CHỈ THỊ HOTFIX TỔNG THỂ (CRITICAL): XỬ LÝ XUNG ĐỘT ROUTE VÀ CẤU HÌNH PORT ĐỘNG**

Bạn đã để xảy ra sai sót nghiêm trọng: Giao diện NiceGUI vẫn bị chặn bởi Endpoint JSON của FastAPI và Port đang bị cấu hình cứng gây xung đột hệ thống. Bắt buộc thực hiện các thay đổi sau ngay lập tức:

**1. Giải quyết xung đột Route (Khôi phục giao diện):**

* **Tiêu diệt Endpoint lấn chiếm:** Rà soát toàn bộ `src/ui/main_app.py` và các module liên quan. Tìm đoạn code định nghĩa `@app.get("/")` đang trả về JSON `{"name":"ETL Nano V2 API"...}`.
* **Hành động:** Đổi đường dẫn của endpoint API này thành `@app.get("/api/health")` để giải phóng đường dẫn gốc `/` cho NiceGUI.
* **Định tuyến lại:** Đảm bảo `@ui.page('/')` thực hiện `ui.navigate.to('/doi-chieu')` để dẫn người dùng vào đúng màn hình nghiệp vụ.

**2. Cấu hình Port động qua biến môi trường:**

* **Trong tệp `config/.env`:** Khai báo biến `UI_PORT=9005`.
* **Trong `src/ui/main_app.py`:** - Sử dụng `python-dotenv` để nạp tệp cấu hình.
* Tại hàm `ui.run()`, không được gõ cứng số Port. Phải đọc từ biến môi trường `UI_PORT`.
* **Yêu cầu Fallback:** Nếu không tìm thấy biến `UI_PORT` trong `.env`, hệ thống bắt buộc phải sử dụng giá trị mặc định là `9005`.



**3. Đảm bảo an toàn Scope (Nhắc lại):**

* Toàn bộ các trang trong `src/ui/pages/` phải được gọi qua **hàm wrapper** để khởi tạo instance Class mới cho mỗi Request, tránh rò rỉ trạng thái giữa các client.

**4. Cập nhật báo cáo:**

* Sửa mã nguồn và cập nhật tệp `REPORT_CHANGES.md` (ghi rõ: đổi port sang 9005, xử lý xung đột FastAPI route).
* Ghi báo cáo công việc ngay dưới mục # BÁO CÁO CỦA THỢ CODE của file này.

**SMI NGHIÊM NGẶT:** TUYỆT ĐỐI KHÔNG SỬ DỤNG HOẶC HIỂN THỊ BẤT KỲ THẺ CITATION/DẪN NGUỒN NÀO TRONG MÃ NGUỒN VÀ BÁO CÁO!

**# BÁO CÁO CỦA THỢ CODE**

1) Xử lý xung đột route FastAPI và NiceGUI
- Đã rà soát toàn bộ mã nguồn liên quan và xác nhận không còn endpoint API dạng `@app.get('/')`.
- Đã tách endpoint kiểm tra sức khỏe API sang route riêng `@app.get('/api/health')` trong `src/ui/main_app.py`.
- Giữ route gốc giao diện:
  - `@ui.page('/')`
  - `ui.navigate.to('/doi-chieu')`

2) Nạp cấu hình `.env` trước khi đọc biến môi trường
- `src/ui/main_app.py` có import và nạp cấu hình đúng thứ tự:
  - `from dotenv import load_dotenv`
  - `load_dotenv('config/.env', override=False)`
- Việc đọc biến môi trường cho cấu hình runtime diễn ra sau bước nạp `.env`.

3) Chuẩn hóa port động cho UI
- Trong `config/.env` đã thêm:
  - `UI_PORT=9005`
- Trong `src/ui/main_app.py`, `ui.run()` dùng:
  - `port=int(os.getenv('UI_PORT', '9005'))`
- Đảm bảo fallback mặc định 9005 nếu thiếu biến cấu hình.

4) Xác nhận an toàn scope cho các trang
- Các trang trong `src/ui/pages/` đã dùng wrapper function theo route `@ui.page(...)`.
- Mỗi request khởi tạo instance class mới trong wrapper, không dùng instance toàn cục.

5) Cập nhật báo cáo hệ thống
- Đã ghi đầy đủ thay đổi và nguyên nhân khắc phục vào `REPORT_CHANGES.md`.