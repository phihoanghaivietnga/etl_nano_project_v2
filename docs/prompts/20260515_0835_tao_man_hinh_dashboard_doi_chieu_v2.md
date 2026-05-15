
**# YÊU CẦU CỦA MASTER**

1. **Bắt buộc đọc:**
* `docs/knowledge/FINAL_SYSTEM_SPECIFICATION_V2.md`: Nhận thức rõ sự cô lập vật lý giữa máy chủ Production và máy chủ Datamart/Staging. Prepend ngặt nghèo `SET NOCOUNT ON;` trước lệnh SQL, quản lý giao dịch ở cấp độ Python (`autocommit=False`).
* `GEM_CODE_MAP.md`: Đăng ký toàn bộ phân hệ UI, Base Class và file SQL mới vào nhóm **INTERFACE**.
* `GEM_TECHNICAL_STANDARDS.md`: Tiêu chuẩn nạp dữ liệu BCP định dạng UTF-16-LE (cờ `-w`) và logic SQL Fallback doanh thu.
* **SMI CRITICAL RULE:** Tuyệt đối không bao giờ sử dụng hoặc hiển thị các thẻ dẫn nguồn/citation trong toàn bộ mã nguồn sinh ra cũng như các tài liệu báo cáo để tránh lỗi biên dịch hệ thống.


2. **Yêu cầu chi tiết:**
* **Quản lý Cấu hình & Chuỗi kết nối:**
* Hệ thống lưu cấu hình tại tệp `config/.env`. Bắt buộc nạp và sử dụng thông tin kết nối thông qua các biến môi trường: `PROD_CONNECTION_HANOI` (kết nối máy chủ Production cơ sở Hà Nội) và `DATAMART_CONNECTION_STRING` (dùng chung cho việc kết nối đến schema Staging và DataMart).
* Sau này có thêm nhiều cơ sở, mỗi cơ sở có 1 database riêng thì sẽ khai báo thêm các biến kết nối `PROD_CONNECTION_XXX` với XXX là tên cơ sở tương ứng


* **Kiến trúc Lõi & Tái sử dụng (Code Reusability):**
* Tạo khung `BaseLoader` tại `src/core/base_loader.py` dùng chung cho Auto Runner và Manual Runner.
* Phương thức `execute_load()` bọc trọn vẹn quy trình thực thi: Prepend `SET NOCOUNT ON;`, chạy lệnh BCP UTF-16-LE với cờ `-w`, bảo tồn tuyệt đối các thuật ngữ y tế tiếng Việt gốc, và chịu trách nhiệm tối cao về quản lý Transaction (`autocommit=False`, tự động commit nếu Success và rollback toàn cục nếu Failed).
* Bắt buộc tiêm cờ hiệu kết thúc (Poison Pill, ví dụ `None` hoặc chuỗi `"[DONE]"`) vào hàng đợi log sau khi hoàn tất tiến trình để ngắt luồng đọc log an toàn trên giao diện.


* **Kiến trúc UI (NiceGUI Native OOP):**
* Mã nguồn Python phải viết hoàn toàn theo hướng đối tượng (OOP). Tạo lớp `BaseUI` tại `src/core/base_ui.py` chịu trách nhiệm dựng layout chung (Header, Navigation Drawer).
* **CRITICAL DB HELPER RULE:** Lớp `BaseUI` tuyệt đối không lưu giữ đối tượng kết nối vĩnh cửu. Phải triển khai DB Helper dưới dạng Context Manager (`get_db_context(connection_string_var)`) nạp chuỗi kết nối tương ứng từ `.env` tùy theo ngữ cảnh máy chủ cần truy vấn, và tự động đóng kết nối khi truy vấn xong.
* Mọi thao tác I/O với cơ sở dữ liệu trên UI bắt buộc phải đẩy vào Background Task thông qua `await nicegui.run.io_bound(...)` nhằm bảo đảm giao diện Non-blocking tuyệt đối.
* Thiết lập 4 Class màn hình con độc lập kế thừa từ `BaseUI` và bọc định tuyến bằng decorator `@ui.page`.


