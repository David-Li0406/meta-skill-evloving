---
name: python-backend-fastapi
description: >
  FastAPI + Pydantic v2 backend workflow: implement/modify API endpoints with thin
  handlers + service layer, add pytest tests, manage idempotent Alembic migrations,
  and implement streaming ETL/parsers with invalid-row CSV logging. Use this skill
  when working on Python backend APIs, schema changes, or ingestion/parsing pipelines.
compatibility: >
  Python backend using FastAPI, Pydantic v2, Alembic, pytest. Intended for agent-driven
  coding workflows in Cursor.
metadata:
  author: janjaszczak
  version: "1.0"
---

# Python backend (FastAPI + Pydantic v2 + Alembic)

## Activation cues
Use this skill when the task involves:
1) new or modified FastAPI endpoints, routers, dependencies, middleware  
2) request/response validation, schema design, OpenAPI correctness (Pydantic v2)  
3) database schema changes (Alembic revisions)  
4) backend logging and request tracing  
5) ETL / parsers / import pipelines with memory constraints and “bad rows” reporting

## Operating principles (agent workflow)
1) Start with a short plan before editing code. Prefer file-path-specific steps and repository-aligned patterns.  
2) Ask up to 1–3 clarifying questions only if truly blocking.  
3) Prefer verifiable goals: tests, migrations, reproducible API calls, and deterministic outputs.  
4) For complex/high-risk changes, run an internal Chain-of-Verification (CoVe): draft → 3–5 verification questions → answer independently → revise; surface only final result + (optional) UNCERTAIN items and how to verify them.

## Standard implementation workflow

### 1) Context discovery (do not invent patterns)
- Locate existing routers, dependency injection conventions, error handling, and response schema patterns.
- Identify service layer boundaries (or create them if missing).
- Find existing migration conventions and logging format.

### 2) API contract first (Pydantic v2)
- Define/extend request & response models with Pydantic v2.
- Ensure OpenAPI reflects reality (status codes, response shapes, optional fields).
- Keep handlers thin: parse/validate, delegate to service, map service result to response.

**Definition of “thin handler”:**
- No business rules in the endpoint function beyond wiring + basic validation.
- No direct DB logic in the handler unless the codebase already standardizes it there.

### 3) Service layer + tests (pytest)
- Move business logic to a service module with unit tests.
- Prefer tests that encode behavior and edge cases (happy path, validation, not found, conflicts).
- Add/extend fixtures in line with repo conventions.

### 4) Dependency Injection (FastAPI Depends)
- Use `Depends` for DI and request-scoped dependencies.
- If a request-id is used in the project, propagate it through dependencies/services.

### 5) Alembic migrations (every schema change)
- Create a new revision for each schema change.
- Make migrations idempotent and safe:
  - avoid non-deterministic operations
  - provide both upgrade and downgrade
  - ensure ordering is correct with dependencies
- If the change is data-destructive, clearly annotate risk and required operator steps.

### 6) Logging (stdlib logging)
- Use Python stdlib `logging`.
- Include request id (if available) and key fields relevant to the operation.
- Avoid logging secrets/PII; log identifiers and high-level state transitions instead.

### 7) ETL / parsers (streaming, error CSV)
When implementing ingestion/parsing:
- Process input **file-by-file** (and ideally row-by-row) to avoid loading all data into memory.
- For invalid records:
  - write a CSV containing: `timestamp`, `file`, `line`, `error`, `original_row`
  - keep `original_row` as close to raw input as possible (avoid “fixing” it before logging)
- Logging must allow operators to reproduce and patch upstream data.

## Definition of done (backend changes)
A change is “done” only if:
1) endpoint behavior matches contract (schemas + status codes)  
2) tests exist and pass for new/changed logic  
3) migrations exist for schema changes (upgrade + downgrade)  
4) logging is present for operationally relevant paths  
5) for new endpoints: provide example `curl` or `httpie` calls + expected responses

## Examples (template snippets)

### Example: endpoint acceptance checklist
- Request model defined (Pydantic v2)
- Response model defined (Pydantic v2)
- Handler delegates to service
- Tests cover core behavior + edge case
- Example `curl` included in PR/plan notes

### Example: ETL error row
- timestamp: ISO-8601
- file: input filename
- line: input line number (1-based)
- error: short human-readable description
- original_row: raw row payload
