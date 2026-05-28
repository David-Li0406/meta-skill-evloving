---
id: communications-management
name: "Communications Management"
domain: PM
skill: faion-project-manager
category: "project-management"
---

# Communications Management

## Metadata
- **Category:** Project Management Framework / Stakeholder Performance Domain
- **Difficulty:** Beginner
- **Tags:** #methodology #pmbok #communication #stakeholders #project-management
- **Agent:** faion-pm-agent

---

## Problem

Stakeholders feel surprised by project status. Team members work on outdated information. Meetings consume time without producing decisions. Important updates get lost in email. Some people get too much information, others too little.

Without communications management:
- Misalignment between stakeholders
- Decisions made on wrong information
- Time wasted on ineffective meetings
- Trust erodes from lack of transparency

---

## Framework

### Step 1: Identify Communication Needs

For each stakeholder (from Stakeholder Register), determine:

| Question | Purpose |
|----------|---------|
| What do they need to know? | Content |
| How often? | Frequency |
| In what format? | Channel |
| From whom? | Source |
| What response expected? | Interaction type |

### Step 2: Create Communication Matrix

Map stakeholders to communication requirements:

| Stakeholder | Information Need | Frequency | Format | Owner |
|-------------|------------------|-----------|--------|-------|
| Sponsor | Budget, risks, milestones | Weekly | Report | PM |
| Team | Tasks, blockers, decisions | Daily | Standup | Scrum Master |
| Client | Progress, demos, feedback | Bi-weekly | Meeting | PM |
| Steering Committee | Strategic status | Monthly | Presentation | PM |

### Step 3: Define Communication Types

**Push communication:** Sent to recipient (email, reports)
- Good for: Updates, documentation, announcements
- Risk: May be ignored

**Pull communication:** Available when needed (wiki, dashboard)
- Good for: Reference info, detailed documentation
- Risk: May not be found

**Interactive communication:** Two-way exchange (meetings, calls)
- Good for: Problem-solving, decisions, complex topics
- Risk: Time-consuming, scheduling challenges

### Step 4: Establish Communication Rhythms

Create regular cadences:

| Meeting | Frequency | Duration | Purpose | Attendees |
|---------|-----------|----------|---------|-----------|
| Daily standup | Daily | 15 min | Coordination | Team |
| Sprint review | Bi-weekly | 1 hour | Demo progress | Team + Stakeholders |
| Status meeting | Weekly | 30 min | Report progress | PM + Sponsor |
| Steering committee | Monthly | 1 hour | Strategic decisions | Leadership |

### Step 5: Create Templates

Standardize recurring communications:

**Status report template:**
```markdown
# Weekly Status Report
**Project:** [Name]
**Date:** [Date]
**PM:** [Name]

## Summary
[1-2 sentences overall status]

## Progress This Week
- [Accomplishment 1]
- [Accomplishment 2]

## Planned Next Week
- [Plan 1]
- [Plan 2]

## Risks/Issues
| Item | Impact | Mitigation |
|------|--------|------------|
| [Risk] | [Impact] | [Action] |

## Metrics
- Schedule: [On track / X days behind]
- Budget: [On track / $X over]
- Scope: [X% complete]
```

### Step 6: Monitor Effectiveness

Track communication quality:
- Are stakeholders getting what they need?
- Are meetings productive?
- Is information reaching everyone?
- Are decisions being documented?

---

## Templates

### Communication Plan Template

