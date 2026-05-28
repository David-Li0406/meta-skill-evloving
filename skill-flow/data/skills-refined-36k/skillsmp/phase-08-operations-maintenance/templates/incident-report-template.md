# Incident Report Template

**Document ID:** P8-INC-{XXX}  
**Incident ID:** INC-{YYYYMMDD}-{XXX}  
**Status:** Open | Investigating | Resolved | Closed  
**Author:** {Incident Commander}  

---

## 1. Incident Summary

| Field | Value |
|-------|-------|
| **Title** | {Brief incident title} |
| **Severity** | SEV1 / SEV2 / SEV3 |
| **Service(s) Affected** | {Service names} |
| **Duration** | {X} hours {Y} minutes |
| **Impact** | {Brief impact description} |
| **Root Cause** | {One-line root cause} |

---

## 2. Timeline

| Time (UTC) | Event |
|------------|-------|
| {HH:MM} | Issue first detected by {monitoring/user report} |
| {HH:MM} | Alert triggered, on-call paged |
| {HH:MM} | Incident declared, war room started |
| {HH:MM} | Root cause identified |
| {HH:MM} | Fix deployed |
| {HH:MM} | Service restored |
| {HH:MM} | Incident resolved |

**Total Duration:** {X} hours {Y} minutes  
**Time to Detect (TTD):** {X} minutes  
**Time to Resolve (TTR):** {X} hours {Y} minutes

---

## 3. Impact Assessment

### 3.1 User Impact

| Metric | Value |
|--------|-------|
| Users Affected | {Number or percentage} |
| Requests Failed | {Number} |
| Revenue Impact | ${X} (estimated) |
| Geographic Regions | {Regions affected} |

### 3.2 Business Impact

- [ ] Customer-facing outage
- [ ] Data loss
- [ ] SLA breach
- [ ] Regulatory impact
- [ ] Reputation damage

### 3.3 SLA Impact

| SLA Metric | Target | Actual | Breach? |
|------------|--------|--------|---------|
| Availability | 99.9% | {X}% | Yes/No |
| Error Rate | < 1% | {X}% | Yes/No |

---

## 4. Root Cause Analysis

### 4.1 What Happened

{Detailed description of what occurred from a technical perspective}

### 4.2 Why It Happened

**Root Cause:**
{Detailed explanation of the underlying cause}

**Contributing Factors:**
1. {Factor 1}
2. {Factor 2}
3. {Factor 3}

### 4.3 Five Whys Analysis

1. **Why did the service fail?**
   {Answer 1}

2. **Why did {Answer 1} happen?**
   {Answer 2}

3. **Why did {Answer 2} happen?**
   {Answer 3}

4. **Why did {Answer 3} happen?**
   {Answer 4}

5. **Why did {Answer 4} happen?**
   {Answer 5 - Root cause}

---

## 5. Resolution

### 5.1 Immediate Fix

{Description of the fix applied to resolve the incident}

```bash
# Commands or changes applied
{Commands}
```

### 5.2 Verification

- [ ] Service health restored
- [ ] Metrics back to normal
- [ ] User reports stopped
- [ ] Monitoring confirmed

---

## 6. Lessons Learned

### 6.1 What Went Well

- {Positive observation 1}
- {Positive observation 2}

### 6.2 What Went Poorly

- {Negative observation 1}
- {Negative observation 2}

### 6.3 Where We Got Lucky

- {Lucky circumstance that prevented worse impact}

---

## 7. Action Items

| ID | Action | Owner | Priority | Due Date | Status |
|----|--------|-------|----------|----------|--------|
| AI-001 | {Action description} | {Name} | P1 | {Date} | ⬜ Open |
| AI-002 | {Action description} | {Name} | P1 | {Date} | ⬜ Open |
| AI-003 | {Action description} | {Name} | P2 | {Date} | ⬜ Open |
| AI-004 | {Action description} | {Name} | P3 | {Date} | ⬜ Open |

### 7.1 Action Categories

**Detection Improvements:**
- {Action to improve detection}

**Prevention:**
- {Action to prevent recurrence}

**Process Improvements:**
- {Action to improve incident response}

**Documentation:**
- {Runbook updates needed}

---

## 8. Incident Response Review

### 8.1 Response Effectiveness

| Aspect | Rating (1-5) | Notes |
|--------|--------------|-------|
| Detection | {X} | {Notes} |
| Communication | {X} | {Notes} |
| Investigation | {X} | {Notes} |
| Resolution | {X} | {Notes} |
| Documentation | {X} | {Notes} |

### 8.2 Communication Review

| Communication | Sent? | Timely? | Notes |
|---------------|-------|---------|-------|
| Internal alert | / | / | |
| Status page update | / | / | |
| Customer notification | / | / | |
| Executive update | / | / | |
| Resolution notification | / | / | |

---

## 9. Supporting Information

### 9.1 Related Tickets

| Ticket | Type | Status |
|--------|------|--------|
| {JIRA-XXX} | Bug fix | Open |
| {JIRA-XXX} | Improvement | Open |

### 9.2 Related Incidents

| Incident | Date | Similarity |
|----------|------|------------|
| INC-{XXX} | {Date} | {How related} |

### 9.3 Attachments

- {Link to dashboard screenshot}
- {Link to logs}
- {Link to war room recording}

---

## 10. Post-Mortem Meeting

| Field | Value |
|-------|-------|
| Date | {Date} |
| Attendees | {Names} |
| Facilitator | {Name} |
| Notes | {Link to meeting notes} |

---

## 11. Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Incident Commander | | | |
| Engineering Manager | | | |
| VP Engineering (SEV1 only) | | | |

---

**Incident Closed:** {Date}

---

**Document End**

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
