
**# YÊU CẦU CỦA MASTER**
Tái cấu trúc luồng đồng bộ Incremental: Chuyển đổi toàn diện sang cơ chế cấu hình Whitelist cột trong `tables.yaml`. Xóa bỏ triệt để logic quét metadata loại trừ (`exclude_datatypes`), thực hiện ghép các cột enrichment key có sẵn từ cấu hình cơ sở vào câu lệnh truy vấn để bảo toàn cấu trúc hình học cho BCP và cô lập giao dịch biên chống Deadlock.

### 1. Các file tài liệu bắt buộc phải cập nhật sau khi xử lý:

* `docs/knowledge/GEM_TECHNICAL_STANDARDS.md` (Cập nhật chuẩn Whitelist và loại bỏ tiêu chuẩn Black-list).
* `docs/knowledge/GEM_CODE_MAP.md` (Cập nhật vai trò mới của Extractor và Loader theo cấu trúc Whitelist).
* `PROJECT_CHRONICLE.md` (Ghi nhận ADR thay đổi kiến trúc sang Whitelist cột, đồng bộ cờ BCP và an toàn giao dịch tránh deadlock).
* `REPORT_CHANGES.md` (Liệt kê chính xác danh sách các tệp `.py` và `.yaml` bị tác động thay đổi).

### 2. Yêu cầu triển khai chi tiết cho Thợ code:

#### 2.1. Cấu hình lại toàn diện `config/tables.yaml`:

* **Xóa bỏ hoàn toàn và không để lại bất kỳ dấu vết nào** của biến `exclude_datatypes` ở tất cả các bảng trong cấu hình `incremental_tables`.
* Bổ sung tham số `selected_columns` (kiểu mảng danh sách chuỗi - `list[string]`) cho từng bảng Incremental (`ThuPhiDichVu`, `ThuPhiBaoHiem`, `ThuPhiTangGiam`, `ThuPhiGoi`, `DoThiLuc`, `HoSoKhamBenhNgoaiTru`).
* Người quản trị sẽ tự điền thủ công danh sách các cột cần đồng bộ từ Production vào đây (đã chủ động lược bỏ các cột image, text, xml nặng).

#### 2.2. Thanh trừng và viết lại logic tại `src/core/base_extractor.py`:

* **Xóa bỏ triệt để toàn bộ mã nguồn** liên quan đến hàm `build_dynamic_select_columns` cũ (logic kết nối và quét bảng `INFORMATION_SCHEMA.COLUMNS`).
* Nâng cấp phương thức sinh SQL để đọc trực tiếp mảng `selected_columns` từ `tables.yaml`.
* **Logic ghép cột ngữ cảnh:** Nhận vào các giá trị biến có sẵn từ hệ thống: `co_so_key`, `nguon_du_lieu_key`, `ma_co_so`. Tự động bổ sung các biểu thức trường này vào danh sách cột SELECT (Ví dụ: `SELECT [Cot1], [Cot2], ..., {co_so_key} AS [CoSoKey], {nguon_du_lieu_key} AS [NguonDuLieuKey], '{ma_co_so}' AS [MaCoSo] FROM ...`).
* Đảm bảo thứ tự và số lượng cột được tạo ra trong câu lệnh `SELECT` động này phải khớp chính xác 100% với cấu trúc vật lý của bảng đích `stg_nano_v2` để file text xuất ra không bị lệch vị trí khi nạp thô.

#### 2.3. Chuẩn hóa BCP và cô lập biên giao dịch tại `src/core/base_loader.py` và `src/jobs/fact_loader.py`:

* Hàm BCP OUT (`run_bcp_utf16le`) nhận chuỗi kết nối nguồn để kéo dữ liệu ra file text, bắt buộc ép các cờ định dạng: `-w`, `-t\t`, `-r\n`.
* Viết mới hàm BCP IN (`run_bcp_in`) nhận chuỗi kết nối đích chọc vào Staging, bắt buộc ép đầy đủ các cờ: `-w`, `-k` (Keep Nulls), `-E` (Keep Identity), `-t\t`, `-r\n`.
* **Quy trình tuần tự an toàn tại Tầng 1 (Ngăn chặn Deadlock):**
1. Chạy tiến trình BCP OUT để xuất file dữ liệu thô hoàn tất.
2. Mở Connection A chọc vào DB đích ➔ Thực thi lệnh `TRUNCATE TABLE stg_nano_v2.[TenBang]` ➔ Gọi `commit()`.
3. **Đóng và giải phóng hoàn toàn Connection A ngay lập tức** để giải phóng khóa Sch-M (Schema-Modification Lock) trên bảng.
4. Gọi tiến trình `subprocess` chạy lệnh BCP IN để nạp file vào bảng landing, chờ tiến trình trả về `exit code == 0`.
5. Sau khi BCP IN hoàn thành, mới mở Connection B hoàn toàn mới để thực thi tệp tin SQL MERGE dữ liệu sang tầng tiếp theo.



#### 2.4. Ràng buộc môi trường và đối soát:

