---
id: quality-management
name: "Quality Management"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Quality Management

## Metadata
- **Category:** Project Management Framework 7 - Delivery Performance Domain
- **Difficulty:** Intermediate
- **Tags:** #product, #methodology, #pmbok
- **Read Time:** 8 min
- **Agent:** faion-pm-agent

---

## Problem

Poor quality leads to:
- Rework consuming 20-40% of project time
- Customer dissatisfaction and churn
- Technical debt accumulating
- Team morale declining from constant firefighting

## Framework

### Quality Concepts

| Concept | Definition |
|---------|------------|
| **Quality** | Degree to which requirements are met |
| **Grade** | Category/rank of features (premium vs basic) |
| **Prevention** | Building quality in (better than detection) |
| **Detection** | Finding defects (testing, reviews) |

### Three Quality Processes

```
Plan Quality → Manage Quality → Control Quality
     ↓              ↓                ↓
  Standards     Processes         Verification
```

### Step 1: Plan Quality

Define quality standards before work begins:

**Quality Metrics:**
| Type | Example Metrics |
|------|-----------------|
| **Product** | Performance, reliability, usability |
| **Process** | Defect rate, code coverage, review completion |
| **Perception** | Customer satisfaction, NPS |

### Step 2: Manage Quality (Assurance)

Ensure processes produce quality:

**Quality Assurance Activities:**
- Code review standards
- Definition of Done
- Automated testing requirements
- Documentation standards
- Regular audits/retrospectives

### Step 3: Control Quality

Verify deliverables meet standards:

**Quality Control Activities:**
- Testing (unit, integration, UAT)
- Inspections and reviews
- Checklists verification
- Defect tracking and resolution

---

## Templates

### Definition of Done (DoD)

```markdown
## Definition of Done

A feature is "Done" when:

### Code Quality
- [ ] Code compiles without warnings
- [ ] All unit tests pass
- [ ] Test coverage > 80%
- [ ] No critical/high security issues
- [ ] Code reviewed and approved

### Documentation
- [ ] README updated (if needed)
- [ ] API documentation complete
- [ ] User-facing changes documented

### Deployment
- [ ] Deployed to staging
- [ ] QA verified in staging
- [ ] Performance acceptable
- [ ] Rollback plan documented

### Acceptance
- [ ] Product Owner approved
- [ ] Acceptance criteria met
- [ ] No blocking bugs
```

### Quality Checklist

```markdown
## Quality Checklist - [Feature Name]

### Code Quality
- [ ] Follows coding standards
- [ ] No code smells (SonarQube clean)
- [ ] Error handling implemented
- [ ] Logging added for debugging
- [ ] Edge cases covered

### Testing
- [ ] Unit tests written and passing
- [ ] Integration tests (if applicable)
- [ ] Manual QA completed
- [ ] Regression testing done

### Performance
- [ ] Page loads < 3 seconds
- [ ] API response < 500ms
- [ ] No memory leaks
- [ ] Tested with realistic data volume

### Security
- [ ] Input validation
- [ ] Authentication checked
- [ ] No sensitive data exposed
- [ ] SQL injection prevention

### Accessibility
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast compliant
- [ ] Alt text for images
```

### Defect Report Template

```markdown
## Defect Report

**ID:** BUG-2024-042
**Severity:** Critical / High / Medium / Low
**Priority:** P1 / P2 / P3

### Summary
Login fails with valid credentials on Safari browser

### Steps to Reproduce
1. Open Safari 17.x on macOS
2. Navigate to /login
3. Enter valid email and password
4. Click "Sign In"

### Expected Result
User is logged in and redirected to dashboard

### Actual Result
Error message "Invalid credentials" displayed

### Environment
- Browser: Safari 17.2
- OS: macOS Sonoma 14.2
- Device: MacBook Pro M3

### Screenshots/Logs
[Attach relevant screenshots or console logs]

### Root Cause
[To be filled during investigation]

### Resolution
[To be filled when fixed]
```

---

## Examples

### Example 1: Quality Metrics Dashboard

```markdown
## Quality Dashboard - Sprint 15

### Code Quality
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Test Coverage | > 80% | 85% | OK |
| Code Review Completion | 100% | 100% | OK |
| Critical Bugs | 0 | 0 | OK |
| Technical Debt | < 2 days | 1.5 days | OK |

### Process Quality
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| DoD Compliance | 100% | 95% | WARNING |
| Sprint Completion | > 85% | 90% | OK |
| Defect Escape Rate | < 5% | 3% | OK |

### Product Quality
| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Customer Satisfaction | > 4.5 | 4.6 | OK |
| Uptime | > 99.9% | 99.95% | OK |
| Response Time | < 500ms | 320ms | OK |
```

### Example 2: Quality for Solopreneurs

```markdown
## My Quality Checklist

Before shipping anything:

### Content
- [ ] Proofread for typos
- [ ] Links all work
- [ ] Images load properly
- [ ] Mobile responsive

### Code
- [ ] Works in Chrome, Safari, Firefox
- [ ] No console errors
- [ ] Form validation works
- [ ] Thank you page displays

### Customer Experience
- [ ] Clear next step for user
- [ ] Support email visible
- [ ] Privacy policy linked
- [ ] Terms of service linked

Time to quality check: 30 minutes
Worth it: Always (bugs = lost customers)
```

---

## Common Mistakes

1. **Quality as afterthought** - Build it in, don't test it in
2. **Skipping code reviews** - "We're in a hurry" creates technical debt
3. **No Definition of Done** - "Done" means different things to different people
4. **Ignoring minor bugs** - They accumulate into major problems
5. **Not measuring quality** - What gets measured gets managed

---

## Related Methodologies

- **Change Control:** Managing quality-related changes
- **Usability Testing:** UX quality validation
- **Code Review Process:** Development quality assurance

---

*Methodology from Project Management Framework 7 - Delivery Performance Domain*
