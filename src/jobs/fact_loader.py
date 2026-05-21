from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import pyodbc
import yaml

from src.core.base_extractor import BaseExtractor, ExtractPlan
from src.core.base_loader import BaseLoader


@dataclass(frozen=True)
class FactTableSpec:
    table_name: str
    key_columns: tuple[str, ...]
    date_column: str
    merge_script: str
    lookback_days: int
    selected_columns: tuple[str, ...]


class FactLoader(BaseLoader):
    LANDING_SCHEMA = "stg_nano_v2"

    TABLE_KEY_COLUMNS: dict[str, tuple[str, ...]] = {
        "ThuPhiDichVu": ("MaHoSo", "MaChiTieu", "MaPhieuDichVu"),
        "ThuPhiBaoHiem": ("MaHoSo", "MaChiTieu", "MaPhieuDichVu"),
        "ThuPhiTangGiam": ("MaHoSo", "MaChiTieu", "MaPhieuDichVu"),
        "ThuPhiGoi": ("MaHoSo", "MaPhieuThu"),
        "DoThiLuc": ("MaHoSo", "NgayDo"),
        "HoSoKhamBenhNgoaiTru": ("MaHoSo",),
    }

    def __init__(
        self,
        datamart_connection: str,
        production_connection: str,
        facility_code: str,
        facility_schema: str,
        nguon_dulieu_key: int,
        co_so_key: int,
        tables_config_path: str = "config/tables.yaml",
        batch_size: int = 10000,
        target_table_name: str | None = None,
    ) -> None:
        super().__init__(connection_string=datamart_connection, table_name=f"FactLoader:{facility_code}")
        self.production_connection = production_connection
        self.facility_code = facility_code
        self.facility_schema = facility_schema
        self.nguon_dulieu_key = nguon_dulieu_key
        self.co_so_key = co_so_key
        self.tables_config_path = Path(tables_config_path)
        self.batch_size = batch_size
        self.target_table_name = (target_table_name or "").strip()

        self.extractor = BaseExtractor(production_connection=production_connection)
        self.fact_specs = self._load_incremental_specs()

        if self.target_table_name:
            available_tables = {spec.table_name for spec in self.fact_specs}
            if self.target_table_name not in available_tables:
                raise ValueError(
                    f"Bảng incremental mục tiêu không hợp lệ: {self.target_table_name}. "
                    f"Danh sách hợp lệ: {sorted(available_tables)}"
                )

    def _load_incremental_specs(self) -> tuple[FactTableSpec, ...]:
        with self.tables_config_path.open("r", encoding="utf-8") as stream:
            config = yaml.safe_load(stream) or {}

        incremental_cfg = config.get("incremental_tables", {})
        specs: list[FactTableSpec] = []

        for table_name, cfg in incremental_cfg.items():
            if str(cfg.get("type", "")).strip().lower() != "fact":
                continue

            date_column = str(cfg.get("date_column", "")).strip()
            merge_script = str(cfg.get("merge_script", "")).strip()
            lookback_days = int(cfg.get("lookback_days", 0))
            selected_columns = tuple(str(x).strip() for x in cfg.get("selected_columns", []) if str(x).strip())

            key_columns = self.TABLE_KEY_COLUMNS.get(table_name)
            if not key_columns or not date_column or not merge_script or not selected_columns:
                continue

            specs.append(
                FactTableSpec(
                    table_name=table_name,
                    key_columns=key_columns,
                    date_column=date_column,
                    merge_script=merge_script,
                    lookback_days=lookback_days,
                    selected_columns=selected_columns,
                )
            )

        if not specs:
            raise ValueError("Không có cấu hình incremental fact hợp lệ trong config/tables.yaml")

        return tuple(specs)

    def _truncate_table(self, connection: pyodbc.Connection, schema_name: str, table_name: str) -> None:
        sql = f"TRUNCATE TABLE [{schema_name}].[{table_name}];"
        self._log(f"TRUNCATE {schema_name}.{table_name}")
        self.execute_sql_sync(connection, sql)

    @staticmethod
    def _build_explicit_insert_sql(schema_name: str, table_name: str, selected_columns: tuple[str, ...]) -> str:
        if not selected_columns:
            raise ValueError(f"Không có selected_columns để build INSERT cho bảng {table_name}")

        column_clause = ", ".join([f"[{column}]" for column in selected_columns])
        placeholders = ", ".join(["?"] * len(selected_columns))
        return f"INSERT INTO [{schema_name}].[{table_name}] ({column_clause}) VALUES ({placeholders});"

    @staticmethod
    def _table_has_identity(cursor: pyodbc.Cursor, schema_name: str, table_name: str) -> bool:
        object_name = f"[{schema_name}].[{table_name}]"
        cursor.execute(
            "SELECT OBJECTPROPERTY(OBJECT_ID(?), 'TableHasIdentity');",
            object_name,
        )
        result = cursor.fetchone()
        return bool(result and result[0] == 1)

    @staticmethod
    def _set_identity_insert(cursor: pyodbc.Cursor, schema_name: str, table_name: str, enabled: bool) -> None:
        switch = "ON" if enabled else "OFF"
        cursor.execute(f"SET IDENTITY_INSERT [{schema_name}].[{table_name}] {switch};")

    # Tầng 1: Global Transient Staging (PyODBC SELECT -> TRUNCATE 1 lần -> executemany theo chunk)
    def _load_to_global_staging(self, plan: ExtractPlan) -> None:
        insert_sql = self._build_explicit_insert_sql(
            schema_name=self.LANDING_SCHEMA,
            table_name=plan.table_name,
            selected_columns=plan.selected_columns,
        )

        total_rows = 0
        with pyodbc.connect(self.production_connection, autocommit=True) as production_connection:
            production_cursor = production_connection.cursor()
            production_cursor.execute(plan.select_sql)

            with self.get_db_context() as staging_connection:
                # Nguyên tắc 1: TRUNCATE chỉ chạy đúng 1 lần trước vòng lặp chunking
                self._truncate_table(staging_connection, self.LANDING_SCHEMA, plan.table_name)

                staging_cursor = staging_connection.cursor()
                staging_cursor.fast_executemany = False
                has_identity = self._table_has_identity(staging_cursor, self.LANDING_SCHEMA, plan.table_name)

                if has_identity:
                    self._log(f"Bật IDENTITY_INSERT cho {self.LANDING_SCHEMA}.{plan.table_name}")
                    self._set_identity_insert(staging_cursor, self.LANDING_SCHEMA, plan.table_name, enabled=True)

                # Nguyên tắc 2: INSERT động tường minh theo selected_columns
                try:
                    while True:
                        rows = production_cursor.fetchmany(self.batch_size)
                        if not rows:
                            break

                        staging_cursor.executemany(insert_sql, rows)
                        total_rows += len(rows)
                finally:
                    if has_identity:
                        self._set_identity_insert(staging_cursor, self.LANDING_SCHEMA, plan.table_name, enabled=False)
                        self._log(f"Tắt IDENTITY_INSERT cho {self.LANDING_SCHEMA}.{plan.table_name}")

                staging_connection.commit()

        self._log(
            f"Hoàn tất nạp Tầng 1 bằng PyODBC cho {plan.table_name}: {total_rows} dòng, chunk_size={self.batch_size}"
        )

    def _get_common_columns(
        self,
        connection: pyodbc.Connection,
        source_schema: str,
        source_table: str,
        target_schema: str,
        target_table: str,
    ) -> list[str]:
        sql = """
            SELECT s.COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS s
            INNER JOIN INFORMATION_SCHEMA.COLUMNS t
                ON s.COLUMN_NAME = t.COLUMN_NAME
               AND t.TABLE_SCHEMA = ?
               AND t.TABLE_NAME = ?
            WHERE s.TABLE_SCHEMA = ?
              AND s.TABLE_NAME = ?
            ORDER BY s.ORDINAL_POSITION;
        """
        cursor = connection.cursor()
        cursor.execute(sql, target_schema, target_table, source_schema, source_table)
        return [row[0] for row in cursor.fetchall()]

    def _build_ods_merge_sql(self, spec: FactTableSpec, common_columns: list[str], from_date: date, to_date: date) -> str:
        if not common_columns:
            raise ValueError(f"Không tìm thấy cột chung để MERGE ODS cho bảng {spec.table_name}")

        key_columns = [column for column in spec.key_columns if column in common_columns]
        if not key_columns:
            raise ValueError(f"Không đủ cột khóa cho MERGE ODS ở bảng {spec.table_name}")

        update_columns = [
            column
            for column in common_columns
            if column not in key_columns and column.lower() not in {"createdat", "created_at", "ngaytao"}
        ]

        on_clause = " AND ".join([f"Target.[{column}] = Source.[{column}]" for column in key_columns])
        update_clause = ",\n                ".join([f"Target.[{column}] = Source.[{column}]" for column in update_columns])
        insert_columns = ", ".join([f"[{column}]" for column in common_columns])
        insert_values = ", ".join([f"Source.[{column}]" for column in common_columns])

        return f"""
            MERGE [{self.facility_schema}].[{spec.table_name}] AS Target
            USING [{self.LANDING_SCHEMA}].[{spec.table_name}] AS Source
                ON {on_clause}
            WHEN MATCHED THEN
                UPDATE SET
                {update_clause}
            WHEN NOT MATCHED BY TARGET THEN
                INSERT ({insert_columns})
                VALUES ({insert_values})
            WHEN NOT MATCHED BY SOURCE
                 AND CAST(Target.[{spec.date_column}] AS DATE) >= CAST('{from_date:%Y-%m-%d}' AS DATE)
                 AND CAST(Target.[{spec.date_column}] AS DATE) <= CAST('{to_date:%Y-%m-%d}' AS DATE)
            THEN DELETE;
        """

    # Tầng 2: Facility Historical Staging (UPSERT/MERGE, không TRUNCATE)
    def _upsert_from_global_to_facility_staging(
        self,
        connection: pyodbc.Connection,
        spec: FactTableSpec,
        from_date: date,
        to_date: date,
    ) -> None:
        common_columns = self._get_common_columns(
            connection=connection,
            source_schema=self.LANDING_SCHEMA,
            source_table=spec.table_name,
            target_schema=self.facility_schema,
            target_table=spec.table_name,
        )
        merge_sql = self._build_ods_merge_sql(spec, common_columns, from_date, to_date)
        self.execute_sql_sync(connection, merge_sql)

    def _substitute_sql_template(self, sql_text: str, date_from: date, date_to: date) -> str:
        return (
            sql_text.replace("{dm_schema}", "dm")
            .replace("{staging_schema}", self.facility_schema)
            .replace("{source_schema}", self.facility_schema)
            .replace("{nguon_dulieu_key}", str(self.nguon_dulieu_key))
            .replace("{co_so_key}", str(self.co_so_key))
            .replace("{coso_key}", str(self.co_so_key))
            .replace("{ma_co_so}", self.facility_code)
            .replace("{date_from}", f"{date_from:%Y-%m-%d}")
            .replace("{date_to}", f"{date_to:%Y-%m-%d}")
        )

    # Tầng 3: Datamart dm (chỉ thực thi SQL template có sẵn)
    def _merge_to_datamart_using_template(self, connection: pyodbc.Connection, spec: FactTableSpec, date_from: date, date_to: date) -> None:
        sql_path = Path(spec.merge_script)
        template = sql_path.read_text(encoding="utf-8")
        rendered = self._substitute_sql_template(template, date_from=date_from, date_to=date_to)
        self.execute_sql_sync(connection, rendered)

    def _execute_core(self, connection: pyodbc.Connection, *args: Any, **kwargs: Any) -> None:
        _ = connection
        from_date_input = args[0] if len(args) > 0 else kwargs.get("from_date")
        to_date_input = args[1] if len(args) > 1 else kwargs.get("to_date")

        today = date.today()
        to_date = self.extractor.normalize_date(to_date_input, fallback=today)
        from_date = self.extractor.normalize_date(from_date_input, fallback=to_date)

        target_specs = self.fact_specs
        if self.target_table_name:
            # Khi chon ThuPhiDichVu tren UI, mo rong cum 3 bang doanh thu chay tuan tu
            if self.target_table_name == "ThuPhiDichVu":
                CLUSTER = {"ThuPhiBaoHiem", "ThuPhiTangGiam", "ThuPhiDichVu"}
                target_specs = tuple(
                    spec for spec in self.fact_specs
                    if spec.table_name in CLUSTER
                )
            else:
                target_specs = tuple(
                    spec for spec in self.fact_specs
                    if spec.table_name == self.target_table_name
                )


        for spec in target_specs:
            self._log(f"[STAGE-1][START] Prod -> Landing cho bảng {spec.table_name}")
            plan = self.extractor.build_extract_plan(
                table_name=spec.table_name,
                date_column=spec.date_column,
                from_date=from_date,
                to_date=to_date,
                lookback_days=spec.lookback_days,
                selected_columns=spec.selected_columns,
            )

            self._load_to_global_staging(plan)
            self._log(f"[STAGE-1][SUCCESS] Prod -> Landing hoàn tất cho bảng {spec.table_name}")

            with self.get_db_context() as merge_connection:
                self._log(f"[STAGE-2][START] Landing -> ODS cho bảng {spec.table_name}")
                self._upsert_from_global_to_facility_staging(
                    connection=merge_connection,
                    spec=spec,
                    from_date=plan.effective_from_date,
                    to_date=to_date,
                )
                self._log(f"[STAGE-2][SUCCESS] Landing -> ODS hoàn tất cho bảng {spec.table_name}")

                self._log(f"[STAGE-3][START] ODS -> Datamart cho bảng {spec.table_name}")
                self._merge_to_datamart_using_template(
                    connection=merge_connection,
                    spec=spec,
                    date_from=plan.effective_from_date,
                    date_to=to_date,
                )
                self._log(f"[STAGE-3][SUCCESS] ODS -> Datamart hoàn tất cho bảng {spec.table_name}")
                merge_connection.commit()
