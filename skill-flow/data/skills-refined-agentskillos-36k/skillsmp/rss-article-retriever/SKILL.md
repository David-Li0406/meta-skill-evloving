---
name: "rss-article-retriever"
description: "Fetch articles from local WeWe-RSS service, read full content via Playwright, clean and output structured data. Use when user asks to get RSS articles, list recent articles, search articles by keyword, or retrieve article content for video script generation."
---

This skill retrieves articles from a local RSS service (WeWe-RSS) and outputs clean, structured content ready for downstream processing (e.g., video script generation).

## Mandatory Execution Steps

Follow these steps EXACTLY when executing this skill:

### Step 1: Determine Operation Mode
Analyze user input to determine mode:
- **list** → Return article list without full content
- **search** → Filter by keyword, return list
- **get** → Fetch full article content (must use Playwright/curl method)

### Step 2: Fetch from RSS API
### Step 2: Fetch from RSS API
Use the provided python script to fetch RSS articles:
```bash
python3 app/agentic/skills/rss-article-retriever/scripts/fetch_rss.py --limit {limit} --title_include "{keyword}"
```

### Step 3: For Full Content (get mode)
Use the provided python script which uses Playwright:

```bash
python3 app/agentic/skills/rss-article-retriever/scripts/fetch_content.py "{article_url}"
```

If these scripts are available as tools, use the tool directly. Otherwise execute via shell.

### Step 4: Clean Content
Apply cleaning rules from [CLEANING_RULES.md](references/CLEANING_RULES.md):
- Remove author profile sections
- Remove QR codes
- Remove subscription prompts
- Preserve main article text and legal sections

### Step 5: Identify Sections
Look for common legal article headings:
- 案情简介
- 法院审理
- 法院判决
- 法官说法

### Step 6: Output Structured Result
Wrap output in `<skill-output>` markers with proper JSON format.

### Step 7: CRITICAL - Auto-Chain to video-script-generator

**MANDATORY:** After outputting the RSS article result, check the original user request:

If the user's request contains **ANY** of these phrases:
- "制作视频脚本"
- "生成口播脚本"
- "生成视频脚本"
- "make video script"
- "create video script"
- "generate script"
- "to make script"

**You MUST IMMEDIATELY call the video-script-generator skill** with the article content.

**DO NOT ask the user "现在需要用这篇文章来制作视频脚本吗？" or similar questions.**

**DO NOT stop after outputting the article.**

**Execute this command:**
```
Skill(video-script-generator)
```

**With the article's `plain_text` content as input.**

**Example of correct behavior:**
```
User: "请找一篇关于'民间借贷合同'的文章制作视频脚本"

Agent actions:
1. Search RSS for articles about "民间借贷合同"
2. Get full content using Python Playwright
3. Output <skill-output type="rss-article">...</skill-output>
4. IMMEDIATELY call: Skill(video-script-generator) with the article content
5. Output <skill-output type="video-script">...</skill-output>
```

## Important: DO NOT Do This

❌ **DO NOT use Python `requests` library** - WeChat pages are dynamically rendered with JavaScript
❌ **DO NOT use `import requests` or `from bs4 import BeautifulSoup`** - These won't work for dynamic content
❌ **DO NOT say "Playwright is unavailable" or "tool usage limit reached"** - The Python Playwright method above works
❌ **DO NOT give up and ask user to provide content** - Always use the Python Playwright method first
❌ **DO NOT use `curl` to parse WeChat article content** - WeChat articles are JavaScript-rendered

✅ **USE Python Playwright via Bash `python3 -c`** - This is the ONLY reliable method for WeChat articles
✅ **USE `asyncio` and `playwright.async_api`** - These handle async browser operations
✅ **USE `page.evaluate()` to extract content** - This gets the rendered text content
✅ **USE `wait_until='networkidle'`** - This ensures the page is fully loaded before extraction

## Workflow Overview

1. **Parse User Intent** - Determine operation mode (list/search/get)
2. **Call RSS API** - Fetch article metadata from `http://localhost:4000/feeds/all.atom`
3. **Read Full Content** - Use Playwright to access WeChat article pages
4. **Clean Content** - Remove ads, author info, QR codes per cleaning rules
5. **Output Structured Result** - Return JSON with `<skill-output>` boundary markers

## Operation Modes

| Mode | Trigger Keywords | Action | Output |
|------|------------------|--------|--------|
| `list` | "列表", "有哪些", "最近文章", "list" | Return article list (no content) | `article_summary[]` |
| `search` | "关于", "包含", "搜索" + keyword | Filter by title keyword | `article_summary[]` |
| `get` | "最新", "第N篇", "内容", "完整", "get" | Fetch full content via Playwright | `article_full` |

## RSS API Reference

**Endpoint:** `http://localhost:4000/feeds/all.atom`

**Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | number | Number of articles to return (default: 10) |
| `page` | number | Page number for pagination |
| `title_include` | string | Filter: title must include this keyword |
| `title_exclude` | string | Filter: title must not include this keyword |

**Article URL Pattern:** `https://mp.weixin.qq.com/s/{article.id}`

