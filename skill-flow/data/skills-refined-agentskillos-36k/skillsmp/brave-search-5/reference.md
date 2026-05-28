# Brave Search MCP Reference

## Server setup

The official MCP server is `@brave/brave-search-mcp-server` (supports STDIO and HTTP; default is STDIO).

### Environment variables
- `BRAVE_API_KEY` (required)
- `BRAVE_MCP_TRANSPORT` (`stdio` or `http`, default `stdio`)
- `BRAVE_MCP_PORT` (HTTP port, default `8080`)
- `BRAVE_MCP_HOST` (HTTP host, default `0.0.0.0`)
- `BRAVE_MCP_LOG_LEVEL` (`debug|info|notice|warning|error|critical|alert|emergency`, default `info`)
- `BRAVE_MCP_ENABLED_TOOLS` (whitelist)
- `BRAVE_MCP_DISABLED_TOOLS` (blacklist)

## Tool catalog

### brave_web_search
Web search with filtering, pagination, and optional summarization.

Key params: `query`, `count`, `country`, `search_lang`, `ui_lang`, `offset`, `safesearch`, `freshness`, `result_filter`, `summary`.

### brave_local_search
Local business search (requires Pro for full local results; falls back to web search otherwise).

Key params: same as `brave_web_search`.

### brave_image_search
Image search.

Key params: `query`, `count`, `country`, `search_lang`, `safesearch`.

### brave_video_search
Video search.

Key params: `query`, `count`, `country`, `search_lang`, `freshness`.

### brave_news_search
News search.

Key params: `query`, `count`, `country`, `search_lang`, `freshness`, `safesearch`.

### brave_summarizer
Summarize results using a summary key from `brave_web_search` with `summary=true`.

Key params: `key`, `entity_info`, `inline_references`.

