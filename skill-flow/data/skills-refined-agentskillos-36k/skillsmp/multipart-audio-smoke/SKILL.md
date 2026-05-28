---
name: multipart-audio-smoke
description: Smoke test an audio upload endpoint using multipart/form-data. Use for quick end-to-end validation of transcription pipelines.
---

# Skill Instructions

## Inputs

- `BASE_URL` (string): e.g. `http://localhost:8001`
- `PATH` (string): e.g. `/transcribe`
- `FILE` (string): e.g. `live_test_sample.wav`

## Procedure

```bash
set -euo pipefail

base_url="${BASE_URL:?BASE_URL is required}"
path="${PATH:?PATH is required}"
file="${FILE:?FILE is required}"

curl -sS -X POST "$base_url$path" \
  -F "audio=@$file" \
  -F "language=en" \
  | head -c 2000
```

## Acceptance Criteria

- HTTP 200
- Response indicates success and includes a recognized text field (schema varies per project)
