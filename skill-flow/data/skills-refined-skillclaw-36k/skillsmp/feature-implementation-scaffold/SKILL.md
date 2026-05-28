---
name: Feature Implementation Scaffold
description: A comprehensive full-stack checklist for implementing new features consistently and safely.
---

# Feature Implementation Skill

## Purpose
To provide a structured, step-by-step workflow for adding new features, ensuring all layers (Database, Backend, Frontend) are implemented correctly and tested.

## Phase 1: Backend Implementation

1.  **Model**: Create/Update `backend/models/<entity>.py`.
    -   *If changed*: Use the **Database Migration** skill.
2.  **Repository**: Create/Update `backend/repositories/<entity>_repository.py`.
    -   Implement CRUD operations.
    -   **Add Unit Tests**: `backend/tests/unit/repositories/test_<entity>_repository.py`.
3.  **Service**: Create/Update `backend/services/<entity>_service.py` (Optional, if business logic is complex).
4.  **Router**: Create/Update `backend/routers/v1/<entity>.py`.
    -   Define Pydantic schemas (Request/Response) with explicit types.
    -   **Add Unit Tests**: `backend/tests/unit/routers/test_<entity>_router.py`.
5.  **Verify Backend**:
    -   `backend/.venv/bin/ruff check backend`
    -   `backend/.venv/bin/mypy backend`
    -   `backend/.venv/bin/pytest backend`
6.  **Commit**: `feat(backend): implement <entity> logic`

## Phase 2: Frontend Implementation

1.  **Types**: Define interfaces in `frontend/src/types` or co-located with components.
2.  **API Hook**: Create `frontend/src/hooks/queries/use<Entity>Query.ts`.
    -   Use TanStack Query v5 conventions.
3.  **UI Component**: Create `frontend/src/components/<Entity>/*.tsx`.
    -   Use Tailwind CSS v4.
4.  **Route**: Create `frontend/src/routes/<path>.tsx`.
5.  **Verify Frontend**:
    -   `npm run validate` (in `frontend/`)
    -   `npm test` (in `frontend/`)
6.  **Commit**: `feat(frontend): add <entity> ui`

## Phase 3: Push

Use the **Safe Push** skill to push your commits.
