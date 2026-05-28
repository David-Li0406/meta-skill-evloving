---
name: hlab-executor
description: Converts an approved spec into production-grade bash when implementation is needed; use it after planning to build idempotent executors. Output is code changes plus a summary of commands, diffs, and tests executed.
metadata:
  version: "2.0"
  style: "Defensive Bash"
---

# HLab Executor Skill

## Coding Standards (Strict Enforcement)
1. **Header**: All scripts must start with `#!/usr/bin/env bash` and `set -euo pipefail`.
2. **Variables**: All variables must be quoted: `"${VAR}"`.
3. **Paths**: Use `"${REPO_ROOT}/..."`. Never rely on relative `cd`.
4. **Logging**:
   - **Wizard**: Use `echo` for user prompts.
   - **Executor**: Use `log_info`/`log_error` (from `lib/common.sh`) which writes to `/var/log/horizon.log`. **DO NOT** spam the user's screen with `apt-get` output.
5. **Idempotency**: "Install OLS" script must run successfully even if OLS is already installed (check before install).

## Prohibitions
- **NO `read` commands in Executors**. If you need input, assume it's in the environment variable sourced from the Wizard.
- **NO `curl | bash`**. All downloads must have a checksum verification or use apt/yum.
- **NO `sudo` inside scripts**. Check for `EUID==0` at the start.

## Integration
- Always `source "${REPO_ROOT}/lib/common.sh"` at the beginning.
- If a "Pro" feature hook is defined in the Spec, add `try_load_module "pro/seo_optimizer"` logic.
