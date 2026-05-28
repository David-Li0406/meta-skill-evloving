# Web Search with Gemini CLI

Use Gemini CLI to search Google and get current information, latest documentation, or answers to questions requiring up-to-date knowledge.

## No Special Requirements

Web search works out of the box - **no `--yolo` flag needed**.

## Command Syntax

```bash
gemini "Search for <your query> and <what to do with results>"
```

## Common Use Cases

### Find Latest Information

```bash
gemini "Search for TypeScript 5.7 features and summarize the key changes"
```

### Find Documentation

```bash
gemini "Search for React Query v5 migration guide and extract the breaking changes"
```

### Compare Technologies

```bash
gemini "Search for Bun vs Node.js performance comparisons and summarize the findings"
```

### Find Best Practices

```bash
gemini "Search for Next.js 15 app router best practices and list the top recommendations"
```

### Research Questions

```bash
gemini "Search for how to implement rate limiting in FastAPI and explain the recommended approach"
```

## Output Formatting

For clean, parseable output:

```bash
gemini "Search for Rust async programming tutorials" --output-format text
```

## Faster Execution

Disable MCP servers for faster startup:

```bash
gemini --allowed-mcp-server-names "" "Search for latest Python 3.13 features"
```

## How It Works

Gemini performs a Google search, retrieves relevant results, and synthesizes the information based on your prompt. You get summarized, relevant information without manually searching and reading multiple sources.

## Search Strategies

### Focused Searches

Be specific about what you want:

```bash
# Good - specific request
gemini "Search for Vue 3 Composition API lifecycle hooks and create a reference table"

# Less effective - too vague
gemini "Search for Vue 3"
```

### Date-Sensitive Searches

Include timeframes for recent information:

```bash
gemini "Search for JavaScript build tools 2025 trends and summarize"
```

### Comparative Searches

```bash
gemini "Search for Tailwind CSS vs Bootstrap 2025 and create a pros/cons comparison"
```

### Tutorial/Guide Finding

```bash
gemini "Search for deploying Django to Railway tutorial and extract the key steps"
```

### Problem-Solving

```bash
gemini "Search for how to fix CORS errors in Express.js and explain the solutions"
```

## Example Full Workflows

### Research Workflow

```bash
# 1. Get overview
gemini "Search for Redis caching strategies and list the main approaches"

# 2. Deep dive
gemini "Search for Redis cache invalidation patterns and explain each with examples"

# 3. Compare
gemini "Search for Redis vs Memcached for session storage and recommend which to use"
```

### Stay Updated Workflow

```bash
# Check latest releases
gemini "Search for what's new in PostgreSQL 16 and list the major features"

# Find migration guides
gemini "Search for PostgreSQL 15 to 16 migration guide and extract important notes"

# Find community discussions
gemini "Search for PostgreSQL 16 performance improvements real-world results"
```

### Learning Workflow

```bash
# Find tutorials
gemini "Search for Docker multi-stage builds tutorial and explain the concept"

# Find examples
gemini "Search for Docker multi-stage build Python example and show the pattern"

# Find best practices
gemini "Search for Docker multi-stage build optimization tips"
```

## Advanced Techniques

### Structured Output

```bash
gemini "Search for Python web frameworks 2025 and create a table with: name, use case, popularity, learning curve"
```

### Source-Specific Searches

```bash
gemini "Search site:github.com for awesome-python lists and find the most starred repository"
```

### Multiple Queries

```bash
gemini "Search for: 1) Svelte vs React performance 2025, 2) Svelte learning curve discussions, 3) Svelte production readiness - then synthesize findings and recommend for a new project"
```


## Best Practices

1. **Be specific** - Detailed queries get better results
2. **Include action** - Tell Gemini what to do with search results (summarize, extract, compare, etc.)
3. **Use timeframes** - Add years or "latest" for current information
4. **Request structure** - Ask for lists, tables, or organized output
5. **Iterate** - Refine searches based on initial results

## When to Use Web Search vs Web Fetch

| Use Web Search | Use Web Fetch |
|----------------|---------------|
| Don't have specific URL | Have exact URL |
| Need latest information | Need specific page content |
| Researching topic | Analyzing known resource |
| Finding best practices | Reading documentation |
| Comparing options | Extracting specific data |

**Example:**
- Web Search: "Search for Prisma ORM tutorials"
- Web Fetch: "Analyze https://www.prisma.io/docs/getting-started"

## Limitations

- Results depend on Google search quality
- May not have access to very recent information (hours old)
- Cannot access paywalled or login-required content
- Summaries are AI-generated interpretations of search results
- May miss niche or specialized sources

## Combining with Other Features

```bash
# Search + YouTube
gemini --yolo "Search for best TypeScript conference talks 2024, find YouTube links, and summarize the top 3"

# Search + Web Fetch
gemini --yolo "Search for Next.js 15 announcement, get the URL, fetch it, and extract the release date and key features"
```
