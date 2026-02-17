from fastapi import APIRouter, Depends, Request

from app.api.v1.utils import audit_log, not_found
from app.core.rbac import require_roles
from app.core.security import TokenPayload
from app.repositories.entities import mix_repo
from app.schemas.resources import Mix, MixBase

router = APIRouter(prefix="/mixes", tags=["mixes"])

@router.get("", response_model=list[Mix])
def list_items() -> list[Mix]: return mix_repo.list()

@router.post("", response_model=Mix)
def create_item(payload: MixBase, request: Request, user: TokenPayload = Depends(require_roles("admin", "engineer"))) -> Mix:
    item = mix_repo.create(payload); audit_log(request, user, "create", "mix", item.id); return item

@router.get("/{item_id}", response_model=Mix)
def get_item(item_id: int) -> Mix:
    item = mix_repo.get(item_id)
    if not item: raise not_found("Mix", item_id)
    return item

@router.put("/{item_id}", response_model=Mix)
def update_item(item_id: int, payload: MixBase, request: Request, user: TokenPayload = Depends(require_roles("admin", "engineer"))) -> Mix:
    item = mix_repo.update(item_id, payload)
    if not item: raise not_found("Mix", item_id)
    audit_log(request, user, "update", "mix", item.id); return item

@router.delete("/{item_id}")
def delete_item(item_id: int, request: Request, user: TokenPayload = Depends(require_roles("admin"))) -> dict[str, bool]:
    if not mix_repo.delete(item_id): raise not_found("Mix", item_id)
    audit_log(request, user, "delete", "mix", item_id); return {"ok": True}
