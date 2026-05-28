---
name: code-review-inline
description: Inline orchestration workflow for code review with Beads integration. Provides comprehensive analysis of issues (bugs) AND improvements (recommendations), issue creation, priority-based fixing, and verification cycles.
version: 1.1.0
---

# Code Review (Inline Orchestration)

You ARE the orchestrator. Execute this workflow directly without spawning a separate orchestrator agent.

## Workflow Overview

```
Beads Init → Review → Create Issues → Fix by Priority → Close Issues → Verify → Beads Complete
```

**Max iterations**: 2
**Priorities**: critical → high → medium → low
**Beads integration**: Automatic issue tracking
**Context7**: Use for documentation and examples

---

## Phase 1: Pre-flight & Beads Init

1. **Setup directories**:

   ```bash
   mkdir -p .tmp/current/{plans,changes,backups}
   mkdir -p docs/reports/code-reviews/$(date +%Y-%m)
   ```

2. **Validate environment**:
   - Check `package.json` exists
   - Check `type-check` and `build` scripts exist

3. **Determine review scope**:
   - If user specifies files/dirs → use those
   - If user specifies "recent changes" → `git diff --name-only HEAD~5`
   - If user specifies PR → `gh pr diff {number} --name-only`
   - Default → ask user for scope

4. **Create Beads wisp**:

   ```bash
   bd mol wisp exploration --vars "question=Code review: {scope_description}"
   ```

   **IMPORTANT**: Save the wisp ID (e.g., `mc2-xxx`) for later use.

5. **Initialize TodoWrite**:
   ```json
   [
     { "content": "Code review analysis", "status": "in_progress", "activeForm": "Reviewing code" },
     { "content": "Create Beads issues", "status": "pending", "activeForm": "Creating issues" },
     {
       "content": "Fix critical issues",
       "status": "pending",
       "activeForm": "Fixing critical issues"
     },
     {
       "content": "Fix high priority issues",
       "status": "pending",
       "activeForm": "Fixing high issues"
     },
     {
       "content": "Fix medium priority issues",
       "status": "pending",
       "activeForm": "Fixing medium issues"
     },
     {
       "content": "Fix low priority issues",
       "status": "pending",
       "activeForm": "Fixing low issues"
     },
     { "content": "Verification", "status": "pending", "activeForm": "Verifying fixes" },
     { "content": "Complete Beads wisp", "status": "pending", "activeForm": "Completing wisp" }
   ]
   ```

---

## Phase 2: Code Review Analysis

**Invoke code-reviewer** via Task tool:

```
subagent_type: "code-reviewer"
description: "Comprehensive code review"
prompt: |
  Perform comprehensive code review of: {scope}

  Use Context7 for documentation and examples where relevant.

  ## Part 1: Issues (bugs, errors, problems)

  Review checklist:
  - Security vulnerabilities (SQL injection, XSS, auth issues)
  - Type errors and type safety
  - Runtime bugs and edge cases
  - Error handling gaps
  - Dead code and debug statements
  - Missing validation
  - Hardcoded values that should be configurable

  For each ISSUE found:
  - Category: bug/security/type-error/dead-code
  - Priority: critical/high/medium/low
  - File path and line number
  - Problem description
  - Fix with code example

  ## Part 2: Improvements (recommendations, enhancements)

  Review checklist:
  - Performance optimizations
  - Code readability and clarity
  - Better abstractions and patterns
  - Naming improvements
  - Architecture compliance
  - Missing tests suggestions
  - Documentation gaps
  - DRY violations (code duplication)
  - Modern TypeScript patterns
  - React/Next.js best practices

  For each IMPROVEMENT found:
  - Category: performance/readability/architecture/testing/docs/refactor
  - Priority: high/medium/low (no critical for improvements)
  - File path and line number
  - Current state description
  - Recommended improvement with code example
  - Impact: what gets better

  ## Validation

  Run:
  - pnpm type-check
  - pnpm build

  ## Report

  Generate: docs/reports/code-reviews/{YYYY-MM}/CR-{date}-{topic}.md

  Sections:
  1. Executive Summary
  2. Issues Found (by priority)
  3. Improvements Recommended (by priority)
  4. Validation Results
  5. Next Steps

  Return summary:
  - Issue counts per priority
  - Improvement counts per priority
```

**After code-reviewer returns**:

1. Read the generated report
2. Parse issue counts by priority
3. If zero issues → skip to Phase 7 (Final Summary)
4. Update TodoWrite: mark analysis complete

---

## Phase 3: Create Beads Issues

### 3.1 Issues (bugs, errors)