* **Màn hình 1 (Đối chiếu kết quả):**
* Cơ chế đọc SQL: Nạp các script truy vấn từ thư mục phân cấp chuẩn: `src/db/templates/sql/dashboard_doichieu/<ten_bang>/` (<ten_bang> là tên bảng trong Datamart và theo quy định snake_case).
* Mỗi bảng nghiệp vụ cần đối chiếu phải khởi tạo đúng 3 script độc lập: `production.sql` (thực thi qua `PROD_CONNECTION_HANOI`), `staging.sql` và `datamart.sql` (thực thi qua `DATAMART_CONNECTION_STRING`).
* Sử dụng marker `?` của `pyodbc` để truyền tham số mốc thời gian một cách an toàn.
* Ứng dụng Backend Dashboard phải thực thi 3 câu truy vấn đối chiếu này một cách bất đồng bộ đồng thời thông qua `asyncio.gather` kết hợp `nicegui.run.io_bound` nhằm tối ưu hóa tốc độ tải và chống treo luồng.
* Đối với cụm Revenue (FactThuPhiDichVu), câu truy vấn SUM đối chiếu bắt buộc tuân thủ công thức chống NULL doanh thu: `SUM(ISNULL(TongTienSauTangGiam, TongTien))`.

* **Xử lý Đa cơ sở (Multi-tenant) cho Màn hình Đối chiếu:**
* Cơ chế gom Production: File `config/.env` sẽ định nghĩa nhiều biến kết nối nguồn (ví dụ `PROD_CONNECTION_HANOI`, `PROD_CONNECTION_HCM`). Lớp Backend UI phải đọc toàn bộ các biến có tiền tố `PROD_CONNECTION_`, sử dụng `asyncio.gather` để chạy cùng một file `production.sql` trên nhiều máy chủ, sau đó tổng hợp (SUM) kết quả RowCount/Doanh thu bằng logic Python trước khi render ra màn hình.
* Cơ chế Dynamic Staging Schema: Tệp `staging.sql` phải sử dụng template string của Python cho tên schema: `SELECT COUNT(1) FROM {staging_schema}.<TenBang>`. Trước khi execute bằng `pyodbc`, hàm Python phải đọc cấu hình list schema staging tương ứng và dùng hàm `.format(staging_schema=...)` để render câu lệnh SQL nội suy, tuyệt đối không hardcode tên schema trong file `.sql`.


* **Màn hình 2 (Chạy Job ETL thủ công - Manual Runner):**
* Giao diện cho phép chọn Class lõi của bảng cần đồng bộ và khoảng thời gian.
* Kích hoạt Non-blocking: Bắt buộc import Class lõi tương ứng vào UI và kích hoạt phương thức `execute_load()` thông qua Thread Pool nội bộ của NiceGUI (`await nicegui.run.io_bound`) hoặc luồng nền đẩy dữ liệu qua `asyncio.Queue`. Tuyệt đối không dùng `subprocess`.
* Tích hợp thành phần `ui.log` để hứng và hiển thị Streaming Log luân chuyển từ tiến trình ETL lõi lên giao diện theo thời gian thực.


* **Màn hình 3 (Lịch sử chạy Job):** Truy xuất và hiển thị danh sách lịch sử thực thi, làm nổi bật trạng thái Success/Failed bằng màu sắc giao diện tương ứng.
* **Màn hình 4 (Báo cáo):** Khởi tạo Class giao diện với khung trang trắng dọn đường cho việc tích hợp mã nguồn báo cáo từ bản V1.


3. **Kết quả đối soát:**
* Cung cấp trọn vẹn mã nguồn của `src/core/base_ui.py` thể hiện rõ logic nạp `.env`, Context Manager và bọc `nicegui.run.io_bound`.
* Cung cấp cấu trúc thư mục và nội dung 3 file `.sql` mẫu của bảng `dim_luot_kham` (đặt ngặt nghèo tại `src/db/templates/sql/dashboard_doichieu/dim_luot_kham/`). Script Staging bắt buộc trỏ vào schema đích đã làm giàu dữ liệu: `hanoi_hisnano_v2.HoSoKhamBenhNgoaiTru`.
* Cung cấp đoạn mã Backend trong `src/ui/dashboard_app.py` thực thi `asyncio.gather` đồng thời cho 3 kết nối đối chiếu.


4. **Cập nhật tri thức:**
* Cập nhật danh sách các file UI, Base Class và thư mục SQL template mới vào `GEM_CODE_MAP.md` (Nhóm INTERFACE).


