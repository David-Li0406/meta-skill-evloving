---
id: stakeholder-management
name: "Stakeholder Management"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Stakeholder Management

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #stakeholders, #communication |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-pm-agent |

---

## Problem

Products fail due to stakeholder misalignment, not technology. Common issues:
- Conflicting requirements from different stakeholders
- Last-minute changes from executives
- Silent stakeholders who block later
- Unclear decision-making authority

**The root cause:** No systematic approach to identifying, engaging, and managing stakeholders.

---

## Framework

### What is Stakeholder Management?

Stakeholder management is identifying everyone affected by your product, understanding their needs, and keeping them appropriately engaged. It answers: "Who matters and how do we work with them?"

### Stakeholder Identification

#### 1. Who Are Stakeholders?

| Type | Examples | Needs |
|------|----------|-------|
| End Users | Customers, employees | Value from product |
| Decision Makers | Executives, sponsors | Business outcomes |
| Influencers | Advisors, thought leaders | Credibility, early access |
| Builders | Developers, designers | Clear requirements |
| Support | Customer success, sales | Product knowledge |
| External | Partners, regulators | Compliance, compatibility |

#### 2. Stakeholder Mapping

**Power/Interest Grid:**

```
          INTEREST
          High      Low
     High │ Manage   │ Keep
POWER     │ Closely  │ Satisfied
     Low  │ Keep     │ Monitor
          │ Informed │
```

**Categories:**
- **High Power, High Interest:** Engage deeply, regular updates
- **High Power, Low Interest:** Keep satisfied, periodic updates
- **Low Power, High Interest:** Keep informed, involve in feedback
- **Low Power, Low Interest:** Monitor, minimal effort

### Stakeholder Engagement

#### Level of Engagement

| Level | Description | Tactics |
|-------|-------------|---------|
| Partner | Active collaboration | Co-creation, regular meetings |
| Involved | Regular input | Reviews, feedback sessions |
| Informed | One-way updates | Newsletters, demos |
| Monitor | Minimal contact | Periodic check-ins |

### Stakeholder Management Process

#### Step 1: Identify All Stakeholders

**Brainstorm:**
- Who uses this?
- Who pays for this?
- Who approves this?
- Who builds this?
- Who supports this?
- Who could block this?

#### Step 2: Analyze Each Stakeholder

**For each:**
- What do they want?
- What do they fear?
- How much power do they have?
- How interested are they?
- What's their attitude (supporter/neutral/resistor)?

#### Step 3: Plan Engagement

**Based on analysis:**
- How often to communicate
- What format (meeting, email, doc)
- What information they need
- Who manages the relationship

#### Step 4: Execute and Adapt

- Regular touchpoints
- Track satisfaction
- Adjust as dynamics change
- Handle conflicts proactively

---

## Templates

### Stakeholder Register

```markdown
## Stakeholder Register: [Project/Product]

| Name | Role | Interest | Power | Attitude | Engagement | Owner |
|------|------|----------|-------|----------|------------|-------|
| [Name] | [Title] | High | High | Supporter | Partner | [PM] |
| [Name] | [Title] | Medium | High | Neutral | Informed | [PM] |
| [Name] | [Title] | High | Low | Resistor | Involved | [Lead] |

### Detailed Profiles

#### [Stakeholder 1]
**Role:** [Title/Function]
**Interest in project:** [What they care about]
**Potential concerns:** [What might worry them]
**Influence:** [How they can affect project]
**Communication preference:** [How/when to reach them]
**Key messages:** [What to emphasize]
**Action items:** [Specific engagement tasks]

---

#### [Stakeholder 2]
...
```

### Stakeholder Communication Plan

```markdown
## Communication Plan: [Project]

### Communication Matrix

| Stakeholder | What | When | How | Owner |
|-------------|------|------|-----|-------|
| Executive sponsor | Status, decisions | Weekly | 1:1 meeting | PM |
| Dev team | Requirements, changes | Daily | Stand-up | PM |
| Sales team | Features, timeline | Bi-weekly | Email update | PM |
| Customers | Releases, feedback | Monthly | Newsletter | Marketing |

### Key Messages by Audience

#### For Executives
- Focus: Business impact, timelines, risks
- Avoid: Technical details
- Format: Executive summary

#### For Technical Team
- Focus: Requirements, decisions, blockers
- Avoid: Business politics
- Format: Detailed specs

#### For Customers
- Focus: Benefits, how-to, support
- Avoid: Internal process
- Format: User-friendly guides

### Escalation Path
1. Issue raised to [PM]
2. If unresolved in 24h → [Director]
3. If unresolved in 48h → [Executive sponsor]
```

### Stakeholder Meeting Template

```markdown
## Stakeholder Update: [Date]

### Attendees
- [Name] - [Role]

### Agenda
1. Progress update (10 min)
2. Decisions needed (15 min)
3. Risks and concerns (10 min)
4. Q&A (10 min)

### Progress Update
- **Completed:** [What's done]
- **In progress:** [What's happening]
- **Upcoming:** [What's next]

### Decisions Needed
| Decision | Options | Recommendation | Deadline |
|----------|---------|----------------|----------|
| [Decision] | A, B, C | B | [Date] |

### Risks
| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| [Risk] | High | Medium | [Action] |

### Action Items
- [ ] [Action] - [Owner] - [Due date]

### Next Meeting
[Date and time]
```

---

## Examples

### Example 1: SaaS Feature Launch Stakeholders

**Stakeholders identified:**
| Stakeholder | Power | Interest | Strategy |
|-------------|-------|----------|----------|
| CEO | High | Medium | Keep satisfied, quarterly updates |
| Head of Sales | High | High | Partner, weekly sync |
| Engineering Lead | Medium | High | Involved, daily standups |
| Key Customer | Low | High | Informed, beta access |
| Support Team | Low | High | Involved, training sessions |

**Engagement plan:**
- Weekly: Sales + Engineering sync
- Bi-weekly: Demo to support team
- Monthly: Customer advisory board
- Quarterly: CEO update

### Example 2: Solo Product Stakeholders

Even solopreneurs have stakeholders:

| Stakeholder | What They Need | How to Engage |
|-------------|----------------|---------------|
| Early customers | Working product, support | Discord, email |
| Payment processor | Compliance | Documentation |
| Hosting provider | Technical requirements | Support tickets |
| Advisor/mentor | Progress updates | Monthly call |
| Family | Time boundaries | Clear schedule |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Ignoring silent stakeholders | Proactively seek their input |
| Same message to everyone | Tailor by audience |
| Infrequent communication | Regular, predictable updates |
| Only positive updates | Share challenges early |
| No escalation path | Define how to resolve conflicts |
| Assuming alignment | Explicitly verify understanding |

---

## Related Methodologies

- **stakeholder-engagement:** Stakeholder Engagement
- **raci-matrix:** RACI Matrix
- **roadmap-design:** Roadmap Design
- **business-analysis-planning:** Business Analysis Planning
- **gtm-strategy:** GTM Strategy

---

## Agent

**faion-pm-agent** helps with stakeholder management. Invoke with:
- "Identify stakeholders for [project]"
- "Create a communication plan for [stakeholders]"
- "How should I handle [difficult stakeholder]?"
- "Review my stakeholder analysis: [content]"

---

*Methodology | Product | Version 1.0*
