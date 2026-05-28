# Retrieve Workflow

Intelligent multi-layer content retrieval system for DIFFICULT content retrieval. Uses built-in tools (WebFetch, WebSearch), BrightData (CAPTCHA handling, advanced scraping), and Apify (RAG browser, Actor ecosystem). USE ONLY WHEN user indicates difficulty: 'can't get this', 'having trouble', 'site is blocking', 'protected site', 'keeps giving CAPTCHA', 'won't let me scrape'. DO NOT use for simple 'read this page' or 'get content from' without indication of difficulty.

## 🎯 Load Full PAI Context

**Before starting any task with this skill, load complete PAI context:**

`Skill("CORE")` or `read ${PAI_DIR}/skills/CORE/SKILL.md`

This provides access to:
- Stack preferences and tool configurations
- Security rules and repository safety protocols
- Response format requirements
- Personal preferences and operating instructions

## When to Use This Skill

**⚠️ IMPORTANT:** This skill is for CHALLENGING content retrieval only, not routine fetching.

**✅ DO USE this skill when user indicates difficulty:**
- "I can't get this content"
- "Having trouble retrieving this"
- "Site is blocking me"
- "Protected site" / "CloudFlare protected"
- "Keeps giving me CAPTCHA"
- "Won't let me scrape this"
- "Bot detection blocking me"
- "Rate limited when trying to get this"
- "Tried to fetch but failed"
- "Need advanced scraping for this"

**❌ DO NOT use this skill for simple requests:**
- "Read this page" → Use WebFetch directly
- "Get content from [URL]" → Use WebFetch directly
- "What does this site say" → Use WebFetch directly
- "Fetch this article" → Use WebFetch directly
- "Check this URL" → Use WebFetch directly

**Simple rule:** Only activate when user signals DIFFICULTY, not for routine content requests.

**NOT for research questions** - use the research skill instead for "research X" or "find information about X"

## 🎯 Intelligent Retrieval Strategy

The Retrieve skill uses a **3-layer fallback strategy** to ensure content can always be retrieved:

```
Layer 1: Built-in Tools (Fast, Simple)
  ↓ (If blocked, rate-limited, or fails)
Layer 2: BrightData (CAPTCHA handling, advanced scraping)
  ↓ (If specialized scraping needed)
Layer 3: Apify (RAG browser, Actor ecosystem)
```

### Decision Tree: Which Layer to Use?

**Start with Layer 1 (Built-in) if:**
- Simple public webpage
- No known bot detection
- Standard HTML content
- Quick one-off fetch

**Use Layer 2 (BrightData) if:**
- Layer 1 blocked or failed
- Known bot detection (CloudFlare, etc.)
- CAPTCHA protection
- Rate limiting encountered
- Multiple pages from same domain
- Search engine results needed (Google, Bing, Yandex)

**Use Layer 3 (Apify) if:**
- Need specialized extraction (social media, e-commerce)
- Complex JavaScript rendering required
- Specific Actor exists for the site
- Layer 1 and 2 both failed
- Need RAG-optimized content (markdown format for LLM processing)

## Layer 1: Built-in Tools

### WebFetch Tool

**Best for:** Simple HTML pages, public content, one-off fetches

**Usage:**
```typescript
// Fetch and extract specific information
WebFetch({
  url: "https://example.com/page",
  prompt: "Extract the main article content and author name"
})
```

**When it fails:**
- Returns error about blocked request
- Gets rate-limited (429 status)
- Receives CAPTCHA challenge
- Returns empty/broken content
→ **Escalate to Layer 2 (BrightData)**

### WebSearch Tool

**Best for:** Finding content when you have keywords but not URLs

**Usage:**
```typescript
// Search for content, get URLs, then fetch them
WebSearch({
  query: "latest React 19 features documentation",
  allowed_domains: ["react.dev"]
})
```

**When it fails:**
- Need more comprehensive search results
- Need specific search engine (Google, Bing, Yandex)
→ **Escalate to Layer 2 (BrightData search_engine)**

## Layer 2: BrightData

### scrape_as_markdown

**Best for:** Sites with bot protection, CAPTCHA, JavaScript rendering

**Key Features:**
- Bypasses CloudFlare, bot detection, CAPTCHAs
- Returns clean markdown (perfect for LLM consumption)
- Handles JavaScript-heavy sites
- Residential proxy network

**Usage via BrightData CLI or API:**
```bash
# Single URL scraping with bot protection bypass
brightdata scrape "https://protected-site.com/article"

# Multiple URLs in parallel (up to 10)
brightdata scrape-batch "https://site.com/page1" "https://site.com/page2" "https://site.com/page3"
```

