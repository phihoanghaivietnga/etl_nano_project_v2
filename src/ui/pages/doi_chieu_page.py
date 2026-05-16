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
        self.result_container: ui.column | None = None
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

    @staticmethod
    def _build_table_columns(keys: list[str]) -> list[dict[str, Any]]:
        return [{"name": key, "label": key, "field": key, "align": "left"} for key in keys]

    def _render_domain_card(self, domain_result: dict[str, Any]) -> None:
        if self.result_container is None:
            return
        with self.result_container:
            with ui.card().classes("w-full"):
                ui.label(domain_result.get("title", "BẢNG ĐỐI CHIẾU")).classes("text-base font-semibold")
                table_columns = self._build_table_columns(domain_result.get("columns", []))
                table_rows = domain_result.get("rows", [])
                ui.table(columns=table_columns, rows=table_rows).classes("w-full")

                errors = domain_result.get("errors", {})
                for source in ["Production", "Staging", "DataMart"]:
                    error_text = (errors.get(source, "") or "").strip()
                    if error_text:
                        ui.label(f"{source}: {error_text}").classes("text-red-600 text-sm")

    async def run_compare_all(self) -> None:
        try:
            if self.result_container is not None:
                self.result_container.clear()

            results = await self.backend.compare_all(self.from_date, self.to_date)
            for domain_result in results:
                self._render_domain_card(domain_result)

            ui.notify("Đã chạy đối chiếu toàn bộ", color="positive")
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
                ui.button("Chạy đối chiếu toàn bộ", on_click=self.run_compare_all, color="primary")

            with ui.scroll_area().classes("w-full h-[70vh]"):
                self.result_container = ui.column().classes("w-full gap-4")


@ui.page("/doi-chieu")
def doi_chieu_route() -> None:
    page = DoiChieuPage()
    page.render()
