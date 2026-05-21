
**# YÊU CẦU CỦA MASTER**
Hủy bỏ hoàn toàn kế hoạch sử dụng BCP cho luồng Incremental. Tái cấu trúc luồng đồng bộ Incremental quay về sử dụng thư viện `pyodbc` (như bản V1) để đảm bảo tính ổn định tuyệt đối trong việc ép kiểu dữ liệu ngầm, kết hợp với cơ chế Whitelist để tối ưu hóa bộ nhớ. Bắt buộc duy trì kiến trúc Staging 3 tầng.

### 1. Yêu cầu triển khai chi tiết cho Thợ code:

#### 1.1. Cấu hình `config/tables.yaml` (Duy trì Whitelist):

* Tiếp tục sử dụng biến `selected_columns` cho các bảng Incremental để người quản trị chỉ định đích danh các cột cần lấy.
* Xóa bỏ hoàn toàn logic `exclude_datatypes`.
* Viết một script độc lập. Script này sử dụng chuỗi kết nối môi trường đích STAGING_CONNECTION_STRING để kết nối vào Database Staging.
Logic xử lý của script:
- Quét hệ thống INFORMATION_SCHEMA.COLUMNS của chính các bảng đích tương ứng trong schema stg_nano_v2 (bao gồm: ThuPhiDichVu, ThuPhiBaoHiem, ThuPhiTangGiam, ThuPhiGoi, DoThiLuc, HoSoKhamBenhNgoaiTru).
- Sắp xếp danh sách cột thu được nghiêm ngặt theo đúng ORDINAL_POSITION (vị trí hình học vật lý của bảng Staging).
- Loại trừ tự động: Loại bỏ 3 cột Enrichment Key hệ thống ra khỏi danh sách kết quả (gồm: MaCoSo, CoSoKey, NguonDuLieuKey).
- Thực hiện .strip() làm sạch khoảng trắng ở tên cột.
- Tự động ghi trực tiếp (hoặc in ra định dạng cấu trúc YAML chuẩn) danh sách các cột sản xuất còn lại vào biến selected_columns của từng bảng tương ứng trong tệp tin config/tables.yaml.

#### 1.2. Đơn giản hóa `src/core/base_extractor.py` (Không cần đệm NULL):

* Build câu lệnh `SELECT` động chỉ chứa các cột được liệt kê trong `selected_columns`.
* **Lợi thế PyODBC:** Vì `pyodbc` map dữ liệu theo tên cột (không phải vị trí vật lý như BCP), mày **KHÔNG CẦN** phải sinh thêm các cột đệm `CAST(NULL AS INT)` cho `CoSoKey` hay `NguonDuLieuKey` vào câu lệnh truy vấn nữa. Chỉ cần SELECT đúng danh sách sản xuất.

#### 1.3. Đập bỏ BCP, khôi phục luồng nạp PyODBC tại `src/core/base_loader.py` & `fact_loader.py`:

* **Xóa bỏ hoàn toàn** các hàm `run_bcp_utf16le` và `run_bcp_in` cho luồng Incremental. Không cần phải parse Connection String bằng Regex nữa!
* **Khôi phục quy trình Tầng 1 (Transient Staging) an toàn bằng RAM:**
1. Mở Connection vào DB Nguồn (Production) ➔ Gọi `cursor.execute(select_sql)` và dùng `fetchall()` (hoặc `fetchmany` chia chunk) để kéo dữ liệu vào bộ nhớ RAM của Python.
2. Mở Connection vào DB Đích (Staging) ➔ Thực thi `TRUNCATE TABLE stg_nano_v2.[TenBang]`.
3. Sử dụng `cursor.executemany()` (khuyến khích bật `fast_executemany = True` của pyodbc) để INSERT trực tiếp mảng dữ liệu trong RAM vào bảng `stg_nano_v2.[TenBang]`. Các cột metadata của Staging (như `CoSoKey`) nếu trong lệnh INSERT không truyền thì DB sẽ tự nhận giá trị mặc định hoặc NULL.
4. Gọi `commit()` để hoàn tất Tầng 1.


* **Quy trình Tầng 2 & 3:**
5. Tiếp tục sử dụng Connection Đích để gọi thực thi câu lệnh SQL MERGE động (hoặc từ template) để đẩy dữ liệu từ `stg_nano_v2` sang `hanoi_hisnano_v2` và Datamart.

### 2. Cập nhật Tri thức và Tài liệu:

* **`GEM_TECHNICAL_STANDARDS.md`, `GEM_MAP_CODE.md`:** Xóa bỏ các quy định khắt khe về vị trí hình học của BCP đối với luồng Incremental. Cập nhật chuẩn nạp dữ liệu: "Sử dụng PyODBC `fast_executemany` kết hợp Whitelist để tối ưu sự ổn định cho cả FULL_LOAD và INCREMENTAL_LOAD."
* **`PROJECT_CHRONICLE.md`:** Ghi nhận ADR: "Quyết định chiến lược từ Master - Từ bỏ BCP, quay về kiến trúc nạp PyODBC cho Incremental Load để đảm bảo an toàn ép kiểu dữ liệu (Implicit Casting), chấp nhận đánh đổi tốc độ nạp Bulk nhưng bù đắp bằng cơ chế lọc Whitelist trên RAM."
* **`REPORT_CHANGES.md`:** Liệt kê các file Python được dọn dẹp lại.

