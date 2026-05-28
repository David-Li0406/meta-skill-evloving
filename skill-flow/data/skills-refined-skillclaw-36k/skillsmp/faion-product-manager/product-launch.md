---
id: product-launch
name: "Product Launch"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Product Launch

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #launch, #marketing |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-mlp-impl-planner-agent |

---

## Problem

Launches are either underwhelming or chaotic. Issues:
- "Just put it out there" approach
- Last-minute scrambling
- No launch coordination
- Missed momentum opportunity

**The root cause:** No structured launch playbook.

---

## Framework

### What is a Product Launch?

A product launch is the coordinated introduction of a product to its target market. It's not just deployment - it's a strategic moment to generate awareness and adoption.

### Launch Types

| Type | Scope | Effort | Risk |
|------|-------|--------|------|
| Soft launch | Limited audience | Low | Low |
| Beta launch | Early adopters | Medium | Medium |
| Full launch | Public | High | High |
| Major release | Existing users | Medium | Low |

### Launch Planning Timeline

```
T-8 weeks: Define strategy
T-6 weeks: Create assets
T-4 weeks: Build audience
T-2 weeks: Prep coordination
T-1 week: Final checks
T-Day: Execute
T+1 week: Monitor and respond
T+2 weeks: Retrospective
```

### Launch Components

#### 1. Positioning & Messaging

- Value proposition
- Key messages
- Competitive differentiation
- Target audience

#### 2. Assets

| Asset | Purpose | Owner |
|-------|---------|-------|
| Landing page | Convert visitors | Marketing |
| Demo/video | Show product | Product |
| Press kit | Media coverage | PR |
| Email templates | Outreach | Marketing |
| Social content | Awareness | Marketing |
| Documentation | Onboarding | Product |

#### 3. Channels

| Channel | Use For |
|---------|---------|
| Email list | Warm audience |
| Social media | Awareness |
| Product Hunt | Tech audience |
| Press/PR | Credibility |
| Influencers | Reach |
| Paid ads | Scale |
| Communities | Targeted groups |

#### 4. Coordination

- Internal: Team alignment, support prep
- External: Partners, press, influencers

### Launch Process

#### Step 1: Define Launch Strategy

**Answer:**
- What are we launching?
- Who is it for?
- What's the goal? (awareness, signups, revenue)
- What's the budget/timeline?
- What type of launch?

#### Step 2: Build Launch Plan

**Components:**
- Timeline with milestones
- Asset checklist
- Channel strategy
- Team responsibilities
- Success metrics

#### Step 3: Create Assets

**Minimum viable launch:**
- Landing page
- Demo or screenshots
- Announcement email
- Social posts
- Basic documentation

#### Step 4: Build Pre-Launch Audience

**Tactics:**
- Waitlist signup
- Email list building
- Social following
- Community engagement
- Content marketing

#### Step 5: Coordinate Launch Day

**Launch day checklist:**
- [ ] Deploy product
- [ ] Verify everything works
- [ ] Update landing page
- [ ] Send email announcement
- [ ] Post on social media
- [ ] Submit to directories
- [ ] Notify press/influencers
- [ ] Monitor and respond

#### Step 6: Post-Launch

- Monitor metrics
- Respond to feedback
- Fix urgent issues
- Capture testimonials
- Retrospective

---

## Templates

### Launch Plan

