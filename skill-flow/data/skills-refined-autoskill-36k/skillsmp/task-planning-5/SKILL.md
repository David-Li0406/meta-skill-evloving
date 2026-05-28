---
name: task-planning
description: 任務規劃技能。基於研究結果建立可執行的階段性計劃，輸出標準化的計劃、細節、提示文檔至 .copilot-tracking/。適用於需要結構化規劃的開發任務。
---

# Task Planning Skill

此技能提供結構化的規劃流程，用於將研究結果轉換為可執行的任務計劃。

---

## When to Use This Skill

當你需要：
- 基於研究結果建立可執行的實作計劃
- 將複雜任務拆解為階段性的檢查清單
- 建立詳細的實作細節文檔
- 產生用於驅動執行的提示文檔

---

## Core Principles

### Research First

- You MUST verify research document exists and is complete before planning
- If research is missing: Use `task-research` skill immediately
- If research needs updates: Use `task-research` skill for refinement

### Planning Only, No Implementation

- ✅ You WILL create/edit files in `.copilot-tracking/plans/`, `details/`, `prompts/`
- ❌ You MUST NOT modify any source code or configuration files
- ❌ You MUST NOT plan without verified research

---

## File Operations

| Operation | Scope |
|-----------|-------|
| READ | Entire workspace |
| WRITE | `.copilot-tracking/plans/`, `details/`, `prompts/`, `research/` (updates only) |
| OUTPUT | Brief status updates only, do NOT display full plan content |

---

## Planning Workflow

### 1. Research Validation (MANDATORY)

1. Search for research files in `.copilot-tracking/research/`
2. Validate research completeness:
   - Tool usage documentation with verified findings
   - Complete code examples and specifications
   - Project structure analysis with actual patterns
   - External source research with implementation examples
   - Evidence-based implementation guidance
3. If research is missing/incomplete: Use `task-research` skill
4. Proceed ONLY after research validation

### 2. Planning File Creation

| File Type | Naming Format | Location |
|-----------|--------------|----------|
| Plan | `YYYYMMDD-##-task-description-plan.instructions.md` | `plans/` |
| Details | `YYYYMMDD-##-task-description-details.md` | `details/` |
| Prompt | `implement-##-task-description.prompt.md` | `prompts/` |

### 3. Line Number Management

You MUST maintain accurate line number references:

- **Research → Details**: Include specific line ranges `(Lines X-Y)` for each reference
- **Details → Plan**: Include specific line ranges for each reference
- **On Updates**: Update all line number references when files are modified
- **Verification**: Verify references point to correct sections before completing

---

## Template Conventions

You MUST use `{{placeholder}}` markers:

- **Format**: `{{descriptive_name}}` with double curly braces and snake_case
- **Final Output**: Ensure NO template markers remain in final files

**Examples**:
- `{{task_name}}` → "API Migration Implementation"
- `{{date}}` → "20260114"
- `{{file_path}}` → "src/services/api.ts"

---

## Output File Structures

### Plan File (`*-plan.instructions.md`)

```markdown
---
applyTo: ".copilot-tracking/changes/{{date}}-{{task_description}}-changes.md"
---

<!-- markdownlint-disable-file -->

# Task Checklist: {{task_name}}

## Overview
{{one_sentence_description}}

## Objectives
- {{specific_goal_1}}
- {{specific_goal_2}}

## Research Summary
- #file:../research/{{research_file}} - {{description}}

## Implementation Checklist

### [ ] Phase 1: {{phase_name}}
- [ ] Task 1.1: {{action}}
  - Details: .copilot-tracking/details/{{file}}.md (Lines X-Y)

## Dependencies
- {{tool_or_framework}}

## Success Criteria
- {{completion_indicator}}
```

### Details File (`*-details.md`)

```markdown
<!-- markdownlint-disable-file -->

# Task Details: {{task_name}}

## Research Reference
**Source**: #file:../research/{{research_file}}

## Phase 1: {{phase_name}}

### Task 1.1: {{action}}

{{description}}

- **Files**: {{file_path}} - {{purpose}}
- **Success**: {{criteria}}
- **Research**: Lines X-Y - {{section}}
- **Dependencies**: {{prerequisites}}
```

### Prompt File (`implement-*.prompt.md`)

```markdown
---
agent: agent
model: Claude Sonnet 4.5 (copilot)
---

<!-- markdownlint-disable-file -->

# Implementation Prompt: {{task_name}}

## Instructions

1. Create changes tracking file if not exists
2. Follow task-execution skill workflow
3. Implement #file:../plans/{{plan_file}} systematically
4. If phaseStop=true: Stop after each Phase for review
5. On completion: Delete this prompt file

## Success Criteria
- [ ] All plan items implemented
- [ ] Changes file continuously updated
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

## Completion Summary

規劃完成時，提供：

- **Research Status**: [Verified/Missing/Updated]
- **Planning Status**: [New/Continued]
- **Files Created**: List of planning files
- **Ready for Implementation**: [Yes/No] with assessment

---

## Reference Files

- See [references/plan-template.md](references/plan-template.md) for complete templates
