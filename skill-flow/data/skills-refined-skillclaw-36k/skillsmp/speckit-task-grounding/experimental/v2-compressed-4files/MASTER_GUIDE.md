# SpecKit Task Grounding Validation Framework - Master Guide
**Version**: 2.0.0 (Compressed) | **Status**: Ready for Use
**Date**: January 12, 2026

---

## 🚀 What is This Framework?

A **standardized, repeatable workflow** for validating that every task in `tasks.md` is grounded in planning artifacts (spec.md, plan.md, data-model.md, api-contracts.md, research.md, quickstart.md).

### 🎯 Problem Solved
- ❌ Tasks disconnected from documented requirements
- ❌ Invented assumptions without planning evidence
- ❌ Unclear task dependencies and risks
- ❌ Inconsistent quality across features

### ✅ Solution Provided
- ✅ Mandatory validation gate between planning and implementation
- ✅ Clear traceability for every task (0-100% grounding score)
- ✅ Automated evidence checking (optional)
- ✅ Standardized decision framework
- ✅ Actionable gap identification

---

## 📋 Quick Start (15-25 Minutes)

### The 5-Step Process

```
STEP 1: Run validation script (2 min)
        ↓ Confirms artifacts exist

STEP 2: Review task mappings (5 min)
        ↓ Use FRAMEWORK.md checklists

STEP 3: Generate analysis report (5 min)
        ↓ Use template from FRAMEWORK.md

STEP 4: Check against checklist (10 min)
        ↓ Mark items ✅/⚠️/🔴

STEP 5: Make decision (2 min)
        ↓ Use decision matrix below

RESULT: TASK_GROUNDING_ANALYSIS.md + Decision Gate
        (✅ Approved / ⚠️ Needs Clarification / 🔴 Blocked)
```

---

## 👥 Role-Based Usage Guide

