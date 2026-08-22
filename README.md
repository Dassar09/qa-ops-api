# QA Ops API

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Install dependencies

```powershell
python -m pip install -r requirements.txt
```
## Run
docler start qa-pg
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload

## Endpoints
- GET /health
- /projects CRUD
- /issues CRUD + filters
- /issues/{id}/comments

# stack
FatAPI - SQLModel - PostgreSQL - Docker