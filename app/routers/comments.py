from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Comment, Issue
from app.schemas import CommentCreate, CommentRead

router = APIRouter(tags=["comments"])

@router.post("/issues/{issue_id}/comments", response_model=CommentRead, status_code=201)
def create_comment(
    issue_id: int,
    payload: CommentCreate,
    session: Session = Depends(get_session),
):
    issue = session.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    comment = Comment(
    body=payload.body,
    issue_id=issue_id,
    author_id=payload.author_id,
    )
    session.add(comment)
    session.commit()
    session.refresh(comment)
    return comment

@router.get("/issues/{issue_id}/comments", response_model=list[CommentRead])
def list_comments(issue_id: int, session: Session = Depends(get_session)):
    issue = session.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    return session.exec(select(Comment).where(Comment.issue_id == issue_id)).all()