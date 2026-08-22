from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import projects, issues, comments

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="QA Ops API", lifespan=lifespan)

app.include_router(projects.router)
app.include_router(issues.router)
app.include_router(comments.router)

@app.get("/health")
def health():
    return {"status": "ok"}