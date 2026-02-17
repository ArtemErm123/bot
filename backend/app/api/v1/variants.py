from fastapi import APIRouter, Depends, Request

from app.api.v1.utils import audit_log, not_found
from app.core.rbac import require_roles
from app.core.security import TokenPayload
from app.repositories.entities import variant_repo
from app.schemas.resources import Variant, VariantBase

router = APIRouter(prefix="/variants", tags=["variants"])

@router.get("", response_model=list[Variant])
def list_items() -> list[Variant]: return variant_repo.list()

@router.post("", response_model=Variant)
def create_item(payload: VariantBase, request: Request, user: TokenPayload = Depends(require_roles("admin", "engineer"))) -> Variant:
    item = variant_repo.create(payload); audit_log(request, user, "create", "variant", item.id); return item

@router.get("/{item_id}", response_model=Variant)
def get_item(item_id: int) -> Variant:
    item = variant_repo.get(item_id)
    if not item: raise not_found("Variant", item_id)
    return item

@router.put("/{item_id}", response_model=Variant)
def update_item(item_id: int, payload: VariantBase, request: Request, user: TokenPayload = Depends(require_roles("admin", "engineer"))) -> Variant:
    item = variant_repo.update(item_id, payload)
    if not item: raise not_found("Variant", item_id)
    audit_log(request, user, "update", "variant", item.id); return item

@router.delete("/{item_id}")
def delete_item(item_id: int, request: Request, user: TokenPayload = Depends(require_roles("admin"))) -> dict[str, bool]:
    if not variant_repo.delete(item_id): raise not_found("Variant", item_id)
    audit_log(request, user, "delete", "variant", item_id); return {"ok": True}
