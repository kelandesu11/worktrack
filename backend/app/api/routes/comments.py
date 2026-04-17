from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentOut
from app.services.comment_service import add_comment, list_comments

router = APIRouter(tags=["comments"])


@router.post("/work-items/{work_item_id}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def add_comment_route(
    work_item_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return add_comment(db, work_item_id, payload, current_user)


@router.get("/work-items/{work_item_id}/comments", response_model=list[CommentOut])
def list_comments_route(
    work_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return list_comments(db, work_item_id, current_user)