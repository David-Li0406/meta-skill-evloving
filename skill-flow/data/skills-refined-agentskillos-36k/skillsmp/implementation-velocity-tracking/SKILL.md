---
name: implementation-velocity-tracking
description: Track and analyze implementation velocity metrics (actual vs estimated hours, defects per wave, test coverage trends, completion rates) to provide data-driven estimates for remaining work. Records wave completion metrics, calculates team velocity, identifies quality trends, predicts completion dates, and generates velocity dashboards. Use after wave completion, before epic planning, for sprint reviews, stakeholder reporting, or process improvement analysis.
---

# Implementation Velocity Tracking

Tracks actual implementation velocity and provides predictive estimates for remaining work based on historical data.

## Quick Start

**Record wave completion metrics:**
```
"Record metrics for wave-5.1.1: 28 actual hours, 24 estimated, 3 defects, 92% coverage"
```

**Estimate remaining work:**
```
"Estimate completion time for remaining waves in Feature 5 using historical velocity"
```

**Analyze quality trends:**
```
"Analyze defect density and test coverage trends for last 30 days"
```

## Core Workflow

### Step 1: Record Wave Completion Metrics

After each wave completes, record actual metrics:

**Timing Metrics**:
- Estimated hours (from wave plan)
- Actual hours worked
- Start date
- Completion date
- Duration (calendar days)

**Quality Metrics**:
- Defects found (during development)
- Defects found (post-release)
- Test coverage percentage
- Code review cycle time
- Rework percentage

**Deliverables**:
- User stories completed
- User stories deferred
- Acceptance criteria met
- Technical debt created

### Step 2: Calculate Velocity Metrics

**Wave Velocity**:
```
Wave Velocity = Actual Hours / Estimated Hours
```

**Examples**:
- 1.0 = Perfect estimate
- 0.8 = Finished early (20% faster than estimated)
- 1.25 = Took longer (25% over estimate)

**Rolling Average Velocity** (last N waves):
```
Team Velocity = Average(Wave Velocities)
```

**Velocity Trend**:
- Improving: Velocity decreasing toward 1.0
- Stable: Velocity consistent
- Worsening: Velocity increasing (taking longer than estimated)

### Step 3: Track Quality Metrics

**Defect Density**:
```
Defect Density = Defects Found / KLOC (thousands of lines of code)
```
Or simpler:
```
Defects per Wave = Average defects across waves
```

**Test Coverage Trend**:
- Track coverage percentage over time
- Identify waves with low coverage
- Set coverage targets (e.g., >90%)

**Rework Percentage**:
```
Rework % = (Rework Hours / Total Hours) × 100
```

### Step 4: Generate Predictive Estimates

**Estimate Remaining Work**:
```
Adjusted Estimate = Base Estimate × Team Velocity
```

**Example**:
- Remaining waves: 5 waves
- Estimated hours: 120 hours total
- Team velocity: 1.12
- Adjusted estimate: 120 × 1.12 = 134 hours

**Calendar Estimate** (with team size):
```
Calendar Days = Adjusted Hours / (Team Size × Hours per Day)
```

**Example**:
- Adjusted hours: 134
- Team size: 2 developers
- Hours per day: 8
- Calendar days: 134 / (2 × 8) = 8.4 days

**Confidence Level**:
- High: Based on 15+ completed waves
- Medium: Based on 5-14 completed waves
- Low: Based on <5 completed waves

### Step 5: Analyze Trends and Generate Reports

Create report in `Docs/reports/velocity/metrics-{date}.md`:

```markdown
# Velocity and Quality Metrics Report

**Date**: YYYY-MM-DD
**Scope**: [Epic/Feature/All]
**Period**: Last 30 days

## Executive Summary
[1-2 sentences on team velocity and quality trends]

## Velocity Metrics
- Current Team Velocity: X.XX
- Trend: [Improving/Stable/Worsening]
- Completed Waves: X
- Average Hours per Wave: XX

## Quality Metrics
- Defect Density: X.X per wave
- Test Coverage: XX%
- Rework Percentage: XX%

## Predictive Estimates
- Remaining Waves: X
- Base Estimate: XX hours
- Adjusted Estimate: XX hours (with velocity)
- Expected Completion: YYYY-MM-DD

## Trend Analysis
[Charts and analysis of trends over time]

## Recommendations
[Actions to improve velocity or quality]
```