5. **Kết xuất báo cáo:**
* Ghi nhận chi tiết danh sách file đã sửa/tạo và logic đã thay đổi vào `REPORT_CHANGES.md`.


6. **Chỉ dẫn phản hồi:**
* Ghi rõ dòng sau ở cuối phần yêu cầu: "Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE".



## **# BÁO CÁO CỦA THỢ CODE**

1) Đã cập nhật phụ thuộc hệ thống
- Đã cài `python-dotenv` bằng lệnh `uv add python-dotenv` để nạp `config/.env` chuẩn hóa.

2) Đã refactor `src/core/base_ui.py`
- Nạp `.env` qua `dotenv`.
- Triển khai `get_db_context(connection_string_var)` theo Context Manager, không giữ kết nối vĩnh cửu.
- Mọi truy vấn DB UI chạy qua `await nicegui.run.io_bound(...)`.
- Có prepend `SET NOCOUNT ON;`.
- Có Semaphore dùng chung toàn cục, đọc giới hạn từ `MAX_CONCURRENT_CONNECTIONS`, fallback = `5`.
- Có helper đọc `PROD_CONNECTION_*` và danh sách schema staging.

3) Đã refactor `src/core/base_loader.py`
- `execute_load(*args, **kwargs)` linh hoạt nhận tham số động.
- Transaction ở Python-level: `autocommit=False`, commit/rollback toàn cục.
- Chuẩn BCP UTF-16-LE cờ `-w`.
- Log queue thread-safe bằng `loop.call_soon_threadsafe(queue.put_nowait, msg)`.
- Luôn đẩy Poison Pill `[DONE]` trong `finally`.

4) Đã tách kiến trúc UI theo pages
- Entry mới: `src/ui/main_app.py` có khối khởi chạy:
  - `if __name__ in {"__main__", "__mp_main__"}:`
  - `ui.run(title=..., port=...)`.
- Tách 4 trang:
  - `src/ui/pages/doi_chieu_page.py`
  - `src/ui/pages/manual_runner_page.py`
  - `src/ui/pages/job_history_page.py`
  - `src/ui/pages/bao_cao_page.py`
- Có `src/ui/pages/common.py` và `src/ui/pages/__init__.py` để gom route.

5) Đã cập nhật Backend đối chiếu trong `src/ui/dashboard_app.py`
- Chạy đồng thời production/staging/datamart bằng `asyncio.gather(..., return_exceptions=True)`.
- Có xử lý lỗi từng nguồn, không để 1 nguồn lỗi làm sập toàn bộ kết quả.
- Có gom multi-tenant production từ toàn bộ `PROD_CONNECTION_*`.
- Có dynamic staging schema bằng `.format(staging_schema=...)`.
- Có validate consistency số marker `?` giữa 3 file SQL trong cùng domain.

6) Đã tạo SQL template theo cấu trúc chuẩn
- `src/db/templates/sql/dashboard_doichieu/dim_luot_kham/`
  - `production.sql`
  - `staging.sql` (trỏ `{staging_schema}.HoSoKhamBenhNgoaiTru`, mặc định schema giàu dữ liệu là `hanoi_hisnano_v2`)
  - `datamart.sql`
- `src/db/templates/sql/dashboard_doichieu/fact_thu_phi_dich_vu/`
  - `production.sql`
  - `staging.sql`
  - `datamart.sql`
- Công thức doanh thu đúng chuẩn nghiệp vụ: `SUM(ISNULL(TongTienSauTangGiam, TongTien))`.

7) Đã hoàn thiện Manual Runner theo tiêu chuẩn an toàn
- Lấy loop tường minh `loop = asyncio.get_running_loop()`.
- Gọi đúng mẫu: `await nicegui.run.io_bound(loader.execute_load, from_date, to_date, queue=log_queue, loop=loop)`.
- Bind tham số ngày bằng kiểu native `datetime.date` cho pyodbc marker `?`.
- Nút Run Job có cơ chế `.disable()` / `.enable()` chống spam.
- Vòng đọc `ui.log` break khi nhận `[DONE]`.

8) Đã cập nhật tri thức và báo cáo
- Cập nhật `docs/knowledge/GEM_CODE_MAP.md` nhóm INTERFACE với toàn bộ file mới.
- Cập nhật `REPORT_CHANGES.md` chi tiết file sửa/tạo và logic thay đổi.

Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE
