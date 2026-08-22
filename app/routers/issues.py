from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Issue, Project
from app.schemas import IssueCreate, IssueRead, IssueUpdate

router = APIRouter(prefix="/issues", tags=["issues"])

ALLOWED_STATUS = {"open", "in_progress", "done"}
ALLOWED_PRIORITY = {"low", "medium", "high"}


def _validate_issue_fields(status: str | None, priority: str | None) -> None:
    if status is not None and status not in ALLOWED_STATUS:
        raise HTTPException(status_code=400, detail="Invalid status")
    if priority is not None and priority not in ALLOWED_PRIORITY:
        raise HTTPException(status_code=400, detail="Invalid priority")


def _validate_project_id(session: Session, project_id: int | None) -> None:
    if project_id is None:
        return
    project = session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")


@router.post("", response_model=IssueRead, status_code=201)
def create_issue(payload: IssueCreate, session: Session = Depends(get_session)):
    _validate_issue_fields(payload.status, payload.priority)
    _validate_project_id(session, payload.project_id)

    issue = Issue(**payload.model_dump())
    session.add(issue)
    session.commit()
    session.refresh(issue)
    return issue


@router.get("", response_model=list[IssueRead])
def list_issues(
    session: Session = Depends(get_session),
    status: str | None = None,
    project_id: int | None = None,
    priority: str | None = None,
    skip: int = 0,
    limit: int = 20,
):
    _validate_issue_fields(status, priority)

    query = select(Issue)
    if status:
        query = query.where(Issue.status == status)
    if project_id:
        query = query.where(Issue.project_id == project_id)
    if priority:
        query = query.where(Issue.priority == priority)

    return session.exec(query.offset(skip).limit(limit)).all()


@router.get("/{issue_id}", response_model=IssueRead)
def get_issue(issue_id: int, session: Session = Depends(get_session)):
    issue = session.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue

@router.get("", response_model=list[IssueRead])
def list_issues(
    session: Session = Depends(get_session),
    status: str | None = None,
    project_id: int | None = None,
    priority: str | None = None,
    skip: int = 0,
    limit: int = 20,
):

    query = select(Issue)
    if status:
        query = query.where(Issue.status == status)
    if project_id:
        query = query.where(Issue.project_id == project_id)
    if priority:
        query = query.where(Issue.priority == priority)

    return session.exec(query.offset(skip).limit(limit)).all()

@router.patch("/{issue_id}", response_model=IssueRead)
def update_issue(
    issue_id: int,
    payload: IssueUpdate,
    session: Session = Depends(get_session),
):
    issue = session.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    data = payload.model_dump(exclude_unset=True)
    _validate_issue_fields(data.get("status"), data.get("priority"))
    _validate_project_id(session, data.get("project_id"))

    for key, value in data.items():
        setattr(issue, key, value)

    session.add(issue)
    session.commit()
    session.refresh(issue)
    return issue


@router.delete("/{issue_id}", status_code=204)
def delete_issue(issue_id: int, session: Session = Depends(get_session)):
    issue = session.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    session.delete(issue)
    session.commit()