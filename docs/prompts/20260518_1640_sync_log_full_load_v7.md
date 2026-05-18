
# YÊU CẦU CỦA MASTER: HOTFIX MEMORY ERROR - HẠ CẤP FAST_EXECUTEMANY

1. **PHÂN TÍCH SỰ CỐ:**
Khi chạy `_copy_prod_to_ods`, hệ thống ngay lập tức văng `MemoryError`.
* **Nguyên nhân gốc rễ:** Bảng `DMBenhNhan` chứa các cột `NVARCHAR(MAX)` hoặc `VARCHAR(MAX)`. Khi bật cờ `stg_cursor.fast_executemany = True`, ODBC Driver cố gắng cấp phát bộ nhớ RAM dựa trên kích thước lý thuyết lớn nhất của cột nhân với `chunk_size` (10,000), dẫn đến yêu cầu cấp phát bộ nhớ vượt quá khả năng của hệ điều hành, gây ra lỗi tràn RAM (MemoryError).
* **Giải pháp:** Phải học theo bản V1, vô hiệu hóa `fast_executemany` và giảm `chunk_size` xuống mức an toàn (1000) để đảm bảo tính ổn định (Stability over Speed).

2. **CHỈ THỊ SỬA CODE (`src/jobs/dimension_loader.py`):**
Trong hàm `_copy_prod_to_ods`:
* Tìm và **XÓA/COMMENT** dòng: `stg_cursor.fast_executemany = True` (hoặc sửa thành `False`).
* Sửa `chunk_size = 10000` thành `chunk_size = 1000`.
*(Chỉ sửa 2 điểm này, giữ nguyên toàn bộ logic loop và commit)*

3. **CHỈ THỊ CẬP NHẬT TRI THỨC (`agents.md` BẮT BUỘC):**
* **`PROJECT_CHRONICLE.md`:** Cập nhật **ADR-18**. Ghi nhận sự cố `MemoryError` kinh điển của `pyodbc` khi dùng `fast_executemany` với cột `VARCHAR(MAX)`. Ghi rõ quyết định hy sinh tốc độ, trở về dùng `executemany` tiêu chuẩn và chunk_size=1000 để đảm bảo an toàn bộ nhớ tuyệt đối.
* **`REPORT_CHANGES.md`:** Ghi nhận hotfix MemoryError.

4. **CHỈ DẪN PHẢN HỒI:**
Hoàn tất sửa code và tài liệu. Dưới thẻ `# BÁO CÁO CỦA THỢ CODE`, hãy dán 10 dòng code thể hiện đã đổi cấu hình cursor và chunk_size trong hàm `_copy_prod_to_ods`. Không cần dán cả hàm.

# BÁO CÁO CỦA THỢ CODE

```python
insert_sql = f"INSERT INTO [{self.facility_schema}].[{table_name}] ({col_names_str}) VALUES ({placeholders})"

# 3. Chuẩn bị Cursor cho Staging với fast_executemany
stg_cursor = connection.cursor()
# Hotfix MemoryError: vô hiệu hóa fast_executemany với bảng có cột VARCHAR/NVARCHAR(MAX).
stg_cursor.fast_executemany = False

# 4. Đẩy dữ liệu theo lô (Chunking) để không tràn RAM
chunk_size = 1000
total_rows = 0
```