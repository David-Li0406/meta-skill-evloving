---
name: mcp-integration
description: "Use when working with MCP servers for enhanced capabilities like documentation retrieval, database access, or specialized tools. Triggers - mcp, context7, documentation lookup, external docs."
---

# MCP Integration Patterns

**Iron Law:** MCP servers extend Claude's capabilities. Use them for specialized tasks they're designed for.

## Overview

Model Context Protocol (MCP) servers provide Claude Code with extended capabilities beyond built-in tools. Common MCP servers include:

- **Context7** - Documentation retrieval with vectorized search
- **Supabase** - Database operations and management
- **Playwright** - Browser automation for testing
- **Custom servers** - Project-specific integrations

## When to Use MCP Servers

### Use Context7/Documentation MCPs for:
- Framework/library documentation lookup
- Best practices for specific technologies
- API reference queries
- Pattern examples from official docs

### Use Database MCPs (Supabase, etc.) for:
- Direct database queries
- Schema inspection
- Data operations
- Migration management

### Use Browser MCPs (Playwright, etc.) for:
- E2E testing
- UI automation
- Visual validation
- Screenshot capture

## Context7 Integration Pattern

Context7 provides superior results for development documentation through vectorization and RAG.

### Research Workflow

```markdown
## Context7-First Research Protocol

1. **Attempt Context7 First** - Always try Context7 before WebSearch for docs
2. **Evaluate Results** - Assess completeness, accuracy, relevance
3. **Decision Matrix**:
   - **Context7 Success**: Use as primary source
   - **Context7 Partial**: Combine with WebSearch
   - **Context7 Failure**: Fall back to WebSearch
   - **Context7 Unavailable**: Use WebSearch with notification
```

### Query Optimization

**Good Context7 queries:**
- "Next.js 15 authentication implementation patterns"
- "React Server Components data fetching best practices"
- "Supabase RLS policy examples for multi-tenant apps"

**Less effective queries:**
- "How to code" (too vague)
- "Latest news about React" (not documentation)

### Fallback Strategy

```markdown
## Fallback Decision Tree

1. Context7 query returns results
   → Evaluate: Complete? Current? Relevant?
   → Yes to all → Use Context7 results
   → Partial → Supplement with WebSearch

2. Context7 returns no/poor results
   → Log: "Context7 insufficient for [query]"
   → Fallback: WebSearch with specific terms
   → Note: Retry Context7 for follow-up queries

3. Context7 unavailable
   → Notify: "Context7 unavailable, using WebSearch"
   → Proceed: Full WebSearch workflow
   → Retry: Attempt Context7 next query
```

## Checking MCP Availability

Before relying on an MCP server:

```markdown
## MCP Server Check

**Available MCPs in this session:**
[List active MCP servers from tool list]

**For this task, using:**
- [ ] Context7 for documentation
- [ ] Supabase for database operations
- [ ] Playwright for browser testing
- [ ] Other: [specify]

**If MCP unavailable:**
- Document the limitation
- Use alternative approach
- Note impact on task quality
```

## Integration with Agents

### Deep Researcher + Context7

When the deep-researcher agent is invoked:

1. Check if Context7 MCP is available
2. Use Context7 as PRIMARY documentation source
3. Supplement with WebSearch for:
   - Recent developments (< 30 days)
   - Community discussions
   - Real-world implementation examples
4. Document source attribution

### Database Operations + Supabase MCP

When database work is needed:

1. Check if Supabase MCP is available
2. Use MCP tools for direct operations
3. Fall back to SQL files if MCP unavailable
4. Document which method was used

## Error Handling

### MCP Connection Issues

```markdown
## Error: MCP Connection Failed

**Symptom**: MCP tool calls return errors/timeouts

**Response**:
1. Note: "MCP [name] connection issue"
2. Fallback: Use alternative method
3. Continue: Don't block on MCP availability
4. Retry: Attempt MCP again for next operation
```

### Partial Results

```markdown
## Handling Partial MCP Results

**Symptom**: MCP returns incomplete information

**Response**:
1. Use what's available as foundation
2. Supplement with other sources
3. Note gaps in documentation
4. Provide best-effort response
```

## Best Practices

### DO:
- Check MCP availability before planning MCP-dependent tasks
- Use specific, targeted queries for best results
- Document when MCPs are used vs fallbacks
- Combine MCP results with other sources when appropriate

### DON'T:
- Assume MCPs are always available
- Block task completion on MCP availability
- Use MCPs for tasks they're not designed for
- Skip fallback planning

## Configuration

### Project-Level MCP Configuration

In `CLAUDE.md` or `.claude/settings.json`:

```json
{
  "mcp": {
    "preferredServers": {
      "documentation": "context7",
      "database": "supabase",
      "testing": "playwright"
    },
    "fallbackBehavior": "notify-and-continue",
    "cacheResults": true
  }
}
```

### MCP Server Settings

Each MCP server may have project-specific configuration. Check:
- Server-specific configuration files
- Environment variables
- Connection settings

## Practical Examples

### Example 1: Looking Up React Hook Documentation

```
User: "How do I use useCallback correctly?"

1. Check: Context7 MCP available? Yes
2. Query Context7: "React useCallback hook usage patterns"
3. Result: Returns official React docs with examples
4. Action: Use Context7 results directly
5. Output: Explain useCallback with official examples
```

### Example 2: Supabase RLS Research

```
User: "What's the best way to set up RLS for multi-tenant?"

1. Check: Context7 available? Yes
2. Query Context7: "Supabase RLS multi-tenant patterns"
3. Result: Partial - has basics but not multi-tenant specifics
4. Action: Supplement with WebSearch for "supabase multi-tenant RLS 2024"
5. Output: Combine Context7 foundations with WebSearch examples
```

### Example 3: MCP Unavailable

```
User: "Find Next.js 15 middleware docs"

1. Check: Context7 available? No (not in tool list)
2. Notify: "Context7 not available, using WebSearch"
3. WebSearch: "Next.js 15 middleware documentation"
4. Output: Provide docs from WebSearch results
```

### Example 4: Database Operations with Supabase MCP

```
User: "Check the users table schema"

1. Check: Supabase MCP available? Yes
2. Action: Use mcp__supabase__query to inspect schema
3. Result: Returns table structure
4. Output: Display schema with column types
```

### Example 5: E2E Testing with Playwright MCP

```
User: "Test the login flow"

1. Check: Playwright MCP available? Yes
2. Action: Use mcp__playwright tools to:
   - Navigate to login page
   - Fill credentials
   - Submit form
   - Verify redirect
3. Output: Report test results with screenshots
```

## Quick Reference

```
MCP WORKFLOW:
1. Check availability
2. Use if available, fallback if not
3. Document which path taken
4. Continue without blocking

CONTEXT7 FIRST:
Documentation query → Context7 → Evaluate → WebSearch if needed

ALWAYS:
- Plan for fallback
- Document MCP usage
- Don't block on MCP

NEVER:
- Assume MCP available
- Skip fallback planning
- Fail task because MCP unavailable
```

## Integration

**Pairs with:**
- **deep-researcher** - Context7 for documentation research
- **supabase-patterns** - Supabase MCP for database
- **testing-patterns** - Playwright MCP for browser tests
