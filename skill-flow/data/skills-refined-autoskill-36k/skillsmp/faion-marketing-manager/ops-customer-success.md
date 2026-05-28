---
id: customer-success
name: "Customer Success"
domain: BIZ
skill: faion-marketing-manager
category: "operations"
---

# Customer Success

## Metadata

| Field | Value |
|-------|-------|
| **ID** | customer-success |
| **Name** | Customer Success |
| **Category** | Operations & Business |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | customer-support, churn-prevention, upselling-cross-selling |

---

## Problem

Your customers bought your product, but are they successful? If they're not getting value, they'll churn. Support is reactive - fixing problems after they happen. Customer success is proactive - helping customers succeed before problems arise.

Customer success means ensuring customers achieve their goals with your product.

---

## Framework

Customer success follows this approach:

```
DEFINE    -> What does success look like?
MEASURE   -> Track customer health
ENGAGE    -> Proactive touchpoints
ENABLE    -> Provide resources for success
EXPAND    -> Grow successful customers
```

### Step 1: Define Customer Success

**Success metrics by product type:**

| Product Type | Success = | Metric |
|--------------|-----------|--------|
| SaaS tool | Using core features | Feature adoption |
| Course | Completing content | Completion rate |
| Service | Achieving outcome | Results delivered |
| Membership | Engaging regularly | Engagement score |

**Customer success definition:**

```markdown
Our customers are successful when they:
1. [Primary outcome]
2. [Secondary outcome]
3. [Leading indicator]

Measured by:
- [Metric 1]: Target [X]
- [Metric 2]: Target [X]
```

**Example:**
```markdown
Project management SaaS:
Success = Teams actively using tool for project tracking

Measured by:
- Active projects: 3+ per team
- Daily active users: 50%+ of seats
- Tasks completed: 10+ per user/week
```

### Step 2: Build Health Scoring

**Health score components:**

| Component | Weight | Data Source |
|-----------|--------|-------------|
| Product usage | 30% | Analytics |
| Feature adoption | 25% | Analytics |
| Support sentiment | 20% | Support tickets |
| Engagement | 15% | Email, activity |
| Payment health | 10% | Billing |

**Scoring example:**

```
Usage Score (0-30):
- Daily active: 30
- Weekly active: 20
- Monthly active: 10
- Inactive: 0

Feature Score (0-25):
- Using all core features: 25
- Using most: 20
- Using some: 10
- Using few: 5

Support Score (0-20):
- Positive interactions: 20
- Neutral: 15
- Negative: 5
- Escalated: 0

Health Score = Usage + Feature + Support + Engagement + Payment
```

**Health categories:**

| Score | Status | Action |
|-------|--------|--------|
| 80-100 | Healthy | Maintain, upsell |
| 60-79 | Stable | Monitor, engage |
| 40-59 | At-risk | Intervene |
| 0-39 | Critical | Urgent outreach |

### Step 3: Create Success Touchpoints

**Proactive engagement:**

| Timing | Touchpoint | Purpose |
|--------|------------|---------|
| Day 1 | Welcome | Set expectations |
| Day 3 | Check-in | Early issues |
| Day 7 | Progress | First value |
| Day 14 | Feature | Deeper engagement |
| Day 30 | Review | Success check |
| Monthly | Newsletter | Value, updates |
| Quarterly | Review | Strategic alignment |

**Automated touchpoints:**

```
Trigger: New customer
→ Day 1: Welcome email + resources
→ Day 3: "Need help?" check-in
→ Day 7: Feature tip
→ Day 14: Usage review

Trigger: Low usage (no login 7 days)
→ Immediate: Re-engagement email
→ Day 3: Personal outreach
→ Day 7: Escalate
```

**High-touch vs. low-touch:**

| Customer Type | Approach | Touchpoints |
|---------------|----------|-------------|
| Enterprise | High-touch | Dedicated success manager |
| Mid-market | Medium | Periodic calls + automation |
| SMB | Low-touch | Mostly automated |
| Self-serve | Tech-touch | Fully automated |

### Step 4: Enable Success

**Success resources:**

| Resource | Purpose | Format |
|----------|---------|--------|
| Onboarding guide | Get started quickly | Doc, video |
| Best practices | Optimal usage | Blog, guide |
| Templates | Quick wins | Download |
| Webinars | Deep learning | Live, recorded |
| Community | Peer support | Forum, Slack |
| Office hours | Live help | Scheduled calls |

**Self-service enablement:**

```
Knowledge base:
├── Getting started
├── Core features
├── Advanced features
├── Integrations
├── Best practices
└── Troubleshooting

Video library:
├── Quick start (5 min)
├── Feature tutorials
└── Use case walkthroughs
```

### Step 5: Drive Expansion

**Expansion triggers:**

| Signal | Opportunity | Action |
|--------|-------------|--------|
| Hitting limits | Upgrade | Proactive offer |
| Adding team members | Seats | Invite prompt |
| Using advanced features | Premium tier | Feature showcase |
| Requesting features | Upsell | Show existing solution |
| Success milestone | Cross-sell | Related product |

**Success → Expansion path:**

```
Customer achieves first success
    ↓
Recognize and celebrate
    ↓
Identify next goal
    ↓
Show how upgrade helps
    ↓
Natural expansion conversation
```

---

## Templates

### Customer Health Dashboard

