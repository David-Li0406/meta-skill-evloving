# Web Fetch with Gemini CLI

Use Gemini CLI to fetch and analyze content from any URL: articles, documentation, blog posts, or web pages.

## Critical Requirement

**MUST use `--yolo` mode.** Web fetching requires web_fetch tool, which needs automatic approval via `--yolo`.

## Command Syntax

```bash
gemini --yolo "Your prompt about https://example.com/page"
```

## Common Use Cases

### Summarize Article

```bash
gemini --yolo "Summarize this article: https://example.com/blog/post"
```

### Extract Specific Information

```bash
gemini --yolo "From https://docs.example.com/api, extract all the authentication methods"
```

### Analyze Documentation

```bash
gemini --yolo "What are the main features described at https://product.com/features?"
```

### Compare Pages

```bash
gemini --yolo "Compare the approaches in https://blog1.com/article and https://blog2.com/article"
```

### Research and Synthesis

```bash
gemini --yolo "Read these three articles and identify common themes: https://site1.com/a, https://site2.com/b, https://site3.com/c"
```

## Output Formatting

For clean, parseable output:

```bash
gemini --yolo "Summarize https://example.com/article" --output-format text
```

## Faster Execution

Disable MCP servers for faster startup:

```bash
gemini --yolo --allowed-mcp-server-names "" "Analyze https://example.com"
```

## What Gemini Accesses

Gemini fetches the web page via web_fetch and can access:
- Page HTML content
- Visible text
- Page metadata
- Links and structure

Gemini converts HTML to readable format and analyzes the content.

## Supported URL Types

Works with any publicly accessible URL:

```bash
# Blog posts
gemini --yolo "Summarize https://blog.example.com/my-post"

# Documentation
gemini --yolo "Extract code examples from https://docs.lib.com/guide"

# News articles
gemini --yolo "What are the key points in https://news.com/article"

# Product pages
gemini --yolo "List features from https://product.com/pricing"

# GitHub repositories
gemini --yolo "Summarize the README at https://github.com/user/repo"
```

## Example Full Workflows

### Research Workflow

```bash
# Collect information from multiple sources
gemini --yolo "Read these documentation pages and create a comparison table of their rate limits: https://api1.com/docs, https://api2.com/docs, https://api3.com/docs" --output-format text
```

### Documentation Extraction

```bash
# Extract specific information
gemini --yolo "From https://framework.com/docs/config, extract all available configuration options and their default values"
```

### Content Analysis

```bash
# Analyze writing or content
gemini --yolo "Analyze the writing style and main arguments in https://blog.com/opinion-piece"
```

### Quick Facts

```bash
# Get quick answers
gemini --yolo "What is the release date mentioned at https://product.com/announcement?"
```

## Advanced Usage

### Structured Extraction

```bash
gemini --yolo "From https://recipe.com/chocolate-cake, extract in JSON format: ingredients (list), prep time, cook time, difficulty level"
```

### Multi-Step Analysis

```bash
# First get overview
gemini --yolo "What are the main sections covered in https://guide.com/tutorial?"

# Then dive deeper
gemini --yolo "From https://guide.com/tutorial section 3, explain the authentication flow in detail"
```


## Best Practices

1. **Be specific** - Ask for particular information rather than "summarize everything"
2. **Use --output-format text** - For cleaner output when parsing results
3. **Verify critical information** - Web content may be outdated or incorrect
4. **Respect robots.txt** - Don't fetch pages that prohibit automated access
5. **Chain requests** - Build on previous answers for multi-step research

## Limitations

- Cannot access pages behind authentication/paywalls
- May struggle with heavily JavaScript-rendered content
- Rate limits may apply for repeated requests
- Some sites may block automated access
- Content freshness depends on when page was last updated

## Difference from Web Search

| Web Fetch | Web Search |
|-----------|------------|
| Fetches specific URL | Searches Google |
| Needs `--yolo` | No special flags |
| Analyzes exact page content | Finds and summarizes results |
| Use when you have the URL | Use when you need to find information |
