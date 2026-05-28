# Task Grounding Validation Framework - Core Methodology
**Version**: 2.0.0 (Compressed) | **Purpose**: Complete validation process and tools
**Date**: January 12, 2026

---

## 📋 Overview

**What**: A mandatory workflow step that validates every task in tasks.md is traceable to at least one planning artifact with documented justification.

**Why**: Prevents disconnects between implementation tasks and documented requirements; ensures tasks aren't invented assumptions.

**When**: Executed immediately after tasks.md is generated (before human review, before implementation starts).

**Who**: Automated via script + manual review by project lead.

**Outcome**: TASK_GROUNDING_ANALYSIS.md report with validation results and risk assessment.

---

## 🔄 Process Flow

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

## 🏗️ Validation Framework (6-Step Methodology)

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
- `explicit`: Direct specification (e.g., "Add X to Y") → 100%
- `reference`: Mentioned but not fully specified → 80%
- `implicit`: Inferred from pattern/principle → 60%
- `external`: Depends on spec.md or external doc → 50%+

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
    RiskLevel: "low"
    Factors: ["100% grounding in data-model.md", "Explicit specification"]
    Mitigation: "None required"

  - TaskID: "T002"
    RiskLevel: "medium"
    Factors: ["70% grounding", "Pattern inference required"]
    Mitigation: "Verify FSHRoles.cs pattern before implementation"