```bash
# Critical (P0) - Security, crashes, data loss
bd create "BUG: {issue_title}" -t bug -p 0 -d "{file}:{line} - {description}" \
  --deps discovered-from:{wisp_id}

# High (P1) - Type errors, runtime bugs
bd create "BUG: {issue_title}" -t bug -p 1 -d "{file}:{line} - {description}" \
  --deps discovered-from:{wisp_id}

# Medium (P2) - Error handling, validation
bd create "BUG: {issue_title}" -t bug -p 2 -d "{file}:{line} - {description}" \
  --deps discovered-from:{wisp_id}

# Low (P3) - Dead code, minor issues
bd create "CLEANUP: {issue_title}" -t chore -p 3 -d "{file}:{line} - {description}" \
  --deps discovered-from:{wisp_id}
```

### 3.2 Improvements (recommendations)

```bash
# High (P2) - Performance, architecture
bd create "IMPROVE: {improvement_title}" -t feature -p 2 -d "{file}:{line} - {description}. Impact: {impact}" \
  --deps discovered-from:{wisp_id}

# Medium (P3) - Readability, refactoring
bd create "IMPROVE: {improvement_title}" -t chore -p 3 -d "{file}:{line} - {description}. Impact: {impact}" \
  --deps discovered-from:{wisp_id}

# Low (P4) - Docs, naming, style
bd create "IMPROVE: {improvement_title}" -t chore -p 4 -d "{file}:{line} - {description}" \
  --deps discovered-from:{wisp_id}
```

**Add labels**:

```bash
bd update {issue_id} --add-label code-review
bd update {improvement_id} --add-label improvement
```

**Track IDs** in two mappings:

- `issues_map`: bug/error issues
- `improvements_map`: improvement recommendations

Update TodoWrite: mark "Create Beads issues" complete.

---

## Phase 4: Ask User About Fixing

**Present summary to user**:

```markdown
## Code Review Complete

**Wisp ID**: {wisp_id}
**Report**: docs/reports/code-reviews/{YYYY-MM}/CR-{date}-{topic}.md

### Issues (bugs, errors)

- Critical: {count}
- High: {count}
- Medium: {count}
- Low: {count}

### Improvements (recommendations)

- High: {count}
- Medium: {count}
- Low: {count}

### Beads Created

- Issues: {count} (BUG:, CLEANUP:)
- Improvements: {count} (IMPROVE:)

**Options**:

1. Fix all (issues + improvements)
2. Fix issues only (bugs, errors)
3. Fix critical/high issues only
4. Review report first, then decide
5. Skip fixing (keep in Beads for later)
```

**If user chooses**:

- Option 1 → Fix issues (Phase 5), then improvements (Phase 5b)
- Option 2 → Fix issues only (Phase 5)
- Option 3 → Fix critical/high issues only (Phase 5, partial)
- Option 4/5 → proceed to Phase 7

---

## Phase 5: Fixing Loop

**For each priority** (critical → high → medium → low):

1. **Check if issues exist** for this priority
   - If zero → skip to next priority

2. **Update TodoWrite**: mark current priority in_progress

3. **Claim issues in Beads**:

   ```bash
   bd update {issue_id} --status in_progress
   ```

4. **Select appropriate fixer agent**:

   | Issue Type               | Agent                       |
   | ------------------------ | --------------------------- |
   | TypeScript errors        | typescript-types-specialist |
   | Security vulnerabilities | vulnerability-fixer         |
   | Dead code                | dead-code-remover           |
   | Bug/correctness          | bug-fixer                   |
   | Code style/refactor      | Direct execution (MAIN)     |

5. **Invoke fixer** via Task tool:

   ```
   subagent_type: "{selected_agent}"
   description: "Fix {priority} code review issues"
   prompt: |
     Read code review report: docs/reports/code-reviews/{YYYY-MM}/CR-{date}-{topic}.md

     Fix all {priority} priority issues.

     For each issue:
     1. Backup file before editing
     2. Implement fix as recommended in report
     3. Log change to .tmp/current/changes/code-review-changes.json

     Return: count of fixed issues, count of failed fixes, list of fixed issue IDs.
   ```

6. **Quality Gate** (inline):

   ```bash
   pnpm type-check
   pnpm build
   ```

   - If FAIL → report error, suggest rollback, exit
   - If PASS → continue

7. **Close fixed issues in Beads**:

   ```bash
   bd close {issue_id_1} {issue_id_2} ... --reason "Fixed in code review"
   ```

8. **Update TodoWrite**: mark priority complete

9. **Repeat** for next priority

---

## Phase 6: Verification

After all priorities fixed:

1. **Update TodoWrite**: mark verification in_progress

2. **Run quality gates**:

   ```bash
   pnpm type-check
   pnpm build
   pnpm lint  # if available
   ```

3. **Quick re-check** (optional):
   - Read fixed files
   - Verify fixes match recommendations
   - Check for regressions

