from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate
from app.services.authorization_service import ensure_project_access, ensure_project_mutation, is_admin


def create_project(db: Session, payload: ProjectCreate, current_user: User) -> Project:
    project = Project(
        name=payload.name,
        code=payload.code,
        description=payload.description,
        status=payload.status,
        owner_id=current_user.id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def list_projects(db: Session, current_user: User) -> list[Project]:
    stmt = select(Project).order_by(Project.id.desc())

    if not is_admin(current_user):
        stmt = stmt.where(Project.owner_id == current_user.id)

    return db.execute(stmt).scalars().all()


def get_project_or_404(db: Session, project_id: int, current_user: User) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    ensure_project_access(project, current_user)
    return project


def update_project(db: Session, project_id: int, payload: ProjectUpdate, current_user: User) -> Project:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    ensure_project_mutation(project, current_user)

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(project, key, value)

    db.add(project)
    db.commit()
    db.refresh(project)
    return project