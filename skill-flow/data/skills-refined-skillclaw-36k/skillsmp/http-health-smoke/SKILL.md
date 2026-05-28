---
name: http-health-smoke
description: Run quick HTTP health/readiness smoke checks against one or more endpoints. Use to validate a service is up before running deeper E2E tests.
---

# Skill Instructions

## Inputs

- `BASE_URL` (string): e.g. `http://localhost:8001`
- `PATHS` (string): space-separated paths, e.g. `/health/ /health/ready /health/live /health/models`

## Procedure

```bash
set -euo pipefail

base_url="${BASE_URL:?BASE_URL is required}"
paths="${PATHS:?PATHS is required}"

for p in $paths; do
  curl -sS -f "$base_url$p" | head
done
```

## Acceptance Criteria

- All requests return HTTP 200
- Responses are parseable/expected format for the project (often JSON)
