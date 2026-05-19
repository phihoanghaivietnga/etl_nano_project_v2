
# YÊU CẦU CỦA MASTER: KIẾN TRÚC YAML CONFIG VÀ TENANT INJECTION (MULTI-TENANT)

1. **PHÂN TÍCH KIẾN TRÚC (ADR-19 & ADR-20):**
* **ADR-19 (YAML Configuration Matrix):** Hệ thống V2 quản lý đa cơ sở (Multi-tenant), việc sử dụng file `.env` để lưu danh sách cơ sở (`ACTIVE_FACILITIES`) và `chunk_size` đã trở nên chật chội. Quyết định: Toàn bộ tham số vận hành (chunk_size) và ma trận ID của các cơ sở phải chuyển sang file `config/tables.yaml`.
* **ADR-20 (Tenant Injection):** Dữ liệu Production là Single-tenant (không chứa 3 cột định danh cơ sở). Khi đưa lên Datamart (Multi-tenant), SQL Server báo lỗi `Cannot insert the value NULL`. Giải pháp: Lớp `DimensionLoader` sẽ đọc ma trận từ `tables.yaml` theo `facility_code`, lấy ra `nguon_dulieu_key` và `co_so_key`, sau đó tự động nối (inject) 3 cột này vào dòng dữ liệu trên RAM trước khi đẩy vào ODS.

2. **CHỈ THỊ THỰC THI MÃ NGUỒN:**

* **A. Khởi tạo/Cập nhật file `config/tables.yaml`:**
Tạo hoặc ghi đè file `config/tables.yaml` với cấu trúc sau:
```yaml
etl_settings:
  odbc_chunk_size: 5000
  active_facilities: 
    - hanoi

facilities:
  hanoi:
    nguon_dulieu_key: 2
    co_so_key: 1
    staging_schema: hanoi_hisnano_v2

```

* **B. Sửa đổi `src/jobs/sync_orchestrator.py`:**
Xóa logic đọc `ACTIVE_FACILITIES` từ `os.environ` hoặc `.env`. Thay bằng logic dùng thư viện `yaml` đọc từ `config/tables.yaml` (khóa `etl_settings.active_facilities`).
* **C. Refactor `_copy_prod_to_ods` trong `src/jobs/dimension_loader.py`:**
BẮT BUỘC thực hiện 2 thay đổi lõi trong hàm này:

* **Đọc Chunk Size từ YAML:** Thay vì dùng `os.environ.get`, hãy đọc giá trị `odbc_chunk_size` từ file `tables.yaml`.
* **Tenant Injection:** Đọc `nguon_dulieu_key` và `co_so_key` từ node `facilities` trong YAML. Nối thêm 3 cột `["NguonDuLieuKey", "CoSoKey", "MaCoSo"]` vào danh sách cột của ODS. Biến đổi dữ liệu dòng bằng `tuple(row) + tenant_values`.

```python
            # ... (Sau khi execute SELECT từ prod_cursor)
            import yaml
            from pathlib import Path
            
            prod_columns = [column[0] for column in prod_cursor.description]
            
            # 1. Đọc YAML Config
            yaml_path = Path("config/tables.yaml")
            with open(yaml_path, "r", encoding="utf-8") as f:
                config_data = yaml.safe_load(f)
            
            # Đọc chunk_size và thông tin facility từ YAML
            chunk_size = config_data.get("etl_settings", {}).get("odbc_chunk_size", 2000)
            facility_config = config_data.get("facilities", {}).get(self.facility_code, {})
            current_nguon_key = facility_config.get("nguon_dulieu_key", -1)
            current_coso_key = facility_config.get("co_so_key", -1)
            
            # 2. Chuẩn bị Tenant Injection
            tenant_columns = ["NguonDuLieuKey", "CoSoKey", "MaCoSo"]
            target_columns = prod_columns + tenant_columns
            tenant_values = (current_nguon_key, current_coso_key, self.facility_code)
            
            # 3. Build câu lệnh INSERT động
            col_names_str = ", ".join([f"[{c}]" for c in target_columns])
            placeholders = ", ".join(["?"] * len(target_columns))
            insert_sql = f"INSERT INTO [{self.facility_schema}].[{table_name}] ({col_names_str}) VALUES ({placeholders})"
            
            stg_cursor = connection.cursor()
            
            total_rows = 0
            while True:
                rows = prod_cursor.fetchmany(chunk_size)
                if not rows:
                    break
                
                # 4. Tiêm dữ liệu Tenant (Tenant Injection)
                data_chunk = [tuple(row) + tenant_values for row in rows]
                
                stg_cursor.executemany(insert_sql, data_chunk)
                connection.commit()
                # ...

```

