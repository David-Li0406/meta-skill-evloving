---
name: audit-readiness
description: Evaluate audit readiness of features, pages, or the overall platform. Use when the user asks to "check audit readiness", "test for auditors", "verify compliance evidence", "audit proof", or wants to ensure features will pass real BSI/ISO audits.
---

# Audit Readiness Skill

Evaluate whether LogiDocs Certify features meet the standards required to pass real ISO certification audits. Based on how BSI and other certification body auditors actually assess compliance systems.

## When to Use

- Before releasing compliance features
- Evaluating evidence retrieval capabilities
- Testing audit trail completeness
- Validating terminology accuracy
- Preparing for customer demos to consultants
- Quality assurance of QMS features

## Audit Readiness Framework

### 1. Evidence Accessibility Test

**Goal:** Can auditors find what they need quickly?

Test with common auditor requests:
```
"Show me your management review minutes"
"Show me evidence of supplier evaluation"
"Show me your internal audit schedule"
"Show me how you handle nonconformities"
"Show me your quality objectives and progress"
```

**Pass criteria:**
- Relevant evidence found in <30 seconds
- Evidence clearly identified (title, date, author)
- Links to source documents work
- Multiple search terms return correct results

### 2. Audit Trail Completeness

**Goal:** Is the "who, what, when" captured?

Check every record has:
- [ ] **What:** Clear description of the item
- [ ] **Who:** User who created/modified
- [ ] **When:** Timestamp (automatic, not manual)
- [ ] **Version:** Change history if applicable
- [ ] **Approval:** Workflow evidence if required

### 3. Terminology Accuracy

**Goal:** Does the platform speak ISO language?

Verify correct usage:

| Check For | Should Be | Not |
|-----------|-----------|-----|
| Evidence of compliance | Objective evidence | Proof |
| Issue/problem | Nonconformity | Defect, bug |
| Fix | Corrective action | Resolution |
| Papers | Documented information | Documents |
| Skills | Competence | Qualification |
| Review | Audit | Check |

### 4. Cross-Reference Integrity

**Goal:** Can auditors follow evidence trails?

Verify:
- Action links to source (MRM, Audit, NCR)
- NCR links to corrective action
- Corrective action links to verification
- Metric links to objective
- Evidence links to requirement

### 5. Status Accuracy

**Goal:** Does status reflect reality?

Verify status indicators:
- Green items are genuinely compliant
- Red items have real issues
- Overdue items show as overdue
- Expiring items show warnings
- No false positives/negatives

## Audit Simulation Checklist

Run through these auditor scenarios:

### Management Review (Clause 9.3)
```
□ Can find MRM minutes/records
□ Minutes show required inputs reviewed
□ Actions from MRM are tracked
□ Attendance/participants recorded
□ Outputs documented (decisions, actions, resources)
```

### Document Control (Clause 7.5)
```
□ Documents have version numbers
□ Can identify current version
□ Previous versions accessible
□ Change history available
□ Approval evidence present
□ Review dates tracked
```

### Internal Audit (Clause 9.2)
```
□ Audit schedule exists
□ All QMS areas covered over cycle
□ Auditor competence recorded
□ Audit reports retrievable
□ Findings tracked to closure
□ Audit program evidence
```

### Corrective Action (Clause 10.2)
```
□ NCR register accessible
□ Root cause analysis documented
□ Correction vs corrective action distinguished
□ Effectiveness verification recorded
□ Similar NCRs can be analyzed
```

### Supplier Management (Clause 8.4)
```
□ Approved supplier list exists
□ Evaluation criteria defined
□ Evaluation records available
□ Performance monitoring evident
□ Re-evaluation schedule tracked
```

## Evidence Quality Assessment

Rate each evidence item:

### Identification (1-5)
- 5: Clear title, unique reference, easy to find
- 3: Findable but title unclear
- 1: Ambiguous or hard to locate

### Authenticity (1-5)
- 5: Automatic timestamps, user attribution, tamper-evident
- 3: Manual dates, some attribution
- 1: No dates, no attribution, could be fabricated

### Completeness (1-5)
- 5: All required information present
- 3: Most information, some gaps
- 1: Missing critical information

### Traceability (1-5)
- 5: Clear links to sources, full trail
- 3: Some links, partial trail
- 1: No links, orphaned record

## Common Audit Failures

Watch for these issues:

### Major Nonconformity Risks
- No evidence of management review
- No internal audit records
- Missing corrective action process
- No supplier evaluation records
- Documents without version control

### Minor Nonconformity Risks
- Isolated missing records
- Incomplete audit trails
- Terminology inconsistencies
- Broken links to evidence
- Status indicators inaccurate

## Output Format

```markdown
## Audit Readiness Assessment: [Feature/Area]

### Overall Readiness: [Ready / At Risk / Not Ready]

### Evidence Accessibility
| Request | Found | Time | Quality |
|---------|-------|------|---------|
| "Management review minutes" | Y/N | Xs | 1-5 |

### Audit Trail Check
| Element | Present | Notes |
|---------|---------|-------|
| Who (user) | Y/N | ... |
| What (description) | Y/N | ... |
| When (timestamp) | Y/N | ... |
| Version | Y/N | ... |

### Terminology Issues
| Found | Should Be | Location |
|-------|-----------|----------|

### Potential Findings
| Type | Issue | Clause | Fix Required |
|------|-------|--------|--------------|
| Major/Minor | ... | X.X | ... |

### Recommendations
1. [Priority fix]
2. [Secondary fix]

### Auditor Verdict
> "[What an auditor would say about this]"
```

## Related Agents

- `auditor-simulator` - Deep audit simulation testing
- `iso-expert` - Clause and terminology validation
- `sirius-tester` - Consultant credibility check
