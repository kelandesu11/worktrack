from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_admin
from app.models.activity_log import ActivityLog
from app.models.user import User

router = APIRouter(tags=["activity"])


@router.get("/activity")
def list_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    stmt = select(ActivityLog).order_by(ActivityLog.created_at.desc())
    rows = db.execute(stmt).scalars().all()

    return [
        {
            "id": row.id,
            "actor_id": row.actor_id,
            "work_item_id": row.work_item_id,
            "event_type": row.event_type,
            "event_payload_jsonb": row.event_payload_jsonb,
            "created_at": row.created_at,
        }
        for row in rows
    ]