Use `scripts/calculate_velocity.py` and `scripts/predict_completion.py`.

## Key Concepts

**Velocity**: Ratio of actual hours to estimated hours (1.0 = perfect estimate)

**Team Velocity**: Rolling average velocity across recent waves

**Defect Density**: Number of defects per wave or per KLOC

**Test Coverage**: Percentage of code covered by tests

**Rework**: Time spent fixing issues in already-completed code

**Adjusted Estimate**: Base estimate multiplied by team velocity

**Confidence Level**: Reliability of prediction based on historical data quantity

**Velocity Trend**: Direction velocity is moving (improving/stable/worsening)

## Available Resources

### Scripts
- **scripts/calculate_velocity.py** — Calculates velocity metrics from wave data
  ```bash
  python scripts/calculate_velocity.py \
    --wave wave-5.1.1 \
    --estimated 24 \
    --actual 28 \
    --output velocity-db.json
  # Output: Wave Velocity: 1.17, Team Velocity: 1.12
  ```

- **scripts/predict_completion.py** — Predicts completion date using historical velocity
  ```bash
  python scripts/predict_completion.py \
    --remaining-waves 5 \
    --estimated-hours 120 \
    --velocity-db velocity-db.json \
    --team-size 2
  # Output: Expected Completion: 2025-02-05 (±2 days)
  ```

- **scripts/analyze_trends.py** — Analyzes quality and velocity trends
  ```bash
  python scripts/analyze_trends.py \
    --velocity-db velocity-db.json \
    --metrics defect-density,coverage,velocity \
    --period 30
  # Output: Trend charts and analysis
  ```

### References
- **references/velocity-tracking-guide.md** — Comprehensive guide to velocity tracking
- **references/metrics-definitions.md** — Definitions of all tracked metrics
- **references/estimation-best-practices.md** — How to improve estimation accuracy

## Tracking Phases

### Phase 1: Initial Calibration (First 3-5 Waves)
**When**: Starting new project or team
**Focus**: Establish baseline velocity
**Output**: Initial velocity estimate
**Note**: Low confidence, wide variance expected

### Phase 2: Velocity Stabilization (Waves 6-15)
**When**: Team finding rhythm
**Focus**: Track velocity convergence
**Output**: Medium confidence estimates
**Note**: Velocity should stabilize around consistent value

### Phase 3: Mature Velocity Tracking (Wave 15+)
**When**: Established team and process
**Focus**: Fine-tuning and quality optimization
**Output**: High confidence estimates
**Note**: Focus shifts from velocity to quality metrics

### Phase 4: Continuous Improvement
**When**: Ongoing
**Focus**: Process optimization
**Output**: Trend analysis and recommendations
**Note**: Use data to drive process improvements

## Common Velocity Patterns

**Pattern 1: Early Optimism** (First 3 waves)
```
Velocity starts low (0.6-0.8), then increases to 1.2-1.5
Cause: Initial estimates too optimistic
Solution: Calibrate estimates upward
```

**Pattern 2: Learning Curve** (Waves 1-10)
```
Velocity high initially (1.5+), gradually decreases to 1.0-1.1
Cause: Team learning codebase and process
Solution: Normal, velocity will stabilize
```

**Pattern 3: Technical Debt Impact**
```
Velocity gradually increasing (1.0 → 1.3 → 1.5)
Cause: Accumulated technical debt slowing development
Solution: Dedicate waves to refactoring
```

**Pattern 4: Scope Creep**
```
Velocity consistently high (1.3-1.5)
Cause: Scope creeping beyond estimates
Solution: Better scope control in wave planning
```

**Pattern 5: Quality Issues**
```
Velocity low (0.8-0.9) but defect density high
Cause: Rushing to meet deadlines, creating defects
Solution: Allow realistic timelines, improve quality
```

## Output Format

**Console Output**:
```
Implementation Velocity Tracking
================================

Wave: 5.1.1 - Singleton Patterns
Completed: 2025-01-21

Velocity Metrics:
  Estimated Hours: 24
  Actual Hours: 28
  Wave Velocity: 1.17 (17% over estimate)

Team Velocity (last 8 waves):
  Average: 1.12
  Trend: ↓ Improving (was 1.25)
  Standard Deviation: 0.08

Quality Metrics:
  Defects Found: 3
  Defect Density: 2.8 per wave (↓ improving)
  Test Coverage: 92% (↑ improving)
  Rework: 2 hours (7%)

Updated Velocity Database: velocity-db.json

Predictive Estimate (remaining 5 waves):
  Base Estimate: 120 hours
  Adjusted (velocity 1.12): 134 hours
  With 2-person team: 67 hours/person
  Expected Completion: 2025-02-05 (±2 days)
  Confidence: MEDIUM (8 completed waves)

Report: Docs/reports/velocity/wave-5.1.1-metrics-2025-01-21.md
```

