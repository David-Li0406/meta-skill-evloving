# Website-to-Vite Scraper Agent V2.0
## Enhanced with API MEGA LIBRARY Integrations

---

## Current Implementation (V1.0)
- ✅ Python + BeautifulSoup for static scraping
- ✅ Playwright via GitHub Actions for CSR pages
- ✅ Asset downloading (CSS, JS, images, fonts)
- ✅ Vite project structure generation
- ✅ Cloudflare Pages deployment

---

## Recommended Enhancements from API MEGA LIBRARY

### 🔥 HIGH PRIORITY - Immediate Integration

| Tool | Type | Use Case | Cost | Status |
|------|------|----------|------|--------|
| **@modelcontextprotocol/server-puppeteer** | MCP | Claude-native browser automation | FREE | 🔄 RECOMMENDED |
| **@executeautomation/playwright-mcp-server** | MCP | Playwright with test code generation | FREE | 🔄 RECOMMENDED |
| **Crawl4AI (Apify)** | API | LLM-optimized scraping + markdown output | $5/mo | 🔄 RECOMMENDED |
| **AI Markdown Maker** | API | Web to clean markdown conversion | Per-use | 🔄 RECOMMENDED |
| **Browserless** | API | Cloud Puppeteer with BrowserQL | $35/mo | ✅ INTEGRATED |
| **Firecrawl** | API | Anti-bot bypass + stealth mode | $16/mo | 🔄 EVALUATE |

### 🛠️ MCP Servers for Claude Integration

```json
{
  "mcpServers": {
    "puppeteer": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-puppeteer"]
    },
    "playwright": {
      "command": "npx", 
      "args": ["-y", "@executeautomation/playwright-mcp-server"]
    },
    "browser": {
      "command": "npx",
      "args": ["@agent-infra/mcp-server-browser@latest"]
    }
  }
}
```

### Key MCP Capabilities

| MCP Server | Features | Best For |
|------------|----------|----------|
| **server-puppeteer** | Navigate, click, fill, screenshot, execute JS | General scraping |
| **playwright-mcp-server** | + Test code generation, web scraping | CSR sites |
| **mcp-server-browser** | Accessibility tree, vision mode, cross-platform | LLM-optimized |
| **browser-mcp** | Page summarization, style modification | Content extraction |
| **patchright** | Stealth browser automation, anti-detection | Protected sites |

---

## Enhanced Scraper Architecture V2.0

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEBSITE-TO-VITE SCRAPER V2.0                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   TIER 1    │    │   TIER 2    │    │   TIER 3    │         │
│  │   FREE      │    │   STEALTH   │    │   PREMIUM   │         │
│  ├─────────────┤    ├─────────────┤    ├─────────────┤         │
│  │ BeautifulSoup│    │ Playwright  │    │ Browserless │         │
│  │ Requests    │    │ Puppeteer   │    │ Firecrawl   │         │
│  │ MCP Servers │    │ GitHub Acts │    │ ScrapingBee │         │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘         │
│         │                  │                  │                 │
│         └──────────────────┼──────────────────┘                 │
│                            ▼                                    │
│                   ┌─────────────────┐                          │
│                   │  SMART ROUTER   │                          │
│                   │  (Auto-detect)  │                          │
│                   └────────┬────────┘                          │
│                            │                                    │
│         ┌──────────────────┼──────────────────┐                │
│         ▼                  ▼                  ▼                │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐          │
│  │   STATIC    │   │    CSR      │   │  PROTECTED  │          │
│  │   SITES     │   │   SITES     │   │   SITES     │          │
│  │ (HTML+CSS)  │   │ (React/Vue) │   │ (Cloudflare)│          │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘          │
│         │                  │                  │                 │
│         └──────────────────┼──────────────────┘                 │
│                            ▼                                    │
│                   ┌─────────────────┐                          │
│                   │  VITE PROJECT   │                          │
│                   │   GENERATOR     │                          │
│                   └────────┬────────┘                          │
│                            │                                    │
│                            ▼                                    │
│                   ┌─────────────────┐                          │
│                   │  CLOUDFLARE     │                          │
│                   │  PAGES DEPLOY   │                          │
│                   └─────────────────┘                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Implementation Plan

