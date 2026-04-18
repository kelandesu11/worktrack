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


## Date: 2026-04-17

### What I worked on
Started implementing the frontend using React + Vite.

Created the base application structure and connected it to the existing backend using Docker.

### What was completed
- Set up React app using Vite
- Created project folder structure:
  - pages
  - layouts
  - services
  - context
- Implemented routing using React Router
- Created app shell layout:
  - sidebar navigation
  - top bar
- Added placeholder pages:
  - Dashboard
  - Projects
  - Work Items
  - Login
- Created AuthContext skeleton for future auth flow
- Set up Axios API client
- Added frontend Dockerfile
- Updated docker-compose to include frontend service

### Issues encountered
- Initial import errors due to missing files and incorrect file names
- Fixed by aligning folder structure and filenames with imports
- Docker caching caused stale file issues → resolved by rebuilding containers

### What I learned
- Importance of consistent file naming (case-sensitive in Docker/Linux)
- How to structure a React app cleanly for scaling
- How frontend and backend connect through Docker networking

### Next steps
- Implement login form and authentication flow
- Store and manage JWT token
- Add protected routes properly
- Redirect users based on auth state

### Notes
Frontend is being developed in small feature branches to keep PRs clean and realistic.


### What I worked on
Implemented the frontend authentication flow and connected it to the backend.

### What was completed
- Built login form UI
- Integrated `POST /auth/login`
- Stored JWT token in localStorage
- Implemented AuthContext for global auth state
- Added auto user loading with `GET /auth/me`
- Created protected route wrapper
- Added logout functionality
- Redirect users to login if not authenticated

### Issues encountered
- Login initially failed due to CORS error (`OPTIONS 405`)
  - Fixed by adding CORS middleware to backend
- Backend crash due to incorrect method (`app.add.middleware`)
  - Fixed to `app.add_middleware`
- Login returned 401 because seed data was not loaded
  - Fixed by resetting Docker volume with `docker compose down -v`

### What I learned
- How JWT auth flows work between frontend and backend
- How to manage global state in React using context
- Importance of CORS configuration in fullstack apps
- Docker volumes don’t rerun seed scripts unless reset

### Next steps
- Build dashboard UI using real data
- Implement project list and forms
- Connect frontend to project endpoints


### What I worked on
Built the dashboard view and project management UI.

### What was completed
- Connected dashboard to `/dashboard/summary`
- Displayed project summary cards
- Built project list page
- Implemented create project form
- Implemented update project functionality
- Refreshed project list after create/update

### Issues encountered
- Dashboard not showing new projects after creation
  - Root cause: materialized view not refreshed
  - Fixed by calling `/reports/refresh-materialized-view`
- Slight delay in dashboard updates due to background refresh task

### What I learned
- Materialized views do not update automatically
- Need to trigger refresh when underlying data changes
- How frontend interacts with derived/aggregated backend data
- Handling async updates between UI and backend

### Next steps
- Build work items list page
- Add filtering and search
- Implement create/update work items
- Add work item detail view with comments

### Notes
Frontend is now fully connected to backend auth, dashboard, and project APIs. Core flow is working end-to-end.


### What I worked on
Implemented the work items page and connected it to backend endpoints.

### What was completed
- Built work items list view
- Integrated `GET /work-items`
- Added search using `/work-items/search`
- Implemented filtering by status and priority
- Built create work item form
- Built update work item functionality
- Loaded projects for assigning work items

### Issues encountered
- Work item creation failed when project_id was missing or not converted to number
  - Fixed by ensuring project_id is selected and cast correctly
- Some 403 responses due to backend authorization rules
  - Confirmed expected behavior based on ownership rules

### What I learned
- Handling query params for filtering and search
- Managing multiple UI states (form, filters, list)
- Importance of validating input before API calls
- How frontend interacts with backend authorization rules

### Next steps
- Build work item detail page
- Add comments functionality
- Improve UI polish and user experience

### Notes
Frontend now supports full CRUD (create + update) for projects and work items, with filtering and search.