# Task Grounding Validation Decision Matrix
**Version**: 1.0.0 | **Purpose**: Quick decision-making tool for task grounding approval

---

## Decision Tree: Fast Path

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
                    Have you read VALIDATION_CHECKLIST.md?
                              ↓
                         YES / NO?
                        /         \
                       NO          YES
                        ↓           ↓
                   (Read it)       ↓
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

---

## Approval Matrix (Simple)

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

---

## Risk × Grounding Matrix

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

---

## Gap Severity × Impact Matrix

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

## Confidence Level Mapping

```
Confidence    Approval       Recommended Action
─────────────────────────────────────────────────────
🟢 90-100%   APPROVED       → Proceed immediately
             (High)

🟢 80-89%    APPROVED       → Proceed, monitor execution
             (Medium)

🟡 70-79%    NEEDS CLF.     → Update artifacts (minor)
             (Moderate)

🟡 50-69%    NEEDS CLF.     → Return to planning
             (Low)

🔴 <50%      BLOCKED        → Major return to planning
             (Very Low)
```

---

## Task Count Evaluation

```
Given: Total tasks in Phase = N

Phase 1 Rule:
└─ If ≥90% of N tasks are ≥80% grounded → ✅ APPROVE
   Example: 10 tasks → 9+ must be ≥80% → APPROVE

Phase 2 Rule:
└─ If ≥80% of N tasks are ≥70% grounded → ✅ APPROVE
   Example: 10 tasks → 8+ must be ≥70% → APPROVE

Phase 3+ Rule:
└─ If ≥70% of N tasks are ≥60% grounded → ✅ APPROVE
   Example: 20 tasks → 14+ must be ≥60% → APPROVE
```

### Calculate Your Percentage

```
Example: Phase 1 has 5 tasks
├─ T001: 100% ✅
├─ T002: 100% ✅
├─ T003: 70% ✅
├─ T004: 70% ✅
└─ T005: 60% ❌

Result: 4/5 = 80% at ≥80%
Needed: ≥90% (4.5/5 = need 5/5)
Decision: ⚠️ NEEDS CLARIFICATION
```

---

## Artifact Coverage Check

```
Artifact Status                   Action
─────────────────────────────────────────────────────
7/7 artifacts present            ✅ Full validation
5-6/7 artifacts present          ✅ Proceed (minor gap)
4/7 artifacts present            ⚠️  Proceed with caution
3/7 artifacts present            ⚠️  Validate externals
<3/7 artifacts present           🔴 Return to planning
```

---

## External Reference Validation

```
Task cites spec.md FR-###
           ↓
    Is FR-### in spec.md?
       /     \
      YES    NO
       ↓      ↓
    ✅OK    ❌Invalid
             reference
```

## Consistency Check Scoring

```
Artifact Pairs Checked:
  spec ↔ plan        □ Consistent ✅
  plan ↔ data-model  □ Consistent ✅
  data-model ↔ api   □ Consistent ✅

Consistency Score: 3/3 = 100%
  ≥90% → ✅ Approve
  70-89% → ⚠️ Clarify
  <70% → 🔴 Block
```

---

## Implementation Readiness Score

```
Criteria (each item = 10%)
────────────────────────────────────
□ All artifacts exist (10%)
□ Phase 1 tasks ≥80% grounded (10%)
□ Phase 2 tasks ≥70% grounded (10%)
□ No contradictions in artifacts (10%)
□ All gaps identified (10%)
□ Risk assessment complete (10%)
□ No external refs missing (10%)
□ Decision gate clear (10%)
□ Recommendations actionable (10%)
□ Team acknowledges risks (10%)
────────────────────────────────────
Total: ___/100%

Score Range: Action
80-100%     → ✅ Approve
60-79%      → ⚠️ Clarify
<60%        → 🔴 Block
```

---

## Common Scenarios

### Scenario 1: Phase 1 - All tasks well-grounded

```
Phase 1: 5 tasks
├─ T001: 100% (spec.md + plan.md)
├─ T002: 95% (data-model.md + api-contracts.md)
├─ T003: 85% (plan.md + implicit pattern)
├─ T004: 80% (plan.md explicit)
└─ T005: 75% (inferred from design)

Average: 87%
Threshold: ≥90% at ≥80%
Result: 5/5 (100%) meet threshold

Decision: ✅ APPROVE
```

### Scenario 2: Phase 2 - Some gaps present

```
Phase 2: 4 tasks
├─ T006: 90% (api-contracts.md)
├─ T007: 70% (plan.md + implicit)
├─ T008: 65% (research.md only)
└─ T009: 50% (external spec ref, unverified)

Count ≥70%: 2/4 (50%)
Threshold: ≥80% meet ≥70%
Result: 50% < 80% threshold

Decision: ⚠️ NEEDS CLARIFICATION

Actions:
- Verify spec.md FR-### for T009
- Update research.md for T008
- Regenerate tasks.md
```

### Scenario 3: Phase 1 - Critical gaps

