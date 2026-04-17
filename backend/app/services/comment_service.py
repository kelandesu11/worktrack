from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.models.user import User
from app.models.work_item import WorkItem
from app.schemas.comment import CommentCreate
from app.services.activity_service import log_activity
from app.services.authorization_service import ensure_work_item_access


def add_comment(db: Session, work_item_id: int, payload: CommentCreate, current_user: User) -> Comment:
    work_item = db.get(WorkItem, work_item_id)
    if not work_item or work_item.is_deleted:
        raise HTTPException(status_code=404, detail="Work item not found")

    ensure_work_item_access(db, work_item, current_user)

    comment = Comment(
        work_item_id=work_item_id,
        author_id=current_user.id,
        body=payload.body,
    )
    db.add(comment)
    db.flush()

    log_activity(
        db,
        current_user.id,
        work_item_id,
        "comment_added",
        {"comment_id": comment.id},
    )

    db.commit()
    db.refresh(comment)
    return comment


def list_comments(db: Session, work_item_id: int, current_user: User) -> list[Comment]:
    work_item = db.get(WorkItem, work_item_id)
    if not work_item or work_item.is_deleted:
        raise HTTPException(status_code=404, detail="Work item not found")

    ensure_work_item_access(db, work_item, current_user)

    stmt = select(Comment).where(Comment.work_item_id == work_item_id).order_by(Comment.id.asc())
    return db.execute(stmt).scalars().all()