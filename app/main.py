from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from app.database import create_db_and_tables,get_session
from app.models import Issue

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="QA Ops API", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/issues", response_model=Issue)
def create_issue(issue: Issue, session: Session = Depends(get_session)):
    #avoid clint-sent id
    issue.id = None
    session.add(issue)
    session.commit()
    session.refresh(issue)
    return issue

@app.get("/issues", response_model=list[Issue])
def list_issues(session: Session = Depends(get_session)):
    return session.exec(select(Issue)).all()

@app.get("/issues/{issue_id}", response_model=Issue)
def get_issue(issue_id: int, session: Session = Depends(get_session)):
    issue = session.get(Issue, issue_id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    return issue