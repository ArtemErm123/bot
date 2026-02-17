from fastapi import APIRouter, Depends, Request

from app.api.v1.utils import audit_log, not_found
from app.core.rbac import require_roles
from app.core.security import TokenPayload
from app.repositories.entities import project_repo
from app.schemas.resources import Project, ProjectBase

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("", response_model=list[Project])
def list_projects() -> list[Project]:
    return project_repo.list()


@router.post("", response_model=Project)
def create_project(
    payload: ProjectBase,
    request: Request,
    user: TokenPayload = Depends(require_roles("admin", "engineer")),
) -> Project:
    project = project_repo.create(payload)
    audit_log(request, user, "create", "project", project.id)
    return project


@router.get("/{project_id}", response_model=Project)
def get_project(project_id: int) -> Project:
    project = project_repo.get(project_id)
    if not project:
        raise not_found("Project", project_id)
    return project


@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: int,
    payload: ProjectBase,
    request: Request,
    user: TokenPayload = Depends(require_roles("admin", "engineer")),
) -> Project:
    project = project_repo.update(project_id, payload)
    if not project:
        raise not_found("Project", project_id)
    audit_log(request, user, "update", "project", project.id)
    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    request: Request,
    user: TokenPayload = Depends(require_roles("admin")),
) -> dict[str, bool]:
    if not project_repo.delete(project_id):
        raise not_found("Project", project_id)
    audit_log(request, user, "delete", "project", project_id)
    return {"ok": True}
