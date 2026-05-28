# FastAPI Notes (reference)

- Prefer structuring bigger applications with APIRouter and multiple files (keep endpoints thin; move logic to services).
- Prefer lifespan for startup/shutdown resources (clients, pools).
- Use pydantic-settings for configuration, and load from `.env` in dev.
- Install FastAPI with `fastapi[standard]` for the common recommended extras.
