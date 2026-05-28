---
id: solution-assessment
name: "Solution Assessment"
domain: BA
skill: faion-business-analyst
category: "business-analysis"
---

# Solution Assessment

## Metadata
- **Category:** BA Framework / Solution Evaluation
- **Difficulty:** Intermediate
- **Tags:** #methodology #babok #assessment #evaluation #business-analysis
- **Agent:** faion-ba-agent

---

## Problem

Solutions are built but nobody evaluates if they meet business needs. Users complain about issues but feedback is not structured. The gap between what was promised and what was delivered remains unclear. Lessons are not captured for future initiatives.

Without solution assessment:
- Value not measured
- Issues not systematically addressed
- No improvement loop
- Repeated mistakes

---

## Framework

### What is Solution Assessment?

Solution Assessment evaluates a solution's ability to meet the business need and deliver expected value. It happens both during development and after deployment.

### Assessment Types

| Type | When | Purpose |
|------|------|---------|
| **Design Assessment** | During design | Validate proposed solution |
| **Implementation Assessment** | During build | Verify correct implementation |
| **Deployment Assessment** | At go-live | Confirm readiness |
| **Post-Implementation Assessment** | After deployment | Measure actual value |

### Step 1: Define Assessment Criteria

What makes the solution successful?

| Category | Examples |
|----------|----------|
| **Business Value** | ROI achieved, revenue increased |
| **Functional** | Features work as specified |
| **Performance** | Speed, reliability, scalability |
| **Usability** | User satisfaction, adoption rate |
| **Compliance** | Regulatory requirements met |

### Step 2: Assess Against Requirements

Compare solution to requirements:

| Requirement | Expected | Actual | Gap | Status |
|-------------|----------|--------|-----|--------|
| REQ-001 | [Expected] | [Actual] | [Gap] | Met/Not Met |

### Step 3: Evaluate Business Value

Measure delivered value:

| Metric | Baseline | Target | Actual | Variance |
|--------|----------|--------|--------|----------|
| [Metric] | [Before] | [Goal] | [Now] | [+/-] |

### Step 4: Identify Limitations

Document solution gaps:

| Limitation | Impact | Recommendation |
|------------|--------|----------------|
| [Issue] | [Impact] | [Action] |

### Step 5: Recommend Actions

Based on assessment:
- Accept solution as-is
- Accept with remediation plan
- Require additional changes
- Reject and rework

---

## Templates

### Solution Assessment Report

```markdown
# Solution Assessment Report: [Solution Name]

**Version:** [X.X]
**Date:** [Date]
**Assessor:** [Name]
**Assessment Type:** [Design/Implementation/Deployment/Post-Implementation]

## Executive Summary
[Brief overview of assessment findings]

## Assessment Scope
- **Solution:** [What was assessed]
- **Period:** [Assessment timeframe]
- **Participants:** [Who was involved]

## Requirements Compliance

| Req ID | Requirement | Status | Notes |
|--------|-------------|--------|-------|
| REQ-001 | [Requirement] | Met/Partially/Not Met | [Notes] |
| REQ-002 | [Requirement] | Met/Partially/Not Met | [Notes] |

**Compliance Summary:**
- Requirements Met: [X] ([X%])
- Partially Met: [X] ([X%])
- Not Met: [X] ([X%])

## Business Value Assessment

| Metric | Baseline | Target | Actual | Variance | Status |
|--------|----------|--------|--------|----------|--------|
| [Metric 1] | [Value] | [Value] | [Value] | [+/-X%] | On Track |
| [Metric 2] | [Value] | [Value] | [Value] | [+/-X%] | At Risk |

## User Feedback

| Aspect | Rating | Comments |
|--------|--------|----------|
| Usability | [1-5] | [Feedback] |
| Performance | [1-5] | [Feedback] |
| Functionality | [1-5] | [Feedback] |

**User Satisfaction Score:** [X/5]

## Identified Issues

| Issue | Severity | Impact | Recommendation |
|-------|----------|--------|----------------|
| [Issue 1] | Critical/High/Medium/Low | [Impact] | [Action] |
| [Issue 2] | Critical/High/Medium/Low | [Impact] | [Action] |

## Limitations and Constraints

| Limitation | Business Impact | Workaround |
|------------|-----------------|------------|
| [Limitation] | [Impact] | [Workaround] |

## Recommendations

### Immediate Actions (0-30 days)
1. [Action 1]
2. [Action 2]

### Short-term (30-90 days)
1. [Action 1]
2. [Action 2]

### Long-term (90+ days)
1. [Action 1]

## Conclusion
**Overall Assessment:** [Meets Requirements / Partially Meets / Does Not Meet]

**Recommendation:** [Accept / Accept with conditions / Require changes / Reject]
```

