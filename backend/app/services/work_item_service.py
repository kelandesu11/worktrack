from fastapi import BackgroundTasks, HTTPException
from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.models.work_item import WorkItem
from app.schemas.work_item import WorkItemCreate, WorkItemUpdate
from app.services.activity_service import log_activity
from app.services.authorization_service import ensure_project_access, ensure_work_item_access, is_admin


def create_work_item(
    db: Session,
    payload: WorkItemCreate,
    current_user: User,
    background_tasks: BackgroundTasks,
    refresh_callback,
) -> WorkItem:
    project = db.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    ensure_project_access(project, current_user)

    work_item = WorkItem(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
        due_date=payload.due_date,
        estimated_hours=payload.estimated_hours,
        actual_hours=payload.actual_hours,
        project_id=payload.project_id,
        assignee_id=payload.assignee_id,
        reporter_id=current_user.id,
        metadata_jsonb=payload.metadata_jsonb,
    )
    db.add(work_item)
    db.flush()

    log_activity(
        db,
        current_user.id,
        work_item.id,
        "work_item_created",
        {"title": work_item.title},
    )

    db.commit()
    db.refresh(work_item)
    background_tasks.add_task(refresh_callback)
    return work_item


def list_work_items(
    db: Session,
    current_user: User,
    status: str | None = None,
    priority: str | None = None,
) -> list[WorkItem]:
    stmt = select(WorkItem).where(WorkItem.is_deleted.is_(False)).order_by(WorkItem.id.desc())

    if status:
        stmt = stmt.where(WorkItem.status == status)
    if priority:
        stmt = stmt.where(WorkItem.priority == priority)

    work_items = db.execute(stmt).scalars().all()

    if is_admin(current_user):
        return work_items

    filtered: list[WorkItem] = []
    for work_item in work_items:
        try:
            ensure_work_item_access(db, work_item, current_user)
            filtered.append(work_item)
        except HTTPException:
            continue
    return filtered


def search_work_items(db: Session, current_user: User, q: str) -> list[WorkItem]:
    stmt = select(WorkItem).where(
        WorkItem.is_deleted.is_(False),
        WorkItem.title.ilike(f"%{q}%"),
    )
    work_items = db.execute(stmt).scalars().all()

    if is_admin(current_user):
        return work_items

    filtered: list[WorkItem] = []
    for work_item in work_items:
        try:
            ensure_work_item_access(db, work_item, current_user)
            filtered.append(work_item)
        except HTTPException:
            continue
    return filtered


def get_work_items_by_project(db: Session, project_id: int, current_user: User) -> list[WorkItem]:
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    ensure_project_access(project, current_user)

    stmt = select(WorkItem).where(
        WorkItem.project_id == project_id,
        WorkItem.is_deleted.is_(False),
    )
    return db.execute(stmt).scalars().all()


def search_work_items_by_metadata(
    db: Session,
    current_user: User,
    client_visible: bool | None = None,
    tag: str | None = None,
) -> list[WorkItem]:
    stmt = select(WorkItem).where(WorkItem.is_deleted.is_(False))

    if client_visible is not None:
        stmt = stmt.where(
            cast(WorkItem.metadata_jsonb["client_visible"].astext, String)
            == str(client_visible).lower()
        )

    if tag:
        stmt = stmt.where(WorkItem.metadata_jsonb["tags"].contains([tag]))

    work_items = db.execute(stmt).scalars().all()

    if is_admin(current_user):
        return work_items

    filtered: list[WorkItem] = []
    for work_item in work_items:
        try:
            ensure_work_item_access(db, work_item, current_user)
            filtered.append(work_item)
        except HTTPException:
            continue
    return filtered


def get_work_item_or_404(db: Session, work_item_id: int, current_user: User) -> WorkItem:
    work_item = db.get(WorkItem, work_item_id)
    if not work_item or work_item.is_deleted:
        raise HTTPException(status_code=404, detail="Work item not found")

    ensure_work_item_access(db, work_item, current_user)
    return work_item


def update_work_item(
    db: Session,
    work_item_id: int,
    payload: WorkItemUpdate,
    current_user: User,
    background_tasks: BackgroundTasks,
    refresh_callback,
) -> WorkItem:
    work_item = db.get(WorkItem, work_item_id)
    if not work_item or work_item.is_deleted:
        raise HTTPException(status_code=404, detail="Work item not found")

    ensure_work_item_access(db, work_item, current_user)

    changes = payload.model_dump(exclude_unset=True)
    old_status = work_item.status
    old_priority = work_item.priority

    for key, value in changes.items():
        setattr(work_item, key, value)

    if "status" in changes and old_status != work_item.status:
        log_activity(
            db,
            current_user.id,
            work_item.id,
            "status_changed",
            {"from": old_status, "to": work_item.status},
        )

    if "priority" in changes and old_priority != work_item.priority:
        log_activity(
            db,
            current_user.id,
            work_item.id,
            "priority_changed",
            {"from": old_priority, "to": work_item.priority},
        )

    db.add(work_item)
    db.commit()
    db.refresh(work_item)
    background_tasks.add_task(refresh_callback)
    return work_item


def delete_work_item(db: Session, work_item_id: int, current_user: User) -> dict:
    work_item = db.get(WorkItem, work_item_id)
    if not work_item or work_item.is_deleted:
        raise HTTPException(status_code=404, detail="Work item not found")

    ensure_work_item_access(db, work_item, current_user)

    work_item.is_deleted = True
    db.add(work_item)
    db.commit()
    return {"detail": "Work item deleted"}