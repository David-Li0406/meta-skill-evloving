# Report Output Formats

Report format specifications for design documentation status reports in
markdown, JSON, and HTML.

## Format: Markdown

Generate human-readable markdown report for direct viewing or inclusion in
documentation.

### Structure

```markdown
# Design Documentation Status Report

**Generated:** {date}
**Modules:** {count}
**Total Documents:** {count}
**Overall Health:** {score}/100 {indicator}

---

## Executive Summary
## Module Reports
## Category Coverage
## Issues and Recommendations
## Progress Trends
## Health Score Breakdown
## Next Steps
```

### Executive Summary Section

High-level metrics for quick overview:

```markdown
## Executive Summary

### Progress

- **Total Coverage:** 62% (744 / 1200 points)
- **Average Completeness:** 62%
- **Documents Complete:** 5/12 (42%)

### Health

- **Overall Score:** 72/100
- **Excellent:** 3 docs (25%)
- **Good:** 5 docs (42%)
- **Fair:** 2 docs (17%)
- **Poor:** 2 docs (17%)

### Status Distribution

- Current: 7 (58%)
- Draft: 3 (25%)
- Stub: 2 (17%)
- Needs Review: 0 (0%)
- Archived: 0 (0%)
```

**Indicators:**

- Score >= 90: ✅ (excellent)
- Score >= 70: ⚠️  (good/warning)
- Score < 70: ❌ (needs attention)

### Module Reports Section

Detailed breakdown per module:

```markdown
## Module Reports

### {module-name}

**Documents:** {count}
**Health Score:** {score}/100 {indicator}
**Average Completeness:** {percentage}%

**Status Breakdown:**

- Current: {count} ({percentage}%)
- Draft: {count} ({percentage}%)
- Stub: {count} ({percentage}%)

**Documents:**

1. **{filename}** ({status}, {completeness}%, health: {score})
   - Last updated: {days} days ago
   - Synced: {days} days ago / never
   - Relationships: {count}
   - **Status:** {indicator} {rating}
   - **Issues:** (if any)
     - Issue description
     - Another issue

**Module Issues:**

- {count} orphaned documents
- {count} documents never synced
- {count} documents below expected completeness
```

**Health Indicators:**

- Health >= 90: ✅ Excellent
- Health >= 70: ✅ Good
- Health >= 50: ⚠️  Fair
- Health < 50: ❌ Poor

### Category Coverage Section

Cross-module category analysis:

```markdown
## Category Coverage

### {category-name}

**Documents:** {count}
**Modules:** {count}
**Average Completeness:** {percentage}%
**Health Score:** {score}/100

**Coverage:**

- {module}: {filename} ({completeness}%) {indicator}
- {module}: {filename} ({completeness}%) {indicator}

### Missing Categories

- **{category}:** No documents (expected in {module})
```

**Completeness Indicators:**

- >= 80%: No indicator (on track)
- < 80%: ⚠️  (needs work)
- < 30%: ❌ (critical)

### Issues and Recommendations Section

Prioritized action items:

```markdown
## Issues and Recommendations

### Critical Issues ({count})

1. **{issue-type}**
   - {affected-doc}
   - **Fix:** {action-description}

### Warnings ({count})

1. **{issue-type} ({count} docs)**
   - {affected-doc-1}
   - {affected-doc-2}
   - **Fix:** {action-description}

### Recommendations

**Priority 1 (This Week):**

1. {action-item-1}
2. {action-item-2}

**Priority 2 (This Month):**

1. {action-item-1}
2. {action-item-2}

**Priority 3 (This Quarter):**

1. {action-item-1}
2. {action-item-2}
```

**Priority Assignment:**

- Priority 1: Critical issues, high-impact quick wins
- Priority 2: Important improvements, medium effort
- Priority 3: Long-term enhancements, process improvements

### Progress Trends Section

Historical comparison (if previous report available):

```markdown
## Progress Trends

**Since Last Report:**

- Documents added: +{count}
- Average completeness: {old}% → {new}% ({delta}%)
- Health score: {old}/100 → {new}/100 ({delta})
- Current status docs: {old} → {new} ({delta})

**Velocity:**

- Docs completed per month: ~{count}
- Estimated time to 80% coverage: {months} months
```

**Velocity Calculation:**

```text
velocity = completed_docs / months_since_first_doc
estimated_time = remaining_docs / velocity
```

### Health Score Breakdown Section

Distribution table and targets:

