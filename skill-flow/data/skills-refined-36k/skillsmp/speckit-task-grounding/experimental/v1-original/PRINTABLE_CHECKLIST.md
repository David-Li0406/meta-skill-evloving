# Task Grounding Validation - Printable Checklist
**Print this page for quick reference during task review**

---

## 📋 REVIEWER QUICK CHECKLIST (Use this!)

**Feature**: _________________ **Date**: _______ **Reviewer**: _____________

### PRE-REVIEW (5 min)
- [ ] All artifacts exist? (spec.md, plan.md, tasks.md, data-model.md, api-contracts.md)
- [ ] tasks.md is latest version?
- [ ] I have DECISION_MATRIX.md open

### PHASE 1 REVIEW (10 min)
**Count tasks at ≥80% grounding** (Use 0-100 scale from VALIDATION_CHECKLIST.md)

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

## 📝 SCORE CHEAT SHEET (Keep handy while reviewing)

### Grounding Levels
```
100% = Explicit in primary artifact ("Add X to file Y")
 90% = Detailed example code provided
 80% = Clear specification with reference
 70% = Documented with pattern to infer from
 60% = Weakly documented, multiple sources needed
 50% = Inferred from design/pattern
 40% = Implicit architectural pattern
 20% = Assumption without evidence
  0% = No evidence found
```

### Task Count Rules
```
Phase 1: Need ≥90% of tasks at ≥80% → APPROVE
         Example: 10 tasks → 9+ must be ≥80%

Phase 2: Need ≥80% of tasks at ≥70% → APPROVE
         Example: 10 tasks → 8+ must be ≥70%

Phase 3+: Need ≥70% of tasks at ≥60% → APPROVE
          Example: 15 tasks → 11+ must be ≥60%
```

### Evidence Types (Weight)
```
Explicit (100%)       = "Add X to Y"
Example (90%)         = Code example shown
Reference (70%)       = "See Section Z"
Pattern (50%)         = "Follow pattern X"
Assumption (20%)      = "Likely needed for..."
No Evidence (0%)      = Task invented
```

---

## 🚦 RED FLAGS (Stop & Ask)

If you see ANY of these, ask for clarification:

- [ ] ❌ Task with 0% grounding in Phase 1
- [ ] ❌ Same artifact cited for >70% of tasks
- [ ] ❌ "Grounding unknown" in final report
- [ ] ❌ Task contradicts documented requirement
- [ ] ❌ >30% of gaps marked "discuss in implementation"
- [ ] ❌ External ref (spec.md) not verified
- [ ] ❌ Artifact inconsistencies unresolved
- [ ] ❌ No risk mitigation for high-risk tasks

---

## ✅ APPROVAL CHECKLIST (Must ALL be ✅)

- [ ] ≥90% Phase 1 tasks ≥80% grounded
- [ ] ≥80% Phase 2 tasks ≥70% grounded
- [ ] ≥70% Phase 3+ tasks ≥60% grounded
- [ ] All gaps have mitigation
- [ ] No artifact contradictions
- [ ] All external refs verified
- [ ] Risks documented
- [ ] Decision gate clear
- [ ] Team capacity OK
- [ ] Implementation can start

**If ALL checked**: ✅ APPROVE
**If 8/10 checked**: ⚠️ CLARIFY
**If <8/10 checked**: 🔴 BLOCK

---

## 📌 COMMON ARTIFACTS & LOCATIONS

```
spec.md            → Feature requirements, user stories, acceptance criteria
plan.md            → Technical context, architecture, schedule
data-model.md      → Entities, tables, relationships, migrations
api-contracts.md   → Endpoints, events, DTOs, security
research.md        → Technical decisions, justifications
quickstart.md      → Dev quick start, implementation notes
tasks.md           → The thing you're validating
```

---

## 🎯 WHAT YOU'RE LOOKING FOR

For each task ask:

