from __future__ import annotations

import os
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import pyodbc

from src.core.base_loader import BaseLoader


@dataclass(frozen=True)
class DimensionTableSpec:
    name: str
    source_tables: tuple[str, ...]
    merge_sql_path: str


class DimensionLoader(BaseLoader):
    DEFAULT_DIMENSION_SPECS: tuple[DimensionTableSpec, ...] = (
        DimensionTableSpec(
            name="dim_dich_vu",
            source_tables=("DMLoaiDichVu", "DMDichVu", "DMDichVuChiTiet"),
            merge_sql_path="src/db/templates/sql/dimension/dim_dich_vu_merge.sql",
        ),
        DimensionTableSpec(
            name="dim_benh",
            source_tables=("DMBenh",),
            merge_sql_path="src/db/templates/sql/dimension/DimBenh_merge.sql",
        ),
        DimensionTableSpec(
            name="dim_benh_nhan",
            source_tables=("DMBenhNhan",),
            merge_sql_path="src/db/templates/sql/dimension/DimBenhNhan_merge.sql",
        ),
        DimensionTableSpec(
            name="dim_luot_kham",
            source_tables=("HoSoKhamBenhNgoaiTru",),
            merge_sql_path="src/db/templates/sql/fact/DimLuotKham_merge.sql",
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
        self.facility_code = facility_code
        self.facility_schema = facility_schema
        self.nguon_dulieu_key = nguon_dulieu_key
        self.co_so_key = co_so_key
        self.dimension_specs = dimension_specs or self.DEFAULT_DIMENSION_SPECS

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
        self._log(f"BCP queryout: {' '.join(command)}")
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
        self._log(f"BCP in: {' '.join(command)}")
        subprocess.run(command, check=True, shell=False)

    def _truncate_table(self, connection: pyodbc.Connection, schema_name: str, table_name: str) -> None:
        sql = f"TRUNCATE TABLE [{schema_name}].[{table_name}];"
        self._log(f"TRUNCATE {schema_name}.{table_name}")
        self.execute_sql_sync(connection, sql)

    def _copy_prod_to_ods(self, connection: pyodbc.Connection, table_name: str) -> None:
        prod_parts = self._parse_connection_string(self.production_connection)
        dm_parts = self._parse_connection_string(self.connection_string)

        query = f"SELECT * FROM dbo.{table_name} WITH (NOLOCK)"
        full_target_table = f"{self.facility_schema}.{table_name}"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
            temp_path = tmp_file.name

        try:
            self._run_bcp_queryout(query=query, output_file=temp_path, prod_parts=prod_parts)
            self._run_bcp_in(full_table_name=full_target_table, input_file=temp_path, dm_parts=dm_parts)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def _render_merge_sql(self, merge_sql_path: str) -> str:
        template = Path(merge_sql_path).read_text(encoding="utf-8")
        return template.format(
            dm_schema="dm",
            staging_schema=self.facility_schema,
            source_schema=self.facility_schema,
            nguon_dulieu_key=self.nguon_dulieu_key,
            ma_co_so=self.facility_code,
            co_so_key=self.co_so_key,
            date_from="1900-01-01",
            date_to="2099-12-31",
        )

    def _execute_dimension_spec(self, connection: pyodbc.Connection, spec: DimensionTableSpec) -> None:
        self._log(f"Bắt đầu FULL LOAD dimension: {spec.name}")

        for source_table in spec.source_tables:
            self._truncate_table(connection, self.facility_schema, source_table)
            self._copy_prod_to_ods(connection, source_table)

        merge_sql = self._render_merge_sql(spec.merge_sql_path)
        self._log(f"MERGE ODS -> Datamart cho {spec.name}")
        self.execute_sql_sync(connection, merge_sql)

    def _execute_core(self, connection: pyodbc.Connection, *args: Any, **kwargs: Any) -> None:
        _ = args
        _ = kwargs
        for spec in self.dimension_specs:
            self._execute_dimension_spec(connection, spec)
