# Metrics Calculation

Formulas and algorithms for calculating design documentation metrics and
health scores.

## Progress Metrics

### Overall Metrics

**Total Documents:**

```text
total_documents = count of all design docs (excluding archived if filtered)
```

**By Status:**

```text
For each status (stub, draft, current, needs-review, archived):
  status_count[status] = count of docs with that status
  status_percentage[status] = (status_count[status] / total_documents) * 100
```

**Average Completeness:**

```text
average_completeness = sum(all doc completeness) / total_documents
```

**Total Coverage:**

```text
total_points = sum(all doc completeness)
possible_points = total_documents * 100
total_coverage = (total_points / possible_points) * 100
```

**Documents Complete:**

```text
complete_threshold = 90
documents_complete = count of docs where completeness >= complete_threshold
completion_rate = (documents_complete / total_documents) * 100
```

### Module Metrics

For each module, calculate:

**Document Count:**

```text
module_doc_count = count of docs in module
```

**Average Completeness:**

```text
module_avg_completeness = sum(module doc completeness) / module_doc_count
```

**Status Distribution:**

```text
For each status:
  module_status_count[status] = count of module docs with that status
  module_status_pct[status] =
    (module_status_count[status] / module_doc_count) * 100
```

**Category Coverage:**

```text
For each category in module config:
  if exists doc with category:
    category_covered = true
    category_completeness = doc.completeness
  else:
    category_covered = false

coverage_rate = (covered_categories / total_categories) * 100
```

### Category Metrics

For each category across all modules:

**Document Count:**

```text
category_doc_count = count of docs with this category
```

**Module Distribution:**

```text
modules_with_category = unique modules having docs with this category
module_coverage = (modules_with_category / total_modules) * 100
```

**Average Completeness:**

```text
category_avg_completeness = sum(category doc completeness) / category_doc_count
```

## Health Score Calculation

### Document Health Score

For each document, calculate a 0-100 health score:

#### Formula

```text
Document Health Score = (
  completeness_score * 0.4 +
  status_score * 0.3 +
  freshness_score * 0.2 +
  relationship_score * 0.1
) * 100
```

#### Component: Completeness Score (40% weight)

```text
completeness_score = doc.completeness / 100
```

Range: 0.0 to 1.0

Examples:

- 85% complete → 0.85
- 50% complete → 0.50
- 10% complete → 0.10

#### Component: Status Score (30% weight)

```text
status_score = {
  current: 1.0
  needs-review: 0.8
  draft: 0.6
  stub: 0.2
  archived: 0.0
}[doc.status]
```

Range: 0.0 to 1.0

Rationale:

- **current**: Fully reviewed and approved
- **needs-review**: Complete but awaiting review
- **draft**: In progress
- **stub**: Placeholder only
- **archived**: No longer maintained

#### Component: Freshness Score (20% weight)

Based on days since last update:

```text
days_since_update = today - doc.updated

freshness_score = {
  days_since_update < 30: 1.0
  days_since_update < 90: 0.7
  days_since_update < 180: 0.4
  days_since_update >= 180: 0.1
}
```

Range: 0.1 to 1.0

Rationale:

- Recent updates indicate active maintenance
- Stale docs (>180 days) may be outdated

#### Component: Relationship Score (10% weight)

Based on cross-reference count:

```text
relationship_count = len(doc.related) + len(doc.dependencies)

relationship_score = {
  relationship_count >= 3: 1.0
  relationship_count == 2: 0.7
  relationship_count == 1: 0.4
  relationship_count == 0: 0.0
}
```

Range: 0.0 to 1.0

Rationale:

- More relationships = better integrated documentation
- Orphaned docs (0 relationships) are harder to discover

#### Example Calculation

Document: `observability.md`

- completeness: 85%
- status: current
- updated: 5 days ago
- relationships: 3 (2 related, 1 dependency)

```text
completeness_score = 85 / 100 = 0.85
status_score = 1.0 (current)
freshness_score = 1.0 (updated < 30 days)
relationship_score = 1.0 (>= 3 relationships)

health_score = (0.85 * 0.4 + 1.0 * 0.3 + 1.0 * 0.2 + 1.0 * 0.1) * 100
             = (0.34 + 0.30 + 0.20 + 0.10) * 100
             = 0.94 * 100
             = 94
```

Result: 94/100 (Excellent)

### Module Health Score

Average health score of all documents in module:

```text
module_health = sum(all doc health scores in module) / module_doc_count
```

### Overall Health Score

Weighted average across all modules:

```text
total_health_points = sum(module_health * module_doc_count for each module)
overall_health = total_health_points / total_documents
```

Alternative (simple average):

```text
overall_health = sum(all doc health scores) / total_documents
```

### Health Rating

Convert numeric score to rating:

```text
health_rating = {
  score >= 90: "excellent"
  score >= 70: "good"
  score >= 50: "fair"
  score < 50: "poor"
}
```

### Health Distribution

Count documents in each rating category:

