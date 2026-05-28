---
name: Customer Success Manager
slug: customer-success
description: Manage customer relationships, track health scores, prevent churn, and drive expansion
category: business
complexity: complex
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "customer success"
  - "customer health"
  - "churn prevention"
  - "customer retention"
  - "account management"
  - "expansion revenue"
tags:
  - customer-success
  - retention
  - churn
  - expansion
  - business-operations
---

# Customer Success Manager

Expert customer success management system that helps you monitor customer health, prevent churn, drive product adoption, and identify expansion opportunities. This skill provides structured workflows for proactive account management, health scoring, and retention strategies based on proven CS methodologies.

Customer success is the bridge between acquisition and revenue growth. This skill helps you operationalize CS practices that reduce churn, increase lifetime value, and turn customers into advocates. Whether you're managing a SaaS customer base or enterprise accounts, this provides the framework to scale success.

Built on best practices from leading CS organizations, this skill combines data-driven health monitoring, proactive engagement strategies, and expansion playbooks to maximize customer lifetime value.

## Core Workflows

### Workflow 1: Customer Health Scoring
**Establish and monitor multi-dimensional health metrics**

1. **Health Score Framework**
   - **Product Adoption Metrics**: Login frequency, feature usage, DAU/MAU ratio, depth of usage
   - **Engagement Metrics**: Support ticket volume, NPS/CSAT scores, QBR participation, response times
   - **Business Metrics**: Usage vs. license count, growth trajectory, payment history
   - **Relationship Metrics**: Executive alignment, champion presence, meeting cadence

2. **Scoring Methodology**
   - Assign weights to each dimension based on correlation with retention
   - Define green/yellow/red thresholds (e.g., 80+ = green, 60-79 = yellow, <60 = red)
   - Automate data collection where possible
   - Calculate weekly health scores for all accounts

3. **Health Alerts & Triggers**
   - Set up alerts for score degradation (e.g., drop of 10+ points)
   - Flag accounts transitioning from green to yellow
   - Identify leading indicators of churn (usage drops, support spikes)
   - Create escalation paths for red accounts

### Workflow 2: Proactive Account Management
**Structured engagement to drive adoption and prevent churn**

1. **Onboarding & Activation**
   - Define "activated" state (key usage milestones achieved)
   - Create 30/60/90-day onboarding plans
   - Track time-to-value metrics
   - Identify and address stalled onboardings early

2. **Regular Customer Cadence**
   - **Weekly**: Review health scores, triage alerts
   - **Monthly**: Check-in calls with yellow/red accounts
   - **Quarterly**: Business reviews (QBRs) with strategic accounts
   - **Annual**: Executive business reviews, renewal planning

3. **Proactive Outreach Triggers**
   - Usage drops below threshold → Check-in call
   - New feature released relevant to customer → Demo offer
   - Support ticket spike → CSM intervention
   - Champion leaves company → Rebuild relationships
   - Approaching renewal (90 days out) → Renewal conversation

### Workflow 3: Churn Prevention & Mitigation
**Identify at-risk customers and execute save plays**

1. **Churn Risk Identification**
   - Monitor early warning signals:
     - Declining product usage
     - Increased support tickets with negative sentiment
     - Poor NPS/CSAT scores
     - Executive turnover or champion departure
     - Budget cuts or company layoffs
     - Competitive activity

2. **Intervention Playbooks**
   - **Technical Issues**: Escalate to support/engineering, provide workarounds
   - **Low Adoption**: Schedule training, share best practices, assign resources
   - **Value Perception**: ROI analysis, case studies, executive alignment
   - **Pricing Concerns**: Discuss tier adjustments, payment plans
   - **Competitive Threat**: Feature comparison, roadmap preview, relationship leverage

3. **Save Process**
   - Qualify the risk level (low/medium/high)
   - Assign CSM + executive sponsor to high-risk accounts
   - Create account rescue plan with clear actions and timeline
   - Execute interventions with urgency
   - Document outcomes (saved, lost, lessons learned)

### Workflow 4: Expansion & Growth
**Identify and capture expansion revenue opportunities**

1. **Expansion Signal Detection**
   - **Usage-Based Signals**: Approaching tier limits, high feature utilization, power users
   - **Business Signals**: Company growth, new teams/departments, budget expansion
   - **Relationship Signals**: High NPS scores, executive advocates, referrals
   - **Product Signals**: Asking about advanced features, integration requests

2. **Expansion Playbooks**
   - **Upsell**: Move to higher-tier plan with more features/capacity
   - **Cross-sell**: Introduce complementary products/modules
   - **User Expansion**: Add more seats/licenses to existing account
   - **Professional Services**: Training, implementation, customization

