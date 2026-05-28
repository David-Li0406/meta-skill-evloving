# Design Report Detailed Instructions

Complete step-by-step workflow for generating design documentation status reports.

## Detailed Workflow

### 1. Parse Parameters

Extract module, format, and focus from user request.

**Parameter parsing examples:**

- `/design-report` → module: `all`, format: `markdown`, focus: `all`
- `/design-report effect-type-registry` → module: `effect-type-registry`,
  format: `markdown`, focus: `all`
- `/design-report --format=json` → module: `all`, format: `json`, focus: `all`
- `/design-report --focus=health` → module: `all`, format: `markdown`,
  focus: `health`
- `/design-report module --include-archived` → include archived docs

### 2. Load Configuration

Read `.claude/design/design.config.json` to get:

- Module definitions and paths
- Design docs locations
- Quality standards and targets

**Configuration structure:**

```json
{
  "modules": {
    "module-name": {
      "path": ".claude/design/module-name",
      "description": "...",
      "enabled": true
    }
  },
  "quality": {
    "minCompleteness": 80,
    "maxStaleness": 90,
    "syncFrequency": 60
  }
}
```

**Configuration loading:**

1. Read design.config.json
2. Parse JSON structure
3. Extract module paths
4. Filter by enabled modules
5. Apply module parameter filter if specified
6. Load quality standards for thresholds

### 3. Collect Design Documents

Use Glob to find design docs:

**All modules:**

```bash
for module in ${modules[@]}; do
  glob "*.md" --path=".claude/design/${module}"
done
```

**Specific module:**

```bash
glob "*.md" --path=".claude/design/{module}"
```

**Filtering:**

- By default, exclude archived docs (status: archived)
- If `--include-archived` specified, include all docs
- Exclude non-design files (README.md, templates, etc.)

**Document collection:**

1. Iterate through target modules
2. Glob for `*.md` files in each module path
3. Apply archive filter based on parameters
4. Build list of document paths with module association
5. Sort by module, then by category, then by name

### 4. Parse Document Metadata

For each doc, extract frontmatter and calculate derived metrics.

**Frontmatter extraction:**

Read first 30 lines of document to extract YAML frontmatter:

```yaml
---
status: current
completeness: 85
category: architecture
created: 2025-01-10
updated: 2025-01-15
last-synced: 2025-01-14
related:
  - path/to/related-doc.md
dependencies:
  - path/to/dependency-doc.md
---
```

**Core fields:**

- `status`: Document status (stub, draft, current, needs-review, archived)
- `completeness`: Percentage (0-100)
- `category`: Design doc category (architecture, performance, etc.)
- `created`: ISO date when created
- `updated`: ISO date of last update
- `last-synced`: ISO date of last code sync

**Reference fields:**

- `related`: Array of related document paths
- `dependencies`: Array of dependency paths

**Derived metrics:**

Calculate additional metrics from frontmatter:

```javascript
// Age: Days since creation
age = Math.floor((today - created) / (1000 * 60 * 60 * 24))

// Staleness: Days since last update
staleness = Math.floor((today - updated) / (1000 * 60 * 60 * 24))

// Sync lag: Days since last sync (or null if never synced)
syncLag = lastSynced
  ? Math.floor((today - lastSynced) / (1000 * 60 * 60 * 24))
  : null

// Relationship count: Total cross-references
relationshipCount = (related?.length || 0) + (dependencies?.length || 0)
```

**Metadata validation:**

1. Verify required fields exist
2. Check value ranges (completeness 0-100, valid status)
3. Parse dates correctly
4. Flag invalid frontmatter for error handling

### 5. Calculate Progress Metrics

Aggregate metrics across different dimensions.

**Overall metrics:**

```javascript
// Total document count
totalDocs = documents.length

// Status distribution
statusCounts = {
  stub: documents.filter(d => d.status === 'stub').length,
  draft: documents.filter(d => d.status === 'draft').length,
  current: documents.filter(d => d.status === 'current').length,
  needsReview: documents.filter(d => d.status === 'needs-review').length,
  archived: documents.filter(d => d.status === 'archived').length
}

// Average completeness
avgCompleteness = sum(documents.map(d => d.completeness)) / totalDocs

// Total coverage (weighted by expected doc count)
totalCoverage = (
  sum(documents.map(d => d.completeness)) / (expectedDocs * 100)
) * 100
```

