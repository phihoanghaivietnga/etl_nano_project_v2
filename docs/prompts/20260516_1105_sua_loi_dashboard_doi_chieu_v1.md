
**# YÊU CẦU CỦA MASTER**

**## CHỈ THỊ KHẮC PHỤC LỖI BACKEND MAPPING (CRITICAL BUG FIX)**

Master đã rà soát Tầng tri thức trên Google Drive và phát hiện mã nguồn xử lý dữ liệu của ngươi đang phạm phải các sai lầm kiến trúc nghiêm trọng khiến giao diện hiển thị sai lệch số liệu (toàn bộ bằng 0). 

Bắt buộc thực hiện sửa đổi ngay lập tức tệp `src/ui/dashboard_app.py` theo các tiêu chuẩn sau:

**1. Sửa hàm gộp số liệu `_merge_numeric`:**
- Ngươi đang dùng `isinstance(value, (int, float))` khiến toàn bộ kiểu dữ liệu `decimal.Decimal` do pyodbc trả về từ các lệnh SQL SUM bị loại bỏ hoàn toàn.
- **SỬA NGAY THÀNH:** Hỗ trợ ép kiểu cho cả `decimal.Decimal`.
  *Ví dụ chuẩn:*
  ```python
  from decimal import Decimal
  if isinstance(value, (int, float, Decimal)) and value is not None:
      total[key] = total.get(key, 0.0) + float(value)

```

**2. Chuẩn hóa trích xuất dữ liệu đa nguồn (Production, Staging, Datamart):**

* Rà soát kỹ cấu trúc dữ liệu trả về trong hàm `compare_domain`:
* `prod_result` và `stg_result` là Dict, phải lấy từ `["values"]`.
* `dm_result` là List, phải lấy dòng đầu tiên `dm_result[0]` trước khi `.get()`.


* Đảm bảo ánh xạ chính xác tuyệt đối theo chữ HOA/thường của 2 phím kết quả từ SQL: `TongTien` và `TongTienSauTangGiam`. Xóa bỏ hoàn toàn các tàn dư của `TotalRevenue`.

**3. Ghi báo cáo tiến độ:**

* Sau khi số liệu nảy đầy đủ trên màn hình Multi-Grid, cập nhật nguyên nhân lỗi gộp Decimal này vào `REPORT_CHANGES.md`.
* Ghi báo cáo công việc ngay dưới mục # BÁO CÁO CỦA THỢ CODE trong tệp prompt hiện hành.

SMI: TUYỆT ĐỐI KHÔNG SỬ DỤNG HOẶC HIỂN THỊ THẺ CITATION/DẪN NGUỒN TRONG MÃ NGUỒN VÀ BÁO CÁO!

**# BÁO CÁO CỦA THỢ CODE**

Đã hoàn tất hotfix backend mapping theo chỉ thị.

Các việc đã làm:

1) Vá lỗi gộp số liệu Decimal trong `src/ui/dashboard_app.py`
- Bổ sung `from decimal import Decimal`.
- Sửa `_merge_numeric` để nhận kiểu `(int, float, Decimal)`.
- Sửa `_normalize_metric_map` để nhận kiểu `(int, float, Decimal)`.
- Giữ quy tắc chuẩn hóa `None -> 0.0`.

2) Chuẩn hóa mapping đa nguồn Production/Staging/Datamart
- `prod_result` và `stg_result` tiếp tục lấy đúng từ `['values']`.
- `dm_result` được xử lý an toàn chống rỗng:
  - `dm_data = dm_result[0] if dm_result else {}`
- Đã rà soát và xác nhận không còn tàn dư `TotalRevenue`.
- Mapping giữ đúng key phân biệt hoa/thường theo SQL:
  - `TongTien`
  - `TongTienSauTangGiam`

3) Bổ sung traceback bắt buộc
- Thêm `import traceback`.
- Tại các nhánh lỗi của Production, Staging, Datamart và lỗi tổng hợp domain đều có `traceback.print_exc()` để in đầy đủ stack trace ra terminal.

4) Cập nhật báo cáo hệ thống
- Đã ghi nguyên nhân gốc và hướng khắc phục vào `REPORT_CHANGES.md`:
  - Lỗi bỏ sót `decimal.Decimal` trong pipeline gộp SUM từ pyodbc.
  - Bổ sung chống crash khi Datamart trả rỗng.
  - Bổ sung logging traceback đầy đủ.