**Example Calls:**
```bash
# Get latest 5 articles
curl "http://localhost:4000/feeds/all.atom?limit=5"

# Search articles containing "民间借贷"
curl "http://localhost:4000/feeds/all.atom?title_include=民间借贷"
```

---

## Playwright Usage Strategy

When fetching full article content, use one of these methods:

### Method 1: Python Playwright (Recommended - WORKS FOR WeChat)
```bash
python3 -c "
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://mp.weixin.qq.com/s/{article_id}', wait_until='networkidle', timeout=30000)
        try:
            await page.wait_for_selector('#js_content', timeout=15000)
        except:
            pass
        content = await page.evaluate('() => { const el = document.getElementById(\"js_content\"); return el ? el.innerText : \"\"; }')
        print(content)
        await browser.close()

asyncio.run(main())
" 2>&1
```

### Method 2: Direct curl with HTML parsing (Fallback - MAY NOT WORK for WeChat)
```bash
# For WeChat articles, try direct fetch first
curl -s "https://mp.weixin.qq.com/s/{article_id}" -H "User-Agent: Mozilla/5.0" | \
  grep -A 1000 'id="js_content"' | grep -B 1000 'id="sg_' | \
  sed 's/<[^>]*>//g' | sed 's/&nbsp;/ /g' | sed 's/&lt;/</g' | sed 's/&gt;/>/g' | tr -s '\n'
```

### Method 3: Read from cached file
If previous methods fail, check if content was saved and read from temp file.

**Content Extraction Steps:**
1. Navigate to article page or fetch via curl
2. Extract content from `#js_content` div
3. Remove HTML tags and decode entities
4. Apply cleaning rules (see [CLEANING_RULES.md](references/CLEANING_RULES.md))
5. Structure output as plain text with identified sections

---

## Content Cleaning Rules

See [CLEANING_RULES.md](references/CLEANING_RULES.md) for detailed rules.

### Quick Reference

**Remove these elements:**
- Author profile cards (`#js_profile_qrcode`, `.profile_container`)
- QR codes (`#js_pc_qr_code`, `.qr_code_pc`)
- Share buttons (`.rich_media_tool`)
- Ad areas (`#js_sponsor_ad_area`)
- Subscription prompts (`#js_profile_article`)
- Image alt texts and captions that are ads

**Preserve these elements:**
- Main text paragraphs (`p`, `section` with text)
- Headings (`strong`, `b`, `h1`-`h6`)
- Lists (`ul`, `ol`, `li`)

**Section Recognition (Legal Articles):**
Common headings to identify sections:
- 案情简介
- 法院审理
- 法院判决
- 法官说法

---

## Output Protocol

**All structured output MUST be wrapped in boundary markers:**

```
<skill-output type="rss-article" schema-version="1.0.0">
{JSON conforming to schema/output-schema-v1.json}
</skill-output>
```

**Marker Attributes:**
| Attribute | Value | Description |
|-----------|-------|-------------|
| `type` | `rss-article` | Fixed value identifying skill type |
| `schema-version` | `1.0.0` | Schema version for compatibility |

### Parsing Rules (For Main Agent/Applications)

```
┌─────────────────────────────────────────────────────┐
│  Skill Complete Output                              │
├─────────────────────────────────────────────────────┤
│  [Optional] Explanatory text (should be ignored)   │
│                                                     │
│  <skill-output type="rss-article" schema-version="1.0.0">
│  {                                                  │
│    "version": "1.0.0",                             │
│    "operation": "get",                             │
│    "result": { ... }  ← Structured result          │
│  }                                                  │
│  </skill-output>                                    │
│                                                     │
│  [Optional] Additional notes (should be ignored)   │
└─────────────────────────────────────────────────────┘
```

**Main Agent Parsing Logic:**
1. Extract content between `<skill-output ...>` and `</skill-output>`
2. Parse as JSON
3. Validate against schema (optional but recommended)
4. **All content outside markers should be ignored**

---

## Output Structure

### For `list` and `search` Operations

```json
{
  "version": "1.0.0",
  "operation": "list",
  "result": {
    "type": "summary",
    "total_count": 5,
    "articles": [
      {
        "id": "article-id-123",
        "title": "Article Title",
        "author": "公众号名称",
        "published_at": "2026-01-20T10:30:00Z",
        "url": "https://mp.weixin.qq.com/s/article-id-123",
        "summary": "RSS 摘要内容..."
      }
    ],
    "query": {
      "limit": 5,
      "page": 1,
      "title_include": null,
      "title_exclude": null
    }
  }
}
```

### For `get` Operation

```json
{
  "version": "1.0.0",
  "operation": "get",
  "result": {
    "type": "full",
    "article": {
      "id": "article-id-123",
      "title": "Article Title",
      "author": "公众号名称",
      "published_at": "2026-01-20T10:30:00Z",
      "url": "https://mp.weixin.qq.com/s/article-id-123",
      "content": {
        "plain_text": "清洗后的纯文本，可直接传递给 video-script-generator",
        "sections": [
          { "heading": "案情简介", "text": "..." },
          { "heading": "法院审理", "text": "..." }
        ],
        "source": "playwright"
      },
      "word_count": 1245,
      "cleaning_notes": ["Removed author profile", "Removed QR codes"]
    }
  }
}
```

