---
name: verify-pipeline
description: |
  Run project verification checks using standard Makefile targets.
  Use when user says "verify pipeline", "check my work", "run tests", or "validate changes".
  Wraps `make verify-pipeline` (E2E), `make verify-analysis` (Logic), or `make verify-all`.
  Ensures environment constraints (e.g. Railway Shell) are met.
tags: [workflow, testing, verification, makefile, railway]
allowed-tools:
  - Bash(make verify-*)
  - Bash(railway run *)
  - Bash(railway:*)
  - Bash(curl:*)
  - Read
---

# Verify Pipeline

Standardized verification workflow for Affordabot and V3 projects.

## Purpose

Run standardized verification scripts defined in the project `Makefile`.
Ensures consistency between local dev, CI, and agent workflows.

## When to Use This Skill

**Trigger phrases:**
- "verify pipeline"
- "check my work"
- "run verification"
- "test the changes"
- "did I break anything?"

**Use when:**
- After implementing a features (especially Phase 5 search/RAG)
- Before creating a PR
- When debugging "State of the World"

## Workflow

### 1. Identify Verification Targets

Check `Makefile` for available `verify-*` targets:

```bash
grep "^verify-" Makefile
```

Common targets:
- `verify-pipeline`: E2E RAG Pipeline (requires DB)
- `verify-analysis`: Legislation Logic (Integration)
- `verify-auth`: Auth Config
- `verify-all`: All of the above

### 2. Check Environment

**Railway Projects:**

If the project uses Railway (e.g., `RAILWAY_ENV.md` or `railway.toml` exists):

1. **Validate Railway environment** (optional but recommended):
   ```bash
   ~/.agent/skills/devops-dx/scripts/validate_railway_env.sh
   ```
   This checks:
   - Project linkage
   - Service configuration
   - Staged (unapplied) changes
   - Required environment variables

2. **Ensure Railway Shell or `railway run` is used:**
   Commands should be run in `railway shell` or using `railway run`.
   *Note: The Makefile usually enforces this, but the agent should be aware.*

### 3. Run Verification

**Default (E2E):**
```bash
make verify-pipeline
```

**Comprehensive:**
```bash
make verify-all
```

**Specific Component:**
```bash
make verify-analysis
# or
make verify-auth
```

### 4. Report Results

**Success:**
```
✅ Verification Passed!
   - Pipeline: OK
   - Analysis: OK
```

**Failure:**
```
❌ Verification Failed:
   - Pipeline: DB Connection Error
   
   Tip: Check your Railway Shell connection or .env variables.
```

## Best Practices

- **Always run from root** (where Makefile is).
- **Prefer `make` targets** over direct python scripts (`python scripts/...`).
- **Read output** to catch specific failures (DB vs Logic).

## Related Skills

- **lint-check**: Run before verification to catch syntax errors.
- **sync-feature-branch**: Run verification before syncing/committing.
