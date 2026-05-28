<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Code Ownership Metrics and Measurement

## Overview

Effective code ownership analysis requires robust measurement methodologies. This document covers proven metrics for measuring, tracking, and improving code ownership across repositories.

## Primary Measurement Approaches

### Commit-Based Ownership

**Definition**: Calculates the proportion of code changes made by a developer relative to total commits for a file.

**Formula**:
```
Commit-based ownership = (commits by developer D to file F) / (total commits to file F)
```

**Characteristics**:
- Captures frequency of involvement in active development
- Reflects recent activity and ongoing engagement
- Weights all commits equally (can be refined with LOC weighting)
- Better predictor of defects and quality issues

**Strengths**:
- **Strongest association with software quality** (research shows 97% accuracy predicting defective files)
- **Persistent predictive value**: Important in past releases remains important for current releases
- **Reflects active engagement**: Shows who is currently working on code
- **Simpler to calculate**: Just count commits per author

**Limitations**:
- May overvalue frequent small commits
- Doesn't reflect current code composition
- Recent refactoring may skew results
- Bot commits can distort metrics

**Best For**:
- Quality improvement and bug-fixing efforts
- Identifying who to ask about recent changes
- Predictive defect models
- Active maintainer identification

### Line-Based Ownership

**Definition**: Determines the percentage of source code lines authored by a developer relative to total lines in a file.

**Formula**:
```
Line-based ownership = (lines authored by developer D to file F) / (total lines in file F)
```

**Characteristics**:
- Reflects current code composition
- Shows who wrote what exists today
- Uses `git blame` or similar attribution
- More stable over time (less affected by recent activity)

**Strengths**:
- **Authorship attribution**: Clear intellectual property tracking
- **Identifies more developers**: Captures historical contributors
- **Stable metric**: Less volatile than commit-based
- **Current state reflection**: Shows who owns what code exists now

**Limitations**:
- Weaker association with defect-proneness (compared to commit-based)
- Doesn't reflect ongoing engagement
- Large initial commits dominate
- Refactoring changes attribution

**Best For**:
- Authorship and intellectual property purposes
- Identifying who wrote existing code
- Finding experts on established functionality
- Legal/compliance requirements

## Comparative Analysis

### Method Overlap (Research Findings)

**Key Discovery**: Only 0-40% of developers are commonly identified by both methods.

**File Analysis**: 25-70% of files contain no developers recognized by both approaches.

**Interpretation**: Each method captures distinct contributor populations:
- Commit-based: Active recent contributors
- Line-based: Historical authors of current code

**Major Developer Coverage**: 67-100% of developers missed by one approach qualify as major contributors by the other method.

**Consistency**: Despite different values, 50-93% of commonly identified developers maintain consistent expertise levels across both approaches (ρ = 0.24-0.65 correlation).

### Practical Recommendations

**For Bug Fixing and Quality**: Use commit-based metrics
- Stronger correlation with defects
- Identifies current active maintainers
- Better for predictive models

**For Attribution and Documentation**: Use line-based metrics
- Clear authorship of existing code
- Legal/compliance purposes
- Intellectual property tracking

**For Comprehensive Analysis**: Use both methods
- Commit-based for active engagement
- Line-based for historical authorship
- Combined view provides complete picture

## Advanced Ownership Metrics

### Weighted Ownership Score

Combines multiple factors for nuanced ownership calculation:

```
Ownership Score = (
    commit_frequency * 0.30 +
    lines_contributed * 0.20 +
    review_participation * 0.25 +
    recency_factor * 0.15 +
    consistency * 0.10
)

Where:
commit_frequency = (contributor_commits / total_commits) * 100
lines_contributed = (contributor_lines / total_lines) * 100
review_participation = (reviews_participated / total_reviews) * 100
recency_factor = e^(-ln(2) * days_since_last_commit / 90)
consistency = 1 - coefficient_of_variation(commits_per_month)
```

**Recency Factor Details**:
```
recency_factor = e^(-ln(2) * days_since_last_commit / 90)

Values:
- 1.0: Commits today
- 0.5: Commits 90 days ago (half-life)
- 0.25: Commits 180 days ago
- 0.125: Commits 270 days ago
- ~0.0: Commits >1 year ago
```

