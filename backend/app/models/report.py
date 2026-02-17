from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class ReportStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ReportKind(str, Enum):
    SHORT = "short"
    FULL = "full"


class ReportFormat(str, Enum):
    PDF = "pdf"
    XLSX = "xlsx"


@dataclass
class Report:
    id: str
    kind: ReportKind
    format: ReportFormat
    status: ReportStatus = ReportStatus.PENDING
    file_path: str | None = None
    error: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    generation_metadata: dict[str, Any] = field(default_factory=dict)

    def touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc)
