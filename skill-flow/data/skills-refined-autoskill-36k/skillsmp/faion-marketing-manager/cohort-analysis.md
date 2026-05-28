---
id: cohort-analysis
name: "Cohort Analysis"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Cohort Analysis

## Metadata

| Field | Value |
|-------|-------|
| **ID** | cohort-analysis |
| **Name** | Cohort Analysis |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | aarrr-pirate-metrics, funnel-optimization, retention-loops |

---

## Problem

You look at your overall metrics: "30-day retention is 15%." But is that good? Is it improving? You do not know because you are mixing users who joined yesterday with users who joined 6 months ago.

Cohort analysis groups users by a shared characteristic (usually signup date) and tracks their behavior over time. This reveals trends that aggregate metrics hide.

---

## Framework

### What is a Cohort?

A cohort is a group of users who share a common characteristic, typically when they started using your product.

```
January cohort:  Users who signed up in January
February cohort: Users who signed up in February
...
```

### Why Cohorts Matter

**Without cohorts:**
```
Overall D30 Retention: 15%
(Is this good? Getting better? Worse? Cannot tell.)
```

**With cohorts:**
```
Jan cohort D30: 12%
Feb cohort D30: 14%
Mar cohort D30: 15%
Apr cohort D30: 18%

Insight: Retention is improving each month!
```

### Types of Cohort Analysis

#### 1. Acquisition Cohorts (Most Common)

Group by when users joined.

```
            Week 0  Week 1  Week 2  Week 3  Week 4
Jan 1-7     100%    45%     30%     22%     18%
Jan 8-14    100%    48%     32%     24%     20%
Jan 15-21   100%    52%     35%     26%     22%
Jan 22-28   100%    55%     38%     28%     --
```

**Use for:** Tracking retention, engagement over time

#### 2. Behavioral Cohorts

Group by action taken.

```
Users who completed onboarding vs did not:

                Week 0  Week 1  Week 2  Week 3
Completed       100%    65%     48%     38%
Not completed   100%    30%     15%     8%
```

**Use for:** Finding valuable user behaviors

#### 3. Feature Cohorts

Group by feature used.

```
Users who used feature X vs did not:

                D30 Retention
Used Feature X      42%
Did not use         18%
```

**Use for:** Validating feature impact

### Reading Cohort Tables

**Retention Table:**
```
           Day 0   Day 1   Day 7   Day 14  Day 30
Week 1     1000    420     210     150     100     ← Raw numbers
           100%    42%     21%     15%     10%     ← Percentages

Week 2     1200    540     276     192     --
           100%    45%     23%     16%     --

Week 3     900     414     207     --      --
           100%    46%     23%     --      --
```

**Reading:**
- Row = Cohort (when users joined)
- Column = Time since joining
- Cell = Users still active

**Diagonal = "Today":**
```
           D0      D1      D7      D14     D30
Week 1     ·       ·       ·       ·       10%  ← Oldest cohort, most data
Week 2     ·       ·       ·       16%     --
Week 3     ·       ·       23%     --      --
Week 4     ·       46%     --      --      --
Week 5     100%    --      --      --      --   ← Newest, just joined
           ↑
        Diagonal shows progression through time
```

---

## Templates

### Retention Cohort Table Template

```markdown
# Cohort Retention Analysis

## Period: [Month/Quarter]
## Metric: [Retention definition - e.g., "logged in"]

### Cohort Table

| Cohort | Size | D1 | D7 | D14 | D30 | D60 | D90 |
|--------|------|-----|-----|------|------|------|------|
| [Date] | | | | | | | |
| [Date] | | | | | | | |
| [Date] | | | | | | | |

### Key Observations

1. **Trend:** [Improving / Stable / Declining]
2. **Drop-off point:** [Where biggest drop happens]
3. **Stabilization:** [When retention levels off]

### Cohort Comparison

| Period | D30 Retention | Change |
|--------|---------------|--------|
| This period | | |
| Last period | | |
| YoY | | |

### Actions
- [ ] [Based on observations]
```

### Behavioral Cohort Template

```markdown
# Behavioral Cohort Analysis

## Hypothesis
Users who [take action X] have better [metric] than those who do not.

## Cohort Definitions
| Cohort | Definition | Sample Size |
|--------|------------|-------------|
| A | Users who [did X] | |
| B | Users who [did not do X] | |

## Results

| Metric | Cohort A | Cohort B | Difference |
|--------|----------|----------|------------|
| D30 Retention | | | |
| Conversion Rate | | | |
| LTV | | | |

## Conclusion
[Does action X predict better outcomes?]

## Implications
[If yes, how to get more users to take action X?]
```

---

## Examples

### Example 1: Monthly Acquisition Cohorts

**Product:** SaaS tool

**Cohort Retention Table:**

| Cohort | Size | D1 | D7 | D30 | D60 | D90 |
|--------|------|-----|-----|------|------|------|
| Oct 2025 | 2,000 | 45% | 22% | 12% | 9% | 8% |
| Nov 2025 | 2,400 | 48% | 25% | 14% | 10% | 8% |
| Dec 2025 | 2,100 | 52% | 28% | 16% | 11% | -- |
| Jan 2026 | 2,800 | 55% | 30% | 18% | -- | -- |
| Feb 2026 | 3,200 | 58% | 32% | -- | -- | -- |

**Insights:**
- D1 retention improving: 45% → 58% (+13pp over 5 months)
- D30 retention improving: 12% → 18% (+6pp)
- Recent cohorts are higher quality
- Product improvements are working

