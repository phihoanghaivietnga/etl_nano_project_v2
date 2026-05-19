from __future__ import annotations

import os
import subprocess
import tempfile
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
    exclude_datatypes: tuple[str, ...]


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
    ) -> None:
        super().__init__(connection_string=datamart_connection, table_name=f"FactLoader:{facility_code}")
        self.production_connection = production_connection
        self.facility_code = facility_code
        self.facility_schema = facility_schema
        self.nguon_dulieu_key = nguon_dulieu_key
        self.co_so_key = co_so_key
        self.tables_config_path = Path(tables_config_path)
        self.batch_size = batch_size

        self.extractor = BaseExtractor(production_connection=production_connection)
        self.fact_specs = self._load_incremental_specs()

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
            exclude_datatypes = tuple(str(x).strip() for x in cfg.get("exclude_datatypes", []) if str(x).strip())

            key_columns = self.TABLE_KEY_COLUMNS.get(table_name)
            if not key_columns or not date_column or not merge_script:
                continue

            specs.append(
                FactTableSpec(
                    table_name=table_name,
                    key_columns=key_columns,
                    date_column=date_column,
                    merge_script=merge_script,
                    lookback_days=lookback_days,
                    exclude_datatypes=exclude_datatypes,
                )
            )

        if not specs:
            raise ValueError("Không có cấu hình incremental fact hợp lệ trong config/tables.yaml")

        return tuple(specs)

    @staticmethod
    def _parse_connection_string(connection_string: str) -> dict[str, str]:
        parsed: dict[str, str] = {}
        for item in connection_string.split(";"):
            if not item or "=" not in item:
                continue
            key, value = item.split("=", 1)
            parsed[key.strip().upper()] = value.strip()
        return parsed

    @staticmethod
    def _build_bcp_auth_args(conn_parts: dict[str, str]) -> list[str]:
        if conn_parts.get("UID") and conn_parts.get("PWD"):
            return ["-U", conn_parts["UID"], "-P", conn_parts["PWD"]]
        return ["-T"]

    def _truncate_table(self, connection: pyodbc.Connection, schema_name: str, table_name: str) -> None:
        sql = f"TRUNCATE TABLE [{schema_name}].[{table_name}];"
        self._log(f"TRUNCATE {schema_name}.{table_name}")
        self.execute_sql_sync(connection, sql)
        # Giải phóng lock ngay để tiến trình BCP IN (session khác) không bị treo chờ.
        connection.commit()

    def _run_bcp_queryout(self, query: str, output_file: str, prod_parts: dict[str, str]) -> None:
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
        subprocess.run(command, check=True, shell=False)

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
        subprocess.run(command, check=True, shell=False)

    # Tầng 1: Global Transient Staging (TRUNCATE + BCP IN)
    def _load_to_global_staging(self, connection: pyodbc.Connection, plan: ExtractPlan) -> None:
        self._truncate_table(connection, self.LANDING_SCHEMA, plan.table_name)

        prod_parts = self._parse_connection_string(self.production_connection)
        dm_parts = self._parse_connection_string(self.connection_string)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            temp_path = tmp_file.name

        try:
            self._run_bcp_queryout(query=plan.select_sql, output_file=temp_path, prod_parts=prod_parts)
            self._run_bcp_in(
                full_table_name=f"{self.LANDING_SCHEMA}.{plan.table_name}",
                input_file=temp_path,
                dm_parts=dm_parts,
            )
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

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
        from_date_input = args[0] if len(args) > 0 else kwargs.get("from_date")
        to_date_input = args[1] if len(args) > 1 else kwargs.get("to_date")

        today = date.today()
        to_date = self.extractor.normalize_date(to_date_input, fallback=today)
        from_date = self.extractor.normalize_date(from_date_input, fallback=to_date)

        for spec in self.fact_specs:
            with pyodbc.connect(self.production_connection, autocommit=True) as prod_conn:
                plan = self.extractor.build_extract_plan(
                    connection=prod_conn,
                    table_name=spec.table_name,
                    date_column=spec.date_column,
                    from_date=from_date,
                    to_date=to_date,
                    lookback_days=spec.lookback_days,
                    exclude_datatypes=spec.exclude_datatypes,
                )

            self._load_to_global_staging(connection, plan)
            self._upsert_from_global_to_facility_staging(
                connection=connection,
                spec=spec,
                from_date=plan.effective_from_date,
                to_date=to_date,
            )
            self._merge_to_datamart_using_template(
                connection=connection,
                spec=spec,
                date_from=plan.effective_from_date,
                date_to=to_date,
            )
