
**Role:** Đóng vai một Senior Frontend Developer & UI/UX Designer chuyên xây dựng Hệ thống Báo cáo Quản trị (BI Dashboard) cho ngành Y tế.
**Nhiệm vụ:** Thiết kế và code giao diện cho màn hình **"Dashboard Phân Tích Hành Vi & Giữ Chân Khách Hàng (Customer Retention Dashboard)"**.

**1. BỘ LỌC TỔNG THỂ (GLOBAL FILTERS)**

* **Time-range Picker:** Cho phép người dùng chọn khoảng thời gian tùy chỉnh (Từ ngày... Đến ngày...). Mặc định hiển thị dữ liệu của tháng hiện tại.
* **Nút Action:** Cần có nút "Áp dụng" (Apply) để gọi API làm mới số liệu và nút "Xuất Excel" (Export) để tải báo cáo tổng.

**2. KHỐI HIỂN THỊ CHỈ SỐ TỔNG QUAN (KPI CARDS - SUMMARY TIER)**
Hiển thị 5 thẻ KPI Cards đặt ngang nhau hoặc chia layout lưới hợp lý. Hai thẻ đầu là mẫu số gốc, ba thẻ sau là các chỉ số phân loại kèm Tỷ lệ phần trăm (So với Tổng bệnh nhân duy nhất).
*Yêu cầu UI/UX: 3 thẻ phân loại (Quay lại, Tái khám, Trung thành) phải có hiệu ứng Hover và có thể Click được (Clickable) để gọi API mở Popup chi tiết.*

* **Card 1 (Chỉ hiển thị số): Tổng số lượt khám.** (Đếm theo mã hồ sơ).
* **Card 2 (Chỉ hiển thị số): Tổng bệnh nhân duy nhất.** (Mẫu số gốc, đếm theo ID bệnh nhân).
* **Card 3 (Clickable): Khách Quay Lại (Cross-sell).** Hiển thị số lượng + Tỷ lệ %. Ghi chú tooltip: *"Khách cũ sử dụng dịch vụ mới"*.
* **Card 4 (Clickable): Khách Tái Khám (Follow-up).** Hiển thị số lượng + Tỷ lệ %. Ghi chú tooltip: *"Khách tuân thủ tái khám lâm sàng"*.
* **Card 5 (Clickable): Khách Trung Thành (Loyalty).** Hiển thị số lượng + Tỷ lệ %. Ghi chú tooltip: *"Khách dùng lặp lại cùng 1 Gói dịch vụ"*.

**3. KHỐI HIỂN THỊ CHI TIẾT (DRILL-DOWN POPUP / MODAL - DETAIL TIER)**
Khi người dùng Click vào Card 3, 4, hoặc 5, hệ thống bật lên một Modal/Popup toàn màn hình (hoặc Drawer trượt từ phải sang) hiển thị bảng Dữ liệu chi tiết (Data Grid) để đối soát.

**Logic hoạt động của Popup:**

* **Loading State:** Khi click, hiển thị Spinner/Skeleton trong lúc gọi API. Frontend phải truyền 3 Params xuống Backend: `{ StartDate, EndDate, LoaiBaoCao (QUAY_LAI / TAI_KHAM / TRUNG_THANH) }`.
* **Xác thực số liệu (Critical Validation):** Tổng số dòng (Rows) hiển thị trong bảng chi tiết này **BẮT BUỘC PHẢI KHỚP 100%** với con số tổng hiển thị ngoài KPI Card.
* **Cấu trúc Cột (Columns) của Data Grid:**
1. `Mã Bệnh Nhân` (Text)
2. `Tên Bệnh Nhân` (Text)
3. `Số Điện Thoại` (Text, có thể ẩn bớt số cuối nếu cần bảo mật)
4. `Ngày Khám Trong Kỳ` (Date format: DD/MM/YYYY)
5. `Tên Gói Dịch Vụ` (Text)
6. `Chi Tiết Dịch Vụ Mới Phát Sinh` (Text - Đặc biệt quan trọng cho tệp Khách Quay Lại để đối soát xem họ làm cái gì mới).
7. `Doanh Thu Ghi Nhận` (Number, format tiền tệ VNĐ).


* **Tính năng trong Popup:** Cho phép Search theo Tên/Mã BN, Phân trang (Pagination) nếu số lượng lớn, và Nút "Export CSV" riêng cho tập dữ liệu chi tiết này.

**4. RÀNG BUỘC KỸ THUẬT & TRẢI NGHIỆM (TECHNICAL & UX CONSTRAINTS)**

* Màu sắc: Sử dụng color palette phân biệt rõ 3 trạng thái. Ví dụ: Quay Lại (Blue), Tái Khám (Green), Trung Thành (Gold/Orange).
* Responsive: Đảm bảo bảng Data Grid có thể scroll ngang (Horizontal Scroll) trên màn hình nhỏ mà không bị vỡ layout.
* Hãy sinh ra mã giả (Mockup Code) bằng React/Tailwind (hoặc công nghệ tương ứng) để tôi xem trước bố cục.
