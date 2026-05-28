---
name: cpu-mode-assertions-torch
description: Assert CPU-only runtime inside a container using PyTorch (torch.cuda.is_available()==False) and optional env var checks. Use to prevent accidental GPU execution during CPU smoke tests.
---

# Skill Instructions

## Inputs

- `SERVICE_CONTAINER` (string): container name to exec into
- `CPU_DEVICE_ENV` (string, optional): env var to validate (e.g. `ASR_DEVICE`)
- `CPU_DEVICE_EXPECTED` (string, optional): expected value (e.g. `cpu`)

## Procedure

```bash
set -euo pipefail

service_container="${SERVICE_CONTAINER:?SERVICE_CONTAINER is required}"

# 1) Env assertion (optional)
if [ -n "${CPU_DEVICE_ENV:-}" ]; then
  docker exec "$service_container" printenv "$CPU_DEVICE_ENV"
fi

# 2) Runtime assertion (torch)
docker exec "$service_container" python - <<'PY'
import torch
print('torch_version=', torch.__version__)
print('torch_cuda_is_available=', torch.cuda.is_available())
print('torch_cuda_version=', getattr(torch.version, 'cuda', None))
PY
```

## Acceptance Criteria

- `torch_cuda_is_available` prints `False`
- If `CPU_DEVICE_ENV` is provided, its value equals `CPU_DEVICE_EXPECTED` (or `cpu` if you standardize it)

## Why

Prevents “silent GPU path” during CPU smoke testing (different behavior, heavier images, device-specific bugs).
