# WorkTrack Sprint 1 Backend

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
cd worktrack
docker compose up --build
```

Then open:

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
