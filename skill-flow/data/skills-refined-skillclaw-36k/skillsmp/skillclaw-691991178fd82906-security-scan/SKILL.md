---
name: security-scan
description: Use this skill to scan for security vulnerabilities in your codebase, including dependencies, insecure code patterns, and sensitive information.
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
- If no command is available, mark this check as SKIPPED and note it in the report.

## Step 3: Secrets Detection (Default)

Run a pattern-based secrets scan (stack-agnostic) unless the project documents its own secrets tool. If a project-specific tool exists, use it instead.

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
| Slack Token | `xoxb-[0-9]{12}-[0-9]{12}-[0-9]{24}-[a-zA-Z0-9]{16}` | CRITICAL |