# RSS Article Retriever

Fetch articles from local WeWe-RSS service, read full content via Playwright, and output clean, structured data.

## Overview

This skill retrieves articles from a local RSS service (WeWe-RSS running on `localhost:4000`) and returns clean, structured content ready for downstream processing like video script generation.

## Features

- **List articles** - Get recent article list with metadata
- **Search articles** - Filter articles by keyword in title
- **Get full content** - Read complete article content using Playwright
- **Content cleaning** - Automatically removes ads, QR codes, author profiles
- **Section detection** - Identifies logical sections in legal articles
- **Error handling** - Graceful fallback to RSS summary if Playwright fails

## Prerequisites

1. **WeWe-RSS Service** must be running on `http://localhost:4000`
2. **Playwright** plugin must be configured in Claude Code settings

### Start WeWe-RSS
```bash
# Using Docker (recommended)
docker run -d -p 4000:4000 cooderl/wewe-rss

# Or using npm
npm install -g wewe-rss
wewe-rss --port 4000
```

### Verify Service
```bash
curl "http://localhost:4000/feeds/all.atom?limit=1"
```

## Usage

### Basic Commands

| Command | Description |
|---------|-------------|
| "获取最近5篇文章列表" | List 5 recent articles |
| "找一篇关于'民间借贷'的文章" | Search articles by keyword |
| "获取最新一篇文章的完整内容" | Get full content of latest article |
| "请用最新一篇RSS文章来制作视频脚本" | Chain with video-script-generator |

### Examples

#### List Recent Articles
```
User: 获取最近3篇文章列表

Skill returns:
- Article metadata (title, author, date, URL)
- RSS summary for each
```

#### Search by Keyword
```
User: 找一篇关于"离婚"的文章

Skill returns:
- Articles with "离婚" in title
- Article count and metadata
```

#### Get Full Content
```
User: 获取第一篇的完整内容

Skill returns:
- Cleaned article text
- Sections with headings
- Word count
- Cleaning notes
```

#### Chain with Video Script Generator
```
User: 请用最新一篇关于"民间借贷"的文章来制作视频脚本

Process:
1. rss-article-retriever searches for article
2. rss-article-retriever gets full content
3. video-script-generator processes content
4. Returns final video script
```

## Output Format

All output follows a structured JSON format with boundary markers:

```
<skill-output type="rss-article" schema-version="1.0.0">
{
  "version": "1.0.0",
  "operation": "list",
  "result": {
    "type": "summary",
    "total_count": 5,
    "articles": [...]
  }
}
</skill-output>
```

For detailed output schema, see [schema/output-schema-v1.json](schema/output-schema-v1.json).

## Content Cleaning

The skill automatically cleans WeChat article content by removing:

- Author profile cards and QR codes
- Subscription prompts and share buttons
- Advertisement areas
- Trailing credits and boilerplate text

Preserved content includes:
- Main article text and paragraphs
- Headings and section markers
- Lists and structured content
- Legal case details (case numbers, dates, amounts)

See [CLEANING_RULES.md](references/CLEANING_RULES.md) for detailed rules.

## Configuration

Update `.claude/settings.local.json` to enable Playwright plugin:

```json
{
  "plugins": {
    "allowed": ["plugin-playwright"]
  }
}
```

## API Reference

### RSS Endpoint
- **URL**: `http://localhost:4000/feeds/all.atom`
- **Method**: GET
- **Parameters**:
  - `limit` - Number of articles (default: 10)
  - `page` - Page number for pagination
  - `title_include` - Filter: title must include keyword
  - `title_exclude` - Filter: title must not include keyword

### Article URL Pattern
```
https://mp.weixin.qq.com/s/{article.id}
```

## Troubleshooting

### RSS Connection Error
```
Error: Cannot connect to RSS service at localhost:4000

Solution:
1. Check if WeWe-RSS is running: curl localhost:4000
2. Restart WeWe-RSS service
3. Verify port configuration
```

### Playwright Timeout
```
Note: Playwright timeout - using RSS summary as fallback

This is expected behavior when:
- Article page loads slowly
- Network connectivity issues
- WeChat rate limiting

The skill will automatically fall back to RSS summary.
```

### Empty Content After Cleaning
```
If cleaning results in empty content:
1. Check cleaning_notes for issues
2. Content will use RSS summary as fallback
3. Report the issue if it persists
```

## Integration with video-script-generator

This skill is designed to work seamlessly with the video-script-generator skill:

```
User Request
    ↓
rss-article-retriever (get article)
    ↓
Extract plain_text from output
    ↓
video-script-generator (create script)
    ↓
Final video script output
```

## See Also

- [SKILL.md](SKILL.md) - Technical skill definition
- [schema/output-schema-v1.json](schema/output-schema-v1.json) - JSON Schema
- [references/CLEANING_RULES.md](references/CLEANING_RULES.md) - Content cleaning rules
- [references/EXAMPLES.md](references/EXAMPLES.md) - Input/output examples
