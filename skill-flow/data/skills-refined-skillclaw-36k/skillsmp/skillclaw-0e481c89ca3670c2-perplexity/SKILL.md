---
name: perplexity
description: Use this skill when you need to perform web searches or research using Perplexity AI, especially for generic queries like "search", "find", or "ask".
---

# Perplexity Tools

Use ONLY when the user says "search", "find", "look up", "ask", "research", or "what's the latest" for generic queries. Do NOT use for library/framework documentation (use Context7), Graphite CLI (use Graphite MCP), or workspace questions (use Nx MCP).

## Quick Reference

**Which Perplexity tool?**
- Need search results/URLs? → **Perplexity Search**
- Need conversational answer? → **Perplexity Ask**
- Need deep research? → **Researcher agent** (`/research <topic>`)

**NOT Perplexity - use these instead:**
- Library/framework docs → **Context7 MCP**
- Graphite `gt` CLI → **Graphite MCP**
- THIS workspace → **Nx MCP**
- Specific URL → **URL Crawler**

## Perplexity Search

**When to use:**
- For generic searches, finding resources
- To discover current best practices or recent information
- For tutorial/blog post discovery
- When the user says "search for...", "find...", or "look up..."

**Default parameters (ALWAYS USE):**
```typescript
mcp__perplexity__perplexity_search({
  query: "your search query",
  max_results: 3,           // Default is 10 - too many!
  max_tokens_per_page: 512  // Reduce per-result content
})
```

**When to increase limits:**
Only if:
- The user explicitly needs comprehensive results
- The initial search found nothing useful
- The topic is complex and requires multiple sources

```typescript
// Increased limits (use sparingly)
mcp__perplexity__perplexity_search({
  query: "complex topic",
  max_results: 5,
  max_tokens_per_page: 1024
})
```

## Perplexity Ask

**When to use:**
- When a conversational explanation is needed, not just search results
- To synthesize information from the web
- To explain concepts with current context

**Usage:**
```typescript
mcp__perplexity__perplexity_ask({
  messages: [
    {
      role: "user",
      content: "Explain how postgres advisory locks work"
    }
  ]
})
```

**NOT for:**
- Library documentation (use Context7)
- Deep multi-source research (use researcher agent)

## Prohibited Tool

**NEVER use:** `mcp__perplexity__perplexity_research`

**Use instead:** Researcher agent (`/research <topic>`)
- Token cost: 30-50k tokens
- Provides multi-source synthesis with citations
- Use sparingly for complex questions only

## Tool Selection Chain

**Priority order:**
1. **Context7 MCP** - Library/framework docs
2. **Graphite MCP**