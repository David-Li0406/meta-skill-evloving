---
name: brainbase-workflow-validator
description: Use this skill to validate project workflows against brainbase standards, identifying issues and generating actionable reports.
---

# Skill body

## Overview

This skill automates the validation of project workflows in a two-phase process: requirements analysis and report generation. It checks for compliance with brainbase standards and provides recommendations for improvement.

## Workflow Overview

```
Phase 1: Requirements Analysis
└── agents/phase1_requirements_analysis.md
    └── Skills: [task-format, milestone-management]
    └── Output: Issue list, compliance check results

Phase 2: Report Generation
└── agents/phase2_report_generation.md
    └── Skills: [principles]
    └── Input: Issue list (from Phase 1)
    └── Output: Validation report (issues + recommended actions)
```

## Usage

### Triggers

Use this skill when you want to:
- Identify issues in project workflows.
- Verify compliance with brainbase standard processes.
- Know recommended actions for workflow improvement.

**Example**:
```
User: "Validate the workflow for this project."
User: "Identify issues compared to brainbase standards."
```

### Input Parameters

| Parameter         | Required/Optional | Description                          | Example          |
|-------------------|-------------------|--------------------------------------|------------------|
| Project Name      | Required          | Name of the project to validate      | `brainbase-ui`   |
| Validation Scope  | Optional          | Task/Milestone/Both                  | `both` (default) |

### Output Format

```markdown
# {Project Name} Workflow Validation Report

## Issue Summary
- Total Issues: X
- Severity Breakdown: Critical Y, Medium Z

## Detailed Issue List
{Details of issues...}

## Recommended Actions
{Prioritized improvement suggestions...}

---
**Creation Date**: YYYY-MM-DD
**Number of Phases**: 2
```

## Phase Details

### Phase 1: Requirements Analysis

**Subagent**: `agents/phase1_requirements_analysis.md`

**Purpose**: Investigate the existing workflow (tasks, milestones) of the project and check for compliance with brainbase standards.

**Skills Used**:
- `task-format`: Check against task management standards.
- `milestone-management`: Check against milestone management rules.

**Input**:
- Project Name
- Files under `_codex/projects/{project}/`

**Output**:
```markdown
## Issue List
- Issue 1: Task format inconsistency
- Issue 2: Milestone granularity too large

## Compliance Check Results
- Task format compliance rate: 70%
- Milestone management compliance rate: 60%
```

**Success Criteria**:
- [ ] Specific issues identified (at least 3).
- [ ] Task format compliance rate calculated.
- [ ] Milestone management compliance rate calculated.

### Phase 2: Report Generation

**Subagent**: `agents/phase2_report_generation.md`

**Purpose**: Generate a validation report including recommended actions based on issues identified in Phase 1.

**Skills Used**:
- `principles`: Prioritize based on brainbase values.

**Input** (from Phase 1):
- `## Issue List`: Identified issues.
- `## Compliance Check Results`: Compliance rates.

**Output**:
```markdown
## Validation Report

### Issue Summary
- Total Issues: X
- Severity Breakdown: Critical Y, Medium Z

### Recommended Actions
1. Standardize task format (Priority: P0)
2. Adjust milestone granularity (Priority: P1)
```