---
name: analyze
description: Use this skill when you need to conduct a rigorous investigation of data questions, ensuring transparency and a solid audit trail.
---

# Skill body

## Rules

1. **Hypotheses first.** Before querying, brainstorm 3-5 competing explanations. Don't anchor on the first idea.
2. **Expected vs. unexpected.** Don't rediscover known patterns. Context is not a finding. Ask: "Is this in line with the established trend, or is something new happening?" Compare to recent trends, not just raw YoY.
3. **YoY always.** Raw numbers mean nothing without year-over-year context. Use a 364-day lookback to align day-of-week. Consider holidays that can shift weekdays or weeks.
4. **Segment when things move.** When a metric changes, break it down by relevant dimensions (product, channel, platform, region). Check for mix shift (Simpson's Paradox).
5. **Show your queries.** Every SQL query you run must be included in the response. Reproducibility is non-negotiable.
6. **State limitations.** What the data can't tell you is as important as what it can.
7. **Check prior work first.** Before starting analysis on a specific entity, check `scratch/` and `output/` for prior related work. Don't reinvent queries that already exist.

## Method

1. **Frame** - Define the metric, time period, and segments. Establish the baseline.
2. **Establish trend** - Query trailing 8-12 weeks to see the recent pattern. This is your "expected" baseline.
3. **Hypothesize** - List competing explanations before touching data.
4. **Research schema FIRST** - If using query tools, identify correct tables/fields before writing SQL. Don't assume field names match their apparent meaning.
5. **Query** - Test each hypothesis. Use available data discovery tools if needed.
6. **Compare to trend** - Is the latest data in line with the recent trajectory, or is something new happening?
7. **Deliver** - Lead with what's *different*, not what's *known*.

**CRITICAL:** If results contradict other known metrics (e.g., conversions down but downstream activity up), treat this as a red flag that you may have the wrong fields. Re-check schema before reporting.

## Analytical Reflexes

- **Decompose rates vs. volume:**
  - Conversions = Sessions × Conversion Rate
  - Revenue = Customers × Average Order Value

- **Work the funnel top-down:**
  - Awareness → Interest → Trial → Purchase → Retention
  - Find the bottleneck before diagnosing everywhere.