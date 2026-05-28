# Supabase Integration Reference

How to archive discovered GitHub repositories to Supabase insights table.

## GitHub Actions Workflow Dispatch Method

Use the existing `insert_insight.yml` workflow in target repositories.

### BidDeed.AI Repository

```bash
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/breverdbidder/biddeed-conversational-ai/actions/workflows/insert_insight.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "category": "github_discovery",
      "subcategory": "biddeed",
      "title": "Repository Name - One-line value proposition",
      "content": "{\"repo_url\":\"https://github.com/...\",\"stars\":1234,\"language\":\"Python\",\"license\":\"MIT\",\"relevance_score\":85,\"target_project\":\"BidDeed.AI\",\"summary\":\"...\",\"features\":[...],\"integration\":{...},\"quick_start\":\"...\",\"considerations\":[...],\"discovered_at\":\"2025-12-25T08:30:00Z\",\"search_query\":\"original keywords\"}"
    }
  }'
```

**Note:** Set `GITHUB_TOKEN` environment variable with your personal access token (requires `workflow` scope).

### Life OS Repository

```bash
curl -X POST \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/breverdbidder/life-os/actions/workflows/insert_insight.yml/dispatches \
  -d '{
    "ref": "main",
    "inputs": {
      "category": "github_discovery",
      "subcategory": "life_os",
      "title": "Repository Name - One-line value proposition",
      "content": "{\"repo_url\":\"https://github.com/...\",\"stars\":1234,\"language\":\"TypeScript\",\"license\":\"MIT\",\"relevance_score\":88,\"target_project\":\"Life OS\",\"summary\":\"...\",\"features\":[...],\"integration\":{...},\"quick_start\":\"...\",\"considerations\":[...],\"discovered_at\":\"2025-12-25T08:30:00Z\",\"search_query\":\"original keywords\"}"
    }
  }'
```

**Note:** Set `GITHUB_TOKEN` environment variable with your personal access token (requires `workflow` scope).

## Content Schema

The `content` field must be valid JSON containing:

```json
{
  "repo_url": "https://github.com/owner/repo",
  "stars": 1234,
  "forks": 567,
  "language": "Python",
  "license": "MIT",
  "last_commit": "2024-12-15",
  "relevance_score": 85,
  "target_project": "BidDeed.AI" | "Life OS" | "Both",
  
  "summary": "2-3 sentence description from README",
  
  "features": [
    "Feature 1 description",
    "Feature 2 description",
    "Feature 3 description"
  ],
  
  "integration": {
    "problem_solved": "Specific pain point this addresses",
    "implementation": "How to integrate - API call/library import/workflow pattern",
    "effort": "Low" | "Medium" | "High",
    "effort_hours": 1,
    "dependencies": ["package1", "package2", "service-name"]
  },
  
  "quick_start": "Minimal working code example (escaped for JSON)",
  
  "considerations": [
    "Potential concern or trade-off 1",
    "Potential concern or trade-off 2"
  ],
  
  "discovered_at": "2025-12-25T08:30:00Z",
  "search_query": "Original search keywords used",
  "hunter_version": "1.0"
}
```

## Category Taxonomy

### Category: github_discovery
Fixed category for all GitHub repository discoveries.

### Subcategories
- `biddeed` - Repositories relevant to BidDeed.AI
- `life_os` - Repositories relevant to Life OS
- `both` - Cross-project utilities

## Title Format

Format: `[Repository Name] - [One-line value proposition]`

**Examples:**
- `mailparser - Email parsing automation for confirmation extraction`
- `Marmite - Zero-config Markdown static site generator`
- `SummerCart64 - Open-source N64 flashcart with 64DD emulation`
- `super-productivity - ADHD-focused task management with time tracking`

## Batch Insert Example

When discovering multiple repositories in one session, trigger workflows sequentially with 2-second delays:

```bash
#!/bin/bash

# Repository 1
curl -X POST ... -d '{"ref":"main","inputs":{...}}'
sleep 2

# Repository 2
curl -X POST ... -d '{"ref":"main","inputs":{...}}'
sleep 2

# Repository 3
curl -X POST ... -d '{"ref":"main","inputs":{...}}'
```

## Error Handling

**Common Errors:**

1. **401 Unauthorized**
   - Check GitHub token is valid
   - Verify token has `workflow` scope

2. **404 Not Found**
   - Verify workflow file exists at `.github/workflows/insert_insight.yml`
   - Check repository name is correct

3. **422 Unprocessable Entity**
   - JSON in `content` field is malformed
   - Escape special characters properly
   - Validate JSON structure before sending

4. **Workflow fails to run**
   - Check `SUPABASE_SERVICE_KEY` secret exists in repo
   - Verify Supabase URL is correct
   - Ensure insights table exists with proper schema

## Validation Before Insert

Always validate JSON structure locally before triggering workflow:

```bash
# Test JSON validity
echo '{"repo_url":"https://github.com/...","stars":1234,...}' | python3 -m json.tool

# If valid, proceed with curl request
```

## Supabase Insights Table Schema

The `insights` table has the following structure:

```sql
CREATE TABLE insights (
  id BIGSERIAL PRIMARY KEY,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  category TEXT NOT NULL,
  subcategory TEXT,
  title TEXT NOT NULL,
  content JSONB NOT NULL,
  metadata JSONB
);
```

**Indexes:**
- `idx_insights_category` on `category`
- `idx_insights_subcategory` on `subcategory`
- `idx_insights_created_at` on `created_at DESC`

**Querying discoveries:**

```sql
-- Get all GitHub discoveries
SELECT * FROM insights 
WHERE category = 'github_discovery'
ORDER BY created_at DESC;

-- Get BidDeed.AI discoveries
SELECT * FROM insights 
WHERE category = 'github_discovery' 
  AND subcategory = 'biddeed'
ORDER BY (content->>'relevance_score')::int DESC;

-- Get high-scoring discoveries
SELECT 
  title,
  content->>'repo_url' as repo,
  content->>'relevance_score' as score
FROM insights 
WHERE category = 'github_discovery'
  AND (content->>'relevance_score')::int >= 80
ORDER BY (content->>'relevance_score')::int DESC;
```

## Metadata Field (Optional)

Additional metadata can be stored in the `metadata` JSONB column:

```json
{
  "discovery_session_id": "uuid-of-session",
  "user_request": "Original user request text",
  "total_repos_evaluated": 15,
  "repos_above_threshold": 5,
  "search_queries_used": [
    "site:github.com foreclosure scraper",
    "site:github.com legal document parsing"
  ],
  "discovery_duration_seconds": 120
}
```

## Direct Supabase REST API (Alternative)

If GitHub Actions workflow is unavailable, use direct REST API:

```bash
curl -X POST \
  "https://mocerqjnksmhcjzxrewo.supabase.co/rest/v1/insights" \
  -H "apikey: $SUPABASE_ANON_KEY" \
  -H "Authorization: Bearer $SUPABASE_SERVICE_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{
    "category": "github_discovery",
    "subcategory": "biddeed",
    "title": "Repository Name - Value prop",
    "content": {...},
    "metadata": {...}
  }'
```

**Note:** Direct API calls may encounter SSL certificate issues. Prefer GitHub Actions workflow dispatch method. Set `SUPABASE_ANON_KEY` and `SUPABASE_SERVICE_KEY` environment variables.