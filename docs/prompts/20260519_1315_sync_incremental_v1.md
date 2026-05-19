
**# YÊU CẦU CỦA MASTER**
Thực hiện tái cấu trúc và nâng cấp module đồng bộ Incremental Load (Python OOP) cho các bảng Sự kiện (Fact) và Doanh thu. Áp dụng chuẩn Staging 3 tầng, Lookback Window, tự động loại trừ Data Types. Bắt buộc giữ nguyên Datamart schema hiện tại, không can thiệp SQL Template và cập nhật toàn diện hệ thống tài liệu.

1. **Bắt buộc đọc:**

* `GEM_CODE_MAP.md`
* `GEM_DATA_FLOW.md`
* `GEM_TECHNICAL_STANDARDS.md`
* `PROJECT_CHRONICLE.md`

2. **Yêu cầu chi tiết:**

* **Cấu hình `tables.yaml`:**
* Bổ sung tham số `lookback_days` và `exclude_datatypes` cho các bảng tương ứng.
* **Bắt buộc:** Phía trên mỗi biến mới cấu hình, phải viết block comment giải thích rõ: Mục đích sử dụng, trường hợp nào nên dùng, các giá trị có thể chấp nhận và ý nghĩa của từng giá trị. (Ví dụ: `lookback_days` nhận giá trị int >= 0; `exclude_datatypes` nhận dạng list string tên kiểu dữ liệu).
* Cấu hình chính xác `date_column` cho các bảng Incremental:
* `ThuPhiDichVu`, `ThuPhiBaoHiem`, `ThuPhiTangGiam`: sử dụng `NgayDenKham`.
* `ThuPhiGoi`: sử dụng `NgayThu`.
* `DoThiLuc`: sử dụng `NgayDo`.
* `HoSoKhamBenhNgoaiTru`: sử dụng `NgayVaoKham`, cấu hình `type: fact`, `merge_script: src/db/templates/sql/fact/DimLuotKham_merge.sql`.


* Mục tiêu nạp: Tất cả dữ liệu đích vẫn trỏ về schema `dm` (tuyệt đối không tạo schema mới).


* **Nâng cấp Tầng Code Lõi (OOP Python tại `src/core/base_extractor.py` và luồng liên quan):**
* Viết phương thức tự động đọc mảng `exclude_datatypes` từ config. Nếu tồn tại, thực hiện truy vấn động vào `INFORMATION_SCHEMA.COLUMNS` của DB nguồn để loại trừ các cột tương ứng, tự sinh câu lệnh `SELECT col1, col2...`.
* Logic Incremental: Cập nhật biến `date_from = date_from - lookback_days` trước khi thực thi query filter.
* Giao tiếp Database: Bắt buộc sử dụng BCP với flag `-w` định dạng UTF-16-LE. Bảo tồn tuyệt đối các thuật ngữ y tế tiếng Việt gốc (ví dụ: "nhược thị", "lượt khám").


* **Ràng buộc Kiến trúc Staging 3 Tầng & File SQL:**
* Tầng 1 (Global Transient Staging): Dùng TRUNCATE + INSERT.
* Tầng 2 (Facility Historical Staging): Bắt buộc dùng UPSERT/MERGE qua API có sẵn, nghiêm cấm sử dụng TRUNCATE.
* Tầng 3 (Datamart): Chỉ được phép ĐỌC và THỰC THI các file SQL trong `/src/db/templates/sql/fact/` và `/dimension/`. Tuyệt đối KHÔNG CHỈNH SỬA nội dung file SQL.
* Bắt buộc áp dụng Logic SQL Fallback doanh thu (SMI-3) đã viết sẵn: `COALESCE(ThuPhiDichVu.TongTienSauTangGiam, ThuPhiDichVu.TongTien)`.


* **Quản lý Môi trường:** - Mọi thao tác cấu hình package (nếu cần) phải sử dụng công cụ **uv** (Astral). Tuyệt đối không dùng `pip` hay `conda`.

3. **Kết quả đối soát:**

* Cung cấp Output mẫu của một câu lệnh Dynamic SELECT sau khi loại bỏ cột qua `INFORMATION_SCHEMA`.
* Trích xuất nội dung block comment mẫu trong `tables.yaml` để Master kiểm chứng chất lượng tài liệu.

4. **Cập nhật tri thức:**

* Cập nhật định nghĩa và kiến trúc cấp phát động (lookback, exclude) vào `GEM_CODE_MAP.md` và `GEM_TECHNICAL_STANDARDS.md`.
* Ghi chú các cột ngày cấu hình tương ứng vào `GEM_DATA_FLOW.md`.
* **Bắt buộc:** Ghi chép (Log) sự kiện thay đổi kiến trúc quan trọng này vào `PROJECT_CHRONICLE.md` với đầy đủ ngày tháng, lý do thay đổi và danh sách module bị ảnh hưởng.

5. **Kết xuất báo cáo:**

* Liệt kê toàn bộ file code và cấu hình đã chỉnh sửa vào `REPORT_CHANGES.md`.

6. **Chỉ dẫn phản hồi:**
Mô tả các việc đã làm vào ngay file yêu cầu, bên dưới mục #BÁO CÁO CỦA THỢ CODE.

**# BÁO CÁO CỦA THỢ CODE**

## 1) Danh sách file đã cập nhật
- `config/tables.yaml`
- `src/core/base_extractor.py` (tạo mới)
- `src/jobs/fact_loader.py`
- `src/jobs/sync_orchestrator.py`
- `docs/knowledge/GEM_CODE_MAP.md`
- `docs/knowledge/GEM_DATA_FLOW.md`
- `docs/knowledge/GEM_TECHNICAL_STANDARDS.md`
- `PROJECT_CHRONICLE.md`
- `REPORT_CHANGES.md`
- `docs/prompts/20260519_1315_sync_incremental_v1.md`