## Integration with Workflow

**`/implement-waves` integration**:
```markdown
## Step 7: Record Velocity Metrics

After wave completion:
- Record actual hours worked
- Record defects found
- Record test coverage achieved
- Invoke `implementation-velocity-tracking` skill
- Update velocity database
- Review velocity trends
```

**`/design-waves` integration**:
```markdown
## Step 0.5: Adjust Estimates Using Velocity

Before estimating new waves:
- Check current team velocity
- Adjust estimates by velocity factor
- Use historical data for similar wave types
- Account for team size changes
```

**`/review-waves` integration**:
```markdown
## Wave Retrospective: Velocity Review

During wave retrospective:
- Review velocity for completed wave
- Compare to team average
- Identify causes of variance
- Document lessons learned
- Adjust future estimates
```

**Epic Planning**:
```markdown
## Epic Estimation

Before committing to epic:
- Estimate total hours for all features
- Multiply by team velocity
- Add buffer for uncertainty
- Calculate expected duration
- Get stakeholder buy-in on timeline
```

## Success Criteria

- ✅ All completed waves have recorded metrics
- ✅ Velocity calculated accurately
- ✅ Quality metrics tracked consistently
- ✅ Trends analyzed and visualized
- ✅ Predictive estimates generated
- ✅ Confidence level appropriate
- ✅ Report generated in standard format
- ✅ Recommendations provided for improvement

## Tips for Accurate Velocity Tracking

1. **Record immediately** - Record metrics right after wave completion
2. **Be honest** - Accurate data is more valuable than optimistic data
3. **Track consistently** - Use same metrics for all waves
4. **Sufficient history** - Need 5+ waves for reliable predictions
5. **Adjust for context** - Account for team changes, complexity variations
6. **Review trends** - Look for patterns, not individual waves
7. **Use for learning** - Velocity is a tool for improvement, not judgment

## Examples

### Example 1: Record Wave Completion

**Command**:
```
"Record velocity metrics for wave-5.1.1: 28 actual hours, 24 estimated, 3 defects, 92% coverage"
```

**Process**:
1. Read velocity database (velocity-db.json)
2. Calculate wave velocity: 28 / 24 = 1.17
3. Update rolling average: (previous avg + 1.17) / n
4. Record quality metrics
5. Save to database

**Output**:
- Wave Velocity: 1.17 (17% over)
- Team Velocity: 1.12 (updated average)
- Defect Density: 2.8 per wave (improving)
- Test Coverage: 92% (on target)

---

### Example 2: Predict Remaining Work

**Command**:
```
"Estimate completion for remaining Feature 5 waves using historical velocity"
```

**Process**:
1. Read velocity database
2. Get team velocity: 1.12
3. Find remaining waves: 5 waves
4. Sum estimated hours: 120 hours
5. Apply velocity: 120 × 1.12 = 134 hours
6. Calculate calendar: 134 / (2 × 8) = 8.4 days
7. Add confidence interval: ±2 days

**Output**:
- Adjusted Estimate: 134 hours
- Expected Completion: 2025-02-05
- Confidence: MEDIUM (8 waves of history)

---

### Example 3: Analyze Quality Trends

**Command**:
```
"Analyze defect density and test coverage trends for last 30 days"
```

**Process**:
1. Read velocity database
2. Filter waves from last 30 days
3. Calculate defect density trend
4. Calculate test coverage trend
5. Identify anomalies
6. Generate recommendations

**Output**:
```
Quality Trends (Last 30 Days):

Defect Density:
  Trend: 📈 IMPROVING (4.2 → 2.8 per wave)
  Target: <3.0 ✅ ACHIEVED

Test Coverage:
  Trend: 📈 IMPROVING (85% → 92%)
  Target: >90% ✅ ACHIEVED

Alert: Defect spike in wave-5.3.1 (7 defects)
  Recommendation: Investigate root cause
```

---

**Last Updated**: 2025-01-21