```markdown
## Launch Plan: [Product]

### Launch Overview
- **Product:** [Name]
- **Launch type:** [Soft/Beta/Full]
- **Target date:** [Date]
- **Goal:** [Metric target]

### Target Audience
**Primary:** [Who]
**Messaging:** [Key message]

### Timeline

| Week | Date | Activities |
|------|------|------------|
| T-8 | [Date] | Strategy finalized |
| T-6 | [Date] | Asset creation begins |
| T-4 | [Date] | Audience building |
| T-2 | [Date] | All assets ready |
| T-1 | [Date] | Final prep |
| T-Day | [Date] | Launch |
| T+1 | [Date] | Monitor & respond |

### Asset Checklist

| Asset | Owner | Status | Due |
|-------|-------|--------|-----|
| Landing page | [Name] | [ ] | [Date] |
| Announcement email | [Name] | [ ] | [Date] |
| Demo video | [Name] | [ ] | [Date] |
| Social posts (5) | [Name] | [ ] | [Date] |
| Press kit | [Name] | [ ] | [Date] |
| Documentation | [Name] | [ ] | [Date] |

### Channel Strategy

| Channel | Timing | Content | Owner |
|---------|--------|---------|-------|
| Email list | T-day 9am | Announcement | [Name] |
| Twitter | T-day 10am | Thread | [Name] |
| Product Hunt | T-day 12am PT | Full listing | [Name] |
| LinkedIn | T-day 10am | Article | [Name] |

### Partnerships

| Partner | Commitment | Status |
|---------|------------|--------|
| [Partner] | [What they'll do] | [Confirmed/Pending] |

### Success Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Signups day 1 | [X] | |
| Week 1 signups | [X] | |
| Product Hunt rank | Top 5 | |
| Media mentions | [X] | |

### Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Server overload | Scale infrastructure |
| Critical bugs | Hold rollback ready |
| No press pickup | Focus on community |

### Team
- **Launch lead:** [Name]
- **Product:** [Name]
- **Marketing:** [Name]
- **Engineering:** [Name]
```

### Launch Day Checklist

```markdown
## Launch Day: [Product] - [Date]

### Pre-Launch (Morning)
- [ ] Final staging test
- [ ] Team standup
- [ ] Deploy to production
- [ ] Verify core flows
- [ ] Monitoring dashboards ready

### Launch (Go-Live)
- [ ] Flip feature flags
- [ ] Update landing page
- [ ] Verify public access
- [ ] Screenshot/record for posterity

### Announcement (Coordinated)
- [ ] [Time]: Email blast sent
- [ ] [Time]: Twitter announcement
- [ ] [Time]: LinkedIn post
- [ ] [Time]: Product Hunt live
- [ ] [Time]: Notify partners

### Monitor (Ongoing)
- [ ] Server health
- [ ] Error rates
- [ ] Signup flow
- [ ] Support queue

### Respond (Throughout)
- [ ] Reply to social mentions
- [ ] Answer Product Hunt comments
- [ ] Address support tickets
- [ ] Share updates with team

### End of Day
- [ ] Metrics snapshot
- [ ] Team debrief
- [ ] Document issues
- [ ] Thank everyone

### Contact Info
- On-call engineer: [Name] [Phone]
- Marketing lead: [Name] [Phone]
- Emergency escalation: [Name]
```

---

## Examples

### Example 1: Product Hunt Launch

**Product:** AI Writing Tool
**Goal:** #1 Product of the Day

**Timeline:**
- T-4 weeks: Build hunter relationships
- T-2 weeks: Assets ready, get testimonials
- T-1 week: Prep supporters, schedule everything
- T-Day: 12:01 AM PT launch, all hands on deck
- T+1: Respond to every comment

**Results:** #3 Product of Day, 1,200 signups

### Example 2: Beta Launch

**Product:** Analytics Dashboard
**Goal:** 100 beta users

**Timeline:**
- Soft launch to existing customers first
- Gather feedback for 2 weeks
- Fix critical issues
- Open to waitlist (500 people)
- Accept first 100

**Results:** 100 beta users, 40% active, valuable feedback

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No launch plan | Start planning 6-8 weeks out |
| Launch on Friday | Tuesday-Wednesday best |
| All channels same message | Tailor to each |
| No pre-launch audience | Build waitlist early |
| Ignoring feedback | Respond to everything |
| No monitoring | Watch metrics launch day |
| No retrospective | Always learn from launches |

---

## Related Methodologies

- **release-planning:** Release Planning
- **gtm-strategy:** GTM Strategy
- **landing-page-design:** Landing Page Design
- **social-media-strategy:** Social Media Strategy
- **aarrr-pirate-metrics:** AARRR Pirate Metrics

---

## Agent

**faion-mlp-impl-planner-agent** helps with launches. Invoke with:
- "Create a launch plan for [product]"
- "What should my launch timeline be?"
- "Generate launch checklist for [date]"
- "Review my launch plan: [content]"

---

*Methodology | Product | Version 1.0*
