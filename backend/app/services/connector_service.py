from __future__ import annotations

import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


logger = logging.getLogger(__name__)


@dataclass
class RetryPolicy:
    max_attempts: int = 3
    backoff_seconds: float = 0.1


@dataclass
class ConnectorConfig:
    endpoint: str
    token: str
    timeout_seconds: float = 5.0
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)


class BaseConnector(ABC):
    def __init__(self, config: ConnectorConfig):
        self.config = config

    @abstractmethod
    def fetch_data(self, report_payload: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


class MockConnector(BaseConnector):
    def fetch_data(self, report_payload: dict[str, Any]) -> dict[str, Any]:
        last_error: Exception | None = None

        for attempt in range(1, self.config.retry_policy.max_attempts + 1):
            started = time.perf_counter()
            try:
                if report_payload.get("force_failure") and attempt < self.config.retry_policy.max_attempts:
                    raise RuntimeError("Synthetic connector failure")

                response = {
                    "source": "mock",
                    "endpoint": self.config.endpoint,
                    "records": report_payload.get("records", [{"id": 1, "value": 100}]),
                }

                self._log_call(
                    level="info",
                    payload=report_payload,
                    attempt=attempt,
                    duration_ms=(time.perf_counter() - started) * 1000,
                    result="success",
                )
                return response
            except Exception as exc:  # noqa: BLE001
                last_error = exc
                self._log_call(
                    level="warning",
                    payload=report_payload,
                    attempt=attempt,
                    duration_ms=(time.perf_counter() - started) * 1000,
                    result="error",
                    error=str(exc),
                )
                time.sleep(self.config.retry_policy.backoff_seconds)

        raise RuntimeError(f"Connector failed after retries: {last_error}")

    def _log_call(
        self,
        *,
        level: str,
        payload: dict[str, Any],
        attempt: int,
        duration_ms: float,
        result: str,
        error: str | None = None,
    ) -> None:
        event = {
            "event": "connector_call",
            "connector": self.__class__.__name__,
            "endpoint": self.config.endpoint,
            "timeout_seconds": self.config.timeout_seconds,
            "attempt": attempt,
            "max_attempts": self.config.retry_policy.max_attempts,
            "result": result,
            "duration_ms": round(duration_ms, 2),
            "payload_size": len(json.dumps(payload)),
            "error": error,
        }
        getattr(logger, level)(json.dumps(event, ensure_ascii=False))


class ConnectorService:
    def __init__(self, connector: BaseConnector):
        self.connector = connector

    def get_data(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.connector.fetch_data(payload)
