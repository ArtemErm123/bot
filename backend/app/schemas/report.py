from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.models.report import ReportFormat, ReportKind, ReportStatus


class GenerateReportRequest(BaseModel):
    kind: ReportKind
    format: ReportFormat
    payload: dict[str, Any] = Field(default_factory=dict)


class GenerateReportResponse(BaseModel):
    report_id: str
    status: ReportStatus


class ReportStatusResponse(BaseModel):
    report_id: str
    status: ReportStatus
    artifact_url: str | None
    file_path: str | None
    metadata: dict[str, Any]
    error: str | None
    created_at: datetime
    updated_at: datetime
