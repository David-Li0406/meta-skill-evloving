---
id: metrics-dashboards
name: "Metrics & Dashboards"
domain: BIZ
skill: faion-marketing-manager
category: "operations"
---

# Metrics & Dashboards

## Metadata

| Field | Value |
|-------|-------|
| **ID** | metrics-dashboards |
| **Name** | Metrics & Dashboards |
| **Category** | Operations & Business |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | financial-planning, analytics-setup, annual-planning |

---

## Problem

You're running your business on gut feeling. You don't know your key numbers. When asked "How's business?" you can't give a real answer. Without metrics, you can't improve what you can't measure.

Metrics and dashboards mean knowing your numbers so you can make better decisions.

---

## Framework

Metrics management follows this approach:

```
IDENTIFY  -> Choose the right metrics
TRACK     -> Collect data systematically
VISUALIZE -> Create useful dashboards
ANALYZE   -> Extract insights
ACT       -> Make data-driven decisions
```

### Step 1: Choose Your Metrics

**Metric categories:**

| Category | Purpose | Examples |
|----------|---------|----------|
| **North Star** | Ultimate success measure | Active users, Revenue |
| **Leading** | Predict future outcomes | Signups, Trial starts |
| **Lagging** | Measure past results | Revenue, Churn |
| **Input** | Actions you control | Emails sent, Ads spend |
| **Output** | Results you want | Conversions, Revenue |

**Solopreneur essential metrics:**

| Metric | What It Measures | Frequency |
|--------|------------------|-----------|
| Revenue | Money in | Daily |
| MRR/ARR | Recurring revenue | Weekly |
| Customers | Active paying | Weekly |
| Churn rate | Customers lost | Monthly |
| CAC | Cost to acquire | Monthly |
| LTV | Customer value | Monthly |
| Profit margin | Money kept | Monthly |
| Runway | Time left | Monthly |

**Don't track everything.** Focus on 5-10 metrics that matter.

### Step 2: Implement Tracking

**Data sources:**

| Data Type | Sources |
|-----------|---------|
| Revenue | Stripe, PayPal, accounting |
| Customers | CRM, payment processor |
| Usage | Product analytics |
| Marketing | GA4, ad platforms |
| Support | Help desk, email |

**Tracking setup:**

| Layer | Tool | Purpose |
|-------|------|---------|
| Collection | Segment, GTM | Event capture |
| Storage | Database, spreadsheet | Data warehouse |
| Analysis | Analytics tools | Process data |
| Visualization | Dashboard tools | Display metrics |

**Simple stack for solopreneurs:**
```
Stripe → Google Sheets → Looker Studio
GA4 → Native dashboards
Product → Mixpanel/Amplitude free tier
```

### Step 3: Build Your Dashboard

**Dashboard design principles:**

| Principle | Implementation |
|-----------|----------------|
| Glanceable | See status in 5 seconds |
| Focused | 5-10 key metrics max |
| Current | Real-time or daily updates |
| Actionable | Numbers you can influence |
| Comparative | Show trends, not just values |

**Dashboard layout:**

```
┌─────────────────────────────────────────┐
│  NORTH STAR METRIC                      │
│  ████████████████████████ $50K MRR      │
└─────────────────────────────────────────┘

┌───────────────┬───────────────┬─────────┐
│  Revenue      │  Customers    │  Churn  │
│  $52,000      │  125          │  3.2%   │
│  ↑ 8%         │  ↑ 12         │  ↓ 0.5% │
└───────────────┴───────────────┴─────────┘

┌───────────────┬───────────────┬─────────┐
│  CAC          │  LTV          │  Ratio  │
│  $150         │  $1,200       │  8:1    │
└───────────────┴───────────────┴─────────┘

┌─────────────────────────────────────────┐
│  Revenue Trend (12 months)              │
│  [Line chart showing growth]            │
└─────────────────────────────────────────┘
```

**Dashboard types:**

