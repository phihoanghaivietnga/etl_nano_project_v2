
# YÊU CẦU CỦA MASTER: HOTFIX DEADLOCK TRANSACTION TRONG PIPELINE

1. **PHÂN TÍCH SỰ CỐ (ROOT CAUSE ANALYSIS):**
Hệ thống bị treo cứng ngay khi bắt đầu tiến trình `BCP IN` (đổ dữ liệu vào bảng ODS).
*Nguyên nhân:* Hàm `_truncate_table` thực thi lệnh `TRUNCATE TABLE` qua `pyodbc` nhưng không được `commit()`. Điều này gây ra hiện tượng khóa bảng (Table Lock). Tiến trình `bcp` (chạy bằng subprocess) bị chặn lại do không thể chèn dữ liệu vào bảng đang bị khóa bởi chính session Python cha. Gây ra Deadlock!
2. **CHỈ THỊ SỬA CODE (`src/jobs/dimension_loader.py`):**
BẮT BUỘC phải thực hiện `connection.commit()` ngay sau mọi câu lệnh thay đổi dữ liệu (DDL/DML) để giải phóng khóa (Release Lock) trước khi nhường quyền cho tiến trình khác.

* **Sửa hàm `_truncate_table`:** Thêm `connection.commit()` ngay sau lệnh execute.

```python
    def _truncate_table(self, connection: pyodbc.Connection, schema_name: str, table_name: str) -> None:
        sql = f"TRUNCATE TABLE [{schema_name}].[{table_name}];"
        self.execute_sql_sync(connection, sql)
        connection.commit() # BẮT BUỘC CÓ DÒNG NÀY ĐỂ MỞ KHÓA BẢNG

```

* **Sửa hàm `_execute_dimension_spec` (Bảo vệ luồng MERGE):** Đảm bảo sau khi chạy SQL MERGE cũng phải commit để chốt dữ liệu vào Datamart.

```python
        # ... (đoạn code render merge_sql hiện tại)
        self._log(f"[START] Đang thực thi MERGE ODS -> Datamart cho {spec.dimension_name}...")
        self.execute_sql_sync(connection, merge_sql)
        connection.commit() # BẮT BUỘC COMMIT SAU KHI MERGE
        self._log(f"[SUCCESS] Hoàn thành MERGE {spec.dimension_name}")

```

3. **CHỈ THỊ CẬP NHẬT TRI THỨC (`agents.md` BẮT BUỘC):**

* **`PROJECT_CHRONICLE.md`:** Cập nhật **ADR-14**, ghi chép lại bài học xương máu về Table Lock/Deadlock khi kết hợp giữa `pyodbc` (chạy TRUNCATE chưa commit) và tiến trình BCP Subprocess.
* **`REPORT_CHANGES.md`:** Ghi nhận hotfix Deadlock.

4. **CHỈ DẪN PHẢN HỒI:**
Sửa code và tài liệu. Báo cáo bằng cách dán nội dung 2 hàm `_truncate_table` và `_execute_dimension_spec` vừa sửa xuống dưới thẻ `# BÁO CÁO CỦA THỢ CODE`.

# BÁO CÁO CỦA THỢ CODE

## 1) Hàm `_truncate_table` sau khi sửa

```python
def _truncate_table(self, connection: pyodbc.Connection, schema_name: str, table_name: str) -> None:
    # Lệnh thay đổi dữ liệu chỉ chạy trên connection Datamart/ODS, không dùng Production.
    sql = f"TRUNCATE TABLE [{schema_name}].[{table_name}];"
    self._log(f"TRUNCATE {schema_name}.{table_name}")
    self.execute_sql_sync(connection, sql)
    connection.commit()
```

## 2) Hàm `_execute_dimension_spec` sau khi sửa

```python
def _execute_dimension_spec(self, connection: pyodbc.Connection, spec: DimensionTableSpec) -> None:
    self._log(f"Bắt đầu FULL LOAD dimension: {spec.dimension_name}")

    for source_table in spec.source_tables:
        self._truncate_table(connection, self.facility_schema, source_table)
        self._copy_prod_to_ods(connection, source_table)

    merge_sql = self._render_merge_sql(spec.merge_sql_path)
    self._log(f"[START] Đang thực thi MERGE ODS -> Datamart cho {spec.dimension_name}...")
    # Lệnh MERGE chỉ chạy trên connection Datamart/ODS, không dùng Production.
    self.execute_sql_sync(connection, merge_sql)
    connection.commit()
    self._log(f"[SUCCESS] Hoàn thành MERGE {spec.dimension_name}")
```


