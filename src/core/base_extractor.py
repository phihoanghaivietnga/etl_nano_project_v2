from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta


@dataclass(frozen=True)
class ExtractPlan:
    table_name: str
    date_column: str
    effective_from_date: date
    to_date: date
    select_sql: str
    selected_columns: tuple[str, ...]
    projected_columns: tuple[str, ...]


class BaseExtractor:
    """
    Lớp nền chỉ chịu trách nhiệm EXTRACT.
    Không chứa logic TRUNCATE/BCP IN/MERGE.
    """

    def __init__(self, production_connection: str) -> None:
        self.production_connection = production_connection

    @staticmethod
    def _sanitize_identifier(name: str) -> str:
        clean = str(name).strip()
        if not clean:
            raise ValueError("Tên cột whitelist không được rỗng")
        return clean

    @classmethod
    def _build_whitelist_projections(cls, selected_columns: list[str] | tuple[str, ...]) -> list[str]:
        if not selected_columns:
            raise ValueError("selected_columns bắt buộc có ít nhất 1 cột")
        projections: list[str] = []
        for column in selected_columns:
            column_name = cls._sanitize_identifier(column)
            projections.append(f"[{column_name}]")
        return projections

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

    @staticmethod
    def build_select_sql(table_name: str, date_column: str, projections: list[str], from_date: date, to_date: date) -> str:
        projected = ", ".join(projections)
        return (
            f"SELECT {projected} FROM dbo.[{table_name}] WITH (NOLOCK) "
            f"WHERE CAST([{date_column}] AS DATE) >= '{from_date:%Y-%m-%d}' "
            f"AND CAST([{date_column}] AS DATE) <= '{to_date:%Y-%m-%d}'"
        )

    def build_extract_plan(
        self,
        table_name: str,
        date_column: str,
        from_date: date,
        to_date: date,
        lookback_days: int,
        selected_columns: list[str] | tuple[str, ...],
    ) -> ExtractPlan:
        effective_from_date = self.compute_effective_from_date(from_date=from_date, lookback_days=lookback_days)
        physical_columns = [self._sanitize_identifier(column) for column in selected_columns]

        if not physical_columns:
            raise ValueError(f"selected_columns rỗng cho bảng {table_name}")

        select_projections = self._build_whitelist_projections(selected_columns)
        final_projections = [*select_projections]
        final_columns = [*physical_columns]

        if len(final_columns) != len(final_projections):
            raise ValueError(
                f"Lệch schema projection cho bảng {table_name}: "
                f"physical_columns={len(final_columns)} != select_projections={len(final_projections)}"
            )

        select_sql = self.build_select_sql(
            table_name=table_name,
            date_column=date_column,
            projections=final_projections,
            from_date=effective_from_date,
            to_date=to_date,
        )
        return ExtractPlan(
            table_name=table_name,
            date_column=date_column,
            effective_from_date=effective_from_date,
            to_date=to_date,
            select_sql=select_sql,
            selected_columns=tuple(final_columns),
            projected_columns=tuple(final_projections),
        )
