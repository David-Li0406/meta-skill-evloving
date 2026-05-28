---
id: requirements-validation
name: "Requirements Validation"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Requirements Validation

## Metadata
- **Category:** BA Framework / Requirements Lifecycle Management
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #validation #requirements #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

Requirements are documented but nobody confirms they are correct. Stakeholders sign off without truly understanding. Development builds what is written, not what was meant. After delivery, users say "this is not what we asked for."

Without validation:
- Wrong requirements built
- Expensive rework
- Stakeholder dissatisfaction
- Wasted effort

---

## Framework

### Validation vs. Verification

| Aspect | Validation | Verification |
|--------|------------|--------------|
| **Question** | Are we building the right thing? | Are we building it right? |
| **When** | Before development | After implementation |
| **Focus** | Requirements accuracy | Solution correctness |
| **Who** | Business stakeholders | QA, technical team |

### Validation Objectives

- Requirements are correct
- Requirements are complete
- Requirements are understood
- Requirements are agreed upon

### Step 1: Review Requirements

Examine requirements for quality:

| Quality Attribute | Check |
|-------------------|-------|
| **Correct** | Accurately represents stakeholder needs |
| **Complete** | All necessary information included |
| **Unambiguous** | Only one interpretation possible |
| **Consistent** | No conflicts with other requirements |
| **Testable** | Can create tests to verify |
| **Traceable** | Links to source and purpose |
| **Feasible** | Can be implemented |
| **Necessary** | No gold plating |

### Step 2: Choose Validation Technique

| Technique | Best For |
|-----------|----------|
| **Walkthrough** | Detailed examination |
| **Inspection** | Formal defect finding |
| **Prototype review** | Visual validation |
| **Simulation** | Process validation |
| **User acceptance review** | Business validation |

### Step 3: Conduct Validation Session

**Preparation:**
- Select requirements to review
- Identify participants
- Distribute materials in advance
- Prepare questions and scenarios

**During session:**
- Walk through requirements systematically
- Ask clarifying questions
- Document issues and questions
- Note agreements and decisions

### Step 4: Address Findings

For each issue found:
- Classify severity
- Determine root cause
- Plan resolution
- Update requirements
- Re-validate if needed

### Step 5: Obtain Sign-off

Formal acceptance that requirements are correct:
- Clear what is being approved
- Stakeholder has authority
- Document the approval
- Note any conditions

---

## Templates

### Requirements Review Checklist

```markdown
# Requirements Review Checklist: [Document/Feature]

**Reviewer:** [Name]
**Date:** [Date]
**Document Version:** [X.X]

## General Quality

| Criterion | Pass | Fail | N/A | Comments |
|-----------|------|------|-----|----------|
| Requirements are numbered/identified | | | | |
| Language is clear and unambiguous | | | | |
| No TBD or placeholder text | | | | |
| Consistent terminology used | | | | |
| No duplicate requirements | | | | |

## Individual Requirement Check

For each requirement:

| Check | Pass | Fail |
|-------|------|------|
| Necessary (not gold plating) | | |
| Correct (accurately represents need) | | |
| Complete (all info present) | | |
| Unambiguous (single interpretation) | | |
| Testable (can verify completion) | | |
| Feasible (can be built) | | |
| Traceable (links to source) | | |
| Consistent (no conflicts) | | |

## Completeness Check

| Check | Yes | No | Comments |
|-------|-----|-----|----------|
| All user types covered | | | |
| All functions covered | | | |
| Error handling defined | | | |
| Performance requirements stated | | | |
| Security requirements stated | | | |
| Integration requirements stated | | | |

## Issues Found

| ID | Requirement | Issue | Severity | Recommendation |
|----|-------------|-------|----------|----------------|
| 1 | [REQ-XX] | [Issue description] | H/M/L | [Fix] |

## Summary
- **Requirements Reviewed:** [X]
- **Issues Found:** [X]
- **Recommendation:** [Approve / Approve with changes / Revise and re-review]
```

### Validation Session Agenda

