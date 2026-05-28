# SpecKit Task Grounding Workflow
**Version**: 1.0.0
**Date**: January 12, 2026
**Purpose**: Standardized validation that tasks.md is grounded in planning artifacts

---

## Overview

**What**: A mandatory workflow step that validates every task in tasks.md is traceable to at least one planning artifact with documented justification.

**Why**: Prevents disconnects between implementation tasks and documented requirements; ensures tasks aren't invented assumptions.

**When**: Executed immediately after tasks.md is generated (before human review, before implementation starts).

**Who**: Automated via script + manual review by project lead.

**Outcome**: TASK_GROUNDING_ANALYSIS.md report with validation results and risk assessment.

---

## Process Flow

```
[tasks.md Generated]
         ↓
    [Run Validator Script]
    (Parse tasks, cross-check artifacts)
         ↓
    [Generate Analysis Report]
    (Mapping tables, consistency checks, gaps)
         ↓
    [Human Review]
    (Assess gaps, verify assumptions, approve or block)
         ↓
    [Decision Gate]
    ├─ APPROVED → Proceed to implementation
    ├─ NEEDS CLARIFICATION → Update spec/plan, regenerate
    └─ BLOCKED → Major gaps detected, return to planning
```

---

## Validation Framework

### Step 1: Task Extraction

**Input**: tasks.md file
**Output**: Structured task list

```yaml
Phase: "Phase 1"
PhaseName: "Setup"
Tasks:
  - ID: "T001"
    Title: "Add LifelineAutoRoleAssignment to TenantFeatureFlag"
    FilePath: "src/Core/Shared/FeatureManagement/FeatureFlags.cs"
    Labels:
      - Completed: true
      - Parallelizable: false
      - StoryTag: null
    Description: "..."
```

### Step 2: Artifact Indexing

**Input**: All planning artifacts (spec.md, plan.md, data-model.md, api-contracts.md, research.md, quickstart.md)
**Output**: Cross-indexed artifact index

```yaml
Artifacts:
  - Name: "data-model.md"
    Sections:
      - Title: "Feature Flags"
        Content: "[Full section text]"
        Keywords: ["TenantFeatureFlag", "LifelineAutoRoleAssignment"]
        FileReferences: ["src/Core/Shared/FeatureManagement/FeatureFlags.cs"]
```

### Step 3: Traceability Mapping

**For each task**, find evidence in artifacts:

```yaml
Task: T001
ArtifactMatches:
  - Artifact: "data-model.md"
    Section: "Feature Flags"
    MatchType: "explicit"
    MatchScore: 100
    Evidence: "[Quoted text from artifact]"
  - Artifact: "plan.md"
    Section: "Technical Context"
    MatchType: "reference"
    MatchScore: 60
    Evidence: "[Quoted text from artifact]"
```

**Match Types**:
- `explicit`: Direct specification (e.g., "Add X to Y")
- `reference`: Mentioned but not fully specified
- `implicit`: Inferred from pattern/principle
- `external`: Depends on spec.md or external doc

### Step 4: Consistency Cross-Check

**Compare** task requirements against artifact consistency:

```yaml
ConsistencyChecks:
  - Item: "LifelineCoHost permission count"
    plan.md: "18 total (both roles)"
    data-model.md: "14 permissions"
    api-contracts.md: "14 permissions"
    Status: "✅ Consistent"

  - Item: "Auto-assignment trigger"
    plan.md: "Not specified"
    data-model.md: "Invitation acceptance"
    api-contracts.md: "SessionGroupParticipantInvitationAcceptedEvent"
    Status: "✅ Consistent"
```

### Step 5: Gap Analysis

**Identify** missing or weakly grounded tasks:

```yaml
Gaps:
  - TaskID: "T003"
    Issue: "FSHRoles.cs pattern assumed but not documented in plan.md"
    GroundingLevel: 70%
    ArtifactCoverage: "Implicit only (no explicit reference)"
    Risk: "medium"
    Resolution: "Verify codebase pattern before executing"

  - TaskID: "T004"
    Issue: "SentEvent requirement not explicitly in planning artifacts"
    GroundingLevel: 60%
    ArtifactCoverage: "Schema reference only (incomplete)"
    Risk: "high"
    Resolution: "Verify spec.md FR-001 before executing"
```

### Step 6: Risk Assessment

**Rate** each task's implementation risk:

```yaml
RiskAssessment:
  - TaskID: "T001"
    GroundingLevel: "100%"
    RiskLevel: "🟢 Low"
    RiskFactors:
      - Straightforward enum addition
      - Well-documented in multiple artifacts
      - No dependencies
    ExecutionRecommendation: "Ready to execute immediately"

  - TaskID: "T003"
    GroundingLevel: "70%"
    RiskLevel: "🟡 Medium"
    RiskFactors:
      - Pattern assumed without explicit documentation
      - No codebase validation performed
      - Impacts downstream tasks (seeder, handler)
    ExecutionRecommendation: "Verify codebase pattern first"
```

---

## Validation Report Structure

### Report Template: TASK_GROUNDING_ANALYSIS.md

**Format**: Markdown document with standardized sections

