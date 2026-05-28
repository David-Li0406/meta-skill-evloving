---
name: python-pytest-run-capture
description: Run Python pytest suites and capture reproducible evidence (command, environment, output) into agent-output artifacts. Use for QA verification, debugging, and pre-release confidence.
---

# Skill Instructions

## Inputs

- `PYTEST_ARGS` (string, optional): e.g. `-q`, `-k test_name`, `tests/unit`
- `OUT_DIR` (string, optional): output directory (default: `agent-output/qa/artifacts`)
- `STAMP` (string, optional): override timestamp (default: auto UTC timestamp)

## Procedure

```bash
set -euo pipefail

out_dir="${OUT_DIR:-agent-output/qa/artifacts}"
mkdir -p "$out_dir"

stamp="${STAMP:-$(date -u +%Y%m%dT%H%M%SZ)}"
args="${PYTEST_ARGS:-}"

# Capture environment context
{
  echo "timestamp_utc=$stamp"
  echo "cwd=$(pwd)"
  python --version 2>&1 || true
  python -c "import sys; print('sys.executable=', sys.executable)" 2>&1 || true
  python -c "import platform; print('platform=', platform.platform())" 2>&1 || true
  echo "PYTEST_ARGS=$args"
} > "$out_dir/pytest_env_$stamp.txt"

# Run pytest and capture output
set +e
python -m pytest $args > "$out_dir/pytest_out_$stamp.txt" 2>&1
rc=$?
set -e

echo "pytest_exit_code=$rc" | tee "$out_dir/pytest_rc_$stamp.txt"

# Optional: quick summary
sed -n '1,200p' "$out_dir/pytest_out_$stamp.txt" > "$out_dir/pytest_out_head_$stamp.txt" || true

echo "Wrote artifacts to: $out_dir"
exit $rc
```

## Acceptance Criteria

- Output directory contains `pytest_env_*.txt`, `pytest_out_*.txt`, and `pytest_rc_*.txt`.
- Exit code is non-zero on test failure (so pipelines/agents fail fast).

## Notes

- Prefer targeted runs first (e.g., `PYTEST_ARGS=tests/unit -q`) before running full suite.
- If your project uses a venv/poetry/conda, run pytest via the project’s preferred launcher.
