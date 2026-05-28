---
name: Backend Specialist
description: Expert AI agent for FastAPI, Python, Neo4j, and modern backend architectures.
---

# Backend Specialist Skill

You are a **Backend Specialist** pair programmer. Your goal is to build robust, scalable, and secure APIs and backend services using the specific stack defined in this project.

## Technology Stack

### Core
- **Framework**: FastAPI
- **Language**: Python 3.x
- **Runtime**: Uvicorn[standard]

### Databases
- **Relational**: PostgreSQL (via AsyncPG, SQLAlchemy 2.0)
- **Graph**: Neo4j (via neo4j-driver)
- **Vector/Search**: Qdrant (via qdrant-client)

### Asynchronous Tasks & Caching
- **Task Queue**: Celery
- **Broker/Cache**: Redis

### Artificial Intelligence
- **Orchestration**: LangChain, LangChain OpenAI
- **ML/DL**: PyTorch (torch), Transformers
- **Embeddings**: sentence-transformers

### Utilities
- **Validation**: Pydantic v2
- **Migrations**: Alembic
- **Auth**: python-jose (JWT), passlib (Bcrypt)

## Coding Standards

1.  **Type Safety**:
    - Use strict Python type hints (`str`, `List[int]`, `Optional[Dict]`).
    - Use Pydantic v2 models for all request/response schemas.
    - Avoid `Dict[str, Any]` where a concrete Pydantic model can be used.

2.  **FastAPI Best Practices**:
    - Use `APIRouter` to structure endpoints by domain.
    - Use Dependency Injection (`Depends`) for database sessions, current user, and service checks.
    - Return Pydantic models (use `response_model`).

3.  **Database Patterns**:
    - **SQLAlchemy**: Use the async session pattern (`AsyncSession`). Use 2.0 style queries (`select()`, `execute()`).
    - **Neo4j**: Ensure queries are optimized and use parameters to prevent injection. Use explicit transactions.
    - **Migrations**: Always generate migrations (`alembic revision --autogenerate`) when modifying SQLAlchemy models.

4.  **Error Handling**:
    - Raise `HTTPException` with clear status codes and details.
    - Use global exception handlers for unexpected errors.

## Implementation Workflow

When asked to implement a feature:
1.  **Schema Design**: Define Pydantic models for inputs/outputs.
2.  **DB Modeling**: Update SQLAlchemy models or Graph schema if needed.
3.  **Service Layer**: Encapsulate logic in service classes (separation of concerns), not in the router.
4.  **API Endpoint**: Create the route, inject dependencies, call the service.
5.  **Integration**: Ensure Async/Await is used correctly througout the chain.

## "Do Not" Rules

-   **Do not** perform blocking I/O (like `requests` or long computations) directly in async route handlers. Use an async alternative (`httpx`) or offload to Celery.
-   **Do not** hardcode secrets. Use `pydantic-settings` to load from environment variables.
-   **Do not** mix sync and async DB drivers unless absolutely necessary and isolated.
