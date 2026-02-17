from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.models.report import Report, ReportFormat, ReportKind, ReportStatus
from app.services.connector_service import ConnectorService
from app.storage.report_store import ReportStore


class ReportService:
    def __init__(self, store: ReportStore, connector_service: ConnectorService, artifacts_dir: Path):
        self.store = store
        self.connector_service = connector_service
        self.artifacts_dir = artifacts_dir
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def create_report(self, kind: ReportKind, format_: ReportFormat) -> Report:
        report = Report(id=str(uuid.uuid4()), kind=kind, format=format_)
        return self.store.create(report)

    def process_report(self, report_id: str, payload: dict[str, Any]) -> Report:
        report = self._get_or_raise(report_id)
        report.status = ReportStatus.IN_PROGRESS
        report.generation_metadata["started_at"] = datetime.now(timezone.utc).isoformat()
        report.touch()
        self.store.update(report)

        try:
            source_data = self.connector_service.get_data(payload)
            artifact_path = self._render_artifact(report=report, data=source_data)

            report.status = ReportStatus.COMPLETED
            report.file_path = str(artifact_path)
            report.generation_metadata.update(
                {
                    "finished_at": datetime.now(timezone.utc).isoformat(),
                    "records_count": len(source_data.get("records", [])),
                    "connector_endpoint": source_data.get("endpoint"),
                    "output_format": report.format.value,
                    "report_kind": report.kind.value,
                }
            )
            report.touch()
            return self.store.update(report)
        except Exception as exc:  # noqa: BLE001
            report.status = ReportStatus.FAILED
            report.error = str(exc)
            report.generation_metadata["failed_at"] = datetime.now(timezone.utc).isoformat()
            report.touch()
            return self.store.update(report)

    def get_report(self, report_id: str) -> Report:
        return self._get_or_raise(report_id)

    def _render_artifact(self, report: Report, data: dict[str, Any]) -> Path:
        extension = report.format.value
        artifact = self.artifacts_dir / f"{report.id}.{extension}"

        content = [
            f"Report ID: {report.id}",
            f"Kind: {report.kind.value}",
            f"Format: {report.format.value}",
            f"Generated at: {datetime.now(timezone.utc).isoformat()}",
            f"Source endpoint: {data.get('endpoint')}",
            f"Records: {data.get('records')}",
        ]
        artifact.write_text("\n".join(content), encoding="utf-8")
        return artifact

    def _get_or_raise(self, report_id: str) -> Report:
        report = self.store.get(report_id)
        if report is None:
            raise KeyError(f"Report {report_id} not found")
        return report