```

---

## 📋 Pre-Validation Setup Checklist

### ✅ Validate Inputs Exist

- [ ] `spec.md` exists in feature directory
- [ ] `plan.md` exists in feature directory
- [ ] `tasks.md` exists in feature directory
- [ ] `data-model.md` (or equivalent design doc) exists
- [ ] `api-contracts.md` (or equivalent) exists
- [ ] `research.md` (or equivalent) exists
- [ ] At least 5 of 7 artifacts available (minimum 71%)

**If artifacts missing**:
- [ ] Document which artifacts are missing in report
- [ ] Adjust grounding threshold accordingly (-5% per missing artifact)
- [ ] Note in risk assessment: "Incomplete artifact coverage"

---

## 🔍 Report Validation Checklist

### ✅ Report Structure

- [ ] Title includes feature ID and date
- [ ] Executive summary present (1-2 paragraphs)
- [ ] Summary table with Phase | Status | Tasks | Grounded | Risk columns
- [ ] Detailed mapping section for each phase
- [ ] Cross-artifact consistency check section
- [ ] Critical gaps section with resolution items
- [ ] Risk assessment table
- [ ] Recommendations with clear action items
- [ ] Decision gate clearly stated at end

### ✅ Task Coverage

- [ ] Every task from tasks.md is included in report
- [ ] Each task has unique ID matching tasks.md
- [ ] Task titles match tasks.md exactly
- [ ] File paths match tasks.md exactly
- [ ] No invented tasks in report (only from tasks.md)

### ✅ Grounding Evidence

**For each task**, verify:

- [ ] Primary artifact clearly identified
- [ ] Secondary artifacts listed (if applicable)
- [ ] Grounding level stated (0-100%)
- [ ] Match type documented (explicit/reference/implicit/external)
- [ ] ≥1 evidence quote from artifact
- [ ] Evidence quote is accurate (matches artifact)
- [ ] Evidence quote includes context (sentence before + after)
- [ ] Verdict clearly stated (Fully/Partially/Weakly/Not Grounded)

### ✅ Consistency Validation

**For each key item cross-checked**:

- [ ] Item name clearly stated
- [ ] Value from each artifact documented
- [ ] Discrepancies identified (if any)
- [ ] Consistency verdict stated (✅/⚠️)
- [ ] If inconsistent, explanation provided

### ✅ Gap Identification

**For each gap documented**:

- [ ] Gap title is specific (not vague)
- [ ] Related task(s) clearly identified
- [ ] Root cause explained
- [ ] Impact assessed (Why does this matter?)
- [ ] Resolution steps actionable (not "research further")
- [ ] Checkbox format used (- [ ] action item)
- [ ] Owner/responsibility assigned (if known)

### ✅ Risk Assessment

**For each task rated**:

- [ ] Risk level assigned (Low/Medium/High)
- [ ] Risk factors listed (≥1, specific)
- [ ] Grounding level correlates with risk
  - 100% grounding → Low risk
  - 70-90% → Medium risk
  - <70% → High risk
- [ ] Mitigation/recommendation specific and actionable
- [ ] Color coding used (🟢/🟡/🔴) for visual clarity

---

## 📊 Grounding Level Scale (0-100%)

### Detailed Scoring Guide

| Level | Meaning | Evidence Required | Action |
|-------|---------|-------------------|--------|
| 100% | Explicit in primary artifact | Direct quote: "Add X to Y file" | ✅ Execute immediately |
| 90-99% | Well-documented, clear intent | Strong evidence, minimal inference | ✅ Execute |
| 80-89% | Well-documented, pattern inferred | Clear documentation + reasonable inference | ✅ Execute |
| 70-79% | Documented but needs verification | Documentation exists but verification needed | ⚠️ Verify before executing |
| 60-69% | Weakly documented | Multiple weak references | ⚠️ Recommend clarification |
| 50-59% | Inferred from multiple sources | Cross-artifact inference required | 🔴 High risk, needs resolution |
| 40-49% | Weak inference | Single weak reference | 🔴 High risk, block Phase 2 |
| 30-39% | Assumed with some basis | Very weak evidence | 🔴 Not grounded, block |
| 20-29% | Assumed without clear basis | Assumption only | 🔴 Not grounded, block |
| 10-19% | Contradicted by artifacts | Evidence suggests task is wrong | 🔴 Block and investigate |
| 0% | No evidence found | Task not mentioned anywhere | 🔴 Block and remove |

### Evidence Types (Weighted)

| Evidence Type | Weight | Example |
|---------------|--------|---------|
| Explicit specification | 100% | "Add LifelineAutoRoleAssignment to TenantFeatureFlag" |
| Direct reference | 80% | "Feature flag for auto-assignment" (context implies) |
| Schema/API reference | 70% | Field exists in data model, implies usage |
| Pattern inference | 60% | Similar features use this pattern |
| External dependency | 50% | "Depends on spec.md requirement FR-001" |
| Assumption | 20% | "Probably need this based on similar features" |
| No evidence | 0% | Task appears out of nowhere |

---

## ⚡ Decision Frameworks

### Decision Tree: Fast Path

```
                    Is tasks.md ready for review?
                              ↓
                         YES / NO?
                        /         \
                       NO          YES
                        ↓           ↓
                  (Get artifacts)  Continue
                        ↓           ↓
                   (Try again)      ↓
                                    ↓
                    Have you read validation checklists?
                              ↓
                         YES / NO?
                        /         \
                       NO          YES
                        ↓           ↓
                   (Read them)     ↓
                        ↓          ↓
                   (Try again)      ↓
                                    ↓
                    Score Phase 1 & Phase 2 tasks
                    Using grounding scale (0-100%)
                              ↓
                    ┌─────────┬─────────┬─────────┐
                    ↓         ↓         ↓         ↓
                  All ≥80%  Mix 70-90%  Many <70%  Most <50%
                    ↓         ↓         ↓         ↓
                  APPROVE   CLARIFY   CLARIFY   BLOCK
```

### Approval Matrix (Simple)

```
Phase 1 Tasks Grounding          Decision
────────────────────────────────────────────────
≥90% tasks at ≥80%     ────────>  ✅ APPROVE
70-89% tasks at ≥80%   ────────>  ⚠️  CLARIFY
<70% tasks at ≥80%     ────────>  🔴 BLOCK


Phase 2 Tasks Grounding          Decision
────────────────────────────────────────────────
≥80% tasks at ≥70%     ────────>  ✅ APPROVE
60-79% tasks at ≥70%   ────────>  ⚠️  CLARIFY
<60% tasks at ≥70%     ────────>  🔴 BLOCK


