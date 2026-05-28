---
name: pre-commit-security-audit
description: Use this skill to set up pre-commit hooks for code quality checks and security audits, including secret scanning with GitLeaks.
---

# Skill body

## Workflow

### 1. Setup Pre-commit Hooks

Ensure that pre-commit hooks are configured in your project. If not, set them up.

#### Detection Steps

1. Check if the `.husky/` directory exists.
2. Check if the `.husky/pre-commit` file contains the necessary GitLeaks command.

#### Setup Steps (if GitLeaks is missing)

If the `.husky/` directory does not exist, initialize it:
```bash
npx husky init
```

Add GitLeaks to the `.husky/pre-commit` file before any lint-staged command:
```bash
gitleaks protect --staged --verbose
```

Example `.husky/pre-commit` file:
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Secrets detection - fail fast if secrets found
gitleaks protect --staged --verbose

# Lint staged files
npx lint-staged
```

If the pre-commit file already exists, insert the GitLeaks line before `npx lint-staged`.

### 2. Code Security Audit

After ensuring GitLeaks is configured, run a security audit on the codebase:

```
Use the Task tool with subagent_type: security-auditor to run a security audit.
Focus on OWASP Top 10 vulnerabilities, authentication issues, and data protection.
```

### 3. Secret Scanning

To scan for secrets in the codebase, ensure that the `.gitleaks.toml` configuration file is set up. This file manages the rules for secret detection.

#### Handling False Positives

To ignore false positives, add path patterns to the `allowlist` section in the `.gitleaks.toml` file.

### 4. Retrospective Git History Scan (Optional)

If the user passes the `--scan-history` argument, run a history scan for legacy projects:

```bash
gitleaks detect --source . --verbose
```

Report any secrets found in git history with:
- File path and line number
- Commit where the secret was introduced
- Type of secret detected
- Remediation steps (rotate the secret, use git-filter-repo to remove from history)

## Output Format

1. **GitLeaks Setup Status**: Whether hooks were already configured or newly set up.
2. **Security Audit Findings**: Results from the security-auditor agent.
3. **History Scan Results** (if `--scan-history`): Any secrets found in git history.

## Assumptions

- GitLeaks is already installed on the system (`brew install gitleaks` or equivalent).
- Target projects use Husky + lint-staged (JS/TS stack).