---
name: cloudflare-guide
description: Use this skill when the user asks about "Cloudflare Workers", "Cloudflare Pages", "Wrangler configuration", "R2", "D1", "KV", "Durable Objects", "Workers AI", or any Cloudflare deployment/development question. It uses the cloudflare-docs-fetcher agent to fetch official documentation, keeping the main context clean.
version: 1.0.0
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---

# Cloudflare Development Assistant

## Core Principle

**Use the `cloudflare-docs-fetcher` agent to fetch and analyze official Cloudflare documentation.**

This keeps the main conversation context clean while ensuring answers are based on the latest official documentation.

## How to Use

When a user asks a Cloudflare-related question, spawn the `cloudflare-docs-fetcher` agent:

```
Task(
  subagent_type: "general-purpose",
  description: "Fetch Cloudflare docs for [brief topic]",
  prompt: "User question: [THE EXACT USER QUESTION]"
)
```

The agent will:
1. Determine which official docs URL to fetch
2. Fetch and analyze the documentation
3. Return a concise answer with exact syntax from the docs

## When to Trigger

Trigger this skill when the user mentions:
- **Workers**: runtime, handlers, bindings, Wrangler
- **Pages**: deployment, build config, Pages Functions
- **Storage**: R2, D1, KV, Durable Objects, Queues
- **AI**: Workers AI, AI Gateway, Agents SDK, Vectorize
- **Config**: `wrangler.toml`, `wrangler.jsonc`, compatibility flags
- **Deployment**: `wrangler deploy`, `wrangler dev`, environments

## Quick Commands (No Fetch Needed)

These common commands don't require documentation lookup:

```bash
# Create new project
npm create cloudflare@latest

# Local development  
npx wrangler dev

# Deploy
npx wrangler deploy        # Workers
npx wrangler pages deploy  # Pages

# Manage secrets
npx wrangler secret put <KEY>

# D1 database
npx wrangler d1 create <NAME>
npx wrangler d1 execute <DB> --command "SQL"

# KV namespace
npx wrangler kv:namespace create <NAME>

# R2 bucket
npx wrangler r2 bucket create <NAME>
```

## Example Interaction

**User**: "How do I add a D1 database binding to my Worker?"

**Your action**:
```
Task(
  subagent_type: "general-purpose", 
  description: "Fetch D1 binding docs",
  prompt: "User question: How do I add a D1 database binding to my Worker?"
)
```

**Agent returns** (concise answer with exact wrangler.toml syntax)

**You**: Provide the answer to the user, citing the official source.

## What NOT to Do

1. ❌ **Don't WebFetch in main process** - Use the agent to keep context clean
2. ❌ **Don't guess config syntax** - Let the agent fetch current docs
3. ❌ **Don't skip for "simple" questions** - Cloudflare APIs change frequently

## Additional Resources

- **`../agents/cloudflare-docs-fetcher.md`** - The agent that fetches official docs
- **`references/official-sources.md`** - Complete URL index
