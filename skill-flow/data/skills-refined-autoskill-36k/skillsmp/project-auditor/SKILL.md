---
name: project-auditor
description: "Project health assessment process. Use when auditing project setup, evaluating technical debt, assessing codebase health, or reviewing project configuration. Also use when joining a new project, builds are slow or flaky, experiencing 'works on my machine' problems, security scans find issues, or dependencies are years out of date. Essential for dependency audits, CI/CD reviews, and project infrastructure evaluation."
---

# Project Auditor Skill

## Overview

A healthy project is one where developers can ship confidently. This skill guides systematic assessment of project health—configuration, dependencies, CI/CD, and technical debt.

**Core principle:** Audit to enable, not to blame. Find issues that slow the team down and prioritize fixes by impact.

## The Audit Process

### Phase 1: Quick Health Check

**Get a baseline in 5 minutes:**

1. **Check the Basics**
   - README exists and is useful?
   - Can you run the project in < 10 minutes?
   - Are there tests? Do they pass?

2. **Check Dependencies**
   ```bash
   npm outdated && npm audit    # Node
   pip list --outdated          # Python
   go list -m -u all            # Go
   ```

3. **Check CI/CD**
   - Pipeline exists?
   - Tests run on PR?
   - Main branch protected?

### Phase 2: Deep Assessment

**Systematic evaluation:**

1. **Configuration Completeness**
   - All required files present?
   - Linting configured and enforced?
   - Secrets properly managed?

2. **Dependency Health**
   - How many outdated?
   - Any with known vulnerabilities?
   - Any abandoned/unmaintained?

3. **Code Quality Indicators**
   - Test coverage?
   - Consistent code style?
   - Documentation coverage?

### Phase 3: Prioritized Report

**Findings that drive action:**

1. **Categorize by Impact**
   - Critical: Security, can't build/deploy
   - High: Slows development significantly
   - Medium: Causes friction
   - Low: Nice to fix

2. **Recommend Next Steps**
   - What to fix first?
   - Quick wins vs. larger efforts
   - Dependencies between fixes

## Red Flags - Critical Issues

### Security Critical

```
- Secrets in code or git history
- Dependencies with known CVEs
- No security scanning in CI
- Missing authentication on endpoints
- .env files committed
```

### Operational Critical

```
- Can't build from clean checkout
- No CI/CD pipeline
- Main branch accepts direct pushes
- No automated tests
- Missing LICENSE file
```

### Maintainability Critical

```
- No README or it's useless
- Dependencies 2+ major versions behind
- No linting or formatting rules
- Mix of conflicting patterns
- Circular dependencies
```

## Audit Checklist

### Configuration Files

| File | Status | Notes |
|------|--------|-------|
| README.md | ☐ | Useful quick start? |
| LICENSE | ☐ | Appropriate license? |
| .gitignore | ☐ | Covers all artifacts? |
| CI config | ☐ | Tests, lint, security? |
| Linter config | ☐ | Enforced in CI? |
| .env.example | ☐ | Documents all vars? |

### Dependency Health

| Check | Status | Notes |
|-------|--------|-------|
| Outdated count | ☐ | How many? |
| Vulnerable count | ☐ | npm audit / pip-audit |
| Lock file | ☐ | Committed? |
| Unused deps | ☐ | depcheck / pipdeptree |

### CI/CD Pipeline

| Check | Status | Notes |
|-------|--------|-------|
| Pipeline exists | ☐ | GH Actions, etc? |
| Tests run | ☐ | On every PR? |
| Linting | ☐ | Enforced? |
| Security scan | ☐ | Dependabot, etc? |
| Branch protection | ☐ | Reviews required? |

### Code Quality

| Check | Status | Notes |
|-------|--------|-------|
| Test coverage | ☐ | % covered? |
| Code style | ☐ | Consistent? |
| Documentation | ☐ | API docs? |
| Type coverage | ☐ | Types used? |

## Common Rationalizations - Don't Accept These

| Excuse | Reality |
|--------|---------|
| "We'll fix it after launch" | Post-launch is harder. Fix now. |
| "It's technical debt we know about" | Known debt still costs. Quantify it. |
| "Dependencies work fine" | Until they have a CVE. Update regularly. |
| "CI is too slow" | Slow CI > no CI. Then make it faster. |
| "Tests are flaky" | Flaky tests are worse than no tests. Fix or delete. |

## Audit Report Template

```markdown
# Project Audit: [Name]
Date: [Date]

## Executive Summary
- Overall Health: [Good/Fair/Poor]
- Critical Issues: [Count]
- Recommended Priority: [What to fix first]

## Findings

### Critical
1. [Issue]: [Impact] → [Recommendation]

### High
1. [Issue]: [Impact] → [Recommendation]

### Medium
1. [Issue]: [Impact] → [Recommendation]

## Metrics
- Dependencies: [X] total, [Y] outdated, [Z] vulnerable
- Test Coverage: [X]%
- CI Status: [Passing/Failing/None]

## Recommended Actions
1. [First priority - why it's first]
2. [Second priority]
3. [Third priority]
```

## Quick Audit Commands

```bash
# Node.js
npm outdated
npm audit
npx depcheck

# Python
pip list --outdated
pip-audit
pipdeptree

# Go
go list -m -u all
govulncheck ./...

# General
git log --oneline -20  # Recent activity
git shortlog -sn       # Contributors
wc -l **/*.ts          # Lines of code
```

## References

Detailed patterns and examples in `references/`:
- `project-checklist.md` - Comprehensive setup checklist
- `dependency-management.md` - Keeping deps healthy
- `cicd-patterns.md` - Pipeline best practices
