---
name: Database Migration
description: How to safely create, apply, and verify database migrations using Alembic.
---

# Database Migration Skill

## Purpose
Use this skill when modifying the database schema (Models) in `backend/models/*.py`. It ensures migrations are generated, inspected, and applied safely.

## Workflow

### 1. Create Migration (Local)

1.  **Modify the Model**: Ensure your changes in `backend/models/*.py` are saved.
2.  **Generate Migration**:
    Run the following command:
    ```bash
    cd backend && .venv/bin/alembic revision --autogenerate -m "<describe_your_change>"
    ```
3.  **Review the file**: 
    -   Locate the new file in `backend/alembic/versions/`.
    -   **CRITICAL**: Read the file to ensure it ONLY contains the intended changes. If it drops tables or columns unexpectedly, ABORT and investigate.

### 2. Apply Migration (Local)

1.  **Upgrade Database**:
    ```bash
    cd backend && .venv/bin/alembic upgrade head
    ```
2.  **Verify**: 
    -   Check if the changes are reflected in the database (e.g., table created, column added).
    -   You can use `psql` or run a test script if needed.

### 3. Commit Strategy

Migrations should be their own atomic commit or grouped with the model change.

```bash
git add backend/alembic/versions/
git commit -m "chore(db): add migration for <feature>"
```
