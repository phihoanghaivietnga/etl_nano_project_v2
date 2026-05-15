from __future__ import annotations

import os

from dotenv import load_dotenv
from nicegui import ui

from src.ui.pages import register_all_pages


load_dotenv("config/.env", override=False)
register_all_pages()


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="ETL Dashboard Đối chiếu V2",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", "9001")),
        reload=False,
    )