```
Phase 1: 6 tasks
├─ T001: 100% ✅
├─ T002: 95% ✅
├─ T003: 40% ❌ (pattern not documented)
├─ T004: 35% ❌ (external ref unverified)
├─ T005: 30% ❌ (assumption without evidence)
└─ T006: 20% ❌ (task invented?)

Count ≥80%: 2/6 (33%)
Threshold: ≥90% meet ≥80%
Result: 33% << 90% threshold

Decision: 🔴 BLOCKED

Reason: >50% of critical phase tasks <60% grounded
Action: Return to planning phase
- Validate artifact schema
- Document missing design patterns
- Resolve external dependencies
- Remove invented tasks
```

---

## Quick Approval Flow

```
START
  ↓
Validate artifacts exist
  ├─ Missing >2? → Get them (return to planning)
  └─ OK? ↓
  ↓
Score each task (0-100%)
  ├─ Any <30%? → Remove or document reason (high risk)
  └─ OK? ↓
  ↓
Calculate phase averages
  ├─ Phase 1 avg ≥80%? →✅
  ├─ Phase 2 avg ≥70%? →✅
  └─ Phase 3 avg ≥60%? →✅
  ↓
Check consistency
  ├─ Contradictions? → Flag as gaps
  └─ OK? ↓
  ↓
Assess risks
  ├─ High risks without mitigations? → Recommend block
  └─ OK? ↓
  ↓
Make decision
  ├─ All ✅? → APPROVE
  ├─ Some ⚠️? → NEEDS CLARIFICATION
  └─ Any 🔴? → BLOCK
  ↓
END: Document decision + next steps
```

---

## Blocker Checklist

**Mark 🔴 BLOCKED if ANY of these are true**:

- [ ] >33% of Phase 1 tasks <70% grounded
- [ ] >50% of Phase 2 tasks <60% grounded
- [ ] ≥2 critical tasks with 0% grounding
- [ ] Same artifact cited for >80% of tasks
- [ ] Artifact contradictions unresolved
- [ ] External refs (spec.md) unverified
- [ ] Major features missing from plan
- [ ] Task contradicts documented requirement
- [ ] >30% of gaps marked "TBD"
- [ ] No clear mitigation for high-risk items

---

## Approval Checklist

**Mark ✅ APPROVED only if ALL of these are true**:

- [ ] ≥90% Phase 1 tasks ≥80% grounded
- [ ] ≥80% Phase 2 tasks ≥70% grounded
- [ ] ≥70% Phase 3+ tasks ≥60% grounded
- [ ] Every gap has identified mitigation
- [ ] No artifact contradictions
- [ ] All external refs verified
- [ ] Implementation dependencies clear
- [ ] Team capacity confirmed
- [ ] Risks documented and acceptable
- [ ] Decision gate approved by lead

---

## Thresholds Customization

### For Different Project Phases

```
MVP Phase:
  Phase 1: 95% tasks ≥85% (higher bar)
  Phase 2: 85% tasks ≥75%

Growth Phase:
  Phase 1: 90% tasks ≥80% (standard)
  Phase 2: 80% tasks ≥70%

Maintenance:
  Phase 1: 85% tasks ≥75% (lower bar OK)
  Phase 2: 75% tasks ≥65%
```

### For Different Risk Tolerances

```
Low Risk Tolerance:
  Block if <85% avg grounding
  Block if >2 high-risk items

High Risk Tolerance:
  Approve if ≥70% avg grounding
  Approve if high-risk items documented
```

---

## Report Status Codes

```
✅ APPROVED              → Green light, proceed immediately
⚠️  NEEDS CLARIFICATION  → Yellow light, minor updates needed
🔴 BLOCKED               → Red light, return to planning
⏳ IN REVIEW             → Being analyzed, not ready yet
❓ UNKNOWN               → Not enough info to decide
```

---

## Decision Document Template

```markdown
# Decision: Task Grounding Approval for [Feature]

**Feature**: [ID] | **Date**: [Date] | **Reviewer**: [Name]

**Recommendation**: [✅ APPROVED / ⚠️ NEEDS CLARIFICATION / 🔴 BLOCKED]

**Confidence Level**: [🟢 High / 🟡 Medium / 🔴 Low]

**Key Metrics**:
- Phase 1 Grounding: [X]%
- Phase 2 Grounding: [X]%
- Identified Gaps: [N]
- Risk Level: [Low/Med/High]

**Reasoning**:
[2-3 sentences explaining decision]

**Next Steps**:
1. [Action]
2. [Action]
3. [Action]

**Approval**: _________________ **Date**: _______
```

---

## Integration with PR/Code Review

```markdown
# Pull Request Checklist for tasks.md

- [ ] Task grounding analysis reviewed
- [ ] All artifacts exist and validated
- [ ] ≥80% of Phase 1 tasks ≥80% grounded
- [ ] ≥70% of Phase 2 tasks ≥70% grounded
- [ ] All high-risk gaps documented
- [ ] Decision gate: ✅ Approved
- [ ] Implementation can begin

**Reviewer**: _________________ **Date**: _______
```

---

**Use this matrix during review → Fast, consistent decisions in 10-15 minutes**
