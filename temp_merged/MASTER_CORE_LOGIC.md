# MASTER_CORE_LOGIC.md

## NHÓM: CORE_LOGIC

## MỤC LỤC NGUỒN
  [DESCRIPTION]: Core logic, configuration, and environment settings

### config/.env.example - Thành phần lõi và cấu hình nền tảng của hệ thống ETL
### src/core/base_loader.py - Thành phần lõi và cấu hình nền tảng của hệ thống ETL
### src/core/base_ui.py - Thành phần lõi và cấu hình nền tảng của hệ thống ETL

## NỘI DUNG GỘP

### SOURCE: config/.env.example
```text
# =============================================================================
# ETL Nano V2 - Environment Configuration Template
# =============================================================================
# Lưu ý: Đổi tên file thành .env và điền các giá trị thực
# =============================================================================

# -----------------------------------------------------------------------------
# Database Connections
# -----------------------------------------------------------------------------

# Chuỗi kết nối đến SQL Server Production (Source - Chỉ đọc)
# Sử dụng ODBC Driver 17 for SQL Server
PROD_CONNECTION_STRING=DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.100;DATABASE=HIS_NANO_V2;UID=etl_read;PWD=your_password_here;TrustServerCertificate=yes

# Chuỗi kết nối đến SQL Server Datamart (Target - Đọc/Ghi)
DATAMART_CONNECTION_STRING=DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.1.101;DATABASE=ETL_DATAMART;UID=etl_write;PWD=your_password_here;TrustServerCertificate=yes

# -----------------------------------------------------------------------------
# Database Connection Settings
# -----------------------------------------------------------------------------

# Thời gian chờ kết nối (giây)
CONNECTION_TIMEOUT=30

# Số lần thử kết nối lại khi thất bại
MAX_RETRIES=3

# Thời gian chờ giữa các lần retry (giây)
RETRY_DELAY=5

# -----------------------------------------------------------------------------
# ETL Settings
# -----------------------------------------------------------------------------

# Kích thước batch khi bulk insert (số dòng mỗi batch)
BATCH_SIZE=10000

# Số lần thử lại khi một bảng lỗi
TABLE_MAX_RETRIES=3

# Khoảng thời gian đồng bộ fact tables (phút)
FACT_SYNC_INTERVAL_MINUTES=30

# Thời gian chạy rebuild index hàng ngày (giờ:phút)
INDEX_REBUILD_TIME=02:00

# -----------------------------------------------------------------------------
# Email Alert Settings
# -----------------------------------------------------------------------------

# SMTP Server
SMTP_SERVER=smtp.company.local
SMTP_PORT=587
SMTP_USERNAME=etl@company.local
SMTP_PASSWORD=your_email_password_here

# Danh sách email nhận cảnh báo (phân cách bằng dấu phẩy)
ALERT_EMAIL_TO=operator@company.local,admin@company.local

# -----------------------------------------------------------------------------
# Logging Settings
# -----------------------------------------------------------------------------

# Thư mục lưu log
LOG_DIR=./logs

# Mức độ log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=INFO

# Số ngày lưu log
LOG_RETENTION_DAYS=90

# -----------------------------------------------------------------------------
# Application Settings
# -----------------------------------------------------------------------------

# Môi trường (development, production)
APP_ENV=development

# API Host
API_HOST=0.0.0.0

# API Port
API_PORT=9001

# API URL (duong dan day du cho UI goi toi)
API_URL=http://localhost:9001
```

### SOURCE: src/core/base_loader.py
```py
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
```

### SOURCE: src/core/base_ui.py
```py
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
```
