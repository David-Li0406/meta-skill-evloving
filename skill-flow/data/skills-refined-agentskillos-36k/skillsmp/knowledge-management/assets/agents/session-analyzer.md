---
description: Analyze git changes and create retrospective draft with Before/After context
---

# Session Analyzer

Agent สำหรับวิเคราะห์ session และสร้าง retrospective draft พร้อม Before/After context

## Purpose

- วิเคราะห์ git changes ของ session
- สร้าง retrospective draft อัตโนมัติ
- Extract Before/After context
- ระบุ type และ tags
- เตรียม input สำหรับ `/td`

## When to Use

- ก่อนใช้ `/td` command
- จบ coding session
- เมื่อต้องการสรุป session
- Auto-capture trigger

## Instructions

### Step 1: Gather Session Context

```bash
export TZ='Asia/Bangkok'

echo "=== Session Info ==="
echo "Date: $(date '+%Y-%m-%d')"
echo "Time: $(date '+%H:%M:%S')"
echo "Branch: $(git branch --show-current)"

echo "=== Current Focus ==="
cat docs/current.md 2>/dev/null || echo "No focus set"
```

### Step 2: Analyze Git Changes

```bash
echo "=== Changed Files ==="
git diff --name-only HEAD

echo "=== Staged Files ==="
git diff --cached --name-only

echo "=== Diff Stats ==="
git diff --stat HEAD

echo "=== Recent Commits (this session) ==="
git log --oneline -10 --since="4 hours ago"
```

### Step 3: Determine Session Type

Based on changes, classify:

| Type | Indicators |
|------|------------|
| `feature` | New files, new functionality |
| `bugfix` | Fix in existing code, test additions |
| `refactor` | Code restructure, no behavior change |
| `docs` | Only .md files changed |
| `config` | Config files, build scripts |
| `test` | Only test files added/changed |
| `decision` | Architecture changes, new patterns |

### Step 4: Extract Before/After Context

**Before Context:**
- What problem existed?
- What was the previous behavior?
- What metrics/state before?

**After Context:**
- What solution was applied?
- What is the new behavior?
- What metrics/state after?

### Step 5: Identify Key Insights

From the changes, extract:
- Technical decisions made
- Patterns discovered
- Gotchas encountered
- Lessons learned

### Step 6: Generate Tags

Analyze changes for:
- Technologies used
- Problem domains
- Patterns applied
- Tools involved

## Output Format

```markdown
## Session Analysis

**Date:** YYYY-MM-DD HH:MM:SS (Asia/Bangkok)
**Branch:** branch-name
**Duration:** ~Xh (estimated from commits)

---

### Classification

| Field | Value |
|-------|-------|
| Type | feature/bugfix/refactor/etc |
| Status | completed/pending/blocked |
| Complexity | low/medium/high |

**Tags:** tag1, tag2, tag3

---

### Summary

[2-3 sentence summary of what was accomplished]

---

### Context: Before

- **Problem:** What issue or need existed
- **Existing Behavior:** How it worked before
- **Pain Points:** What wasn't working well
- **Metrics:** Relevant numbers before (if applicable)

---

### Context: After

- **Solution:** What was implemented
- **New Behavior:** How it works now
- **Improvements:** What's better
- **Metrics:** Relevant numbers after (if applicable)

---

### Changes Overview

| Metric | Count |
|--------|-------|
| Files changed | X |
| Files added | Y |
| Files deleted | Z |
| Lines added | +N |
| Lines removed | -M |

#### Key Files Modified

| File | Changes |
|------|---------|
| `path/to/file.ts` | Added feature X |
| `path/to/other.ts` | Fixed bug Y |

---

### Commits This Session

```
abc1234 feat: add feature X
def5678 fix: resolve issue Y
```

---

### Key Insights

1. **Technical:** [insight about code/architecture]
2. **Process:** [insight about workflow]
3. **Gotcha:** [something to watch out for]

---

### Decisions Made

| Decision | Options Considered | Chosen | Rationale |
|----------|-------------------|--------|-----------|
| [decision] | A, B, C | B | [why] |

---

### Follow-up Items

- [ ] Item that needs attention later
- [ ] Improvement for future

---

### Retrospective Draft Location

Ready to create: `docs/retrospective/YYYY-MM/retrospective_YYYY-MM-DD_HHMMSS.md`
```

## Integration

- Runs before `/td` command
- Feeds into retrospective template
- Can trigger auto-capture
- Updates activity log

## Automation Tips

- Use git timestamps for duration estimation
- Extract issue numbers from branch/commits
- Link to related PRs
- Track file type distribution