4. **Decision**:
   - If all checks pass → Phase 7
   - If issues remain and iteration < 2 → Go to Phase 2
   - If iteration >= 2 → Phase 7 with remaining issues

---

## Phase 7: Final Summary & Beads Complete

1. **Complete Beads wisp**:

   ```bash
   # If all fixed
   bd mol squash {wisp_id}

   # If nothing found
   bd mol burn {wisp_id}
   ```

2. **Create issues for remaining items** (if any):

   ```bash
   bd create "CR REMAINING: {issue_title}" -t chore -p {priority} \
     -d "Not fixed in review. See report: {report_path}"
   bd update {new_issue_id} --add-label code-review
   ```

3. **Generate summary for user**:

```markdown
## Code Review Complete

**Wisp ID**: {wisp_id}
**Iterations**: {count}/2
**Status**: {SUCCESS/PARTIAL}

### Results

- Found: {total} issues
- Fixed: {fixed} ({percentage}%)
- Remaining: {remaining}

### By Priority

- Critical: {fixed}/{total}
- High: {fixed}/{total}
- Medium: {fixed}/{total}
- Low: {fixed}/{total}

### Beads Issues

- Created: {count}
- Closed: {count}
- Remaining: {count}

### Validation

- Type Check: {status}
- Build: {status}
- Lint: {status}

### Artifacts

- Report: `docs/reports/code-reviews/{YYYY-MM}/CR-{date}-{topic}.md`
- Changes: `.tmp/current/changes/code-review-changes.json`
```

4. **Update TodoWrite**: mark wisp complete

5. **SESSION CLOSE PROTOCOL**:
   ```bash
   git status
   git add .
   bd sync
   git commit -m "fix: code review - {fixed} issues fixed ({wisp_id})"
   bd sync
   git push
   ```

---

## Error Handling

**If quality gate fails**:

```
Rollback available: .tmp/current/changes/code-review-changes.json

To rollback:
1. Read changes log
2. Restore files from .tmp/current/backups/
3. Re-run workflow
```

**If worker fails**:

- Report error to user
- Keep Beads wisp open for manual completion
- Suggest manual intervention
- Exit workflow

**If Beads command fails**:

- Log error but continue workflow
- Beads tracking is enhancement, not blocker

---

## Quick Reference

| Phase           | Beads Action                            |
| --------------- | --------------------------------------- |
| 1. Pre-flight   | `bd mol wisp exploration`               |
| 3. After review | `bd create` + `--add-label code-review` |
| 5. Before fix   | `bd update --status in_progress`        |
| 5. After fix    | `bd close --reason "Fixed"`             |
| 7. Complete     | `bd mol squash/burn`                    |
| 7. Remaining    | `bd create` for unfixed issues          |

---

## Categories & Agents

### Issues (bugs, errors)

| Category               | Priority    | Agent                       |
| ---------------------- | ----------- | --------------------------- |
| Security vulnerability | P0 Critical | vulnerability-fixer         |
| Type errors            | P1 High     | typescript-types-specialist |
| Runtime bugs           | P1-P2       | bug-fixer                   |
| Error handling         | P2 Medium   | bug-fixer                   |
| Dead code              | P3 Low      | dead-code-remover           |

### Improvements (recommendations)

| Category      | Priority  | Agent                        |
| ------------- | --------- | ---------------------------- |
| Performance   | P2 High   | Direct + profiling           |
| Architecture  | P2 High   | Direct (careful review)      |
| Readability   | P3 Medium | Direct execution             |
| Refactoring   | P3 Medium | reuse-fixer (if duplication) |
| Testing       | P3 Medium | test-writer                  |
| Documentation | P4 Low    | Direct execution             |
| Naming/Style  | P4 Low    | Direct execution             |

---

## Report Format

Reports are saved to: `docs/reports/code-reviews/{YYYY-MM}/CR-{date}-{topic}.md`

Standard sections:

1. Executive Summary (issues + improvements counts)
2. Key Metrics
3. **Issues Found** (by priority: critical → low)
4. **Improvements Recommended** (by priority: high → low)
5. Best Practices Validation
6. Security Review
7. Validation Results
8. Recommendations Summary
9. Next Steps

---

## Usage Examples

### Review recent changes

```
User: Run code review on recent changes
→ Scope: git diff --name-only HEAD~5
```

### Review specific files

```
User: Review the enrichment handlers
→ Scope: packages/course-gen-platform/src/stages/stage7-enrichments/handlers/
```

### Review PR

```
User: Review PR #123
→ Scope: gh pr diff 123 --name-only
```

### Full review with fixes

```
User: Run code review and fix everything
→ Execute full workflow with automatic fixing
```