* Đảm bảo bảo tồn nguyên vẹn thuật ngữ y khoa tiếng Việt (nhược thị, lượt khám) qua cờ `-w`.
* Mọi thao tác liên quan đến môi trường/package (nếu có) bắt buộc chỉ dùng **uv** (Astral).
* Ẩn mật khẩu (`-P ******`) trong tất cả các dòng log in ra console.

### 3. Kết quả đối soát cung cấp tại báo cáo:

* In ra màn hình câu lệnh `SELECT` động mẫu hoàn chỉnh sau khi ghép nối danh sách cột Whitelist và 3 biến ngữ cảnh.
* Trích xuất nguyên văn đoạn code Python thực hiện xử lý đóng/mở Connection tuần tự xung quanh lệnh BCP IN trong `fact_loader.py` để chứng minh đã xử lý triệt để nguy cơ Deadlock.

---

**# BÁO CÁO CỦA THỢ CODE**

## 1) Tệp đã cập nhật theo yêu cầu

- `config/tables.yaml`
- `src/core/base_extractor.py`
- `src/core/base_loader.py`
- `src/jobs/fact_loader.py`
- `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`
- `docs/knowledge/GEM_CODE_MAP.md`
- `PROJECT_CHRONICLE.md`
- `REPORT_CHANGES.md`
- `docs/prompts/20260520_1435_sync_incremental_v5.md`

## 2) Kết quả triển khai kỹ thuật

### 2.1. Cấu hình `tables.yaml` chuyển hoàn toàn sang Whitelist
- Đã xóa toàn bộ `exclude_datatypes` khỏi 6 bảng incremental.
- Đã bổ sung `selected_columns: []` cho:
  - `ThuPhiDichVu`
  - `ThuPhiBaoHiem`
  - `ThuPhiTangGiam`
  - `ThuPhiGoi`
  - `DoThiLuc`
  - `HoSoKhamBenhNgoaiTru`

### 2.2. Thanh trừng metadata-scan trong `base_extractor.py`
- Đã xóa toàn bộ logic cũ liên quan:
  - `DynamicColumnProjection`
  - `build_dynamic_select_columns(...)`
  - truy vấn `INFORMATION_SCHEMA.COLUMNS`
- `build_extract_plan(...)` hiện đọc trực tiếp `selected_columns` và ghép enrichment keys:
  - `{co_so_key} AS [CoSoKey]`
  - `{nguon_du_lieu_key} AS [NguonDuLieuKey]`
  - `'{ma_co_so}' AS [MaCoSo]`

### 2.3. Chuẩn hóa BCP và transaction boundary chống deadlock
- `src/core/base_loader.py`:
  - `run_bcp_utf16le(...)` giữ chuẩn `-w -t\t -r\n`.
  - `run_bcp_in(...)` dùng chuẩn `-w -k -E -t\t -r\n` và cho phép truyền `destination_connection_string`.
  - Log command BCP IN có che mật khẩu (`-P ******`).
- `src/jobs/fact_loader.py`:
  - `FactTableSpec` đổi sang `selected_columns`.
  - Luồng Tầng 1 giữ đúng trình tự:
    1. BCP OUT.
    2. Connection A: TRUNCATE + commit + đóng.
    3. BCP IN subprocess.
    4. Connection B mới để MERGE tầng sau.

## 3) Đối soát bắt buộc

### 3.1. Dynamic SELECT mẫu sau ghép Whitelist + 3 biến ngữ cảnh

```sql
SELECT [MaHoSo], [NgayDenKham], [TongTien], 1 AS [CoSoKey], 2 AS [NguonDuLieuKey], 'hanoi' AS [MaCoSo]
FROM dbo.[ThuPhiDichVu] WITH (NOLOCK)
WHERE CAST([NgayDenKham] AS DATE) >= '2026-05-01'
  AND CAST([NgayDenKham] AS DATE) <= '2026-05-20'
```

### 3.2. Trích code đóng/mở Connection tuần tự quanh BCP IN (chống deadlock)

```python
with self.get_db_context() as truncate_connection:
    self._truncate_table(truncate_connection, self.LANDING_SCHEMA, plan.table_name)

self.run_bcp_in(
    table_name=full_table_name,
    input_file=temp_path,
    destination_connection_string=self.connection_string,
)

with self.get_db_context() as merge_connection:
    self._upsert_from_global_to_facility_staging(
        connection=merge_connection,
        spec=spec,
        from_date=plan.effective_from_date,
        to_date=to_date,
    )
    self._merge_to_datamart_using_template(
        connection=merge_connection,
        spec=spec,
        date_from=plan.effective_from_date,
        date_to=to_date,
    )
    merge_connection.commit()
```

## 4) Cập nhật tri thức

- `GEM_TECHNICAL_STANDARDS.md`: chuẩn Whitelist + cờ BCP + transaction boundary.
- `GEM_CODE_MAP.md`: vai trò mới Extractor/FactLoader theo cơ chế Whitelist.
- `PROJECT_CHRONICLE.md`: ADR-31/32/33 cho chuyển đổi kiến trúc Whitelist và cô lập giao dịch biên.

## 5) Danh sách tệp `.py` và `.yaml` bị tác động

- `.py`:
  - `src/core/base_extractor.py`
  - `src/core/base_loader.py`
  - `src/jobs/fact_loader.py`
- `.yaml`:
  - `config/tables.yaml`