**Benefits**:
- Holistic view of ownership
- Weights multiple contribution types
- Time-decay for relevance
- Includes review activity (often overlooked)

### Major vs. Minor Contributors

**Classification**:
- **Major Contributor**: >5% of contributions to a file/module
- **Minor Contributor**: ≤5% of contributions

**Thresholds by Context**:
```
Critical code: Major = >10%
Core modules: Major = >5%
Shared libraries: Major = >3%
Documentation: Major = >2%
```

**Usage**:
- Identify primary experts (major contributors)
- Find potential reviewers (minor contributors with familiarity)
- Bus factor calculations (count major contributors)
- Succession planning (who can take over from major contributors)

## Coverage Metrics

### Ownership Coverage

**Definition**: Percentage of files/code with assigned owners.

**Formula**:
```
Ownership Coverage = (files_with_owners / total_files) * 100
```

**Granularity Levels**:
```
Repository level: All files
Directory level: Major directories
Component level: Services/modules
File type level: Languages, configs, docs
```

**Thresholds**:
- **Excellent**: >90% coverage
- **Good**: 75-90% coverage
- **Fair**: 50-75% coverage
- **Poor**: <50% coverage

**Contextual Adjustments**:
```
Core business logic: Target 95%+
Shared libraries: Target 90%+
Documentation: Target 80%+
Generated code: Exclude from calculation
Vendor/third-party: Exclude from calculation
```

## Distribution Metrics

### Gini Coefficient

**Purpose**: Measures ownership concentration/inequality.

**Formula**:
```
G = (Σ Σ |files_i - files_j|) / (2n² * mean_files)

Where:
files_i = number of files owned by person i
files_j = number of files owned by person j
n = number of owners
mean_files = average files per owner
```

**Interpretation**:
- **0.0**: Perfect equality (everyone owns same amount)
- **1.0**: Perfect inequality (one person owns everything)

**Thresholds**:
- **Excellent**: <0.3 (well distributed)
- **Good**: 0.3-0.5 (moderate concentration)
- **Fair**: 0.5-0.7 (high concentration)
- **Poor**: >0.7 (very concentrated - high risk)

**Warning Indicators**:
- Gini >0.7: Very concentrated ownership, high bus factor risk
- Top 3 own >50%: Concentration risk
- Top 1 owns >20%: Critical single point of failure

### Top-N Concentration

**Formula**:
```
top_n_concentration = (files_owned_by_top_n / total_files) * 100
```

**Healthy Ranges**:
```
Top 1 owner: <20% of codebase
Top 3 owners: <50% of codebase
Top 10 owners: <80% of codebase
```

**Risk Indicators**:
- Top 1 >20%: Single person critical dependency
- Top 3 >60%: Small group bottleneck
- Top 10 >90%: Limited team breadth

## Activity and Staleness Metrics

### Owner Staleness

**Definition**: Time since owner last contributed to their owned files.

**Formula**:
```
Owner Staleness = days_since_last_commit_to_owned_files
```

**Categories**:
- **Active**: <30 days
- **Recent**: 30-60 days
- **Stale**: 60-90 days
- **Inactive**: 90-180 days
- **Abandoned**: >180 days

**Aggregate Metrics**:
```
Active Owner Percentage = (active_owners / total_owners) * 100
Files with Stale Owners = (files_with_stale_owners / total_files) * 100
```

**Risk Assessment**:
- >20% inactive owners: Knowledge loss risk
- >30% files with stale owners: Maintenance risk
- Critical files with abandoned owners: Immediate action required

### Freshness Score

**Formula**:
```
freshness_score = (active_owners / total_owners) * 100

Where active_owners = owners with commits in last 30 days
```

**Thresholds**:
- **Excellent**: >75% active
- **Good**: 60-75% active
- **Fair**: 40-60% active
- **Poor**: <40% active

## Health Score

### Overall Ownership Health

**Comprehensive Formula**:
```
health_score = (
    coverage_score * 0.35 +
    distribution_score * 0.25 +
    freshness_score * 0.20 +
    engagement_score * 0.20
)

Where:
coverage_score = ownership_coverage_percentage
distribution_score = (1 - gini_coefficient) * 100
freshness_score = (active_owners / total_owners) * 100
engagement_score = (responsive_owners / total_owners) * 100

Responsive = owner responds to reviews within 48 hours
```

