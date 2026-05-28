---
name: developing-backend-app
description: Develops or modifies the FastAPI backend in the @[app] directory. Use when user requests changes to APIs, services, data models, or core logic.
---

# Developing Backend App

## When to use this skill

- Adding new API endpoints.
- Modifying business logic (Services).
- Changing database interactions (Repositories).
- Updating data models (Pydantic/ORM).

## Structure

- Root: `app/`
- Entry Point: `app/main.py`
- API Router: `app/api/v1/api.py`
- Endpoints: `app/api/v1/endpoints/`
- Core Logic: `app/services/`
- Data Access: `app/repositories/` (if applicable)
- Models: `app/models/`
- Config: `app/core/config.py`

## Workflow rules

### 1. Architecture Layering

- **Models**: Defines data structure.
- **Repositories**: Handles database/storage I/O.
- **Services**: Contains business logic. Orchestrates repositories.
- **Endpoints**: Handles HTTP Request/Response. Calls Services.

### 2. Adding a New Endpoint

1.  **Define Model**: Create request/response Pydantic models in `app/models`.
2.  **Create Service**: Implement logic in `app/services/[domain]_service.py`.
3.  **Create Endpoint**: Create `app/api/v1/endpoints/[domain].py`.
    - Use `APIRouter`.
    - Inject Service dependencies.
4.  **Register Router**: Add the new router to `app/api/v1/api.py` to make it live.

### 3. Coding Standards

- Use Type Hints everywhere.
- Use `async def` for endpoints and I/O bound service methods.
- Use `app.core.config.settings` for configuration (env vars).
- Do not put business logic in endpoints.

### 4. Running Locally

- Run with `python main.py` or `uvicorn app.main:app --reload`.
- Swagger UI at `http://localhost:8000/docs`.

## Checklist for Changes

1. [ ] Defined Models.
2. [ ] Implemented Service Logic.
3. [ ] Implemented Endpoint.
4. [ ] Registered in `api_router` (`api.py`).
5. [ ] Verified text/swagger (`/docs`).
