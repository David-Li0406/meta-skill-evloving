# Task Grounding Validation - Quick Reference
**Version**: 1.0.0 | **Date**: January 12, 2026

---

## TL;DR: The 5-Minute Process

```
1️⃣ Run validation script (2 min)
   └─ Confirms artifacts exist

2️⃣ Review task mappings (5 min)
   └─ Read VALIDATION_CHECKLIST.md

3️⃣ Generate analysis report (5 min)
   └─ Use TASK_GROUNDING_ANALYSIS.md template

4️⃣ Check against checklist (10 min)
   └─ Mark items ✅/⚠️/🔴

5️⃣ Make decision (2 min)
   └─ Approved / Needs Clarification / Blocked
```

**Total Time**: ~15-25 minutes per feature

---

## Grounding Level at a Glance

| Level | What it means | What to do |
|-------|--------------|-----------|
| 100% | Explicit in primary artifact | ✅ Safe to execute |
| 80-90% | Well-documented, implementation inferred | ✅ Safe to execute |
| 70-79% | Documented, needs pattern verification | ⚠️ Verify codebase pattern |
| 60-69% | Weakly documented, multiple sources needed | ⚠️ Recommend clarification |
| 50-59% | Inferred from multiple artifacts | 🔴 High risk, block Phase 2 |
| <50% | Assumed without evidence | 🔴 Not grounded, block all |

---

## Decision Gate Quick Table

| Phase | All ≥80% | Some <80% | Many <60% | Most <50% |
|-------|----------|-----------|-----------|-----------|
| Phase 1 | ✅ APPROVE | ⚠️ CLARIFY | 🔴 BLOCK | 🔴 BLOCK |
| Phase 2 | ✅ APPROVE | ✅ APPROVE | ⚠️ CLARIFY | 🔴 BLOCK |
| Phase 3+ | ✅ APPROVE | ✅ APPROVE | ✅ APPROVE | ⚠️ CLARIFY |

---

## Red Flags (Stop & Review)

🛑 **STOP** if you see:

- Any task with 0-20% grounding in Phase 1
- Same artifact cited for >70% of tasks
- "TBD" or "Unknown grounding" in final report
- Task contradicts documented requirement
- >30% of gaps marked "discuss in implementation"
- Missing decision gate status at end

---

## Evidence Requirements by Phase

### Phase 1: Setup
- ✅ Every task must cite primary artifact (spec.md or plan.md)
- ✅ Every task must have ≥80% grounding
- ⚠️ Parallel tasks OK with same evidence if independent

