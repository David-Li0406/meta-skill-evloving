---
name: ciphey-cli
description: "Run the Ciphey CLI to automatically decrypt/decode unknown ciphertext from a string or file. Prefer running via uv (local venv) and fall back to Docker when native install/import fails."
---

# Ciphey CLI (uv-first)

## One-shot (Direct Run)

- Run directly: `bash "<path-to-skill>/scripts/ciphey.sh" --text "<ciphertext>"`
- Or with a file: `bash "<path-to-skill>/scripts/ciphey.sh" --file "<path>"`
- Pass through any Ciphey flags (the wrapper forwards unknown args to Ciphey).

## Runner Preference (uv-first)

- Default mode is `auto`, which tries `uv` first and falls back to Docker.
- Force runners:
  - `CIPHEY_RUNNER_MODE=uv bash "<path-to-skill>/scripts/ciphey.sh" --text "..."`
  - `CIPHEY_RUNNER_MODE=docker bash "<path-to-skill>/scripts/ciphey.sh" --text "..."`
  - Or pass `--runner uv|docker|auto` to the wrapper script.

## Notes

- The script bootstraps `uv` (via the official install script) and creates a local venv at `scripts/.venv` when using the uv runner.
- Default runner is uv-first. If Ciphey cannot be installed on the current platform, the script falls back to Docker.
- Use only on content you are authorized to analyze.