3. **Expansion Process**
   - Qualify expansion readiness (health score green, strong adoption)
   - Build business case with ROI and success metrics
   - Align with customer stakeholders and decision-makers
   - Hand off to sales for contract negotiation if needed
   - Track expansion revenue and conversion rates

### Workflow 5: Customer Advocacy & Voice
**Turn happy customers into advocates and capture feedback**

1. **Advocacy Programs**
   - Identify promoters (NPS 9-10, high health scores)
   - Request case studies, testimonials, reviews
   - Invite to reference calls with prospects
   - Feature in webinars, events, user conferences
   - Reward with beta access, swag, recognition

2. **Feedback Collection**
   - **Surveys**: NPS quarterly, CSAT after interactions
   - **Interviews**: Deep-dive sessions with power users
   - **Advisory Boards**: Strategic customers shaping roadmap
   - **Usage Analytics**: Behavioral data showing pain points

3. **Feedback Loop Closure**
   - Aggregate and categorize feedback themes
   - Share with product, engineering, sales teams
   - Communicate roadmap updates back to customers
   - Close the loop on feature requests

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Check account health | "Show health score for [Customer]" |
| List at-risk accounts | "Show red/yellow accounts" |
| Schedule QBR | "Plan QBR for [Customer]" |
| Churn prevention | "Create save plan for [Customer]" |
| Expansion opportunity | "Identify expansion candidates" |
| Onboarding check | "Review onboarding pipeline" |
| NPS summary | "Show NPS by segment" |
| Usage trends | "Analyze usage for [Customer]" |
| Renewal forecast | "Show renewals next 90 days" |
| Advocacy candidates | "Find customers for case study" |

## Best Practices

### Health Scoring
- Update scores weekly at minimum (daily for high-touch accounts)
- Use both lagging indicators (NPS) and leading indicators (usage)
- Calibrate scoring weights quarterly based on churn correlation
- Make health scores visible to entire customer-facing team
- Don't rely on a single metric—use composite scores

### Segmentation & Coverage
- Segment customers by revenue, potential, complexity
- High-touch: 1 CSM per 10-20 strategic accounts
- Mid-touch: 1 CSM per 50-100 accounts with scaled programs
- Low-touch: Automated playbooks, self-service resources
- Assign coverage based on ARR and strategic value

### Proactive vs. Reactive
- Aim for 80% proactive outreach, 20% reactive firefighting
- Build structured cadences, not ad-hoc check-ins
- Use automation for routine touchpoints
- Reserve CSM time for strategic conversations
- Triage alerts quickly to prevent escalation

### Cross-Functional Collaboration
- **Product**: Share feedback, influence roadmap, beta access
- **Sales**: Warm handoffs, expansion leads, renewals support
- **Support**: Escalations, ticket trends, customer sentiment
- **Marketing**: Case studies, webinars, events, content
- **Finance**: Renewal forecasting, payment issues

### Data & Metrics
- Instrument product for usage tracking
- Integrate CRM, support, billing systems
- Build real-time dashboards for health and activity
- Track leading and lagging churn indicators
- Measure CS impact: GRR, NRR, expansion rate, time-to-value

### Communication
- Document all customer interactions in CRM
- Share account plans with stakeholders
- Escalate risks early and transparently
- Celebrate wins (renewals, expansions, advocacy)
- Run regular CS team sync meetings

## Key Metrics to Track

**Retention Metrics:**
- Gross Revenue Retention (GRR) - Target: 90%+
- Net Revenue Retention (NRR) - Target: 110%+ for SaaS
- Logo churn rate (monthly/annual)
- MRR/ARR churn rate
- Customer lifetime value (LTV)

**Engagement Metrics:**
- Health score distribution (% green/yellow/red)
- Product adoption rate
- DAU/MAU ratio
- Feature adoption depth
- NPS/CSAT scores

**Efficiency Metrics:**
- CSM capacity (accounts per CSM)
- Time-to-value (onboarding to activation)
- QBR completion rate
- Response time to alerts
- Save rate (% of at-risk accounts saved)

**Growth Metrics:**
- Expansion revenue (upsell/cross-sell)
- Expansion rate (% of customers expanding)
- Referrals generated
- Case studies/testimonials collected
- Customer advocacy program participation

## Red Flags to Watch

- **Immediate Risk**: Billing failures, contract not signed at renewal, executive sponsor leaves
- **High Risk**: 30%+ usage decline, NPS detractor, multiple escalated support tickets
- **Medium Risk**: Declining login frequency, missed QBRs, low feature adoption
- **Early Warning**: Stalled onboarding, slow response times, lukewarm engagement

## Expansion Readiness Criteria

Before pursuing expansion, ensure:
- Health score is green (80+)
- Strong product adoption (above segment average)
- Positive NPS (8+)
- Executive relationship in place
- Clear use case for expanded offering
- Budget authority identified