**When to use:**
- Layer 1 WebFetch failed with blocking/CAPTCHA
- Known protected sites (CloudFlare, etc.)
- Need batch scraping from same domain
- Want markdown output for LLM processing

**When it fails:**
- Site requires very specialized extraction logic
- Need social media specific scraping
- **Escalate to Layer 3 (Apify Actors)**

### search_engine

**Best for:** Getting search results from Google, Bing, Yandex

**Usage via BrightData CLI or API:**
```bash
# Search Google for results
brightdata search --engine google "React 19 server components"

# Search multiple engines
brightdata search --engine google "React 19 features"
brightdata search --engine bing "React 19 features"
```

**Output format:**
- Google: JSON with structured results
- Bing/Yandex: Markdown with URLs, titles, descriptions

**When to use:**
- Need search engine results (not just website content)
- Want multiple search engines for comprehensive coverage
- Layer 1 WebSearch insufficient

## Layer 3: Apify

### RAG Web Browser Actor

**Best for:** Content optimized for RAG/LLM consumption, general browsing

**Key Features:**
- Google Search + scraping in one Actor
- Returns markdown optimized for LLM context
- Can scrape individual URLs or search results
- Top N results from search

**Usage via Apify CLI or API:**
```bash
# Search Google and scrape top 3 results
apify call apify/rag-web-browser -i '{"query": "React 19 server components", "maxResults": 3}'

# Scrape specific URL
apify call apify/rag-web-browser -i '{"query": "https://react.dev/blog/2024/12/05/react-19", "maxResults": 1}'
```

**When to use:**
- Need content formatted for LLM consumption
- Want search + scraping in one operation
- Layer 1 and 2 failed or insufficient

**Output:** Returns dataset with full results

### Specialized Actors

**Best for:** Site-specific scraping (Instagram, Twitter, LinkedIn, etc.)

**Finding Actors:**
```bash
# Search for specialized Actor
apify actors search "instagram posts scraper"

# Get Actor details
apify actors info apify/instagram-scraper
```

**Using Actors:**
```bash
# Run Actor with input
apify call apify/instagram-scraper -i '{"username": "example", "resultsLimit": 10}'
```

**When to use:**
- Specialized site needs (social media, e-commerce)
- Layer 1 and 2 failed
- Need platform-specific extraction logic

## 🔄 Complete Retrieval Workflow

### Example: Retrieve Article Content

**User request:** "Get me the content from https://example.com/article"

**Execution:**

```bash
# 1. Try Layer 1 (Built-in) first
# Use WebFetch tool with URL and prompt

# 2. If Layer 1 fails (blocked/CAPTCHA):
brightdata scrape "https://example.com/article"

# 3. If Layer 2 fails (needs specialized extraction):
apify call apify/rag-web-browser -i '{"query": "https://example.com/article", "maxResults": 1}'
```

### Example: Search + Scrape Multiple Pages

**User request:** "Get content about React 19 from the top 5 search results"

**Execution:**

```bash
# 1. Try Layer 1 for search:
# Use WebSearch tool with query and allowed_domains
# Extract URLs from results

# 2. Fetch each URL with Layer 1:
# Use WebFetch tool for each URL (can run in parallel)

# 3. If any Layer 1 fetches fail, use Layer 2 batch:
brightdata scrape-batch "$url1" "$url2" "$url3" "$url4" "$url5"

# 4. OR use Layer 3 for all-in-one search + scrape:
apify call apify/rag-web-browser -i '{"query": "React 19 features documentation", "maxResults": 5}'
```

### Example: Protected Site Scraping

**User request:** "Scrape this CloudFlare-protected site"

**Execution:**

```bash
# Skip Layer 1 (known to fail on protected sites)
# Start with Layer 2:
brightdata scrape "https://cloudflare-protected-site.com"

# If Layer 2 fails, try Layer 3:
apify call apify/rag-web-browser -i '{"query": "https://cloudflare-protected-site.com", "maxResults": 1}'
```

## 📊 Layer Comparison Matrix

