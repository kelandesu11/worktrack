from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.comment import Comment
from app.models.user import User
from app.models.work_item import WorkItem
from app.schemas.comment import CommentCreate, CommentOut
from app.services.activity_service import log_activity

router = APIRouter(tags=["comments"])


@router.post("/work-items/{work_item_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def add_comment(work_item_id: int, payload: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    work_item = db.get(WorkItem, work_item_id)
    if not work_item or work_item.is_deleted:
        raise HTTPException(status_code=404, detail="Work item not found")

    comment = Comment(work_item_id=work_item_id, author_id=current_user.id, body=payload.body)
    db.add(comment)
    db.flush()
    log_activity(db, current_user.id, work_item_id, "comment_added", {"comment_id": comment.id})
    db.commit()
    db.refresh(comment)
    return comment


@router.get("/work-items/{work_item_id}/comments", response_model=list[CommentOut])
def list_comments(work_item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    stmt = select(Comment).where(Comment.work_item_id == work_item_id).order_by(Comment.id.asc())
    return db.execute(stmt).scalars().all()
