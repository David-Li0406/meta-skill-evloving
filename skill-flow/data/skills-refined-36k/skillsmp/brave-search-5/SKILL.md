---
name: brave-search
description: "Fallback search: fast, lightweight web search and content extraction via Brave Search. Use for quick lookups, scoping, or lightweight docs/fact checks when Exa isn't ideal. Load the mcporter skill to execute this skill's MCP calls."
---

# Brave Search MCP

Use Brave Search MCP for web, local, image, video, news, and summarization. This skill documents Brave’s MCP surface and tool parameters.

## When to use

- Fast scoping / quick lookups
- News + recency filters
- Image/video/local search
- Fallback when Exa is overkill
- For deep research or code docs, prefer Exa

## Query tips

- Use `freshness=` for news (e.g. `pd`, `pw`, `pm`, `py`)
- Add `summary=true` for short snippets
- If summarizer fails or results are too thin, switch to Exa

## Output notes

- Some calls return a single top result (not an array). Treat as best-hit.

## Quick start

```bash
brave_web_search query="..." count=5
```

## Common calls

```bash
brave_web_search query="..." count=5 summary=true
brave_local_search query="..." count=5
brave_news_search query="..." count=5 freshness=pd
brave_image_search query="..." count=20
brave_video_search query="..." count=20
brave_summarizer key="..." inline_references=true
```

## Query templates

See `assets/query-templates.json` for reusable parameter templates.

## Reference

See `reference.md` for server setup, tool catalog, and defaults.