```markdown
# Communication Plan: [Project Name]

**Version:** [X.X]
**Date:** [Date]
**Owner:** [PM Name]

## Stakeholder Communication Matrix

| Stakeholder | Role | Needs | Format | Frequency | Owner |
|-------------|------|-------|--------|-----------|-------|
| [Name/Group] | [Role] | [What info] | [How] | [When] | [Who sends] |

## Meeting Schedule

| Meeting | Purpose | Frequency | Duration | Attendees | Owner |
|---------|---------|-----------|----------|-----------|-------|
| [Name] | [Purpose] | [Freq] | [Time] | [Who] | [Facilitator] |

## Communication Channels

| Channel | Used For | Guidelines |
|---------|----------|------------|
| Email | Formal communication, decisions | Response within 24 hours |
| Slack | Quick questions, team chat | Response within 4 hours |
| Wiki | Documentation, reference | Update within 1 week of changes |
| Meetings | Decisions, problem-solving | Agenda required 24h before |

## Escalation Path

| Situation | First Contact | Escalate To | Timeframe |
|-----------|---------------|-------------|-----------|
| Technical issue | Tech Lead | PM | 24 hours |
| Budget/Scope | PM | Sponsor | 48 hours |
| Resource conflict | PM | Resource Manager | 24 hours |

## Templates
- Status report: [Link]
- Meeting notes: [Link]
- Decision log: [Link]
```

### Meeting Notes Template

```markdown
# Meeting Notes: [Meeting Name]

**Date:** [Date]
**Time:** [Time]
**Attendees:** [Names]
**Facilitator:** [Name]
**Note-taker:** [Name]

## Agenda
1. [Topic 1]
2. [Topic 2]

## Discussion

### Topic 1: [Name]
**Discussion:** [Summary of discussion]
**Decision:** [What was decided]
**Action items:**
- [ ] [Action] - [Owner] - [Due date]

### Topic 2: [Name]
[Same structure]

## Action Items Summary

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Action] | [Name] | [Date] | Open |

## Next Meeting
**Date:** [Date]
**Topics:** [Planned topics]
```

---

## Examples

### Example 1: Startup Project Communication Plan

| Stakeholder | Frequency | Format | Content |
|-------------|-----------|--------|---------|
| Founders | Weekly | 30-min call | Progress, blockers, decisions needed |
| Dev team | Daily | 15-min standup | Tasks, blockers, coordination |
| Beta users | Bi-weekly | Email newsletter | Features, feedback requests |
| Investors | Monthly | Email update | Metrics, milestones, runway |

### Example 2: Enterprise Project Communication

| Meeting | Frequency | Attendees | Output |
|---------|-----------|-----------|--------|
| Daily standup | Daily | Team (8) | Blocker identification |
| Sprint planning | Bi-weekly | Team + PO | Sprint backlog |
| Sprint review | Bi-weekly | Team + Stakeholders (15) | Demo feedback |
| Retrospective | Bi-weekly | Team | Improvement actions |
| Steering committee | Monthly | Leadership (6) | Strategic decisions |

---

## Common Mistakes

1. **Too many meetings** - Death by calendar
2. **No agenda** - Meetings wander aimlessly
3. **Missing stakeholders** - Decisions made without right people
4. **No documentation** - Decisions lost, repeated discussions
5. **One-size-fits-all** - Same communication for everyone

---

## Communication Best Practices

### Meetings
- Always have an agenda (shared beforehand)
- Start and end on time
- Document decisions and action items
- Only invite necessary people

### Written Communication
- Lead with the key point
- Keep it concise
- Use bullet points
- Include clear ask/next steps

### Status Reports
- Consistent format
- Honest about issues
- Action-oriented
- Regular cadence

---

## Communication Channels Selection

| Need | Best Channel |
|------|--------------|
| Urgent issue | Phone/call |
| Complex discussion | Meeting |
| Status update | Email/report |
| Quick question | Chat (Slack/Teams) |
| Reference information | Wiki/documentation |
| Formal decision | Email with confirmation |

---

## Next Steps

After establishing communication plan:
1. Share plan with stakeholders
2. Set up recurring meetings
3. Create templates in shared location
4. Train team on communication norms
5. Connect to Resource Management methodology

---

## References

- Project Management Framework Guide 7th Edition - Stakeholder Performance Domain
- PM industry practice standard for Communications