## 2) Mô tả các việc đã làm

### 2.1. Nâng cấp cấu hình `tables.yaml` cho incremental động
- Đã bổ sung node `incremental_tables` cho các bảng:
  - `ThuPhiDichVu`, `ThuPhiBaoHiem`, `ThuPhiTangGiam` với `date_column: NgayDenKham`.
  - `ThuPhiGoi` với `date_column: NgayThu`.
  - `DoThiLuc` với `date_column: NgayDo`.
  - `HoSoKhamBenhNgoaiTru` với `date_column: NgayVaoKham`, `type: fact`, `merge_script: src/db/templates/sql/fact/DimLuotKham_merge.sql`.
- Trên mỗi biến `lookback_days` và `exclude_datatypes` đều có block comment giải thích:
  - mục đích,
  - trường hợp sử dụng,
  - kiểu dữ liệu hợp lệ,
  - ý nghĩa giá trị.

### 2.2. Tạo tầng lõi extractor OOP mới
- Tạo mới `src/core/base_extractor.py` gồm:
  - `ExtractPlan` (dataclass) mô tả kế hoạch extract.
  - `normalize_date(...)` chuẩn hóa input ngày.
  - `compute_effective_from_date(...)` áp dụng `date_from - lookback_days`.
  - `build_dynamic_select_columns(...)` đọc `INFORMATION_SCHEMA.COLUMNS`, loại cột theo `exclude_datatypes`.
  - `build_select_sql(...)` sinh dynamic SELECT theo cột hợp lệ và khoảng ngày.

### 2.3. Refactor `FactLoader` theo kiến trúc 3 tầng + cấu hình động
- Đọc cấu hình động từ `incremental_tables` thay cho hardcode.
- Luồng thực thi:
  1. Tầng 1 Global Transient Staging (`stg_nano_v2`): `TRUNCATE` + BCP `-w`.
  2. Tầng 2 Facility Historical Staging: MERGE/UPSERT (không `TRUNCATE`).
  3. Tầng 3 Datamart `dm`: chỉ đọc và thực thi SQL template qua `merge_script`.
- Giữ nguyên yêu cầu không chỉnh sửa nội dung SQL template trong `src/db/templates/sql/fact/` và `src/db/templates/sql/dimension/`.

### 2.4. Hotfix treo lock khi phối hợp pyodbc và BCP
- Trong `FactLoader._truncate_table(...)` đã thêm `connection.commit()` ngay sau `TRUNCATE`.
- Mục tiêu: giải phóng lock sớm trước khi tiến trình BCP IN (session khác) chạy, tránh treo pipeline.

### 2.5. Đồng bộ orchestrator
- `src/jobs/sync_orchestrator.py` đã truyền `tables_config_path` vào `FactLoader` để thống nhất nguồn cấu hình.

### 2.6. Cập nhật tri thức bắt buộc
- `GEM_CODE_MAP.md`: bổ sung cấu phần `BaseExtractor`, incremental động, và chốt chống lock.
- `GEM_DATA_FLOW.md`: cập nhật mapping cột ngày, dynamic select/exclude datatype, và commit sau truncate landing.
- `GEM_TECHNICAL_STANDARDS.md`: bổ sung chuẩn kỹ thuật incremental động và chuẩn staging 3 tầng.
- `PROJECT_CHRONICLE.md`: thêm ADR-21 (tái cấu trúc incremental động) và ADR-22 (hotfix lock).

## 3) Kết quả đối soát theo yêu cầu

### 3.1. Output mẫu Dynamic SELECT sau loại cột theo `INFORMATION_SCHEMA`
Ví dụ output mẫu (giả định với bảng `ThuPhiDichVu`, đã loại các cột `image/text/ntext/sql_variant/xml`):

```sql
SELECT [MaThuPhi], [MaPhieuDichVu], [MaHoSo], [MaChiTieu], [NgayDenKham], [TongTien], [TongTienSauTangGiam], [DaDongTien]
FROM dbo.[ThuPhiDichVu] WITH (NOLOCK)
WHERE CAST([NgayDenKham] AS DATE) >= '2026-05-16'
AND CAST([NgayDenKham] AS DATE) <= '2026-05-19'
```

### 3.2. Trích xuất block comment mẫu trong `tables.yaml`

```yaml
# Mục đích: Định nghĩa số ngày tua ngược cửa sổ incremental để tránh sót dữ liệu đến trễ.
# Khi dùng: Dùng cho bảng phát sinh có khả năng điều chỉnh/hạch toán lại trong các ngày gần đây.
# Giá trị hợp lệ: int >= 0.
# Ý nghĩa: 0 = chỉ nạp đúng from_date; N > 0 = dịch lùi from_date thêm N ngày trước khi lọc.
lookback_days: 3
# Mục đích: Loại các cột có kiểu dữ liệu đặc biệt gây rủi ro BCP/không cần cho downstream.
# Khi dùng: Dùng khi bảng nguồn chứa cột binary/blob/xml/text lớn hoặc kiểu không tương thích.
# Giá trị hợp lệ: list[string], mỗi phần tử là DATA_TYPE trong INFORMATION_SCHEMA.COLUMNS.
# Ý nghĩa: Cột nào có DATA_TYPE thuộc danh sách này sẽ bị loại khỏi dynamic SELECT.
exclude_datatypes:
  - image
  - text
  - ntext
  - sql_variant
  - xml
```

## 4) Kiểm tra nhanh
- Đã chạy: `python -m compileall src`
- Kết quả: thành công, không phát hiện lỗi cú pháp trong các module đã sửa.
