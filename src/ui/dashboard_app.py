from __future__ import annotations

import asyncio
from decimal import Decimal
from datetime import date
from pathlib import Path
import traceback
from typing import Any

from src.core.base_ui import BaseUI


class DashboardCompareBackend(BaseUI):
    ORDERED_DOMAINS = [
        "dim_benh_nhan",
        "dim_benh",
        "dim_dich_vu",
        "dim_loai_goi_dich_vu",
        "dim_luot_kham",
        "fact_thu_phi_dich_vu",
    ]

    DOMAIN_TITLES = {
        "dim_benh_nhan": "BẢNG ĐỐI CHIẾU BỆNH NHÂN",
        "dim_benh": "BẢNG ĐỐI CHIẾU BỆNH",
        "dim_dich_vu": "BẢNG ĐỐI CHIẾU DỊCH VỤ",
        "dim_loai_goi_dich_vu": "BẢNG ĐỐI CHIẾU LOẠI GÓI DỊCH VỤ",
        "dim_luot_kham": "BẢNG ĐỐI CHIẾU LƯỢT KHÁM",
        "fact_thu_phi_dich_vu": "BẢNG ĐỐI CHIẾU DOANH THU",
    }

    FACT_REQUIRED_METRICS = ["RowCount", "TongTien", "TongTienSauTangGiam"]

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
            if value is None:
                total[key] = total.get(key, 0.0)
                continue
            if isinstance(value, (int, float, Decimal)):
                total[key] = total.get(key, 0.0) + float(value)
        return total

    @staticmethod
    def _normalize_metric_map(values: dict[str, Any]) -> dict[str, float]:
        normalized: dict[str, float] = {}
        for key, value in values.items():
            if value is None:
                normalized[key] = 0.0
            elif isinstance(value, (int, float, Decimal)):
                normalized[key] = float(value)
        return normalized

    @classmethod
    def _resolve_metrics(cls, domain_name: str, source_maps: list[dict[str, float]]) -> list[str]:
        metrics: list[str] = []
        for source_map in source_maps:
            for key in source_map:
                if key not in metrics:
                    metrics.append(key)

        if domain_name == "fact_thu_phi_dich_vu":
            for metric in cls.FACT_REQUIRED_METRICS:
                if metric not in metrics:
                    metrics.append(metric)
        else:
            metrics = ["RowCount"]

        return metrics

    @staticmethod
    def _build_rows_by_source(
        metrics: list[str],
        production_values: dict[str, float],
        staging_values: dict[str, float],
        datamart_values: dict[str, float],
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        source_items = [
            ("Production", production_values),
            ("Staging", staging_values),
            ("DataMart", datamart_values),
        ]
        for source_name, source_values in source_items:
            row: dict[str, Any] = {"Nguon": source_name}
            for metric in metrics:
                row[metric] = source_values.get(metric, 0.0)
            rows.append(row)
        return rows

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
                try:
                    raise result
                except Exception:
                    traceback.print_exc()
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
                try:
                    raise result
                except Exception:
                    traceback.print_exc()
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

        production_values: dict[str, float] = {}
        staging_values: dict[str, float] = {}
        datamart_values: dict[str, float] = {}
        errors: dict[str, str] = {"Production": "", "Staging": "", "DataMart": ""}

        if isinstance(prod_result, Exception):
            try:
                raise prod_result
            except Exception:
                traceback.print_exc()
            errors["Production"] = str(prod_result)
        else:
            production_values = self._normalize_metric_map(prod_result.get("values", {}))
            errors["Production"] = "; ".join(prod_result.get("errors", []))

        if isinstance(stg_result, Exception):
            try:
                raise stg_result
            except Exception:
                traceback.print_exc()
            errors["Staging"] = str(stg_result)
        else:
            staging_values = self._normalize_metric_map(stg_result.get("values", {}))
            errors["Staging"] = "; ".join(stg_result.get("errors", []))

        if isinstance(dm_result, Exception):
            try:
                raise dm_result
            except Exception:
                traceback.print_exc()
            errors["DataMart"] = str(dm_result)
        else:
            dm_data = dm_result[0] if dm_result else {}
            datamart_values = self._normalize_metric_map(dm_data)

        metrics = self._resolve_metrics(
            domain_name,
            [production_values, staging_values, datamart_values],
        )
        rows = self._build_rows_by_source(metrics, production_values, staging_values, datamart_values)
        columns = ["Nguon", *metrics]

        return {
            "domain": domain_name,
            "title": self.DOMAIN_TITLES.get(domain_name, domain_name.upper()),
            "columns": columns,
            "rows": rows,
            "errors": errors,
        }

    async def compare_all(self, from_date: date, to_date: date) -> list[dict[str, Any]]:
        domains = self.ORDERED_DOMAINS
        tasks = [self.compare_domain(domain, from_date, to_date) for domain in domains]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        rows: list[dict[str, Any]] = []
        for domain, result in zip(domains, results, strict=False):
            if isinstance(result, Exception):
                try:
                    raise result
                except Exception:
                    traceback.print_exc()
                rows.append(
                    {
                        "domain": domain,
                        "title": self.DOMAIN_TITLES.get(domain, domain.upper()),
                        "columns": ["Nguon", "RowCount"],
                        "rows": [
                            {"Nguon": "Production", "RowCount": 0.0},
                            {"Nguon": "Staging", "RowCount": 0.0},
                            {"Nguon": "DataMart", "RowCount": 0.0},
                        ],
                        "errors": {"Production": str(result), "Staging": "", "DataMart": ""},
                    }
                )
            else:
                rows.append(result)
        return rows
