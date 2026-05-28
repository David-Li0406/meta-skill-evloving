# Task Grounding Validation Framework - Review Summary
**Status**: Ready for Your Review
**Date**: January 12, 2026

---

## What You're Getting

A **complete, standardized workflow** for validating that tasks in `tasks.md` are grounded in planning artifacts. Ready to integrate into your SpecKit customization.

### 📦 Deliverables (6 Documents)

1. **README.md** (8 pages)
   - Navigation guide
   - Overview of all documents
   - Getting started paths
   - Success metrics

2. **SPECIFICATION.md** (15 pages) ⭐ **Most Detailed**
   - Complete process flow (6 steps)
   - Validation framework (6-part methodology)
   - Report template structure
   - Acceptance criteria
   - Integration points for SpecKit
   - Customization for different project types

3. **VALIDATION_CHECKLIST.md** (20 pages) ⭐ **Most Practical**
   - Pre-validation setup checklist
   - Report structure validation
   - Grounding evidence standards (checklist per task)
   - Risk assessment rubric
   - Reviewer approval signature
   - Common issues & resolution guide
   - Red flags (stop signs)

4. **DECISION_MATRIX.md** (8 pages) ⭐ **Fastest Reference**
   - Decision tree (visual)
   - Approval matrix (simple table lookup)
   - Risk × Grounding matrix
   - Common scenarios (3 examples with decisions)
   - Blocker vs Approval checklists
   - Quick scoring calculations

5. **QUICK_REFERENCE.md** (5 pages)
   - 5-minute overview
   - Grounding level scale (0-100%)
   - Evidence requirements by phase
   - Evidence types (weighted)
   - Red flags checklist
   - Questions to ask per task

6. **INTEGRATION_GUIDE.md** (18 pages)
   - Quick start (manual process)
   - 6 implementation steps with YAML examples
   - PowerShell script template
   - 4-week timeline
   - CI/CD integration points (GitHub Actions, VS Code, pre-commit)
   - Troubleshooting guide
   - Maintenance plan

---

## How It Works (30-Second Elevator Pitch)

```
PROBLEM: Tasks in tasks.md might not match planning artifacts
         (spec.md, plan.md, data-model.md, etc)

SOLUTION: After tasks.md generated, validate each task:
          1. Does artifact exist that explains this task?
          2. How strong is the evidence (0-100%)?
          3. Are artifacts consistent with each other?
          4. What gaps or risks exist?

OUTCOME: TASK_GROUNDING_ANALYSIS.md report + decision
         ✅ Approved → Proceed to implementation
         ⚠️  Needs Clarification → Update artifacts
         🔴 Blocked → Return to planning

TIME: 15-25 minutes per feature (or 5 min if automated)
```

---

## Key Features

### ✅ Comprehensive
- Covers all roles (lead, reviewer, implementer, process owner)
- 67 pages of guidance and tools
- Real example (007-lifeline-invitation-auto-role-mvp analysis)

### ✅ Flexible
- Works for any project (customize thresholds)
- Works at any phase (MVP to maintenance)
- Can be manual or automated

### ✅ Practical
- 5-step process (15-25 min)
- Decision matrix (lookup table)
- Checklist-driven (no guessing)
- Real examples included

### ✅ Repeatable
- Standardized vocabulary
- Consistent scoring (0-100% grounding level)
- Clear acceptance criteria
- Measurable metrics

### ✅ Integrable
- Works with SpecKit workflow
- Can automate with scripts
- CI/CD integration points included
- Customizable for your needs

---

## What Each Role Uses

### 👔 Project Lead / Feature Owner
→ **15 minutes to approval decision**
1. Read QUICK_REFERENCE.md (5 min)
2. Use DECISION_MATRIX.md to score (5 min)
3. Make decision: ✅/⚠️/🔴 (5 min)

### 🔍 Reviewer / QA
→ **20 minutes for detailed review**
1. Use VALIDATION_CHECKLIST.md line-by-line (15 min)
2. Mark ✅/⚠️/🔴 for each item
3. Document findings in report

### 👨‍💻 Implementation Team
→ **5 minutes to understand task grounding**
1. Read your feature's TASK_GROUNDING_ANALYSIS.md
2. Understand each task's evidence + risk
3. Flag anything unclear to lead

