from __future__ import annotations

import asyncio
import subprocess
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

import pyodbc


class BaseLoader:
    def __init__(
        self,
        connection_string: str,
        table_name: str,
    ) -> None:
        self.connection_string = connection_string
        self.table_name = table_name
        self._active_queue: asyncio.Queue[str] | None = None
        self._active_loop: asyncio.AbstractEventLoop | None = None

    def _log(
        self,
        message: str,
        queue: asyncio.Queue[str] | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        text = f"[{self.table_name}] {message}"
        target_queue = queue or self._active_queue
        target_loop = loop or self._active_loop
        if target_queue is not None and target_loop is not None:
            target_loop.call_soon_threadsafe(target_queue.put_nowait, text)
        else:
            print(text)

    def _emit_done(
        self,
        queue: asyncio.Queue[str] | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None:
        target_queue = queue or self._active_queue
        target_loop = loop or self._active_loop
        if target_queue is not None and target_loop is not None:
            target_loop.call_soon_threadsafe(target_queue.put_nowait, "[DONE]")

    @staticmethod
    def _prepend_nocount(sql_text: str) -> str:
        normalized = sql_text.lstrip().upper()
        if normalized.startswith("SET NOCOUNT ON;"):
            return sql_text
        return f"SET NOCOUNT ON;\n{sql_text}"

    @contextmanager
    def get_db_context(self) -> Iterable[pyodbc.Connection]:
        connection = pyodbc.connect(self.connection_string, autocommit=False)
        try:
            yield connection
        finally:
            connection.close()

    def execute_sql_sync(
        self,
        connection: pyodbc.Connection,
        sql_text: str,
        params: tuple[Any, ...] | None = None,
    ) -> None:
        safe_sql = self._prepend_nocount(sql_text)
        cursor = connection.cursor()
        cursor.execute(safe_sql, params or ())

    def run_bcp_utf16le(self, query: str, output_file: str) -> None:
        command = [
            "bcp",
            query,
            "queryout",
            output_file,
            "-w",
            "-t\t",
            "-r\n",
            "-q",
        ]
        self._log(f"Thực thi BCP UTF-16-LE: {' '.join(command)}")
        subprocess.run(command, check=True, shell=False)

    def _execute_core(self, connection: pyodbc.Connection) -> None:
        raise NotImplementedError("Loader con phải override _execute_core")

    def execute_load(
        self,
        *args: Any,
        queue: asyncio.Queue[str] | None = None,
        loop: asyncio.AbstractEventLoop | None = None,
        **kwargs: Any,
    ) -> None:
        self._active_queue = queue
        self._active_loop = loop
        self._log("Bắt đầu execute_load", queue=queue, loop=loop)
        with self.get_db_context() as connection:
            try:
                self._execute_core(connection, *args, **kwargs)
                connection.commit()
                self._log("Hoàn tất thành công, đã commit", queue=queue, loop=loop)
            except Exception as exc:
                connection.rollback()
                self._log(f"Thất bại, đã rollback toàn cục: {exc}", queue=queue, loop=loop)
                raise
            finally:
                self._emit_done(queue=queue, loop=loop)
                self._active_queue = None
                self._active_loop = None


class GenericTableLoader(BaseLoader):
    def __init__(
        self,
        connection_string: str,
        table_name: str,
        merge_sql_path: str | None = None,
        bcp_query: str | None = None,
        bcp_output_file: str | None = None,
    ) -> None:
        super().__init__(connection_string=connection_string, table_name=table_name)
        self.merge_sql_path = merge_sql_path
        self.bcp_query = bcp_query
        self.bcp_output_file = bcp_output_file

    @staticmethod
    def _resolve_date(value: Any) -> date | None:
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        return None

    @staticmethod
    def _build_incremental_params(sql_text: str, from_date: date | None, to_date: date | None) -> tuple[Any, ...]:
        marker_count = sql_text.count("?")
        if marker_count == 0:
            return tuple()
        if from_date is None or to_date is None:
            raise ValueError("Thiếu from_date hoặc to_date để bind marker '?' cho SQL incremental")

        pair = (from_date, to_date)
        params: list[Any] = []
        while len(params) < marker_count:
            params.extend(pair)
        return tuple(params[:marker_count])

    def _execute_core(self, connection: pyodbc.Connection, *args: Any, **kwargs: Any) -> None:
        from_date = self._resolve_date(args[0] if len(args) > 0 else kwargs.get("from_date"))
        to_date = self._resolve_date(args[1] if len(args) > 1 else kwargs.get("to_date"))

        if from_date and to_date:
            self._log(f"Khoảng thời gian: {from_date} -> {to_date}")
        else:
            self._log("Không có tham số ngày, chuyển sang chế độ kiểm tra cơ bản")

        if self.bcp_query and self.bcp_output_file:
            self.run_bcp_utf16le(self.bcp_query, self.bcp_output_file)

        if self.merge_sql_path:
            sql_path = Path(self.merge_sql_path)
            sql_text = sql_path.read_text(encoding="utf-8")
            params = self._build_incremental_params(sql_text, from_date, to_date)
            self._log(f"Thực thi MERGE template: {sql_path}")
            self.execute_sql_sync(connection, sql_text, params)
            return

        health_check_sql = "SELECT GETDATE() AS ThoiGianHeThong;"
        self._log("Không có template cụ thể, chạy health-check SQL")
        self.execute_sql_sync(connection, health_check_sql)
