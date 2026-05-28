---
name: task-execution
description: 任務執行技能。依據計劃文件系統性實作任務，追蹤變更並維護品質門檻。輸出變更追蹤至 .copilot-tracking/changes/。適用於需要結構化實作流程的開發任務。
---

# Task Execution Skill

此技能提供結構化的任務執行流程，用於依據計劃文件系統性實作任務。

---

## When to Use This Skill

當你需要：
- 依據計劃文件系統性實作程式碼
- 追蹤所有變更並記錄於標準化文檔
- 確保品質門檻（編譯、測試）通過
- 支援階段性暫停以便使用者審核

---

## Core Principles

### NO LAZY CODING (Critical)

- You MUST output complete code, NEVER abbreviate
- You MUST NOT use `// ... existing code`, `// ... rest of ...` or any placeholders
- You WILL prefer complete file output unless user explicitly requests diff only
- For large files: Output in segments, but MUST complete all segments in same turn

### Plan-Driven Execution

- Implementation MUST correspond to specific tasks from the plan
- You MUST read complete details section before implementing any task
- Update plan checklist on completion: `[ ]` → `[x]`

### Continuous Tracking

- Update changes file after EVERY task completion
- If changes diverge from plan: Document reason in changes file

---

## Pre-Execution Checklist (Hard Gate)

You MUST verify before starting:

- [ ] All prerequisite tasks completed
- [ ] Required tools and packages installed
- [ ] Planning documents available:
  - [ ] Research: `.copilot-tracking/research/*.md`
  - [ ] Plan: `.copilot-tracking/plans/*.plan.instructions.md`
  - [ ] Details: `.copilot-tracking/details/*.details.md`
- [ ] Understanding confirmed:
  - [ ] Task objectives clear
  - [ ] Success criteria clear
  - [ ] Implementation approach defined

---

## Execution Workflow

### Step 1: Initialize

1. Read implementation prompt: `.copilot-tracking/prompts/implement-*.prompt.md`
2. Create changes file if not exists: `.copilot-tracking/changes/YYYYMMDD-##-task-changes.md`
3. Review all linked planning documents (plan/details/research)
4. Confirm scope and success criteria

### Step 2: Implement by Phase

For each Phase in the plan, execute in order:

1. Read Phase objectives and tasks
2. Reference details/research for implementation specifics
3. Implement completely (follow NO LAZY CODING)
4. Write/update unit tests
5. Update plan checklist: `[ ]` → `[x]`
6. Record changes to changes file
7. Report Phase completion status

**Phase Stop**: If `phaseStop=true`, pause after each Phase for user review.

### Step 3: Verify and Finalize

1. Execute build command (e.g., `dotnet build`, `npm run build`)
2. Execute test command (e.g., `dotnet test`, `npm run test`)
3. Verify all success criteria achieved
4. Update all plan items to `[x]`
5. Produce completion summary with changes file link
6. Delete prompt file: `.copilot-tracking/prompts/implement-*.prompt.md`

**Task Stop**: If `taskStop=true`, pause on task completion.

---

## Changes File Format

**Naming**: `YYYYMMDD-##-task-description-changes.md`

**Location**: `.copilot-tracking/changes/`

```markdown
<!-- markdownlint-disable-file -->
# Release Changes: {{task_name}}

**Related Plan**: {{plan_file_name}}
**Implementation Date**: {{YYYY-MM-DD}}

## Summary
{{brief_description}}

## Changes

### Added
- {{relative/path/file}} - {{summary}}

### Modified
- {{relative/path/file}} - {{summary}}

### Removed
- {{relative/path/file}} - {{summary}}

## Implementation Notes
{{key_decisions, assumptions, deviations_from_plan}}

## Release Summary

**Total Files Affected**: {{number}}

### Files Created ({{count}})
- {{path}} - {{purpose}}

### Files Modified ({{count}})
- {{path}} - {{changes}}

### Dependencies & Infrastructure
- **New Dependencies**: {{list}}
- **Configuration Updates**: {{changes}}

### Deployment Notes
{{deployment_considerations}}
```

---

## Progress Reporting Format

### Phase Completion

```markdown
## Phase X: [Phase Name] - ✅ Completed

**Tasks Completed**: [list]
**Files Changed**: [count]
**Status**: ✅ Tests passed / ⚠️ Issues found
**Next**: Phase X+1 / Task complete
```

### Task Completion Summary

```markdown
## Task ##: [Task Name] - ✅ Completed

**Total Phases**: X
**Files Changed**: Y
**Build**: ✅ Success
**Tests**: ✅ Passed
**Docs**: ✅ Updated

**Changes**: Link to `.copilot-tracking/changes/...`

**Notes/Recommendations**:
- [item]
```

---

## Problem Resolution

| Issue | Resolution |
|-------|------------|
| Build failure | Log error → Analyze root cause → Fix immediately → Re-run build/test → Continue |
| Missing dependency | Inventory missing items → Determine if in scope → Add minimal implementation or escalate |
| Unclear spec | Check research/details → Reference source code → Make reasonable assumption and document → Continue and mark for review |
| Test failure | Log failure → Debug systematically → Fix root cause → Re-run tests → Update changes |

### Requires User Intervention (MUST STOP)

- Critical dependency missing and cannot workaround
- Fundamental spec contradiction
- Major architecture decision needed
- Security issue identified
- Database schema change required

---

## File Operation Rules

### Allowed

- ✅ Create: `.copilot-tracking/changes/`, `.copilot-tracking/prompts/`
- ✅ Modify: `.copilot-tracking/plans/` (checklist updates only), `.copilot-tracking/changes/`
- ✅ Implement: Project source code directories

### Prohibited

- ❌ Do not modify: Research files, analysis documents, SRS/SDS
- ❌ Do not delete: Any planning files (plan/details/research)

---

## Reference Files

- See [references/changes-template.md](references/changes-template.md) for detailed template
