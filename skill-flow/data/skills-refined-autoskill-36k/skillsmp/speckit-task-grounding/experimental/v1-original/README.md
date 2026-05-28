# SpecKit Task Grounding Validation Framework
**Version**: 1.0.0 | **Status**: Ready for Review & Integration
**Created**: January 12, 2026

---

## What is This?

A **standardized, repeatable workflow** for validating that every task in `tasks.md` is grounded in planning artifacts (spec.md, plan.md, data-model.md, api-contracts.md, research.md, quickstart.md).

**Problem it solves**:
- ❌ Tasks disconnected from documented requirements
- ❌ Invented assumptions without planning evidence
- ❌ Unclear task dependencies and dependencies
- ❌ Inconsistent quality across features

**Solution**:
- ✅ Mandatory validation gate between planning and implementation
- ✅ Clear traceability for every task
- ✅ Automated evidence checking (optional)
- ✅ Standardized decision framework
- ✅ Actionable gap identification

---

## Quick Navigation

### 📋 For Different Roles

**Project Lead / Feature Owner** (reviewing tasks.md):
1. Start: [QUICK_REFERENCE.md](#quick_reference)
2. Review: [DECISION_MATRIX.md](#decision-matrix) (5 min decision)
3. Reference: [VALIDATION_CHECKLIST.md](#validation-checklist) (detailed review)

**Implementation Team** (reading grounded tasks):
1. Review: [TASK_GROUNDING_ANALYSIS.md](#sample-report) generated for your feature
2. Understand: Each task's evidence and risk level
3. Flag: Any unclear or risky tasks before starting

**SpecKit Process Owner** (integrating this):
1. Read: [INTEGRATION_GUIDE.md](#integration-guide) (setup)
2. Customize: [SPECIFICATION.md](#specification) (adapt to your project)
3. Deploy: Follow implementation timeline in INTEGRATION_GUIDE.md

---

## Documents Included

### 📚 Core Framework Documents

#### 1. **SPECIFICATION.md** ⭐ Start Here
**Length**: ~15 pages
**Audience**: Technical leads, process designers
**Content**:
- Detailed workflow process (6 steps)
- Validation framework with 6 steps
- Report structure and template
- Acceptance criteria
- Validation input checklist
- Integration points for SpecKit
- Customization guidance

**When to use**:
- Understanding the full validation framework
- Customizing for your project
- Implementing automated validation
- Training technical reviewers

---

#### 2. **VALIDATION_CHECKLIST.md** 📋 Main Tool
**Length**: ~20 pages
**Audience**: Project leads, QA, reviewers
**Content**:
- Pre-validation setup (artifacts check)
- Report structure validation
- Task coverage verification
- Grounding evidence standards
- Consistency validation
- Gap identification standards
- Risk assessment rubric
- Quality standards
- Reviewer checklist
- Common issues & scoring
- Grounding level scale (0-100%)
- Red flags checklist
- Approval signature template

**When to use**:
- Reviewing TASK_GROUNDING_ANALYSIS.md
- Validating tasks before approval
- Training reviewers
- Scoring tasks consistently

---

#### 3. **DECISION_MATRIX.md** ⚡ Quick Decisions
**Length**: ~8 pages
**Audience**: Project leads, feature owners
**Content**:
- Decision tree (visual)
- Approval matrix (simple table)
- Risk × Grounding matrix
- Confidence level mapping
- Task count evaluation
- External reference validation
- Implementation readiness score
- Common scenarios (3 examples)
- Blocker checklist
- Approval checklist
- Threshold customization
- Decision document template

**When to use**:
- Making approval decisions (5 min)
- Scoring phase averages
- Determining confidence levels
- Following common scenarios

---

#### 4. **QUICK_REFERENCE.md** 🎯 One-Pager
**Length**: ~5 pages
**Audience**: Everyone
**Content**:
- TL;DR process (5 steps, 15-25 min)
- Grounding level at a glance
- Decision gate quick table
- Red flags (stop signs)
- Evidence requirements by phase
- Evidence types (weighted)
- Grounding patterns
- Artifact weights
- Key questions per task
- Red flag checklist
- Common patterns
- Training paths
- Metrics dashboard

**When to use**:
- First-time orientation
- Quick reference during review
- Team training (5-min version)
- Decision making in a rush

---

#### 5. **INTEGRATION_GUIDE.md** 🔧 Implementation
**Length**: ~18 pages
**Audience**: Process engineers, automation specialists
**Content**:
- Quick start (manual process)
- Step 1: Define artifact schema (YAML)
- Step 2: Create report template
- Step 3: Create validation script (PowerShell)
- Step 4: Integrate into SpecKit workflow
- Step 5: Create decision framework (YAML)
- Step 6: Review checklist integration
- Implementation timeline (4 weeks)
- Integration points (GitHub Actions, VS Code, pre-commit hooks)
- Troubleshooting guide
- Maintenance & metrics

**When to use**:
- Setting up automation
- Integrating with CI/CD
- Creating custom scripts
- Troubleshooting integration issues

---

#### 6. **TASK_GROUNDING_ANALYSIS.md** (Sample)
**Location**: `specs/007-lifeline-invitation-auto-role-mvp/TASK_GROUNDING_ANALYSIS.md`
**Purpose**: Example report showing how validation works
**Content**:
- Real analysis of Phase 1 & Phase 2 tasks from 007 feature
- Artifact mappings per task
- Cross-artifact consistency checks
- Critical gaps identified with solutions
- Risk assessments
- Recommendations

**When to use**:
- Understanding output format
- Seeing real example
- Training team on expected deliverables

---

## Process Overview

### The 5-Step Process (15-25 minutes)

```
STEP 1: Run validation script (2 min)
        ↓ Confirms artifacts exist

STEP 2: Review task mappings (5 min)
        ↓ Use VALIDATION_CHECKLIST.md

STEP 3: Generate analysis report (5 min)
        ↓ Use template from SPECIFICATION.md

STEP 4: Check against checklist (10 min)
        ↓ Mark items ✅/⚠️/🔴

STEP 5: Make decision (2 min)
        ↓ Use DECISION_MATRIX.md

RESULT: TASK_GROUNDING_ANALYSIS.md + Decision Gate
        (Approved / Needs Clarification / Blocked)
```

---

## Key Concepts

### Grounding Level (0-100%)
**What**: Percentage confidence that a task is required by planning artifacts

| Level | Meaning | Action |
|-------|---------|--------|
| 100% | Explicit in primary artifact | ✅ Execute immediately |
| 80-90% | Well-documented, pattern inferred | ✅ Execute |
| 70-79% | Documented but needs verification | ⚠️ Verify before executing |
| 60-69% | Weakly documented | ⚠️ Recommend clarification |
| 50-59% | Inferred from multiple sources | 🔴 High risk, needs resolution |
| <50% | Assumed without evidence | 🔴 Not grounded, block |

---

### Match Types
**How tasks connect to artifacts**:

- **Explicit**: Direct specification (e.g., "Add X to Y") → 100%
- **Reference**: Mentioned with context → 80%
- **Implicit**: Inferred from pattern or principle → 60%
- **External**: Depends on spec.md or other doc → 50%+

---

### Decision Gates

**✅ APPROVED** (Confidence ≥80%)
- ≥90% Phase 1 tasks at ≥80% grounding
- ≥80% Phase 2 tasks at ≥70% grounding
- All high-risk gaps have mitigations
- Proceed to implementation

**⚠️ NEEDS CLARIFICATION** (Confidence 50-79%)
- Some tasks 60-79% grounded
- Minor artifact inconsistencies
- External references need verification
- Action: Update artifacts, regenerate tasks.md

**🔴 BLOCKED** (Confidence <50%)
- >50% of tasks <50% grounded
- Critical gaps unresolved
- Major artifact contradictions
- Action: Return to planning phase

---

## Usage Patterns

### Pattern 1: Quick Approval (10 min)
```
Use: QUICK_REFERENCE.md + DECISION_MATRIX.md
Goal: Fast approval for well-grounded tasks
Result: ✅ Approved
```

### Pattern 2: Detailed Review (20 min)
```
Use: VALIDATION_CHECKLIST.md + sample report
Goal: Comprehensive validation with gaps identified
Result: ✅ Approved or ⚠️ Needs Clarification
```

### Pattern 3: Troubleshooting (30 min)
```
Use: SPECIFICATION.md + INTEGRATION_GUIDE.md
Goal: Understand process, resolve integration issues
Result: 🔧 Process configured
```

### Pattern 4: Training (1-2 hours)
```
Use: All documents + real example
Goal: Team understands validation process
Result: 👥 Team trained
```

---

## Integration Timeline

### Phase 1: Setup (Week 1)
- [ ] Read SPECIFICATION.md
- [ ] Define artifact schema (see INTEGRATION_GUIDE.md)
- [ ] Create report template
- [ ] Set up validation script

### Phase 2: Pilot (Week 2)
- [ ] Apply to current feature (007-lifeline-invitation-auto-role-mvp)
- [ ] Generate analysis report
- [ ] Get feedback from project lead

### Phase 3: Refine (Week 3)
- [ ] Adjust grounding thresholds
- [ ] Update checklist based on findings
- [ ] Document lessons learned

### Phase 4: Full Integration (Week 4)
- [ ] Add to standard workflow
- [ ] Train team
- [ ] Set up automation (CI/CD hooks)

---

## File Structure

```
.claude/skills/speckit-task-grounding/
├── README.md                          ← You are here
├── SPECIFICATION.md                   ← Framework details
├── VALIDATION_CHECKLIST.md            ← Review tool
├── DECISION_MATRIX.md                 ← Decision helper
├── QUICK_REFERENCE.md                 ← 1-pager
└── INTEGRATION_GUIDE.md               ← Implementation

.specify/config/
├── artifact-schema.yaml               ← Define your artifacts
└── task-grounding-decisions.yaml      ← Decision rules

.specify/scripts/powershell/
└── validate-task-grounding.ps1        ← Automation script

specs/007-lifeline-invitation-auto-role-mvp/
├── spec.md
├── plan.md
├── tasks.md                           ← To validate
├── data-model.md
├── api-contracts.md
├── research.md
├── quickstart.md
└── TASK_GROUNDING_ANALYSIS.md         ← Example output
```

---

## Customization for Your Project

### Adjust Artifact Schema
See [INTEGRATION_GUIDE.md > Step 1](INTEGRATION_GUIDE.md#step-1-define-your-artifact-schema)

### Adjust Grounding Thresholds
See [INTEGRATION_GUIDE.md > Implementation Timeline](INTEGRATION_GUIDE.md#implementation-timeline)

### Adjust Decision Rules
See [DECISION_MATRIX.md > Thresholds Customization](DECISION_MATRIX.md#thresholds-customization)

### Customize for Different Project Types
See [SPECIFICATION.md > Customization Points](SPECIFICATION.md#customization-points)

---

## Common Questions

### Q: How much time does validation take?
**A**: 15-25 minutes per feature if using the 5-step process. Can be automated to <5 min if using script.

### Q: When should we validate?
**A**: Immediately after tasks.md is generated (before human implementation starts). Makes it a decision gate.

### Q: Is this mandatory?
**A**: Recommended for features with ≥3 phases and ≥10 tasks. Can be light-touch for smaller features.

### Q: Can we skip validation?
**A**: Not recommended. Skipping = risk of disconnected tasks, incomplete implementation, scope creep.

### Q: What if a task is weakly grounded?
**A**: Either (a) remove it, (b) add planning artifact explaining why it's needed, or (c) mark as high-risk and proceed with caution.

### Q: Who should approve?
**A**: Project lead or feature owner (someone accountable for scope).

### Q: Can we automate this?
**A**: Yes, see [INTEGRATION_GUIDE.md > Automated Agent-Based](INTEGRATION_GUIDE.md#option-b-automated-agent-based-future)

---

## Success Metrics

Track these to measure effectiveness:

| Metric | Target | Calculation |
|--------|--------|-------------|
| % approved first time | ≥75% | (Approved / Total) |
| Avg grounding by phase | Phase1: ≥80%, Phase2: ≥70% | Mean of all task scores |
| Tasks <50% grounding | <10% | (LowScore / Total) |
| Rework rate | <20% | (Regenerated / Total) |
| Time spent validating | 15-25 min | (Actual / Planned) |
| Post-approval issues | <5% | (Issues found in implementation / Total) |

---

## Support & Questions

| Topic | Document |
|-------|----------|
| "What does grounding level mean?" | QUICK_REFERENCE.md > Grounding Level at a Glance |
| "How do I approve tasks?" | DECISION_MATRIX.md > Quick Approval Flow |
| "How do I set this up?" | INTEGRATION_GUIDE.md > Step 1-6 |
| "What's a red flag?" | VALIDATION_CHECKLIST.md > Red Flags Checklist |
| "What counts as evidence?" | SPECIFICATION.md > Evidence Standards |
| "How do I score tasks?" | VALIDATION_CHECKLIST.md > Grounding Level Scale |
| "What if artifacts don't exist?" | INTEGRATION_GUIDE.md > Troubleshooting |
| "Can I customize thresholds?" | DECISION_MATRIX.md > Thresholds Customization |

---

## Getting Started

### For a Quick Review (10 min)
1. Read [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
2. Use [DECISION_MATRIX.md](DECISION_MATRIX.md) to approve
3. Done!

### For a Detailed Review (20 min)
1. Scan [SPECIFICATION.md](SPECIFICATION.md) > Process Flow
2. Use [VALIDATION_CHECKLIST.md](VALIDATION_CHECKLIST.md) line by line
3. Generate TASK_GROUNDING_ANALYSIS.md
4. Review sample at `specs/007-*/TASK_GROUNDING_ANALYSIS.md`
5. Approve or request clarification

### For Integration (1-2 hours)
1. Read [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md) completely
2. Set up artifact schema (YAML)
3. Create report template
4. Test on current feature
5. Get feedback, refine, deploy

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-12 | Initial release |

---

## Next Steps

1. **Read**: Choose your path above
2. **Pilot**: Apply to 007-lifeline-invitation-auto-role-mvp
3. **Feedback**: Get input from project lead
4. **Integrate**: Add to standard SpecKit workflow
5. **Monitor**: Track success metrics

---

**Questions?** → See Support & Questions table above

**Ready to integrate?** → Start with [INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)

**Want just the checklist?** → Use [QUICK_REFERENCE.md](QUICK_REFERENCE.md)

**Need detailed specs?** → See [SPECIFICATION.md](SPECIFICATION.md)
