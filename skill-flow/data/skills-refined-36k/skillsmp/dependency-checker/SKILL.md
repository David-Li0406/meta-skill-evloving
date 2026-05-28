---
name: dependency-checker
description: Audits Python dependencies for security vulnerabilities and best practices. Use before PR or after adding dependencies.
version: 2.0.0
allowed-tools:
  - Read
  - Bash(pip, python)
  - Grep
plan_mode_required: false
trigger_keywords:
  - dependencies
  - requirements
  - vulnerabilities
  - outdated packages
  - audit dependencies
  - security audit
---

# Dependency Checker

**Mission**: Zero Known Vulnerabilities in production dependencies.

---

## Audit Results (Auto-Executed)

```
!`python .claude/skills/dependency-checker/scripts/check_deps.py 2>&1`
```

---

## Analysis

Based on the audit results above:

### If AUDIT PASSED ✅

```markdown
## ✅ Dependency Audit Passed

All dependencies are secure and properly pinned.
Safe to proceed with deployment.
```

### If AUDIT FAILED ❌

**Critical issues require immediate action:**

| Issue | Action |
|-------|--------|
| Vulnerability | Update to fixed version, test, redeploy |
| Conflict | Resolve version incompatibility |

**Fix Steps:**
1. `pip install package==fixed-version`
2. Update requirements.txt
3. `pytest tests/ -v`
4. `pip freeze > requirements.lock`

### If AUDIT WARNING ⚠️

**Non-blocking issues to address:**
- Outdated packages: Plan updates
- Format issues: Pin versions properly

---

## What It Checks

1. **Security Vulnerabilities** (pip-audit) → CRITICAL/HIGH block deployment
2. **Outdated Packages** (pip list --outdated) → Warning
3. **Format Validation** → All deps should use `==` pinning
4. **Dependency Conflicts** (pip check) → Blocks if conflicts exist

---

## Quick Commands

```bash
# Install audit tool
pip install pip-audit

# Run security audit
pip-audit -r requirements.txt

# Check outdated
pip list --outdated

# Check conflicts
pip check
```

For full command reference, see [policy.md](reference/policy.md)

---

## Safety Rules

### NEVER:
- Auto-update production dependencies without testing
- Ignore CRITICAL/HIGH vulnerabilities
- Deploy with known conflicts

### ALWAYS:
- Run full test suite after updates
- Update lock file: `pip freeze > requirements.lock`
- Document changes in changelog

---

## Integration

```
Add/update dependency → dependency-checker ✅ → commit → push → CI validates
```

**CI Enhancement**: Add pip-audit to `.github/workflows/` for automated checks.

---

## Success Metrics

- ✅ Zero CRITICAL/HIGH vulnerabilities
- ✅ All production deps pinned with `==`
- ✅ Lock file synchronized
- ✅ Audit completes in < 30 seconds
