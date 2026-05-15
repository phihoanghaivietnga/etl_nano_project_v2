
**# YÊU CẦU CỦA MASTER**

1. **Bắt buộc đọc:**
    * `docs/knowledge/FINAL_SYSTEM_SPECIFICATION_V2.md`: Nắm rõ ranh giới 8 bảng, phân biệt Dimension (bỏ qua staging) và Fact (qua staging). Prepend ngặt nghèo `SET NOCOUNT ON;` trước lệnh SQL, quản lý giao dịch bằng Python (`autocommit=False`).
    * `GEM_CODE_MAP.md`: Đăng ký phân hệ UI vào nhóm **INTERFACE**.
    * `GEM_TECHNICAL_STANDARDS.md`: Áp dụng tiêu chuẩn BCP UTF-16-LE, fallback doanh thu.
    * **SMI CRITICAL RULE:** Tuyệt đối không bao giờ sử dụng hoặc hiển thị các thẻ dẫn nguồn/citation trong toàn bộ mã nguồn sinh ra cũng như các tài liệu báo cáo để tránh lỗi biên dịch hệ thống.

2. **Yêu cầu chi tiết:**
    * **Kiến trúc Lõi & Tái sử dụng (Code Reusability):** * Cả Auto Runner và Manual Runner phải dùng chung các Class nạp dữ liệu lõi kế thừa từ `BaseLoader` (đặt tại `src/core/base_loader.py`). 
        * Mọi thao tác nạp, BCP, và MERGE của 8 bảng nghiệp vụ phải được đóng gói gọn gàng bên trong phương thức thực thi của Class tương ứng (ví dụ: `execute_load()`).
    * **Kiến trúc UI (NiceGUI Native OOP):**
        * Toàn bộ mã nguồn giao diện phải viết theo mô hình OOP. Tạo lớp `BaseUI` tại `src/core/base_ui.py` để quản lý khung giao diện chung (Header, Navigation) và bọc các hàm tương tác DB chung. Các màn hình con kế thừa từ `BaseUI` và sử dụng decorator `@ui.page`.
    * **Màn hình 1 (Đối chiếu kết quả):**
        * Đọc file truy vấn tại `src/db/templates/sql/dashboard_doichieu/`.
        * Sử dụng marker `?` của `pyodbc` để truyền tham số ngày an toàn.
        * Nhóm Revenue (FactThuPhiDichVu) bắt buộc áp dụng: `SUM(ISNULL(TongTienSauTangGiam, TongTien))`.
        * **CRITICAL ASYNC RULE:** Thao tác query đối chiếu qua `pyodbc` phải được bọc trong `await nicegui.run.io_bound(...)` để không khóa Main Event Loop.
    * **Màn hình 2 (Chạy Job ETL thủ công - Manual Runner):**
        * Giao diện cho phép chọn Class lõi của bảng cần đồng bộ và mốc thời gian.
        * **Cơ chế Non-blocking Core:** Tuyệt đối không dùng `subprocess` để gọi file độc lập. Phải import Class lõi tương ứng vào UI và kích hoạt phương thức nạp thông qua Thread Pool nội bộ của NiceGUI bằng cú pháp: `await nicegui.run.io_bound(loader_instance.execute_load)` hoặc chạy luồng nền đẩy dữ liệu log qua `asyncio.Queue`.
        * Tích hợp thành phần `ui.log` để hứng và hiển thị log luân chuyển từ tiến trình ETL lõi lên giao diện theo thời gian thực (Real-time Streaming).
    * **Màn hình 3 (Lịch sử chạy Job):** Hiển thị danh sách kết quả, trạng thái Success/Failed từ các Job đã thực thi.
    * **Màn hình 4 (Báo cáo):** Khởi tạo Class giao diện trắng, chuẩn bị sẵn layout dọn đường tích hợp code từ V1.
    * **Tiêu chuẩn đóng gói:** Bổ sung thư viện `nicegui` vào cấu hình quản lý gói của **uv**.

3. **Kết quả đối soát:**
    * Cung cấp mã nguồn cấu trúc OOP của lớp giao diện chính (ví dụ `src/ui/dashboard_app.py`) thể hiện rõ việc import Class lõi và bọc qua `nicegui.run.io_bound`.
    * Cung cấp mẫu 01 file `.sql` hoàn chỉnh dùng để đối chiếu RowCount và SUM cho bảng `HoSoKhamBenhNgoaiTru` tương thích với marker `?`.

4. **Cập nhật tri thức:**
    * Cập nhật danh sách file UI và SQL template mới vào `GEM_CODE_MAP.md` (Nhóm INTERFACE).

5. **Kết xuất báo cáo:**
    * Ghi nhận toàn bộ thay đổi vào `REPORT_CHANGES.md`.

6. **Chỉ dẫn phản hồi:**
    * Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.

**# BÁO CÁO CỦA THỢ CODE**

- Đã tạo `src/core/base_ui.py` theo mô hình OOP:
  - Dựng khung layout dùng chung gồm Header và Navigation Drawer.
  - Cung cấp DB helper dưới dạng context manager `get_db_context()` để tạo kết nối `pyodbc` độc lập theo từng truy vấn và tự động đóng.
  - Bọc thao tác truy vấn bằng `await nicegui.run.io_bound(...)` để không block Main Event Loop.
  - Tự động prepend `SET NOCOUNT ON;` trước mỗi SQL runtime.

- Đã tạo `src/core/base_loader.py`:
  - Khai báo lớp cha `BaseLoader` cho Auto Runner và Manual Runner.
  - `execute_load()` quản lý transaction cấp Python với `autocommit=False`, commit khi thành công, rollback toàn cục khi lỗi.
  - Tích hợp hàm `run_bcp_utf16le(...)` sử dụng BCP cờ `-w` theo chuẩn UTF-16-LE.
  - Tạo `GenericTableLoader` kế thừa từ `BaseLoader` để UI gọi trực tiếp.

- Đã tạo `src/ui/dashboard_app.py` theo kiến trúc Native OOP + NiceGUI:
  - Màn hình 1: Đối chiếu kết quả theo SQL template, bind tham số marker `?`, gọi DB qua `run.io_bound`.
  - Màn hình 2: Manual Runner chọn bảng và thời gian, chạy loader bằng `await run.io_bound(loader.execute_load)`.
  - Màn hình 3: Lịch sử chạy job với trạng thái Success/Failed bằng màu.
  - Màn hình 4: Khung trang báo cáo trắng để dọn đường tích hợp logic V1.
  - Tích hợp `ui.log` + `asyncio.Queue` để streaming log theo thời gian thực từ loader.

- Đã tạo SQL mẫu đối chiếu tại `src/db/templates/sql/dashboard_doichieu/ho_so_kham_benh_ngoai_tru_doi_chieu.sql`:
  - Đối chiếu RowCount và SUM giữa 3 tầng `dbo`, `hanoi_hisnano_v2`, `dm`.
  - Dùng marker `?` chuẩn pyodbc cho khoảng thời gian.
  - Có logic fallback doanh thu `SUM(ISNULL(TongTienSauTangGiam, TongTien))` cho cụm Revenue.

- Đã cập nhật tri thức và báo cáo:
  - `docs/knowledge/GEM_CODE_MAP.md`: bổ sung các file UI/lõi/SQL template mới.
  - `REPORT_CHANGES.md`: ghi chi tiết các file tạo mới/cập nhật và module phụ thuộc liên quan.
