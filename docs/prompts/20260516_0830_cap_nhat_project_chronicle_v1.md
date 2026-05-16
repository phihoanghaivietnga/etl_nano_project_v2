
**# YÊU CẦU CỦA MASTER**

**## CHỈ THỊ CẬP NHẬT BIÊN NIÊN SỬ DỰ ÁN (PROJECT CHRONICLE UPDATE)**

Ngươi đã tập trung viết code mà bỏ quên việc cập nhật `PROJECT_CHRONICLE.md`. Tài liệu này hiện đang dừng lại ở ngày 11/05 (giai đoạn hạ tầng).

BẮT BUỘC phải bổ sung ngay lập tức một mốc thời gian mới (Ví dụ: `## 2026-05-15: Giai đoạn Kiến trúc Dashboard V2`) và ghi nhận lại các Quyết định Kiến trúc (ADRs - Architectural Decision Records) cực kỳ quan trọng sau đây. 

Lưu ý: Chỉ ghi chép TƯ DUY KIẾN TRÚC và LÝ DO (TẠI SAO), tuyệt đối không ghi lắt nhắt như Changelog.

**Nội dung BẮT BUỘC phải tổng hợp vào Chronicle:**

1. **Kiến trúc Native OOP thay thế Client-Server (API):**
   - *Quyết định:* Khai tử cấu trúc gọi API qua HTTP (`API_URL`) để chuyển sang gọi trực tiếp logic Python thông qua `nicegui.run.io_bound`. 
   - *Lý do:* Tối ưu hóa hiệu năng Real-time, giảm độ trễ mạng nội bộ, và hợp nhất FastAPI/NiceGUI vào một tiến trình (Single Process) duy nhất để dễ quản lý.

2. **Quản trị Kết nối Cơ sở dữ liệu (DB Context Manager):**
   - *Quyết định:* Loại bỏ các kết nối DB vĩnh cửu (persistent connection). Bắt buộc sử dụng Context Manager (`get_db_context`) nạp chuỗi kết nối động từ `.env`.
   - *Lý do:* Chống rò rỉ bộ nhớ và ngăn tình trạng "treo" kết nối làm kiệt quệ tài nguyên máy chủ Production.

3. **Bảo vệ CSDL bằng Semaphore Toàn cục:**
   - *Quyết định:* Bọc `asyncio.gather` bằng một Semaphore (`MAX_CONCURRENT_CONNECTIONS`).
   - *Lý do:* Đảm bảo khi UI truy vấn đồng loạt hàng chục bảng/cơ sở, hệ thống sẽ xếp hàng tuần tự thay vì nã đạn DDOS làm sập Server Production.

4. **Cách ly Trạng thái Giao diện (Anti-State Leakage):**
   - *Quyết định:* Bắt buộc dùng hàm wrapper để bọc các class UI dưới decorator `@ui.page` (Khởi tạo instance mới cho mỗi request).
   - *Lý do:* Ngăn chặn thảm họa rò rỉ trạng thái (State Leakage) giữa các client/tab trình duyệt khác nhau trong NiceGUI.

5. **Giao diện Đa Lưới (Multi-Grid All-in-one):**
   - *Quyết định:* Xóa bỏ Dropdown chọn bảng, chuyển sang render Lưới Động (Dynamic Grids) hiển thị toàn bộ các bảng trên một màn hình theo thứ tự: Dim trước, Fact sau.
   - *Lý do:* Tránh xung đột logic lọc ngày tháng (Fact có ngày, Dim full-load) và giữ cho cấu trúc cột động của từng bảng không bị "rác" khi gộp chung.

**HÀNH ĐỘNG CỦA CODEX:**
- Đọc kỹ, dùng văn phong chuyên nghiệp, súc tích để cập nhật các ý trên vào `PROJECT_CHRONICLE.md`.
- Ghi báo cáo "Đã cập nhật Chronicle" vào ngay dưới mục # BÁO CÁO CỦA THỢ CODE trong tệp prompt hiện tại.

**SMI NGHIÊM NGẶT:** TUYỆT ĐỐI KHÔNG SỬ DỤNG HOẶC HIỂN THỊ BẤT KỲ THẺ CITATION/DẪN NGUỒN NÀO TRONG MÃ NGUỒN VÀ BÁO CÁO!

**# BÁO CÁO CỦA THỢ CODE**

Đã cập nhật Chronicle.

Nội dung đã thực hiện:
- Bổ sung mốc mới trong `PROJECT_CHRONICLE.md`:
  - `## 2026-05-15: Giai đoạn Kiến trúc Dashboard V2`
- Ghi nhận đầy đủ 5 ADR bắt buộc theo định dạng kiến trúc (Quyết định + Lý do):
  1. Native OOP thay thế mô hình gọi API HTTP nội bộ.
  2. DB Context Manager thay kết nối vĩnh cửu.
  3. Semaphore toàn cục bảo vệ truy vấn đồng thời.
  4. Wrapper `@ui.page` chống rò rỉ trạng thái giữa client.
  5. Multi-Grid All-in-one theo thứ tự Dim trước, Fact sau.
- Văn phong đã giữ ở mức chuyên nghiệp, súc tích, tập trung vào tư duy kiến trúc và lý do, không ghi dạng changelog chi tiết.