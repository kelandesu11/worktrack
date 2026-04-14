# WorkTrack Sprint 1 Backend

This is the simplest complete backend for Sprint 1.

## What is included

- FastAPI backend
- PostgreSQL in its own container
- Docker Compose for backend + db
- SQLAlchemy models and session setup
- Raw PostgreSQL SQL files
- JWT authentication
- TOTP MFA demo
- Projects, work items, comments, activity, and report endpoints
- One JSONB filter endpoint
- One background task endpoint for refreshing the materialized view

## Run it

```bash
cd worktrack-sprint1-backend
docker compose up --build
```

Then open:

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Notes

This project creates tables on startup with SQLAlchemy. The raw SQL files are included in `backend/sql` for submission.
