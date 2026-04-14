from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy import String, cast, select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, get_db
from app.core.deps import get_current_user
from app.models.project import Project
from app.models.user import User
from app.models.work_item import WorkItem
from app.schemas.work_item import WorkItemCreate, WorkItemOut, WorkItemUpdate
from app.services.activity_service import log_activity
from app.services.report_service import refresh_dashboard_materialized_view

router = APIRouter(prefix="/work-items", tags=["work-items"])


def refresh_dashboard_in_background() -> None:
    db = SessionLocal()
    try:
        refresh_dashboard_materialized_view(db)
    finally:
        db.close()


@router.post("", response_model=WorkItemOut, status_code=status.HTTP_201_CREATED)
def create_work_item(payload: WorkItemCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.get(Project, payload.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

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
    log_activity(db, current_user.id, work_item.id, "work_item_created", {"title": work_item.title})
    db.commit()
    db.refresh(work_item)
    background_tasks.add_task(refresh_dashboard_in_background)
    return work_item


@router.get("", response_model=list[WorkItemOut])
def list_work_items(status: str | None = None, priority: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(WorkItem).where(WorkItem.is_deleted.is_(False)).order_by(WorkItem.id.desc())
    if status:
        stmt = stmt.where(WorkItem.status == status)
    if priority:
        stmt = stmt.where(WorkItem.priority == priority)
    return db.execute(stmt).scalars().all()


@router.get("/search", response_model=list[WorkItemOut])
def search_work_items(q: str = Query(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(WorkItem).where(WorkItem.is_deleted.is_(False), WorkItem.title.ilike(f"%{q}%"))
    return db.execute(stmt).scalars().all()


@router.get("/by-project/{project_id}", response_model=list[WorkItemOut])
def get_by_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(WorkItem).where(WorkItem.project_id == project_id, WorkItem.is_deleted.is_(False))
    return db.execute(stmt).scalars().all()


@router.get("/metadata/search", response_model=list[WorkItemOut])
def search_by_metadata(client_visible: bool | None = None, tag: str | None = None, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(WorkItem).where(WorkItem.is_deleted.is_(False))
    if client_visible is not None:
        stmt = stmt.where(cast(WorkItem.metadata_jsonb["client_visible"].astext, String) == str(client_visible).lower())
    if tag:
        stmt = stmt.where(WorkItem.metadata_jsonb["tags"].contains([tag]))
    return db.execute(stmt).scalars().all()


@router.get("/{work_item_id}", response_model=WorkItemOut)
def get_work_item(work_item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    work_item = db.get(WorkItem, work_item_id)
    if not work_item or work_item.is_deleted:
        raise HTTPException(status_code=404, detail="Work item not found")
    return work_item


@router.patch("/{work_item_id}", response_model=WorkItemOut)
def update_work_item(work_item_id: int, payload: WorkItemUpdate, background_tasks: BackgroundTasks, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    work_item = db.get(WorkItem, work_item_id)
    if not work_item or work_item.is_deleted:
        raise HTTPException(status_code=404, detail="Work item not found")

    changes = payload.model_dump(exclude_unset=True)
    old_status = work_item.status
    old_priority = work_item.priority

    for key, value in changes.items():
        setattr(work_item, key, value)

    if "status" in changes and old_status != work_item.status:
        log_activity(db, current_user.id, work_item.id, "status_changed", {"from": old_status, "to": work_item.status})
    if "priority" in changes and old_priority != work_item.priority:
        log_activity(db, current_user.id, work_item.id, "priority_changed", {"from": old_priority, "to": work_item.priority})

    db.add(work_item)
    db.commit()
    db.refresh(work_item)
    background_tasks.add_task(refresh_dashboard_in_background)
    return work_item


@router.delete("/{work_item_id}")
def delete_work_item(work_item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    work_item = db.get(WorkItem, work_item_id)
    if not work_item or work_item.is_deleted:
        raise HTTPException(status_code=404, detail="Work item not found")

    work_item.is_deleted = True
    db.add(work_item)
    db.commit()
    return {"detail": "Work item deleted"}
