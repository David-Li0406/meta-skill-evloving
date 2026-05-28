# Usage Example: security_audit

## Quick Execution
To scan the entire project for security issues:

```bash
uv run .agent/skills/security_audit/scripts/audit_runner.py
```

## What It Checks
1. **Secrets**: Regex patterns for GitHub tokens, AWS keys, Private Keys.
2. **Risky Files**: Binary files (`.exe`, `.dll`), exposed keys (`.pem`), and files > 50MB.
3. **Dependencies**: Integrity of Python packages installed via `uv`.

## Output Interpretation
- **PASS**: No issues detected.
- **FAIL**: Issues found. Check logs for details (exact file path).
