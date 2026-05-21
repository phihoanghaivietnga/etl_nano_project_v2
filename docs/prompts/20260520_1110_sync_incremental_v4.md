
**# YÊU CẦU CỦA MASTER**
Khắc phục khẩn cấp thảm họa sập luồng BCP do lỗi cắt chuỗi Data Type và thiếu chuỗi kết nối BCP, đồng thời hoàn thiện luồng BCP IN cho Tầng 1 Staging.

1. **Bắt buộc đọc:**

* `GEM_CODE_MAP.md`
* `GEM_ERROR_CONTEXT.md` (Cập nhật lỗi BCP thiếu kết nối).

2. **Yêu cầu chi tiết:**

* **Sửa lỗi Stringification trong `base_extractor.py`:**
* Tại hàm `build_dynamic_select_columns()`, bắt buộc phải `.strip()` ngay sau khi lấy chuỗi từ `pyodbc` để loại bỏ khoảng trắng thừa.
* Sửa thành: `column_name = str(row[0]).strip()` và `data_type = str(row[1]).strip().lower()`.


* **Vá lỗi BCP OUT trong `base_loader.py`:**
* Hàm `run_bcp_utf16le` phải được truyền thêm chuỗi kết nối (hoặc các tham số `-S`, `-U`, `-P`, `-d` được parse từ `connection_string`).
* Không truyền chuỗi kết nối thì BCP không thể chạy được.


* **Hoàn thiện Logic BCP IN (Tầng 1 Staging):**
* Trong `base_loader.py`, viết thêm hàm `run_bcp_in()`.
* Hàm này sử dụng `subprocess` để gọi `bcp [table_name] in [input_file] -w -E ...` kèm theo chuỗi kết nối. Bắt buộc phải có cờ `-k` (Keep Nulls) để tránh lỗi ép kiểu (Cast Specification) khi nạp file UTF-16.
* Sửa logic luồng chạy: Sau khi BCP OUT thành công -> Thực thi lệnh TRUNCATE bảng Tầng 1 -> Thực thi hàm `run_bcp_in()` -> Cuối cùng mới chạy MERGE script.



3. **Kết quả đối soát:**

* Cung cấp đoạn code thể hiện việc parse `connection_string` và gắn vào mảng lệnh `command` của `subprocess.run` trong hàm BCP.
* In ra màn hình Terminal câu lệnh BCP IN động được sinh ra (ẩn mật khẩu) để chứng minh có đầy đủ cờ `-w` và `-k`.

4. **Cập nhật tri thức:**

* Ghi nhận lỗi khoảng trắng (trailing spaces) từ pyodbc vào `GEM_ERROR_CONTEXT.md`.
* Ghi log bổ sung luồng BCP IN vào `PROJECT_CHRONICLE.md` và cập nhật thông tin liên quan vào `GEM_CODE_MAP.md`.

5. **Kết xuất báo cáo:**

* Liệt kê các file Python đã sửa vào `REPORT_CHANGES.md`.

6. **Chỉ dẫn phản hồi:**
Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.

**# BÁO CÁO CỦA THỢ CODE**

Đã hoàn thành toàn bộ hạng mục theo yêu cầu Master, gồm sửa code lõi BCP, chuẩn hóa transaction biên và cập nhật tri thức.

## 1) Các file Python đã sửa
- `src/core/base_extractor.py`
- `src/core/base_loader.py`
- `src/jobs/fact_loader.py`

## 2) Nội dung đã triển khai

### 2.1 Sửa Stringification trong `base_extractor.py`
- Tại `build_dynamic_select_columns()` đã sửa đúng yêu cầu:

```python
column_name = str(row[0]).strip()
data_type = str(row[1]).strip().lower()
```

