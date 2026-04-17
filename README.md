# WorkTrack 


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
```

Then open:

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`
