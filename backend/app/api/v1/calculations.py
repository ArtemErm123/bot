from fastapi import APIRouter, Depends, Request

from app.api.v1.utils import audit_log, not_found
from app.core.rbac import require_roles
from app.core.security import TokenPayload
from app.repositories.entities import calculation_repo
from app.schemas.resources import Calculation, CalculationBase

router = APIRouter(prefix="/calculations", tags=["calculations"])

@router.get("", response_model=list[Calculation])
def list_items() -> list[Calculation]: return calculation_repo.list()

@router.post("", response_model=Calculation)
def create_item(payload: CalculationBase, request: Request, user: TokenPayload = Depends(require_roles("admin", "engineer"))) -> Calculation:
    item = calculation_repo.create(payload); audit_log(request, user, "create", "calculation", item.id); return item

@router.get("/{item_id}", response_model=Calculation)
def get_item(item_id: int) -> Calculation:
    item = calculation_repo.get(item_id)
    if not item: raise not_found("Calculation", item_id)
    return item

@router.put("/{item_id}", response_model=Calculation)
def update_item(item_id: int, payload: CalculationBase, request: Request, user: TokenPayload = Depends(require_roles("admin", "engineer"))) -> Calculation:
    item = calculation_repo.update(item_id, payload)
    if not item: raise not_found("Calculation", item_id)
    audit_log(request, user, "update", "calculation", item.id); return item

@router.delete("/{item_id}")
def delete_item(item_id: int, request: Request, user: TokenPayload = Depends(require_roles("admin"))) -> dict[str, bool]:
    if not calculation_repo.delete(item_id): raise not_found("Calculation", item_id)
    audit_log(request, user, "delete", "calculation", item_id); return {"ok": True}
