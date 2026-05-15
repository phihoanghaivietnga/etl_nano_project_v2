from __future__ import annotations

from nicegui import ui

from src.core.base_ui import BaseUI
from src.ui.pages.common import JobHistoryStore, NAV_ITEMS


class JobHistoryPage(BaseUI):
    def __init__(self) -> None:
        super().__init__(page_title="Dashboard ETL - Lịch sử chạy Job", navigation_items=NAV_ITEMS)

    def render(self) -> None:
        self.build_layout(active_route="/job-history")
        with ui.column().classes("w-full p-4 gap-3"):
            ui.label("Màn hình 3 - Lịch sử chạy Job").classes("text-xl font-semibold")
            with ui.card().classes("w-full"):
                with ui.column().classes("w-full gap-2"):
                    if not JobHistoryStore.records:
                        ui.label("Chưa có bản ghi lịch sử").classes("text-slate-500")
                    else:
                        for record in JobHistoryStore.records:
                            status_class = "text-green-600" if record.trang_thai == "Success" else "text-red-600"
                            with ui.row().classes("w-full justify-between border-b pb-2"):
                                ui.label(f"{record.thoi_gian} | {record.ten_bang} | {record.tu_ngay} -> {record.den_ngay}")
                                ui.label(record.trang_thai).classes(f"font-semibold {status_class}")
                            ui.label(record.chi_tiet).classes("text-xs text-slate-600")


@ui.page("/job-history")
def job_history_route() -> None:
    page = JobHistoryPage()
    page.render()
