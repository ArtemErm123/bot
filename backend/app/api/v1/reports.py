from fastapi import APIRouter, Depends, Request

from app.api.v1.utils import audit_log, not_found
from app.core.rbac import require_roles
from app.core.security import TokenPayload
from app.repositories.entities import report_repo
from app.schemas.resources import Report, ReportBase

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("", response_model=list[Report])
def list_items() -> list[Report]: return report_repo.list()

@router.post("", response_model=Report)
def create_item(payload: ReportBase, request: Request, user: TokenPayload = Depends(require_roles("admin", "engineer"))) -> Report:
    item = report_repo.create(payload); audit_log(request, user, "create", "report", item.id); return item

@router.get("/{item_id}", response_model=Report)
def get_item(item_id: int) -> Report:
    item = report_repo.get(item_id)
    if not item: raise not_found("Report", item_id)
    return item

@router.put("/{item_id}", response_model=Report)
def update_item(item_id: int, payload: ReportBase, request: Request, user: TokenPayload = Depends(require_roles("admin", "engineer"))) -> Report:
    item = report_repo.update(item_id, payload)
    if not item: raise not_found("Report", item_id)
    audit_log(request, user, "update", "report", item.id); return item

@router.delete("/{item_id}")
def delete_item(item_id: int, request: Request, user: TokenPayload = Depends(require_roles("admin"))) -> dict[str, bool]:
    if not report_repo.delete(item_id): raise not_found("Report", item_id)
    audit_log(request, user, "delete", "report", item_id); return {"ok": True}
