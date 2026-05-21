
**# YÊU CẦU CỦA MASTER**
Quyết định kiến trúc tối hậu: Chấp nhận hy sinh tốc độ nạp Bulk để đổi lấy an toàn bộ nhớ tuyệt đối 100%. Yêu cầu tắt bỏ vĩnh viễn tính năng `fast_executemany` của `pyodbc` cho luồng Incremental Tầng 1, đưa cơ chế nạp về dạng truyền thống (như V1) để khắc phục triệt để lỗi `MemoryError` do cấp phát tĩnh 2GB của cột `NVARCHAR(MAX)`.

### 1. Các file tài liệu bắt buộc phải cập nhật sau khi xử lý:

* `docs/knowledge/GEM_TECHNICAL_STANDARDS.md` (Xóa bỏ cơ chế Fallback phức tạp. Cập nhật chuẩn nạp dữ liệu Tầng 1: "Bắt buộc thiết lập `fast_executemany = False` để vô hiệu hóa cấp phát bộ nhớ tĩnh, bảo vệ RAM tuyệt đối khi nạp các cột MAX").
* `PROJECT_CHRONICLE.md` (Ghi nhận ADR: "Quyết định kiến trúc tối hậu - Tắt hoàn toàn `fast_executemany` cho luồng Incremental. Chấp nhận tốc độ nạp Row-by-Row ngầm của PyODBC để đổi lấy sự an toàn 100% trước lỗi MemoryError của các bảng chứa cột văn bản lớn").
* `REPORT_CHANGES.md` (Liệt kê chính xác file `src/jobs/fact_loader.py` đã được dọn dẹp).

### 2. Yêu cầu triển khai chi tiết cho Thợ code:

* **Vị trí can thiệp:** Tệp `src/jobs/fact_loader.py` (trong hàm thực thi nạp Tầng 1 `_load_to_global_staging`).
* **Dọn dẹp mã nguồn:** - Xóa bỏ hoàn toàn khối `try...except (MemoryError, pyodbc.Error)` (cơ chế fallback lùi bước) mà tao vừa yêu cầu trước đó.
* Thiết lập tường minh lệnh: `cursor.fast_executemany = False` trước khi bước vào vòng lặp nạp dữ liệu.


* **Bảo tồn các lớp giáp bảo vệ đã có:**
* Bắt buộc GIỮ NGUYÊN logic kiểm tra động `TableHasIdentity` và khối `try...finally` để bật/tắt cờ `SET IDENTITY_INSERT` mô phỏng BCP.
* Bắt buộc GIỮ NGUYÊN lệnh `TRUNCATE` nằm ngoài vòng lặp chunking.
* Bắt buộc GIỮ NGUYÊN câu lệnh `INSERT INTO ... VALUES ...` động có chỉ định đích danh tên cột.



### 3. Cấu trúc mã nguồn mẫu để Thợ code rập khuôn:

```python
# 1. Kiểm tra identity
staging_cursor.execute(f"SELECT OBJECTPROPERTY(OBJECT_ID('{self.LANDING_SCHEMA}.{table_name}'), 'TableHasIdentity')")
result = staging_cursor.fetchone()
has_identity = bool(result and result[0] == 1)

# 2. TRUNCATE Bảng (Ngoài vòng lặp)
staging_cursor.execute(f"TRUNCATE TABLE {self.LANDING_SCHEMA}.{table_name}")

# 3. Mở khóa Identity
if has_identity:
    staging_cursor.execute(f"SET IDENTITY_INSERT {self.LANDING_SCHEMA}.{table_name} ON")

try:
    # 4. CHỐT CHẶN AN TOÀN RAM (TẮT TĂNG TỐC)
    staging_cursor.fast_executemany = False
    
    # 5. Vòng lặp Chunking nạp chậm mà chắc
    while True:
        chunk = production_cursor.fetchmany(chunk_size)
        if not chunk:
            break
        staging_cursor.executemany(insert_sql, chunk)
finally:
    # 6. Đóng khóa Identity
    if has_identity:
        staging_cursor.execute(f"SET IDENTITY_INSERT {self.LANDING_SCHEMA}.{table_name} OFF")

```