```markdown
# Task Grounding Analysis: [Feature Name]
**Feature**: [feature-id] | **Date**: [date]
**Status**: [Analysis Result Summary]

---

## Executive Summary
[1-2 paragraph overview of validation results]

| Phase | Status | Tasks | Grounded | Risk |
|-------|--------|-------|----------|------|
| Phase 1 | ✅ | T001-T003 | 100%, 100%, 70% | Low, Low, Medium |
| Phase 2 | ⚠️ | T004-T005 | 60%, 50% | High, High |

---

## Phase [N] - [Phase Name] - Detailed Mapping

### Task T[NNN]: [Task Title]
| Aspect | Details |
|--------|---------|
| **Status** | [Not started / In progress / Completed] |
| **Primary Artifact** | [artifact.md - Section Name] |
| **Secondary Artifacts** | [artifact2.md, artifact3.md] |
| **Grounding Level** | [NN%] |

**Grounding Evidence**:
[Numbered list of evidence items with quotes]

**Assessment**: [Verdict - Fully/Partially/Weakly Grounded]

---

## Cross-Artifact Consistency Check

| Item | Artifact1 | Artifact2 | Artifact3 | Consistency |
|------|-----------|-----------|-----------|-------------|
| [Item] | [Value] | [Value] | [Value] | ✅/⚠️ |

---

## Critical Gaps & Questions

### Gap [N]: [Gap Title]
**Status**: [Level] [Task affected]
**Issue**: [Description]
**Resolution**:
- [ ] [Action item]
- [ ] [Action item]

---

## Risk Assessment

| Task | Risk Level | Mitigation |
|------|-----------|-----------|
| T001 | 🟢 Low | [Mitigation] |
| T002 | 🟡 Medium | [Mitigation] |

---

## Recommendations

### Before Proceeding:
[Numbered list of validation requirements]

### Decision Gate:
- ✅ **APPROVED**: Proceed to implementation
- ⚠️ **NEEDS CLARIFICATION**: Update artifacts, regenerate
- 🔴 **BLOCKED**: Major gaps, return to planning

---

## Summary

**Overall Assessment**: [Verdict]
**Confidence Level**: [Color] [Percentage]
**Next Action**: [Clear statement of what should happen next]
```

---

## Acceptance Criteria

### For Report to be Valid:

- [ ] All tasks in tasks.md are listed in report
- [ ] Each task has primary artifact mapped
- [ ] Each task has grounding level (0-100%)
- [ ] Each task has risk assessment (Low/Medium/High)
- [ ] Cross-artifact consistency verified for key items
- [ ] All gaps identified and explained
- [ ] Decision gate clearly stated (Approved/Needs Clarification/Blocked)
- [ ] No tasks marked as "Grounding Level: Unknown"

### For Analysis to Support Approval:

- [ ] ≥90% of Phase 1 tasks grounded at 80%+
- [ ] ≥80% of Phase 2 tasks grounded at 70%+
- [ ] No high-risk gaps with unresolved dependencies
- [ ] All external references (spec.md, research.md, etc.) verified against actual files
- [ ] Inconsistencies between artifacts identified and documented
- [ ] Clear action items for any gaps

---

## Validation Inputs Checklist

Before running validator, confirm these artifacts exist:

- [ ] spec.md
- [ ] plan.md
- [ ] data-model.md (or equivalent)
- [ ] api-contracts.md (or equivalent)
- [ ] research.md (or equivalent)
- [ ] quickstart.md (optional but recommended)
- [ ] tasks.md (must be present)

**Note**: If any artifact is missing, validator adjusts scoring and notes incomplete coverage.

---

## Integration Points

### For SpecKit Workflow:

```yaml
# In speckit.constitution.md or workflow runner
Workflow:
  - Step: "Generate tasks.md"
    Agent: "speckit.tasks"
    Artifact: "tasks.md"

  - Step: "Validate task grounding"          # NEW STEP
    Agent: "speckit.task-grounding"          # New agent
    Input: "tasks.md + all planning artifacts"
    Output: "TASK_GROUNDING_ANALYSIS.md"
    Decision: "Approved / Needs Clarification / Blocked"
    Gate: "Block if gaps critical"

  - Step: "Review and approve"
    Role: "Project Lead"
    Input: "TASK_GROUNDING_ANALYSIS.md"
    Decision: "Proceed to implementation"
```

### For CI/CD Pipeline (Optional):

```bash
# Automated validation on spec commit
validate-tasks.sh:
  1. Extract feature directory
  2. Check all artifacts exist
  3. Run grounding validator
  4. Generate TASK_GROUNDING_ANALYSIS.md
  5. Check decision gate
  6. Fail if Blocked, warn if Needs Clarification
```

---

## Customization Points

### For Different Project Types:

**Adjust grounding thresholds** by phase/project maturity:

```yaml
DefaultThresholds:
  Phase1Setup:
    MinGroundingLevel: 80%
    ApprovalThreshold: "≥90% tasks at 80%+"
  Phase2Foundational:
    MinGroundingLevel: 70%
    ApprovalThreshold: "≥80% tasks at 70%+"
  Phase3+UserStories:
    MinGroundingLevel: 60%
    ApprovalThreshold: "≥70% tasks at 60%+"

ProjectOverrides:
  MVP: [Raise all thresholds +10%]
  Research: [Lower foundational threshold to 50%]
  Infrastructure: [Require 100% for all phases]
```

### For Different Artifact Schemas:

Map your artifacts to standard validation categories:

```yaml
ArtifactMapping:
  "spec.md":
    Type: "specification"
    Sections: ["User Stories", "Acceptance Criteria", "Feature Requirements"]
    Weight: 1.0

  "plan.md":
    Type: "plan"
    Sections: ["Technical Context", "Project Structure", "Phase Summary"]
    Weight: 0.8

  "data-model.md":
    Type: "design"
    Sections: ["Entities", "Relationships", "Migrations"]
    Weight: 0.7

  "api-contracts.md":
    Type: "contract"
    Sections: ["Endpoints", "Events", "DTOs"]
    Weight: 0.8
```

---

## Workflow Automation (Optional)

See `.specify/scripts/powershell/validate-task-grounding.ps1` for:
- Automated artifact parsing
- Traceability matching algorithm
- Consistency validation rules
- Report generation template