```markdown
## Customer Health: [Month]

### Overview
| Status | Customers | % | MRR |
|--------|-----------|---|-----|
| Healthy (80+) | X | X% | $X |
| Stable (60-79) | X | X% | $X |
| At-risk (40-59) | X | X% | $X |
| Critical (<40) | X | X% | $X |

### At-Risk Accounts
| Customer | Health | MRR | Issue | Action |
|----------|--------|-----|-------|--------|
| [Name] | 45 | $X | Low usage | Outreach |
| [Name] | 38 | $X | Support issue | Escalate |

### Critical Accounts
| Customer | Health | MRR | Days Critical | Owner |
|----------|--------|-----|---------------|-------|
| [Name] | 25 | $X | 14 | [Name] |

### Expansion Ready
| Customer | Health | Current | Opportunity |
|----------|--------|---------|-------------|
| [Name] | 95 | Pro | Enterprise |
| [Name] | 88 | Basic | Pro |
```

### Customer Success Playbook

```markdown
## Customer Success Playbook

### Onboarding (Day 1-30)
| Day | Action | Trigger | Owner |
|-----|--------|---------|-------|
| 1 | Welcome email | Signup | Auto |
| 3 | Check-in | No key action | Auto |
| 7 | Progress review | Time | CSM |
| 14 | Feature introduction | Time | Auto |
| 30 | Success review | Time | CSM |

### Ongoing Engagement
| Trigger | Action | Owner |
|---------|--------|-------|
| Health drop | Outreach | CSM |
| New feature | Announcement | Auto |
| Usage milestone | Celebration | Auto |
| Renewal 30d | Pre-renewal check | CSM |

### At-Risk Intervention
| Signal | Action | Timeline |
|--------|--------|----------|
| No login 7d | Email | Auto |
| No login 14d | Personal email | CSM |
| Support escalation | Call | CSM |
| Health <50 | Review meeting | CSM |
```

### Customer Success Review

```markdown
## Customer Review: [Customer Name]

### Profile
- Plan: [Plan]
- MRR: $[X]
- Customer since: [Date]
- Primary contact: [Name]

### Health Metrics
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Usage | X | X | On track |
| Adoption | X% | X% | Behind |
| Sentiment | X | X | At risk |
| **Overall** | X | X | [Status] |

### Recent Activity
- [Activity 1]
- [Activity 2]
- [Activity 3]

### Success Milestones
- [x] Completed onboarding
- [x] First success metric
- [ ] Full team adoption
- [ ] Advanced feature use

### Next Steps
- [ ] Schedule review call
- [ ] Share best practices guide
- [ ] Introduce [feature]

### Expansion Opportunity
[Assessment of upgrade potential]
```

---

## Examples

### Example 1: SaaS Customer Success

**Product:** Team collaboration tool

**Success definition:**
- Team uses daily
- 3+ active projects
- 80%+ adoption

**Health scoring:**
- Usage: Daily logins / team size
- Adoption: Features used / available
- Engagement: Support interactions
- Growth: Seat expansion

**Playbook:**
```
Day 1: Admin onboarding call
Day 7: Team training webinar
Day 14: Check-in email
Day 30: Success review call
Monthly: Usage report
Quarterly: Business review
```

### Example 2: Info Product Customer Success

**Product:** Online course

**Success definition:**
- Complete 80% of content
- Implement learnings
- Achieve stated goal

**Health scoring:**
- Progress: Lessons completed
- Engagement: Community participation
- Assignments: Submitted work

**Playbook:**
```
Day 1: Welcome + roadmap
Day 3: First module reminder
Weekly: Progress email
Module completion: Congrats + next steps
Completion: Survey + testimonial request
```

---

## Implementation Checklist

### Setup
- [ ] Define success metrics
- [ ] Build health scoring
- [ ] Set up tracking
- [ ] Create customer segments

### Content
- [ ] Create onboarding materials
- [ ] Build knowledge base
- [ ] Develop email sequences
- [ ] Design health dashboard

### Process
- [ ] Define touchpoint cadence
- [ ] Create playbooks
- [ ] Set up alerts
- [ ] Train team (if applicable)

### Optimization
- [ ] Monitor health scores
- [ ] Track leading indicators
- [ ] Iterate on playbooks
- [ ] Review monthly

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| No definition | Don't know if winning | Define success metrics |
| Reactive only | Too late to save | Proactive engagement |
| One-size-fits-all | Different needs | Segment customers |
| Over-communication | Annoying | Right message, right time |
| No health tracking | Blind to issues | Build health scoring |
| Ignoring small customers | Miss signals | Automate touchpoints |

---

## Customer Success Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| NPS | Promoters - Detractors | > 50 |
| CSAT | Satisfied / Total | > 4.5/5 |
| Time to value | Days to first success | < 7 days |
| Adoption rate | Users active / Total | > 80% |
| Expansion rate | Customers expanded / Total | > 20% |
| Net retention | MRR after churn + expansion | > 100% |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Health scoring | Vitally, Totango, Custom |
| Email | Customer.io, Intercom |
| Analytics | Mixpanel, Amplitude |
| Surveys | Typeform, Delighted |
| Community | Circle, Discord |
| Knowledge base | Notion, GitBook |

---

## Related Methodologies

- **customer-support:** Customer Support (reactive support)
- **churn-prevention:** Churn Prevention (at-risk intervention)
- **upselling-cross-selling:** Upselling & Cross-selling (expansion)
- **onboarding-emails:** Onboarding Emails (automated touchpoints)

---

*Methodology: customer-success | Operations & Business | faion-growth-agent*