| Type | Purpose | Update |
|------|---------|--------|
| Daily pulse | Quick health check | Daily |
| Weekly review | Deeper analysis | Weekly |
| Monthly report | Full analysis | Monthly |
| Real-time | Live monitoring | Real-time |

### Step 4: Set Targets and Alerts

**Target setting:**

| Metric | Current | Target | Basis |
|--------|---------|--------|-------|
| MRR | $50K | $75K | 50% growth |
| Churn | 5% | 3% | Best practice |
| LTV:CAC | 5:1 | 8:1 | Improve efficiency |

**Status indicators:**

| Status | Meaning | Visual |
|--------|---------|--------|
| On track | Within 10% of target | Green |
| Watch | 10-20% off target | Yellow |
| Off track | >20% off target | Red |

**Alerts to set up:**

| Alert | Trigger | Action |
|-------|---------|--------|
| Revenue drop | Down 20% WoW | Investigate |
| Churn spike | Above threshold | Review immediately |
| Zero sales | 24+ hours | Check system |
| High CAC | Above target | Review ads |

### Step 5: Create Review Cadence

**Review rhythm:**

| Frequency | Focus | Time |
|-----------|-------|------|
| Daily | Pulse check | 2 min |
| Weekly | Performance review | 30 min |
| Monthly | Deep analysis | 2 hours |
| Quarterly | Strategy review | Half day |

**Weekly review template:**

```markdown
## Weekly Review: [Date]

### Key Metrics
| Metric | This Week | Last Week | Change | Target |
|--------|-----------|-----------|--------|--------|
| Revenue | $X | $X | +X% | $X |
| Customers | X | X | +X | X |
| Churn | X% | X% | -X% | X% |

### What Went Well
- [Highlight 1]
- [Highlight 2]

### What Needs Attention
- [Issue 1]
- [Issue 2]

### Actions for Next Week
- [ ] [Action 1]
- [ ] [Action 2]
```

---

## Templates

### Essential Metrics Tracker (Spreadsheet)

```markdown
## Monthly Metrics Tracker

### Revenue
| Month | MRR | Growth | New | Churned | Net |
|-------|-----|--------|-----|---------|-----|
| Jan | $X | X% | $X | $X | $X |
| Feb | $X | X% | $X | $X | $X |

### Customers
| Month | Total | New | Churned | Net | Churn % |
|-------|-------|-----|---------|-----|---------|
| Jan | X | X | X | X | X% |
| Feb | X | X | X | X | X% |

### Unit Economics
| Month | CAC | LTV | Ratio | Payback |
|-------|-----|-----|-------|---------|
| Jan | $X | $X | X:1 | X mo |
| Feb | $X | $X | X:1 | X mo |

### Marketing
| Month | Visits | Signups | Conv % | Spend | CPA |
|-------|--------|---------|--------|-------|-----|
| Jan | X | X | X% | $X | $X |
| Feb | X | X | X% | $X | $X |
```

### Dashboard Specification

```markdown
## Dashboard: [Name]

### Purpose
[What decisions this dashboard supports]

### Audience
[Who will use it]

### Metrics
| Metric | Definition | Source | Update |
|--------|------------|--------|--------|
| [Metric 1] | [How calculated] | [Data source] | [Frequency] |

### Visualizations
1. **[Chart 1]**: [Type] showing [what]
2. **[Chart 2]**: [Type] showing [what]

### Filters
- Date range: [Options]
- Segments: [Options]

### Access
- Location: [URL]
- Permissions: [Who can access]
```

### Monthly Metrics Report

