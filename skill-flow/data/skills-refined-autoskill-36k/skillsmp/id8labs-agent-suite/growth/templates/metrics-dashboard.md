# Metrics Dashboard Template

Use this template to define and track key performance indicators.

---

## Template

```markdown
# Metrics Dashboard: {Product Name}

**Last Updated:** {YYYY-MM-DD}
**Reporting Period:** {Week/Month} of {date}

---

## North Star

### {North Star Metric Name}

**Current:** {value}
**Target:** {value}
**Change:** {+/- X%} vs last period

```
[Trend visualization - ASCII chart or description]

Week 1  ████████████████  {value}
Week 2  ████████████████████  {value}
Week 3  ██████████████████████  {value}
Week 4  ████████████████████████  {value}
```

**Status:** {🟢 On Track / 🟡 At Risk / 🔴 Off Track}

---

## Acquisition Metrics

### Traffic

| Source | This Period | Last Period | Change |
|--------|-------------|-------------|--------|
| Organic Search | {N} | {N} | {+/-X%} |
| Direct | {N} | {N} | {+/-X%} |
| Social | {N} | {N} | {+/-X%} |
| Referral | {N} | {N} | {+/-X%} |
| Email | {N} | {N} | {+/-X%} |
| **Total** | **{N}** | **{N}** | **{+/-X%}** |

### Conversion

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Visitor → Signup | {%} | {%} | {🟢/🟡/🔴} |
| Signup → Activated | {%} | {%} | {🟢/🟡/🔴} |
| New users | {N} | {N} | {🟢/🟡/🔴} |
| CAC | ${X} | ${X} | {🟢/🟡/🔴} |

---

## Engagement Metrics

### Active Users

| Metric | Value | Last Period | Change |
|--------|-------|-------------|--------|
| DAU | {N} | {N} | {+/-X%} |
| WAU | {N} | {N} | {+/-X%} |
| MAU | {N} | {N} | {+/-X%} |
| DAU/MAU | {%} | {%} | {+/-X%} |

### Usage

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Sessions/user | {N} | {N} | {🟢/🟡/🔴} |
| Avg. session duration | {X min} | {X min} | {🟢/🟡/🔴} |
| Actions/session | {N} | {N} | {🟢/🟡/🔴} |
| Power users (5+ days) | {N} ({%}) | {%} | {🟢/🟡/🔴} |

---

## Retention Metrics

### Retention Rates

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| D1 Retention | {%} | {%} | {🟢/🟡/🔴} |
| D7 Retention | {%} | {%} | {🟢/🟡/🔴} |
| D30 Retention | {%} | {%} | {🟢/🟡/🔴} |
| Monthly Churn | {%} | {%} | {🟢/🟡/🔴} |

### Cohort View (Weekly)

| Cohort | W0 | W1 | W2 | W3 | W4 |
|--------|----|----|----|----|-----|
| {date} | 100% | {%} | {%} | {%} | {%} |
| {date} | 100% | {%} | {%} | {%} | - |
| {date} | 100% | {%} | {%} | - | - |
| {date} | 100% | {%} | - | - | - |

**Trend:** {Improving / Stable / Declining}

---

## Revenue Metrics

### Revenue

| Metric | Value | Last Period | Change |
|--------|-------|-------------|--------|
| MRR | ${X} | ${X} | {+/-X%} |
| New MRR | ${X} | ${X} | {+/-X%} |
| Expansion MRR | ${X} | ${X} | {+/-X%} |
| Churned MRR | ${X} | ${X} | {+/-X%} |
| Net MRR change | ${X} | ${X} | {+/-X%} |

### Unit Economics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| ARPU | ${X} | ${X} | {🟢/🟡/🔴} |
| LTV | ${X} | ${X} | {🟢/🟡/🔴} |
| LTV:CAC | {X}:1 | 3:1 | {🟢/🟡/🔴} |
| Payback period | {X} mo | {X} mo | {🟢/🟡/🔴} |

### Conversion Funnel

| Stage | Users | Rate | Revenue |
|-------|-------|------|---------|
| Free users | {N} | - | $0 |
| Trial | {N} | {%} of free | $0 |
| Paid - Basic | {N} | {%} of trial | ${X}/mo |
| Paid - Pro | {N} | {%} of basic | ${X}/mo |

---

## Referral Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| NPS | {score} | {score} | {🟢/🟡/🔴} |
| Referral rate | {%} | {%} | {🟢/🟡/🔴} |
| K-factor | {X} | {X} | {🟢/🟡/🔴} |
| Referred users | {N} | {N} | {🟢/🟡/🔴} |

---

## Experiment Metrics

### Active Experiments

| Experiment | Metric | Control | Variant | Status |
|------------|--------|---------|---------|--------|
| {exp} | {metric} | {value} | {value} | {Running/Done} |

### Recent Results

| Experiment | Winner | Lift | Significance | Shipped |
|------------|--------|------|--------------|---------|
| {exp} | {C/V} | {%} | {%} | {Y/N} |

---

## Health Indicators

### System Health

| Indicator | Status | Notes |
|-----------|--------|-------|
| Uptime | {%} | {notes} |
| Error rate | {%} | {notes} |
| Page load | {X}s | {notes} |
| Support tickets | {N} | {notes} |

### Business Health

| Indicator | Status | Notes |
|-----------|--------|-------|
| Runway | {X} months | {notes} |
| Burn rate | ${X}/mo | {notes} |
| Team capacity | {%} | {notes} |

---

## Key Insights

### What's Working
1. {insight with data}
2. {insight with data}

### What's Not Working
1. {concern with data}
2. {concern with data}

### Actions Needed
1. {action item}
2. {action item}
3. {action item}

---

## Definitions

| Metric | Definition |
|--------|------------|
| {metric} | {how it's calculated} |
| {metric} | {how it's calculated} |
| {metric} | {how it's calculated} |

---

## Data Sources

| Source | Provides | Update Frequency |
|--------|----------|------------------|
| {source} | {what} | {frequency} |
| {source} | {what} | {frequency} |
```

---

## Status Indicators

| Status | Meaning | Threshold |
|--------|---------|-----------|
| 🟢 On Track | Metric at or above target | ≥100% of target |
| 🟡 At Risk | Below target but acceptable | 80-99% of target |
| 🔴 Off Track | Significantly below target | <80% of target |

---

## Update Frequency

| Dashboard Section | Update Frequency |
|-------------------|------------------|
| North Star | Weekly |
| Acquisition | Weekly |
| Engagement | Weekly |
| Retention | Weekly |
| Revenue | Weekly |
| Cohorts | Monthly |
| Experiments | Real-time |

---

## Usage Notes

1. Update dashboard on a consistent schedule
2. Include commentary, not just numbers
3. Highlight concerning trends early
4. Link metrics to actions
5. Share with stakeholders regularly
