from __future__ import annotations

import os

from dotenv import load_dotenv
from nicegui import app, ui

from src.ui.pages import bao_cao_page, doi_chieu_page, job_history_page, manual_runner_page


load_dotenv("config/.env", override=False)


@app.get("/api/health")
def api_health() -> dict[str, str]:
    return {
        "name": "ETL Nano V2 API",
        "version": "1.0.0",
        "status": "running",
    }


@ui.page("/")
def index_page() -> None:
    ui.navigate.to("/doi-chieu")


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(
        title="ETL Dashboard Đối chiếu V2",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("UI_PORT", "9005")),
        reload=False,
    )
