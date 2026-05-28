---
name: npms-suggest
description: Get npm package name suggestions and autocomplete from NPMS.io. Use when the user asks for package name suggestions, wants to autocomplete a package name, or search for packages by name pattern.
---

# Get npm Package Name Suggestions (NPMS.io)

Get package name suggestions and autocomplete from NPMS.io based on a search query.

## Usage

```bash
npx tsx scripts/suggest.ts <query> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `query` | Yes | Search query (minimum 2 characters) |

### Options

| Option | Description |
|--------|-------------|
| `--size=N` | Number of suggestions to return (default: 25, max: 250) |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

```
Suggestions for "react" (25 results)
------------------------------------

1. react
   Score: 1000000
   URL: https://www.npmjs.com/package/react

2. react-dom
   Score: 950000
   URL: https://www.npmjs.com/package/react-dom

3. react-redux
   Score: 923000
   URL: https://www.npmjs.com/package/react-redux

...

Top 10 suggestions:
  react, react-dom, react-redux, react-router, react-scripts,
  react-native, react-hook-form, react-query, react-test-renderer
```

## Script Execution (Preferred)

```bash
npx tsx scripts/suggest.ts <query> [options]
```

Options:
- `--size=N` - Number of suggestions to return (default: 25, max: 250)
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the npms-io plugin directory: `~/.claude/plugins/cache/npms-io/`

## Suggestions API

```
GET https://api.npms.io/v2/search/suggestions?q={query}
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `q` | Yes | Search query (minimum 2 characters) |

### Examples

Get suggestions:
```
https://api.npms.io/v2/search/suggestions?q=react
```

Scoped packages:
```
https://api.npms.io/v2/search/suggestions?q=@babel
```

## Response Format

The response contains an array of package suggestions:

```json
[
  {
    "name": "react",
    "score": 1000000,
    "searchScore": 1000000
  },
  {
    "name": "react-dom",
    "score": 950000,
    "searchScore": 950000
  }
]
```

**Fields:**
- `name` - Package name
- `score` - Package quality score (higher is better)
- `searchScore` - Relevance to the search query (higher is better)

## Search Query Requirements

- **Minimum length**: 2 characters
- **Case sensitivity**: Search is case-insensitive
- **Partial matching**: Matches package names containing the query
- **Scoped packages**: Include `@scope/` prefix to search within a scope

## Caching

Suggestions are cached for 1 hour. The package registry changes relatively slowly, and suggestion results remain stable for reasonable periods.

Use the `--no-cache` flag to bypass the cache.

## Related

- Use `npms-analyze` to analyze specific package quality
- Use `npms-compare` to compare multiple packages
- Use `npm-search` for full-text search by keyword and description

## Search Patterns

### Exact Name
Find exact package name:
```bash
npx tsx scripts/suggest.ts react
```

### Prefix Match
Find packages starting with a prefix:
```bash
npx tsx scripts/suggest.ts react-
```

### Scoped Packages
Search within a scope:
```bash
npx tsx scripts/suggest.ts @babel/
npx tsx scripts/suggest.ts @types/react
```

### Partial Match
Find packages containing a term:
```bash
npx tsx scripts/suggest.ts express
npx tsx scripts/suggest.ts router
```

## Use Cases

### Package Discovery
Discover packages when you know part of the name:
```bash
npx tsx scripts/suggest.ts redux
```

### Autocomplete
Implement autocomplete for package input:
```bash
npx tsx scripts/suggest.ts --size=10 reac
```

### Find Alternatives
Find related packages by name pattern:
```bash
npx tsx scripts/suggest.ts router
```

### Scope Exploration
Explore packages in a specific scope:
```bash
npx tsx scripts/suggest.ts @babel/
npx tsx scripts/suggest.ts @types/
```

## Tips

1. **Be specific**: Longer queries produce more relevant results
2. **Use prefixes**: Add `-` to find packages with specific prefixes
3. **Explore scopes**: Use `@scope/` to browse scoped packages
4. **Check quality**: Use `npms-analyze` to review package quality before using
5. **Compare options**: Use `npms-compare` to evaluate multiple packages

## Limitations

- Only searches package names (not descriptions or keywords)
- Minimum 2 character query required
- Maximum 250 results per request
- Results sorted by relevance and quality score

## Difference from npm-search

| Feature | npms-suggest | npm-search |
|---------|--------------|------------|
| Searches | Package names only | Names, descriptions, keywords |
| Speed | Very fast (name-only) | Slower (full-text) |
| Results | Name-based matches | Semantic matches |
| Best for | Autocomplete, name discovery | General package search |

## Notes

- NPMS.io suggestions are optimized for name matching and autocomplete
- Results include both quality and relevance scores
- Use for quick package name lookups when building CLIs or tools
- For comprehensive search, combine with `npm-search`
