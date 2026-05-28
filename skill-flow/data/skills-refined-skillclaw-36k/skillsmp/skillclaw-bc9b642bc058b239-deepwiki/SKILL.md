---
name: deepwiki
description: Use this skill when you need to query technical documentation for frameworks and libraries.
---

# Skill body

## Core Principle

> **Fact-based**: Rely on official documentation, avoiding outdated memories.

## Use Cases

| Scenario      | Example                          |
|---------------|----------------------------------|
| Framework Use | Best practices for React Hooks   |
| Library API   | Prisma query syntax              |
| Configuration  | Vite configuration options       |
| Best Practices | TypeScript type tips             |

## Invocation

```javascript
deepwiki.query("React useEffect cleanup")
deepwiki.query("Prisma relation queries")
deepwiki.query("Next.js App Router")
```

## Timing of Use

### I Phase (Innovation)
```javascript
// Technical selection queries
deepwiki.query("Next.js vs Remix comparison") // Framework comparison
deepwiki.query("Zustand vs Jotai state management") // Library features
```

### E Phase (Execution)
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

If mcp-deepwiki is unavailable → Search official documentation online.