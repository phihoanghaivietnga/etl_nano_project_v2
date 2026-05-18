from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import pyodbc

from src.core.base_loader import BaseLoader


@dataclass(frozen=True)
class DimensionTableSpec:
    dimension_name: str
    source_tables: tuple[str, ...]
    merge_sql_path: str


class DimensionLoader(BaseLoader):
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

    def __init__(
        self,
        datamart_connection: str,
        production_connection: str,
        facility_code: str,
        facility_schema: str,
        nguon_dulieu_key: int,
        co_so_key: int,
        dimension_specs: tuple[DimensionTableSpec, ...] | None = None,
    ) -> None:
        super().__init__(connection_string=datamart_connection, table_name=f"DimensionLoader:{facility_code}")
        self.production_connection = production_connection
        self.prod_env_key = "production"
        self.connection_strings: dict[str, str] = {self.prod_env_key: production_connection}
        self.facility_code = facility_code
        self.facility_schema = facility_schema
        self.nguon_dulieu_key = nguon_dulieu_key
        self.co_so_key = co_so_key
        self.dimension_specs = dimension_specs or self.DEFAULT_DIMENSION_SPECS

    def _log(self, message: str, **kwargs) -> None:
        _ = kwargs
        from datetime import datetime

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}] {message}", flush=True)

    def _truncate_table(self, connection: pyodbc.Connection, schema_name: str, table_name: str) -> None:
        # Lệnh thay đổi dữ liệu chỉ chạy trên connection Datamart/ODS, không dùng Production.
        sql = f"TRUNCATE TABLE [{schema_name}].[{table_name}];"
        self._log(f"TRUNCATE {schema_name}.{table_name}")
        self.execute_sql_sync(connection, sql)
        connection.commit()

    def _copy_prod_to_ods(self, connection: pyodbc.Connection, table_name: str) -> None:
        self._log(f"Đang kéo dữ liệu {table_name} từ Prod -> ODS bằng ODBC Bulk Copy...")

        # 1. Kết nối Production (Chỉ được SELECT)
        prod_conn_str = self.connection_strings[self.prod_env_key]
        prod_conn = pyodbc.connect(prod_conn_str, autocommit=True)
        prod_cursor = prod_conn.cursor()

        try:
            # 2. Truy vấn dữ liệu gốc
            query = f"SELECT * FROM dbo.[{table_name}] WITH (NOLOCK)"
            prod_cursor.execute(query)

            # Lấy danh sách cột để sinh câu lệnh INSERT động
            columns = [column[0] for column in prod_cursor.description]
            col_names_str = ", ".join([f"[{c}]" for c in columns])
            placeholders = ", ".join(["?"] * len(columns))
            insert_sql = f"INSERT INTO [{self.facility_schema}].[{table_name}] ({col_names_str}) VALUES ({placeholders})"

            # 3. Chuẩn bị Cursor cho Staging với fast_executemany
            stg_cursor = connection.cursor()
            # Hotfix MemoryError: vô hiệu hóa fast_executemany với bảng có cột VARCHAR/NVARCHAR(MAX).
            stg_cursor.fast_executemany = False

            # 4. Đẩy dữ liệu theo lô (Chunking) để không tràn RAM
            chunk_size = 1000
            total_rows = 0

            while True:
                rows = prod_cursor.fetchmany(chunk_size)
                if not rows:
                    break

                # Chuyển đổi pyodbc.Row thành tuple để executemany có thể xử lý
                data_chunk = [tuple(row) for row in rows]
                stg_cursor.executemany(insert_sql, data_chunk)
                connection.commit()

                total_rows += len(data_chunk)
                self._log(f"Đã copy {total_rows} dòng vào ODS...")

            self._log(f"[SUCCESS] Hoàn tất kéo {total_rows} dòng cho {table_name}.")
        finally:
            prod_cursor.close()
            prod_conn.close()

    def _render_merge_sql(self, merge_sql_path: str) -> str:
        template = Path(merge_sql_path).read_text(encoding="utf-8")
        return template.format(
            dm_schema="dm",
            staging_schema=self.facility_schema,
            nguon_dulieu_key=self.nguon_dulieu_key,
            ma_co_so=self.facility_code,
            co_so_key=self.co_so_key,
        )

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

    def _execute_core(self, connection: pyodbc.Connection, *args: Any, **kwargs: Any) -> None:
        _ = args
        _ = kwargs
        for spec in self.dimension_specs:
            self._execute_dimension_spec(connection, spec)