### 3. Chỉ dẫn phản hồi:

Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE. Không cần sinh script hay in log BCP phức tạp nữa.

**# BÁO CÁO CỦA THỢ CODE**

## 1) Các tệp đã cập nhật

- `src/core/base_extractor.py`
- `src/core/base_loader.py`
- `src/jobs/fact_loader.py`
- `scripts/sync_selected_columns_from_staging.py` (mới)
- `config/tables.yaml`
- `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`
- `docs/knowledge/GEM_CODE_MAP.md`
- `PROJECT_CHRONICLE.md`
- `REPORT_CHANGES.md`
- `docs/prompts/20260520_1540_sync_incremental_v6.md`

## 2) Kết quả triển khai theo yêu cầu

### 2.1. Duy trì Whitelist trong `config/tables.yaml`
- Giữ `selected_columns` cho 6 bảng incremental.
- Không có `exclude_datatypes`.
- Cập nhật chú thích để phản ánh chuẩn mới: SELECT động chỉ lấy cột sản xuất, nạp bằng PyODBC.

### 2.2. Viết script đồng bộ `selected_columns` từ Staging
- Đã tạo `scripts/sync_selected_columns_from_staging.py`.
- Script dùng `STAGING_CONNECTION_STRING` từ môi trường (`config/.env`).
- Quét `INFORMATION_SCHEMA.COLUMNS` trong schema `stg_nano_v2` cho 6 bảng:
  - `ThuPhiDichVu`, `ThuPhiBaoHiem`, `ThuPhiTangGiam`, `ThuPhiGoi`, `DoThiLuc`, `HoSoKhamBenhNgoaiTru`.
- Sắp xếp theo `ORDINAL_POSITION`.
- Làm sạch tên cột bằng `.strip()`.
- Tự loại 3 cột hệ thống:
  - `MaCoSo`, `CoSoKey`, `NguonDuLieuKey`.
- Hỗ trợ 2 chế độ:
  - Preview YAML ra terminal.
  - Ghi thẳng vào `config/tables.yaml` bằng cờ `--write`.

### 2.3. Đơn giản hóa `base_extractor.py`
- `build_extract_plan(...)` chỉ nhận `selected_columns`.
- Dynamic SELECT chỉ chứa cột từ Whitelist.
- Bỏ hoàn toàn ghép cột enrichment vào câu SELECT incremental.

### 2.4. Đập bỏ BCP, khôi phục nạp PyODBC ở Incremental
- `src/core/base_loader.py`:
  - Xóa các hàm/logic BCP và parse regex connection string:
    - `parse_connection_string`, `_build_bcp_connection_args`, `_mask_bcp_command`, `run_bcp_utf16le`, `run_bcp_in`.
- `src/jobs/fact_loader.py`:
  - Tầng 1 chuyển sang pipeline PyODBC:
    1. `cursor.execute(select_sql)` từ Production.
    2. `TRUNCATE stg_nano_v2.[TenBang]` đúng 1 lần trước loop.
    3. `fetchmany(batch_size)` + `executemany(...)` vào Landing.
    4. `commit()` hoàn tất Tầng 1.
  - Đã áp dụng đúng 2 nguyên tắc bắt buộc:
    - INSERT động tường minh theo `selected_columns`:
      - `INSERT INTO [stg_nano_v2].[TenBang] ([Col1], [Col2], ...) VALUES (?, ?, ...)`.
    - TRUNCATE chạy ngoài vòng chunking, đúng 1 lần.
  - Tầng 2 và 3 vẫn chạy MERGE như cũ.

## 3) Cập nhật tri thức

- `GEM_TECHNICAL_STANDARDS.md`:
  - Gỡ quy định BCP cho incremental.
  - Chuẩn mới: PyODBC `executemany` + `fast_executemany`, TRUNCATE 1 lần ngoài loop, INSERT tường minh theo Whitelist.
- `GEM_CODE_MAP.md`:
  - Bổ sung mục v6: bỏ BCP incremental, chuyển kiến trúc sang PyODBC chunking, thêm script sync whitelist.
- `PROJECT_CHRONICLE.md`:
  - Ghi ADR-34/35/36 cho quyết định chiến lược bỏ BCP và chuẩn nạp mới.

## 4) Danh sách file Python được dọn dẹp

- `src/core/base_extractor.py`
- `src/core/base_loader.py`
- `src/jobs/fact_loader.py`
- `scripts/sync_selected_columns_from_staging.py`