### 4. Kết quả đối soát cung cấp tại báo cáo:

* Trích xuất nguyên văn khối logic nạp Tầng 1 vừa được làm sạch tại `fact_loader.py` vào mục báo cáo để Master duyệt. Không được phép sót lệnh khóa Identity trong khối `finally`.

---

**# BÁO CÁO CỦA THỢ CODE**

## 1) Tóm tắt xử lý theo chỉ đạo Master
- Đã dọn dẹp luồng Incremental Tầng 1 tại `src/jobs/fact_loader.py` theo quyết định kiến trúc tối hậu.
- Đã chốt cứng cấu hình nạp:
  - `staging_cursor.fast_executemany = False`
- Đã xác nhận không còn khối fallback `except (MemoryError, pyodbc.Error)` trong `fact_loader.py`.

## 2) Bảo tồn các lớp giáp bắt buộc
- Giữ nguyên kiểm tra động identity:
  - `TableHasIdentity` qua `OBJECTPROPERTY(OBJECT_ID(...), 'TableHasIdentity')`.
- Giữ nguyên `TRUNCATE` nằm ngoài vòng lặp chunking.
- Giữ nguyên `INSERT INTO ... VALUES ...` động theo `selected_columns`.
- Giữ nguyên khối `try...finally` với lệnh khóa identity trong `finally`:
  - `SET IDENTITY_INSERT ... OFF`.

## 3) Các tệp đã cập nhật đúng yêu cầu
1. `src/jobs/fact_loader.py`
2. `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`
3. `PROJECT_CHRONICLE.md`
4. `REPORT_CHANGES.md`

## 4) Cập nhật tri thức bắt buộc
- `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`:
  - Bỏ định hướng fallback phức tạp.
  - Chốt chuẩn Incremental Tầng 1: bắt buộc `fast_executemany = False` để vô hiệu hóa cấp phát bộ nhớ tĩnh với cột MAX.
- `PROJECT_CHRONICLE.md`:
  - Bổ sung ADR-38: Quyết định tắt hoàn toàn `fast_executemany`, chấp nhận đánh đổi tốc độ để lấy an toàn RAM 100%.
- `REPORT_CHANGES.md`:
  - Liệt kê chính xác `src/jobs/fact_loader.py` đã được dọn dẹp.
  - Ghi nhận đầy đủ nội dung xử lý của task `20260521_0835_sync_incremental_v8.md`.

## 5) Trích xuất nguyên văn khối logic nạp Tầng 1 đã làm sạch
```python
    # Tầng 1: Global Transient Staging (PyODBC SELECT -> TRUNCATE 1 lần -> executemany theo chunk)
    def _load_to_global_staging(self, plan: ExtractPlan) -> None:
        insert_sql = self._build_explicit_insert_sql(
            schema_name=self.LANDING_SCHEMA,
            table_name=plan.table_name,
            selected_columns=plan.selected_columns,
        )

        total_rows = 0
        with pyodbc.connect(self.production_connection, autocommit=True) as production_connection:
            production_cursor = production_connection.cursor()
            production_cursor.execute(plan.select_sql)

            with self.get_db_context() as staging_connection:
                # Nguyên tắc 1: TRUNCATE chỉ chạy đúng 1 lần trước vòng lặp chunking
                self._truncate_table(staging_connection, self.LANDING_SCHEMA, plan.table_name)

                staging_cursor = staging_connection.cursor()
                staging_cursor.fast_executemany = False
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

                staging_connection.commit()

        self._log(
            f"Hoàn tất nạp Tầng 1 bằng PyODBC cho {plan.table_name}: {total_rows} dòng, chunk_size={self.batch_size}"
        )
```

## 6) Kết quả đối soát nhanh
- `fast_executemany` trong `fact_loader.py`: chỉ còn `False`.
- Mẫu `except (MemoryError, pyodbc.Error)`: không còn xuất hiện.
- Lệnh `SET IDENTITY_INSERT ... OFF` hiện diện trong khối `finally` đúng yêu cầu.
