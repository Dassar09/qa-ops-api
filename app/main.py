from fastapi import FastAPI

app = FastAPI(title="QA Ops API")

@app.get("/health")
def health():
    return {"status": "ok"}