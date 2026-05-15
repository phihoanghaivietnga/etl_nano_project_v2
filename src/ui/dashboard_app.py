from __future__ import annotations

import asyncio
from datetime import date
from pathlib import Path
from typing import Any

from src.core.base_ui import BaseUI


class DashboardCompareBackend(BaseUI):
    def __init__(self) -> None:
        super().__init__(page_title="", navigation_items=[])
        self.sql_root = Path("src/db/templates/sql/dashboard_doichieu")

    @staticmethod
    def _build_params(marker_count: int, from_date: date, to_date: date) -> tuple[Any, ...]:
        if marker_count == 0:
            return tuple()
        pair = (from_date, to_date)
        params: list[Any] = []
        while len(params) < marker_count:
            params.extend(pair)
        return tuple(params[:marker_count])

    @staticmethod
    def _ensure_marker_consistency(sql_list: list[str]) -> int:
        counts = {sql.count("?") for sql in sql_list}
        if len(counts) != 1:
            raise ValueError("Ba file SQL trong cùng domain phải có cùng số lượng marker '?'")
        return counts.pop()

    @staticmethod
    def _merge_numeric(total: dict[str, float], row: dict[str, Any]) -> dict[str, float]:
        for key, value in row.items():
            if isinstance(value, (int, float)) and value is not None:
                total[key] = total.get(key, 0.0) + float(value)
        return total

    async def _aggregate_production(self, production_sql: str, params: tuple[Any, ...]) -> dict[str, Any]:
        prod_vars = self.get_production_connection_vars()
        if not prod_vars:
            raise ValueError("Không tìm thấy biến kết nối nào theo mẫu PROD_CONNECTION_*")

        tasks = [
            self.execute_query_async(prod_var, production_sql, params)
            for prod_var in prod_vars
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        errors: list[str] = []
        aggregated: dict[str, float] = {}
        for prod_var, result in zip(prod_vars, results, strict=False):
            if isinstance(result, Exception):
                errors.append(f"{prod_var}: {result}")
                continue
            if result:
                self._merge_numeric(aggregated, result[0])

        return {"values": aggregated, "errors": errors}

    async def _aggregate_staging(self, staging_sql_template: str, params: tuple[Any, ...]) -> dict[str, Any]:
        staging_schemas = self.get_staging_schemas()
        tasks = [
            self.execute_query_async(
                "DATAMART_CONNECTION_STRING",
                staging_sql_template.format(staging_schema=schema),
                params,
            )
            for schema in staging_schemas
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        errors: list[str] = []
        aggregated: dict[str, float] = {}
        for schema, result in zip(staging_schemas, results, strict=False):
            if isinstance(result, Exception):
                errors.append(f"{schema}: {result}")
                continue
            if result:
                self._merge_numeric(aggregated, result[0])

        return {"values": aggregated, "errors": errors}

    async def compare_domain(self, domain_name: str, from_date: date, to_date: date) -> dict[str, Any]:
        domain_path = self.sql_root / domain_name
        production_sql = self.read_sql_template(domain_path / "production.sql")
        staging_sql = self.read_sql_template(domain_path / "staging.sql")
        datamart_sql = self.read_sql_template(domain_path / "datamart.sql")

        marker_count = self._ensure_marker_consistency([production_sql, staging_sql, datamart_sql])
        params = self._build_params(marker_count, from_date, to_date)

        prod_task = self._aggregate_production(production_sql, params)
        stg_task = self._aggregate_staging(staging_sql, params)
        dm_task = self.execute_query_async("DATAMART_CONNECTION_STRING", datamart_sql, params)

        prod_result, stg_result, dm_result = await asyncio.gather(
            prod_task,
            stg_task,
            dm_task,
            return_exceptions=True,
        )

        row: dict[str, Any] = {
            "TenBang": domain_name,
            "RowCount_Production": None,
            "RowCount_Staging": None,
            "RowCount_DataMart": None,
            "TotalRevenue_Production": None,
            "TotalRevenue_Staging": None,
            "TotalRevenue_DataMart": None,
            "Loi_Production": "",
            "Loi_Staging": "",
            "Loi_DataMart": "",
        }

        if isinstance(prod_result, Exception):
            row["Loi_Production"] = str(prod_result)
        else:
            row["RowCount_Production"] = prod_result["values"].get("RowCount")
            row["TotalRevenue_Production"] = prod_result["values"].get("TotalRevenue")
            row["Loi_Production"] = "; ".join(prod_result["errors"])

        if isinstance(stg_result, Exception):
            row["Loi_Staging"] = str(stg_result)
        else:
            row["RowCount_Staging"] = stg_result["values"].get("RowCount")
            row["TotalRevenue_Staging"] = stg_result["values"].get("TotalRevenue")
            row["Loi_Staging"] = "; ".join(stg_result["errors"])

        if isinstance(dm_result, Exception):
            row["Loi_DataMart"] = str(dm_result)
        elif dm_result:
            dm_row = dm_result[0]
            row["RowCount_DataMart"] = dm_row.get("RowCount")
            row["TotalRevenue_DataMart"] = dm_row.get("TotalRevenue")

        return row

    async def compare_all(self, from_date: date, to_date: date) -> list[dict[str, Any]]:
        domains = ["dim_luot_kham", "fact_thu_phi_dich_vu"]
        tasks = [self.compare_domain(domain, from_date, to_date) for domain in domains]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        rows: list[dict[str, Any]] = []
        for domain, result in zip(domains, results, strict=False):
            if isinstance(result, Exception):
                rows.append(
                    {
                        "TenBang": domain,
                        "RowCount_Production": None,
                        "RowCount_Staging": None,
                        "RowCount_DataMart": None,
                        "TotalRevenue_Production": None,
                        "TotalRevenue_Staging": None,
                        "TotalRevenue_DataMart": None,
                        "Loi_Production": str(result),
                        "Loi_Staging": "",
                        "Loi_DataMart": "",
                    }
                )
            else:
                rows.append(result)
        return rows