1. **Why this task?** → Find in artifact (spec or plan)
2. **What does it do?** → Find in data-model or api-contracts
3. **How implement?** → Find in research or quickstart
4. **File path correct?** → Match against actual structure
5. **Dependencies clear?** → Listed in task description
6. **Risk level?** → Rate Low/Medium/High
7. **Missing info?** → List as gap

---

## 💡 QUICK SCORING EXAMPLES

### Example 1: T001 - Add enum value
```
Found in:
- plan.md (mentions feature flag needed)        ✅ 70%
- data-model.md (exact location & name)         ✅ 100%
Average: 85% → ✅ GOOD SCORE
```

### Example 2: T003 - Add role constants
```
Found in:
- plan.md (no mention of FSHRoles pattern)      ❌ 0%
- data-model.md (uses hardcoded strings)        ⚠️  50%
- Inferred from FSHPermissions pattern          ⚠️  40%
Average: 30% → 🔴 WEAK, NEEDS VERIFICATION
```

### Example 3: T004 - Define SentEvent
```
Found in:
- api-contracts.md (schema reference only)      ⚠️  50%
- spec.md (not provided, external ref)          ❓ 30%
- No pattern in codebase for reference          ❌ 0%
Average: 27% → 🔴 HIGH RISK, BLOCK PHASE 2
```

---

## 🔄 DECISION TREE (Quick Decision)

```
                    Start here ➡ All Phase 1-2 ≥70% avg?
                                      ↙         ↘
                                    YES        NO
                                     ↓          ↓
                              Gaps <5?    → 🔴 BLOCK
                             ↙      ↘
                           YES      NO
                            ↓        ↓
                        Risks OK? → 🔴 BLOCK
                       ↙      ↘
                     YES      NO
                      ↓        ↓
                   ✅ APPROVE  ⚠️ CLARIFY
```

---

## 📊 SIMPLE SCORING TEMPLATE

**Copy this for each Phase**:

```
PHASE X: [Phase Name]
─────────────────────────────────────────────
Total Tasks: ___
At ≥80% grounding: ___ / ___ = ___% ✅/⚠️/🔴
At 70-79% grounding: ___ / ___
At <70% grounding: ___

Threshold needed: [Check rules above]
Current: ___ %
Status: ✅ OK / ⚠️ LOW / 🔴 FAIL

Notes: ___________________________________
```

---

## 💬 REVIEWER SIGN-OFF

**Use this when done**:

```
═══════════════════════════════════════════════
TASK GROUNDING VALIDATION - SIGN-OFF
───────────────────────────────────────────────
Feature: _______________________________
Reviewer: ______________________________
Date: __________________________________

Overall Status: ☐ ✅ APPROVED
                ☐ ⚠️ NEEDS CLARIFICATION
                ☐ 🔴 BLOCKED

Confidence: ☐ 🟢 High  ☐ 🟡 Medium  ☐ 🔴 Low

Key Findings:
├─ Phase 1 Grounding: ____%
├─ Phase 2 Grounding: ____%
├─ Gaps Identified: ___
└─ High Risks: ___

Next Steps: ___________________________________

Signature: ______________________________
═══════════════════════════════════════════════
```

---

## 📞 WHO TO CONTACT

- **Questions about process**: See README.md
- **Scoring help**: See VALIDATION_CHECKLIST.md > Grounding Level Scale
- **Decision help**: See DECISION_MATRIX.md
- **Integration help**: See INTEGRATION_GUIDE.md
- **Quick ref**: See QUICK_REFERENCE.md

---

## ⏱️ TIME BUDGET

```
Activity               Time    Critical?
─────────────────────────────────────────
Pre-review check       5 min   ✅ Yes
Phase 1 scoring       10 min   ✅ Yes
Phase 2 scoring       10 min   ✅ Yes
Consistency check      5 min   ✅ Yes
Gap analysis           5 min   ✅ Yes
Risk assessment        3 min   ✅ Yes
Final decision         2 min   ✅ Yes
─────────────────────────────────────────
TOTAL               40 min   Can shorten to
                             15-20 min with
                             practice
```

---

**Print & keep handy during reviews!**
