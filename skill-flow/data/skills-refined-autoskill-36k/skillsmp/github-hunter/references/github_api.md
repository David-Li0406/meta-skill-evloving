# GitHub API Reference for Repository Discovery

## Search Repositories

**Endpoint:** `https://github.com/search?q={query}&type=repositories&s=stars&o=desc`

**Query Syntax:**
```
foreclosure data scraping language:python stars:>100
```

**Query Parameters:**
- `language:python` - Filter by programming language
- `stars:>100` - Minimum stars
- `pushed:>2024-01-01` - Last updated after date
- `topic:web-scraping` - Filter by topic
- `license:mit` - Filter by license

**Sort Options:**
- `s=stars` - Sort by stars
- `s=updated` - Sort by last updated
- `s=forks` - Sort by forks

**Order:**
- `o=desc` - Descending
- `o=asc` - Ascending

## Get Repository Details

**Endpoint:** `https://api.github.com/repos/{owner}/{name}`

**Response Fields:**
```json
{
  "name": "repository-name",
  "full_name": "owner/repository-name",
  "description": "Repository description",
  "html_url": "https://github.com/owner/repository-name",
  "stargazers_count": 1234,
  "watchers_count": 567,
  "forks_count": 89,
  "language": "Python",
  "license": {
    "key": "mit",
    "name": "MIT License"
  },
  "pushed_at": "2025-12-20T10:30:00Z",
  "created_at": "2020-01-15T08:00:00Z",
  "updated_at": "2025-12-20T10:30:00Z",
  "topics": ["web-scraping", "python", "automation"],
  "has_issues": true,
  "has_wiki": true,
  "archived": false,
  "disabled": false
}
```

## Get README

**Endpoint:** `https://api.github.com/repos/{owner}/{name}/readme`

**Response:**
```json
{
  "name": "README.md",
  "path": "README.md",
  "size": 5432,
  "content": "base64_encoded_content",
  "encoding": "base64"
}
```

**To decode:**
```python
import base64
readme_text = base64.b64decode(content).decode('utf-8')
```

## Rate Limits

**Unauthenticated:** 60 requests/hour
**Authenticated:** 5,000 requests/hour

**Check rate limit:**
```
GET https://api.github.com/rate_limit
```

## Best Practices

1. **Use web_search for initial discovery**
   - Finds repos via GitHub's web interface
   - No authentication required
   - Good for broad searches

2. **Use web_fetch for detailed info**
   - Get repo metadata via API
   - Get README content
   - Check license and stats

3. **Batch processing**
   - Discover multiple repos per topic
   - Score them all
   - Archive threshold: score >= 60
   - Alert threshold: top 3 or score >= 80

## Example Workflow

```python
# 1. Search GitHub
search_query = "foreclosure auction data language:python stars:>50"
search_url = f"https://github.com/search?q={search_query}&type=repositories&s=stars&o=desc"
# Use web_search to find repos

# 2. Extract repo URLs from results
# Parse GitHub search results page

# 3. For each repo:
api_url = f"https://api.github.com/repos/{owner}/{name}"
# Use web_fetch to get details

# 4. Score and archive
score = score_repo(repo_data, relevance_score=20)
if score['total'] >= 60:
    archive_to_supabase(repo_data)
```

## Supabase Integration

**Workflow dispatch** (preferred):
```bash
curl -X POST \
  -H "Authorization: Bearer ghp_..." \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/breverdbidder/life-os/actions/workflows/insert_insight.yml/dispatches \
  -d '{"ref":"main","inputs":{"category":"github_discovery","subcategory":"auto_hunter","title":"GitHub Hunter: repo-name","content":"{...}"}}'
```

**Direct SQL** (fallback):
```sql
INSERT INTO insights (category, subcategory, title, content, created_at)
VALUES ('github_discovery', 'auto_hunter', 'GitHub Hunter: repo-name', '{"repo_url":"...","score":85}'::jsonb, NOW());
```
