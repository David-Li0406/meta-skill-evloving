---
name: security-scan
description: Scan for security vulnerabilities in dependencies, code patterns, and secrets. Uses project-documented tooling where available.
---

# Security Scan Skill

Scan the codebase for security issues across three categories:
1. **Dependency vulnerabilities** — Known CVEs in packages
2. **Static analysis** — Insecure code patterns (per project tooling)
3. **Secrets detection** — API keys, passwords, tokens in code

## When This Skill Runs

- Automatically during `/phase-checkpoint`
- On-demand via `/security-scan`
- Optionally during `/verify-task` for security-critical tasks

## Workflow Overview

```
1. Discover security tooling from project docs
2. Run dependency audit (if configured)
3. Run secrets detection
4. Run static analysis (if configured)
5. Aggregate and deduplicate findings
6. Present issues with severity and fix suggestions
7. Offer to apply fixes where possible
```

## Step 1: Discover Project Security Tooling

Read project documentation and task runners to find the correct commands:
- `README.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `Makefile`
- `Taskfile.yml`
- `justfile`
- Any security or build scripts under `scripts/`

Extract any documented commands for:
- Dependency auditing
- Static analysis / security scanning
- Secrets detection (if the project has a preferred tool)

If nothing is documented, ask the human to provide the correct commands.

## Step 2: Dependency Audit

- If a dependency audit command is documented or provided, run it.
- If no command is available, mark this check as SKIPPED and note it in the
  report.

## Step 3: Secrets Detection (Default)

Run a pattern-based secrets scan (stack-agnostic) unless the project documents
its own secrets tool. If a project-specific tool exists, use it instead.

### Patterns to Detect

| Pattern | Regex | Severity |
|---------|-------|----------|
| AWS Access Key | `AKIA[0-9A-Z]{16}` | CRITICAL |
| AWS Secret Key | `(?i)aws_secret_access_key\s*=\s*['"][^'"]+['"]` | CRITICAL |
| GitHub Token | `ghp_[a-zA-Z0-9]{36}` | CRITICAL |
| GitHub Token (old) | `github_pat_[a-zA-Z0-9]{22}_[a-zA-Z0-9]{59}` | CRITICAL |
| Generic API Key | `(?i)(api[_-]?key|apikey)\s*[:=]\s*['"][a-zA-Z0-9]{20,}['"]` | HIGH |
| Generic Secret | `(?i)(secret|password|passwd|pwd)\s*[:=]\s*['"][^'"]{8,}['"]` | HIGH |
| Private Key | `-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----` | CRITICAL |
| JWT Token | `eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*` | HIGH |
| Slack Token | `xox[baprs]-[0-9a-zA-Z]{10,48}` | HIGH |
| Stripe Key | `sk_live_[0-9a-zA-Z]{24}` | CRITICAL |

### Directories to Skip

- `node_modules/`
- `.git/`
- `vendor/`
- `venv/`, `.venv/`, `env/`
- `dist/`, `build/`
- `*.min.js`, `*.bundle.js`
- Binary files

## Step 4: Static Analysis

- If a static analysis or security scanning command is documented or provided,
  run it.
- If no command is available, mark this check as SKIPPED and note it in the
  report.

## Step 5: Aggregate Findings

Collect all findings into a unified format:

```
SECURITY SCAN RESULTS
=====================

Scanned: {timestamp}
Checks Run: Dependencies | Secrets | Static Analysis

CRITICAL (N)
------------
[issue details]

HIGH (N)
--------
[issue details]

MEDIUM (N)
----------
[issue details]

LOW (N)
-------
[issue details]

Summary: {N} critical, {N} high, {N} medium, {N} low
```

## Step 6: Present Issues

For CRITICAL and HIGH issues, present interactively with resolution options.
If a fix command is documented, offer it as the primary option.

## Step 7: Apply Fixes

Apply fixes based on user choices:
- Use project-documented fix commands when available
- Otherwise, propose manual code changes and confirm before editing

## Output Format

### When called from /phase-checkpoint

Return a structured result:

```
Security Scan: PASSED | FAILED | PASSED WITH NOTES

Issues: X critical, Y high, Z medium
Fixed: N issues
Skipped: M checks (documented)

Blocking: Yes/No
```

### When called standalone

Show full report with all findings and options.

## Severity Definitions

| Severity | Meaning | Action |
|----------|---------|--------|
| CRITICAL | Exploitable vulnerability, exposed secrets | BLOCKS checkpoint |
| HIGH | Significant security risk | BLOCKS checkpoint |
| MEDIUM | Should be addressed | Note, doesn't block |
| LOW | Minor issue or informational | Note only |

## Tool Installation Notes

If required tools are missing, instruct the user to install them based on the
project's documentation or security policy.

## Example Invocations

```bash
/security-scan              # Full scan
/security-scan --deps       # Dependencies only
/security-scan --secrets    # Secrets detection only
/security-scan --code       # Static analysis only
/security-scan --fix        # Auto-fix where possible
```