Phase 3+ Tasks Grounding         Decision
────────────────────────────────────────────────
≥70% tasks at ≥60%     ────────>  ✅ APPROVE
50-69% tasks at ≥60%   ────────>  ⚠️  CLARIFY
<50% tasks at ≥60%     ────────>  🔴 BLOCK
```

### Risk × Grounding Matrix

```
                         Grounding Level
                    100%    80%    60%    40%    20%
            ┌──────────────────────────────────────────────
        High│  ⚠️    🔴    🔴    🔴    🔴
  Risk      │
        Med │  ✅    ⚠️    ⚠️    🔴    🔴
        Level
        Low │  ✅    ✅    ⚠️    ⚠️    🔴
            │
            └──────────────────────────────────────────────

Legend:
✅ = Approve (low risk, high confidence)
⚠️  = Clarify (medium risk, needs review)
🔴 = Block (high risk, return to planning)
```

### Gap Severity × Impact Matrix

```
                    Implementation Impact
          ┌─────────────────────────────────────────
Severity  │  Low      Medium    High      Critical
──────────┼─────────────────────────────────────────
Critical  │  Block    Block     Block     Block
High      │  Clarify  Block     Block     Block
Medium    │  Clarify  Clarify   Block     Block
Low       │  Approve  Clarify   Clarify   Block
          └─────────────────────────────────────────
```

---

## 🚨 Red Flags Checklist

### Critical Red Flags (Automatic Block)

- [ ] >50% of tasks have <50% grounding level
- [ ] Critical gaps unresolved (data integrity, security, compliance)
- [ ] Major artifact contradictions (conflicting requirements)
- [ ] No primary artifact exists (spec.md or plan.md missing)
- [ ] Task contradicts existing artifact specifications
- [ ] High-risk tasks without mitigation plans

### Warning Red Flags (Needs Clarification)

- [ ] ≥30% of tasks have 50-69% grounding level
- [ ] Multiple consistency check failures
- [ ] External references not verified
- [ ] Pattern assumptions not documented
- [ ] Risk assessments incomplete
- [ ] Gap analysis missing actionable resolutions

### Quality Red Flags (Review Required)

- [ ] Inconsistent scoring methodology
- [ ] Evidence quotes lack context
- [ ] Risk factors not specific
- [ ] Recommendations not actionable
- [ ] Report structure incomplete
- [ ] Task coverage gaps

---

## 📝 Report Template Structure

### Required Sections

```markdown
# Task Grounding Analysis: [Feature-ID]
**Date**: [YYYY-MM-DD]
**Reviewer**: [Name]

## Executive Summary
[1-2 paragraphs summarizing overall grounding quality, key findings, and recommendation]

## Summary Table
| Phase | Status | Tasks | Grounded | Risk Level |
|-------|--------|-------|----------|------------|
| Phase 1 | ✅ Approved | 5/5 | 95% | Low |
| Phase 2 | ⚠️ Needs Clarification | 3/3 | 75% | Medium |

## Phase 1: [Phase Name] - Detailed Analysis

### Task T001: [Task Title]
**File**: [path/to/file.cs]
**Grounding Level**: 100%
**Primary Artifact**: [artifact.md > Section]
**Match Type**: explicit
**Evidence**: "[Quoted text with context]"
**Risk Assessment**: 🟢 Low risk - Explicitly specified

### Task T002: [Task Title]
[... continue for each task ...]

