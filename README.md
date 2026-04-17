# WorkTrack Sprint 1 Backend

This is the simplest complete backend for Sprint 1.

## What is included

- FastAPI backend
- PostgreSQL in its own container
- Docker Compose for backend + db
- SQLAlchemy models and session setup
- JWT authentication
- TOTP MFA demo
- Projects, work items, comments, activity, and report endpoints
- JSONB filtering
- Background task endpoint for refreshing the materialized view
- Database initialization SQL mounted into Postgres startup

## Run it

From the repository root:

```bash
docker compose up --build