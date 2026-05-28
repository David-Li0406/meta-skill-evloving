# Task Grounding Validation Checklist
**Version**: 1.0.0
**Purpose**: Standardized review rubric for validating task grounding analysis

---

## Pre-Validation Setup Checklist

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

## Report Validation Checklist

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

## Quality Standards Checklist

### ✅ Traceability Standards

**For each task-to-artifact mapping**:

- [ ] Mapping is not circular (doesn't cite task as evidence)
- [ ] Evidence from planning phase only (not implementation code)
- [ ] Evidence is from official artifacts, not comments/notes
- [ ] At least one artifact per task (minimum coverage)
- [ ] Cross-references to related tasks documented

### ✅ Accuracy Standards

- [ ] No artifact quotes altered or paraphrased without noting
- [ ] Artifact versions dated (if applicable)
- [ ] External references validated (e.g., "see spec.md") verified
- [ ] No assumptions presented as facts without marking [ASSUMED]
- [ ] Confidence levels noted where evidence is weak

### ✅ Actionability Standards

**For each recommendation**:

- [ ] Specific action (not "review the code")
- [ ] Clear owner/role (who does this?)
- [ ] Estimated effort stated (quick / medium / complex)
- [ ] Success criteria defined (how do we verify?)
- [ ] Blocked by anything? (dependencies noted)

### ✅ Clarity Standards

- [ ] Report is readable by non-technical stakeholders
- [ ] Technical terms explained or avoided
- [ ] Tables well-formatted (no overflowing cells)
- [ ] Verdict colors used consistently
- [ ] No contradictions between sections

---

## Decision Gate Checklist

### ✅ For APPROVED Status

**ALL of the following must be true**:

- [ ] ≥90% of Phase 1 tasks grounded at 80%+
- [ ] ≥80% of Phase 2 tasks grounded at 70%+
- [ ] ≥70% of Phase 3+ tasks grounded at 60%+
- [ ] No unresolved HIGH-risk gaps
- [ ] No critical inconsistencies in artifacts
- [ ] All external references verified as valid
- [ ] Clear implementation path documented

**Confidence Level**: 🟢 **≥80%**

---

### ⚠️ For NEEDS CLARIFICATION Status

**One or more of the following is true**:

- [ ] ≥1 Phase 1 task grounded at <60%
- [ ] ≥2 Phase 2 tasks grounded at <50%
- [ ] Moderate gaps with resolvable action items
- [ ] Inconsistencies between artifacts that need clarification
- [ ] External references need verification
- [ ] Implementation path has conditional dependencies

**Confidence Level**: 🟡 **50-79%**

**Next Step**: Return to planning phase, update artifacts, regenerate tasks.md

---

### 🔴 For BLOCKED Status

**One or more of the following is true**:

- [ ] >50% of tasks have grounding <50%
- [ ] Multiple CRITICAL gaps identified
- [ ] Artifact inconsistencies prevent implementation
- [ ] Major dependencies on unresolved planning questions
- [ ] Feature scope fundamentally unclear
- [ ] Risk assessment shows >50% HIGH-risk tasks

**Confidence Level**: 🔴 **<50%**

**Next Step**: Return to planning phase, resolve major gaps, regenerate spec + plan + tasks.md

---

## Reviewer Checklist

**Project Lead / Feature Owner** review before approving:

### ✅ Requirements Verification

- [ ] I read the spec.md for this feature
- [ ] I read the plan.md for this feature
- [ ] I understand the scope of work
- [ ] I've reviewed the grounding analysis report

### ✅ Artifact Consistency

- [ ] Artifacts agree on key technical decisions
- [ ] No contradictions between spec and plan
- [ ] Scope hasn't drifted from initial planning
- [ ] Assumptions explicitly documented

### ✅ Task Quality

- [ ] Tasks are at right level of granularity (not too big/small)
- [ ] Task dependencies are correct
- [ ] All critical path items covered
- [ ] No task is a duplicate

### ✅ Risk Awareness

- [ ] I understand the identified gaps
- [ ] I'm comfortable with recommended mitigations
- [ ] Team has capacity to address identified risks
- [ ] No blockers that would delay implementation

### ✅ Implementation Readiness

- [ ] All prerequisite tasks are complete
- [ ] Necessary technical decisions made
- [ ] Required infrastructure available
- [ ] Team has required skills/knowledge

### ✅ Final Decision

**Status**:
- [ ] APPROVED - Proceed to implementation
- [ ] NEEDS CLARIFICATION - Update artifacts and regenerate
- [ ] BLOCKED - Cannot proceed, return to planning

**Reviewer**: _________________ **Date**: _______ **Notes**: _____________

---

## Common Issues & How to Grade Them

### Issue: Task grounded in only 1 artifact

**Assessment**:
- If artifact is primary source document (spec.md, plan.md) → Accept as ✅
- If artifact is secondary (api-contracts.md) → Mark as ⚠️ Weak (60-70%)
- If artifact is inferred pattern → Mark as ⚠️ Weak (50-60%)

**Action**:
- Request additional cross-check in secondary artifacts
- Mark grounding level accordingly
- Note: "Grounded in [Artifact] only, recommend verification in [Other Artifact]"

---

### Issue: Task references external requirement (spec.md feature not documented)

**Assessment**:
- If requirement clearly stated in spec.md → Accept as ✅ (even if not in other artifacts)
- If requirement vague or implicit in spec.md → Mark as ⚠️ (60-70%)
- If requirement not found in spec.md → Mark as 🔴 (0-50%)

**Action**:
- Add note: "Grounded in spec.md FR-### [paraphrase]"
- If FR-### not clearly stated, request spec.md clarification
- Consider: Is this task invented by task generator?

---

### Issue: Inconsistency between artifacts (e.g., permission count mismatch)

**Assessment**:
- If inconsistency is in non-critical area → Minor ⚠️
- If inconsistency affects core functionality → Critical 🔴
- If inconsistency is documentation error → Document and resolve

**Action**:
- Create gap item: "Artifact inconsistency: [Item] differs in [Artifact1] vs [Artifact2]"
- Document both values and actual requirement
- Request decision: Which artifact is source of truth?
- Update other artifacts if needed

---

### Issue: Task assumes implementation pattern not documented

**Assessment**:
- If pattern is common in codebase → Accept as ✅ Implicit (70%)
- If pattern matches established architecture → Accept as ⚠️ Implicit (60%)
- If pattern unclear/unique → Mark as 🔴 Not Grounded (0-50%)

**Action**:
- Mark as "Implicit grounding - verify codebase pattern"
- Add to gap: "Implementation pattern X assumed, needs validation"
- Include action item: "Inspect codebase to confirm [Pattern]"

---

## Grounding Level Scale

**Use this rubric to assign grounding percentages**:

| Level | Definition | Evidence | Example |
|-------|-----------|----------|---------|
| 100% | Explicit in primary artifact | Direct specification with exact wording | "Add TenantFeatureFlag enum value [name]" in plan.md |
| 90% | Explicit in primary, confirmed in secondary | Clear spec + implementation example provided | Permission list fully specified in data-model.md |
| 80% | Explicit in primary artifact | Clear but missing some implementation detail | "Create seeder class" documented, implementation approach not specified |
| 70% | Explicit in primary, implicit in secondary | Requirement clear, implementation inferred from pattern | "Create role seeder" required, pattern followed from existing seeders |
| 60% | Explicit in secondary artifact only | Requirement found in supporting doc, not primary | Schema reference in contracts, not fully specified |
| 50% | Implicit across multiple artifacts | Requirement inferred from multiple sources, not stated directly | "Emit SentEvent" inferred from schema reference + pattern |
| 40% | Inferred from established pattern | No explicit requirement, but pattern is clear | "Use ICustomSeeder" inferred from existing seeder pattern |
| 30% | Weakly inferred from pattern | Pattern exists but not clearly applicable | Task assumes architecture pattern without strong evidence |
| 20% | External dependency | Requirement depends on unverified external doc | Task references spec.md, but spec.md not yet validated |
| 10% | Assumption only | No artifact evidence, pure assumption | Task invented without documented requirement |
| 0% | Not grounded | Task has no connection to artifacts | Spurious task |

---

## Red Flags Checklist

**Stop review if you see any of these**:

- [ ] ❌ Task with 0-20% grounding in critical phase
- [ ] ❌ Task contradicts documented requirement (opposite of spec)
- [ ] ❌ Same artifact quoted for >50% of tasks (lack of cross-check)
- [ ] ❌ "Grounding unknown" or similar placeholder in final report
- [ ] ❌ Gaps marked as "to be determined in implementation"
- [ ] ❌ Risk assessment missing for any high-grounding task (asymmetry)
- [ ] ❌ Decision gate not clearly stated at end
- [ ] ❌ >30% of tasks with "Needs verification" in Phase 1
- [ ] ❌ Circular references (task A grounded in task B grounded in task A)
- [ ] ❌ External reference (e.g., "see spec.md FR-001") not validated

**If ANY red flag found**: → Request clarification or mark BLOCKED

---

## Approval Signature

**Project Lead / Feature Owner**

I have reviewed the Task Grounding Analysis for feature _________________ and confirm:

- [ ] All tasks are grounded in planning artifacts
- [ ] Identified gaps are acceptable or have clear resolution paths
- [ ] I'm comfortable with the confidence level
- [ ] Risks have been assessed and mitigated

**Name**: _________________________ **Title**: _________________ **Date**: _______

**Status**:
- [ ] ✅ APPROVED
- [ ] ⚠️ NEEDS CLARIFICATION
- [ ] 🔴 BLOCKED

**Notes / Conditions**:
```
[Optional notes about decision]
```