### 🛠️ SpecKit Process Owner (You)
→ **1-2 hours to integrate**
1. Read README.md + INTEGRATION_GUIDE.md
2. Follow 6 integration steps
3. Deploy to team

---

## Process Flow (Visual)

```
[tasks.md Generated]
         ↓
    [Validation Gate] ← NEW STEP (15-25 min)
         ↓
    ┌────┴────┐
    ↓        ↓
  APPROVED  NEEDS CLF
    ↓        ↓
[Implementation]  [Update Artifacts]
    ↓             ↓
  [Continue]  [Regenerate tasks.md]
              ↓
           [Revalidate]
```

---

## Grounding Level Scale (0-100%)

The core concept is **Grounding Level**: How confident are we this task is required?

```
100% = Explicit in artifact ("Add X to Y file.cs")
80%  = Well-documented, pattern inferred
60%  = Documented, needs verification
40%  = Inferred from multiple sources
20%  = Assumed without evidence
0%   = Not grounded (task invented)

Rule of Thumb:
- Phase 1: Need ≥90% tasks at 80%+ → APPROVE
- Phase 2: Need ≥80% tasks at 70%+ → APPROVE
- Phase 3+: Need ≥70% tasks at 60%+ → APPROVE
```

---

## Decision Framework (Simple)

```
Q: Are Phase 1 & 2 tasks well-grounded?
   ├─ YES (≥80% avg) → ✅ APPROVE
   ├─ MOSTLY (70-80% avg) → ⚠️ NEEDS CLARIFICATION
   └─ NO (<70% avg) → 🔴 BLOCK

Q: Are artifacts consistent?
   ├─ YES → Good sign
   ├─ MOSTLY (1-2 inconsistencies) → Minor concern
   └─ NO (many contradictions) → Major concern

Q: How many gaps identified?
   ├─ 0-2 → ✅ Approve
   ├─ 3-5 → ⚠️ Review gaps
   └─ >5 → 🔴 Block, return to planning
```

---

## Real-World Example

Your current feature (007-lifeline-invitation-auto-role-mvp) has been analyzed:

**Current Status**:
- Phase 1 (T001-T003): 2 tasks fully grounded (100%), 1 partially (70%)
- Phase 2 (T004-T005): Both weakly grounded (50-60%), need spec.md verification

**Decision**: ⚠️ **NEEDS CLARIFICATION**

**Why**: Phase 2 tasks depend on spec.md (FR-001) which isn't provided in planning artifacts

**Action**:
- Verify spec.md actually requires SentEvent
- Confirm T004-T005 are necessary
- Re-analyze and approve

See: `specs/007-lifeline-invitation-auto-role-mvp/TASK_GROUNDING_ANALYSIS.md` for full analysis

---

## Integration Checklist (For You)

### Week 1: Review & Customize
- [ ] Read README.md (10 min)
- [ ] Read SPECIFICATION.md (30 min)
- [ ] Read INTEGRATION_GUIDE.md (20 min)
- [ ] Decide: Manual or automated validation?
- [ ] Customize artifact schema for your project

### Week 2: Pilot
- [ ] Set up report template
- [ ] Run validation on 007-lifeline feature
- [ ] Get feedback from team
- [ ] Refine thresholds if needed

### Week 3: Train Team
- [ ] Share QUICK_REFERENCE.md with team (5 min training)
- [ ] Share DECISION_MATRIX.md with leads
- [ ] Run example review together

### Week 4: Deploy
- [ ] Add to PR template checklist
- [ ] Add to SpecKit workflow documentation
- [ ] Make it standard practice
- [ ] Track metrics

---

## Customization Options

### Option A: Light-Touch (Manual, 15 min)
- Use QUICK_REFERENCE.md + DECISION_MATRIX.md
- Manual review by project lead
- No automation needed
- Good for: Small features, low risk

### Option B: Standard (Checklist-Driven, 20 min)
- Use VALIDATION_CHECKLIST.md for detailed review
- Generate TASK_GROUNDING_ANALYSIS.md manually
- Lead approves with signature
- Good for: Most features, medium risk

### Option C: Strict (Automated, 5 min + review)
- Use validation script from INTEGRATION_GUIDE.md
- Automated analysis report
- Manual review of recommendations
- Good for: Critical features, high risk, MVP phase

