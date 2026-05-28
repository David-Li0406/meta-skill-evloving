---
name: app-versioning
description: Guide to managing application versions and deployment releases.
---
# App Versioning Skill

## 1. The Versioning Strategy
Simple Platform uses **Semantic Versioning (SemVer)**: `MAJOR.MINOR.PATCH` (e.g., `1.0.0`, `2.1.5`).

*   **MAJOR:** Breaking changes (e.g., changing a data type, removing a field).
*   **MINOR:** New features (backward compatible) (e.g., new table, new field).
*   **Pre-Release:** `MAJOR.MINOR.PATCH-ENV.COUNTER` (e.g., `1.1.0-dev.1`, `1.1.0-staging.5`).

## 2. Defining Version in SCL
The source of truth is `apps/<app>/app.scl`.

```scl
id com.mycompany.crm
version 1.2.0  # <--- THIS LINE
display_name "CRM"
```

## 3. Deploying with Version Bumps
The CLI manages versions automatically based on the target environment (`--env`).

### A. Starting a New Cycle (Prod -> Dev)
When you have a stable version (e.g., `1.0.0`) and start new work, you **MUST** provide `--bump`.
```bash
# Start work on next patch
simple deploy com.mycompany.crm --env dev --bump patch
# Result: 1.0.1-dev.1
```

### B. Iterating (Dev -> Dev)
When iterating in a non-prod environment, the CLI **auto-increments** the counter. No flag needed.
```bash
simple deploy com.mycompany.crm --env dev
# Result: 1.0.1-dev.2 -> 1.0.1-dev.3
```

### C. Promoting (Dev -> Staging -> Prod)
Moving between environments handles the suffixes automatically.
```bash
# Promote to Staging
simple deploy com.mycompany.crm --env staging
# Result: 1.0.1-staging.1

# Release to Prod
simple deploy com.mycompany.crm --env prod
# Result: 1.0.1 (Stable)
```

## 4. Best Practices
1.  **Always Forward:** Versions must strictly increase. There is **NO** concept of rollback.
2.  **Forward Rollback:** To revert a bad deployment, revert the code in git and deploy a **new higher version**.
3.  **Sync:** Ensure `app.scl` is committed to git after a deployment, as the CLI updates it.