```markdown
## Health Score Breakdown

| Range | Rating | Count | Percentage |
| :---- | :----- | :---- | :--------- |
| 90-100 | Excellent | {count} | {pct}% |
| 70-89 | Good | {count} | {pct}% |
| 50-69 | Fair | {count} | {pct}% |
| 0-49 | Poor | {count} | {pct}% |

**Target Distribution:**

- Excellent: 50% (currently {pct}%, need {delta} docs)
- Good: 40% (currently {pct}%, {status})
- Fair: 10% (currently {pct}%, need {delta} docs)
- Poor: 0% (currently {pct}%, need {delta} docs)
```

**Target Benchmarks:**

- Excellent (90-100): 50% of docs
- Good (70-89): 40% of docs
- Fair (50-69): 10% of docs
- Poor (0-49): 0% of docs

### Next Steps Section

Concrete action plan:

```markdown
## Next Steps

1. **Immediate Actions:**
   - {action} ({target-doc})
   - {action} ({target-doc})

2. **This Week:**
   - {action} ({target-doc})
   - {action}

3. **This Month:**
   - {goal}
   - {goal}

---

**Report Generated:** {timestamp}
**Next Report:** {date} ({interval})
```

## Format: JSON

Generate machine-readable JSON for programmatic consumption or API
integration.

### Top-Level Structure

```json
{
  "metadata": {},
  "summary": {},
  "modules": [],
  "categories": [],
  "issues": {},
  "recommendations": {},
  "trends": {}
}
```

### Metadata Object

Report generation metadata:

```json
{
  "metadata": {
    "generated": "2026-01-17T10:30:00Z",
    "generator": "design-report",
    "version": "1.0",
    "modules": 3,
    "total_documents": 12,
    "include_archived": false
  }
}
```

### Summary Object

High-level aggregate metrics:

```json
{
  "summary": {
    "progress": {
      "total_coverage": 62,
      "average_completeness": 62,
      "documents_complete": 5,
      "documents_total": 12,
      "completion_rate": 42
    },
    "health": {
      "overall_score": 72,
      "rating": "good",
      "distribution": {
        "excellent": 3,
        "good": 5,
        "fair": 2,
        "poor": 2
      }
    },
    "status": {
      "current": 7,
      "draft": 3,
      "stub": 2,
      "needs_review": 0,
      "archived": 0
    }
  }
}
```

**Rating Mapping:**

- 90-100: "excellent"
- 70-89: "good"
- 50-69: "fair"
- 0-49: "poor"

### Modules Array

Per-module breakdown:

```json
{
  "modules": [
    {
      "name": "effect-type-registry",
      "path": ".claude/design/effect-type-registry",
      "document_count": 4,
      "health_score": 78,
      "rating": "good",
      "average_completeness": 68,
      "status_distribution": {
        "current": 3,
        "draft": 1,
        "stub": 0
      },
      "documents": [
        {
          "name": "observability.md",
          "path": ".claude/design/effect-type-registry/observability.md",
          "status": "current",
          "category": "observability",
          "completeness": 85,
          "health_score": 88,
          "rating": "excellent",
          "created": "2025-12-01",
          "updated": "2026-01-12",
          "last_synced": "2026-01-12",
          "age_days": 45,
          "updated_days_ago": 5,
          "synced_days_ago": 5,
          "relationships": {
            "related": 2,
            "dependencies": 1,
            "total": 3
          },
          "issues": []
        },
        {
          "name": "type-system.md",
          "status": "stub",
          "completeness": 5,
          "health_score": 12,
          "rating": "poor",
          "relationships": {
            "total": 0
          },
          "issues": [
            {
              "type": "orphaned",
              "severity": "critical",
              "description": "No relationships"
            },
            {
              "type": "low_completeness",
              "severity": "warning",
              "description": "Very low completeness for age"
            },
            {
              "type": "never_synced",
              "severity": "warning",
              "description": "Never synced with codebase"
            }
          ]
        }
      ],
      "module_issues": {
        "orphaned": 1,
        "never_synced": 2,
        "low_completeness": 1
      }
    }
  ]
}
```

### Categories Array

Cross-module category analysis:

```json
{
  "categories": [
    {
      "name": "architecture",
      "document_count": 5,
      "module_count": 3,
      "average_completeness": 76,
      "health_score": 81,
      "rating": "good",
      "coverage": [
        {
          "module": "effect-type-registry",
          "document": "architecture.md",
          "completeness": 90
        },
        {
          "module": "rspress-plugin-api-extractor",
          "document": "build-architecture.md",
          "completeness": 85
        }
      ]
    }
  ],
  "missing_categories": [
    {
      "name": "testing",
      "expected_in": ["rspress-plugin-api-extractor"]
    }
  ]
}
```

