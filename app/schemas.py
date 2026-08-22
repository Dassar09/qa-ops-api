from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime

class IssueCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "open"
    priority: str = "medium"
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None

class IssueUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None

class IssueRead(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    project_id: Optional[int] = None
    assigned_to: Optional[int] = None
    created_at: datetime

class CommentCreate(BaseModel):
    body: str
    author_id: Optional[int] = None

class CommentRead(BaseModel):
    id: int
    body: str
    issue_id: int
    author_id: Optional[int] = None
    created_at: datetime