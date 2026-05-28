---
name: task-execution-planning-research
description: Use this skill when you need to systematically execute, plan, and research tasks in a structured development workflow.
---

# Task Execution, Planning, and Research Skill

此技能提供結構化的任務執行、規劃和研究流程，用於在開發任務中系統性地實作、計劃和分析。

---

## When to Use This Skill

當你需要：
- 依據計劃文件系統性實作程式碼
- 基於研究結果建立可執行的實作計劃
- 追蹤所有變更並記錄於標準化文檔
- 確保品質門檻（編譯、測試）通過
- 在實作前進行全面調查和分析

---

## Core Principles

### NO LAZY CODING (Critical)

- You MUST output complete code, NEVER abbreviate.
- You MUST NOT use placeholders or incomplete code snippets.
- You WILL prefer complete file output unless user explicitly requests diff only.

### Research First

- You MUST verify research document exists and is complete before planning or execution.
- If research is missing: Use `task-research` skill immediately.

### Plan-Driven Execution

- Implementation MUST correspond to specific tasks from the plan.
- You MUST read complete details section before implementing any task.

### Continuous Tracking

- Update changes file after EVERY task completion.
- If changes diverge from plan: Document reason in changes file.

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

## Research Workflow

### 1. Research Planning and Discovery

- Analyze research scope and use all available tools to conduct a thorough investigation.
- Collect evidence from multiple sources to establish a complete understanding.

### 2. Alternative Analysis and Evaluation

- Identify multiple implementation methods, documenting pros and cons for each.
- Use evidence-driven standards to evaluate alternatives and form recommendations.

### 3. Collaborative Refinement

- Present findings concisely to the user, highlighting key discoveries and alternatives.
- Guide the user to select a single recommended approach and remove alternatives from the final research document.

---

## Output Formats

### Changes File Format

**Naming**: `YYYYMMDD-##-task-description-changes.md`

**Location**: `.copilot-tracking/changes/`

```markdown
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
```

### Research Output Format

**File naming**: `YYYYMMDD-##-task-description-research.md`

**Location**: `.copilot-tracking/research/`

```markdown
# Task Research Notes: {{task_name}}

## Research Executed

### File Analysis
- {{file_path}}
  - {{findings_summary}}

### Code Search Results
- {{search_term}}
  - {{matches_found}}

### External Research
- #githubRepo:"{{org/repo}} {{search_terms}}"
  - {{patterns_found}}
- #fetch:{{url}}
  - {{key_information}}

## Key Discoveries

### Project Structure
{{project_organization_findings}}

### Implementation Patterns
{{code_patterns_and_conventions}}

### Recommended Approach
{{selected_approach_with_details}}
```

---

## Quality Standards

| Aspect | Requirement |
|--------|-------------|
| Actionable | Use specific action verbs (create, modify, update, test) |
| Research-Driven | Include only validated information from research |
| Implementation Ready | Provide sufficient detail for immediate work |
| Complete | No missing steps between phases |

---

## Reference Files

- See [references/plan-template.md](references/plan-template.md) and [references/research-template.md](references/research-template.md) for complete templates.