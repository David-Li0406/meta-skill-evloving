<!--
Embedded Navigator Command: review
Standalone version for plugin-free operation
-->
---
allowed-tools: Task, Glob, Grep, Read, Bash(git diff:*), Bash(git log:*), Bash(git status:*), AskUserQuestion
argument-hint: <spec file>
description: Review implementation against spec and patterns
---

## Context

Arguments: `/spec-review <SPEC_FILE>`
- **<spec_file>** - Path to spec that was implemented

Current directory: !`pwd`
Current branch: !`git branch --show-current`

## Workflow

### 1. Pre-flight

**Verify atlas and spec exist.**

### 2. Load Context

**Read spec:**
- Success criteria
- Pattern guides referenced
- Expected files

**Load atlas:**
- Schema and relevant patterns

**Get changes:**
```bash
git diff {base_branch}...HEAD --name-only
git diff {base_branch}...HEAD --stat
```

### 3. Review Against Spec

**Check success criteria:**

| Criterion | Status | Evidence |
|-----------|--------|----------|
| {criterion} | ✅/❌ | {how verified} |

**Check files:**

| Expected | Status | Notes |
|----------|--------|-------|
| {file} | ✅/❌ | {notes} |

### 4. Review Against Patterns

For each pattern:
- Check conventions followed
- Check for anti-patterns
- Note good adherence
- Suggest improvements

### 5. Code Quality

Check:
- Readability
- Consistency
- Completeness
- Testing

### 6. Run Validation

Execute validation commands.
Report pass/fail.

### 7. Generate Report

```markdown
## Navigator Review: {spec_name}

**Spec:** `{spec_file}`
**Branch:** `{branch}`

---

### Summary

| Category | Score | Details |
|----------|-------|---------|
| Spec Compliance | {A-F} | {X/Y criteria} |
| Pattern Adherence | {A-F} | {X/Y conventions} |
| Code Quality | {A-F} | {notes} |
| Validation | {A-F} | {pass/fail} |

**Status:** {✅ Ready | ⚠️ Needs attention | ❌ Issues}

---

### Findings

#### ✅ Successes
{list}

#### ⚠️ Suggestions
{list}

#### ❌ Issues
{list}

---

### Validation Results

| Check | Status |
|-------|--------|
{results}

---

### Recommendations

{action items}
```

**Scoring:**
- A: Excellent (90%+)
- B: Good (80%+)
- C: Acceptable (60%+)
- F: Needs work (<60%)
