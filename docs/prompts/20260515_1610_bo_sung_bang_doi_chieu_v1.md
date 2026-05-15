
**# YÊU CẦU CỦA MASTER**

**## CHỈ THỊ NÂNG CẤP HỆ THỐNG (FEATURE UPGRADE): MỞ RỘNG DIMENSION & DYNAMIC COLUMNS**

Hệ thống cần được mở rộng để đối chiếu thêm các danh mục và hỗ trợ hiển thị đa cột doanh thu. Ngươi BẮT BUỘC phải thực hiện chính xác các yêu cầu sau, tuyệt đối không được tự ý "cầm đèn chạy trước ô tô" sửa những phần không được phép.

**1. Tạo Template SQL cho 4 bảng Dimension mới:**
- **Danh sách Domain cần tạo:** `dim_benh`, `dim_benh_nhan`, `dim_dich_vu`, `dim_loai_goi_dich_vu`.
- **Cấu trúc thư mục:** Tạo đủ 3 file `production.sql`, `staging.sql`, `datamart.sql` cho từng domain trong thư mục `src/db/templates/sql/dashboard_doichieu/`.
- **Luật viết SQL bắt buộc (Full Load Count):**
  - Vì giao diện dùng chung một cơ sở hạ tầng truyền tham số ngày tháng, ngươi BẮT BUỘC phải khai báo `DECLARE @TuNgay DATE = ?;` và `DECLARE @DenNgay DATE = ?;` ở đầu file để hứng marker `?` từ Python.
  - TUYỆT ĐỐI KHÔNG sử dụng `@TuNgay` và `@DenNgay` trong mệnh đề `WHERE`. Các bảng Dim này phải được `COUNT(1)` toàn bộ dữ liệu.
  - Alias cột kết quả BẮT BUỘC phải bọc trong ngoặc vuông: `AS [RowCount]`.
  
*Ví dụ mẫu cho `dim_benh/staging.sql`:*
```sql
SET NOCOUNT ON;
DECLARE @TuNgay DATE = ?;
DECLARE @DenNgay DATE = ?;

SELECT COUNT(1) AS [RowCount]
FROM {staging_schema}.DimBenh WITH (NOLOCK);

```

**2. GIỚI HẠN PHẠM VI (CRITICAL BORDER):**

* TUYỆT ĐỐI KHÔNG ĐƯỢC CHẠM VÀO hay sinh lại bất kỳ file SQL nào thuộc về `dim_luot_kham` và `fact_thu_phi_dich_vu`. Master đã tự tay tối ưu hoàn hảo các file này. Nếu ngươi tự ý ghi đè, toàn bộ kết quả sẽ bị hủy bỏ.

**3. Nâng cấp Giao diện UI (`DoiChieuPage`):**

* Thêm 4 domain Dimension mới vào danh sách Dropdown/Select để người dùng có thể chọn đối chiếu.
* **Render Cột Động (Dynamic Columns):** Hiện tại UI đang hardcode chỉ hiển thị cột `RowCount`. Master đã nâng cấp SQL của `fact_thu_phi_dich_vu` để trả về thêm các cột như `[TongTien]`, `[TongTienSauTangGiam]`. Ngươi phải viết lại logic render bảng (Table/DataGrid) trong NiceGUI sao cho:
* Tự động quét các Keys trong Dictionary kết quả trả về từ cơ sở dữ liệu.
* Tự động sinh ra các cột tương ứng trên giao diện (Ví dụ: Cột `RowCount`, Cột `TongTien`, Cột `TongTienSauTangGiam`).
* Nếu kết quả trả về giá trị `None` (do cơ sở dữ liệu trống), logic Python phải ép về `0` trước khi hiển thị/cộng dồn.



**4. Cập nhật Báo cáo:**

* Sinh các file SQL mới và sửa mã nguồn UI.
* Ghi chú các thay đổi (thêm 4 Dim, hỗ trợ Dynamic Columns) vào `REPORT_CHANGES.md`.
* Ghi báo cáo công việc ngay dưới mục # BÁO CÁO CỦA THỢ CODE trong tệp prompt hiện tại.

**SMI NGHIÊM NGẶT:** TUYỆT ĐỐI KHÔNG SỬ DỤNG HOẶC HIỂN THỊ BẤT KỲ THẺ CITATION/DẪN NGUỒN NÀO TRONG MÃ NGUỒN VÀ BÁO CÁO!

**# BÁO CÁO CỦA THỢ CODE**