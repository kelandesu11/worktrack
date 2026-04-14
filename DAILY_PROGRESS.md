## Date: 2026-04-10

### Goal for today
- Get backend started
- Make sure FastAPI runs
- Begin Docker setup

### What I completed
- Set up initial backend folder structure
- Created basic FastAPI app and tested locally
- Started writing Dockerfile for backend

### Files / modules touched
- backend/app/main.py
- backend/Dockerfile
- backend/requirements.txt

### API endpoints completed
- GET /health

### SQL completed
- None

### Docker / infra completed
- Backend Dockerfile started

### Frontend completed
- None

### Blockers / questions
- None

### Plan for next day
- Add Postgres container
- Connect backend to DB


## Date: 2026-04-11

### Goal for today
- Set up PostgreSQL in Docker
- Connect FastAPI to DB
- Start schema

### What I completed
- Added Postgres to docker-compose
- Got backend talking to DB
- Created base SQLAlchemy setup
- Started writing schema.sql

### Files / modules touched
- docker-compose.yml
- backend/app/core/database.py
- backend/app/models/base.py
- backend/sql/schema.sql

### API endpoints completed
- None

### SQL completed
- Basic tables created (users, projects, work_items, etc.)

### Docker / infra completed
- DB container running
- Backend connected (had to fix host from localhost → db)

### Frontend completed
- None

### Blockers / questions
- Small issue with DB connection string but fixed

### Plan for next day
- Build auth
- Add JWT
- Start MFA


## Date: 2026-04-12

### Goal for today
- Get authentication working
- Add TOTP support

### What I completed
- Built register + login endpoints
- Added password hashing
- Implemented JWT tokens
- Got basic TOTP setup working (generate + verify)

### Files / modules touched
- backend/app/api/routes/auth.py
- backend/app/api/routes/mfa.py
- backend/app/core/security.py
- backend/app/schemas/auth.py

### API endpoints completed
- POST /auth/register
- POST /auth/login
- GET /auth/me
- POST /mfa/setup
- POST /mfa/verify

### SQL completed
- Started seed.sql (users)

### Docker / infra completed
- None

### Frontend completed
- None

### Blockers / questions
- TOTP took a bit to get right (format/verification)

### Plan for next day
- Build projects + work items
- Add JSONB field


## Date: 2026-04-13

### Goal for today
- Build core business endpoints
- Add JSONB functionality

### What I completed
- Added project endpoints
- Added work item CRUD
- Added comments
- Implemented metadata_jsonb field
- Built a simple metadata search endpoint

### Files / modules touched
- backend/app/api/routes/projects.py
- backend/app/api/routes/work_items.py
- backend/app/api/routes/comments.py
- backend/app/models/work_item.py

### API endpoints completed
- POST /projects
- GET /projects
- GET /projects/{id}
- POST /work-items
- GET /work-items
- GET /work-items/{id}
- PATCH /work-items/{id}
- DELETE /work-items/{id}
- GET /work-items/metadata/search

### SQL completed
- jsonb_queries.sql

### Docker / infra completed
- None

### Frontend completed
- None

### Blockers / questions
- Had to double check JSONB query syntax

### Plan for next day
- Add reporting
- Add background task
- Finish SQL files


## Date: 2026-04-14

### Goal for today
- Finish remaining backend requirements
- Add reports + background task

### What I completed
- Added activity logging
- Created reports endpoints
- Added materialized view SQL
- Wired up background task to refresh view
- Finished SQL files
- Verified docker-compose runs everything

### Files / modules touched
- backend/app/api/routes/reports.py
- backend/app/api/routes/activity.py
- backend/sql/materialized_views.sql
- backend/sql/views.sql
- docker-compose.yml

### API endpoints completed
- GET /activity
- GET /dashboard/summary
- GET /reports/work-items-by-status
- POST /reports/refresh-materialized-view

### SQL completed
- views.sql
- materialized_views.sql
- advanced_queries.sql
- seed.sql

### Docker / infra completed
- Full setup working (backend + db)

### Frontend completed
- None

### Blockers / questions
- None

### Plan for next day
- Start frontend (Sprint 2)