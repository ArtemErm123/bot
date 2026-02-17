from fastapi import APIRouter, Depends, Request

from app.api.v1.utils import audit_log, not_found
from app.core.rbac import require_roles
from app.core.security import TokenPayload
from app.repositories.entities import material_repo
from app.schemas.resources import Material, MaterialBase

router = APIRouter(prefix="/materials", tags=["materials"])

@router.get("", response_model=list[Material])
def list_items() -> list[Material]: return material_repo.list()

@router.post("", response_model=Material)
def create_item(payload: MaterialBase, request: Request, user: TokenPayload = Depends(require_roles("admin", "engineer"))) -> Material:
    item = material_repo.create(payload); audit_log(request, user, "create", "material", item.id); return item

@router.get("/{item_id}", response_model=Material)
def get_item(item_id: int) -> Material:
    item = material_repo.get(item_id)
    if not item: raise not_found("Material", item_id)
    return item

@router.put("/{item_id}", response_model=Material)
def update_item(item_id: int, payload: MaterialBase, request: Request, user: TokenPayload = Depends(require_roles("admin", "engineer"))) -> Material:
    item = material_repo.update(item_id, payload)
    if not item: raise not_found("Material", item_id)
    audit_log(request, user, "update", "material", item.id); return item

@router.delete("/{item_id}")
def delete_item(item_id: int, request: Request, user: TokenPayload = Depends(require_roles("admin"))) -> dict[str, bool]:
    if not material_repo.delete(item_id): raise not_found("Material", item_id)
    audit_log(request, user, "delete", "material", item_id); return {"ok": True}
