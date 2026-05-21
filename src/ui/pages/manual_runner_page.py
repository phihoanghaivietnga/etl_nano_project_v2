from __future__ import annotations

import asyncio
from datetime import date, datetime
from pathlib import Path
from typing import Any

from nicegui import run, ui
import yaml

from src.core.base_ui import BaseUI
from src.jobs.dimension_loader import DimensionLoader
from src.jobs.fact_loader import FactLoader
from src.ui.pages.common import JobHistoryRecord, JobHistoryStore, NAV_ITEMS


class ManualRunnerPage(BaseUI):
    # Cụm bảng doanh thu 3-in-1: ThuPhiDichVu đóng vai trò key kích hoạt,
    # ThuPhiBaoHiem và ThuPhiTangGiam được chạy ngầm theo sau.
    _THUPHI_CLUSTER_HIDDEN_KEYS: frozenset[str] = frozenset({"ThuPhiBaoHiem", "ThuPhiTangGiam"})

    def __init__(self) -> None:
        super().__init__(page_title="Dashboard ETL - Chạy Job thủ công", navigation_items=NAV_ITEMS)
        self.from_date = date.today().replace(day=1)
        self.to_date = date.today()
        self.tables_config_path = Path("config/tables.yaml")
        self.tables_config = self._load_tables_config()
        self.incremental_table_names = self._load_incremental_table_names()
        self.full_load_dimension_names = self._load_dimension_names()
        self.manual_table_options = self._build_manual_table_options()
        self.selected_table = self.manual_table_options[0] if self.manual_table_options else ""
        self.log_queue: asyncio.Queue[str] = asyncio.Queue()
        self.log_panel: ui.log | None = None
        self.run_button: ui.button | None = None

    def _load_tables_config(self) -> dict[str, Any]:
        if not self.tables_config_path.exists():
            raise FileNotFoundError(f"Không tìm thấy file cấu hình: {self.tables_config_path}")
        with self.tables_config_path.open("r", encoding="utf-8") as stream:
            return yaml.safe_load(stream) or {}

    def _load_incremental_table_names(self) -> list[str]:
        incremental_cfg = self.tables_config.get("incremental_tables", {})
        return [str(table_name).strip() for table_name in incremental_cfg.keys() if str(table_name).strip()]

    @staticmethod
    def _load_dimension_names() -> list[str]:
        return [spec.dimension_name for spec in DimensionLoader.DEFAULT_DIMENSION_SPECS]

    def _build_manual_table_options(self) -> list[str]:
        ordered: list[str] = []
        for table_name in self.incremental_table_names + self.full_load_dimension_names:
            if table_name and table_name not in ordered:
                # Loại trừ 2 bảng thuộc cụm 3-in-1 khỏi combobox,
                # chúng sẽ được FactLoader xử lý tự động khi chọn ThuPhiDichVu.
                if table_name in self._THUPHI_CLUSTER_HIDDEN_KEYS:
                    continue
                ordered.append(table_name)
        return ordered

    def _resolve_active_facility_code(self) -> str:
        etl_settings = self.tables_config.get("etl_settings", {})
        active_facilities = etl_settings.get("active_facilities", [])
        if active_facilities:
            return str(active_facilities[0]).strip().lower()

        facilities_cfg = self.tables_config.get("facilities", {})
        if facilities_cfg:
            return str(next(iter(facilities_cfg.keys()))).strip().lower()

        raise ValueError("Không tìm thấy facility trong config/tables.yaml")

    def _resolve_facility_runtime(self) -> tuple[str, str, int, int, str]:
        facility_code = self._resolve_active_facility_code()
        facilities_cfg = self.tables_config.get("facilities", {})
        facility_cfg = facilities_cfg.get(facility_code, {})
        if not facility_cfg:
            raise ValueError(f"Không tìm thấy cấu hình facility '{facility_code}'")

        facility_schema = str(facility_cfg.get("staging_schema", "")).strip()
        if not facility_schema:
            raise ValueError(f"Thiếu staging_schema cho facility '{facility_code}'")

        nguon_dulieu_key = int(facility_cfg.get("nguon_dulieu_key", -1))
        co_so_key = int(facility_cfg.get("co_so_key", -1))

        production_env_key = f"PROD_CONNECTION_{facility_code.upper()}"
        production_connection = self.get_env(production_env_key)
        if not production_connection:
            raise ValueError(f"Thiếu biến môi trường {production_env_key}")

        return facility_code, facility_schema, nguon_dulieu_key, co_so_key, production_connection

    @staticmethod
    def _to_native_date(value: Any) -> date:
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            if "-" in value:
                return datetime.strptime(value, "%Y-%m-%d").date()
            return datetime.strptime(value, "%Y%m%d").date()
        raise ValueError(f"Không parse được ngày: {value}")

    async def _consume_log_queue(self) -> None:
        while True:
            message = await self.log_queue.get()
            if self.log_panel is not None:
                self.log_panel.push(message)
            if message == "[DONE]":
                break

    def _on_from_date_change(self, value: Any) -> None:
        self.from_date = self._to_native_date(value)

    def _on_to_date_change(self, value: Any) -> None:
        self.to_date = self._to_native_date(value)

    async def run_job(self) -> None:
        loop = asyncio.get_running_loop()
        if self.run_button is not None:
            self.run_button.disable()

        datamart_connection = self.get_env("DATAMART_CONNECTION_STRING")
        if not datamart_connection:
            ui.notify("Thiếu DATAMART_CONNECTION_STRING, chưa thể chạy job", color="negative")
            if self.run_button is not None:
                self.run_button.enable()
            return

        self.log_queue = asyncio.Queue()
        consumer_task = asyncio.create_task(self._consume_log_queue())
        from_date_native = self._to_native_date(self.from_date)
        to_date_native = self._to_native_date(self.to_date)
        done_emitted = False

        try:
            facility_code, facility_schema, nguon_dulieu_key, co_so_key, production_connection = self._resolve_facility_runtime()

            if self.selected_table in self.incremental_table_names:
                loader = FactLoader(
                    datamart_connection=datamart_connection,
                    production_connection=production_connection,
                    facility_code=facility_code,
                    facility_schema=facility_schema,
                    nguon_dulieu_key=nguon_dulieu_key,
                    co_so_key=co_so_key,
                    tables_config_path=str(self.tables_config_path),
                    target_table_name=self.selected_table,
                )
                await run.io_bound(
                    loader.execute_load,
                    from_date_native,
                    to_date_native,
                    queue=self.log_queue,
                    loop=loop,
                )
                done_emitted = True
            elif self.selected_table in self.full_load_dimension_names:
                loader = DimensionLoader(
                    datamart_connection=datamart_connection,
                    production_connection=production_connection,
                    facility_code=facility_code,
                    facility_schema=facility_schema,
                    nguon_dulieu_key=nguon_dulieu_key,
                    co_so_key=co_so_key,
                    target_dimension_name=self.selected_table,
                )
                await run.io_bound(
                    loader.execute_load,
                    queue=self.log_queue,
                    loop=loop,
                )
                done_emitted = True
            else:
                raise ValueError(f"Bảng/Danh mục không hợp lệ trong cấu hình Manual Runner: {self.selected_table}")

            await consumer_task
            JobHistoryStore.add_record(
                JobHistoryRecord(
                    thoi_gian=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ten_bang=self.selected_table,
                    tu_ngay=from_date_native.strftime("%Y%m%d"),
                    den_ngay=to_date_native.strftime("%Y%m%d"),
                    trang_thai="Success",
                    chi_tiet="Job hoàn tất và commit thành công",
                )
            )
            ui.notify("Run Job thành công", color="positive")
        except Exception as exc:
            if not done_emitted:
                self.log_queue.put_nowait("[DONE]")
            await consumer_task
            JobHistoryStore.add_record(
                JobHistoryRecord(
                    thoi_gian=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ten_bang=self.selected_table,
                    tu_ngay=from_date_native.strftime("%Y%m%d"),
                    den_ngay=to_date_native.strftime("%Y%m%d"),
                    trang_thai="Failed",
                    chi_tiet=str(exc),
                )
            )
            ui.notify(f"Run Job thất bại: {exc}", color="negative")
        finally:
            if self.run_button is not None:
                self.run_button.enable()

    def render(self) -> None:
        self.build_layout(active_route="/manual-runner")
        with ui.column().classes("w-full p-4 gap-4"):
            ui.label("Màn hình 2 - Chạy Job ETL thủ công").classes("text-xl font-semibold")
            with ui.row().classes("items-end gap-4"):
                ui.select(
                    self.manual_table_options,
                    value=self.selected_table,
                    on_change=lambda e: setattr(self, "selected_table", e.value),
                    label="Chọn bảng lõi",
                )
                ui.date(value=self.from_date.isoformat(), on_change=lambda e: self._on_from_date_change(e.value)).props(
                    "label=Từ ngày"
                )
                ui.date(value=self.to_date.isoformat(), on_change=lambda e: self._on_to_date_change(e.value)).props(
                    "label=Đến ngày"
                )
                self.run_button = ui.button("Run Job", on_click=self.run_job, color="primary")
            self.log_panel = ui.log().classes("w-full h-72 bg-black text-green-400")


@ui.page("/manual-runner")
def manual_runner_route() -> None:
    page = ManualRunnerPage()
    page.render()