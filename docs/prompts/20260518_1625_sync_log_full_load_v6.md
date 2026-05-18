
# YÊU CẦU CỦA MASTER: THAY ĐỔI KIẾN TRÚC - LOẠI BỎ BCP CLI, CHUYỂN SANG ODBC BULK COPY

1. **PHÂN TÍCH QUYẾT ĐỊNH KIẾN TRÚC (ADR-17):**
Sau nhiều lần vá lỗi, công cụ `bcp` CLI vẫn liên tục văng lỗi `Invalid character value for cast specification`. 
* **Nguyên nhân gốc rễ (Root Cause):** Dữ liệu Y tế (HIS) trên Production chứa cực kỳ nhiều ký tự rác ẩn trong các trường văn bản tự do (như phím Enter `\n`, `\r`, Tab `\t` trong cột DiaChi, GhiChu). Khi `bcp queryout` xuất ra file `.txt`, các ký tự Enter ẩn này phá vỡ cấu trúc dòng của file text. Khi `bcp in` đọc lại, nó lầm tưởng đó là dòng mới, dẫn đến việc lấy chuỗi text nhét nhầm vào các cột kiểu INT hoặc DATETIME, gây ra lỗi ép kiểu (Cast) và xô lệch cột.
* **Giải pháp (Học từ V1):** Loại bỏ hoàn toàn việc gọi `bcp` qua `subprocess` và không dùng file `.txt` trung gian nữa. Chuyển sang sử dụng API `executemany` của thư viện `pyodbc`. Kỹ thuật này sẽ truyền dữ liệu dưới dạng tham số hóa (Parameterized), bảo toàn tuyệt đối các ký tự rác mà không làm xô cột. Để đảm bảo tốc độ, BẮT BUỘC bật cờ `fast_executemany = True` (ODBC Binary Bulk Copy).

2. **CHỈ THỊ REFACTOR CODE (`src/jobs/dimension_loader.py`):**

* **A. Xóa bỏ rác cũ:** Xóa hoàn toàn 2 hàm `_run_bcp_queryout` và `_run_bcp_in`. Bỏ thư viện `subprocess` và `tempfile` ở phần import nếu không còn dùng đến.
* **B. Viết lại hàm `_copy_prod_to_ods`:** Thay vì gọi BCP, hãy mở kết nối đến Prod, đọc dữ liệu, và dùng `executemany` đẩy thẳng vào ODS theo từng lô (Chunking). BẮT BUỘC tuân thủ logic code sau:

```python
    def _copy_prod_to_ods(self, connection: pyodbc.Connection, table_name: str) -> None:
        self._log(f"Đang kéo dữ liệu {table_name} từ Prod -> ODS bằng ODBC Bulk Copy...")
        
        # 1. Kết nối Production (Chỉ được SELECT)
        prod_conn_str = self.connection_strings[self.prod_env_key]
        prod_conn = pyodbc.connect(prod_conn_str, autocommit=True)
        prod_cursor = prod_conn.cursor()
        
        try:
            # 2. Truy vấn dữ liệu gốc
            query = f"SELECT * FROM dbo.[{table_name}] WITH (NOLOCK)"
            prod_cursor.execute(query)
            
            # Lấy danh sách cột để sinh câu lệnh INSERT động
            columns = [column[0] for column in prod_cursor.description]
            col_names_str = ", ".join([f"[{c}]" for c in columns])
            placeholders = ", ".join(["?"] * len(columns))
            insert_sql = f"INSERT INTO [{self.facility_schema}].[{table_name}] ({col_names_str}) VALUES ({placeholders})"
            
            # 3. Chuẩn bị Cursor cho Staging với fast_executemany
            stg_cursor = connection.cursor()
            stg_cursor.fast_executemany = True
            
            # 4. Đẩy dữ liệu theo lô (Chunking) để không tràn RAM
            chunk_size = 10000
            total_rows = 0
            
            while True:
                rows = prod_cursor.fetchmany(chunk_size)
                if not rows:
                    break
                
                # Chuyển đổi pyodbc.Row thành tuple để executemany có thể xử lý
                data_chunk = [tuple(row) for row in rows]
                stg_cursor.executemany(insert_sql, data_chunk)
                connection.commit()
                
                total_rows += len(data_chunk)
                self._log(f"Đã copy {total_rows} dòng vào ODS...")
                
            self._log(f"[SUCCESS] Hoàn tất kéo {total_rows} dòng cho {table_name}.")
            
        finally:
            prod_cursor.close()
            prod_conn.close()

```

3. **CHỈ THỊ CẬP NHẬT TRI THỨC (`agents.md` BẮT BUỘC):**
Ngươi phải ghi nhận sự kiện thay đổi kiến trúc lớn này vào các file sau:

