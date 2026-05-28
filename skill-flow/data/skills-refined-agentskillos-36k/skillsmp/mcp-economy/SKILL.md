---
name: mcp-economy
description: Enforce cost-aware MCP usage. Use when a task might trigger heavy external tools, web search, or broad context expansion. Prevents token burn by ensuring MCPs are only used when local context is insufficient.
---

# MCP Economy Skill

## Purpose

Reduce token burn by ensuring MCP tools are only used when local context is insufficient. This skill provides explicit guidance on when to use external tools and when to avoid them.

## Why This Matters

MCP tools add tokens to context quickly. Some servers (like GitHub or broad web search) can add thousands of tokens per call. This skill helps you:
- Preserve context window for actual work
- Reduce API costs
- Avoid unnecessary external calls
- Make deliberate, cost-aware decisions

---

## Core Rules

### Rule 1: Default to Local
Always try local reasoning and available files first. Most tasks can be solved with:
- Files already in context
- Previous conversation history
- Built-in knowledge

### Rule 2: MCPs Only When Needed
Use MCPs only when local context is missing or ambiguous:
- Missing documentation for a library
- Need to find code patterns across GitHub
- User explicitly asks for web/external research

### Rule 3: Prefer Lightweight MCPs
Use this priority order:
1. **context7** - Docs lookup (low cost, high utility)
2. **grep_app** - GitHub code search (medium cost, targeted)
3. **zai-zread** - Repo structure/docs (medium cost)
4. **exa/zai-search** - Web search (higher cost, use sparingly)

### Rule 4: Cap Expensive Queries
- **exa/web search:** 1-2 queries per task unless user explicitly asks for more
- **GitHub search:** Narrow scope first, broaden only if needed
- **Notion/Linear:** Query only what's needed, avoid broad fetches

### Rule 5: Summarize and Stop
When you use an MCP:
- Extract only the relevant information
- Summarize findings succinctly
- Don't chain multiple MCP calls unless necessary

---

## Decision Checklist

Before using an MCP, ask yourself:

```
[ ] Do I already have the answer locally?
[ ] Can I solve this with files already in context?
[ ] Is a small doc lookup (context7) enough?
[ ] Is GitHub code search specifically required?
[ ] Does the user explicitly ask for web discovery?
[ ] Have I already used my MCP budget for this task?
```

If you answer "yes" to the first two questions, **do not use an MCP**.

---

## Token Budget Guidelines

| MCP | Typical Cost | Budget Per Task |
|-----|-------------|-----------------|
| context7 | ~500-1500 tokens | 2-3 calls |
| grep_app | ~1000-3000 tokens | 1-2 calls |
| zai-zread | ~1000-2000 tokens | 1-2 calls |
| exa/web search | ~2000-5000 tokens | 1 call |
| linear/notion | ~500-2000 tokens | As needed |

**Total external budget per task:** ~5000-10000 tokens unless user explicitly approves more.

---

## When to Use Each MCP

### context7 (Docs Lookup)
**Use when:**
- Need API documentation for a library
- Looking up function signatures
- Understanding library concepts

**Avoid when:**
- You already know the API
- The library is well-known (lodash, react, etc.)
- Information is in project files

### grep_app (GitHub Search)
**Use when:**
- Looking for real-world usage patterns
- Finding how others solved a specific problem
- Researching open-source implementations

**Avoid when:**
- The pattern is obvious
- Local codebase has examples
- User hasn't asked for external research

### exa/zai-search (Web Search)
**Use when:**
- User explicitly asks for web research
- Documentation is missing or outdated
- Need recent/current information

**Avoid when:**
- context7 or grep_app can answer
- The question is about code (use grep_app instead)
- Local context is sufficient

### linear/notion (Project Management)
**Use when:**
- User asks about tickets/issues
- Need to create/update project items
- Looking up project documentation

**Avoid when:**
- Just coding tasks
- User hasn't mentioned project management

---

## Anti-Patterns (Avoid These)

### Token Burner Patterns
- Using web search for every question
- Chaining multiple MCP calls without summarizing
- Fetching entire repos when you only need one file
- Running broad searches before trying narrow ones

### Lazy Patterns
- Using MCP instead of thinking through the problem
- Fetching docs for libraries you already know
- Searching GitHub for trivial patterns

### Overkill Patterns
- Using exa when context7 would suffice
- Running multiple searches for the same concept
- Fetching full Notion databases when you need one page

---

## Examples

### Good: Minimal MCP Usage
```
User: "How do I use zod for form validation?"

Thought: I know zod well. Let me check if there's a specific pattern
the user wants, or if my knowledge is sufficient.

Action: Answer from knowledge first. If user needs specifics,
use context7 for zod docs (1 call max).
```

### Good: Targeted Search
```
User: "Find how other projects handle rate limiting in Express"

Thought: This requires external research. Use grep_app with
a narrow query.

Action: grep_app search for "express rate limit middleware" (1 call)
Summarize top 2-3 patterns found.
```

### Bad: Token Burning
```
User: "How do I use lodash?"

Bad Action: 
1. exa search for "lodash tutorial" 
2. context7 lookup for lodash
3. grep_app search for "lodash usage patterns"

This burns ~8000+ tokens for something you already know.
```

---

## Quick Reference

| Situation | Action |
|-----------|--------|
| Know the answer | Don't use MCP |
| Need library docs | context7 (1 call) |
| Need code patterns | grep_app (1 call) |
| User asks for web research | exa (1 call max) |
| Need project info | linear/notion (as needed) |
| Unsure if MCP needed | Default to no; ask user if critical |

---

## Summary

1. **Local first** - Most answers are already available
2. **Lightweight MCPs** - context7 > grep_app > exa
3. **Budget conscious** - Cap expensive calls
4. **Summarize** - Extract what you need, don't chain
5. **Ask if unsure** - User can approve more MCP usage

**Default stance:** Do not use MCPs unless clearly necessary.
