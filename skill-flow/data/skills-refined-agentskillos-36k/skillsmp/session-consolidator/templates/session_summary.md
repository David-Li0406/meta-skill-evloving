# Session Consolidation Report: {feature-name}

> **Generated:** {YYYY-MM-DD HH:MM}
> **Branch:** {branch-name}
> **Spec:** `.ai/specs/{branch-name}.md`
> **Duration:** {start-date} → {end-date} ({days} days)

---

## Executive Summary

{2-3 sentences describing what was accomplished in this session}

**Compliance Score:** {X}/10 — {adjective}

---

## Pipeline Compliance Analysis

### Compliance Score: {X}/10

| Check | Status | Notes |
|-------|--------|-------|
| confidence-evaluator used | ✅/❌ | {brief explanation} |
| Spec file exists | ✅/❌ | {path or reason for missing} |
| Spec followed | ✅/❌ | {percentage of stages completed as planned} |
| Line limits respected | ✅/❌ | {max lines in commit, any violations} |
| Conventional commits | ✅/❌ | {count non-compliant commits if any} |
| CHANGELOG updated | ✅/❌ | {entries per commit count} |
| Stage tracking | ✅/❌ | {status progression verification} |
| Tests run before commits | ✅/❌ | {test evidence} |

### Deviations from Framework

{If any deviations found, list them with detailed explanation}

**Deviation #{N}: {Title}**
- **What happened:** {description}
- **Impact:** {low/medium/high}
- **Recommendation:** {how to prevent in future}

{If no deviations:}
✅ No significant deviations from framework detected.

---

## Ambiguities Encountered

{List ambiguities discovered during analysis in chronological order}

### {Category Name}: {Brief Title}

**Ambiguity:**
{Description of the unclear requirement or situation}

**How it was resolved:**
{Explanation of the decision made}

**Rationale:**
{Why this approach was chosen over alternatives}

**Evidence:**
{Commit hashes, file paths, or other indicators}

{If no ambiguities:}
✅ No significant ambiguities encountered during implementation.

---

## Decisions Made

{Document key architectural and implementation decisions}

### {Decision Area}: {Brief Title}

**Decision:**
{What was decided}

**Alternatives Considered:**
- Alternative 1: {description}
- Alternative 2: {description}

**Justification:**
{Why this option was chosen}

**Impact:**
{Effect on codebase, performance, maintainability}

{If no significant decisions:}
All implementation decisions were specified in the original spec.

---

## Stage Execution Summary

| Stage | Status | Commits | Lines Changed | Duration | Notes |
|-------|--------|---------|---------------|----------|-------|
| {stage-1 name} | ✅ | {hash1, hash2} | {+123, -45} | {days} | {brief notes} |
| {stage-2 name} | ✅ | {hash3} | {+67, -12} | {days} | {brief notes} |
| {stage-3 name} | ✅ | {hash4, hash5, hash6} | {+234, -89} | {days} | {brief notes} |

**Total Changes:**
- Commits: {total_count}
- Files changed: {total_files}
- Lines added: {+total_additions}
- Lines deleted: {-total_deletions}
- Net change: {net_change}

---

## Git Statistics

```bash
# Branch info
Branch: {branch-name}
Base branch: {main/master}
Commits in branch: {count}

# First commit
{first_commit_hash} - {first_commit_date} - {first_commit_message}

# Last commit
{last_commit_hash} - {last_commit_date} - {last_commit_message}

# Changed files by type
Python: {count} files
Markdown: {count} files
Config: {count} files
Tests: {count} files
```

---

## Lessons Learned

### What Went Well

{2-3 bullets about positive aspects}

- {example: "Clear spec structure enabled parallel execution"}
- {example: "Line limit constraint kept changes focused"}

### Areas for Improvement

{2-3 bullets about what could be better}

- {example: "Spec could have more detailed acceptance criteria"}
- {example: "Some stages exceeded 250 lines due to complexity"}

---

## Recommendations for Future Sessions

1. **{Area}:** {specific recommendation with rationale}
2. **{Area}:** {specific recommendation with rationale}
3. **{Area}:** {specific recommendation with rationale}

---

## Archive Metadata

- **Spec File:** `.ai/specs/{branch-name}.md`
- **Session Summary:** `.ai/specs/archive/{branch-name}-session-summary.md`
- **Feature Branch:** {branch-name}
- **First Commit:** {first_commit_hash}
- **Final Commit:** {last_commit_hash}
- **Total Duration:** {days} days
- **Total Changes:** {files} files changed, {insertions} insertions(+), {deletions} deletions(-)

---

*Report generated automatically by session-consolidator skill in fresh context*
