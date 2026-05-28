---
name: security-checker
description: Validates that no secrets or sensitive data are being committed. Use before commit or PR creation.
version: 2.0.0
allowed-tools:
  - Read
  - Bash(git, python)
  - Grep
plan_mode_required: false
trigger_keywords:
  - security
  - secrets
  - commit
  - before commit
  - check secrets
---

# Security Checker

**Mission**: Zero Secrets Committed - this is a **PUBLIC repository**.

---

## Security Scan Results (Auto-Executed)

```
!`python .claude/skills/security-checker/scripts/scan_secrets.py 2>&1`
```

---

## Analysis

Based on the scan results above:

### If SCAN PASSED ✅

```markdown
## ✅ Security Check Passed

Safe to commit. No secrets detected in staged changes.
```

### If SECRETS DETECTED ❌

For each finding:

| Severity | Action |
|----------|--------|
| CRITICAL | **BLOCK** - Must fix before commit |
| HIGH | **BLOCK** - Likely real secret |

**Fix Steps:**
1. Unstage: `git reset HEAD <file>`
2. Remove secret from code
3. Use SecretManager: `manager.get_secret("SECRET-NAME")`
4. Re-stage and scan again

---

## What It Scans

**Secret Patterns:**
- AWS Keys (AKIA...)
- GitHub PATs (ghp_...)
- Anthropic/OpenAI API keys
- JWT tokens, private keys
- Database URLs with passwords

**Forbidden Files:**
- `.env*` files
- `*credentials*.json`
- `*.pem`, `*.p12` keys

For full pattern list, see [patterns.md](reference/patterns.md)

---

## Safety Rules (CRITICAL)

### NEVER:
- Print or log secret values
- Allow "temporary" commits with secrets
- Trust obfuscation (base64, etc.)

### ALWAYS:
- Block commits with detected secrets
- Err on side of caution (false positive > false negative)
- Suggest SecretManager usage

---

## False Positives

The scanner ignores:
- Files in `tests/` or `docs/` directories
- Lines with: `example`, `placeholder`, `fake`, `test`
- Prefixes: `FAKE_`, `TEST_`, `EXAMPLE_`

If legitimate code blocked, check [patterns.md](reference/patterns.md)

---

## Integration

```
Staged changes → security-checker ✅ → commit → push → CI validates
```

**First line of defense** - CI (GitLeaks) is the second.

---

## If Secret Already Pushed

1. **Assume compromised** - act immediately
2. Rotate the secret in GCP Secret Manager
3. Never try git rebase to hide (history persists)
4. Document in incident report

---

## Success Metrics

- ✅ Zero secrets in repository history
- ✅ Scan completes in < 3 seconds
- ✅ Clear remediation guidance
- ✅ Low false positive rate (< 5%)
