<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Weighted Ownership Scoring Algorithm

## Overview

Zero's enhanced ownership analysis uses a multi-factor scoring algorithm to determine true code ownership beyond simple commit frequency. This approach provides a more accurate picture of who really owns and understands the code.

## Scoring Components

### 1. Commit Score (30% weight)

Measures contribution volume through commit count.

```
commit_score = (contributor_commits / max_commits) * 30
```

**Why It Matters**: Commits indicate active involvement, but alone they don't tell the whole story. A developer might make many small commits or few large ones.

### 2. Code Review Score (25% weight)

Measures review participation via PR approvals and comments.

```
review_score = (contributor_reviews / max_reviews) * 25
```

**Why It Matters**: Code reviewers develop deep understanding of the codebase without necessarily being the primary author. They catch issues, suggest improvements, and transfer knowledge.

**Data Source**: GitHub API PR review data

### 3. Lines Changed Score (20% weight)

Measures actual code contribution volume.

```
lines_changed = lines_added + lines_removed
lines_score = (contributor_lines / max_lines) * 20
```

**Why It Matters**: Some contributions are more substantial than others. Lines changed captures the magnitude of involvement.

### 4. Recency Score (15% weight)

Measures how recently the contributor was active, using exponential decay.

```
days_since_last_commit = (now - last_commit).days
half_life = 90  # days

recency_decay = 0.5 ^ (days_since_last_commit / half_life)
recency_score = recency_decay * 15
```

**Why It Matters**: Recent activity indicates current knowledge. Someone who contributed heavily a year ago may no longer remember the code as well as someone who worked on it last week.

**Decay Curve**:
| Days Since Last Commit | Recency Score (out of 15) |
|------------------------|---------------------------|
| 0 | 15.0 |
| 30 | 12.6 |
| 90 | 7.5 |
| 180 | 3.75 |
| 365 | 0.94 |

### 5. Consistency Score (10% weight)

Measures regularity of contributions over time.

```
# Calculate coefficient of variation (CV) of commit gaps
gaps = [time between consecutive commits]
mean_gap = average(gaps)
std_gap = standard_deviation(gaps)
cv = std_gap / mean_gap

# Convert CV to score (lower CV = more consistent)
consistency_score = max(0, 1 - cv/2) * 10
```

**Why It Matters**: Consistent contributors maintain ongoing familiarity with the code. Sporadic contributors may have deep but outdated knowledge.

**Examples**:
| Contribution Pattern | Consistency Score |
|---------------------|-------------------|
| Daily commits | 9-10 |
| Weekly commits | 7-8 |
| Monthly commits | 5-6 |
| Sporadic bursts | 2-4 |

## Total Score Calculation

```
total_score = commit_score + review_score + lines_score + recency_score + consistency_score
```

Maximum possible score: 100

## Activity Status

Based on days since last commit:

| Status | Days Since Last Commit |
|--------|----------------------|
| Active | 0-30 |
| Recent | 31-90 |
| Stale | 91-180 |
| Inactive | 181-365 |
| Abandoned | 365+ |

## Confidence Score

The confidence score (0-1) indicates data quality:

| Confidence Level | Criteria |
|-----------------|----------|
| 0.9-1.0 | 10+ commits, PR review data available, 5+ commit dates |
| 0.7-0.9 | 5-9 commits, PR data available |
| 0.5-0.7 | 5+ commits, no PR data |
| 0.3-0.5 | < 5 commits |

## Example Output

```json
{
  "name": "Alice Developer",
  "email": "alice@example.com",
  "ownership_score": 78.5,
  "score_breakdown": {
    "commit_score": 24.0,
    "review_score": 18.75,
    "lines_score": 16.0,
    "recency_score": 12.75,
    "consistency_score": 7.0
  },
  "activity_status": "active",
  "last_active": "2025-12-10T14:30:00Z",
  "confidence": 0.9,
  "pr_reviews_given": 45
}
```

## Configuration

Weights can be customized in the scanner configuration:

```json
{
  "weights": {
    "commits": 0.30,
    "reviews": 0.25,
    "lines": 0.20,
    "recency": 0.15,
    "consistency": 0.10
  }
}
```

### Alternative Weight Profiles

**Security-Focused** (prioritize review participation):
```json
{
  "commits": 0.20,
  "reviews": 0.35,
  "lines": 0.15,
  "recency": 0.20,
  "consistency": 0.10
}
```

**Volume-Focused** (prioritize code contribution):
```json
{
  "commits": 0.35,
  "reviews": 0.15,
  "lines": 0.30,
  "recency": 0.10,
  "consistency": 0.10
}
```

## Bus Factor Calculation

Bus factor uses ownership scores to determine how many people need to leave before knowledge is lost:

```go
// Sort by ownership score descending
// Bus factor = minimum people whose combined ownership exceeds threshold

threshold := 0.5  // 50%
cumulative := 0.0

for i, owner := range sortedOwners {
    cumulative += owner.Score / totalScore
    if cumulative >= threshold {
        return i + 1  // Bus factor
    }
}
```

**Risk Levels**:
| Bus Factor | Risk Level |
|------------|------------|
| 1 | Critical |
| 2 | Warning |
| 3+ | Healthy |

## Limitations

1. **Shallow Clones**: Limited git history reduces accuracy
2. **Merge Commits**: May inflate commit counts for some developers
3. **Bot Accounts**: Automated commits can skew metrics
4. **Private Forks**: Cross-repo contributions may not be visible
5. **Pair Programming**: Git only tracks the committer, not the pair

## Best Practices

1. **Use Teams, Not Just Individuals**: Aggregate scores at team level for organizational insights
2. **Consider Context**: High ownership in legacy code may not indicate current expertise
3. **Validate with Domain Knowledge**: Metrics inform but don't replace human judgment
4. **Review Regularly**: Run analysis quarterly to track ownership trends
5. **Address Low Scores**: Low bus factor or coverage should trigger knowledge transfer