3. **CHỈ THỊ CẬP NHẬT TRI THỨC (`agents.md` BẮT BUỘC):**

* **`PROJECT_CHRONICLE.md`:** Cập nhật **ADR-19** (chuyển config sang YAML) và **ADR-20** (triển khai Tenant Injection tại DimensionLoader để xử lý lỗi thiếu cột khi MERGE).
* **`docs/knowledge/GEM_CODE_MAP.md`:** Cập nhật mô tả của hàm `_copy_prod_to_ods` trong lớp `DimensionLoader`. Ghi rõ hàm này giờ đây chịu trách nhiệm: (1) Đọc cấu hình `chunk_size` từ YAML, (2) Lấy tham số cơ sở từ YAML, (3) Tự động thực hiện **Tenant Injection** (nối thêm NguonDuLieuKey, CoSoKey, MaCoSo) vào luồng ODBC Bulk Copy.
* **`docs/knowledge/GEM_AUTO_PIPELINE.md`:** Cập nhật hướng dẫn khai báo tham số vận hành sang file `config/tables.yaml`.
* **`REPORT_CHANGES.md`:** Ghi nhận hotfix cấu trúc YAML và Tenant Injection.

4. **CHỈ DẪN PHẢN HỒI:**
Dưới thẻ `# BÁO CÁO CỦA THỢ CODE`, dán nguyên văn phần xử lý đọc file YAML tại `sync_orchestrator.py` và vòng lặp `while True` đã được sửa trong `dimension_loader.py`. Đồng thời trích dẫn nội dung đã cập nhật trong `GEM_CODE_MAP.md`.

# BÁO CÁO CỦA THỢ CODE

## Phần xử lý đọc YAML tại `sync_orchestrator.py`

```python
def _load_tables_config(self) -> dict:
    if not self.tables_config_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file cấu hình YAML: {self.tables_config_path}")
    with self.tables_config_path.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream) or {}
    return data

def _resolve_target_facilities(self, target_facilities: list[str] | None = None) -> list[str]:
    if target_facilities is not None:
        normalized = [facility.strip().lower() for facility in target_facilities if facility.strip()]
        if not normalized or "all" in normalized:
            return list(self.facility_registry.keys())
        return normalized

    yaml_facilities = self.tables_config.get("etl_settings", {}).get("active_facilities", [])
    if not yaml_facilities:
        return list(self.facility_registry.keys())
    normalized = [str(facility).strip().lower() for facility in yaml_facilities if str(facility).strip()]
    return normalized or list(self.facility_registry.keys())
```

## Vòng lặp `while True` đã sửa trong `dimension_loader.py`

```python
total_rows = 0

while True:
    rows = prod_cursor.fetchmany(chunk_size)
    if not rows:
        break

    # Tiêm dữ liệu Tenant (Tenant Injection)
    data_chunk = [tuple(row) + tenant_values for row in rows]
    stg_cursor.executemany(insert_sql, data_chunk)
    connection.commit()

    total_rows += len(data_chunk)
    self._log(f"Đã copy {total_rows} dòng vào ODS...")
```

## Trích dẫn nội dung đã cập nhật trong `GEM_CODE_MAP.md`

> - Hàm `_copy_prod_to_ods(...)` đọc `odbc_chunk_size` từ `config/tables.yaml`.
> - Hàm `_copy_prod_to_ods(...)` đọc cấu hình facility từ YAML để lấy `nguon_dulieu_key` và `co_so_key` theo `facility_code`.
> - Hàm `_copy_prod_to_ods(...)` tự động Tenant Injection bằng cách nối thêm 3 cột `NguonDuLieuKey`, `CoSoKey`, `MaCoSo` vào payload insert ODS.