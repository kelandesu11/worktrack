from fastapi import APIRouter, BackgroundTasks, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.work_item import WorkItemCreate, WorkItemOut, WorkItemUpdate
from app.services.report_service import refresh_dashboard_materialized_view
from app.services.work_item_service import (
    create_work_item,
    delete_work_item,
    get_work_item_or_404,
    get_work_items_by_project,
    list_work_items,
    search_work_items,
    search_work_items_by_metadata,
    update_work_item,
)

router = APIRouter(prefix="/work-items", tags=["work-items"])


def refresh_dashboard_in_background() -> None:
    db = SessionLocal()
    try:
        refresh_dashboard_materialized_view(db)
    finally:
        db.close()


@router.post("", response_model=WorkItemOut, status_code=status.HTTP_201_CREATED)
def create_work_item_route(
    payload: WorkItemCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_work_item(db, payload, current_user, background_tasks, refresh_dashboard_in_background)


@router.get("", response_model=list[WorkItemOut])
def list_work_items_route(
    status: str | None = None,
    priority: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_work_items(db, current_user, status=status, priority=priority)


@router.get("/search", response_model=list[WorkItemOut])
def search_work_items_route(
    q: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return search_work_items(db, current_user, q)


@router.get("/by-project/{project_id}", response_model=list[WorkItemOut])
def get_by_project_route(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_work_items_by_project(db, project_id, current_user)


@router.get("/metadata/search", response_model=list[WorkItemOut])
def search_by_metadata_route(
    client_visible: bool | None = None,
    tag: str | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return search_work_items_by_metadata(db, current_user, client_visible=client_visible, tag=tag)


@router.get("/{work_item_id}", response_model=WorkItemOut)
def get_work_item_route(
    work_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_work_item_or_404(db, work_item_id, current_user)


@router.patch("/{work_item_id}", response_model=WorkItemOut)
def update_work_item_route(
    work_item_id: int,
    payload: WorkItemUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_work_item(
        db,
        work_item_id,
        payload,
        current_user,
        background_tasks,
        refresh_dashboard_in_background,
    )


@router.delete("/{work_item_id}")
def delete_work_item_route(
    work_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_work_item(db, work_item_id, current_user)