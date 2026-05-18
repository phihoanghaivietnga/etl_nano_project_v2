
# YÊU CẦU CỦA MASTER: HOTFIX BẢO MẬT LOG VÀ LỖI CAST SPECIFICATION (BCP)

1. **PHÂN TÍCH SỰ CỐ:**

* **Bảo mật:** Log in ra màn hình chứa toàn bộ thông tin nhạy cảm của Database (User, Password, Server) do việc in trực tiếp biến `command` của BCP.
* **Lỗi BCP (Invalid character value for cast specification):** Do thiếu cờ `-k` (Keep Nulls) khi `bcp in`, khiến SQL Server không thể convert chuỗi rỗng thành `INT/DATETIME`. Đồng thời, cần phòng ngừa xô lệch cột do ký tự đặc biệt trong dữ liệu y tế.

2. **CHỈ THỊ SỬA CODE (`src/jobs/dimension_loader.py`):**

* **Xử lý Bảo mật Log:**
Trong 2 hàm `_run_bcp_queryout` và `_run_bcp_in`, TUYỆT ĐỐI KHÔNG ĐƯỢC `print` hoặc `_log` biến `command` ra màn hình. Chỉ in log chung chung dạng: `_log("Đang thực thi BCP OUT...")` hoặc `_log("Đang thực thi BCP IN...")`.
* **Xử lý tham số BCP (BẮT BUỘC):**
* Hàm `_run_bcp_queryout` (Lệnh kéo ra): Bắt buộc phải có các tham số `-w` (UTF-16LE) và `-t "<|>"` (Dấu phân cách cột an toàn).
* Hàm `_run_bcp_in` (Lệnh đẩy vào): Bắt buộc phải có các tham số `-w` (UTF-16LE), `-t "<|>"` và đặc biệt là cờ **`-k` (Keep Nulls)**.



*(Ví dụ đoạn nối chuỗi command cần đảm bảo chứa các cờ: `bcp ... out ... -w -t "<|>" -S ...`)*

3. **CHỈ THỊ CẬP NHẬT TRI THỨC (`agents.md` BẮT BUỘC):**

* **`PROJECT_CHRONICLE.md`:** Cập nhật **ADR-15**. Ghi nhận 2 vấn đề: Cấm in log chứa credentials (Security) và bộ tham số sinh tử của BCP (`-w -t "<|>" -k`) để xử lý lỗi ép kiểu dữ liệu và xô cột.
* **`REPORT_CHANGES.md`:** Ghi nhận Hotfix bảo mật và BCP parameters.

4. **CHỈ DẪN PHẢN HỒI:**
Dưới thẻ `# BÁO CÁO CỦA THỢ CODE`, hãy dán đoạn code cấu trúc lệnh `command = ...` của 2 hàm `_run_bcp_queryout` và `_run_bcp_in` sau khi đã chèn các cờ yêu cầu và đã xóa lệnh in log nhạy cảm.

# BÁO CÁO CỦA THỢ CODE

## 1) Cấu trúc `command` trong `_run_bcp_queryout` sau khi sửa

```python
command = [
    "bcp",
    query,
    "queryout",
    output_file,
    "-S",
    prod_parts.get("SERVER", ""),
    "-d",
    prod_parts.get("DATABASE", ""),
    *self._build_bcp_auth_args(prod_parts),
    "-w",
    "-t",
    "<|>",
    "-r\\n",
    "-q",
]
```

## 2) Cấu trúc `command` trong `_run_bcp_in` sau khi sửa

```python
command = [
    "bcp",
    full_table_name,
    "in",
    input_file,
    "-S",
    dm_parts.get("SERVER", ""),
    "-d",
    dm_parts.get("DATABASE", ""),
    *self._build_bcp_auth_args(dm_parts),
    "-w",
    "-t",
    "<|>",
    "-k",
    "-r\\n",
    "-q",
]
```

## 3) Xác nhận bảo mật log
- Đã xóa log in chi tiết biến `command` ở cả 2 hàm.
- Chỉ giữ log trung tính:
  - `Đang thực thi BCP OUT...`
  - `Đang thực thi BCP IN...`
