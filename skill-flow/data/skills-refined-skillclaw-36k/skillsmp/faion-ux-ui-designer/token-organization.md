# Token Organization

### Problem

Token bloat reduces discoverability and defeats the purpose of systematization.

### Solution: Structured Token Architecture

**Hierarchy:**
```
Primitives (raw values)
    ↓
Semantic tokens (purpose-based)
    ↓
Component tokens (component-specific, use sparingly)
```

**Best Practices:**

| Practice | Description |
|----------|-------------|
| Start lean | MVP mindset, not waterfall |
| Avoid bloat | Don't create token for every variation |
| Clear naming | `color.surface.primary` not `blue-1` |
| Document purpose | Why this token exists |
| Version control | Track changes over time |

**Token Naming Convention:**
```
{category}.{property}.{variant}.{state}

Examples:
color.background.primary
color.background.primary.hover
spacing.component.button
typography.heading.xl
```
