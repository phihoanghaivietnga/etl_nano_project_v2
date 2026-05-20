
**# YÊU CẦU CỦA MASTER**
Khắc phục khẩn cấp lỗi lệch Schema BCP (Error 22005) bằng kỹ thuật Masking NULL trong Dynamic SELECT và vá lỗ hổng bảo mật rò rỉ Connection String.

1. **Bắt buộc đọc:**

* `GEM_TECHNICAL_STANDARDS.md` (Phần tiêu chuẩn an toàn bảo mật và bảo toàn Schema).
* `GEM_ERROR_CONTEXT.md` (Bổ sung mã lỗi BCP 22005).
* `GEM_CODE_MAP.md` (Bổ sung mã lỗi BCP 22005).

2. **Yêu cầu chi tiết:**

* **Sửa lỗi lệch Schema (BCP Error 22005) bằng OOP Python:**
* Mở class `BaseExtractor` (hoặc module sinh query).
* Viết lại logic duyệt qua `INFORMATION_SCHEMA.COLUMNS`. Nếu cột thuộc danh sách `exclude_datatypes`, **tuyệt đối không được bỏ qua cột đó**.
* Phải sinh ra chuỗi thay thế: `CAST(NULL AS VARCHAR(1)) AS [TenCot] ` (hoặc đơn giản là `NULL AS [TenCot]`).
* Đối với các cột không bị loại trừ, giữ nguyên `[TenCot]`.
* Mục tiêu: Danh sách cột trả về từ query phải khớp 100% (cả số lượng và vị trí) với bảng Staging đích để BCP IN không bị xô lệch dữ liệu.


* **Vá lỗ hổng bảo mật (Sanitize Logging):**
* Quét toàn bộ mã nguồn (đặc biệt trong `src/core/db/connection.py`, `extractor.py`, `loader.py`).
* Xóa toàn bộ các lệnh `print()` hoặc `logger` có chứa biến `connection_string`, mật khẩu, hoặc thông tin nhạy cảm.
* Chỉ được log định dạng an toàn (Ví dụ: `Connected to Database [Ten_DB] at Server [Ten_Server] successfully`).


* **Ràng buộc tiêu chuẩn hiện hành:**
* Vẫn giữ nguyên cơ chế BCP `-w` (UTF-16-LE) để bảo tồn tiếng Việt (SMI-2).
* Vẫn phải đảm bảo hàm kiểm duyệt Python (Regex) `validate_sql_revenue_rules()` đang hoạt động để bảo vệ logic Fallback Doanh Thu `COALESCE` (SMI-3).



3. **Kết quả đối soát:**

* Cung cấp Output mẫu của câu lệnh Dynamic SELECT MỚI (phải chứa các cột bị loại trừ dưới dạng `NULL AS [TenCot]`) để AI Test kiểm tra độc lập.
* Trích xuất dòng code thay đổi trong module connection chứng minh đã gỡ bỏ log nhạy cảm.

4. **Cập nhật tri thức:**

* Cập nhật lỗi `22005 (BCP Schema Shift)` và cách giải quyết (Masking NULL) vào `GEM_ERROR_CONTEXT.md`.
* Ghi nhận tiêu chuẩn bảo mật "Không log connection string" vào `GEM_TECHNICAL_STANDARDS.md`.
* Cập nhật thông tin liên quan có thay đổi vào `GEM_CODE_MAP.md`.
* **Bắt buộc:** Ghi chép (Log) sự kiện thay đổi kiến trúc quan trọng này vào `PROJECT_CHRONICLE.md` với đầy đủ ngày tháng, lý do thay đổi và danh sách module bị ảnh hưởng.

5. **Kết xuất báo cáo:**

* Liệt kê các file bị tác động vào tệp `REPORT_CHANGES.md`.

6. **Chỉ dẫn phản hồi:**
Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.

**# BÁO CÁO CỦA THỢ CODE**

## 1) Các hạng mục đã hoàn thành

