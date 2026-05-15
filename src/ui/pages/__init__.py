from src.ui.pages.bao_cao_page import register_page as register_bao_cao_page
from src.ui.pages.doi_chieu_page import register_page as register_doi_chieu_page
from src.ui.pages.job_history_page import register_page as register_job_history_page
from src.ui.pages.manual_runner_page import register_page as register_manual_runner_page


def register_all_pages() -> None:
    register_doi_chieu_page()
    register_manual_runner_page()
    register_job_history_page()
    register_bao_cao_page()
