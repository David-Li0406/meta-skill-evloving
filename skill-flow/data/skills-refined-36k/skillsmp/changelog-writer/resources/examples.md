# Changelog Examples

## Writing Style

### Good Examples (Cursor-style brevity + technical specificity)

**Feature description:**
> "Connect GitHub repositories with automatic webhook-driven synchronization. When you push code, Lightfast incrementally updates your knowledge base. Currently supports file contents via Git Trees API; PR metadata coming in v0.2."

**Improvement bullet:**
> "Config hash tracking auto-detects embedding changes and re-processes affected documents"

**Technical detail:**
> "Vector embeddings (Pinecone) + BM25 full-text search with cross-encoder reranking for sub-second results"

### Bad Examples

**Too vague:**
> "GitHub Integration" (what does this cover? files? PRs? issues?)

**Too verbose:**
> "You can now search your entire organization's code using natural language instead of exact keywords. Ask questions like 'how does authentication work' or 'where do we handle rate limiting' and get relevant results based on semantic understanding, not just text matching. This revolutionary approach transforms how teams discover knowledge..." [2 more paragraphs]

**Overselling:**
> "Coming soon: Linear, Notion, Slack, Sentry, and 10 more integrations!" (when they're at 0%)

**Missing limitations:**
> "GitHub integration is live!" (but doesn't mention it's only file contents)

---

## Full Example: v0.1 Changelog

```yaml
---
title: "GitHub File Sync, Semantic Search, Team Workspaces"
slug: "0-1-lightfast-github-file-sync-semantic-search"
publishedAt: "2025-01-15"
excerpt: "Connect GitHub repos with webhook-driven sync, search code semantically with vector + full-text retrieval, and organize work in isolated team workspaces."
tldr: "Lightfast v0.1 brings GitHub file sync with automatic webhook updates, semantic code search combining vector embeddings and BM25 full-text with cross-encoder reranking, and team workspaces with Clerk SSO. Currently supports file contents; PR metadata coming in v0.2."

improvements:
  - "Search highlighting with context-aware snippets and keyword emphasis"
  - "Intelligent chunking that respects code structure (functions, classes, modules)"
  - "Activity tracking with per-workspace job status and search metrics"
  - "Batch processing for efficient handling of large repository updates"
  - "Webhook verification using HMAC SHA-256 signature validation"
  - "Incremental sync that only re-indexes changed files on push"
  - "Config hash tracking to auto-detect config changes and re-process"
  - "Full glob pattern support including **, *, and ! syntax"

infrastructure:
  - "Multi-source schema with generic document model ready for future integrations"
  - "Event-driven workflows using Inngest orchestration with waitForEvent"
  - "Idempotent processing with safe retries and partial failure recovery"
  - "Metrics tracking for per-workspace job lifecycle monitoring"
  - "Type-safe APIs with discriminated unions throughout (TypeScript + Zod)"

seo:
  metaDescription: "Lightfast v0.1 brings GitHub file sync with webhook-driven updates, semantic code search with vector + full-text retrieval, and isolated team workspaces. Production-ready."
  focusKeyword: "webhook-driven sync"
  secondaryKeyword: "semantic code search"
  faq:
    - question: "What is webhook-driven sync?"
      answer: "Webhook-driven sync automatically updates your knowledge base when you push code to GitHub. Instead of polling, Lightfast receives instant notifications, ensuring sub-minute latency for code updates."
    - question: "How does semantic code search work?"
      answer: "Lightfast combines vector embeddings (Pinecone) with BM25 full-text search and cross-encoder reranking. Ask natural language questions like 'how does authentication work' and get relevant code results."

_internal:
  status: draft
  source_prs: ["#1", "#2", "#3"]
  generated: "2025-01-15T10:00:00Z"
---
```

**Body content:**

**GitHub File Sync, Semantic Search, and Team Workspaces**

---

### GitHub Repository Sync (File Contents)

Connect GitHub repositories with automatic webhook-driven synchronization. When you push code, Lightfast incrementally updates your knowledge base using Git Trees API to handle repositories with 100k+ files efficiently.

**What's included:**
- File contents (code, markdown, docs) indexed via webhook events
- `lightfast.yml` configuration with glob patterns for include/exclude
- HMAC SHA-256 webhook verification
- Incremental sync (only changed files re-indexed)

**Not yet:** PR metadata, issue discussions, commit history (planned for v0.2 based on feedback)

**Example config:**
```yaml
# lightfast.yml
include:
  - "src/**/*.ts"
  - "docs/**/*.md"
exclude:
  - "**/*.test.ts"
  - "node_modules/**"
```

**Why webhooks over polling:** Webhooks provide sub-minute update latency while avoiding GitHub API rate limits (5,000 requests/hour). Polling would exhaust limits for active teams.

[Learn more about GitHub setup](/docs/integrations/github)

---

### Semantic Code Search

Search your codebase using natural language, not keywords. Ask "how does authentication work" and get relevant results ranked by meaning with highlighted snippets and citations.

**What's included:**
- Vector embeddings (Pinecone) + BM25 full-text search
- Cross-encoder reranking for top results
- Sub-second queries across 100k+ files
- Snippet highlighting with source citations

**How it works:** Each file is chunked with context preservation, embedded using sentence transformers, and indexed with metadata. Queries use hybrid retrieval (dense + sparse) followed by reranking.

[API documentation](/docs/api/search)

---

### Team Workspaces

Create isolated knowledge bases per team or project. Each workspace has separate GitHub integrations, search access, and activity tracking.

**What's included:**
- Clerk authentication with SSO support
- Per-workspace GitHub app installations
- Team-based access control
- Activity and metrics tracking

[Setup guide](/docs/workspaces)

---

### What's Coming Next

Based on your feedback:

1. **PR & Issue ingestion** (v0.2) — Search pull requests, reviews, issue discussions
2. **Posthog integration** (when 3+ customers request it) — 1-2 week implementation
3. **Render integration** (when 3+ customers request it) — 1-2 week implementation

---

### Resources

- [Quick Start Guide](/docs/quick-start)
- [GitHub Integration Setup](/docs/integrations/github)
- [Configuration Reference](/docs/config)
- [API Documentation](/docs/api)
- [Workspace Management](/docs/workspaces)