---

## Output Modes

| Mode | Trigger | Output Content | Use Case |
|------|---------|----------------|----------|
| **Default** | No parameter | Boundary markers + JSON + optional notes | SaaS integration, main agent calls |
| **Raw** | `--raw` | Pure JSON (no markers, no notes) | Direct API calls, testing |

---

## Pre-Execution Checklist

Before generating output, complete these checks:

1. **Read Schema File**
   - Read `schema/output-schema-v1.json`
   - Confirm all required fields
   - Note format requirements

2. **Reference Examples**
   - Read `references/EXAMPLES.md`
   - Match standard JSON structure

3. **Format Requirements**
   - `version` must use semantic versioning: `"1.0.0"`
   - `published_at` must use ISO 8601 format
   - `word_count` must be calculated from cleaned content

---

## Error Handling

### RSS API Errors

```json
{
  "version": "1.0.0",
  "operation": "list",
  "error": {
    "code": "RSS_CONNECTION_ERROR",
    "message": "Cannot connect to RSS service at localhost:4000",
    "suggestion": "Ensure WeWe-RSS service is running"
  }
}
```

### Playwright Errors

```json
{
  "version": "1.0.0",
  "operation": "get",
  "result": {
    "type": "full",
    "article": {
      "id": "...",
      "content": {
        "plain_text": "RSS 摘要作为回退内容...",
        "sections": [],
        "source": "rss_fallback"
      },
      "cleaning_notes": ["Playwright timeout - using RSS summary as fallback"]
    }
  }
}
```

### Error Codes

| Code | Description |
|------|-------------|
| `RSS_CONNECTION_ERROR` | Cannot connect to RSS service |
| `RSS_PARSE_ERROR` | Failed to parse RSS feed |
| `ARTICLE_NOT_FOUND` | Article ID not found in feed |
| `PLAYWRIGHT_TIMEOUT` | Page load timeout (fallback to RSS summary) |
| `CONTENT_EMPTY` | No content extracted from page |

---

## Integration with video-script-generator

When user requests "用RSS文章制作视频脚本":

1. **Execute rss-article-retriever** with `get` operation
2. **Extract content:** `result.article.content.plain_text`
3. **Call video-script-generator** with extracted content

**Example Chain:**
```
User: "请用最新一篇RSS文章来制作视频脚本"

Step 1: rss-article-retriever (get latest)
  → Outputs: <skill-output type="rss-article">...</skill-output>

Step 2: Extract plain_text from result

Step 3: video-script-generator (with plain_text as input)
  → Outputs: <skill-output type="video-script">...</skill-output>
```

---

## Usage Examples

### List Recent Articles

**User input:** "获取最近5篇文章列表"

**Output:**
```
<skill-output type="rss-article" schema-version="1.0.0">
{
  "version": "1.0.0",
  "operation": "list",
  "result": {
    "type": "summary",
    "total_count": 5,
    "articles": [
      {
        "id": "abc123",
        "title": "民间借贷纠纷案例分析",
        "author": "法律公众号",
        "published_at": "2026-01-20T10:30:00Z",
        "url": "https://mp.weixin.qq.com/s/abc123",
        "summary": "本案涉及民间借贷..."
      },
      ...
    ],
    "query": { "limit": 5, "page": 1 }
  }
}
</skill-output>
```

### Search by Keyword

**User input:** "找一篇关于'民间借贷'的文章"

**Output:**
```
<skill-output type="rss-article" schema-version="1.0.0">
{
  "version": "1.0.0",
  "operation": "search",
  "result": {
    "type": "summary",
    "total_count": 2,
    "articles": [...],
    "query": { "title_include": "民间借贷" }
  }
}
</skill-output>
```

### Get Full Content

**User input:** "获取最新一篇文章的完整内容"

**Output:**
```
<skill-output type="rss-article" schema-version="1.0.0">
{
  "version": "1.0.0",
  "operation": "get",
  "result": {
    "type": "full",
    "article": {
      "id": "abc123",
      "title": "民间借贷纠纷案例分析",
      "author": "法律公众号",
      "published_at": "2026-01-20T10:30:00Z",
      "url": "https://mp.weixin.qq.com/s/abc123",
      "content": {
        "plain_text": "案情简介\n\n张某与李某系朋友关系...",
        "sections": [
          { "heading": "案情简介", "text": "张某与李某系朋友关系..." },
          { "heading": "法院审理", "text": "法院经审理认为..." },
          { "heading": "法院判决", "text": "判决被告李某..." }
        ],
        "source": "playwright"
      },
      "word_count": 1245,
      "cleaning_notes": ["Removed author profile", "Removed QR codes", "Removed subscription prompt"]
    }
  }
}
</skill-output>
```

---

## Reference Materials

- [output-schema-v1.json](schema/output-schema-v1.json) - JSON Schema for output validation
- [CLEANING_RULES.md](references/CLEANING_RULES.md) - Detailed content cleaning rules
- [EXAMPLES.md](references/EXAMPLES.md) - Input/output examples
