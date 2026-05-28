---
name: github-rate-limit
description: Check GitHub API rate limit status and remaining quota. Use when the user asks about API quota, rate limits, or wants to know how many requests are remaining.
---

# Check GitHub API Rate Limit

Check your current GitHub API rate limit status and remaining requests.

## Usage

```bash
npx tsx scripts/rate-limit.ts [options]
```

### Options

| Option | Description |
|--------|-------------|
| `--token=TOKEN` | GitHub Personal Access Token (optional, overrides GITHUB_TOKEN env var) |
| `--no-cache` | Bypass cache and fetch fresh data from API |

### Output

```
GitHub API Rate Limit Status
-----------------------------

Core API:
  Limit: 5,000 requests/hour
  Used: 1,234 requests
  Remaining: 3,766 requests
  Resets in: 23 minutes

Search API:
  Limit: 30 requests/minute
  Used: 5 requests
  Remaining: 25 requests
  Resets in: 45 seconds

Authentication: Authenticated (your_token_here)
```

## Script Execution (Preferred)

```bash
npx tsx scripts/rate-limit.ts [options]
```

Options:
- `--token=TOKEN` - GitHub Personal Access Token (optional, overrides GITHUB_TOKEN env var)
- `--no-cache` - Bypass cache and fetch fresh data from API

Run from the github-api plugin directory: `~/.claude/plugins/cache/github-api/`

## Rate Limit API

```
GET https://api.github.com/rate_limit
```

## Response Format

The response contains rate limit information for different API categories:

```json
{
  "resources": {
    "core": {
      "limit": 5000,
      "used": 1234,
      "remaining": 3766,
      "reset": 1697376000
    },
    "search": {
      "limit": 30,
      "used": 5,
      "remaining": 25,
      "reset": 1697372400
    }
  },
  "rate": {
    "limit": 5000,
    "used": 1234,
    "remaining": 3766,
    "reset": 1697376000
  }
}
```

## Rate Limit Categories

### Core API
- **Endpoints**: Most GitHub REST API endpoints
- **Unauthenticated**: 60 requests/hour
- **Authenticated**: 5,000 requests/hour
- **Reset**: Hourly

### Search API
- **Endpoints**: Search endpoints (e.g., code search, repo search)
- **Unauthenticated**: 10 requests/minute
- **Authenticated**: 30 requests/minute
- **Reset**: Every minute

## Rate Limits by Authentication

| Authentication Type | Core API | Search API |
|---------------------|----------|------------|
| None (Unauthenticated) | 60/hour | 10/minute |
| Personal Access Token | 5,000/hour | 30/minute |
| OAuth App | 5,000/hour | 30/minute |
| GitHub App Installation | 5,000/hour | 30/minute |

## Authentication

To check your authenticated rate limit, provide a GitHub Personal Access Token:

**Via environment variable:**
```bash
export GITHUB_TOKEN=your_token_here
npx tsx scripts/rate-limit.ts
```

**Via command-line option:**
```bash
npx tsx scripts/rate-limit.ts --token=your_token_here
```

Create a token at: https://github.com/settings/tokens

## Caching

Rate limit status is cached for 5 minutes. Rate limits reset frequently, so short cache times provide near-real-time accuracy while improving performance.

Use the `--no-cache` flag to bypass the cache.

## Best Practices

1. **Check before bulk operations**: Run this script before making many API calls
2. **Use authentication**: Authenticated requests have 80x more quota
3. **Handle rate limits**: Implement exponential backoff when limits are approached
4. **Cache responses**: Use caching to reduce redundant API calls

## Rate Limit Exhaustion

When you exceed your rate limit:

```
HTTP 403 Forbidden
{
  "message": "API rate limit exceeded for xxx.xxx.xxx.xxx.",
  "documentation_url": "https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"
}
```

**Solutions:**
1. Wait for the quota to reset (shown in the output)
2. Authenticate with a Personal Access Token
3. Use conditional requests with `If-None-Match` headers
4. Implement caching to reduce redundant requests

## Related

- Use `github-repo` to get repository information (consumes core quota)
- Use `github-readme` to fetch READMEs (consumes core quota)
- Use `github-user` to get user profiles (consumes core quota)

## Error Handling

**Authentication errors**: Verify your token is valid and not expired.

**Network errors**: Check your internet connection and try again.

**Invalid response**: The GitHub API may be temporarily unavailable.

## Use Cases

### Before Bulk Operations
Check quota before running many API calls:
```bash
npx tsx scripts/rate-limit.ts --token=$GITHUB_TOKEN
```

### Monitor Usage
Track API usage during development:
```bash
npx tsx scripts/rate-limit.ts
```

### Debug Rate Limit Issues
Diagnose rate limit problems:
```bash
npx tsx scripts/rate-limit.ts --no-cache
```

## Notes

- Rate limits are per IP address for unauthenticated requests
- Rate limits are per authenticated user/token
- Different API categories have different rate limits
- The `reset` timestamp is Unix epoch time in seconds
- Rate limits reset at the top of each hour/minute