**Per-module metrics:**

```javascript
for (module in modules) {
  moduleDocs = documents.filter(d => d.module === module)

  moduleMetrics[module] = {
    docCount: moduleDocs.length,
    avgCompleteness: sum(moduleDocs.map(d => d.completeness)) / moduleDocs.length,
    statusDistribution: calculateStatusDistribution(moduleDocs),
    categoryCoverage: calculateCategoryCoverage(moduleDocs)
  }
}
```

**Per-category metrics:**

```javascript
for (category in categories) {
  categoryDocs = documents.filter(d => d.category === category)

  categoryMetrics[category] = {
    docCount: categoryDocs.length,
    moduleDistribution: calculateModuleDistribution(categoryDocs),
    avgCompleteness: sum(categoryDocs.map(d => d.completeness)) / categoryDocs.length
  }
}
```

### 6. Assess Documentation Health

Calculate health scores using weighted formula.

**Document-level health:**

```javascript
function calculateDocumentHealth(doc) {
  // Status score (0-1)
  const statusScores = {
    archived: 0,
    stub: 0.2,
    draft: 0.5,
    'needs-review': 0.8,
    current: 1.0
  }
  const statusScore = statusScores[doc.status] || 0

  // Completeness score (0-1)
  const completenessScore = doc.completeness / 100

  // Freshness score (0-1)
  const freshnessScore = doc.staleness <= 30 ? 1.0 :
                        doc.staleness <= 60 ? 0.7 :
                        doc.staleness <= 90 ? 0.4 :
                        0.0

  // Relationship score (0-1)
  const relationshipScore = Math.min(doc.relationshipCount / 3, 1.0)

  // Weighted total (0-100)
  return (
    completenessScore * 0.4 +
    statusScore * 0.3 +
    freshnessScore * 0.2 +
    relationshipScore * 0.1
  ) * 100
}
```

**Module-level health:**

```javascript
function calculateModuleHealth(moduleDocs) {
  const docHealthScores = moduleDocs.map(calculateDocumentHealth)
  return sum(docHealthScores) / moduleDocs.length
}
```

**Overall health:**

```javascript
function calculateOverallHealth(modules) {
  // Weighted average (larger modules have more weight)
  let totalWeight = 0
  let weightedSum = 0

  for (module in modules) {
    const weight = modules[module].docCount
    const health = modules[module].health

    weightedSum += health * weight
    totalWeight += weight
  }

  return weightedSum / totalWeight
}
```

**Health ratings:**

Convert numeric scores to letter grades:

```javascript
function getHealthRating(score) {
  if (score >= 90) return { grade: 'A', label: 'Excellent' }
  if (score >= 70) return { grade: 'B', label: 'Good' }
  if (score >= 50) return { grade: 'C', label: 'Fair' }
  return { grade: 'D', label: 'Poor' }
}
```

### 7. Identify Issues and Gaps

Detect problems requiring attention.

**Stale documents:**

```javascript
staleDocs = documents.filter(d =>
  d.status !== 'archived' &&
  d.staleness > 90
)
```

**Orphaned documents:**

```javascript
orphanedDocs = documents.filter(d =>
  d.status !== 'archived' &&
  d.relationshipCount === 0
)
```

**Incomplete documents:**

```javascript
incompleteDocs = documents.filter(d =>
  d.status === 'current' &&
  d.completeness < 80
)
```

**Missing categories:**

```javascript
const expectedCategories = [
  'architecture',
  'performance',
  'security',
  'testing',
  'deployment'
]

missingCategories = expectedCategories.filter(cat =>
  !documents.some(d => d.category === cat)
)
```

**Sync lag issues:**

```javascript
syncLagDocs = documents.filter(d =>
  d.status === 'current' &&
  (d.syncLag === null || d.syncLag > 60)
)
```

