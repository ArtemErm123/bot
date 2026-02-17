from __future__ import annotations

from threading import Lock

from app.models.report import Report


class ReportStore:
    def __init__(self) -> None:
        self._reports: dict[str, Report] = {}
        self._lock = Lock()

    def create(self, report: Report) -> Report:
        with self._lock:
            self._reports[report.id] = report
        return report

    def get(self, report_id: str) -> Report | None:
        with self._lock:
            return self._reports.get(report_id)

    def update(self, report: Report) -> Report:
        with self._lock:
            self._reports[report.id] = report
        return report