**Visualization:**
```
D30 Retention by Cohort

18% │                              ███
16% │                    ███
14% │          ███
12% │ ███
10% │
 8% │
    └────────────────────────────────────
      Oct    Nov    Dec    Jan    Feb
```

### Example 2: Behavioral Cohort - Onboarding

**Hypothesis:** Users who complete onboarding tutorial have better retention.

**Cohorts:**
- A: Completed all 5 onboarding steps (n=1,500)
- B: Skipped or partial onboarding (n=2,500)

**Results:**

| Metric | Completed (A) | Skipped (B) | Lift |
|--------|---------------|-------------|------|
| D7 Retention | 68% | 32% | +113% |
| D30 Retention | 45% | 15% | +200% |
| Conversion to Paid | 8% | 2% | +300% |

**Conclusion:** Onboarding completion is a strong predictor of success. Focus on increasing completion rate.

### Example 3: Feature Adoption Cohort

**Question:** Does using the "collaboration" feature improve retention?

**Cohorts:**
- A: Used collaboration feature in first week (n=800)
- B: Did not use collaboration (n=3,200)

**Results:**

| Metric | Used Collab (A) | No Collab (B) | Lift |
|--------|-----------------|---------------|------|
| D30 Retention | 52% | 18% | +189% |
| D90 Retention | 38% | 10% | +280% |
| LTV | $420 | $95 | +342% |

**Insight:** Collaboration is a "magic feature." Priority: Get users to invite teammates in first week.

### Example 4: Detecting a Problem

**Cohort Retention Table:**

| Cohort | D1 | D7 | D30 |
|--------|-----|-----|------|
| Week 1 | 55% | 30% | 18% |
| Week 2 | 52% | 28% | 16% |
| Week 3 | 48% | 24% | 14% |
| Week 4 | 42% | 20% | -- |
| Week 5 | 38% | -- | -- |

**Problem detected:** Retention is declining week over week.

**Investigation:**
- Traffic source changed? (Lower quality leads)
- Product broken? (Bug introduced)
- Competition? (New competitor launched)
- Seasonality? (Holiday period)

---

## Building Cohort Analysis

### Step 1: Define Cohorts

```sql
-- Example: Weekly acquisition cohorts
SELECT
  DATE_TRUNC('week', signup_date) AS cohort_week,
  user_id,
  signup_date
FROM users
```

### Step 2: Track Activity

```sql
-- Activity by day since signup
SELECT
  u.cohort_week,
  DATEDIFF('day', u.signup_date, e.event_date) AS days_since_signup,
  COUNT(DISTINCT e.user_id) AS active_users
FROM users u
JOIN events e ON u.user_id = e.user_id
WHERE e.event_type = 'login'
GROUP BY 1, 2
```

### Step 3: Calculate Retention

```sql
-- Retention percentages
SELECT
  cohort_week,
  days_since_signup,
  active_users,
  ROUND(100.0 * active_users / cohort_size, 1) AS retention_pct
FROM (
  -- Previous query
)
```

### Step 4: Pivot to Table

```
        D0    D1    D7    D30
Week1   100%  45%   22%   12%
Week2   100%  48%   25%   14%
...
```

---

## Implementation Checklist

- [ ] Define cohort grouping (weekly/monthly)
- [ ] Define retention metric (login, action, etc.)
- [ ] Build data pipeline
- [ ] Create cohort table
- [ ] Set up automated updates
- [ ] Establish benchmarks
- [ ] Review weekly
- [ ] Investigate any declines

---

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Using averages without cohorts | Hides trends | Always segment by cohort |
| Too granular cohorts | Small samples, noisy data | Weekly minimum for most products |
| Not waiting for data | Incomplete picture | Wait for cohort to mature |
| Ignoring cohort size | Small cohorts skew results | Weight by size or filter |
| Only acquisition cohorts | Miss behavioral insights | Add behavioral cohorts |

---

## Benchmarks

### SaaS Retention (B2B)

| Metric | Poor | Average | Good | Great |
|--------|------|---------|------|-------|
| D1 | <30% | 30-40% | 40-50% | >50% |
| D7 | <15% | 15-25% | 25-35% | >35% |
| D30 | <8% | 8-15% | 15-25% | >25% |
| D90 | <5% | 5-10% | 10-20% | >20% |

### Consumer App

| Metric | Poor | Average | Good | Great |
|--------|------|---------|------|-------|
| D1 | <20% | 20-30% | 30-40% | >40% |
| D7 | <10% | 10-15% | 15-25% | >25% |
| D30 | <4% | 4-8% | 8-15% | >15% |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Product analytics | Amplitude, Mixpanel, Posthog |
| Data warehouse | BigQuery, Snowflake, Redshift |
| Visualization | Metabase, Looker, Mode |
| Spreadsheet | Google Sheets, Excel |

---

## Cohort Analysis Checklist

Weekly review:
- [ ] Pull latest cohort data
- [ ] Compare to previous cohorts
- [ ] Identify any significant changes
- [ ] Investigate declines
- [ ] Document insights

Monthly review:
- [ ] Analyze long-term retention (D60, D90)
- [ ] Compare cohort quality over time
- [ ] Correlate with acquisition channels
- [ ] Update benchmarks

---

## Related Methodologies

- **aarrr-pirate-metrics:** AARRR Pirate Metrics (retention as a stage)
- **funnel-optimization:** Funnel Optimization (analyze by cohort)
- **retention-loops:** Retention Loops (improve retention)

---

*Methodology: cohort-analysis | Growth | faion-growth-agent*