**Issue severity:**

Assign severity based on impact:

- **Critical**: Current docs with <50% completeness, never synced
- **High**: Stale current docs (>90 days), major category gaps
- **Medium**: Orphaned docs, sync lag >60 days
- **Low**: Draft docs incomplete, minor category gaps

### 8. Generate Report

Create output in requested format.

**Markdown report structure:**

```markdown
# Design Documentation Status Report

**Generated:** {timestamp}
**Scope:** {modules}

## Executive Summary

- Total Documents: {count}
- Overall Health: {score} ({rating})
- Average Completeness: {percentage}%
- Status Distribution: {current}/{draft}/{stub}

## Progress Metrics

### Overall Progress
{tables and charts}

### Per Module
{module breakdowns}

### Per Category
{category breakdowns}

## Health Assessment

### Overall Health: {score}/100 ({rating})

{health details}

### Module Health Scores
{module scores table}

## Issues and Gaps

### Critical Issues ({count})
{list}

### High Priority ({count})
{list}

## Recommendations

### Priority 1: This Week
{actionable items}

### Priority 2: This Month
{actionable items}

### Priority 3: This Quarter
{actionable items}
```

**JSON report structure:**

```json
{
  "metadata": {
    "generated": "2025-01-17T10:30:00Z",
    "scope": ["module1", "module2"]
  },
  "summary": {
    "totalDocs": 42,
    "overallHealth": 78.5,
    "avgCompleteness": 72.3,
    "statusDistribution": {...}
  },
  "progress": {
    "overall": {...},
    "byModule": {...},
    "byCategory": {...}
  },
  "health": {
    "overall": {...},
    "modules": {...},
    "documents": [...]
  },
  "issues": {
    "stale": [...],
    "orphaned": [...],
    "incomplete": [...],
    "syncLag": [...]
  },
  "recommendations": [...]
}
```

**HTML report:**

- Use CSS for styling and layout
- Include interactive charts (if possible)
- Color-coded health indicators
- Expandable sections for details

### 9. Provide Recommendations

Prioritize actions based on impact and effort.

#### Priority 1: This Week (High Impact, Low Effort)

- Fix critical completeness gaps in current docs
- Sync never-synced current docs
- Update stale high-traffic docs

#### Priority 2: This Month (High Impact, Medium Effort)

- Promote high-quality draft docs to current
- Fill major category gaps
- Connect orphaned docs with references

#### Priority 3: This Quarter (Long-term Improvements)

- Implement automated sync workflows
- Create missing category documentation
- Archive outdated draft docs
- Improve cross-module documentation

**Recommendation format:**

```markdown
### {Title}

**Impact:** {High/Medium/Low}
**Effort:** {Low/Medium/High}
**Affected:** {module or category}

{Description of the issue}

**Action:**
1. {Step 1}
2. {Step 2}

**Expected improvement:** {metric} from {current} to {target}
```

## Advanced Features

### Trend Analysis

Compare current report with historical reports:

```javascript
function analyzeTrends(currentReport, historicalReports) {
  return {
    completenessChange: calculateChange(current.avgCompleteness, previous.avgCompleteness),
    healthChange: calculateChange(current.overallHealth, previous.overallHealth),
    documentGrowth: current.totalDocs - previous.totalDocs,
    velocityMetrics: calculateVelocity(historicalReports)
  }
}
```

### Benchmarking

Compare modules against each other:

```javascript
function benchmarkModules(moduleMetrics) {
  const sorted = sortBy(moduleMetrics, 'health')

  return {
    topPerformer: sorted[0],
    needsAttention: sorted[sorted.length - 1],
    averageHealth: calculateAverage(moduleMetrics.map(m => m.health)),
    variance: calculateVariance(moduleMetrics.map(m => m.health))
  }
}
```

### Custom Focus Areas

Generate focused reports:

- **Progress focus:** Emphasize completion metrics and velocity
- **Health focus:** Emphasize health scores and improvement areas
- **Gaps focus:** Emphasize missing docs and coverage holes
- **Sync focus:** Emphasize sync status and code alignment
