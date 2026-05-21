
**# YÊU CẦU CỦA MASTER**
Xử lý khẩn cấp lỗi 544 (IDENTITY_INSERT is set to OFF) khi nạp dữ liệu bằng PyODBC tại luồng Incremental Tầng 1. Bắt buộc mô phỏng lại cơ chế của cờ `-E` (Keep Identity) của BCP sang PyODBC một cách linh hoạt và an toàn thông qua việc kiểm tra động metadata của SQL Server.

### 1. Các file tài liệu bắt buộc phải cập nhật sau khi xử lý:

* `docs/knowledge/GEM_TECHNICAL_STANDARDS.md` (Bổ sung quy định mới tại mục nạp dữ liệu PyODBC: Bắt buộc phải kiểm tra `TableHasIdentity` và bọc khối `try...finally` để quản lý lệnh `SET IDENTITY_INSERT ON/OFF` mô phỏng cờ `-E` của BCP).
* `PROJECT_CHRONICLE.md` (Ghi nhận ADR: Xử lý sự cố lỗi ép kiểu tự tăng (544) khi chuyển đổi từ BCP sang PyODBC bằng cơ chế kích hoạt Identity Insert động).
* `REPORT_CHANGES.md` (Liệt kê chính xác file `src/jobs/fact_loader.py` đã được cập nhật logic).

### 2. Yêu cầu triển khai chi tiết cho Thợ code:

* **Vị trí cần can thiệp:** Tệp `src/jobs/fact_loader.py` (trong hàm thực thi nạp Tầng 1: `SELECT` -> `TRUNCATE` -> `executemany` vào bảng `stg_nano_v2`).
* **Bước 1 (Kiểm tra động):** Trước khi bắt đầu vòng lặp chunking `fetchmany()`, hãy sử dụng `cursor` của DB Đích (Staging) thực thi câu lệnh SQL sau để kiểm tra xem bảng đích có chứa cột IDENTITY hay không:
```sql
SELECT OBJECTPROPERTY(OBJECT_ID('stg_nano_v2.[TenBang]'), 'TableHasIdentity')

```


Nếu kết quả trả về `1`, gán một biến cờ `has_identity = True`.
* **Bước 2 (Mở khóa):** Nếu `has_identity == True`, thực thi lệnh `cursor.execute("SET IDENTITY_INSERT stg_nano_v2.[TenBang] ON")`.
* **Bước 3 (Thực thi an toàn):** Đưa toàn bộ vòng lặp `while True` chứa lệnh `cursor.executemany(insert_sql, chunk)` vào trong khối `try... finally`.
* **Bước 4 (Đóng khóa bắt buộc):** Trong khối `finally:`, nếu `has_identity == True`, bắt buộc phải trả lại trạng thái an toàn bằng lệnh: `cursor.execute("SET IDENTITY_INSERT stg_nano_v2.[TenBang] OFF")`. Tuyệt đối không được quên lệnh này để tránh treo session.

### 3. Cấu trúc mã nguồn mẫu để Thợ code tuân thủ:

```python
# Kiểm tra identity
cursor_dich.execute(f"SELECT OBJECTPROPERTY(OBJECT_ID('{landing_schema}.{table_name}'), 'TableHasIdentity')")
result = cursor_dich.fetchone()
has_identity = bool(result and result[0] == 1)

# TRUNCATE Bảng (Chạy đúng 1 lần ngoài vòng lặp)
cursor_dich.execute(f"TRUNCATE TABLE {landing_schema}.{table_name}")

# Xử lý bật tắt Identity Insert
if has_identity:
    cursor_dich.execute(f"SET IDENTITY_INSERT {landing_schema}.{table_name} ON")

try:
    while True:
        chunk = cursor_nguon.fetchmany(chunk_size)
        if not chunk:
            break
        cursor_dich.executemany(insert_sql, chunk)
finally:
    if has_identity:
        cursor_dich.execute(f"SET IDENTITY_INSERT {landing_schema}.{table_name} OFF")

```

### 4. Kết quả đối soát cung cấp tại báo cáo:

* Trích xuất nguyên văn khối code xử lý vòng lặp nạp Tầng 1 đã được nâng cấp (chứa các khối `TableHasIdentity`, `try... finally`) tại `fact_loader.py` vào mục báo cáo để Master duyệt logic.

---

**# BÁO CÁO CỦA THỢ CODE**

## 1) Tệp đã cập nhật theo yêu cầu

- `src/jobs/fact_loader.py`
- `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`
- `PROJECT_CHRONICLE.md`
- `REPORT_CHANGES.md`
- `docs/prompts/20260520_1705_sync_incremental_v7.md`

## 2) Kết quả triển khai chính

### 2.1. Vá lỗi 544 tại Tầng 1 trong `fact_loader.py`
- Đã bổ sung kiểm tra động metadata identity cho bảng landing `stg_nano_v2.[TenBang]`.
- Nếu bảng có identity thì bật `IDENTITY_INSERT ON` trước vòng nạp.
- Đưa toàn bộ vòng nạp chunking `fetchmany -> executemany` vào `try...finally`.
- Trong `finally` bắt buộc tắt `IDENTITY_INSERT OFF` để trả trạng thái an toàn session.

### 2.2. Khối code Tầng 1 đã nâng cấp (trích nguyên văn)

```python
staging_cursor = staging_connection.cursor()
staging_cursor.fast_executemany = True
has_identity = self._table_has_identity(staging_cursor, self.LANDING_SCHEMA, plan.table_name)

if has_identity:
    self._log(f"Bật IDENTITY_INSERT cho {self.LANDING_SCHEMA}.{plan.table_name}")
    self._set_identity_insert(staging_cursor, self.LANDING_SCHEMA, plan.table_name, enabled=True)

# Nguyên tắc 2: INSERT động tường minh theo selected_columns
try:
    while True:
        rows = production_cursor.fetchmany(self.batch_size)
        if not rows:
            break

        staging_cursor.executemany(insert_sql, rows)
        total_rows += len(rows)
finally:
    if has_identity:
        self._set_identity_insert(staging_cursor, self.LANDING_SCHEMA, plan.table_name, enabled=False)
        self._log(f"Tắt IDENTITY_INSERT cho {self.LANDING_SCHEMA}.{plan.table_name}")
```

## 3) Cập nhật tri thức

- `GEM_TECHNICAL_STANDARDS.md`:
  - Bổ sung chuẩn bắt buộc kiểm tra `TableHasIdentity` trước nạp incremental PyODBC.
  - Bổ sung quy tắc mô phỏng cờ BCP `-E` bằng `SET IDENTITY_INSERT ON/OFF`.
  - Bắt buộc bọc vòng nạp trong `try...finally` để luôn `OFF` dù có lỗi.

- `PROJECT_CHRONICLE.md`:
  - Bổ sung ADR-37: xử lý sự cố SQL 544 khi chuyển từ BCP sang PyODBC bằng Identity Insert động.

- `REPORT_CHANGES.md`:
  - Ghi rõ `src/jobs/fact_loader.py` là file Python được cập nhật logic cho v7.