```text
For each rating (excellent, good, fair, poor):
  rating_count[rating] = count of docs in that range
  rating_percentage[rating] = (rating_count[rating] / total_documents) * 100
```

## Derived Metrics

### Age Metrics

**Document Age:**

```text
age_days = today - doc.created
age_weeks = age_days / 7
age_months = age_days / 30
```

**Staleness:**

```text
staleness_days = today - doc.updated
```

**Sync Lag:**

```text
if doc.last_synced == "never":
  sync_lag = "never"
else:
  sync_lag_days = today - doc.last_synced
```

### Velocity Metrics

**Completion Velocity:**

```text
completed_docs = count of docs where completeness >= 90
months_since_first = (today - first_doc.created) / 30
velocity = completed_docs / months_since_first
```

**Estimated Completion Time:**

```text
remaining_docs = total_documents - completed_docs
estimated_months = remaining_docs / velocity
```

### Coverage Gaps

**Missing Categories:**

```text
expected_categories = union of all module.categories from config
documented_categories = unique categories from all docs
missing_categories = expected_categories - documented_categories
```

**Under-Documented Categories:**

```text
For each category:
  if avg_completeness < 60:
    under_documented.append(category)
```

## Issue Detection

### Stale Documents

```text
stale_threshold = 90  # days

For each doc:
  if (today - doc.updated) > stale_threshold:
    if doc.status == "current":
      stale_docs.append({
        doc: doc,
        days: today - doc.updated,
        severity: "high"
      })
```

### Orphaned Documents

```text
For each doc:
  relationships = len(doc.related) + len(doc.dependencies)
  incoming_refs = count of other docs referencing this doc

  if relationships == 0 and incoming_refs == 0:
    orphaned_docs.append(doc)
```

### Incomplete Documents

```text
completeness_threshold = 80

For each doc:
  if doc.status == "current" and doc.completeness < completeness_threshold:
    incomplete_docs.append({
      doc: doc,
      expected: completeness_threshold,
      actual: doc.completeness,
      gap: completeness_threshold - doc.completeness
    })
```

### Sync Lag

```text
sync_threshold = 60  # days

For each doc:
  if doc.last_synced == "never":
    never_synced.append(doc)
  elif (today - doc.last_synced) > sync_threshold:
    sync_lagged.append({
      doc: doc,
      days: today - doc.last_synced
    })
```

### Status Mismatches

```text
For each doc:
  expected_status = {
    completeness >= 90: "current"
    completeness >= 60: "current" or "draft"
    completeness >= 20: "draft"
    completeness < 20: "stub"
  }

  if doc.status not in expected_status:
    mismatched.append({
      doc: doc,
      actual_status: doc.status,
      expected_status: expected_status,
      completeness: doc.completeness
    })
```

## Trend Analysis

### Requires Historical Data

If previous report available:

**Document Count Change:**

```text
docs_added = current.total_documents - previous.total_documents
docs_removed = (count of previous docs not in current)
net_change = docs_added - docs_removed
```

**Completeness Change:**

```text
completeness_delta = current.avg_completeness - previous.avg_completeness
```

**Health Score Change:**

```text
health_delta = current.overall_health - previous.overall_health
```

**Status Distribution Change:**

```text
For each status:
  status_change[status] =
    current.status_count[status] - previous.status_count[status]
```

### Growth Rate

```text
report_interval_days = current.date - previous.date
daily_growth_rate = docs_added / report_interval_days
monthly_growth_rate = daily_growth_rate * 30
```

## Prioritization

### Issue Priority

Assign priority based on impact and urgency:

```text
For each issue:
  priority = calculate_priority(issue.type, issue.severity, issue.impact)

  where:
    priority = {
      orphaned + stub: "critical"
      stale + current: "high"
      never_synced + current: "high"
      incomplete + current: "medium"
      never_synced + draft: "low"
      status_mismatch: "low"
    }
```

### Recommendation Priority

```text
Priority 1 (This Week):
  - Critical issues
  - High-impact, low-effort fixes

Priority 2 (This Month):
  - Medium priority issues
  - Complete draft documents

Priority 3 (This Quarter):
  - Low priority issues
  - Process improvements
  - Documentation enhancements
```

## Benchmarking

### Target Metrics

Define target benchmarks for healthy documentation:

```text
targets = {
  overall_health: >= 80
  avg_completeness: >= 75
  current_status_percentage: >= 60
  orphaned_percentage: <= 10
  stale_percentage: <= 15
  never_synced_percentage: <= 20
  excellent_health_percentage: >= 40
  poor_health_percentage: <= 10
}
```

### Gap Analysis

```text
For each metric:
  gap = target - actual
  if gap > 0:
    gaps.append({
      metric: metric_name,
      target: target,
      actual: actual,
      gap: gap,
      actions_needed: calculate_actions(gap)
    })
```

### Actions Needed

```text
For completeness gap:
  points_needed = gap * total_documents
  actions = "Complete {points_needed} percentage points across docs"

For health gap:
  docs_to_improve = calculate_docs_needing_improvement(gap)
  actions = "Improve {docs_to_improve} documents to good/excellent"
```