### 2.2 Vá BCP OUT + hoàn thiện BCP IN trong `base_loader.py`
- Đã bổ sung parse `connection_string` bằng Regex `re.IGNORECASE`.
- `run_bcp_utf16le(...)` nhận thêm `source_connection_string` để BCP OUT luôn dùng kết nối nguồn Production.
- Đã bổ sung `run_bcp_in(...)` với đầy đủ cờ `-w -k -E -t\t -r\n`.

### 2.3 Chuẩn hóa luồng Tầng 1 Staging trong `fact_loader.py`
- Luồng đã đổi sang thứ tự cứng:
  1. BCP OUT thành công.
  2. Mở connection A -> TRUNCATE landing -> `commit()` -> đóng connection A.
  3. BCP IN bằng subprocess session riêng.
  4. Mở connection B mới để chạy MERGE tầng sau.

## 3) Đoạn code parse connection_string và gắn vào command (nguyên văn)

```python
@classmethod
def parse_connection_string(cls, connection_string: str) -> dict[str, str]:
    conn_parts: dict[str, str] = {}
    for match in cls._CONNECTION_PART_PATTERN.finditer(connection_string):
        key = match.group("key").strip().upper()
        value = match.group("value").strip()
        if key:
            conn_parts[key] = value
    return conn_parts

def _build_bcp_connection_args(self, connection_string: str) -> list[str]:
    conn_parts = self.parse_connection_string(connection_string)
    server = self._resolve_conn_value(conn_parts, ("SERVER", "DATA SOURCE", "ADDRESS", "ADDR", "NETWORK ADDRESS"))
    database = self._resolve_conn_value(conn_parts, ("DATABASE", "INITIAL CATALOG"))
    uid = self._resolve_conn_value(conn_parts, ("UID", "USER ID"))
    pwd = self._resolve_conn_value(conn_parts, ("PWD", "PASSWORD"))

    if not server or not database:
        raise ValueError("Thiếu SERVER hoặc DATABASE trong connection_string để chạy BCP")

    auth_args = ["-T"]
    if uid and pwd:
        auth_args = ["-U", uid, "-P", pwd]

    return ["-S", server, "-d", database, *auth_args]
```

```python
def run_bcp_in(self, table_name: str, input_file: str) -> None:
    connection_args = self._build_bcp_connection_args(self.connection_string)
    command = [
        "bcp",
        table_name,
        "in",
        input_file,
        *connection_args,
        "-w",
        "-k",
        "-E",
        "-t\t",
        "-r\n",
        "-q",
    ]
    self._log(f"BCP IN command: {self._mask_bcp_command(command)}")
    subprocess.run(command, check=True, shell=False)
```

## 4) Bằng chứng terminal cho BCP IN động (đã ẩn mật khẩu)

```text
[DemoBCP] BCP IN command: bcp stg_nano_v2.ThuPhiDichVu in C:/temp/demo.txt -S SRV01 -d DMART -U etl_user -P ****** -w -k -E -t\t -r\n -q
```

## 5) Cập nhật tri thức đã thực hiện
- `docs/knowledge/GEM_ERROR_CONTEXT.md`:
  - Thêm `E-ETL-BCP-METADATA-TRIM` (lỗi trailing spaces từ pyodbc).
  - Thêm `E-ETL-BCP-CONNECTION-001` (lỗi thiếu tham số kết nối BCP).
- `docs/knowledge/GEM_CODE_MAP.md`:
  - Bổ sung mục 20260520_1110 cho parse Regex, BCP IN mới và transaction biên.
- `PROJECT_CHRONICLE.md`:
  - Đã chèn nguyên văn câu bắt buộc:
    - `Cảnh báo rủi ro (Nợ kỹ thuật): Đã gỡ bỏ cơ chế Validate SQL Fallback Doanh Thu bằng Python theo quyết định của Master. Luồng ETL hiện tại hoàn toàn tin tưởng vào các file SQL Template. Nếu file SQL bị sửa sai, hệ thống sẽ không thể tự động chặn lỗi.`
  - Bổ sung ADR-28/29/30 cho hotfix BCP v4.
