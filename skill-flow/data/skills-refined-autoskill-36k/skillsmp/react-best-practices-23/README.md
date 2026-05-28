# React Best Practices

Performance optimization guidelines for React and Next.js applications.

## Structure

- `SKILL.md` - Entry point (Claude reads this first)
- `rules/` - Individual rule files for deep-dives
- `metadata.json` - Version info

## Rule Categories

| Priority | Category                  | Prefix       |
| -------- | ------------------------- | ------------ |
| 1        | Eliminating Waterfalls    | `async-`     |
| 2        | Bundle Size Optimization  | `bundle-`    |
| 3        | Server-Side Performance   | `server-`    |
| 4        | Client-Side Data Fetching | `client-`    |
| 5        | Re-render Optimization    | `rerender-`  |
| 6        | Rendering Performance     | `rendering-` |
| 7        | JavaScript Performance    | `js-`        |
| 8        | Advanced Patterns         | `advanced-`  |

## Impact Levels

- `CRITICAL` - Major performance gains
- `HIGH` - Significant improvements
- `MEDIUM-HIGH` - Moderate-high gains
- `MEDIUM` - Moderate improvements
- `LOW-MEDIUM` - Low-medium gains
- `LOW` - Incremental improvements

## Creating New Rules

To add a new rule:

1. Follow the structure in `rules/_template.md`
2. Use the correct prefix from `rules/_sections.md`
3. Save as `rules/{prefix}-{description}.md`
