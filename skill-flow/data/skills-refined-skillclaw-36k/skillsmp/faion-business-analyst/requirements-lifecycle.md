---
id: requirements-lifecycle
name: "Requirements Lifecycle Management"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Requirements Lifecycle Management

## Metadata
- **Category:** BA Framework / Requirements Lifecycle Management
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #requirements #lifecycle #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

Requirements exist in multiple versions with no clarity on which is current. Approved requirements change without process. Some requirements are implemented differently than documented. At project end, nobody can reconstruct the history of requirements evolution.

Without lifecycle management:
- Version confusion
- Uncontrolled changes
- Implementation mismatches
- No audit trail

---

## Framework

### Requirements Lifecycle Stages

```
Identify → Analyze → Specify → Validate → Verify → Manage
                        ↑                            |
                        └────────────────────────────┘
                              (Continuous refinement)
```

| Stage | Purpose | Output |
|-------|---------|--------|
| **Identify** | Discover requirements | Raw requirements |
| **Analyze** | Understand and structure | Analyzed requirements |
| **Specify** | Document formally | Documented requirements |
| **Validate** | Confirm correctness | Validated requirements |
| **Verify** | Confirm implementation | Verified requirements |
| **Manage** | Control changes | Baselined requirements |

### Step 1: Identify Requirements

Gather raw requirements from sources:
- Stakeholder interviews
- Workshops
- Document analysis
- Observation
- Existing systems

### Step 2: Analyze Requirements

Process raw input:
- Categorize (business, stakeholder, solution)
- Identify relationships
- Detect conflicts
- Prioritize
- Assess feasibility

### Step 3: Specify Requirements

Document formally:
- Use standard templates
- Apply naming conventions
- Assign unique IDs
- Include all attributes
- Write clearly

### Step 4: Validate Requirements

Confirm requirements are correct:

| Validation Activity | Purpose |
|--------------------|---------|
| Stakeholder review | Confirm understanding |
| Walkthrough | Detailed examination |
| Prototype review | Visual validation |
| Acceptance criteria review | Testability check |

### Step 5: Verify Requirements

Confirm implementation matches requirements:

| Verification Activity | When |
|----------------------|------|
| Design review | During design |
| Code inspection | During development |
| Testing | During testing |
| User acceptance | Before release |

### Step 6: Manage Requirements

Ongoing management:
- Version control
- Change control
- Traceability maintenance
- Status tracking
- Communication

---

## Requirements States

| State | Description | Next State |
|-------|-------------|------------|
| **Draft** | Initial capture | Proposed |
| **Proposed** | Ready for review | Approved / Rejected |
| **Approved** | Accepted for implementation | Implemented |
| **Rejected** | Not accepted | - |
| **Implemented** | Built | Verified |
| **Verified** | Tested and confirmed | - |
| **Deferred** | Postponed to future | Proposed (later) |
| **Deleted** | Removed from scope | - |

```
Draft → Proposed → Approved → Implemented → Verified
                     ↓
                 Rejected
                     ↓
                 Deferred
```

---

## Templates

### Requirements Status Log

```markdown
# Requirements Status Log: [Project Name]

**Version:** [X.X]
**Date:** [Date]
**BA:** [Name]

## Status Summary

| Status | Count | % of Total |
|--------|-------|------------|
| Draft | [X] | [X%] |
| Proposed | [X] | [X%] |
| Approved | [X] | [X%] |
| Implemented | [X] | [X%] |
| Verified | [X] | [X%] |
| Deferred | [X] | [X%] |
| Rejected | [X] | [X%] |
| **Total** | **[X]** | **100%** |

## Detailed Status

| Req ID | Name | Status | Updated | Notes |
|--------|------|--------|---------|-------|
| REQ-001 | [Name] | Approved | [Date] | - |
| REQ-002 | [Name] | Implemented | [Date] | - |
| REQ-003 | [Name] | Deferred | [Date] | Phase 2 |
```