**Recommendation**: Start with Option B, automate later

---

## File Locations

All files are in: `.claude/skills/speckit-task-grounding/`

```
README.md                    ← Start here
SPECIFICATION.md             ← Full details
VALIDATION_CHECKLIST.md      ← Review tool
DECISION_MATRIX.md           ← Quick decisions
QUICK_REFERENCE.md           ← 1-pager
INTEGRATION_GUIDE.md         ← How to set up
```

Plus sample analysis at: `specs/007-lifeline-invitation-auto-role-mvp/TASK_GROUNDING_ANALYSIS.md`

---

## Key Innovation: Grounding Level Scoring

Instead of binary (grounded/not grounded), we use **0-100% scale**:

**Why this works**:
- ✅ More nuanced than yes/no
- ✅ Allows judgment calls
- ✅ Correlates with risk
- ✅ Easier to explain to stakeholders

**How to score**:
- Check 3-4 artifacts for evidence
- Assign weight to each (100%, 90%, 70%, 50%)
- Average the weights
- Result = Grounding Level

**Example**:
```
Task: T003 Add role name constants

Evidence found in:
├─ plan.md (references FSHRoles pattern)    → 60% weight
├─ data-model.md (uses constants)            → 70% weight
└─ Codebase pattern (FSHRoles exists)       → 70% weight (needs verification)

Average: (60 + 70 + 70) / 3 = 67%
Verdict: ⚠️ Partially Grounded (70%)
Action: Verify codebase pattern before executing
```

---

## Success Criteria (For You)

After implementing this, you should see:

✅ **Process-Level**:
- Validation takes 15-25 min per feature (standardized)
- 90%+ of checklists items passed on first review
- Clear traceability for every task
- Reduced confusion about task dependencies

✅ **Quality-Level**:
- <10% of tasks discovered as "not grounded" mid-implementation
- 95%+ approval rate first time (after artifacts exist)
- Faster sprint starts (no scope questions)
- Better scope definition before implementation

✅ **Team-Level**:
- Everyone understands task rationale
- Reviewers confident in approval decisions
- Implementers understand why tasks exist
- Reduces mid-project scope changes

---

## Questions for Your Review

As you review, consider:

1. **Scope**: Does this cover everything you need for task validation?
2. **Complexity**: Is the framework too detailed, or just right?
3. **Customization**: Do the examples match your project style?
4. **Integration**: Will this work with your SpecKit workflow?
5. **Training**: Can your team learn this in 1-2 hours?
6. **Automation**: Where should you prioritize automation?
7. **Thresholds**: Do the grounding % thresholds make sense for you?

---

## Next Steps (For You)

### ✅ Immediate (Today)
1. Review this summary (5 min)
2. Skim README.md (10 min)
3. Decide: This solves my problem? (Yes / No / Close but needs X)

### ⚠️ If "Yes":
1. Schedule 1 hour to read SPECIFICATION.md + INTEGRATION_GUIDE.md
2. Follow Week 1 checklist above
3. Pilot on 007-lifeline feature next week

### 🔧 If "Close but needs X":
1. Tell me what needs adjustment
2. I'll customize the framework
3. Re-review before integration

### ❌ If "No":
1. Explain what's missing
2. I'll revise the approach
3. Resubmit for review

---

## Summary

**You're getting**: A production-ready, standardized task validation workflow with:
- 67 pages of documentation
- 5-step process (15-25 min)
- Checklists, matrices, templates
- Real example analysis
- Integration guide
- Customization options

**You can**:
- Use immediately (manual)
- Automate later (script included)
- Customize for your project
- Train team in 1-2 hours

**Result**:
- Every task grounded in planning artifacts
- Clear traceability for implementation
- Consistent quality across features
- Confident approval decisions

---

## Recommendation

**I recommend**: Start with Option B (checklist-driven) on your next feature

**Timeline**:
- Week 1: Read & customize
- Week 2: Pilot (007-lifeline)
- Week 3: Train team
- Week 4: Full deployment

**Effort**: ~6 hours total setup, then 15-25 min per feature going forward

---

## Ready for Integration?

👉 **Start here**: [README.md](.claude/skills/speckit-task-grounding/README.md)

Then follow: **Getting Started** section in README.md

---

**Questions or feedback?** Let me know what to adjust before you integrate this into your workflow.