### 👔 Project Lead / Feature Owner (Reviewing tasks.md)
**Your Job**: Approve tasks before implementation (15 min)
**Quick Path**:
1. Read this section (2 min)
2. Use [Decision Matrix](#decision-matrix) below (5 min)
3. Reference [TOOLS.md](TOOLS.md) for detailed checklists if needed

### 🔍 Quality Reviewer (Validating reports)
**Your Job**: Thoroughly validate task grounding (20 min)
**Path**:
1. Read [FRAMEWORK.md](FRAMEWORK.md) > Validation Methodology
2. Use detailed checklists in [FRAMEWORK.md](FRAMEWORK.md)
3. Generate TASK_GROUNDING_ANALYSIS.md report

### 👨‍💻 Implementation Team (Reading grounded tasks)
**Your Job**: Understand task rationale (5 min)
**Path**:
1. Read your feature's TASK_GROUNDING_ANALYSIS.md
2. Check each task's grounding level and evidence
3. Flag any unclear or risky tasks before starting

### 🛠️ SpecKit Process Owner (Integrating this)
**Your Job**: Set up and deploy (1-2 hours)
**Path**:
1. Read [IMPLEMENTATION.md](IMPLEMENTATION.md) completely
2. Follow 6-step integration guide
3. Customize for your project needs

---

## 🎯 Key Concepts

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

### Match Types
**How tasks connect to artifacts**:
- **Explicit**: Direct specification (e.g., "Add X to Y") → 100%
- **Reference**: Mentioned with context → 80%
- **Implicit**: Inferred from pattern or principle → 60%
- **External**: Depends on spec.md or other doc → 50%+

---

## ⚡ Decision Matrix (Quick Reference)

### Decision Gates

**✅ APPROVED** (Confidence ≥80%)
- ≥90% Phase 1 tasks at ≥80% grounding
- ≥80% Phase 2 tasks at ≥70% grounding
- All high-risk gaps have mitigations
- **Action**: Proceed to implementation

**⚠️ NEEDS CLARIFICATION** (Confidence 50-79%)
- Some tasks 60-79% grounded
- Minor artifact inconsistencies
- External references need verification
- **Action**: Update artifacts, regenerate tasks.md

**🔴 BLOCKED** (Confidence <50%)
- >50% of tasks <50% grounded
- Critical gaps unresolved
- Major artifact contradictions
- **Action**: Return to planning phase

### Quick Decision Table

| Phase | All ≥80% | Some <80% | Many <60% | Most <50% |
|-------|----------|-----------|-----------|-----------|
| Phase 1 | ✅ APPROVE | ⚠️ CLARIFY | 🔴 BLOCK | 🔴 BLOCK |
| Phase 2 | ✅ APPROVE | ✅ APPROVE | ⚠️ CLARIFY | 🔴 BLOCK |
| Phase 3+ | ✅ APPROVE | ✅ APPROVE | ✅ APPROVE | ⚠️ CLARIFY |

---

## 📚 Framework Structure (4-File Version)

### 📖 MASTER_GUIDE.md (This File)
**Purpose**: Navigation, overview, quick start
**Content**: What this is, how to use, key concepts, decision matrix
**Time**: 10 min read
**For**: Everyone (first stop)

### 🏗️ FRAMEWORK.md
**Purpose**: Core methodology and validation process
**Content**: Detailed process, checklists, scoring, decisions
**Time**: 30-45 min read
**For**: Reviewers, process designers

### 🔧 IMPLEMENTATION.md
**Purpose**: Setup, integration, and deployment
**Content**: How to integrate, automate, customize
**Time**: 45 min read
**For**: Process engineers, automation specialists

### 🛠️ TOOLS.md
**Purpose**: Reference materials and templates
**Content**: Checklists, templates, examples, appendices
**Time**: 20 min reference
**For**: Practical use during reviews

---

## 📊 Success Metrics

Track these to measure effectiveness:

| Metric | Target | How to Calculate |
|--------|--------|------------------|
| % approved first time | ≥75% | (Approved / Total reviews) |
| Avg grounding by phase | Phase1: ≥80%, Phase2: ≥70% | Mean of all task scores |
| Tasks <50% grounding | <10% | (LowScore / Total tasks) |
| Rework rate | <20% | (Regenerated / Total) |
| Time spent validating | 15-25 min | (Actual / Planned) |
| Post-approval issues | <5% | (Issues found in implementation / Total) |

---

## ⏱️ Integration Timeline

### Phase 1: Setup (Week 1)
- [ ] Read this MASTER_GUIDE.md
- [ ] Read [FRAMEWORK.md](FRAMEWORK.md) > Process Overview
- [ ] Define artifact schema (see [IMPLEMENTATION.md](IMPLEMENTATION.md))
- [ ] Create report template

### Phase 2: Pilot (Week 2)
- [ ] Apply to current feature
- [ ] Generate analysis report
- [ ] Get feedback from project lead

### Phase 3: Refine (Week 3)
- [ ] Adjust grounding thresholds
- [ ] Update checklists based on findings
- [ ] Document lessons learned

### Phase 4: Full Integration (Week 4)
- [ ] Add to standard workflow
- [ ] Train team
- [ ] Set up automation (CI/CD hooks)

---

## ❓ Frequently Asked Questions

### Q: How much time does validation take?
**A**: 15-25 minutes per feature using the 5-step process. Can be automated to <5 min with scripts.

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
**A**: Yes, see [IMPLEMENTATION.md](IMPLEMENTATION.md) > Automation section.

---

## 🆘 Support & Help

| Question | Where to Find Answer |
|----------|----------------------|
| "What does grounding level mean?" | [TOOLS.md](TOOLS.md) > Grounding Scale |
| "How do I approve tasks?" | Decision Matrix above |
| "How do I set this up?" | [IMPLEMENTATION.md](IMPLEMENTATION.md) > 6 Steps |
| "What's a red flag?" | [FRAMEWORK.md](FRAMEWORK.md) > Red Flags |
| "What counts as evidence?" | [FRAMEWORK.md](FRAMEWORK.md) > Evidence Standards |
| "How do I score tasks?" | [FRAMEWORK.md](FRAMEWORK.md) > Scoring Guide |
| "What if artifacts don't exist?" | [IMPLEMENTATION.md](IMPLEMENTATION.md) > Troubleshooting |
| "Can I customize thresholds?" | [FRAMEWORK.md](FRAMEWORK.md) > Customization |

---

## 🎯 Getting Started Paths

### 🚀 Quick Review (10 min)
1. Read this MASTER_GUIDE.md (you're here!)
2. Use Decision Matrix above to approve tasks
3. Done!

### 📋 Detailed Review (20 min)
1. Read this MASTER_GUIDE.md
2. Scan [FRAMEWORK.md](FRAMEWORK.md) > Process Flow
3. Use checklists in [FRAMEWORK.md](FRAMEWORK.md)
4. Generate TASK_GROUNDING_ANALYSIS.md
5. Approve or request clarification

### 🔧 Integration Setup (1-2 hours)
1. Read this MASTER_GUIDE.md
2. Read [IMPLEMENTATION.md](IMPLEMENTATION.md) completely
3. Set up artifact schema (YAML)
4. Create report template
5. Test on current feature
6. Get feedback, refine, deploy

---

## 📁 File Structure

```
speckit-task-grounding/
├── v1-original/                    # Original 13-file structure (preserved)
├── v2-compressed-4files/          # Current: This compressed version
│   ├── MASTER_GUIDE.md            # This file
│   ├── FRAMEWORK.md               # Core methodology
│   ├── IMPLEMENTATION.md          # Setup & deployment
│   └── TOOLS.md                   # References & templates
├── v3-future-iterations/          # Future compression versions
└── README.md                      # Version control guide
```

---

## 🔗 Related Files

- **Real Example**: `specs/007-lifeline-invitation-auto-role-mvp/TASK_GROUNDING_ANALYSIS.md`
- **Original Files**: See `v1-original/` folder
- **Integration Scripts**: See [IMPLEMENTATION.md](IMPLEMENTATION.md) > Automation

---

## 📞 Questions?

**"What's in the other files?"**
→ See Framework Structure section above

**"How do I use this?"**
→ See Role-Based Usage Guide above

**"Can I customize it?"**
→ See [FRAMEWORK.md](FRAMEWORK.md) > Customization Points

**"How long to set up?"**
→ See Integration Timeline above

---

## ✨ Ready to Get Started?

### Next Steps:
1. **Choose your path** from Getting Started Paths above
2. **Read the appropriate files** for your role
3. **Apply to a feature** using the 5-step process
4. **Provide feedback** on the compressed structure

---

**This MASTER_GUIDE.md gives you the 80/20 overview. Dive deeper into [FRAMEWORK.md](FRAMEWORK.md) for detailed methodology or [IMPLEMENTATION.md](IMPLEMENTATION.md) for setup instructions.**