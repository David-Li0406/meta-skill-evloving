# Operations Playbook Template

Use this template to document your entire operations setup for a product.

---

## Template

```markdown
# Operations Playbook: {Product Name}

**Version:** {X.Y}
**Last Updated:** {YYYY-MM-DD}
**Owner:** {Name}

---

## Quick Reference

### Emergency Contacts

| Situation | Contact | Method |
|-----------|---------|--------|
| System outage | {who} | {how} |
| Security issue | {who} | {how} |
| Customer escalation | {who} | {how} |

### Critical Links

| System | URL | Access |
|--------|-----|--------|
| Production | {url} | {how to access} |
| Admin panel | {url} | {credentials location} |
| Monitoring | {url} | {how to access} |
| Support inbox | {url} | {who has access} |

---

## Team & Roles

### Current Team

| Name | Role | Responsibilities | Contact |
|------|------|------------------|---------|
| {Name} | Founder | Everything else | {contact} |
| {Name} | {Role} | {responsibilities} | {contact} |

### Responsibilities Matrix

| Function | Owner | Backup |
|----------|-------|--------|
| Customer support | {name} | {name} |
| Technical ops | {name} | {name} |
| Marketing | {name} | {name} |
| Finance | {name} | {name} |

---

## Daily Operations

### Morning Checklist

- [ ] Check system monitoring dashboard
- [ ] Review overnight support tickets
- [ ] Check payment/billing alerts
- [ ] Review analytics for anomalies
- [ ] Check social mentions

### Daily Tasks

| Task | When | Owner | SOP |
|------|------|-------|-----|
| {task} | {time} | {who} | [Link](sops/xxx.md) |

### End of Day

- [ ] Respond to all urgent tickets
- [ ] Update task tracking
- [ ] Set priorities for tomorrow

---

## Weekly Operations

### Weekly Review (Day: {day})

**Agenda:**
1. Metrics review
2. Support summary
3. Technical health
4. Upcoming priorities
5. Blockers

**Output:** Weekly update to {stakeholders}

### Weekly Tasks

| Task | Day | Owner | SOP |
|------|-----|-------|-----|
| {task} | {day} | {who} | [Link](sops/xxx.md) |
| Backup verification | {day} | {who} | |
| Metrics report | {day} | {who} | |

---

## Monthly Operations

### Monthly Tasks

| Task | When | Owner | SOP |
|------|------|-------|-----|
| Invoice customers | 1st | {who} | |
| Pay contractors | 1st | {who} | |
| Financial reconciliation | 5th | {who} | |
| Metrics deep dive | 15th | {who} | |
| SOP review | Last week | {who} | |

### Monthly Review

**Metrics to review:**
- MRR and changes
- User growth
- Churn rate
- Support volume
- System uptime

---

## Support Operations

### Support Channels

| Channel | SLA | Owner | Hours |
|---------|-----|-------|-------|
| Email | < 24h | {who} | {hours} |
| In-app chat | < 1h | {who} | {hours} |
| Twitter/Social | < 4h | {who} | {hours} |

### Ticket Categories

| Category | Priority | Target Resolution |
|----------|----------|-------------------|
| Bug - Critical | P0 | < 4 hours |
| Bug - Major | P1 | < 24 hours |
| Bug - Minor | P2 | < 1 week |
| Feature request | P3 | Logged |
| Question | P2 | < 24 hours |
| Billing | P1 | < 24 hours |

### Escalation Matrix

| Level | Trigger | Action |
|-------|---------|--------|
| L1 | Standard ticket | Follow SOP |
| L2 | Can't resolve | Escalate to {who} |
| L3 | Technical issue | Escalate to {who} |
| L4 | Customer at risk | Founder involvement |

### Common Issues & Solutions

| Issue | Solution | SOP |
|-------|----------|-----|
| {common issue 1} | {solution} | [Link] |
| {common issue 2} | {solution} | [Link] |

---

## Technical Operations

### Systems Overview

```
{Architecture diagram or description}

User → CDN → App Server → Database
              ↓
         Background Jobs → External APIs
