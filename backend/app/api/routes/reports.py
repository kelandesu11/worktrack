from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import SessionLocal, get_db
from app.core.deps import get_current_user
from app.models.user import User

router = APIRouter(tags=["reports"])


def background_refresh_mv() -> None:
    db = SessionLocal()
    try:
        db.execute(text("REFRESH MATERIALIZED VIEW dashboard_summary_mv"))
        db.commit()
    finally:
        db.close()


@router.get("/dashboard/summary")
def dashboard_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = db.execute(text("SELECT * FROM dashboard_summary_mv ORDER BY project_id")).mappings().all()
    return [dict(row) for row in rows]


@router.get("/reports/work-items-by-status")
def work_items_by_status(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = db.execute(text("SELECT status, COUNT(*) AS total FROM work_items WHERE is_deleted = false GROUP BY status ORDER BY status")).mappings().all()
    return [dict(row) for row in rows]


@router.get("/reports/project-load")
def project_load(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = db.execute(text("SELECT p.name AS project_name, COUNT(w.id) AS total_work_items FROM projects p LEFT JOIN work_items w ON w.project_id = p.id AND w.is_deleted = false GROUP BY p.id, p.name ORDER BY p.name")).mappings().all()
    return [dict(row) for row in rows]


@router.get("/reports/recent-activity")
def recent_activity(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rows = db.execute(text("SELECT id, event_type, created_at FROM activity_logs ORDER BY created_at DESC LIMIT 20")).mappings().all()
    return [dict(row) for row in rows]


@router.post("/reports/refresh-materialized-view")
def refresh_materialized_view(background_tasks: BackgroundTasks, current_user: User = Depends(get_current_user)):
    background_tasks.add_task(background_refresh_mv)
    return {"detail": "Materialized view refresh started"}