### 1.1. Vá lỗi lệch Schema BCP 22005 bằng Masking NULL trong Dynamic SELECT
- Đã sửa `src/core/base_extractor.py` theo hướng OOP:
  - Không còn loại cột thuộc `exclude_datatypes`.
  - Cột thuộc datatype loại trừ được mask bằng `CAST(NULL AS VARCHAR(1)) AS [TenCot]`.
  - Cột hợp lệ giữ nguyên `[TenCot]`.
  - Bảo toàn thứ tự cột theo `INFORMATION_SCHEMA.COLUMNS.ORDINAL_POSITION`.
- Đã bổ sung cấu trúc DTO:
  - `DynamicColumnProjection`
  - mở rộng `ExtractPlan` thêm `projected_columns`.

### 1.2. Vá lỗ hổng bảo mật log kết nối
- Đã sanitize log trong `src/core/base_loader.py`:
  - Gỡ log in trực tiếp command/query BCP.
  - Thay bằng log an toàn, không chứa dữ liệu nhạy cảm.

### 1.3. Giữ ràng buộc SMI-2 và củng cố SMI-3
- SMI-2: Giữ nguyên cơ chế BCP `-w` (UTF-16-LE), không thay đổi.
- SMI-3: Bổ sung guard `validate_sql_revenue_rules()` trong `src/jobs/fact_loader.py`:
  - Dùng Regex để kiểm duyệt fallback doanh thu `COALESCE/ISNULL` trước khi chạy SQL template doanh thu.

## 2) Output mẫu Dynamic SELECT mới (để AI Test)

Ví dụ với bảng `ThuPhiDichVu`, giả sử `xml` và `text` nằm trong `exclude_datatypes`:

```sql
SELECT [MaHoSo], [MaChiTieu], CAST(NULL AS VARCHAR(1)) AS [NoiDungXML], [NgayDenKham], CAST(NULL AS VARCHAR(1)) AS [GhiChuText]
FROM dbo.[ThuPhiDichVu] WITH (NOLOCK)
WHERE CAST([NgayDenKham] AS DATE) >= '2026-05-19'
AND CAST([NgayDenKham] AS DATE) <= '2026-05-20'
```

Output này thể hiện rõ:
- Cột bị loại trừ datatype vẫn giữ nguyên vị trí trong projection.
- Dùng NULL mask để không làm lệch số lượng/thứ tự cột khi BCP IN.

## 3) Trích xuất dòng code chứng minh đã gỡ log nhạy cảm

Tại `src/core/base_loader.py` (hàm `run_bcp_utf16le`):

```python
self._log("Thực thi BCP UTF-16-LE (đã ẩn nội dung query/command để bảo mật)")
```

Dòng trên thay cho kiểu log cũ in raw command/query, giúp tránh lộ thông tin kết nối và dữ liệu nhạy cảm.

## 4) Cập nhật tri thức đã thực hiện

- `docs/knowledge/GEM_ERROR_CONTEXT.md`:
  - Bổ sung `E-ETL-22005: BCP Schema Shift` + nguyên nhân + cách xử lý Masking NULL.
- `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`:
  - Bổ sung chuẩn “không log connection string / thông tin nhạy cảm”.
  - Cập nhật chuẩn Dynamic SELECT mới theo cơ chế masking NULL.
- `docs/knowledge/GEM_CODE_MAP.md`:
  - Cập nhật cấu phần mới trong `BaseExtractor` và guard `validate_sql_revenue_rules()`.
- `PROJECT_CHRONICLE.md`:
  - Ghi nhận ADR-23, ADR-24, ADR-25 cho đợt hotfix 2026-05-20.

## 5) Danh sách file bị tác động

- `src/core/base_extractor.py`
- `src/core/base_loader.py`
- `src/jobs/fact_loader.py`
- `docs/knowledge/GEM_ERROR_CONTEXT.md`
- `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`
- `docs/knowledge/GEM_CODE_MAP.md`
- `PROJECT_CHRONICLE.md`
- `REPORT_CHANGES.md`
- `docs/prompts/20260519_1710_sync_incremental_v2.md`
