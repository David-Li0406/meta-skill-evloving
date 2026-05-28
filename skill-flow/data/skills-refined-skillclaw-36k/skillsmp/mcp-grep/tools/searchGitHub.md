# searchGitHub

Find real-world code examples from over a million public GitHub repositories to help answer programming questions.

**IMPORTANT: This tool searches for literal code patterns (like grep), not keywords. Search for actual code that would appear in files:**
- ✅ Good: `useState(`, `import React from`, `async function`, `(?s)try {.*await`
- ❌ Bad: `react tutorial`, `best practices`, `how to use`

**When to use this tool:**
- When implementing unfamiliar APIs or libraries and need to see real usage patterns
- When unsure about correct syntax, parameters, or configuration for a specific library
- When looking for production-ready examples and best practices for implementation
- When needing to understand how different libraries or frameworks work together

**Perfect for questions like:**
- "How do developers handle authentication in Next.js apps?" → Search: `getServerSession` with `language=['TypeScript', 'TSX']`
- "What are common React error boundary patterns?" → Search: `ErrorBoundary` with `language=['TSX']`
- "Show me real useEffect cleanup examples" → Search: `(?s)useEffect\(\(\) => {.*removeEventListener` with `useRegexp=true`
- "How do developers handle CORS in Flask applications?" → Search: `CORS(` with `matchCase=true` and `language=['Python']`

Use regular expressions with `useRegexp=true` for flexible patterns like `(?s)useState\(.*loading` to find useState hooks with loading-related variables. Prefix the pattern with `(?s)` to match across multiple lines.

Filter by language, repository, or file path to narrow results.

## Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| query | string | Yes | - | The literal code pattern to search for (e.g., `useState(`, `export function`). Use actual code that would appear in files, not keywords or questions. |
| matchCase | boolean | No | false | Whether the search should be case sensitive |
| matchWholeWords | boolean | No | false | Whether to match whole words only |
| useRegexp | boolean | No | false | Whether to interpret the query as a regular expression |
| repo | string | No | - | Filter by repository. Examples: `facebook/react`, `microsoft/vscode`, `vercel/ai`. Can match partial names, e.g., `vercel/` will find repositories in the vercel org. |
| path | string | No | - | Filter by file path. Examples: `src/components/Button.tsx`, `README.md`. Can match partial paths, e.g., `/route.ts` will find route.ts files at any level. |
| language | array | No | - | Filter by programming language. Examples: `["TypeScript", "TSX"]`, `["JavaScript"]`, `["Python"]`, `["Java"]`, `["C#"]`, `["Markdown"]`, `["YAML"]` |

## Examples

### Basic Search

```bash
node ./scripts/mcp-caller.mjs call searchGitHub '{"query":"useState("}'
```

### Language-Filtered Search

```bash
node ./scripts/mcp-caller.mjs call searchGitHub '{"query":"useState(","language":["TypeScript","TSX"]}'
```

### Repository-Specific Search

```bash
node ./scripts/mcp-caller.mjs call searchGitHub '{"query":"useEffect","repo":"facebook/react"}'
```

### Path-Filtered Search

```bash
node ./scripts/mcp-caller.mjs call searchGitHub '{"query":"ErrorBoundary","path":"src/components/"}'
```

### Case-Sensitive Search

```bash
node ./scripts/mcp-caller.mjs call searchGitHub '{"query":"CORS(","matchCase":true,"language":["Python"]}'
```

### Regular Expression Search

```bash
node ./scripts/mcp-caller.mjs call searchGitHub '{"query":"(?s)useEffect\\(\\(\\) => {.*removeEventListener","useRegexp":true,"language":["TypeScript","TSX"]}'
```

### Whole Word Search

```bash
node ./scripts/mcp-caller.mjs call searchGitHub '{"query":"test","matchWholeWords":true}'
```

### Complex Example

```bash
node ./scripts/mcp-caller.mjs call searchGitHub '{"query":"getServerSession","language":["TypeScript"],"path":"/app/","repo":"vercel/"}'
```

## Tips

1. **Start Simple**: Begin with basic patterns like `useState(` before trying complex regex
2. **Filter Strategically**: Use language/path filters to get more relevant results
3. **Use Regex for Flexibility**: Enable regex mode to find patterns that vary slightly
4. **Multi-line Patterns**: Always prefix regex with `(?s)` when searching across lines
5. **Partial Matches**: Repository and path filters support partial matching for flexibility

## Expected Output

The tool returns code snippets with:
- Repository name and URL
- File path
- Line numbers
- Surrounding context

Results are ranked by relevance and repository popularity.
