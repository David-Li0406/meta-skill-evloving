---
name: docs-seeker
description: Find documentation using llms.txt standard, context7.com, and repomix. Best practices for library research.
---

# Docs Seeker

> **Load this skill** when you need to find documentation for libraries, frameworks, or APIs.

## Documentation Sources (Priority Order)

### 1. Context7 (llms.txt aggregator) - TRY FIRST

```
# Use the context7 MCP tool
context7_resolve_library_id(libraryName="next.js")
context7_get_library_docs(libraryId="...", topic="app router")
```

**Supported libraries:** Next.js, React, shadcn/ui, Tailwind CSS, Better Auth, Drizzle ORM, and many more.

**Why first:** Aggregates llms.txt files from official sources, AI-optimized format.

---

### 2. Official Documentation Sites

If context7 doesn't have it:

```
# Use webfetch for official docs
webfetch(url="https://docs.example.com/api/reference")
```

**Best sources:**
- GitHub README.md
- Official docs site
- API reference pages

---

### 3. Repomix (GitHub Repo Analysis)

For understanding library internals:

```bash
# Package entire repo for analysis
npx repomix --remote https://github.com/owner/repo --output repo.xml
```

**Use when:**
- Need to understand internal implementation
- Docs are incomplete
- Looking for usage examples in source

---

## Search Strategy

### For Framework/Library Usage

```
1. context7 → resolve library ID
2. context7 → get docs for specific topic
3. If incomplete → webfetch official docs
4. If still unclear → repomix the source
```

### For API/SDK Integration

```
1. webfetch → API reference page
2. Look for: endpoints, auth, rate limits
3. Find code examples
4. Test with minimal example first
```

### For Error Messages

```
1. grep_app → search GitHub for exact error
2. Look for: issues, discussions, PRs
3. Find the fix or workaround
4. Verify solution applies to your version
```

---

## llms.txt Standard

Many sites now provide `/llms.txt` files optimized for AI:

```
# Check for llms.txt
webfetch(url="https://example.com/llms.txt")
```

**Format:** Markdown with structured sections for AI consumption.

**Growing adoption:** Next.js, Vercel, Anthropic, and more.

---

## Best Practices

### DO

- ✅ Check context7 first (fastest, most reliable)
- ✅ Get specific: "Next.js app router dynamic routes" not "Next.js"
- ✅ Verify version compatibility
- ✅ Look for code examples, not just prose
- ✅ Test examples before using in production

### DON'T

- ❌ Rely on memory for API details
- ❌ Use outdated Stack Overflow answers
- ❌ Copy code without understanding it
- ❌ Skip version checks (APIs change!)
- ❌ Assume docs are complete

---

## Quick Reference

| Need | Tool | Example |
|------|------|---------|
| Library docs | context7 | `context7_get_library_docs("react", "hooks")` |
| API reference | webfetch | `webfetch("https://api.example.com/docs")` |
| GitHub search | grep_app | `grep_app("error message")` |
| Source analysis | repomix | `npx repomix --remote url` |

---

## Parallel Research Pattern

For comprehensive research, fire multiple agents:

```
task(agent="researcher", prompt="Find Next.js app router docs via context7")
task(agent="researcher", prompt="Find authentication patterns for Next.js")
task(agent="explore", prompt="Find how auth is implemented in this codebase")
```

Combine external docs with internal patterns for best results.
