---
name: npm-search
description: Search for npm packages by keyword, name, or description. Use when the user asks to search npm packages, find packages related to a topic, or discover packages for a specific purpose.
---

# Search npm Registry

Search the npm registry for packages by keyword, name, or description.

## Usage

```bash
npx tsx scripts/search.ts <query> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `query` | Yes | Search query (can be package name, keyword, or description text) |

### Options

| Option | Description |
|--------|-------------|
| `--size=N` | Number of results to return (default: 20, max: 250) |
| `--from=N` | Offset for pagination (default: 0) |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

```
Found 1,234 packages for "http"

1. express (4.18.2)
   Fast, unopinionated, minimalist web framework
   Score: 0.98 (quality: 0.95, popularity: 1.0, maintenance: 0.99)
   https://www.npmjs.com/package/express

2. axios (1.6.0)
   Promise based HTTP client for the browser and node.js
   Score: 0.97 (quality: 0.94, popularity: 1.0, maintenance: 0.98)
   https://www.npmjs.com/package/axios
```

## Script Execution (Preferred)

```bash
npx tsx scripts/search.ts <query> [options]
```

Options:
- `--size=N` - Number of results to return (default: 20, max: 250)
- `--from=N` - Offset for pagination (default: 0)
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the npm-registry plugin directory: `~/.claude/plugins/cache/npm-registry/`

## Search API

```
GET https://registry.npmjs.org/-/v1/search
```

### Parameters

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `text` | Yes | string | Search query (can be package name, keyword, or description text) |
| `size` | No | number | Number of results to return (default: 20, max: 250) |
| `from` | No | number | Offset for pagination (default: 0) |

### Examples

Search for HTTP-related packages:
```
https://registry.npmjs.org/-/v1/search?text=http&size=10
```

Search with pagination:
```
https://registry.npmjs.org/-/v1/search?text=react&size=20&from=20
```

## Response Format

Each result contains:
- `package.name` - Package name
- `package.version` - Latest version
- `package.description` - Package description
- `package.keywords` - Array of keywords (if available)
- `package.author` - Author information
- `package.links` - URLs to npm, homepage, repository, bugs
- `score.final` - Overall score (0-1)
- `score.detail.quality` - Quality score (0-1)
- `score.detail.popularity` - Popularity score (0-1)
- `score.detail.maintenance` - Maintenance score (0-1)
- `searchScore` - Relevance to search query

## Search Tips

- **Keyword search**: Use common keywords like "http", "database", "testing"
- **Specific packages**: Type the package name directly
- **Combine terms**: Use multiple words for more specific results
- **Author search**: Search by author name to find their packages

## Caching

Search results are cached for 1 hour. The npm registry search index is updated frequently but package metadata changes less often.

Use the `--no-cache` flag to bypass the cache and fetch fresh results.

## Related

- Use `npm-info` to get detailed package metadata
- Use `npm-exists` to quickly check if a package name is available
- Use `npm-downloads` to view download statistics

## Error Handling

If the search returns no results, try:
1. Using more general search terms
2. Checking for typos in the query
3. Exploring alternative keywords

Rate limiting: The npm registry may rate limit excessive requests. If you encounter rate limiting, wait a few minutes before trying again.
