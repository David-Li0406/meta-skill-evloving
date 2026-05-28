# CLI Commands

Export, import, and search commands for managing learning patterns.

## Export Patterns

Share learnings between projects:

```bash
# Export all patterns
jikime-adk learnings export --output learnings-export.yaml

# Export specific category
jikime-adk learnings export --category workaround --output workarounds.yaml

# Export high-confidence only
jikime-adk learnings export --min-confidence 0.85 --output reliable-patterns.yaml
```

## Import Patterns

```bash
# Import from another project
jikime-adk learnings import --source ../other-project/.jikime/learnings/

# Import with merge strategy
jikime-adk learnings import --source patterns.yaml --strategy merge

# Import with confidence adjustment
jikime-adk learnings import --source patterns.yaml --confidence-penalty 0.1
```

## Export Format

```yaml
export_version: "1.0"
exported_at: "2024-01-22T15:30:00Z"
source_project: "auth-service"
patterns:
  - id: "wk-nextjs-001"
    category: "workaround"
    confidence: 0.93
    pattern:
      technology: "Next.js 14"
      issue: "Dynamic routes with middleware"
      solution: "..."
    metadata:
      created: "2024-01-15"
      frequency: 8
```

---

## Searching Patterns

Query stored patterns:

```bash
# Search by keyword
jikime-adk learnings search "useState"

# Search by category
jikime-adk learnings search --category workaround

# Search by technology
jikime-adk learnings search --tech nextjs

# Full-text search
jikime-adk learnings search "hydration mismatch react"
```

### Search Output Example

```markdown
## Search Results: "hydration mismatch"

### 1. React Hydration Mismatch Fix
**Category**: error_resolution
**Confidence**: 0.91
**Frequency**: 7

**Pattern**:
When encountering hydration mismatch in Next.js:
1. Check for browser-only APIs (window, localStorage)
2. Use useEffect for client-side only code
3. Consider dynamic import with ssr: false

### 2. Dynamic Import Workaround
**Category**: workaround
**Confidence**: 0.88
**Frequency**: 5

**Pattern**:
```jsx
import dynamic from 'next/dynamic'
const Component = dynamic(() => import('./Component'), { ssr: false })
```
```

---

Version: 1.0.0
Source: jikime-workflow-learning SKILL.md
