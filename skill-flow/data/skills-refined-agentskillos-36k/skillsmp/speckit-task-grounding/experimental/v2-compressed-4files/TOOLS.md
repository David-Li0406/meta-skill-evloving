# Task Grounding Validation - Tools & Templates
**Version**: 2.0.0 (Compressed) | **Purpose**: Practical checklists, templates, and reference materials
**Date**: January 12, 2026

---

## 📋 REVIEWER QUICK CHECKLIST (Print This!)

**Feature**: _________________ **Date**: _______ **Reviewer**: _____________

### PRE-REVIEW (5 min)
- [ ] All artifacts exist? (spec.md, plan.md, tasks.md, data-model.md, api-contracts.md)
- [ ] tasks.md is latest version?
- [ ] I have decision matrix open

### PHASE 1 REVIEW (10 min)
**Count tasks at ≥80% grounding** (Use 0-100 scale)

| Task | Grounding | ✅/⚠️/🔴 | Notes |
|------|-----------|---------|-------|
| T001 | ___% | ☐ | ________________ |
| T002 | ___% | ☐ | ________________ |
| T003 | ___% | ☐ | ________________ |
| T004 | ___% | ☐ | ________________ |
| T005 | ___% | ☐ | ________________ |

**Phase 1 Average**: ___% **Threshold**: ≥80%, ≥90% of tasks
**Status**: ☐ OK | ☐ Low | ☐ Block

### PHASE 2 REVIEW (10 min)
**Count tasks at ≥70% grounding**

| Task | Grounding | ✅/⚠️/🔴 | Notes |
|------|-----------|---------|-------|
| T006 | ___% | ☐ | ________________ |
| T007 | ___% | ☐ | ________________ |
| T008 | ___% | ☐ | ________________ |
| T009 | ___% | ☐ | ________________ |
| T010 | ___% | ☐ | ________________ |

**Phase 2 Average**: ___% **Threshold**: ≥70%, ≥80% of tasks
**Status**: ☐ OK | ☐ Low | ☐ Block

### CONSISTENCY CHECK (5 min)
**Do artifacts agree on**:
- [ ] Permission counts (CoHost 14, Participant 4)
- [ ] Role mapping (CoHost → "Lifeline CoHost")
- [ ] Feature flag names (LifelineAutoRoleAssignment)
- [ ] Seeder pattern (ICustomSeeder)
- [ ] Event names (SessionGroupParticipantInvitationAcceptedEvent)

**Inconsistencies found**: ___________________________________________

### GAP ANALYSIS (5 min)
**Count critical gaps** (things that block implementation):

| Gap | Critical? | Mitigation | Action |
|-----|-----------|-----------|--------|
| ________________ | Y/N | __________ | __________ |
| ________________ | Y/N | __________ | __________ |
| ________________ | Y/N | __________ | __________ |

**Total Gaps**: ___  **Critical**: ___

### RISK ASSESSMENT (3 min)
**Count high-risk tasks** (grounding <50% OR high complexity):

| Task | Risk | Reason | Mitigation |
|------|------|--------|-----------|
| ____ | H/M/L | ______ | __________ |
| ____ | H/M/L | ______ | __________ |

**High-risk count**: ___

### FINAL DECISION (2 min)

Use this table:

```
Phase 1 ≥80%?    Phase 2 ≥70%?    Gaps <3?    High Risks <2?    Decision
─────────────────────────────────────────────────────────────────────────
YES              YES               YES         YES               ✅ APPROVE
YES              YES               YES         NO                ⚠️  CLARIFY
YES              NO                YES         YES               ⚠️  CLARIFY
NO               Any               Any         Any               🔴 BLOCK
```

**FINAL DECISION**: ☐ ✅ APPROVE | ☐ ⚠️ CLARIFY | ☐ 🔴 BLOCK

**Confidence Level**: ☐ 🟢 High (≥80%) | ☐ 🟡 Medium (50-79%) | ☐ 🔴 Low (<50%)

---

## 📊 SCORE CHEAT SHEET

### Grounding Levels
```
100% = Explicit in primary artifact ("Add X to file Y")
 90% = Detailed example code provided
 80% = Clear specification with reference
 70% = Documented with pattern to infer from
 60% = Weakly documented, multiple sources needed
 50% = Inferred from multiple artifacts
 40% = Weak inference from single source
 30% = Assumed with some basis
 20% = Assumed without clear basis
 10% = Contradicted by artifacts
  0% = No evidence found
```

### Evidence Types (Weight Order)
1. **Explicit specification**: "Add X to Y" → 100%
2. **Detailed example**: Code/SQL example shown → 90%
3. **Reference + context**: "Section X covers Y" → 80%
4. **Schema/pattern reference**: "See contracts/ folder" → 70%
5. **Implied requirement**: "Following pattern from [artifact]" → 60%
6. **Architectural principle**: "Per Clean Architecture" → 50%
7. **Common practice**: "Standard in similar features" → 40%
8. **Developer assumption**: "Likely needed based on..." → 20%
9. **No evidence**: "Task invented" → 0%

