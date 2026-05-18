
# YÊU CẦU CỦA MASTER: NÂNG CẤP HỆ THỐNG GIÁM SÁT REAL-TIME VÀ CẬP NHẬT TRI THỨC

1. **MỤC TIÊU:**
Khắc phục tình trạng "nuốt log" gây đóng băng Terminal khi xử lý bảng lớn (như `DimBenhNhan`). Sửa đổi mã nguồn để stream log BCP theo thời gian thực (real-time). BẮT BUỘC cập nhật toàn diện Tầng tri thức theo đúng quy định tại `agents.md`.
2. **CHỈ THỊ CẢI TIẾN MÃ NGUỒN Python (`src/jobs/dimension_loader.py`):**

* **A. Cải tiến hàm Log:**
Cập nhật hàm `_log` để in log kèm timestamp (đến mili-giây) và ép đẩy luồng ra màn hình lập tức:
```python
def _log(self, message: str) -> None:
    from datetime import datetime
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] {message}", flush=True)

```


* **B. Stream dữ liệu BCP Real-time (QUAN TRỌNG):**
Sửa lại 2 hàm `_run_bcp_queryout` và `_run_bcp_in`. Thay vì dùng `subprocess.run`, BẮT BUỘC dùng `subprocess.Popen` để đọc và in trực tiếp `stdout` ra Terminal theo từng dòng.
*Mã mẫu yêu cầu tuân thủ:*
```python
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
while True:
    line = process.stdout.readline()
    if not line and process.poll() is not None:
        break
    if line:
        print(line.strip(), flush=True)
if process.returncode != 0:
    raise subprocess.CalledProcessError(process.returncode, command)

```


* **C. Bọc Log trạng thái MERGE:**
Trong hàm `_execute_dimension_spec`, trước lệnh `self.execute_sql_sync`, in rõ: `[START] Đang thực thi MERGE ODS -> Datamart cho <dimension_name>...`. Sau lệnh, in rõ: `[SUCCESS] Hoàn thành MERGE <dimension_name>`.

3. **CHỈ THỊ CẬP NHẬT TÀI LIỆU TRI THỨC (TUÂN THỦ `agents.md` BẮT BUỘC):**
Ngươi đóng vai trò Thợ Code, phải thực hiện Bước 3 và Bước 4 theo chuẩn `agents.md`:

* **`PROJECT_CHRONICLE.md`:** Ghi nhật ký (ADR) về quyết định chuyển sang dùng Popen để stream log BCP real-time nhằm tránh lỗi ngầm/đóng băng UI.
* **`docs/knowledge/GEM_CODE_MAP.md`:** Cập nhật mô tả chi tiết cho hàm `_run_bcp_queryout` và `_run_bcp_in` (ghi rõ tính năng streaming realtime).
* **`docs/knowledge/GEM_AUTO_PIPELINE.md`:** Thêm mục "Cơ chế Giám sát (Monitoring)" mô tả việc log timestamp mili-giây và luồng BCP/MERGE được bắn ra Terminal trực tiếp.
* **`REPORT_CHANGES.md`:** Xuất báo cáo tổng kết các thay đổi.

4. **CHỈ DẪN PHẢN HỒI:**
Hoàn tất các bước trên. Dưới thẻ `# BÁO CÁO CỦA THỢ CODE`, hãy:

* Dán đoạn code của hai hàm `_run_bcp_queryout` và `_run_bcp_in` vừa sửa.
* Trích dẫn các đoạn text đã chèn vào `PROJECT_CHRONICLE.md`, `GEM_CODE_MAP.md` và `GEM_AUTO_PIPELINE.md`.

# BÁO CÁO CỦA THỢ CODE

## 1) Đoạn code hai hàm `_run_bcp_queryout` và `_run_bcp_in` đã sửa

```python
def _run_bcp_queryout(self, query: str, output_file: str, prod_parts: dict[str, str]) -> None:
    if not query.strip().lower().startswith("select"):
        raise ValueError("Kết nối Production chỉ được phép truy vấn SELECT/BCP OUT")

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
        "-t\t",
        "-r\n",
        "-q",
    ]
    self._log(f"BCP queryout: {' '.join(command)}")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        shell=False,
    )
    while True:
        line = process.stdout.readline() if process.stdout is not None else ""
        if not line and process.poll() is not None:
            break
        if line:
            print(line.strip(), flush=True)
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command)


def _run_bcp_in(self, full_table_name: str, input_file: str, dm_parts: dict[str, str]) -> None:
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
        "-t\t",
        "-r\n",
        "-q",
    ]
    self._log(f"BCP in: {' '.join(command)}")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        shell=False,
    )
    while True:
        line = process.stdout.readline() if process.stdout is not None else ""
        if not line and process.poll() is not None:
            break
        if line:
            print(line.strip(), flush=True)
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, command)
```

## 2) Trích dẫn các đoạn text đã chèn vào tài liệu tri thức

### Trích từ `PROJECT_CHRONICLE.md`

> "### ADR-12: Nâng cấp giám sát real-time cho FULL_LOAD Dimension"

> "Chuyển cơ chế thực thi BCP trong `DimensionLoader` từ `subprocess.run` sang `subprocess.Popen` để stream log theo thời gian thực, tránh hiện tượng nuốt log khi xử lý bảng lớn (đặc biệt `DimBenhNhan`)."

> "Guard Production ở `_run_bcp_queryout` không thay đổi: chỉ chấp nhận câu lệnh bắt đầu bằng `SELECT`."

### Trích từ `docs/knowledge/GEM_CODE_MAP.md`

> "Hàm `_run_bcp_queryout(...)` dùng `subprocess.Popen` để stream `stdout` theo từng dòng trong lúc BCP đang chạy."

> "Hàm `_run_bcp_in(...)` dùng `subprocess.Popen` để stream `stdout` theo từng dòng trong lúc BCP đang chạy."

> "Guard an toàn Production giữ nguyên tại `_run_bcp_queryout`: chỉ cho phép câu lệnh bắt đầu bằng `SELECT`."

### Trích từ `docs/knowledge/GEM_AUTO_PIPELINE.md`

> "## Cơ chế Giám sát (Monitoring)"

> "Log runtime dùng timestamp đến mili-giây theo format `YYYY-MM-DD HH:MM:SS.mmm` và `flush=True` để đẩy ra terminal ngay lập tức."

> "BCP `queryout` và `in` được chạy bằng `subprocess.Popen` thay cho `subprocess.run`."
