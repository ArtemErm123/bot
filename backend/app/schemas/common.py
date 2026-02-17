from datetime import datetime

from pydantic import BaseModel, Field


class ProblemDetails(BaseModel):
    """RFC7807-like error payload."""

    type: str = Field(example="about:blank")
    title: str = Field(example="Bad Request")
    status: int = Field(example=400)
    detail: str = Field(example="Validation failed")
    instance: str | None = Field(default=None, example="/api/v1/projects/1")
    trace_id: str | None = Field(default=None)


class AuditInfo(BaseModel):
    """Audit metadata for mutating operations."""

    changed_by: str = Field(description="Actor identifier (user id/email)")
    changed_at: datetime = Field(description="UTC timestamp of change")
    action: str = Field(description="Operation type: create/update/delete")
    resource: str = Field(description="Resource type")
    resource_id: int = Field(description="Resource identifier")
