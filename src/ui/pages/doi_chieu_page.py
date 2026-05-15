from __future__ import annotations

from datetime import date, datetime
from typing import Any

from nicegui import ui

from src.core.base_ui import BaseUI
from src.ui.dashboard_app import DashboardCompareBackend
from src.ui.pages.common import NAV_ITEMS


class DoiChieuPage(BaseUI):
    def __init__(self) -> None:
        super().__init__(page_title="Dashboard ETL - Đối chiếu kết quả", navigation_items=NAV_ITEMS)
        self.from_date = date.today().replace(day=1)
        self.to_date = date.today()
        self.rows: list[dict[str, Any]] = []
        self.table: ui.table | None = None
        self.backend = DashboardCompareBackend()

    @staticmethod
    def _to_native_date(value: Any) -> date:
        if isinstance(value, date):
            return value
        if isinstance(value, str):
            if "-" in value:
                return datetime.strptime(value, "%Y-%m-%d").date()
            return datetime.strptime(value, "%Y%m%d").date()
        raise ValueError(f"Không parse được ngày: {value}")

    def _on_from_date_change(self, value: Any) -> None:
        self.from_date = self._to_native_date(value)

    def _on_to_date_change(self, value: Any) -> None:
        self.to_date = self._to_native_date(value)

    async def load_data(self) -> None:
        try:
            self.rows = await self.backend.compare_all(self.from_date, self.to_date)
            if self.table is not None:
                self.table.columns = [
                    {"name": key, "label": key, "field": key, "align": "left"}
                    for key in (self.rows[0].keys() if self.rows else [])
                ]
                self.table.rows = self.rows
                self.table.update()
            ui.notify("Đã tải dữ liệu đối chiếu", color="positive")
        except Exception as exc:
            ui.notify(f"Lỗi đối chiếu: {exc}", color="negative")

    def render(self) -> None:
        self.build_layout(active_route="/doi-chieu")
        with ui.column().classes("w-full p-4 gap-4"):
            ui.label("Màn hình 1 - Đối chiếu kết quả").classes("text-xl font-semibold")
            with ui.row().classes("items-end gap-4"):
                ui.date(value=self.from_date.isoformat(), on_change=lambda e: self._on_from_date_change(e.value)).props(
                    "label=Từ ngày"
                )
                ui.date(value=self.to_date.isoformat(), on_change=lambda e: self._on_to_date_change(e.value)).props(
                    "label=Đến ngày"
                )
                ui.button("Tải dữ liệu đối chiếu", on_click=self.load_data, color="primary")

            self.table = ui.table(columns=[], rows=self.rows).classes("w-full")


@ui.page("/doi-chieu")
def doi_chieu_route() -> None:
    page = DoiChieuPage()
    page.render()
