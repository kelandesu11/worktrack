from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

import app.models
from app.api.routes import activity, auth, comments, mfa, projects, reports, work_items
from app.core.config import get_settings
from app.core.database import Base, SessionLocal, engine

settings = get_settings()
app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_materialized_view() -> None:
    db = SessionLocal()
    try:
        db.execute(text("CREATE MATERIALIZED VIEW IF NOT EXISTS dashboard_summary_mv AS SELECT p.id AS project_id, p.name AS project_name, COUNT(w.id) AS total_work_items, COUNT(*) FILTER (WHERE w.status != 'done' AND w.id IS NOT NULL AND w.is_deleted = false) AS open_work_items, COUNT(*) FILTER (WHERE w.status = 'done' AND w.id IS NOT NULL AND w.is_deleted = false) AS done_work_items, COUNT(*) FILTER (WHERE w.priority = 'high' AND w.id IS NOT NULL AND w.is_deleted = false) AS high_priority_items FROM projects p LEFT JOIN work_items w ON w.project_id = p.id GROUP BY p.id, p.name"))
        db.commit()
    finally:
        db.close()


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    create_materialized_view()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"name": settings.app_name, "version": settings.app_version}


app.include_router(auth.router)
app.include_router(mfa.router)
app.include_router(projects.router)
app.include_router(work_items.router)
app.include_router(comments.router)
app.include_router(activity.router)
app.include_router(reports.router)
