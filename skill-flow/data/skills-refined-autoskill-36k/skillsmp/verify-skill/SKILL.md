---
name: verify-skill
description: Use before claiming work is complete - runs tests, checks git status, verifies changelog
---

# Verification Before Completion

Run this before saying "task complete" or "done".

## Checklist

### 1. Tests Pass
```bash
npm run test:backend
```
Do NOT proceed if tests fail.

### 2. Code Committed
```bash
git status
```
All work-related files should be committed.

### 3. Changelog Updated
Check CHANGELOG.md [Unreleased] section has entry for this work.
If not, run /changelog.

## Quick Verification
```powershell
# Run tests
cd src-tauri && cargo test

# Check status
git status

# Check changelog
head -20 CHANGELOG.md
```

See CLAUDE.md for project constraints.
