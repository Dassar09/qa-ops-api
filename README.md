# QA Ops API

Day 1: minimal FastAPI service with a health-check endpoint.

## Run locally

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/health` to verify the service. It returns:

```json
{"status":"ok"}
```

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Install dependencies

```powershell
python -m pip install -r requirements.txt
```
