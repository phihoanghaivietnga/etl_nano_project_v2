
# YÊU CẦU CỦA MASTER: HOTFIX LỖI CÚ PHÁP BCP VÀ RÒ RỈ TRACEBACK

1. **PHÂN TÍCH LỖI SỰ CỐ:**

* **Vẫn lộ thông tin kết nối:** Do `subprocess.CalledProcessError` tự động in biến `command` ra Traceback khi ứng dụng crash.
* **Lỗi Cast & Incomplete Column:** Do định dạng chuỗi tham số trong mảng `command` bị sai. Tham số `"-r\\n"` truyền chuỗi escape sai, khiến `bcp` không nhận diện được dấu xuống dòng, dẫn đến đọc gộp dòng và văng lỗi sai kiểu dữ liệu. Việc tách rời `"-t"` và `"<|>"` cũng dễ gây lỗi parsing của `bcp`.

2. **CHỈ THỊ SỬA CODE (`src/jobs/dimension_loader.py`):**

* **A. Khắc phục lỗi cú pháp mảng `command`:**
Trong cả 2 hàm `_run_bcp_queryout` và `_run_bcp_in`, bắt buộc phải gộp các cờ và giá trị lại, đồng thời sử dụng đúng ký tự raw escape `\n`. Thay thế các phần tử cuối của list `command` thành cấu trúc chuẩn sau:
* Cho `queryout`: `..., "-w", "-t<|>", "-r\n", "-q"]`
* Cho `in`: `..., "-w", "-t<|>", "-k", "-r\n", "-q"]`


* **B. Khắc phục rò rỉ bảo mật ở Traceback:**
Phải bọc lại Exception của `subprocess`. Nếu tiến trình lỗi, KHÔNG ĐƯỢC raise `CalledProcessError` mang theo biến `command`. Hãy raise một lỗi chung chung. Sửa lại đoạn cuối của cả 2 hàm như sau:

```python
    if process.returncode != 0:
        raise RuntimeError(f"Tiến trình BCP thất bại (Exit code: {process.returncode}). Đã ẩn chi tiết command để bảo mật.")

```

3. **CHỈ THỊ CẬP NHẬT TRI THỨC (`agents.md` BẮT BUỘC):**

* **`PROJECT_CHRONICLE.md`:** Thêm **ADR-16** ghi nhận bài học xương máu về việc cấu hình tham số list cho subprocess BCP (phải dùng `-t<|>` và `-r\n`) để tránh lỗi tràn dòng (Text column data incomplete), và cách che giấu credentials khỏi Exception Traceback.
* **`REPORT_CHANGES.md`:** Ghi nhận Hotfix 16.

4. **CHỈ DẪN PHẢN HỒI:**
Dán cấu trúc mảng `command` và đoạn xử lý `Exception` của 2 hàm sau khi sửa xuống dưới thẻ `# BÁO CÁO CỦA THỢ CODE`. Không cần giải thích thêm.

# BÁO CÁO CỦA THỢ CODE

## _run_bcp_queryout

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
    "-t<|>",
    "-r\\n",
    "-q",
]

if process.returncode != 0:
    raise RuntimeError(
        f"Tiến trình BCP thất bại (Exit code: {process.returncode}). Đã ẩn chi tiết command để bảo mật."
    )
```

## _run_bcp_in

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
    "-t<|>",
    "-k",
    "-r\\n",
    "-q",
]

if process.returncode != 0:
    raise RuntimeError(
        f"Tiến trình BCP thất bại (Exit code: {process.returncode}). Đã ẩn chi tiết command để bảo mật."
    )
```