### Requirement Change Request

```markdown
# Requirement Change Request: CR-[XXX]

**Date:** [Date]
**Requestor:** [Name]
**Affected Requirement:** [REQ-XXX]

## Change Details

**Current Requirement:**
[Current text]

**Proposed Change:**
[New text or modification]

**Reason for Change:**
[Why this change is needed]

## Impact Analysis

| Area | Impact |
|------|--------|
| Requirements | [Related requirements affected] |
| Design | [Design changes needed] |
| Development | [Code changes needed] |
| Testing | [Test changes needed] |
| Schedule | [Timeline impact] |
| Cost | [Budget impact] |

## Recommendation
[BA recommendation: Approve / Reject / Defer]

## Approval

| Role | Name | Decision | Date |
|------|------|----------|------|
| BA | | | |
| Project Manager | | | |
| Sponsor | | | |

**Final Decision:** [Approved / Rejected / Deferred]
```

### Version History Template

```markdown
# Requirement Version History: [REQ-XXX]

**Requirement:** [Name]
**Current Version:** [X.X]

## Version History

| Version | Date | Author | Change Description | Status |
|---------|------|--------|--------------------|--------|
| 1.0 | [Date] | [Name] | Initial creation | Draft |
| 1.1 | [Date] | [Name] | Added acceptance criteria | Proposed |
| 1.2 | [Date] | [Name] | Stakeholder feedback incorporated | Approved |
| 2.0 | [Date] | [Name] | CR-005: Major scope change | Approved |

## Current Version Content
[Current requirement text]

## Previous Version (1.2)
[Previous requirement text for comparison]
```

---

## Examples

### Example 1: Requirement State Transitions

**REQ-045: Password Reset**

| Date | State Change | Trigger |
|------|--------------|---------|
| Jan 5 | Draft | Created from interview |
| Jan 8 | Proposed | Ready for review |
| Jan 10 | Approved | Stakeholder sign-off |
| Jan 25 | Implemented | Code complete |
| Feb 1 | Verified | Testing passed |

### Example 2: Change Request Flow

**CR-012: Modify login timeout**

1. **Request received:** User requests longer session timeout
2. **Impact analysis:**
   - REQ-030 (Session Management) affected
   - Security policy review needed
   - Test cases TC-50, TC-51 need update
3. **Decision:** Approved with modification (15 min → 30 min, not requested 60 min)
4. **Implementation:** Update REQ-030 v1.0 → v2.0

---

## Common Mistakes

1. **No version control** - Which version is current?
2. **Skipping validation** - Assuming requirements are correct
3. **No change process** - Ad-hoc modifications
4. **Status not updated** - Tracking becomes fiction
5. **No baseline** - Cannot compare to approved version

---

## Validation vs. Verification

| Aspect | Validation | Verification |
|--------|------------|--------------|
| **Question** | Are we building the right thing? | Are we building it right? |
| **When** | During requirements | After implementation |
| **How** | Reviews, walkthroughs | Testing, inspection |
| **Who** | Stakeholders, BA | QA, BA, Users |

---

## Requirements Attributes

Track these for each requirement:

| Attribute | Purpose |
|-----------|---------|
| **ID** | Unique identifier |
| **Name** | Short descriptive title |
| **Description** | Full requirement text |
| **Status** | Current lifecycle state |
| **Priority** | Importance (MoSCoW, 1-5) |
| **Source** | Where it came from |
| **Owner** | Who is responsible |
| **Version** | Current version number |
| **Created** | When created |
| **Modified** | Last update |
| **Author** | Who wrote it |

---

## Next Steps

After lifecycle setup:
1. Implement requirements repository
2. Define state transition rules
3. Train team on process
4. Monitor compliance
5. Connect to Solution Assessment methodology

---

## References

- BA Framework Guide v3 - Requirements Lifecycle Management
- BA industry Requirements Management Standards
