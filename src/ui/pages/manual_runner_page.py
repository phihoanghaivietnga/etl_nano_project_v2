from __future__ import annotations

import asyncio
from datetime import date, datetime
from typing import Any

from nicegui import run, ui

from src.core.base_loader import GenericTableLoader
from src.core.base_ui import BaseUI
from src.ui.pages.common import JobHistoryRecord, JobHistoryStore, NAV_ITEMS


TABLE_MERGE_TEMPLATE: dict[str, str] = {
    "HoSoKhamBenhNgoaiTru": "src/db/templates/sql/fact/DimLuotKham_merge.sql",
    "DoThiLuc": "src/db/templates/sql/fact/FactDoThiLuc_merge.sql",
    "ThuPhiGoi": "src/db/templates/sql/fact/FactThuPhiDichVu_ThuPhiGoi_merge.sql",
}


class ManualRunnerPage(BaseUI):
    def __init__(self) -> None:
        super().__init__(page_title="Dashboard ETL - Chạy Job thủ công", navigation_items=NAV_ITEMS)
        self.from_date = date.today().replace(day=1)
        self.to_date = date.today()
        self.selected_table = "HoSoKhamBenhNgoaiTru"
        self.log_queue: asyncio.Queue[str] = asyncio.Queue()
        self.log_panel: ui.log | None = None
        self.run_button: ui.button | None = None

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

        connection_string = self.get_env("DATAMART_CONNECTION_STRING")
        merge_template = TABLE_MERGE_TEMPLATE.get(self.selected_table)
        if not connection_string:
            ui.notify("Thiếu DATAMART_CONNECTION_STRING, chưa thể chạy job", color="negative")
            if self.run_button is not None:
                self.run_button.enable()
            return

        self.log_queue = asyncio.Queue()
        consumer_task = asyncio.create_task(self._consume_log_queue())
        from_date_native = self._to_native_date(self.from_date)
        to_date_native = self._to_native_date(self.to_date)

        loader = GenericTableLoader(
            connection_string=connection_string,
            table_name=self.selected_table,
            merge_sql_path=merge_template,
        )

        try:
            await run.io_bound(
                loader.execute_load,
                from_date_native,
                to_date_native,
                queue=self.log_queue,
                loop=loop,
            )
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
                    list(TABLE_MERGE_TEMPLATE.keys()),
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


def register_page() -> None:
    @ui.page("/manual-runner")
    def page_manual_runner() -> None:
        ManualRunnerPage().render()