| Feature | Layer 1 (Built-in) | Layer 2 (BrightData) | Layer 3 (Apify) |
|---------|-------------------|----------------------|-----------------|
| **Speed** | Fast (< 5s) | Medium (10-30s) | Slower (30-60s) |
| **Bot Detection Bypass** | ❌ No | ✅ Yes | ✅ Yes |
| **CAPTCHA Handling** | ❌ No | ✅ Yes | ✅ Yes |
| **JavaScript Rendering** | ⚠️ Limited | ✅ Full | ✅ Full |
| **Batch Operations** | Manual | ✅ Up to 10 | ✅ Unlimited |
| **Search Integration** | ✅ Basic | ✅ Multi-engine | ✅ Google only |
| **Markdown Output** | ✅ Yes | ✅ Yes | ✅ Optimized |
| **Specialized Extraction** | ❌ No | ❌ No | ✅ Yes (Actors) |
| **Cost** | Free | Paid | Paid |
| **Best For** | Simple pages | Protected sites | Specialized scraping |

## 🚨 Error Handling & Escalation

**Layer 1 Errors → Escalate to Layer 2:**
- HTTP 403 (Forbidden)
- HTTP 429 (Rate Limited)
- HTTP 503 (Service Unavailable)
- Empty content returned
- CAPTCHA challenge detected
- Bot detection messages

**Layer 2 Errors → Escalate to Layer 3:**
- Scraping failed after retries
- Site requires very specialized logic
- Need social media specific extraction
- Platform-specific data structures needed

**Layer 3 Errors → Report to User:**
- All layers exhausted
- Site technically impossible to scrape
- Requires manual intervention or login
- Legal/ethical concerns with scraping

## 📁 Scratchpad → History Pattern

**Working Directory (Scratchpad):** `${PAI_DIR}/scratchpad/YYYY-MM-DD-HHMMSS_retrieve-[site-or-topic]/`

**Process:**

1. **Scratchpad (Working Files - Temporary):**
   - Create timestamped directory for each retrieval task
   - Store raw scraped content (HTML, markdown, JSON)
   - Keep intermediate processing notes
   - Save error logs and retry attempts
   - Draft extracted data and transformations

2. **History (Permanent Archive):**
   - Move to `${PAI_DIR}/history/research/YYYY-MM-DD_[description]/` when complete
   - Include: `README.md`, final extracted content, metadata
   - Archive for future reference and reuse

3. **Verification (MANDATORY):**
   - Check if hooks captured output to history automatically
   - If hooks failed, manually save to history
   - Confirm all files present in history directory

**File Structure Example:**

**Scratchpad (temporary workspace):**
```
${PAI_DIR}/scratchpad/2025-10-26-143022_retrieve-react19-docs/
├── raw-content/
│   ├── page1.md (Layer 2 output)
│   ├── page2.md (Layer 2 output)
│   └── page3.md (Layer 2 output)
├── processed/
│   ├── combined-content.md
│   └── extracted-features.json
├── metadata.json (URLs, layers used, timestamps)
└── errors.log (failed attempts, escalations)
```

**History (permanent archive):**
```
${PAI_DIR}/history/research/2025-10-26_react19-documentation/
├── README.md (retrieval documentation)
├── content.md (final extracted content)
├── metadata.json (sources, layers used, timestamps)
└── summary.md (key extracted information)
```

**README.md Template:**
```markdown
# Retrieval: [Site/Topic]

**Date:** YYYY-MM-DD
**Target:** [URLs or site description]
**Layers Used:** Layer 1 / Layer 2 / Layer 3

## Retrieval Request
[Original request]

## URLs Retrieved
- URL 1
- URL 2
- URL 3

## Layers & Tools Used
- Layer 1: WebFetch (success/failed)
- Layer 2: BrightData scrape_as_markdown (success/failed)
- Layer 3: Apify RAG browser (success/failed)

## Challenges Encountered
- Bot detection: Yes/No
- CAPTCHA: Yes/No
- JavaScript rendering: Yes/No
- Rate limiting: Yes/No

## Output Files
- content.md: Final extracted content
- metadata.json: Source tracking
- summary.md: Key information extracted

## Notes
[Any limitations, challenges, or follow-up needed]
```

## 🎯 Quick Reference Card

**Start with Layer 1 (Built-in):**
- Simple public webpages
- Quick one-off fetches
- Basic search queries

**Use Layer 2 (BrightData):**
- Bot detection blocking Layer 1
- CAPTCHA protection
- Rate limiting encountered
- Need batch scraping (2-10 URLs)
- Search engine results needed

**Use Layer 3 (Apify):**
- Specialized site scraping (social media, e-commerce)
- Layer 1 and 2 both failed
- Need RAG-optimized markdown
- Complex extraction logic required

**Remember:**
- Always try simplest approach first (Layer 1)
- Escalate only when previous layer fails
- Document which layers were used and why
- Save valuable retrieved content to history, not scratchpad