---

## 📝 SCORING EXAMPLES

### Well-Grounded Task (100%)
```
Task: T001 Add TenantFeatureFlag enum value

Artifact: data-model.md > Feature Flags
Evidence: "Location: src/Core/Shared/FeatureManagement/FeatureFlags.cs
           New Value: [Display(Name = "X")] LifelineAutoRoleAssignment"

Assessment: ✅ Fully Grounded (100%)
```

### Partially Grounded Task (70%)
```
Task: T003 Add role name constants

Artifact: plan.md > Project Structure (references FSHPermissions.cs)
Secondary: data-model.md > Seeder (uses hardcoded "Lifeline CoHost")

Assessment: ⚠️ Partially Grounded (70%)
Issue: Plan doesn't mention FSHRoles.cs, inferred from pattern
Action: Verify codebase has FSHRoles pattern before executing
```

### Weakly Grounded Task (50%)
```
Task: T004 Define SentEvent

Artifact: api-contracts.md > schemas (references schema file, not documented)
Secondary: None clear

Assessment: 🔴 Weakly Grounded (50%)
Issue: Event definition not specified in any artifact
Action: Add event specification to api-contracts.md
```

---

## 🛠️ TEMPLATE: TASK_GROUNDING_ANALYSIS.md

```markdown
# Task Grounding Analysis: [FEATURE_NAME]
**Feature**: [FEATURE_ID] | **Date**: [DATE]
**Status**: 🔄 In Review

---

## Executive Summary

[1-2 paragraphs summarizing overall grounding quality, key findings, and recommendation]

## Summary Table
| Phase | Status | Tasks | Grounded | Risk |
|-------|--------|-------|----------|------|
| Phase 1 | ✅ Approved | 5/5 | 95% | Low |
| Phase 2 | ⚠️ Needs Clarification | 3/3 | 75% | Medium |

---

## Phase 1: [Phase Name] - Detailed Analysis

### Task T001: [Task Title]

**Artifact Mapping**:
- **Primary**: [artifact.md - Section]
- **Secondary**: [artifact2.md, artifact3.md]
- **Grounding Level**: [0-100%]

**Evidence**:
[Copy quote from artifact with context]

**Assessment**: [Fully/Partially/Weakly Grounded]
- ✅ [Positive finding]
- ⚠️ [Concern if any]

[Repeat for each task...]

---

## Cross-Artifact Consistency Checks

| Item | Artifact A | Artifact B | Match |
|------|-----------|-----------|-------|
| [Item] | [Value] | [Value] | ✅ |

---

## Critical Gaps & Resolutions

### Gap: [Specific Gap Title]
**Related Tasks**: T[NNN], T[MMM]
**Root Cause**: [Why this gap exists]
**Impact**: [Why it matters]
**Resolution**:
- [ ] [Actionable step 1]
- [ ] [Actionable step 2]
- [ ] [Actionable step 3]

---

## Risk Assessment Summary

| Risk Level | Tasks | Mitigation Required |
|------------|-------|-------------------|
| 🟢 Low | [N] | None |
| 🟡 Medium | [N] | Verification needed |
| 🔴 High | [N] | Block until resolved |

---

## Recommendations

### Immediate Actions
- [ ] [Action for next 1-2 days]

### Before Implementation
- [ ] [Action before coding starts]

### During Implementation
- [ ] [Action during development]

---

## Decision Gate

**Status**: ✅ APPROVED / ⚠️ NEEDS CLARIFICATION / 🔴 BLOCKED

**Rationale**:
[Brief explanation of decision based on grounding levels, gaps, and risks]

**Next Steps**:
[What happens next based on decision]

**Reviewer**: [Your Name]
**Date**: [YYYY-MM-DD]
```

---

## 📋 VALIDATION CHECKLIST (Detailed)

### Before you approve, verify:

| Item | Check | Status |
|------|-------|--------|
| All tasks from tasks.md listed | ☐ | |
| Each task has grounding 0-100% | ☐ | |
| Phase 1 avg ≥80% grounding | ☐ | |
| Phase 2 avg ≥70% grounding | ☐ | |
| No task with 0% grounding | ☐ | |
| Gaps clearly identified | ☐ | |
| Risks rated (Low/Med/High) | ☐ | |
| Decision gate marked | ☐ | |
| No contradictions vs spec | ☐ | |
| External refs verified | ☐ | |

**If ≥9/10 checked**: → Ready to review

---

## 🚨 RED FLAGS CHECKLIST

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

## 📊 METRICS DASHBOARD TEMPLATE

