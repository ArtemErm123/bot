from datetime import datetime, timezone

from fastapi import HTTPException, Request, status

from app.core.logging import get_audit_logger
from app.core.security import TokenPayload
from app.schemas.common import AuditInfo


def not_found(entity: str, entity_id: int) -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity} with id={entity_id} not found",
    )


def audit_log(request: Request, user: TokenPayload, action: str, resource: str, resource_id: int) -> AuditInfo:
    info = AuditInfo(
        changed_by=str(user.get("sub", "unknown")),
        changed_at=datetime.now(timezone.utc),
        action=action,
        resource=resource,
        resource_id=resource_id,
    )
    get_audit_logger().info(
        "actor=%s action=%s resource=%s resource_id=%s path=%s",
        info.changed_by,
        action,
        resource,
        resource_id,
        request.url.path,
    )
    return info