* **`PROJECT_CHRONICLE.md`:** Thêm **ADR-17**. Ghi rõ nguyên nhân khai tử BCP CLI (do dữ liệu y tế chứa newline/tab ngầm làm vỡ file text gây lỗi Cast). Ghi nhận quyết định chuyển sang `pyodbc.fast_executemany` (ODBC Bulk Copy) kết hợp chunking 10k dòng để an toàn ép kiểu và bảo mật.
* **`docs/knowledge/GEM_CODE_MAP.md`:** Xóa bỏ phần mô tả của 2 hàm `_run_bcp_queryout` và `_run_bcp_in`. Cập nhật mô tả mới cho hàm `_copy_prod_to_ods` (sử dụng pyodbc fast_executemany).
* **`REPORT_CHANGES.md`:** Ghi nhận sự thay đổi kiến trúc lõi Data Ingestion từ CLI BCP sang Python Native ODBC.

4. **CHỈ DẪN PHẢN HỒI:**
Hoàn tất code và cập nhật tài liệu. Dưới thẻ `# BÁO CÁO CỦA THỢ CODE`, hãy dán nguyên văn hàm `_copy_prod_to_ods` mới vừa được thay thế, đồng thời trích dẫn nội dung đã cập nhật trong `PROJECT_CHRONICLE.md`.

# BÁO CÁO CỦA THỢ CODE

## Hàm `_copy_prod_to_ods` mới

```python
def _copy_prod_to_ods(self, connection: pyodbc.Connection, table_name: str) -> None:
    self._log(f"Đang kéo dữ liệu {table_name} từ Prod -> ODS bằng ODBC Bulk Copy...")

    # 1. Kết nối Production (Chỉ được SELECT)
    prod_conn_str = self.connection_strings[self.prod_env_key]
    prod_conn = pyodbc.connect(prod_conn_str, autocommit=True)
    prod_cursor = prod_conn.cursor()

    try:
        # 2. Truy vấn dữ liệu gốc
        query = f"SELECT * FROM dbo.[{table_name}] WITH (NOLOCK)"
        prod_cursor.execute(query)

        # Lấy danh sách cột để sinh câu lệnh INSERT động
        columns = [column[0] for column in prod_cursor.description]
        col_names_str = ", ".join([f"[{c}]" for c in columns])
        placeholders = ", ".join(["?"] * len(columns))
        insert_sql = f"INSERT INTO [{self.facility_schema}].[{table_name}] ({col_names_str}) VALUES ({placeholders})"

        # 3. Chuẩn bị Cursor cho Staging với fast_executemany
        stg_cursor = connection.cursor()
        stg_cursor.fast_executemany = True

        # 4. Đẩy dữ liệu theo lô (Chunking) để không tràn RAM
        chunk_size = 10000
        total_rows = 0

        while True:
            rows = prod_cursor.fetchmany(chunk_size)
            if not rows:
                break

            # Chuyển đổi pyodbc.Row thành tuple để executemany có thể xử lý
            data_chunk = [tuple(row) for row in rows]
            stg_cursor.executemany(insert_sql, data_chunk)
            connection.commit()

            total_rows += len(data_chunk)
            self._log(f"Đã copy {total_rows} dòng vào ODS...")

        self._log(f"[SUCCESS] Hoàn tất kéo {total_rows} dòng cho {table_name}.")
    finally:
        prod_cursor.close()
        prod_conn.close()
```

## Trích dẫn nội dung đã cập nhật trong `PROJECT_CHRONICLE.md`

> ### ADR-17: Khai tử BCP CLI, chuyển sang ODBC Bulk Copy (`pyodbc.fast_executemany`)
> - **Nguyên nhân gốc rễ**:
>   - Dữ liệu HIS Production chứa ký tự ẩn trong text tự do (`\n`, `\r`, `\t`) làm vỡ cấu trúc file `.txt` khi đi qua `bcp queryout`.
>   - Khi `bcp in` đọc lại, các dòng bị xô lệch cột, dẫn đến ép kiểu sai (`Invalid character value for cast specification`) vào cột `INT/DATETIME`.
> - **Quyết định kiến trúc**:
>   - Loại bỏ hoàn toàn đường ống BCP CLI qua `subprocess` và file trung gian `.txt`.
>   - Chuyển sang nạp trực tiếp bằng `pyodbc` theo cơ chế parameterized `executemany` để bảo toàn dữ liệu text bẩn.
>   - Bật `fast_executemany = True` và chạy chunking 10,000 dòng/lô để tối ưu tốc độ và tránh tràn RAM.