### Phase 1: MCP Integration (Week 1)
1. Add Puppeteer MCP server to Claude config
2. Create fallback chain: MCP → Playwright → Firecrawl
3. Auto-detect CSR vs SSR sites

### Phase 2: Smart Router (Week 2)
1. Implement site classification
2. Route to appropriate scraper tier
3. Add retry logic with tier escalation

### Phase 3: Advanced Features (Week 3)
1. Multi-page crawling with sitemap detection
2. Asset optimization (image compression, CSS minification)
3. SEO preservation (meta tags, structured data)

---

## API Integration Code Snippets

### Crawl4AI Integration
```python
# LLM-optimized scraping with markdown output
import httpx

async def crawl4ai_scrape(url: str) -> dict:
    """Use Crawl4AI for LLM-friendly content extraction."""
    response = await httpx.post(
        "https://api.apify.com/v2/acts/raizen~ai-web-scraper/runs",
        headers={"Authorization": f"Bearer {APIFY_TOKEN}"},
        json={
            "startUrls": [{"url": url}],
            "outputFormat": "markdown",
            "includeMetadata": True
        }
    )
    return response.json()
```

### Firecrawl Integration
```python
# Anti-bot bypass for protected sites
import firecrawl

def firecrawl_scrape(url: str) -> dict:
    """Use Firecrawl for protected/anti-bot sites."""
    app = firecrawl.FirecrawlApp(api_key=FIRECRAWL_KEY)
    result = app.scrape_url(url, params={
        "formats": ["markdown", "html"],
        "onlyMainContent": True,
        "waitFor": 5000  # Wait for JS
    })
    return result
```

### Browserless Integration
```python
# Cloud Puppeteer with BrowserQL
async def browserless_scrape(url: str) -> str:
    """Use Browserless for complex JS rendering."""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://chrome.browserless.io/content?token={BROWSERLESS_KEY}",
            json={
                "url": url,
                "waitFor": 5000,
                "gotoOptions": {"waitUntil": "networkidle0"}
            }
        )
        return response.text
```

---

## Cost Optimization Strategy

| Tier | Tool | Cost | Use When |
|------|------|------|----------|
| FREE | BeautifulSoup + Requests | $0 | Static HTML sites |
| FREE | Playwright (GitHub Actions) | $0 | CSR sites (most common) |
| FREE | MCP Servers | $0 | Claude-integrated scraping |
| PAID | Browserless | $35/mo | Heavy JS, complex interactions |
| PAID | Firecrawl | $16/mo | Anti-bot protected sites |
| PAID | Apify Actors | Per-use | Specialized scrapers |

**Target: 80% FREE tier, 20% PAID tier**

---

## Next Steps

1. [ ] Deploy MCP servers to Claude Desktop config
2. [ ] Create smart router in `website_scraper.py`
3. [ ] Add Firecrawl fallback for anti-bot sites
4. [ ] Implement multi-page crawling
5. [ ] Add asset optimization pipeline
6. [ ] Create GitHub Action for batch website cloning

---

## GitHub Repos to Monitor

| Repo | Purpose |
|------|---------|
| [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) | MCP server discovery |
| [mendableai/firecrawl](https://github.com/mendableai/firecrawl) | Anti-bot scraping |
| [unclecode/crawl4ai](https://github.com/unclecode/crawl4ai) | LLM-optimized crawling |
| [anthropics/mcp](https://github.com/anthropics/mcp) | Official MCP SDK |
| [browserless/browserless](https://github.com/browserless/browserless) | Cloud browser |

---

*Generated: December 23, 2025*
*Skill: website-to-vite-scraper*
*Location: breverdbidder/life-os/skills/website-to-vite-scraper/*
