# Standard Operating Procedures (SOPs) Framework

## Purpose

SOPs are the building blocks of operational excellence. A good SOP lets anyone perform a task correctly without additional guidance.

---

## What Makes a Good SOP

### Characteristics

| Characteristic | Good SOP | Bad SOP |
|----------------|----------|---------|
| Completeness | All steps included | "You know the rest" |
| Clarity | Unambiguous actions | "Adjust as needed" |
| Testability | Can verify completion | Unclear success state |
| Accessibility | Easy to find/follow | Hidden or convoluted |
| Maintainability | Easy to update | Outdated within weeks |

### The "Anyone" Test

A good SOP should be usable by:
- A new hire on day one
- You in 6 months (when you've forgotten)
- An AI assistant or automation
- A contractor with zero context

---

## SOP Structure

### Essential Components

```markdown
## SOP: {Process Name}

### Metadata
- Version: {X.Y}
- Last Updated: {YYYY-MM-DD}
- Owner: {who maintains this}
- Review Cycle: {frequency}

### Purpose
{Why this process exists - one paragraph max}

### Scope
- Applies to: {when/what}
- Does NOT apply to: {exceptions}

### Prerequisites
- [ ] {Access/permission needed}
- [ ] {Tool/system needed}
- [ ] {Information needed}

### Steps
1. **{Action verb}** - {specific action}
   - Detail: {additional context if needed}
   - Note: {gotchas or tips}

2. **{Action verb}** - {specific action}
   - If {condition}: {do this}
   - Otherwise: {do that}

3. **{Action verb}** - {specific action}

### Output
{What this process produces/achieves}

### Quality Check
- [ ] {Verification step 1}
- [ ] {Verification step 2}

### Troubleshooting
| Issue | Cause | Solution |
|-------|-------|----------|
| {problem} | {why} | {fix} |

### Related
- {Link to related SOP}
- {Link to tool/system}
```

---

## SOP Categories

### Critical SOPs (Must Have)

| Category | SOPs to Create |
|----------|----------------|
| **Customer Support** | Responding to tickets, Escalation process, Refund handling |
| **Security** | Access management, Incident response, Data backup |
| **Financial** | Invoice processing, Expense tracking, Tax prep |
| **Product** | Release process, Bug triage, Feature requests |

### Operational SOPs (Should Have)

| Category | SOPs to Create |
|----------|----------------|
| **Marketing** | Content publishing, Social posting, Newsletter sending |
| **Sales** | Lead qualification, Demo process, Follow-up |
| **Onboarding** | User setup, Welcome sequence, Feature intro |
| **Maintenance** | Database cleanup, Log rotation, Performance check |

### Emergency SOPs (Critical)

| Category | SOPs to Create |
|----------|----------------|
| **Outages** | Service restoration, Communication template, Post-mortem |
| **Security** | Breach response, User notification, Containment |
| **Data** | Recovery process, Backup restoration, Integrity check |

---

## Writing Effective Steps

### Use Action Verbs

| Good | Bad |
|------|-----|
| "Click the Submit button" | "The Submit button" |
| "Enter the customer email" | "Customer email field" |
| "Verify the total is correct" | "Check total" |
| "Send the notification" | "Notification" |

### Be Specific

| Vague | Specific |
|-------|----------|
| "Update the record" | "Set status to 'Complete' in the Order table" |
| "Notify the team" | "Post in #alerts Slack channel with error message" |
| "Check the logs" | "Run `grep ERROR /var/log/app.log | tail -20`" |
| "Adjust as needed" | "If value > 100, reduce by 10%" |

### Handle Decisions

```markdown
5. **Evaluate** - Check the payment status
   - If status is "SUCCEEDED":
     - Continue to step 6
   - If status is "PENDING":
     - Wait 30 minutes
     - Return to step 5
   - If status is "FAILED":
     - Jump to Troubleshooting section
```

---

## SOP Maintenance

### Version Control

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 1.0 | 2024-01-01 | Initial creation | Name |
| 1.1 | 2024-02-15 | Added step 4 | Name |
| 2.0 | 2024-06-01 | Major revision | Name |

### Review Triggers

- **Scheduled:** Quarterly review of all SOPs
- **Event-based:** After any process failure
- **Change-based:** When tools/systems change
- **Request-based:** When user reports confusion

### Review Checklist

- [ ] All steps still accurate?
- [ ] Screenshots/examples current?
- [ ] Links still work?
- [ ] Tools referenced still used?
- [ ] Common issues documented?
- [ ] Owner still appropriate?

---

## SOP Organization

### Naming Convention

```
{Category}-{Action}-{Subject}.md

Examples:
support-handle-refund.md
ops-backup-database.md
marketing-publish-newsletter.md
security-respond-incident.md
```

### Folder Structure

```
docs/sops/
├── support/
│   ├── handle-ticket.md
│   ├── escalate-issue.md
│   └── process-refund.md
├── operations/
│   ├── backup-database.md
│   ├── deploy-release.md
│   └── monitor-health.md
├── marketing/
│   ├── publish-blog.md
│   └── send-newsletter.md
└── emergency/
    ├── respond-outage.md
    └── handle-breach.md
```

---

## SOP Quality Levels

### Level 1: Basic
- Steps listed
- Can be followed
- Minimal detail

### Level 2: Complete
- All steps with detail
- Decision trees included
- Troubleshooting section

### Level 3: Excellent
- Fully tested
- Video/screenshots
- Automation-ready
- Metrics tracked

### Quality Matrix

| Aspect | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| Steps | Listed | Detailed | With media |
| Decisions | Implicit | Documented | Flowcharted |
| Errors | Not covered | Listed | With fixes |
| Verification | None | Checklist | Automated |
| Maintenance | Ad-hoc | Scheduled | Continuous |

---

## Common SOP Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Too vague | Can't follow | Be specific |
| Too detailed | Overwhelming | Focus on actions |
| No verification | Don't know if done right | Add quality checks |
| Missing context | Confusion on when to use | Add scope section |
| Never updated | Becomes wrong | Schedule reviews |
| Hard to find | Not used | Good organization |

---

## SOP Testing Protocol

### Before Publishing

1. **Walk-through test**
   - Follow SOP yourself
   - Note any confusion
   - Update unclear steps

2. **Fresh eyes test**
   - Have someone else follow it
   - Watch without helping
   - Note where they struggle

3. **Edge case test**
   - Try unusual inputs
   - Try error scenarios
   - Document exceptions

### After Publishing

- Track completion rate
- Log issues encountered
- Measure time to complete
- Gather improvement suggestions

---

## Output Format

```markdown
## SOP Inventory

### Critical (P0)
| SOP | Status | Owner | Last Updated |
|-----|--------|-------|--------------|
| {name} | {Draft/Ready/Review} | {who} | {date} |

### Operational (P1)
| SOP | Status | Owner | Last Updated |
|-----|--------|-------|--------------|
| {name} | {status} | {who} | {date} |

### To Create
1. {SOP name} - {priority}
2. {SOP name} - {priority}

### To Review
1. {SOP name} - {last updated, issues}
2. {SOP name} - {last updated, issues}
```
