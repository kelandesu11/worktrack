from sqlalchemy.orm import Session

from app.models.activity_log import ActivityLog


def log_activity(db: Session, actor_id: int, work_item_id: int | None, event_type: str, payload: dict) -> None:
    db.add(
        ActivityLog(
            actor_id=actor_id,
            work_item_id=work_item_id,
            event_type=event_type,
            event_payload_jsonb=payload,
        )
    )
