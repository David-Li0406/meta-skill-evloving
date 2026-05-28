# Enrichment Strategies

Domain-specific content fetching for clipping distillation.

## CRITICAL: Tool Selection is Non-Negotiable

**The wrong tool WILL fail. You MUST match domain to tool exactly.**

## Strategy Selection

Always determine strategy from the `source` URL domain:

```javascript
const url = new URL(source);
const domain = url.hostname.replace('www.', '');
```

| Domain Pattern | Tool | Why | Fallback |
|----------------|------|-----|----------|
| `x.com`, `twitter.com` | **Chrome DevTools** | Firecrawl is BLOCKED | Ask user |
| `youtube.com`, `youtu.be` | **YouTube Transcript MCP** | Specialized API | Use description |
| Everything else | **Firecrawl** | General scraping | WebFetch |

### NEVER Do This

- **NEVER** use Firecrawl for x.com or twitter.com URLs - it returns "website not supported"
- **NEVER** skip Chrome DevTools and go straight to Firecrawl for Twitter
- **NEVER** assume a tool is unavailable without trying it first

---

## Twitter/X.com Strategy

X.com requires JavaScript rendering and often authentication for full content.

### Tool Availability Check

**CRITICAL:** Before attempting Chrome DevTools, check if the tools are available in your current session. The `mcp__chrome-devtools__*` tools may not be configured.

**How to detect:** If you attempt to call `mcp__chrome-devtools__navigate_page` and receive a "tool not found" error, or if the tool simply isn't in your available tools list, proceed directly to the fallback strategy.

### Primary: Chrome DevTools MCP (if available)

```
mcp__chrome-devtools__navigate_page({ url: source })
```

Wait for page load, then:

```
mcp__chrome-devtools__take_snapshot()
```

Returns page HTML. Parse for:
- Tweet text content
- Author display name
- Handle (@username)
- Post date
- Thread replies (if thread)

For complex extraction:

```
mcp__chrome-devtools__evaluate_script({
  script: `
    const article = document.querySelector('article');
    const text = article?.querySelector('[data-testid="tweetText"]')?.textContent;
    const author = article?.querySelector('[data-testid="User-Name"]')?.textContent;
    return { text, author };
  `
})
```

### Fallback: User-Assisted Content (when Chrome DevTools unavailable)

**When to use this fallback:**
1. Chrome DevTools MCP tools are not available in the session
2. Chrome DevTools call fails (timeout, connection error)
3. Page returns empty/blocked content

**Step 1: Parse URL for context**

```
URL: https://x.com/mattpocockuk/status/1876540660609491024

Parsed:
- username: mattpocockuk
- tweet_id: 1876540660609491024
```

**Step 2: Check existing clipping content**

The clipping may already have partial content captured. Check if the note body contains any tweet text beyond just the URL.

**Step 3: Ask user for content**

Present a helpful prompt that makes it easy for the user:

```
I can't fetch X/Twitter content directly (Chrome DevTools MCP isn't available in this session).

**Tweet by @[username]:** [source URL]

Could you help me out? Either:
1. **Paste the tweet text** here
2. **Summarize what it's about** from memory
3. **Skip this clipping** and move to the next one

What would you prefer?
```

**Step 4: Proceed with user-provided content**

Once the user provides content, continue the distillation dialogue as normal. The learning process works just as well with user-provided context.

---

## YouTube Strategy

Use dedicated YouTube Transcript MCP tools.

### Step 1: Get Video Info

```
mcp__youtube-transcript__get_video_info({ url: source })
```

Returns:
- `title` - Video title
- `uploader` - Channel name
- `description` - Video description
- `upload_date` - Publication date (YYYYMMDD format)
- `duration` - Video length

### Step 2: Get Transcript

```
mcp__youtube-transcript__get_transcript({ url: source })
```

Returns full transcript text.

**Pagination:** Check for `next_cursor` in response. If present:

```
mcp__youtube-transcript__get_transcript({
  url: source,
  next_cursor: "[cursor from previous response]"
})
```

Continue until no `next_cursor` returned.

### Fallback: Video Info Only

If transcript unavailable (no captions, private video):

```
Transcript not available for this video. Using description and metadata only.
```

Proceed with video description as content.

---

## Firecrawl Strategy (Default)

For all other URLs, use Firecrawl for intelligent web scraping.

### Standard Fetch

```
mcp__firecrawl__firecrawl_scrape({
  url: source,
  formats: ["markdown"],
  onlyMainContent: true
})
```

Returns:
- `markdown` - Main content as markdown
- `metadata` - Title, description, author if detected

### For Longer Content

If content appears truncated, add options:

```
mcp__firecrawl__firecrawl_scrape({
  url: source,
  formats: ["markdown"],
  onlyMainContent: true,
  waitFor: 3000  // Wait for dynamic content
})
```

### Fallback: Basic Fetch

If Firecrawl fails:

```
WebFetch({
  url: source,
  prompt: "Extract the main article content, title, and author"
})
```

---

## Content Extraction Patterns

After fetching, extract these fields:

| Field | Priority Sources |
|-------|------------------|
| `title` | H1, meta title, URL path |
| `author` | Byline, meta author, channel name |
| `published` | Meta date, URL date pattern |
| `content` | Main article body, transcript, tweet text |
| `summary` | Meta description, first paragraph |

---

## Error Handling

| Error | Strategy |
|-------|----------|
| Network timeout | Retry once with longer timeout |
| 403/401 | Note auth required, use existing clipping content |
| 404 | Note content unavailable, ask if user has copy |
| Rate limit | Wait and retry, or proceed with existing content |
| Empty response | Use existing clipping content, note limitation |

### Graceful Degradation

Always proceed even with partial content:

```
I was able to fetch partial content from this URL. The summary may be incomplete,
but let's work with what we have. You can add context if you remember more.
```