```markdown
# Requirements Validation Session

**Date:** [Date]
**Time:** [Time]
**Location:** [Room/Virtual]
**Facilitator:** [Name]

## Objectives
- Validate [document/feature] requirements
- Identify gaps and issues
- Obtain stakeholder sign-off

## Participants

| Name | Role | Responsibility |
|------|------|----------------|
| [Name] | [Role] | [Responsibility in session] |

## Agenda

| Time | Topic | Duration |
|------|-------|----------|
| 0:00 | Welcome, objectives | 10 min |
| 0:10 | Requirements walkthrough | 45 min |
| 0:55 | Discussion and questions | 20 min |
| 1:15 | Issue resolution | 15 min |
| 1:30 | Sign-off discussion | 15 min |
| 1:45 | Next steps | 5 min |

## Pre-work
Participants should review:
- [Document 1]
- [Document 2]

## Output
- Validated requirements
- Issue log
- Sign-off (or action plan)
```

### Requirements Sign-off Form

```markdown
# Requirements Sign-off: [Document Name]

**Document Version:** [X.X]
**Date:** [Date]

## Scope of Sign-off
This sign-off confirms that:
- [ ] Requirements accurately represent business needs
- [ ] Requirements are complete for [scope]
- [ ] Requirements are understood and agreed
- [ ] Requirements can proceed to [next phase]

## Conditions
[Any conditions or assumptions for this sign-off]

## Outstanding Items
[Items not covered but tracked separately]

| Item | Owner | Target Date |
|------|-------|-------------|
| [Item] | [Name] | [Date] |

## Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Business Owner | | | |
| Product Owner | | | |
| Technical Lead | | | |
| Project Manager | | | |

## Notes
[Any additional notes or context]
```

---

## Examples

### Example 1: Walkthrough Session

**Scenario:** Validating payment processing requirements

**Participants:**
- Product Owner (business perspective)
- Finance SME (domain expertise)
- Tech Lead (feasibility)
- BA (facilitation)

**Walkthrough approach:**
1. Read each requirement aloud
2. Ask: "Is this correct?"
3. Ask: "Is anything missing?"
4. Ask: "Can we test this?"
5. Document feedback

**Issues found:**
- REQ-45: Missing currency handling
- REQ-48: Ambiguous "reasonable time"
- REQ-52: Conflicts with REQ-47

### Example 2: Prototype Validation

**Scenario:** Validating UI requirements through prototype

**Approach:**
1. Show prototype to end users
2. Ask them to complete tasks
3. Observe where they struggle
4. Note differences from expectations

**Findings:**
- Users expected "Save" button on top (not bottom)
- Search results pagination confusing
- Missing filter option identified

**Updates:**
- 3 requirements modified
- 2 requirements added
- Prototype updated for re-validation

---

## Common Mistakes

1. **Rubber stamp approval** - Signing without reading
2. **Wrong participants** - Missing key stakeholders
3. **Too much at once** - Reviewing 200 requirements in one session
4. **No follow-up** - Issues found but not resolved
5. **Skipping validation** - Straight to development

---

## Validation Techniques Detail

### Walkthrough
- Informal, collaborative
- Author presents requirements
- Participants ask questions
- Good for early-stage validation

### Inspection
- Formal, structured
- Checklist-based
- Defect focus
- Good for critical requirements

### Prototype Review
- Visual, interactive
- User performs tasks
- Shows vs. tells
- Good for UI/UX requirements

### Simulation
- Process-focused
- Step through scenarios
- Find gaps in flow
- Good for process requirements

---

## When to Validate

| Trigger | Validation Activity |
|---------|---------------------|
| Requirements drafted | Initial review |
| Major changes made | Re-validation |
| Before design starts | Formal sign-off |
| Prototype available | User validation |
| Before UAT | Final confirmation |

---

## Next Steps

After validation:
1. Update requirements with findings
2. Re-validate if significant changes
3. Baseline approved requirements
4. Begin design/development
5. Connect to Requirements Prioritization methodology

---

## References

- BA Framework Guide v3 - Requirements Lifecycle Management
- BA industry Requirements Validation Guidelines
