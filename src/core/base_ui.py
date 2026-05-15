from __future__ import annotations

import asyncio
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable

import pyodbc
from dotenv import load_dotenv
from nicegui import run, ui


class BaseUI:
    ENV_PATH = Path("config/.env")
    _env_loaded = False
    _shared_semaphore: asyncio.Semaphore | None = None
    _max_concurrent_connections = 5

    def __init__(self, page_title: str, navigation_items: list[tuple[str, str]] | None = None) -> None:
        self._ensure_environment_loaded()
        self.page_title = page_title
        self.navigation_items = navigation_items or []
        if BaseUI._shared_semaphore is None:
            BaseUI._shared_semaphore = asyncio.Semaphore(BaseUI._max_concurrent_connections)

    @classmethod
    def _ensure_environment_loaded(cls) -> None:
        if cls._env_loaded:
            return
        load_dotenv(dotenv_path=cls.ENV_PATH, override=False)
        cls._max_concurrent_connections = cls._parse_int(
            os.getenv("MAX_CONCURRENT_CONNECTIONS"),
            default=5,
        )
        cls._env_loaded = True

    @staticmethod
    def _parse_int(value: str | None, default: int) -> int:
        try:
            parsed = int((value or "").strip())
            return parsed if parsed > 0 else default
        except (TypeError, ValueError):
            return default

    def build_layout(self, active_route: str) -> None:
        with ui.header().classes("items-center justify-between"):
            ui.label(self.page_title).classes("text-lg font-semibold")

        with ui.left_drawer(value=True).classes("bg-slate-50"):
            ui.label("Điều hướng Dashboard").classes("text-sm text-slate-700 font-medium")
            for route, label in self.navigation_items:
                style = "text-primary font-semibold" if route == active_route else ""
                ui.link(label, route).classes(f"block py-1 {style}")

    def get_env(self, key: str, default: str = "") -> str:
        return os.getenv(key, default)

    def get_production_connection_vars(self) -> list[str]:
        keys = [key for key in os.environ if key.startswith("PROD_CONNECTION_")]
        return sorted(keys)

    def get_staging_schemas(self) -> list[str]:
        raw = self.get_env("STAGING_SCHEMAS", "hanoi_hisnano_v2")
        schemas = [item.strip() for item in raw.split(",") if item.strip()]
        return schemas or ["hanoi_hisnano_v2"]

    @contextmanager
    def get_db_context(self, connection_string_var: str) -> Iterable[pyodbc.Connection]:
        connection_string = self.get_env(connection_string_var).strip()
        if not connection_string:
            raise ValueError(f"Thiếu cấu hình kết nối: {connection_string_var}")

        connection = pyodbc.connect(connection_string, autocommit=False)
        try:
            yield connection
        finally:
            connection.close()

    @staticmethod
    def _prepend_nocount(sql_text: str) -> str:
        normalized = sql_text.lstrip().upper()
        if normalized.startswith("SET NOCOUNT ON;"):
            return sql_text
        return f"SET NOCOUNT ON;\n{sql_text}"

    def _query_sync(
        self,
        connection_string_var: str,
        sql_text: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[dict[str, Any]]:
        safe_sql = self._prepend_nocount(sql_text)
        with self.get_db_context(connection_string_var) as connection:
            cursor = connection.cursor()
            cursor.execute(safe_sql, params or ())
            if cursor.description is None:
                connection.commit()
                return []

            columns = [item[0] for item in cursor.description]
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]

    async def execute_query_async(
        self,
        connection_string_var: str,
        sql_text: str,
        params: tuple[Any, ...] | None = None,
    ) -> list[dict[str, Any]]:
        if BaseUI._shared_semaphore is None:
            BaseUI._shared_semaphore = asyncio.Semaphore(BaseUI._max_concurrent_connections)
        async with BaseUI._shared_semaphore:
            return await run.io_bound(self._query_sync, connection_string_var, sql_text, params)

    def read_sql_template(self, sql_path: str | Path) -> str:
        path_obj = Path(sql_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"Không tìm thấy SQL template: {path_obj}")
        return path_obj.read_text(encoding="utf-8")
