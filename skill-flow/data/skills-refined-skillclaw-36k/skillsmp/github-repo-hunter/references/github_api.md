# GitHub Search API Reference

## Authentication

```bash
curl -H "Authorization: Bearer ghp_YOUR_TOKEN" \
     -H "Accept: application/vnd.github+json" \
     -H "X-GitHub-Api-Version: 2022-11-28" \
     https://api.github.com/search/repositories
```

## Rate Limits

- **Unauthenticated:** 60 requests/hour
- **Authenticated:** 5,000 requests/hour
- **Search API:** 30 requests/minute

Check rate limit status:
```bash
curl https://api.github.com/rate_limit
```

## Search Repositories

**Endpoint:** `GET /search/repositories`

**Parameters:**
- `q` - Search query (required)
- `sort` - stars, forks, help-wanted-issues, updated
- `order` - asc, desc
- `per_page` - Results per page (max 100)
- `page` - Page number

**Query Qualifiers:**
- `language:python` - Filter by language
- `stars:>100` - Stars greater than 100
- `forks:>50` - Forks greater than 50
- `created:>2023-01-01` - Created after date
- `pushed:>2024-01-01` - Pushed after date
- `topic:machine-learning` - Has topic
- `license:mit` - Has MIT license
- `is:public` - Public repos only
- `archived:false` - Exclude archived

**Example Queries:**
```bash
# Foreclosure tools in Python
foreclosure auction language:python stars:>10

# ADHD productivity with good docs
adhd productivity stars:>50 topic:productivity

# Multi-agent systems with recent activity
langgraph multi-agent pushed:>2024-01-01 language:python

# Real estate ML models
real-estate machine-learning xgboost language:python
```

## Get Repository Details

**Endpoint:** `GET /repos/{owner}/{repo}`

Returns full repo metadata including:
- Description, topics, language
- Stars, forks, watchers
- Created, updated, pushed dates
- License, size, default branch
- Has issues, wiki, pages

## Get README

**Endpoint:** `GET /repos/{owner}/{repo}/readme`

Returns README in base64-encoded format:
```python
import base64
content = base64.b64decode(data['content']).decode('utf-8')
```

## Get Contributors

**Endpoint:** `GET /repos/{owner}/{repo}/contributors`

Returns list of contributors with contribution counts.

## Get Languages

**Endpoint:** `GET /repos/{owner}/{repo}/languages`

Returns language breakdown:
```json
{
  "Python": 245234,
  "JavaScript": 123456
}
```

## Best Practices

1. **Use authentication** - 5000 req/hr vs 60 req/hr
2. **Batch requests** - Fetch multiple data points in single call
3. **Cache results** - Avoid redundant API calls
4. **Handle rate limits** - Check headers: `X-RateLimit-Remaining`
5. **Use conditional requests** - ETags for unchanged data
6. **Paginate efficiently** - Use Link headers for next page

## Error Handling

**Common Status Codes:**
- `200` - Success
- `304` - Not Modified (cached)
- `401` - Unauthorized (bad token)
- `403` - Rate limit exceeded
- `404` - Not found
- `422` - Validation failed

**Rate Limit Headers:**
```
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4999
X-RateLimit-Reset: 1372700873
```