```markdown
# Task Grounding Metrics Dashboard
**Generated**: [DATE]

## Overall Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Features Analyzed | [N] | - | - |
| First-Time Approval | [N]% | ≥75% | [✅/⚠️] |
| Average Grounding | [N]% | ≥80% | [✅/⚠️] |
| Gap Resolution | [N]% | ≥90% | [✅/⚠️] |

## Trends

[Chart showing grounding levels over time]

## Recent Validations

| Feature | Date | Grounding | Decision | Gaps |
|---------|------|-----------|----------|------|
| [Feature] | [Date] | [N]% | [Decision] | [N] |

---
*Auto-generated by generate-metrics-dashboard.ps1*
```

---

## 🏷️ APPROVAL SIGNATURE TEMPLATE

```markdown
## Approval Signature

**Feature**: [FEATURE_NAME]
**Reviewer**: [REVIEWER_NAME]
**Date**: [DATE]

### Grounding Assessment
- **Phase 1 Average**: [N]% (Target: ≥80%)
- **Phase 2 Average**: [N]% (Target: ≥70%)
- **Critical Gaps**: [N] identified, [N] resolved
- **High Risks**: [N] identified, [N] mitigated

### Decision
**Status**: ☐ ✅ APPROVED | ☐ ⚠️ NEEDS CLARIFICATION | ☐ 🔴 BLOCKED

**Rationale**:
[Detailed explanation of decision]

**Conditions for Approval** (if applicable):
- [ ] [Condition 1]
- [ ] [Condition 2]
- [ ] [Condition 3]

**Reviewer Signature**: ___________________________
**Date**: __________

### Follow-up Actions
- [ ] Update artifacts if clarification needed
- [ ] Regenerate tasks.md if blocked
- [ ] Schedule implementation kickoff
- [ ] Monitor for issues during implementation
```

---

## 📈 COMMON SCENARIOS & DECISIONS

### Scenario 1: Well-Grounded Feature (APPROVE)
**Grounding**: Phase 1: 95%, Phase 2: 85%
**Gaps**: 1 minor gap with clear resolution
**Risks**: All low to medium
**Decision**: ✅ APPROVE
**Rationale**: Meets all thresholds, gaps resolvable

### Scenario 2: Mixed Quality (CLARIFY)
**Grounding**: Phase 1: 88%, Phase 2: 65%
**Gaps**: 3 gaps requiring artifact updates
**Risks**: 2 medium risks
**Decision**: ⚠️ CLARIFY
**Rationale**: Phase 2 below threshold, gaps need resolution

### Scenario 3: Poorly Grounded (BLOCK)
**Grounding**: Phase 1: 45%, Phase 2: 30%
**Gaps**: 7 critical gaps, major inconsistencies
**Risks**: 5 high risks
**Decision**: 🔴 BLOCK
**Rationale**: Below minimum thresholds, return to planning

### Scenario 4: MVP with Assumptions (CLARIFY)
**Grounding**: Phase 1: 75%, Phase 2: 55%
**Gaps**: 2 assumptions documented as "MVP scope"
**Risks**: 1 high risk for scalability
**Decision**: ⚠️ CLARIFY
**Rationale**: Close to thresholds but assumptions need validation

---

## 🔧 TROUBLESHOOTING QUICK REFERENCE

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

## 📚 GLOSSARY

### Artifact Types
- **spec.md**: Requirements specification (highest authority)
- **plan.md**: Technical implementation plan
- **data-model.md**: Data structures and schemas
- **api-contracts.md**: API interfaces and contracts
- **research.md**: Research findings and decisions
- **quickstart.md**: Implementation guides

### Grounding Concepts
- **Primary Artifact**: Main source of task requirements
- **Secondary Artifact**: Supporting evidence
- **Match Type**: How strongly task connects to artifact (explicit/reference/implicit/external)
- **Evidence Quote**: Direct text from artifact proving task requirement
- **Grounding Level**: 0-100% confidence score
- **Gap**: Missing requirement or unclear specification
- **Risk**: Implementation uncertainty or complexity

### Decision Terms
- **Approved**: Meets thresholds, proceed to implementation
- **Needs Clarification**: Minor issues, update artifacts then proceed
- **Blocked**: Major issues, return to planning phase
- **Confidence Level**: Overall assessment quality (High/Medium/Low)

---

## 🎯 QUICK DECISION REFERENCE

### Phase Thresholds
- **Phase 1** (Setup): ≥90% tasks at ≥80% grounding
- **Phase 2** (Foundation): ≥80% tasks at ≥70% grounding
- **Phase 3+** (Features): ≥70% tasks at ≥60% grounding

### Risk Thresholds
- **Low Risk**: ≥90% grounding, no gaps
- **Medium Risk**: 70-89% grounding, resolvable gaps
- **High Risk**: <70% grounding, critical gaps

### Gap Thresholds
- **Acceptable**: <3 gaps, all with clear resolutions
- **Concerning**: 3-5 gaps, some requiring major changes
- **Blocking**: >5 gaps, critical functionality affected

---

**This TOOLS.md provides practical templates and references. Use [FRAMEWORK.md](FRAMEWORK.md) for methodology and [IMPLEMENTATION.md](IMPLEMENTATION.md) for setup.**