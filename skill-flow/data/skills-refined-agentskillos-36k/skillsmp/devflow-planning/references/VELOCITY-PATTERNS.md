# Velocity Patterns

Analysis patterns for sprint velocity, trend detection, and predictive forecasting.

## Velocity Metrics

### Core Metrics

| Metric | Formula | Purpose |
|--------|---------|---------|
| Sprint Velocity | Points completed in sprint | Raw performance |
| Average Velocity | Sum(velocities) / N sprints | Planning baseline |
| Velocity Variance | σ of sprint velocities | Predictability |
| Completion Rate | Completed / Committed | Reliability |

### Weighted Average

Recent sprints matter more:

```
Weighted Velocity = (V₁×3 + V₂×2 + V₃×1) / 6

Example:
- Sprint 1 (oldest): 35 pts
- Sprint 2: 40 pts
- Sprint 3 (recent): 45 pts

Weighted = (35×1 + 40×2 + 45×3) / 6 = 41.7 pts
```

## Trend Detection

### Direction Analysis

```
Trend = Linear regression slope of last N sprints

Interpretation:
- Slope > 2:  Significantly increasing
- Slope 0-2:  Stable/slight increase
- Slope -2-0: Stable/slight decrease
- Slope < -2: Significantly decreasing
```

### Trend Classification

| Trend | 3-Sprint Pattern | Action |
|-------|-----------------|--------|
| Increasing | 35→40→45 | Can commit more |
| Stable | 40→38→42 | Maintain pace |
| Decreasing | 45→40→35 | Investigate cause |
| Volatile | 30→50→35 | Increase buffer |

## Variance Analysis

### Calculating Variance

```
Variance = Σ(Vi - Vavg)² / N

Standard Deviation = √Variance

Coefficient of Variation = σ / Vavg × 100%
```

### Variance Interpretation

| CV% | Stability | Planning Impact |
|-----|-----------|-----------------|
| <10% | Very stable | High confidence |
| 10-20% | Normal | Standard buffer |
| 20-30% | Variable | Increase buffer |
| >30% | Unstable | Conservative planning |

## Prediction Models

### Simple Prediction

```
Next Sprint = Weighted Average × Trend Factor

Trend Factors:
- Increasing: 1.05
- Stable: 1.00
- Decreasing: 0.95
```

### Confidence Intervals

```
Prediction Range = Predicted ± (σ × Confidence)

90% confidence: ± 1.65σ
80% confidence: ± 1.28σ
70% confidence: ± 1.04σ

Example:
Predicted: 42 pts, σ: 5
80% range: 42 ± 6.4 = [35.6, 48.4]
```

## Success Probability

### Sprint Success Prediction

```
Success Rate = P(completing all committed work)

Factors:
- Historical completion rate
- Current sprint load vs capacity
- Dependency risk count
- Team stability
```

### Success Calculation

```
Base Rate = Historical completion rate (e.g., 0.85)

Adjustments:
- Load >100%: -0.15
- Load 90-100%: -0.05
- Load 80-90%: 0
- Load <80%: +0.05

- Each high-risk dependency: -0.05
- New team member: -0.05
- All stories refined: +0.05
```

## Spillover Risk

### Per-Issue Risk Score

```
Risk Score = Size Factor + Dependency Factor + History Factor

Size Factor:
- 1-3 pts: 0
- 5 pts: 1
- 8 pts: 2
- 13+ pts: 3

Dependency Factor:
- No dependencies: 0
- Internal dependency: 1
- External dependency: 2
- Blocked currently: 3

History Factor:
- Never spilled: 0
- Spilled once: 1
- Spilled 2+ times: 2
```

### Risk Classification

| Score | Risk Level | Recommendation |
|-------|------------|----------------|
| 0-1 | Low | Standard monitoring |
| 2-3 | Medium | Active tracking |
| 4-5 | High | Early intervention |
| 6+ | Critical | Consider removal |

## Velocity Patterns

### Healthy Patterns

```
Pattern: Gradual Increase
[35] → [38] → [40] → [42]
Indicates: Team maturing, process improving

Pattern: Stable with Minor Variation
[40] → [38] → [42] → [39]
Indicates: Consistent, predictable team
```

### Warning Patterns

```
Pattern: Continuous Decline
[45] → [40] → [35] → [30]
Investigate: Tech debt, team issues, unclear requirements

Pattern: High Volatility
[30] → [50] → [25] → [55]
Investigate: Estimation problems, scope changes, interruptions

Pattern: Artificial Ceiling
[40] → [40] → [40] → [40]
Investigate: May be gaming estimates to match capacity
```

## Seasonal Adjustments

| Period | Expected Impact | Adjustment |
|--------|----------------|------------|
| End of quarter | -10% (demos, releases) | Reduce load |
| Holiday period | -20% (absences) | Reduce load |
| Post-release | -15% (bug fixes) | Buffer for support |
| New hire period | -10% (onboarding) | Account for training |
