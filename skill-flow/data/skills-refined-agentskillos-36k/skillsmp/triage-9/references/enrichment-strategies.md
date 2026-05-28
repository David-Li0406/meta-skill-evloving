# Enrichment Strategies

## CRITICAL: Enrichment vs Analysis Parallelization

Clippings are **stubs** - they contain URLs but not the full content. Before analysis can happen, content must be **enriched** (fetched from source).

**Key insight:** Enrichment and analysis have DIFFERENT parallelization constraints.

## Enrichment Parallelization by Source Type

| Source Type | Tool | Parallel? | Reason |
|-------------|------|-----------|--------|
| **YouTube** | `youtube-transcript` MCP | ✅ **YES** | Stateless API calls |
| **Public Articles** | Firecrawl `firecrawl_scrape` | ✅ **YES** | Batch API, no auth |
| **GitHub** | Firecrawl | ✅ **YES** | Public, no auth |
| **Twitter/X** | Chrome DevTools | ❌ **NO** | Single browser instance, needs auth |
| **Confluence** | Chrome DevTools | ❌ **NO** | Single browser instance, needs auth |

## Why Chrome DevTools Cannot Parallelize

Chrome DevTools MCP runs a **single browser instance**. Even with `--isolated` flag:
- One browser = one active page interaction at a time
- `select_page` switches context, but tools operate on selected page only
- Multiple MCP server instances would require separate config entries
- Authenticated sessions (Twitter, Confluence) share cookies in one browser

## Parallel Enrichment Examples

**YouTube (parallel):**
```typescript
// All 3 calls execute simultaneously
mcp__youtube-transcript__get_transcript({ url: "https://youtube.com/watch?v=abc" })
mcp__youtube-transcript__get_transcript({ url: "https://youtube.com/watch?v=def" })
mcp__youtube-transcript__get_transcript({ url: "https://youtube.com/watch?v=ghi" })
```

**Public articles (parallel):**
```typescript
// All 3 calls execute simultaneously
mcp__firecrawl__firecrawl_scrape({ url: "https://blog.example.com/post1" })
mcp__firecrawl__firecrawl_scrape({ url: "https://docs.example.com/guide" })
mcp__firecrawl__firecrawl_scrape({ url: "https://github.com/user/repo" })
```

**Twitter (sequential - CANNOT parallelize):**
```typescript
// Must wait for each to complete before starting next
mcp__chrome-devtools__navigate_page({ url: "https://x.com/user/status/123" })
mcp__chrome-devtools__take_snapshot({})
// ... extract content ...
mcp__chrome-devtools__navigate_page({ url: "https://x.com/user/status/456" })
mcp__chrome-devtools__take_snapshot({})
// ... and so on
```

## Phase 1: Enrichment Implementation

**CRITICAL:** Enrichment happens BEFORE spawning analysis subagents. Subagents receive full content, not stubs.

### 1.1 Enrich Parallel-Capable Items

Run all parallel-capable enrichments simultaneously:

```typescript
// YouTube - all at once
mcp__youtube-transcript__get_transcript({ url: "https://youtube.com/watch?v=abc" })
mcp__youtube-transcript__get_transcript({ url: "https://youtube.com/watch?v=def" })

// Public articles - all at once
mcp__firecrawl__firecrawl_scrape({ url: "https://blog.example.com/post", formats: ["markdown"] })
mcp__firecrawl__firecrawl_scrape({ url: "https://github.com/user/repo", formats: ["markdown"] })
```

Store enriched content in memory, keyed by original filename.

### 1.2 Enrich Sequential-Only Items

For Twitter/X, Confluence, or other auth-required sites, use Chrome DevTools **one at a time**:

```typescript
// Twitter thread 1
mcp__chrome-devtools__navigate_page({ url: "https://x.com/user/status/123", timeout: 30000 })
mcp__chrome-devtools__take_snapshot({})
// Extract and store content

// Twitter thread 2 (after thread 1 completes)
mcp__chrome-devtools__navigate_page({ url: "https://x.com/user/status/456", timeout: 30000 })
mcp__chrome-devtools__take_snapshot({})
// Extract and store content
```

**Why sequential?** Chrome DevTools MCP runs a single browser instance. The `--isolated` flag creates a temp profile but doesn't enable parallel page interactions.

### 1.3 Update Enrichment Status

After enrichment completes, update the clipping's frontmatter:

```typescript
para_frontmatter_set({
  file: "00 Inbox/✂️ Article.md",
  set: { distill_status: "enriched" }
})
```

Or store enriched content in a temporary location for the analysis phase.

## Source Type Detection

When scanning inbox, detect source type for enrichment strategy:

| Source | Detection | Enrichment Tool | Parallel? |
|--------|-----------|-----------------|-----------|
| YouTube | `domain === "youtube.com"` or `clipping_type === "youtube"` | `youtube-transcript` MCP | ✅ Yes |
| Twitter/X | `domain === "x.com"` or `domain === "twitter.com"` | Chrome DevTools | ❌ No |
| GitHub | `domain === "github.com"` | Firecrawl | ✅ Yes |
| Confluence | `domain contains "atlassian.net"` | Chrome DevTools | ❌ No |
| Public article | Default for clippings | Firecrawl | ✅ Yes |
| Voice memo | `type === "transcription"` | None (already has content) | N/A |
| Attachment | PDF/DOCX | None (use para scan CLI) | N/A |

## Grouping Items by Enrichment Capability

```typescript
parallelEnrichable: [youtube1, youtube2, article1, github1]  // Can all run at once
sequentialEnrichable: [twitter1, twitter2, confluence1]       // One at a time
noEnrichmentNeeded: [voice1, attachment1]                     // Already have content
```
