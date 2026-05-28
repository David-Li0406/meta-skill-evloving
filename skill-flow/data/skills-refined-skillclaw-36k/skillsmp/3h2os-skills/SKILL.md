---
name: 3h2os-skills
description: Automated marathon training coach skills/tools.
---

This skill defines the operational capabilities for the 3h2Os marathon training project. It is used to automate the feedback loop between the plan and actual execution.

## Training Operations

> **Infrastructure Note**: This project runs in Docker.
> - **Container**: Execute scripts inside the container: `docker exec running_app uv run [script_path]`.
> - **Orchestration**: Use `docker-compose` for managing services.
> - **Environment**: Ensure Docker Desktop is running before attempting operations.

### Fetch Actuals
Retrieves recent completed activities from Garmin/Strava sources and persists them to the local dataset.
**Note**: Automated background sync is deprecated in favor of user-initiated sync via the Web UI to improve security (limiting credential handling).
- **Trigger**: Web UI (Sync Button) or API call with Token.
- **Endpoint**: `POST /api/integrations/garmin/sync`
- **Inputs**: Garmin Token (Header `X-Garmin-Token`), Database
- **Outputs**: Updates `data/database.db` (Postgres/SQLite). Includes detailed metric splits and zone distribution.

### Reflect & Validate
The "Brain" of the operation. Compares executed runs against the plan. It enforces safety guardrails (15% volume cap, 80/20 intensity distribution) and creates adaptations for future weeks if necessary.
- **Script**: [`../../../backend/scripts/reflect_and_validate.py`](../../../backend/scripts/reflect_and_validate.py)
- **Command**: `cd backend && uv run scripts/reflect_and_validate.py`
- **Inputs**: `database.db` (Plan and Actuals)
- **Outputs**: Updates `database.db`, Logs validation warnings.

### Sync to Garmin
Pushes structured workouts from the JSON plan to the Garmin Connect Calendar for execution on the watch.
**Note**: Deprecated/Disabled pending UI integration for Token Auth.
- **Script**: [`../../../backend/scripts/sync_to_garmin.py`](../../../backend/scripts/sync_to_garmin.py)
- **Status**: Disabled.

### Update Weight
Updates the runner's current weight in the context profile, used for mechanics and fueling calculations.
- **Script**: [`../../../backend/scripts/update_weight.py`](../../../backend/scripts/update_weight.py)
- **Command**: `cd backend && uv run scripts/update_weight.py [KG]`
- **Inputs**: Weight in KG (float)
- **Outputs**: Updates `database.db`

---

## Deployment

### Build Static Site
Freezes the dynamic FastAPI application into a static HTML/JS bundle for hosting on GitHub Pages.
- **Script**: [`../../../backend/scripts/build_static.py`](../../../backend/scripts/build_static.py)
- **Command**: `cd backend && uv run scripts/build_static.py`
- **Outputs**: `index.html`, `dashboard.html` (and static assets)

### Run Dev Server
Starts the FastAPI backend for local development and UI testing.
- **Command**: `cd backend && uv run uvicorn app.main:app --reload`
- **Address**: `http://localhost:8000`
