# Python best practices checklist (production)

## Project layout
- src/ layout
- tests/ exists and runs via pytest
- no dumping grounds (mega utils modules)

## Tooling
- uv.lock committed
- CI uses `uv sync --frozen`
- `uv run task lint_fix` exists and is used before commits

## Code quality
- typing at boundaries (public APIs, adapters)
- minimal essential docstrings
- deterministic tests

## Reliability
- logging via getLogger(__name__)
- no silent exception swallowing
- timeouts on external calls

## Security baseline
- no untrusted pickle
- careful subprocess usage
- secrets not in git