### Phase 2: Foundational
- ✅ Every task must cite primary artifact
- ✅ Every task must have ≥70% grounding
- ⚠️ External dependencies (spec.md FR-###) must be verified

### Phase 3+: User Stories
- ✅ Every task must have ≥1 artifact reference
- ✅ Story tasks should cite data-model.md or api-contracts.md
- ⚠️ 60%+ grounding is acceptable for user story work

---

## Evidence Types (in order of weight)

1. **Explicit specification**: "Add X to Y" → Evidence weight: 100%
2. **Detailed example**: Code or SQL example shown → Evidence weight: 90%
3. **Reference + context**: "Section X covers Y" → Evidence weight: 80%
4. **Schema/pattern reference**: "See contracts/ folder" → Evidence weight: 70%
5. **Implied requirement**: "Following pattern from [artifact]" → Evidence weight: 60%
6. **Architectural principle**: "Per Clean Architecture" → Evidence weight: 50%
7. **Common practice**: "Standard in similar features" → Evidence weight: 40%
8. **Developer assumption**: "Likely needed based on..." → Evidence weight: 20%
9. **No evidence**: "Task invented" → Evidence weight: 0%

---

## Checklist Items for Review

### Before you approve, verify:

| Item | Check |
|------|-------|
| All tasks from tasks.md listed | ✅ ☐ |
| Each task has grounding 0-100% | ✅ ☐ |
| Phase 1 avg ≥80% grounding | ✅ ☐ |
| Phase 2 avg ≥70% grounding | ✅ ☐ |
| No task with 0% grounding | ✅ ☐ |
| Gaps clearly identified | ✅ ☐ |
| Risks rated (Low/Med/High) | ✅ ☐ |
| Decision gate marked | ✅ ☐ |
| No contradictions vs spec | ✅ ☐ |
| External refs verified | ✅ ☐ |

**If ≥9/10 checked**: → Ready to review

---

## Common Grounding Patterns

### Well-Grounded Task
```
Task: T001 Add TenantFeatureFlag enum value

Artifact: data-model.md > Feature Flags
Evidence: "Location: src/Core/Shared/FeatureManagement/FeatureFlags.cs
           New Value: [Display(Name = "X")] LifelineAutoRoleAssignment"

Assessment: ✅ Fully Grounded (100%)
```

### Partially Grounded Task
```
Task: T003 Add role name constants

Artifact: plan.md > Project Structure (references FSHPermissions.cs)
Secondary: data-model.md > Seeder (uses hardcoded "Lifeline CoHost")

Assessment: ⚠️ Partially Grounded (70%)
Issue: Plan doesn't mention FSHRoles.cs, inferred from pattern
Action: Verify codebase has FSHRoles pattern before executing
```

### Weakly Grounded Task
```
Task: T004 Define SentEvent

Artifact: api-contracts.md > schemas (references schema file, not documented)
Secondary: None clear

Assessment: 🔴 Weakly Grounded (50%)
Issue: Requirement not explicitly in planning artifacts
Action: Verify spec.md FR-001 before executing
```

---

## Artifact Weights for Scoring

**Use these to weight evidence**:

| Artifact | Phase 1 Weight | Phase 2 Weight | Phase 3+ Weight |
|----------|----------------|----------------|-----------------|
| spec.md | 1.0 (100%) | 1.0 (100%) | 1.0 (100%) |
| plan.md | 0.9 (90%) | 0.9 (90%) | 0.8 (80%) |
| data-model.md | 0.7 (70%) | 0.8 (80%) | 0.9 (90%) |
| api-contracts.md | 0.6 (60%) | 0.7 (70%) | 0.8 (80%) |
| research.md | 0.6 (60%) | 0.7 (70%) | 0.6 (60%) |
| quickstart.md | 0.5 (50%) | 0.6 (60%) | 0.5 (50%) |
| Codebase pattern | 0.4 (40%) | 0.5 (50%) | 0.6 (60%) |

**How to use**: If task cited in "plan.md" + "data-model.md", grounding = avg(0.9, 0.7) = 80%

---

## Artifact Checklist

**Before validating, ensure you have:**

- [ ] spec.md (required)
- [ ] plan.md (required)
- [ ] tasks.md (to validate)
- [ ] data-model.md (or design document)
- [ ] api-contracts.md (or contract document)
- [ ] research.md (or decisions document)
- [ ] quickstart.md (optional, but helpful)

**Minimum to proceed**: spec.md + plan.md + tasks.md

**Recommended**: All 7 artifacts

**If <5 artifacts**: Adjust grounding scores -5% each for missing artifact

---

## Questions to Ask Per Task

### For Every Task, Answer:

1. **Explicit?** Is requirement explicitly stated in any artifact? (Yes → 80%+, No → 60%-80%)
2. **Where?** Which artifact(s) state this requirement? (List them)
3. **File path correct?** Does path match artifact? (Yes → +5%, No → -10%)
4. **Feasible?** Can developer execute this task independently? (No → -20%)
5. **Blocking?** Does this task block other tasks? (Yes → higher priority)
6. **Risk?** What could go wrong? (Document it)
7. **Evidence?** Can you quote artifact supporting this task? (No quote → <60%)

---

## When to Mark BLOCKED

❌ **BLOCKED** if:

- [ ] ≥2 Phase 1 tasks with <50% grounding
- [ ] ≥5 Phase 2 tasks with <60% grounding
- [ ] Core requirement contradicted in artifacts
- [ ] Cannot find artifact evidence for task
- [ ] Task depends on unresolved spec requirement
- [ ] Gaps prevent implementation (not just complexity)

---

## When to Mark NEEDS CLARIFICATION

⚠️ **NEEDS CLARIFICATION** if:

- [ ] ≥1 Phase 1 task with 60-79% grounding
- [ ] ≥2 Phase 2 tasks with <70% grounding
- [ ] Minor artifact inconsistencies
- [ ] External references need verification
- [ ] Pattern assumptions unconfirmed

---

## When to Mark APPROVED

✅ **APPROVED** if:

- [ ] ≥90% Phase 1 tasks ≥80% grounding
- [ ] ≥80% Phase 2 tasks ≥70% grounding
- [ ] All high-risk gaps have mitigations
- [ ] No task contradicts spec
- [ ] External refs verified

---

## Report Template (1-pager)

```markdown
# Task Grounding: [Feature]

| Phase | Count | Avg Grounding | Risk | Status |
|-------|-------|---------------|------|--------|
| Phase 1 | 3 | 93% | 🟢 Low | ✅ OK |
| Phase 2 | 2 | 65% | 🟡 Med | ⚠️ Review |
| Phase 3 | 8 | 72% | 🟢 Low | ✅ OK |

**Gaps**: [Count] identified
**Risks**: [Count] High risk items need mitigation
**Decision**: [APPROVED / NEEDS CLARIFICATION / BLOCKED]

Next: [Clear statement of what happens next]
```

---

## Review Workflow

```
START: tasks.md generated
  ↓
Run validation script → Artifacts OK?
  ├─ NO  → Get missing artifacts
  │        └─ Return to planning
  └─ YES → Continue
  ↓
Review each task mapping
  ├─ Finding issues? → Document in gaps section
  └─ Looks good? → Continue
  ↓
Check consistency across artifacts
  ├─ Inconsistencies? → Document as gap
  └─ OK? → Continue
  ↓
Assess risks
  ├─ High risks? → Add mitigations
  └─ OK? → Continue
  ↓
Make decision
  ├─ APPROVED → Proceed to implementation
  ├─ NEEDS CLARIFICATION → Update artifacts
  └─ BLOCKED → Return to planning
END
```

---

## Training for Team

### 5-Min Onboarding
1. Read this page (quick reference)
2. Review sample TASK_GROUNDING_ANALYSIS.md
3. Ask: "Is task grounded, and do you see contradictions?"

### 15-Min Training
1. Watch demo of validation process
2. Review VALIDATION_CHECKLIST.md
3. Walk through one example feature

### 1-Hr Deep Dive (for reviewers)
1. Read SPECIFICATION.md
2. Study VALIDATION_CHECKLIST.md
3. Practice on 2-3 features
4. Learn to adjust for your project context

---

## Metrics Dashboard

**Track these to improve process**:

- % of features approved first time (target: ≥75%)
- Average grounding level by phase
- % of tasks <60% grounding (target: <10%)
- Rework rate (target: <20%)
- Time spent validating (target: 15-25 min/feature)

---

## Where to Find Help

| Item | Location |
|------|----------|
| Full specification | `.claude/skills/speckit-task-grounding/SPECIFICATION.md` |
| Validation checklist | `.claude/skills/speckit-task-grounding/VALIDATION_CHECKLIST.md` |
| Integration guide | `.claude/skills/speckit-task-grounding/INTEGRATION_GUIDE.md` |
| This quick ref | `.claude/skills/speckit-task-grounding/QUICK_REFERENCE.md` |
| Sample analysis | `specs/007-*/TASK_GROUNDING_ANALYSIS.md` |
| Validation script | `.specify/scripts/powershell/validate-task-grounding.ps1` |

---

**Questions?** → Review INTEGRATION_GUIDE.md > Troubleshooting