### Post-Implementation Review Template

```markdown
# Post-Implementation Review: [Solution Name]

**Review Date:** [Date]
**Solution Go-Live:** [Date]
**Review Period:** [X months post go-live]
**Reviewer:** [Name]

## Business Outcomes

### Original Business Case

| Benefit | Projected Value | Projected Timeframe |
|---------|-----------------|---------------------|
| [Benefit 1] | [$X] or [X%] | [Timeframe] |
| [Benefit 2] | [$X] or [X%] | [Timeframe] |

### Actual Results

| Benefit | Projected | Actual | Variance | Status |
|---------|-----------|--------|----------|--------|
| [Benefit 1] | [Value] | [Value] | [+/-X%] | Achieved |
| [Benefit 2] | [Value] | [Value] | [+/-X%] | Partially |

## Adoption Metrics

| Metric | Target | Actual | Notes |
|--------|--------|--------|-------|
| User adoption rate | [X%] | [X%] | - |
| Feature usage | [X%] | [X%] | - |
| Training completion | [X%] | [X%] | - |

## Issues Encountered

| Issue | Resolution | Time to Resolve |
|-------|------------|-----------------|
| [Issue] | [How resolved] | [Duration] |

## Lessons Learned

### What Worked Well
- [Item 1]
- [Item 2]

### What Could Be Improved
- [Item 1]
- [Item 2]

## Recommendations

### Enhancement Opportunities
1. [Opportunity 1]
2. [Opportunity 2]

### Process Improvements
1. [Improvement 1]
2. [Improvement 2]

## Stakeholder Feedback Summary
[Summary of stakeholder input]

## Conclusion
[Overall assessment of solution success]
```

---

## Examples

### Example 1: CRM Implementation Assessment

**Requirements Compliance:**
- 85% fully met
- 10% partially met
- 5% not met (deferred to phase 2)

**Business Value:**

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Lead conversion | +20% | +18% | On track |
| Sales cycle | -15% | -12% | Behind |
| Data accuracy | 95% | 97% | Exceeded |

**Recommendation:** Accept with remediation plan for sales cycle improvement.

### Example 2: User Feedback Analysis

**Survey Results (n=50 users):**

| Question | Score (1-5) |
|----------|-------------|
| Easy to learn | 4.2 |
| Meets my needs | 3.8 |
| Performance acceptable | 3.5 |
| Would recommend | 3.9 |

**Key Feedback Themes:**
1. Performance needs improvement (mentioned 15 times)
2. Missing export feature (mentioned 8 times)
3. Training materials helpful (mentioned 12 times)

---

## Common Mistakes

1. **No baseline** - Cannot measure improvement
2. **Skipping assessment** - Moving to next project
3. **Only functional testing** - Not measuring business value
4. **Ignoring user feedback** - Technical metrics only
5. **One-time assessment** - No ongoing monitoring

---

## Assessment Metrics

| Category | Metrics |
|----------|---------|
| **Business** | ROI, revenue, cost savings, market share |
| **Operational** | Efficiency, throughput, error rate |
| **User** | Satisfaction, adoption, usage frequency |
| **Technical** | Performance, reliability, scalability |
| **Compliance** | Audit findings, violations |

---

## When to Assess

| Trigger | Assessment Type |
|---------|-----------------|
| Design complete | Design review |
| Sprint complete | Implementation check |
| Before go-live | Deployment readiness |
| 30 days post go-live | Initial assessment |
| 90 days post go-live | Full assessment |
| Annually | Ongoing value assessment |

---

## Next Steps

After assessment:
1. Present findings to stakeholders
2. Prioritize remediation
3. Update project documentation
4. Capture lessons learned
5. Connect to Business Process Analysis methodology

---

## References

- BA Framework Guide v3 - Solution Evaluation
- BA industry Solution Assessment Guidelines
