from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Issue(BaseModel):
    title: str
    description: str

issues: list[Issue] = []

@app.post("/issues")
def create_issue(issue: Issue):
    issues.append(issue)
    return issue

@app.get("/issues")
def list_issues():
    return issues

@app.get("/health")
def health():
    return {"status": "ok"}
