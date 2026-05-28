---
name: docker-logs-snapshot
description: Capture a quick, reproducible snapshot of Docker/Compose logs and container state for debugging. Use when smoke tests fail or you need attachable evidence.
---

# Skill Instructions

## Inputs

- `SERVICE_CONTAINER` (string, optional): container to snapshot (e.g. `speech-recognition-service`)
- `COMPOSE_FILES` (string, optional): compose flags (e.g. `-f docker-compose.yml -f docker-compose.gpu.yml`)
- `LOGS_TAIL` (string/int, optional): how many lines (default: `500`)
- `OUT_DIR` (string, optional): output directory (default: `agent-output/live-testing/artifacts`)

## Procedure

```bash
set -euo pipefail

out_dir="${OUT_DIR:-agent-output/live-testing/artifacts}"
logs_tail="${LOGS_TAIL:-500}"
mkdir -p "$out_dir"

stamp="$(date -u +%Y%m%dT%H%M%SZ)"

# 1) Basic inventory
{
  echo "timestamp_utc=$stamp"
  echo "cwd=$(pwd)"
  docker version || true
  docker compose version || true
  echo "---"
  docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}' || true
} > "$out_dir/docker_snapshot_$stamp.txt"

# 2) Compose status (if provided)
if [ -n "${COMPOSE_FILES:-}" ]; then
  docker compose $COMPOSE_FILES ps > "$out_dir/compose_ps_$stamp.txt" || true
fi

# 3) Container-focused logs + inspect
if [ -n "${SERVICE_CONTAINER:-}" ]; then
  docker logs --tail "$logs_tail" "$SERVICE_CONTAINER" > "$out_dir/${SERVICE_CONTAINER}_logs_$stamp.txt" || true
  docker inspect "$SERVICE_CONTAINER" > "$out_dir/${SERVICE_CONTAINER}_inspect_$stamp.json" || true
fi

# 4) Optional: all compose logs (can be noisy)
if [ -n "${COMPOSE_FILES:-}" ]; then
  docker compose $COMPOSE_FILES logs --no-color --tail "$logs_tail" > "$out_dir/compose_logs_$stamp.txt" || true
fi

echo "Wrote artifacts to: $out_dir"
```

## Acceptance Criteria

- Output directory contains at least:
  - `docker_snapshot_<timestamp>.txt`
  - and (if `SERVICE_CONTAINER` set) `<service>_logs_<timestamp>.txt` and `<service>_inspect_<timestamp>.json`

## Notes

- Do not paste secrets from logs into chat; attach files or summarize.
- Prefer `--tail` to keep snapshots small and reproducible.
