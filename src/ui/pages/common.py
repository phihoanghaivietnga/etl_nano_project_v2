from __future__ import annotations

from dataclasses import dataclass


NAV_ITEMS: list[tuple[str, str]] = [
    ("/doi-chieu", "Đối chiếu kết quả"),
    ("/manual-runner", "Chạy Job ETL thủ công"),
    ("/job-history", "Lịch sử chạy Job"),
    ("/bao-cao", "Báo cáo"),
]


@dataclass
class JobHistoryRecord:
    thoi_gian: str
    ten_bang: str
    tu_ngay: str
    den_ngay: str
    trang_thai: str
    chi_tiet: str


class JobHistoryStore:
    records: list[JobHistoryRecord] = []

    @classmethod
    def add_record(cls, record: JobHistoryRecord) -> None:
        cls.records.insert(0, record)
