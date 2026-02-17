from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI

from app.api.reports import router as reports_router
from app.services.connector_service import ConnectorConfig, ConnectorService, MockConnector, RetryPolicy
from app.services.report_service import ReportService
from app.storage.report_store import ReportStore

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Reporting Backend")

connector_config = ConnectorConfig(
    endpoint="https://mock.local/api/reports",
    token="dev-token",
    timeout_seconds=3,
    retry_policy=RetryPolicy(max_attempts=3, backoff_seconds=0.05),
)
connector_service = ConnectorService(connector=MockConnector(config=connector_config))
report_store = ReportStore()
report_service = ReportService(
    store=report_store,
    connector_service=connector_service,
    artifacts_dir=Path("backend/artifacts"),
)

app.include_router(reports_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
