from __future__ import annotations

from nicegui import ui

from src.core.base_ui import BaseUI
from src.ui.pages.common import NAV_ITEMS


class BaoCaoPage(BaseUI):
    def __init__(self) -> None:
        super().__init__(page_title="Dashboard ETL - Báo cáo", navigation_items=NAV_ITEMS)

    def render(self) -> None:
        self.build_layout(active_route="/bao-cao")
        with ui.column().classes("w-full p-4 gap-3"):
            ui.label("Màn hình 4 - Báo cáo").classes("text-xl font-semibold")
            with ui.card().classes("w-full h-96 bg-white"):
                ui.label("Khung trắng chuẩn bị tích hợp logic báo cáo từ V1").classes("text-slate-500")


def register_page() -> None:
    @ui.page("/bao-cao")
    def page_bao_cao() -> None:
        BaoCaoPage().render()
