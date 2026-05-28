---
name: security-and-pre-commit-setup
description: Use this skill when setting up pre-commit hooks for code quality checks and running security audits with GitLeaks.
---

# Body of the merged SKILL.md

You are a security engineer setting up pre-commit hooks and running security audits.

## Workflow

### 1. Setup Pre-commit Hooks

Ensure that pre-commit hooks are configured in the project. If not, set them up.

#### Detection Steps

1. Check if the `.husky/` directory exists.
2. Check if the `.husky/pre-commit` file contains the necessary commands for GitLeaks.

#### Setup Steps (if hooks are missing)

If the `.husky/` directory does not exist:
```bash
npx husky init
```

Add GitLeaks to the `.husky/pre-commit` file before any lint-staged command:
```bash
gitleaks protect --staged --verbose
```

Example `.husky/pre-commit` with lint-staged:
```bash
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Secrets detection - fail fast if secrets found
gitleaks protect --staged --verbose

# Lint staged files
npx lint-staged
```

If the pre-commit file already exists, insert the GitLeaks line before `npx lint-staged`.

### 2. Code Quality Checks

Utilize the pre-commit framework to run basic code quality checks, such as removing whitespace and ensuring end-of-file newlines. After cloning the repository, initialize the pre-commit hooks:
```bash
make pre-commit-init
```

To run checks on all files manually:
```bash
make pre-commit-run
```

### 3. Code Security Audit

After ensuring GitLeaks is configured, spawn the security-auditor agent to analyze the codebase:
```
Use the Task tool with subagent_type: security-auditor to run a security audit on the codebase.
Focus on OWASP Top 10 vulnerabilities, authentication issues, and data protection.
```

### 4. Retrospective Git History Scan (Optional)

Run this step only if the user passes the `--scan-history` argument. This is for legacy projects being onboarded to GitLeaks:
```bash
gitleaks detect --source . --verbose
```

Report any secrets found in git history with:
- File path and line number
- Commit where the secret was introduced
- Type of secret detected
- Remediation steps (rotate the secret, use git-filter-repo to remove from history)

## Output Format

1. **Pre-commit Setup Status**: Whether hooks were already configured or newly set up.
2. **Security Audit Findings**: Results from the security-auditor agent.
3. **History Scan Results** (if `--scan-history`): Any secrets found in git history.

## Assumptions

- GitLeaks is already installed on the system (`brew install gitleaks` or equivalent).
- Target projects use Husky + lint-staged (JS/TS stack).
- The gitleaks configuration is managed in the `.gitleaks.toml` file, with basic secret detection rules enabled.

### Handling False Positives

To ignore false positives, add path patterns to the `allowlist` section in the `.gitleaks.toml` file.