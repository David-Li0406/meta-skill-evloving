---
name: compose-bringup
description: Bring up a Docker Compose stack reliably and verify basic service/container status. Use for local smoke tests, live testing, and staging-like bring-up.
---

# Skill Instructions

## Inputs

- `COMPOSE_FILES` (string): compose flags, e.g. `-f docker-compose.yml` or `-f docker-compose.yml -f docker-compose.gpu.yml`
- `BUILD` (string/bool): when set (non-empty), include `--build`

## Procedure

```bash
set -euo pipefail

compose_files="${COMPOSE_FILES:-}"
build_flag=""
if [ -n "${BUILD:-}" ]; then
  build_flag="--build"
fi

# Bring up
if [ -n "$compose_files" ]; then
  docker compose $compose_files up -d $build_flag
else
  docker compose up -d $build_flag
fi

# Inspect status
if [ -n "$compose_files" ]; then
  docker compose $compose_files ps
else
  docker compose ps
fi
```

## Acceptance Criteria

- `docker compose ... ps` shows expected services are `running` / `healthy` (if healthchecks exist)

## Notes

- Use `docker-compose.yml` alone for CPU-only runs.
- Add an override file (e.g. `docker-compose.gpu.yml`) only when you explicitly want GPU.
