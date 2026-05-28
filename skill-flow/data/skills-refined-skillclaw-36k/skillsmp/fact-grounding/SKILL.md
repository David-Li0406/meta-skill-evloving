---
name: fact-grounding
description: "Use when you need current, accurate information from the web - verifying claims, researching unfamiliar topics, looking up error codes, or when LLM training data may be outdated or insufficient. Selects appropriate Perplexity tool based on depth needed."
---

# Fact-Grounding with External Sources

## Overview

Ground responses in verified, current information rather than relying solely on LLM knowledge. Use Perplexity MCP tools to search the web for facts.

**Core principle:** When in doubt, verify. When outdated, search. When complex, research.

## When to Use

### Error Resolution
- **Error codes/messages** - Look up specific error codes to find working solutions
- **Stack traces** - Search for others who encountered the same issue
- **Deprecation warnings** - Find migration guides and updated approaches

### Exploration & Discovery
- **New territory** - Exploring unfamiliar frameworks, APIs, or domains
- **What's possible** - Finding what others have tried, patterns that work
- **Best practices** - Current recommendations (not outdated training data)

### Verification
- **API signatures** - Verify current method signatures, parameters
- **Version compatibility** - Check which versions work together
- **Pricing/limits** - Current pricing, rate limits, quotas
- **Release status** - Is feature X stable? When was Y released?

### Currency
- **Recent releases** - Features in versions released after training cutoff
- **Current events** - News, announcements, breaking changes
- **Documentation changes** - APIs evolve, docs update

## Tool Selection (by depth)

| Need | Tool | Use Case |
|------|------|----------|
| **Quick answer** | `perplexity_ask` | Single factual question, error code lookup, conversational follow-up |
| **Find sources** | `perplexity_search` | Multiple sources needed, comparing solutions, finding alternatives |
| **Deep dive** | `perplexity_research` | Complex topic, synthesized analysis with citations, exploring new ground |

## The Process

1. **Recognize the trigger** - Is this something I should verify externally?
2. **Select depth** - Quick answer, source search, or deep research?
3. **Formulate query** - Clear, specific, searchable
4. **Execute search** - Use appropriate Perplexity tool
5. **Synthesize results** - Present findings with source attribution
6. **Acknowledge limitations** - Note if information is incomplete or conflicting

## Query Formulation Tips

### For Error Lookups
- Include the **exact error message** or code
- Add **technology context**: framework, version, platform
- Example: `"ECONNREFUSED 127.0.0.1:5432" PostgreSQL Docker Windows`

### For Exploration
- Be specific about **what you're trying to achieve**
- Include **constraints**: language, framework, requirements
- Example: `"real-time collaboration React alternatives to Yjs 2024"`

### For Verification
- Include **version numbers** when relevant
- Ask for **current** or **latest** explicitly
- Example: `"Next.js 14 app router middleware current syntax"`

### Poor Queries (avoid)
- Vague: "best framework"
- Opinion-seeking: "should I use React"
- Too broad: "how does authentication work"

## Examples

### Error Code Lookup
```
Query: "CS8602 possible null reference" C# nullable reference types fix
Tool: perplexity_ask
```

### Exploring Possibilities
```
Query: "PDF generation libraries .NET 8 comparison 2024" features pricing
Tool: perplexity_search
```

### Deep Research
```
Query: "implementing event sourcing with Azure Cosmos DB" patterns pitfalls production
Tool: perplexity_research
```

## Red Flags

- **Presenting outdated info as current** - Always verify versions, dates, pricing
- **Skipping verification for technical claims** - API signatures, library features change
- **Not citing sources** - When using researched info, attribute it
- **Over-researching simple facts** - Use `perplexity_ask` for quick answers
- **Under-researching complex topics** - Use `perplexity_research` for deep dives

## Integration

Related workflows (shortcuts for specific depths):
- `/ask` - Quick questions (uses `perplexity_ask`)
- `/search` - Find sources (uses `perplexity_search`)
- `/research` - Deep investigation (uses `perplexity_research`)

Invoke with `@fact-grounding` when you need guidance on which approach to use.