### Issues Object

Categorized issues with severity levels:

```json
{
  "issues": {
    "critical": [
      {
        "type": "orphaned",
        "count": 1,
        "documents": ["effect-type-registry/type-system.md"],
        "fix": "Add cross-references or archive",
        "priority": 1
      },
      {
        "type": "stale",
        "count": 1,
        "documents": [
          {
            "path": "rspress-plugin-api-extractor/legacy-api.md",
            "days_old": 120,
            "status": "current"
          }
        ],
        "fix": "Review for archival",
        "priority": 1
      }
    ],
    "warnings": [
      {
        "type": "never_synced",
        "count": 3,
        "documents": [
          "effect-type-registry/cache-optimization.md",
          "effect-type-registry/type-system.md",
          "design-doc-system/implementation-status.md"
        ],
        "fix": "Run /design-sync to verify accuracy",
        "priority": 1
      },
      {
        "type": "low_completeness_for_status",
        "count": 1,
        "documents": [
          {
            "path": "design-doc-system/user-documentation.md",
            "status": "current",
            "completeness": 65,
            "expected": 80
          }
        ],
        "fix": "Complete or change status to draft",
        "priority": 2
      }
    ],
    "info": [
      {
        "type": "missing_categories",
        "count": 2,
        "categories": ["testing", "integration"],
        "fix": "Create docs or remove from config",
        "priority": 3
      }
    ]
  }
}
```

**Issue Types:**

- **Critical**: orphaned, stale, broken_references
- **Warning**: never_synced, low_completeness_for_status, sync_lag
- **Info**: missing_categories, status_mismatch

### Recommendations Object

Prioritized action items:

```json
{
  "recommendations": {
    "priority_1": [
      {
        "action": "Resolve orphaned documents",
        "target": ["effect-type-registry/type-system.md"],
        "effort": "low",
        "impact": "high"
      },
      {
        "action": "Sync never-synced documents",
        "target": [
          "effect-type-registry/cache-optimization.md",
          "effect-type-registry/type-system.md",
          "design-doc-system/implementation-status.md"
        ],
        "effort": "low",
        "impact": "medium"
      }
    ],
    "priority_2": [
      {
        "action": "Complete draft documents",
        "target": [
          "effect-type-registry/cache-optimization.md",
          "design-doc-system/implementation-status.md"
        ],
        "effort": "medium",
        "impact": "medium"
      }
    ],
    "priority_3": [
      {
        "action": "Establish regular sync schedule",
        "effort": "low",
        "impact": "low"
      }
    ]
  }
}
```

### Trends Object

Historical comparison (if available):

```json
{
  "trends": {
    "previous_report": {
      "date": "2026-01-01",
      "total_documents": 10,
      "average_completeness": 58,
      "health_score": 68
    },
    "changes": {
      "documents_added": 2,
      "documents_removed": 0,
      "completeness_delta": 4,
      "health_delta": 4,
      "status_changes": {
        "current": 2
      }
    },
    "velocity": {
      "docs_per_month": 1.5,
      "estimated_months_to_80_percent": 3
    }
  }
}
```

## Format: HTML

Generate styled HTML report for viewing in browsers or sharing as standalone
file.

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Design Documentation Status Report</title>
  <style>
    /* Embedded styles */
  </style>
</head>
<body>
  <header><!-- Report title and metadata --></header>
  <main>
    <section class="summary"><!-- Executive summary --></section>
    <section class="modules"><!-- Module reports --></section>
    <section class="categories"><!-- Category coverage --></section>
    <section class="issues"><!-- Issues and recommendations --></section>
  </main>
  <footer><!-- Report metadata --></footer>
</body>
</html>
```

### CSS Styles

```css
body {
  font-family: system-ui, -apple-system, BlinkMacSystemFont,
    "Segoe UI", Roboto, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  line-height: 1.6;
  color: #333;
}

