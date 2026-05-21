
**# YÊU CẦU CỦA MASTER**
Khắc phục khẩn cấp lỗi "BCP copy in failed" (Mã 22005) do xung đột kiểu dữ liệu. Bắt buộc thay đổi kỹ thuật Masking NULL sang định dạng Unicode diện rộng để tương thích tuyệt đối với cờ BCP -w.

1. **Bắt buộc đọc:**

* `GEM_ERROR_CONTEXT.md`
* `GEM_TECHNICAL_STANDARDS.md`
* `PROJECT_CHRONICLE.md`

2. **Yêu cầu chi tiết:**

* **Sửa mã nguồn `src/core/base_extractor.py` (OOP):**
* Tìm đến hàm xử lý `exclude_datatypes` trong quá trình sinh Dynamic SELECT.
* **Xóa bỏ ngay lập tức** chuỗi `CAST(NULL AS VARCHAR(1)) AS [TenCot]`.
* **Thay thế bắt buộc bằng:** `CAST(NULL AS NVARCHAR(MAX)) AS [TenCot]`.
* Đảm bảo danh sách cột (`physical_columns` và `select_projections`) khớp 100% về số lượng và vị trí.


* **Ràng buộc tiêu chuẩn cốt lõi:**
* Tuyệt đối giữ nguyên cờ `-w` (UTF-16-LE) cho lệnh BCP để bảo vệ từ vựng y khoa tiếng Việt.
* Mọi thao tác quản lý package (nếu phát sinh) bắt buộc phải dùng **uv** (Astral), nghiêm cấm dùng `pip` hay `conda`.



3. **Kết quả đối soát:**

* In ra màn hình Terminal câu lệnh Dynamic SELECT mới, trong đó thể hiện rõ việc đã sử dụng `NVARCHAR(MAX)` cho các cột bị loại trừ.
* In ra một dòng log chứa dữ liệu tiếng Việt (ví dụ: "nhược thị", "lượt khám") sau khi chạy qua luồng BCP để chứng minh không bị lỗi font (Tiêu chuẩn SMI-2).

4. **Cập nhật tri thức (BẮT BUỘC):**

* **`GEM_ERROR_CONTEXT.md`**: Sửa lại nội dung hướng dẫn khắc phục lỗi 22005. Xóa bỏ ví dụ `VARCHAR(1)` sai trái, cập nhật thành `CAST(NULL AS NVARCHAR(MAX))` để tương thích với BCP `-w`.
* **`GEM_TECHNICAL_STANDARDS.md`**: Cập nhật tiêu chuẩn sinh Dynamic SELECT, nhấn mạnh việc ép kiểu Unicode (`NVARCHAR`) khi che giấu cột (Masking NULL).
* **`PROJECT_CHRONICLE.md`**: Ghi rõ khoản Nợ kỹ thuật (Technical Debt) bằng dòng chữ: *"Cảnh báo rủi ro: Đã gỡ bỏ cơ chế Validate SQL Fallback Doanh Thu (COALESCE) bằng Python theo quyết định của Master. Luồng ETL hiện tại hoàn toàn tin tưởng vào các file SQL Template. Nếu file SQL bị sửa sai, hệ thống sẽ không thể tự động chặn lỗi."*

5. **Kết xuất báo cáo:**

* Liệt kê các file Python (.py) và tài liệu Markdown (.md) đã được chỉnh sửa vào tệp `REPORT_CHANGES.md`.

6. **Chỉ dẫn phản hồi:**
Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.

**# BÁO CÁO CỦA THỢ CODE**

## 1) Các hạng mục đã hoàn thành

### 1.1. Sửa BaseExtractor theo chuẩn Unicode Masking
- Đã cập nhật `src/core/base_extractor.py`:
  - Loại bỏ hoàn toàn biểu thức `CAST(NULL AS VARCHAR(1)) AS [TenCot]`.
  - Thay bằng `CAST(NULL AS NVARCHAR(MAX)) AS [TenCot]` cho các cột thuộc `exclude_datatypes`.
  - Giữ nguyên thứ tự cột theo `ORDINAL_POSITION`.
  - Bổ sung chốt kiểm tra `physical_columns` và `select_projections` khớp 100% số lượng.

### 1.2. Gỡ cơ chế validate Python fallback doanh thu theo quyết định Master
- Đã cập nhật `src/jobs/fact_loader.py`:
  - Gỡ `validate_sql_revenue_rules()`.
  - Gỡ toàn bộ hằng/import liên quan Regex guard fallback `COALESCE`.
  - Luồng ETL hiện chỉ thực thi SQL Template theo đúng chỉ thị.

### 1.3. Giữ nguyên chuẩn BCP UTF-16-LE
- Không thay đổi cờ `-w` trong luồng BCP hiện tại.

## 2) Kết quả đối soát

### 2.1. Dynamic SELECT mẫu có NVARCHAR(MAX)

```sql
SELECT [MaHoSo], CAST(NULL AS NVARCHAR(MAX)) AS [NoiDungXML], [NgayDenKham]
FROM dbo.[ThuPhiDichVu] WITH (NOLOCK)
WHERE CAST([NgayDenKham] AS DATE) >= '2026-05-19'
AND CAST([NgayDenKham] AS DATE) <= '2026-05-20'
```

### 2.2. Dòng log tiếng Việt đối soát SMI-2

```text
[SMI-2] Kiểm tra Unicode thành công: nhược thị | lượt khám
```

## 3) Cập nhật tri thức bắt buộc
- `docs/knowledge/GEM_ERROR_CONTEXT.md`:
  - Đã thay hướng dẫn lỗi 22005 sang `CAST(NULL AS NVARCHAR(MAX))`.
- `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`:
  - Đã cập nhật tiêu chuẩn Dynamic SELECT bắt buộc masking Unicode `NVARCHAR(MAX)`.
- `PROJECT_CHRONICLE.md`:
  - Đã thêm ADR-26 và ADR-27, bao gồm nguyên văn cảnh báo nợ kỹ thuật theo chỉ thị.

## 4) Danh sách file đã chỉnh sửa

### Python
- `src/core/base_extractor.py`
- `src/jobs/fact_loader.py`

### Markdown
- `docs/knowledge/GEM_ERROR_CONTEXT.md`
- `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`
- `PROJECT_CHRONICLE.md`
- `REPORT_CHANGES.md`
- `docs/prompts/20260519_1710_sync_incremental_v3.md`