# Design Index Templates

Index templates for different output formats and detail levels.

## Markdown Templates

### Minimal Template

Brief listing with links:

```markdown
# Design Docs

- [Observability](./observability.md) - 85% complete
- [Cache Optimization](./cache-optimization.md) - 90% complete
- [Architecture](./architecture.md) - 70% complete
```

### Standard Template

With metadata and summaries:

```markdown
# Design Documentation Index

## Architecture

### [Observability System](./observability.md)

**Status:** current | **Completeness:** 85% | **Updated:** 2026-01-17

Event-based observability architecture.
```

### Detailed Template

With sections and statistics:

```markdown
# Design Documentation Index

## Architecture

### [Observability System](./observability.md)

**Metadata:**

- Status: current
- Completeness: 85%
- Created: 2026-01-15
- Updated: 2026-01-17

**Summary:**

Event-based observability architecture for tracking package fetching.

**Sections:**

1. Overview
2. Current State
3. Event System Architecture
4. Future Enhancements

**Statistics:**

- 456 lines
- 5 sections
- 12 code blocks
```

## HTML Template

Full HTML navigation with embedded CSS:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Design Documentation Index - {module}</title>
    <style>
        body {
            font-family: system-ui, -apple-system, sans-serif;
            max-width: 1200px;
            margin: 2rem auto;
            padding: 0 1rem;
        }
        .header {
            border-bottom: 2px solid #e1e4e8;
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }
        .category { margin-bottom: 2rem; }
        .category h2 {
            color: #0366d6;
            border-bottom: 1px solid #e1e4e8;
            padding-bottom: 0.5rem;
        }
        .doc-card {
            background: #f6f8fa;
            border-radius: 6px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .doc-title { font-size: 1.25rem; margin-bottom: 0.5rem; }
        .doc-title a { color: #24292e; text-decoration: none; }
        .doc-title a:hover { text-decoration: underline; }
        .doc-meta {
            color: #586069;
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
        }
        .doc-summary { color: #24292e; line-height: 1.5; }
        .badge {
            display: inline-block;
            padding: 0.25rem 0.5rem;
            border-radius: 3px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-right: 0.5rem;
        }
        .badge-current { background: #28a745; color: white; }
        .badge-draft { background: #ffd33d; color: #24292e; }
        .badge-stub { background: #6c757d; color: white; }
        .stats {
            background: #f6f8fa;
            border-radius: 6px;
            padding: 1rem;
            margin-top: 2rem;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Design Documentation Index</h1>
        <p>
            <strong>Module:</strong> {module} |
            <strong>Documents:</strong> {count} |
            <strong>Updated:</strong> {date}
        </p>
    </div>

    <div class="category">
        <h2>{category}</h2>

        <div class="doc-card">
            <div class="doc-title">
                <a href="./{file}">{title}</a>
            </div>
            <div class="doc-meta">
                <span class="badge badge-{status}">{status}</span>
                <span>{completeness}% complete</span> |
                <span>Updated {date}</span>
            </div>
            <div class="doc-summary">
                {summary}
            </div>
        </div>
    </div>

    <div class="stats">
        <h3>Statistics</h3>
        <ul>
            <li>Total documents: {count}</li>
            <li>Current: {current}</li>
            <li>Draft: {draft}</li>
            <li>Average completeness: {avg}%</li>
        </ul>
    </div>

    <footer style="margin-top: 2rem; padding-top: 1rem;
        border-top: 1px solid #e1e4e8; color: #586069;
        font-size: 0.875rem;">
        Generated {timestamp} by design-index skill
    </footer>
</body>
</html>
```

## JSON Template

Structured JSON output:

```json
{
  "module": "effect-type-registry",
  "generated": "2026-01-17T15:30:00Z",
  "organization": "category",
  "statistics": {
    "total": 4,
    "by_status": {
      "current": 2,
      "draft": 1,
      "stub": 1
    },
    "average_completeness": 78
  },
  "categories": {
    "architecture": [
      {
        "title": "Observability System",
        "file": "observability.md",
        "path": ".claude/design/effect-type-registry/observability.md",
        "status": "current",
        "category": "architecture",
        "completeness": 85,
        "created": "2026-01-15",
        "updated": "2026-01-17",
        "summary": "Event-based observability architecture",
        "sections": [
          "Overview",
          "Current State",
          "Event System Architecture",
          "Rationale",
          "Future Enhancements"
        ],
        "statistics": {
          "lines": 456,
          "words": 3200,
          "sections": 5,
          "code_blocks": 12
        }
      }
    ]
  }
}
```

## Statistics Templates

### Status Distribution

```markdown
## Documentation Health

### Status Distribution

- ✅ **Current (production):** 2 docs (50%)
- 🔄 **Draft (in progress):** 1 doc (25%)
- 📝 **Stub (planned):** 1 doc (25%)
- 📦 **Archived:** 0 docs (0%)
```

### Completeness Metrics

```markdown
### Completeness

- **Average:** 78%
- **Highest:** cache-optimization.md (90%)
- **Lowest:** new-feature.md (15%)
- **Needs attention:** 1 doc < 50% complete
```

### Recent Activity

```markdown
### Recent Activity

- **Updated today:** 1 doc
- **Updated this week:** 3 docs
- **Stale (>30 days):** 0 docs
```

### Coverage by Category

```markdown
### Coverage by Category

- **Architecture:** 2 docs
- **Performance:** 1 doc
- **Observability:** 1 doc
```
