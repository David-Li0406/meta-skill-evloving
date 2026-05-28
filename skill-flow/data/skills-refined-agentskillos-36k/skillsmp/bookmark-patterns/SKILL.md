---
name: bookmark-patterns
description: Teaches Bookmark Vault coding patterns. Use when asking about best practices, patterns, or how to implement features in the bookmark app.
---

# Bookmark Vault Patterns

Quick navigation to Bookmark Vault coding patterns and best practices.

## Pattern Categories

- **Component patterns** → [component-patterns.md](reference/component-patterns.md)
- **Hook patterns** → [hook-patterns.md](reference/hook-patterns.md)
- **Storage patterns** → [storage-patterns.md](reference/storage-patterns.md)

## Examples

- **Good examples** → [good-examples.md](examples/good-examples.md)
- **Anti-patterns to avoid** → [anti-patterns.md](examples/anti-patterns.md)

## Quick Tips

1. Always use `"use client"` for components touching `localStorage`/`sessionStorage`
2. Validate with Zod before saving to storage
3. Keep components under 100 lines (split larger features)
4. Use Context + reducer for cross-component state, Zustand for singleton stores
5. Handle loading/empty states in list components
6. Use optimistic UI for mutations (add immediately, resolve after server)

## When to Use This Skill

- "What's the pattern for X in bookmark vault?"
- "How do I implement a bookmark form?"
- "Show me examples of good component structure"
- "What anti-patterns should I avoid?"
