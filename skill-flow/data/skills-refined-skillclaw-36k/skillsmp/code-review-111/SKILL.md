---
name: code-review
description: Review code for best practices. Enforces universal rules plus language-specific rules for TypeScript and Python. Use when reviewing PRs, code changes, or auditing code quality.
allowed-tools: Read, Glob, Grep, Bash
argument-hint: [--staged | --files=<paths> | --all] [--inline | --report | --beads] [--lang=typescript|python]
---

# Code Review

Review code against best practices with automatic language detection.

## Arguments

Parse `$ARGUMENTS` for:

| Flag | Default | Description |
|------|---------|-------------|
| `--staged` | Yes (if no scope given) | Review staged git changes |
| `--files=<paths>` | - | Review specific files or directories |
| `--all` | - | Review entire codebase |
| `--inline` | Yes (if no output given) | Show findings in conversation |
| `--report` | - | Generate `code-review-report.md` |
| `--beads` | - | Create beads issues for findings |
| `--lang=<lang>` | Auto-detect | Force language: `typescript` or `python` |

## Workflow

### Step 1: Determine Scope

```bash
# If --staged or no scope specified:
git diff --cached --name-only

# If --files=<paths>:
# Use provided paths directly

# If --all:
# Scan entire codebase (exclude node_modules, .git, __pycache__, etc.)
```

If no files in scope, inform user and exit.

### Step 2: Detect Languages

Check files in scope for language markers:

**TypeScript/JavaScript:**
- File extensions: `.ts`, `.tsx`, `.js`, `.jsx`
- Config files: `tsconfig.json`, `package.json`

**Python:**
- File extensions: `.py`, `.pyi`
- Config files: `pyproject.toml`, `setup.py`, `requirements.txt`

If `--lang` flag provided, use that instead of auto-detection.

### Step 3: Load Rules

1. **Always load:** Read [rules/universal.md](rules/universal.md) for language-agnostic rules
2. **If TypeScript detected:** Read [rules/typescript.md](rules/typescript.md)
3. **If Python detected:** Read [rules/python.md](rules/python.md)
4. **For deep dives:** Reference [checklists/](checklists/) as needed

### Step 4: Review Code

For each file in scope:

1. Read the file content
2. Apply universal rules (naming, functions, errors, security, etc.)
3. Apply language-specific rules
4. Record findings with severity:
   - **Critical**: Security flaw, data loss risk, crash potential
   - **Warning**: Bug potential, maintainability issue
   - **Info**: Style suggestion, minor improvement

### Step 5: Report Findings

**If `--inline` (default):**
Present findings in conversation grouped by file:

```
## path/to/file.ts

**[Critical]** Line 42: SQL injection vulnerability
- Issue: User input concatenated directly into query
- Fix: Use parameterized queries

**[Warning]** Line 15-28: Function too long (45 lines)
- Issue: Exceeds recommended 20 lines
- Fix: Extract helper functions for distinct operations

**[Info]** Line 8: Consider more descriptive name
- Issue: Variable `d` is unclear
- Fix: Rename to `dateCreated` or similar
```

**If `--report`:**
Generate `code-review-report.md` with all findings organized by severity, then by file.

**If `--beads`:**
Create beads issues for Critical and Warning findings:
```bash
bd create "[Critical] SQL injection in auth.ts:42" --label code-review
bd create "[Warning] Long function in utils.ts:15" --label code-review
```

### Step 6: Summary

Provide a summary at the end:

```
## Summary

- Files reviewed: 12
- Critical: 2 (must fix)
- Warning: 8 (should fix)
- Info: 15 (optional)

Languages detected: TypeScript, Python
```

## Anti-Patterns

- Do NOT review files outside the specified scope
- Do NOT suggest changes unrelated to the rules
- Do NOT auto-fix code without explicit user request
- Do NOT create beads issues for Info-level findings
- Do NOT be overly pedantic about style when logic is correct

## Quick Reference

```bash
# Review staged changes (default)
/code-review

# Review specific files
/code-review --files=src/auth.ts,src/utils.ts

# Review entire codebase, generate report
/code-review --all --report

# Force Python rules
/code-review --lang=python

# Create tracking issues
/code-review --staged --beads
```
