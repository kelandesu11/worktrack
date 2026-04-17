from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.models.work_item import WorkItem


def is_admin(user: User) -> bool:
    return user.role == "admin"


def ensure_project_access(project: Project, current_user: User) -> None:
    if is_admin(current_user):
        return
    if project.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this project",
        )


def ensure_project_mutation(project: Project, current_user: User) -> None:
    ensure_project_access(project, current_user)


def ensure_work_item_access(db: Session, work_item: WorkItem, current_user: User) -> None:
    if is_admin(current_user):
        return

    project = db.get(Project, work_item.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    allowed = {
        project.owner_id,
        work_item.assignee_id,
        work_item.reporter_id,
    }

    if current_user.id not in allowed:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this work item",
        )