```markdown
## Monthly Report: [Month Year]

### Executive Summary
[2-3 sentence overview]

### Key Metrics
| Metric | Actual | Target | Status |
|--------|--------|--------|--------|
| Revenue | $X | $X | On/Off track |
| Growth | X% | X% | On/Off track |
| Churn | X% | X% | On/Off track |

### Revenue Analysis
- MRR: $X (↑X% MoM)
- New MRR: $X from X new customers
- Expansion: $X from upgrades
- Churned: $X from X customers

### Customer Analysis
- Total customers: X
- New this month: X
- Churned: X (X%)
- Net change: +X

### Channel Performance
| Channel | Visitors | Signups | Conv | Revenue |
|---------|----------|---------|------|---------|
| Organic | X | X | X% | $X |
| Paid | X | X | X% | $X |
| Referral | X | X | X% | $X |

### Insights
- [Key insight 1]
- [Key insight 2]
- [Key insight 3]

### Next Month Focus
- [Priority 1]
- [Priority 2]
```

---

## Examples

### Example 1: SaaS Dashboard

**North Star:** Monthly Active Users

**Key metrics:**
```
Revenue Dashboard:
├── MRR: $25,000 (↑8% MoM)
├── ARR: $300,000
├── New MRR: $3,500
├── Churned MRR: $1,500
└── Net New: $2,000

Customer Dashboard:
├── Total: 150
├── New: 20
├── Churned: 5
├── Churn rate: 3.3%
└── LTV:CAC: 6:1

Product Dashboard:
├── MAU: 1,200
├── DAU: 400
├── Feature adoption: 65%
└── NPS: 45
```

### Example 2: Info Product Dashboard

**North Star:** Course Completion Rate

**Key metrics:**
```
Revenue Dashboard:
├── Monthly sales: $15,000
├── Units sold: 30
├── Avg order value: $500
└── Refund rate: 2%

Funnel Dashboard:
├── Visitors: 10,000
├── Email signups: 500 (5%)
├── Sales page visits: 200
└── Purchases: 30 (15% of page)

Student Dashboard:
├── Active students: 200
├── Completion rate: 60%
├── Avg rating: 4.7/5
└── Testimonials: 25
```

---

## Implementation Checklist

### Setup
- [ ] Define 5-10 key metrics
- [ ] Identify data sources
- [ ] Choose dashboard tool
- [ ] Set up data connections

### Build
- [ ] Create metric calculations
- [ ] Design dashboard layout
- [ ] Build visualizations
- [ ] Add comparisons and targets

### Process
- [ ] Set review cadence
- [ ] Create alert rules
- [ ] Document definitions
- [ ] Train team (if applicable)

### Optimize
- [ ] Review weekly
- [ ] Update targets quarterly
- [ ] Add/remove metrics as needed
- [ ] Improve visualizations

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Too many metrics | Analysis paralysis | Focus on 5-10 |
| Vanity metrics | Don't drive decisions | Track actionable metrics |
| No targets | No accountability | Set clear goals |
| Stale data | Outdated decisions | Automate updates |
| Complex dashboards | Nobody uses them | Keep simple |
| No action | Data without decisions | Review and act |

---

## Metric Definitions

| Metric | Formula |
|--------|---------|
| MRR | Sum of all monthly recurring revenue |
| ARR | MRR x 12 |
| Churn rate | Customers lost / Starting customers |
| LTV | ARPU / Churn rate |
| CAC | Marketing spend / New customers |
| LTV:CAC | LTV / CAC |
| ARPU | Revenue / Customers |
| Net retention | (Starting + Expansion - Churn) / Starting |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Dashboards | Looker Studio, Geckoboard, Databox |
| Spreadsheets | Google Sheets, Airtable |
| Product analytics | Mixpanel, Amplitude, PostHog |
| Revenue | Baremetrics, ProfitWell, ChartMogul |
| Marketing | GA4, Plausible |
| Data warehouse | BigQuery, Snowflake |

---

## Related Methodologies

- **financial-planning:** Financial Planning (financial metrics)
- **analytics-setup:** Analytics Setup (marketing analytics)
- **annual-planning:** Annual Planning (annual targets)
- **customer-success:** Customer Success (customer metrics)

---

*Methodology: metrics-dashboards | Operations & Business | faion-growth-agent*
