---
name: technical-documentation-query
description: Use this skill for querying technical documentation and researching frameworks or libraries.
---

# Technical Documentation Query Skill

This skill is designed for querying technical documentation to assist in the research of frameworks and libraries.

## Core Principle

> **Fact-based**: Rely on official documentation rather than outdated memory.

## Use Cases

| Scenario      | Example                          |
|---------------|----------------------------------|
| Framework Use | Best practices for React Hooks   |
| Library API   | Prisma query syntax              |
| Configuration | Vite configuration options       |
| Best Practices | TypeScript type tips            |

## Invocation

```javascript
deepwiki.query("React useEffect cleanup")
deepwiki.query("Prisma relation queries")
deepwiki.query("Next.js App Router")
```

## Timing of Use

### Innovation Phase (I)

```javascript
// Technical selection queries
deepwiki.query("Next.js vs Remix comparison") // Framework comparison
deepwiki.query("Zustand vs Jotai state management") // Library features
```

### Execution Phase (E)

```javascript
// Implementation queries
deepwiki.query("Prisma many-to-many relation") // Specific usage
deepwiki.query("Tailwind CSS custom colors") // Configuration parameters
```

## Best Practices

### ✅ Effective Queries

```javascript
deepwiki.query("Prisma many-to-many relation")  // Specific question
deepwiki.query("React 18 concurrent features")   // Version-related
```

### ❌ Queries to Avoid

```javascript
deepwiki.query("how to code")    // Too vague
deepwiki.query("best framework") // Subjective
```

## Fallback Plan

If `mcp-deepwiki` is unavailable → Perform a web search for official documentation.