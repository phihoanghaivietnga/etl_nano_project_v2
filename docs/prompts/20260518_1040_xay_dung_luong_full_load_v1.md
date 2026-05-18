
# YÊU CẦU CỦA MASTER DÀNH CHO CODEX: THỰC THI FULL_LOAD DANH MỤC

1. **TÀI LIỆU VÀ TÀI NGUYÊN BẮT BUỘC SỬ DỤNG:**

* Các file SQL thực thi MERGE dữ liệu từ ODS lên Datamart **ĐÃ CÓ SẴN** trong dự án. **TUYỆT ĐỐI KHÔNG ĐƯỢC VIẾT LẠI HOẶC TẠO MỚI CÁC FILE SQL NÀY**.
* Danh sách file SQL hiện có:
1. `DimBenhNhan_merge.sql`
2. `DimBenh_merge.sql`
3. `DimLoaiGoiDichVu_merge.sql`
4. `dim_dich_vu_merge.sql`



2. **CHỈ THỊ PHÁT TRIỂN PYTHON PIPELINE (`src/jobs/dimension_loader.py`):**

* Tạo class `DimensionLoader` kế thừa từ `BaseLoader` (hoặc `GenericTableLoader`).
* Thực hiện luồng 2-Hop (Production -> ODS Cơ sở -> Datamart) theo đúng quy trình sau cho mỗi bảng danh mục:
* **Bước 1 (Kéo dữ liệu):** Thực thi lệnh `TRUNCATE TABLE` trên Schema ODS của cơ sở (VD: `hanoi_hisnano_v2.<TableName>`). Sau đó dùng `subprocess` gọi `bcp -w` (UTF-16-LE) đẩy dữ liệu từ Production vào ODS.
* **Bước 2 (Merge Datamart):** Đọc nội dung file SQL tương ứng, format/bind các tham số bắt buộc (`{dm_schema}`, `{staging_schema}`, `{nguon_dulieu_key}`, `{ma_co_so}`, `{co_so_key}`) và thực thi thông qua connection đến Datamart.



3. **CẤU HÌNH MAPPING ĐẶC BIỆT (CHÚ Ý TỬ HUYỆT DimDichVu):**
Thiết lập danh sách cấu hình chạy trong Python phải tuân thủ ánh xạ sau:

* **DimBenhNhan:** Kéo bảng `DMBenhNhan` -> Chạy file `DimBenhNhan_merge.sql`
* **DimBenh:** Kéo bảng `DMBenh` -> Chạy file `DimBenh_merge.sql`
* **DimLoaiGoiDichVu:** Kéo bảng `LoaiGoiDichVuNT` -> Chạy file `DimLoaiGoiDichVu_merge.sql`
* **DimDichVu (BẮT BUỘC LÀM ĐÚNG):** Phải thực hiện Bước 1 (TRUNCATE + BCP) cho **CẢ 3 BẢNG** (`DMLoaiDichVu`, `DMDichVu`, `DMDichVuChiTiet`) vào ODS Cơ sở. Chỉ sau khi cả 3 bảng này đã nằm gọn trong ODS thì mới được phép thực thi Bước 2 là gọi file `dim_dich_vu_merge.sql`.

4. **TÍCH HỢP ORCHESTRATOR:**

* Tích hợp `DimensionLoader` vào `SyncOrchestrator` đã thiết kế. Luồng Dimension phải được chạy trót lọt xong xuôi cho một cơ sở rồi mới được phép chạy đến luồng Fact.

5. **CẬP NHẬT TÀI LIỆU TRI THỨC (BẮT BUỘC):**

* Cập nhật `PROJECT_CHRONICLE.md`: Ghi log hoàn thành tích hợp luồng Python cho FULL_LOAD 4 bảng Dimension. Nhấn mạnh việc xử lý BCP 3 bảng liên tiếp cho `DimDichVu` trước khi gọi SQL.
* Cập nhật `GEM_CODE_MAP.md`: Đăng ký class `DimensionLoader` và giải thích luồng mapping với các file SQL có sẵn.

6. **CHỈ DẪN PHẢN HỒI:**
Dưới thẻ `# BÁO CÁO CỦA THỢ CODE`, hãy:

* Liệt kê tên các class/hàm Python vừa viết.
* Cung cấp đoạn code cấu hình mapping (chứng minh đã xử lý việc kéo 3 bảng cho DimDichVu).
* Trích dẫn nguyên văn đoạn text đã cập nhật vào `PROJECT_CHRONICLE.md`.

# BÁO CÁO CỦA THỢ CODE

## 1) Danh sách class/hàm Python đã viết/chỉnh sửa

### `src/jobs/dimension_loader.py`
- `DimensionTableSpec`
- `DimensionLoader(BaseLoader)`
  - `_parse_connection_string`
  - `_build_bcp_auth_args`
  - `_run_bcp_queryout`
  - `_run_bcp_in`
  - `_truncate_table`
  - `_copy_prod_to_ods`
  - `_render_merge_sql`
  - `_execute_dimension_spec`
  - `_execute_core`

### `src/jobs/fact_loader.py`
- `FactLoader(BaseLoader)`
  - Bổ sung hằng theo dõi nợ kỹ thuật: `PENDING_INCREMENTAL_DIMENSIONS = ("DimLuotKham",)`

### `src/jobs/sync_orchestrator.py`
- `SyncOrchestrator`
  - Đã rà soát và giữ nguyên thứ tự tuần tự: chạy xong Dimension của một cơ sở mới chạy Fact.

## 2) Đoạn code cấu hình mapping (chứng minh kéo 3 bảng cho DimDichVu)

```python
DEFAULT_DIMENSION_SPECS: tuple[DimensionTableSpec, ...] = (
    DimensionTableSpec(
        dimension_name="DimBenhNhan",
        source_tables=("DMBenhNhan",),
        merge_sql_path="src/db/templates/sql/dimension/DimBenhNhan_merge.sql",
    ),
    DimensionTableSpec(
        dimension_name="DimBenh",
        source_tables=("DMBenh",),
        merge_sql_path="src/db/templates/sql/dimension/DimBenh_merge.sql",
    ),
    DimensionTableSpec(
        dimension_name="DimLoaiGoiDichVu",
        source_tables=("LoaiGoiDichVuNT",),
        merge_sql_path="src/db/templates/sql/dimension/DimLoaiGoiDichVu_merge.sql",
    ),
    DimensionTableSpec(
        dimension_name="DimDichVu",
        source_tables=("DMLoaiDichVu", "DMDichVu", "DMDichVuChiTiet"),
        merge_sql_path="src/db/templates/sql/dimension/dim_dich_vu_merge.sql",
    ),
)
```

## 3) Trích dẫn nguyên văn đoạn đã cập nhật vào `PROJECT_CHRONICLE.md`

> "### ADR-10: Điều chỉnh FULL_LOAD danh mục theo chỉ thị 20260518_1040"

> "Với `DimDichVu`, pipeline phải chạy Bước 1 liên tiếp cho cả 3 bảng `DMLoaiDichVu`, `DMDichVu`, `DMDichVuChiTiet` vào ODS cơ sở; chỉ sau khi hoàn tất mới chạy Bước 2 gọi `dim_dich_vu_merge.sql`."

> "Gỡ hoàn toàn `DimLuotKham` khỏi `DimensionLoader` để tránh rủi ro `TRUNCATE` sai vào bảng có bản chất incremental."