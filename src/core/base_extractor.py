from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta

import pyodbc


@dataclass(frozen=True)
class ExtractPlan:
    table_name: str
    date_column: str
    effective_from_date: date
    to_date: date
    select_sql: str
    selected_columns: tuple[str, ...]


class BaseExtractor:
    """
    Lớp nền chỉ chịu trách nhiệm EXTRACT.
    Không chứa logic TRUNCATE/BCP IN/MERGE.
    """

    def __init__(self, production_connection: str) -> None:
        self.production_connection = production_connection

    @staticmethod
    def normalize_date(value: object | None, fallback: date) -> date:
        if value is None:
            return fallback
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            return datetime.strptime(value, "%Y-%m-%d").date()
        raise ValueError(f"Không parse được ngày: {value}")

    @staticmethod
    def compute_effective_from_date(from_date: date, lookback_days: int) -> date:
        if lookback_days < 0:
            raise ValueError("lookback_days phải >= 0")
        return from_date - timedelta(days=lookback_days)

    def build_dynamic_select_columns(
        self,
        connection: pyodbc.Connection,
        table_name: str,
        exclude_datatypes: list[str] | tuple[str, ...] | None,
    ) -> list[str]:
        excluded = {dtype.strip().lower() for dtype in (exclude_datatypes or []) if str(dtype).strip()}

        sql = """
            SELECT COLUMN_NAME, DATA_TYPE
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'dbo'
              AND TABLE_NAME = ?
            ORDER BY ORDINAL_POSITION;
        """
        cursor = connection.cursor()
        cursor.execute(sql, table_name)

        selected: list[str] = []
        for row in cursor.fetchall():
            column_name = str(row[0])
            data_type = str(row[1]).lower()
            if data_type in excluded:
                continue
            selected.append(column_name)

        if not selected:
            raise ValueError(f"Không còn cột hợp lệ sau khi exclude_datatypes cho bảng {table_name}")

        return selected

    @staticmethod
    def build_select_sql(table_name: str, date_column: str, columns: list[str], from_date: date, to_date: date) -> str:
        projected = ", ".join([f"[{col}]" for col in columns])
        return (
            f"SELECT {projected} FROM dbo.[{table_name}] WITH (NOLOCK) "
            f"WHERE CAST([{date_column}] AS DATE) >= '{from_date:%Y-%m-%d}' "
            f"AND CAST([{date_column}] AS DATE) <= '{to_date:%Y-%m-%d}'"
        )

    def build_extract_plan(
        self,
        connection: pyodbc.Connection,
        table_name: str,
        date_column: str,
        from_date: date,
        to_date: date,
        lookback_days: int,
        exclude_datatypes: list[str] | tuple[str, ...] | None,
    ) -> ExtractPlan:
        effective_from_date = self.compute_effective_from_date(from_date=from_date, lookback_days=lookback_days)
        selected_columns = self.build_dynamic_select_columns(
            connection=connection,
            table_name=table_name,
            exclude_datatypes=exclude_datatypes,
        )
        select_sql = self.build_select_sql(
            table_name=table_name,
            date_column=date_column,
            columns=selected_columns,
            from_date=effective_from_date,
            to_date=to_date,
        )
        return ExtractPlan(
            table_name=table_name,
            date_column=date_column,
            effective_from_date=effective_from_date,
            to_date=to_date,
            select_sql=select_sql,
            selected_columns=tuple(selected_columns),
        )
