---
name: github-readme
description: Fetch the README content from a GitHub repository. Use when the user asks for a repository README, documentation, or wants to read the repo's main documentation file.
---

# Get GitHub Repository README

Fetch and decode the README content from a GitHub repository.

## Usage

```bash
npx tsx scripts/readme.ts <repository> [options]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `repository` | Yes | Repository in format `owner/repo` or full GitHub URL |

### Options

| Option | Description |
|--------|-------------|
| `--token=TOKEN` | GitHub Personal Access Token (optional, overrides GITHUB_TOKEN env var) |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

```
README.md from facebook/react
-----------------------------
Size: 12.3 KB
URL: https://github.com/facebook/react/blob/main/README.md

# README Contents

[decoded README content displayed here]
```

## Script Execution (Preferred)

```bash
npx tsx scripts/readme.ts <repository> [options]
```

Options:
- `--token=TOKEN` - GitHub Personal Access Token (optional, overrides GITHUB_TOKEN env var)
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the github-api plugin directory: `~/.claude/plugins/cache/github-api/`

## README API

```
GET https://api.github.com/repos/{owner}/{repo}/readme
```

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `owner` | Yes | Repository owner (user or organization) |
| `repo` | Yes | Repository name |

### Examples

Get README content:
```
https://api.github.com/repos/facebook/react/readme
```

## Response Format

The response contains README metadata and base64-encoded content:

- **`name`** - README filename (e.g., "README.md")
- **`path`** - Path to the README
- **`sha`** - Git SHA for the file
- **`size`** - File size in bytes
- **`url`** - API URL for the file
- **`html_url`** - GitHub URL to view the README
- **`content`** - Base64-encoded content
- **`encoding`** - Encoding type (always "base64")

## README Detection

GitHub automatically detects and prioritizes README files in this order:
1. `README.md`
2. `README.markdown`
3. `README.rst`
4. `README.asciidoc`
5. `README.textile`
6. `README.creole`
7. `README`

The API returns the first matching file found.

## URL Format Support

The script accepts various URL formats:
- `owner/repo` (simple format)
- `https://github.com/owner/repo`
- `git+https://github.com/owner/repo`
- `git@github.com:owner/repo`
- `ssh://git@github.com/owner/repo`

## Authentication

README access follows GitHub visibility rules:
- **Public repositories**: No authentication required
- **Private repositories**: Valid token with `repo` scope required

To access private repositories, provide a GitHub Personal Access Token:

**Via environment variable:**
```bash
export GITHUB_TOKEN=your_token_here
npx tsx scripts/readme.ts private/repo
```

**Via command-line option:**
```bash
npx tsx scripts/readme.ts private/repo --token=your_token_here
```

## Caching

README content is cached for 1 hour. READMEs change relatively infrequently, so this provides a good balance between freshness and performance.

Use the `--no-cache` flag to bypass the cache.

## Related

- Use `github-repo` to get repository metadata
- Use `github-user` to get owner profile information
- Use `github-rate-limit` to check your remaining API quota

## Error Handling

**No README found**: Not all repositories have READMEs. The API will return 404 if no README file exists.

**Repository not found**: Verify the owner and repository name are correct.

**Private repository**: Authentication required for private repositories. Provide a valid token.

**Rate limit exceeded**: Use a Personal Access Token for higher rate limits.

## Use Cases

### Package Documentation
Read package documentation from source:
```bash
npx tsx scripts/readme.ts facebook/react
npx tsx scripts/readme.ts vercel/next.js
```

### Quick Reference
Get quick reference for a repository:
```bash
npx tsx scripts/readme.ts nodejs/node
```

### Private Repository Docs
Access private repository documentation:
```bash
npx tsx scripts/readme.ts mycompany/private-repo --token=$GITHUB_TOKEN
```

## Notes

- README content is base64-encoded and decoded automatically
- Large READMEs are fully displayed
- Markdown and other markup formats are displayed in raw form
- For rendered Markdown, use the HTML URL provided in the output