## Cross-Artifact Consistency Checks
[Validation that artifacts don't contradict each other]

## Critical Gaps & Resolutions
[List any gaps with specific resolution steps]

## Risk Assessment Summary
[Overall risk evaluation]

## Recommendations
[Clear action items for next steps]

## Decision Gate
**Status**: ✅ APPROVED / ⚠️ NEEDS CLARIFICATION / 🔴 BLOCKED
**Rationale**: [Brief explanation]
**Next Steps**: [What happens next]
```

---

## 🔧 Customization Points

### Adjust Grounding Thresholds

**Conservative** (High quality bar):
- Phase 1: ≥95% tasks at ≥90% grounding
- Phase 2: ≥90% tasks at ≥80% grounding
- Phase 3+: ≥80% tasks at ≥70% grounding

**Standard** (Balanced - Recommended):
- Phase 1: ≥90% tasks at ≥80% grounding
- Phase 2: ≥80% tasks at ≥70% grounding
- Phase 3+: ≥70% tasks at ≥60% grounding

**Lenient** (Faster approval):
- Phase 1: ≥80% tasks at ≥70% grounding
- Phase 2: ≥70% tasks at ≥60% grounding
- Phase 3+: ≥60% tasks at ≥50% grounding

### Customize Artifact Schema

**Default Artifacts**:
```yaml
required_artifacts:
  - spec.md: {type: specification, weight: 100}
  - plan.md: {type: planning, weight: 90}
  - data-model.md: {type: design, weight: 85}
  - api-contracts.md: {type: interface, weight: 80}
  - research.md: {type: research, weight: 60}
  - quickstart.md: {type: documentation, weight: 50}
```

**Custom Artifacts** (add your own):
```yaml
custom_artifacts:
  - architecture.md: {type: architecture, weight: 95}
  - security-review.md: {type: security, weight: 100}
  - performance.md: {type: performance, weight: 75}
```

### Adjust Match Type Weights

**Default Weights**:
- explicit: 100%
- reference: 80%
- implicit: 60%
- external: 50%

**Custom Weights** (for your project):
- explicit: 100%
- reference: 85%
- implicit: 70%
- external: 40%

---

## 📊 Quality Standards

### Traceability Standards

- [ ] Every task links to ≥1 artifact
- [ ] Evidence quotes include context (sentence before/after)
- [ ] Artifact references are specific (section/title)
- [ ] Cross-references between artifacts validated
- [ ] No circular references or assumptions

### Evidence Standards

- [ ] Primary evidence is from authoritative artifact (spec.md > plan.md > data-model.md)
- [ ] Secondary evidence supports primary (not contradicts)
- [ ] Evidence is current (not outdated references)
- [ ] Evidence is complete (not partial quotes)
- [ ] Evidence is accurate (quotes match artifacts)

### Risk Assessment Standards

- [ ] Risk level correlates with grounding level
- [ ] Risk factors are specific and measurable
- [ ] Mitigation steps are actionable
- [ ] Risk assessment considers implementation impact
- [ ] Risk assessment includes timeline impact

---

## 🎯 Common Issues & Solutions

### Issue: Tasks not grounded in artifacts
**Symptoms**: Many tasks at 0-30% grounding
**Root Cause**: Planning incomplete or tasks invented during implementation
**Solution**:
- Return to planning phase
- Add missing specifications to artifacts
- Remove unneeded tasks

### Issue: Artifact inconsistencies
**Symptoms**: Cross-check failures, contradictory requirements
**Root Cause**: Artifacts not synchronized during planning
**Solution**:
- Update all artifacts to reflect current requirements
- Clarify ambiguities with product owner
- Regenerate tasks.md after artifact updates

### Issue: Weak evidence quality
**Symptoms**: Tasks at 40-60% with thin evidence
**Root Cause**: Planning artifacts lack detail or specificity
**Solution**:
- Enhance artifact detail during planning
- Add implementation examples to specifications
- Use pattern documentation for similar features

### Issue: Risk assessments incomplete
**Symptoms**: Generic risk factors, missing mitigations
**Root Cause**: Reviewers rushing through validation
**Solution**:
- Use detailed risk assessment template
- Consider implementation, testing, and maintenance risks
- Include specific mitigation actions

---

## 📋 Reviewer Checklist (Final)

- [ ] All required artifacts exist (minimum 5/7)
- [ ] Every task from tasks.md is analyzed
- [ ] Grounding level assigned to each task (0-100%)
- [ ] Evidence quotes accurate and contextual
- [ ] Consistency checks completed
- [ ] Gaps identified with resolutions
- [ ] Risk assessment complete for all tasks
- [ ] Decision gate clearly stated
- [ ] Report structure follows template
- [ ] Recommendations are actionable

---

**This FRAMEWORK.md contains the complete methodology for task grounding validation. Use [TOOLS.md](TOOLS.md) for practical templates and [IMPLEMENTATION.md](IMPLEMENTATION.md) for setup instructions.**