**Grading Scale**:
- **Excellent**: 85-100 (healthy, sustainable)
- **Good**: 70-84 (solid, minor improvements needed)
- **Fair**: 50-69 (concerning, action required)
- **Poor**: <50 (critical, immediate intervention)

**Component Breakdown**:
```
Coverage (35%): Files with assigned owners
Distribution (25%): Balance of ownership
Freshness (20%): Recent owner activity
Engagement (20%): Review participation
```

## Knowledge Distribution Metrics

### Expertise Breadth

**Definition**: Number of distinct areas each person contributes to.

**Categories**:
- **Specialist**: 1-2 areas (deep in narrow domain)
- **Balanced**: 3-4 areas (T-shaped profile)
- **Generalist**: 5+ areas (broad knowledge)

**Team Balance**:
```
Healthy Team Mix:
- 30% Specialists (deep expertise)
- 50% Balanced (T-shaped)
- 20% Generalists (connectors)
```

### Knowledge Overlap

**Formula**:
```
overlap = Σ(contributors_per_file - 1) / total_files
```

**Interpretation**:
- **High overlap (>2.0)**: Multiple people know each area (resilient)
- **Medium overlap (1.0-2.0)**: Some redundancy (acceptable)
- **Low overlap (<1.0)**: Single person per area (risky)

**Target**: >1.5 overlap for critical code

### Backup Coverage

**Definition**: Percentage of files where primary owner has a backup.

**Formula**:
```
backup_coverage = files_with_backup / total_files

Backup criteria:
- Has >15% contributions to area (not primary but familiar)
- Active in last 60 days
- Participated in code reviews for area
```

**Thresholds**:
- **Excellent**: >80% backup coverage
- **Good**: 60-80%
- **Fair**: 40-60%
- **Poor**: <40%

## Review Metrics

### Owner Approval Rate

**Formula**:
```
owner_approval_rate = (PRs_with_owner_approval / total_PRs) * 100
```

**Target**: >90% of PRs touching owned code get owner review

**Segmentation**:
```
Critical code: Target 100%
Core modules: Target 95%
Shared code: Target 85%
Documentation: Target 70%
```

### Review Turnaround Time

**Metrics by Owner Type**:
```
Primary owner: Median <4 hours (target)
Secondary owner: Median <8 hours (target)
Team: Median <24 hours (target)
```

**Bottleneck Detection**:
Identify owners with:
- >10 pending review requests
- >75th percentile turnaround time
- Declining participation trend

### Review Depth Score

**Scale 1-10**:
- **1-3**: Superficial (LGTM only, no comments)
- **4-6**: Moderate (some comments, catches obvious issues)
- **7-9**: Thorough (detailed feedback, catches subtle issues)
- **10**: Exceptional (architectural insights, mentoring)

**Usage**:
- Track reviewer quality
- Identify mentorship opportunities
- Balance workload by capability

## Tracking and Monitoring

### Trend Analysis

**Time Series Metrics**:
- Ownership coverage trend (monthly)
- Gini coefficient trend (monthly)
- Active owner percentage (weekly)
- Review turnaround trend (daily)

**Alerts and Thresholds**:
```
Alert if:
- Coverage drops >5% month-over-month
- Gini increases >0.1 quarter-over-quarter
- Active owners <60%
- >20% PRs waiting >48 hours for review
```

### Dashboard Metrics

**Executive View**:
- Overall health score
- Coverage percentage
- Bus factor
- Top risks

**Manager View**:
- Team-level metrics
- Individual contribution patterns
- Review bottlenecks
- Staleness alerts

**Developer View**:
- Personal ownership areas
- Review queue
- Collaboration patterns
- Expertise growth

## References

- "Code Ownership: The Principles, Differences, and Their Associations with Software Quality" (2024 arXiv:2408.12807v1)
- Microsoft Research: "An Analysis of the Effect of Code Ownership on Software Quality"
- Various ownership analysis tools and research papers (2014-2024)
