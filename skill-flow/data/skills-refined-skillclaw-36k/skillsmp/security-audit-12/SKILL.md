---
name: security_audit
description: Security scan for secrets, risky files, and vulnerable dependencies.
version: 1.0.0 (Divine)
author: Antigravity
---

# Operational Instructions

This skill executes a static security audit on the project. It identifies dangerous files, exposed credentials, and broken dependencies.

## Trigger
- **Pre-Commit**: Before uploading sensitive code.
- **Refactor**: When touching configuration files.
- **On-Demand**: Explicit request "Verify security".

## Inputs
- **Target Logic**: Directory to scan (default: `.`).
- **Exclude Patterns**: Files/Folders to ignore (e.g., `.git`, `.venv`, `node_modules`).

## Steps
1. **Secret Scanning**: Search for Regex patterns (AWS, GitHub, Generic Keys) in tracked files.
2. **Risky Files Audit**: Search for prohibited extensions (`.exe`, `.p12`, `.key`) and giant files (>50MB).
3. **Dependency Check**: Run `uv pip check` to verify Python environment consistency.
4. **Reporting**: Generate JSON/Markdown output with PASS/FAIL status for each check.

## Outputs
- **Console**: Colored log with immediate result.
- **Report**: List of violated files (if FAIL).

## Fail-Fast
- If **Confirmed Secrets** (High Confidence) are found, the audit FAILS and requires manual intervention.

## Suggested Commands
```bash
uv run .agent/skills/security_audit/scripts/audit_runner.py
```
