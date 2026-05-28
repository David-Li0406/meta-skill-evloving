---
name: oe-backend-startup-triage
description: Use this skill to quickly debug issues when the backend won't start, you encounter first request errors, or ports are stuck.
---

# Skill body

## Preferred startup path

1. Use the canonical dev script (port cleanup + key loading):
   - `./scripts/dev_server.sh start`

2. If the frontend is stuck (white page / endless spinner), clear zombie processes:
   - `kill -9 $(lsof -nP -iTCP:3000 -sTCP:LISTEN -t)`
   - `cd atelier-ai-frontend && npm run dev`

## If port 8000 is stuck

- Identify and kill listeners:
  - `lsof -nP -iTCP:8000 -sTCP:LISTEN`
  - `lsof -nP -tiTCP:8000 -sTCP:LISTEN | xargs kill -9`

## If the first request fails with “unexpected keyword argument …”

This is usually due to stale `.pyc` / `__pycache__` files from changed dataclasses.

1. Clear bytecode caches:
   - `find backend -name "*.pyc" -delete`
   - `find backend -type d -name "__pycache__" -exec rm -rf {} +`

2. Restart with bytecode disabled:
   - `export PYTHONDONTWRITEBYTECODE=1`
   - `./scripts/dev_server.sh start`

## If imports fail (ImportError / missing export)

1. Run the compile/import sanity gate:
   - `python3 scripts/verify_refactor.py`

2. If the failure is in a workflow wrapper, ensure the wrapper re-exports the referenced symbol (see `docs/guides/TEAM_GUIDE.md` for prior “missing export” regressions).