/* Health score colors */
.health-excellent { color: #28a745; }
.health-good { color: #5cb85c; }
.health-fair { color: #ffc107; }
.health-poor { color: #dc3545; }

/* Cards */
.metric-card {
  background: #f8f9fa;
  padding: 20px;
  margin: 10px 0;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Progress bars */
.progress-bar {
  background: #e9ecef;
  height: 24px;
  border-radius: 12px;
  overflow: hidden;
  position: relative;
}

.progress-fill {
  background: linear-gradient(90deg, #007bff, #0056b3);
  height: 100%;
  transition: width 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 14px;
}

/* Tables */
table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #dee2e6;
}

th {
  background: #f8f9fa;
  font-weight: 600;
  color: #495057;
}

tr:hover {
  background: #f8f9fa;
}

/* Issue badges */
.badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-critical { background: #dc3545; color: white; }
.badge-warning { background: #ffc107; color: #333; }
.badge-info { background: #17a2b8; color: white; }
```

### HTML Body Template

```html
<body>
  <header>
    <h1>Design Documentation Status Report</h1>
    <p class="metadata">
      Generated: <time>2026-01-17 10:30:00 UTC</time> |
      Modules: 3 |
      Total Documents: 12
    </p>
  </header>

  <main>
    <section class="summary">
      <h2>Executive Summary</h2>

      <div class="metric-card">
        <h3>Overall Health:
          <span class="health-good">72/100</span>
        </h3>
        <div class="progress-bar">
          <div class="progress-fill" style="width: 72%">72%</div>
        </div>
      </div>

      <div class="metrics-grid">
        <div class="metric-card">
          <h4>Total Coverage</h4>
          <div class="metric-value">62%</div>
          <div class="metric-detail">744 / 1200 points</div>
        </div>

        <div class="metric-card">
          <h4>Average Completeness</h4>
          <div class="metric-value">62%</div>
        </div>

        <div class="metric-card">
          <h4>Documents Complete</h4>
          <div class="metric-value">5/12</div>
          <div class="metric-detail">42%</div>
        </div>
      </div>
    </section>

    <section class="modules">
      <h2>Module Reports</h2>

      <article class="module">
        <h3>effect-type-registry</h3>
        <div class="module-stats">
          <span>Documents: 4</span>
          <span>Health: <strong class="health-good">78/100</strong></span>
          <span>Completeness: 68%</span>
        </div>

        <table class="documents">
          <thead>
            <tr>
              <th>Document</th>
              <th>Status</th>
              <th>Completeness</th>
              <th>Health</th>
              <th>Issues</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>observability.md</td>
              <td><span class="badge badge-current">Current</span></td>
              <td>85%</td>
              <td class="health-excellent">88</td>
              <td>—</td>
            </tr>
            <tr class="has-issues">
              <td>type-system.md</td>
              <td><span class="badge badge-stub">Stub</span></td>
              <td>5%</td>
              <td class="health-poor">12</td>
              <td>
                <span class="badge badge-critical">Orphaned</span>
                <span class="badge badge-warning">Never synced</span>
              </td>
            </tr>
          </tbody>
        </table>
      </article>
    </section>

    <section class="issues">
      <h2>Issues and Recommendations</h2>

      <div class="issue-category critical">
        <h3>
          <span class="badge badge-critical">Critical</span>
          Critical Issues (2)
        </h3>
        <ul>
          <li>
            <strong>Orphaned Documents</strong>
            <p>effect-type-registry/type-system.md</p>
            <p class="fix">Fix: Add cross-references or archive</p>
          </li>
        </ul>
      </div>

      <div class="recommendations">
        <h3>Priority 1 (This Week)</h3>
        <ol>
          <li>Resolve 2 orphaned documents</li>
          <li>Sync 3 never-synced documents</li>
        </ol>
      </div>
    </section>
  </main>

  <footer>
    <p>Report Generated: 2026-01-17 10:30:00 UTC</p>
    <p>Next Report: 2026-02-01</p>
  </footer>
</body>
```

## Format Selection

Choose format based on use case:

### Use Markdown When

- Reviewing in terminal or IDE
- Including in documentation repository
- Human-readable quick review
- Version control and diffs
- Sharing in Slack/Teams/GitHub

### Use JSON When

- Programmatic consumption
- API integration
- Dashboard visualization
- Automated reporting pipelines
- Storing historical snapshots
- Trend analysis scripts

### Use HTML When

- Sharing with stakeholders
- Presenting in meetings
- Email reports
- Archiving for reference
- Print-friendly format
- Standalone distribution

## Usage Examples

### Markdown to File

```bash
# Generate and save markdown report
/design-report > design-status-2026-01-17.md
```

### JSON to Dashboard

```bash
# Generate JSON and pipe to dashboard
/design-report --format=json | jq '.' | \
  curl -X POST https://dashboard/api/reports -d @-
```

### HTML for Email

```bash
# Generate HTML report for email
/design-report --format=html > report.html
# Attach report.html to email
```