```

### Monitoring

| System | Tool | Alert Channel |
|--------|------|---------------|
| Uptime | {tool} | {channel} |
| Errors | {tool} | {channel} |
| Performance | {tool} | {channel} |
| Security | {tool} | {channel} |

### Deployment

**Process:**
1. {Step 1}
2. {Step 2}
3. {Step 3}

**Rollback:**
1. {How to rollback}

**SOP:** [Deployment SOP](sops/deployment.md)

### Backups

| Data | Frequency | Retention | Verification |
|------|-----------|-----------|--------------|
| Database | {freq} | {period} | {how verified} |
| Files | {freq} | {period} | {how verified} |
| Code | Continuous | Forever | {how verified} |

---

## Financial Operations

### Revenue

| Source | Processing | Payout |
|--------|------------|--------|
| Subscriptions | {processor} | {when} |
| One-time | {processor} | {when} |

### Expenses

| Category | Typical Amount | Due Date |
|----------|---------------|----------|
| Hosting | ${X}/mo | {date} |
| Tools | ${X}/mo | Various |
| Contractors | ${X}/mo | {date} |

### Financial Tasks

| Task | Frequency | Owner |
|------|-----------|-------|
| Invoice reconciliation | Weekly | {who} |
| Expense tracking | Weekly | {who} |
| Tax preparation | Quarterly | {who} |

---

## Marketing Operations

### Content Calendar

| Day | Content Type | Channel |
|-----|--------------|---------|
| {day} | {type} | {where} |

### Regular Marketing Tasks

| Task | Frequency | Owner |
|------|-----------|-------|
| {task} | {freq} | {who} |

---

## Emergency Procedures

### Incident Response

**For any major incident:**

1. **ASSESS** - What's happening? Who's affected?
2. **COMMUNICATE** - Update status page, notify users
3. **CONTAIN** - Stop the bleeding
4. **RESOLVE** - Fix the issue
5. **REVIEW** - Post-mortem within 48 hours

### Incident Severity

| Level | Definition | Response Time |
|-------|------------|---------------|
| P0 - Critical | Service down, data at risk | Immediate |
| P1 - Major | Major feature broken | < 1 hour |
| P2 - Minor | Minor issue, workaround exists | < 24 hours |
| P3 - Low | Cosmetic or minor | Next sprint |

### Communication Templates

**Status page update:**
```
[INVESTIGATING/IDENTIFIED/MONITORING/RESOLVED]
{Brief description of issue}
Impact: {Who is affected}
Next update: {When}
```

**Customer notification:**
```
Subject: {Product} - Service Update

We're currently experiencing {issue}.

Impact: {What customers are experiencing}
Status: {What we're doing}
ETA: {When we expect resolution}

We'll provide updates as we have them.
```

---

## SOPs Index

### Support SOPs
- [Handle support ticket](sops/support-ticket.md)
- [Process refund](sops/refund.md)
- [Escalate issue](sops/escalation.md)

### Technical SOPs
- [Deploy release](sops/deployment.md)
- [Handle outage](sops/outage.md)
- [Restore backup](sops/backup-restore.md)

### Business SOPs
- [Invoice customer](sops/invoicing.md)
- [Onboard new user](sops/user-onboarding.md)

---

## Metrics Dashboard

### Key Metrics

| Metric | Current | Target | Trend |
|--------|---------|--------|-------|
| MRR | ${X} | ${Y} | {↑/↓/→} |
| Active users | {N} | {N} | {↑/↓/→} |
| Churn rate | {%} | <{%} | {↑/↓/→} |
| Uptime | {%} | >{%} | {↑/↓/→} |
| Support response | {X}h | <{Y}h | {↑/↓/→} |

### Where to Find Metrics

| Metric | Source | Dashboard Link |
|--------|--------|----------------|
| Revenue | {source} | {link} |
| Users | {source} | {link} |
| Support | {source} | {link} |
| Technical | {source} | {link} |

---

## Appendix

### Tool Access

| Tool | Purpose | Access Method |
|------|---------|---------------|
| {tool} | {purpose} | {how to access} |

### Credential Management

Credentials stored in: {password manager/vault}
Access granted by: {who}

### Vendor Contacts

| Vendor | Contact | For |
|--------|---------|-----|
| {vendor} | {contact} | {what issues} |

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| {date} | Initial creation | {name} |
```

---

## Usage Notes

1. This is a living document - update it regularly
2. Review monthly and update any stale information
3. Share with anyone who needs operational context
4. Use this as the single source of truth for "how we run things"
