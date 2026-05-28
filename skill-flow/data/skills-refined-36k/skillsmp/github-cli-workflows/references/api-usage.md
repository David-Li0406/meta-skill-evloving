# GitHub API Usage with gh api

Comprehensive guide to using `gh api` for custom GitHub operations beyond core commands.

## Overview

The `gh api` command provides direct access to the GitHub REST and GraphQL APIs with automatic authentication. Use it for operations not covered by dedicated `gh` commands or when you need more control over the request.

**When to use `gh api`:**
- Custom API operations not in core commands
- Complex GraphQL queries
- Batch operations
- Advanced filtering and data manipulation
- Beta API features
- Webhooks, repository settings, organization management

## Quick Reference

```bash
gh api <endpoint>                # GET request
gh api <endpoint> -X POST        # POST request
gh api <endpoint> -F key=value   # Typed field
gh api <endpoint> -f key=value   # String field
gh api <endpoint> --method PATCH # PATCH request
gh api graphql -f query='...'    # GraphQL query
gh api <endpoint> --paginate     # Auto-paginate results
gh api <endpoint> --jq '.field'  # Extract with jq
```

**Remember:** Use `gh api --help` for extensive examples and detailed documentation.

## Basic REST API Calls

### GET Requests

**Repository information:**
```bash
gh api repos/{owner}/{repo}
gh api repos/octocat/hello-world
```

**Placeholder replacement:**
- `{owner}` - Repository owner from current directory
- `{repo}` - Repository name from current directory
- `{branch}` - Current branch

```bash
gh api repos/{owner}/{repo}/branches/{branch}
```

**Query parameters:**
```bash
gh api repos/{owner}/{repo}/issues --field state=closed --field per_page=100
```

### POST Requests

**Create repository:**
```bash
gh api user/repos \
  -X POST \
  -f name=my-new-repo \
  -f description="A new repository" \
  -F private=true
```

**Create issue:**
```bash
gh api repos/{owner}/{repo}/issues \
  -X POST \
  -f title="Bug report" \
  -f body="Description of the bug" \
  -F assignees='["username"]' \
  -F labels='["bug", "priority-high"]'
```

### PATCH Requests

**Update repository settings:**
```bash
gh api repos/{owner}/{repo} \
  -X PATCH \
  -F has_issues=true \
  -F has_wiki=false \
  -f description="Updated description"
```

### DELETE Requests

**Delete reference:**
```bash
gh api repos/{owner}/{repo}/git/refs/heads/feature-branch -X DELETE
```

## Field Types and Magic Conversion

### -f vs -F Flag Difference

**`-f` (--raw-field):** Always strings
```bash
gh api repos/{owner}/{repo}/issues \
  -X POST \
  -f title="Issue title"  # String: "Issue title"
```

**`-F` (--field):** Magic type conversion
```bash
gh api repos/{owner}/{repo}/issues \
  -X POST \
  -F private=true        # Boolean: true
  -F count=42            # Number: 42
  -F data=null           # Null: null
  -F items='["a","b"]'   # Array: ["a", "b"]
```

### Reading Values from Files

**Read field value from file:**
```bash
gh api repos/{owner}/{repo}/issues \
  -X POST \
  -f title="Bug report" \
  -F body=@issue-description.md  # @ prefix reads file
```

**Read from stdin:**
```bash
echo "Issue description" | gh api repos/{owner}/{repo}/issues \
  -X POST \
  -f title="Bug" \
  -F body=@-  # @- reads from stdin
```

### Nested Parameters

**Object fields:**
```bash
gh api repos/{owner}/{repo} \
  -X PATCH \
  -F security_and_analysis[secret_scanning][status]=enabled
```

**Array fields:**
```bash
gh api repos/{owner}/{repo}/issues \
  -X POST \
  -f title="Multiple assignees" \
  -F assignees[]=alice \
  -F assignees[]=bob
```

**Empty arrays:**
```bash
gh api repos/{owner}/{repo}/issues/123 \
  -X PATCH \
  -F assignees[]  # Empty array clears assignees
```

## Request Body from File

### JSON Payloads

**POST with JSON file:**
```bash
# payload.json
# {
#   "title": "New issue",
#   "body": "Description",
#   "labels": ["bug", "urgent"]
# }

gh api repos/{owner}/{repo}/issues --input payload.json
```

**PATCH with JSON:**
```bash
gh api repos/{owner}/{repo}/settings/branches/main/protection \
  --method PUT \
  --input protection-rules.json
```

### Read from stdin

```bash
cat issue.json | gh api repos/{owner}/{repo}/issues --input -
```

**Combine stdin with fields:**
```bash
# Fields go to query string when --input is used
echo '{"title":"Issue"}' | gh api repos/{owner}/{repo}/issues \
  --input - \
  --field state=open
```

## Pagination

### Automatic Pagination

**Fetch all pages:**
```bash
gh api repos/{owner}/{repo}/issues --paginate
```

**With processing:**
```bash
gh api repos/{owner}/{repo}/issues --paginate \
  --jq '.[] | {number: .number, title: .title}'
```

### Slurp All Pages into Array

```bash
gh api repos/{owner}/{repo}/issues --paginate --slurp
```

**Difference:**
- Without `--slurp`: Each page is separate JSON array
- With `--slurp`: All pages combined into single JSON array

### Manual Pagination

**Get specific page:**
```bash
gh api repos/{owner}/{repo}/issues --field page=2 --field per_page=100
```

**Follow Link headers:**
```bash
gh api repos/{owner}/{repo}/issues --include | grep "^link:"
```

## GraphQL Queries

### Basic GraphQL

**Syntax:**
```bash
gh api graphql -f query='
  query {
    viewer {
      login
      name
    }
  }
'
```

**With variables:**
```bash
gh api graphql \
  -F owner='{owner}' \
  -F name='{repo}' \
  -f query='
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        name
        description
        stargazerCount
      }
    }
  '
```

### Pagination in GraphQL

**Using cursor:**
```bash
gh api graphql -f query='
  query($endCursor: String) {
    repository(owner: "{owner}", name: "{repo}") {
      issues(first: 100, after: $endCursor) {
        nodes {
          number
          title
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
'
```

**Auto-paginate:**
```bash
gh api graphql --paginate -f query='
  query($endCursor: String) {
    viewer {
      repositories(first: 100, after: $endCursor) {
        nodes {
          nameWithOwner
        }
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
'
```

### Complex GraphQL Examples

**Get PR with review comments:**
```bash
gh api graphql -F owner='{owner}' -F repo='{repo}' -F number=123 -f query='
  query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $number) {
        title
        body
        reviews(first: 10) {
          nodes {
            author {
              login
            }
            state
            body
          }
        }
      }
    }
  }
'
```

**Get repository dependencies:**
```bash
gh api graphql -F owner='{owner}' -F repo='{repo}' -f query='
  query($owner: String!, $repo: String!) {
    repository(owner: $owner, name: $repo) {
      dependencyGraphManifests(first: 10) {
        nodes {
          filename
          dependencies(first: 50) {
            nodes {
              packageName
              requirements
            }
          }
        }
      }
    }
  }
'
```

## Output Formatting

### Using --jq Flag

**Extract specific fields:**
```bash
gh api repos/{owner}/{repo}/issues --jq '.[].title'
```

**Filter results:**
```bash
gh api repos/{owner}/{repo}/issues \
  --jq '.[] | select(.state == "open") | .number'
```

**Transform output:**
```bash
gh api repos/{owner}/{repo}/issues \
  --jq 'map({issue: .number, title: .title, author: .author.login})'
```

### Using --template Flag

**Go template format:**
```bash
gh api repos/{owner}/{repo}/issues --template '
{{range .}}
Issue #{{.number}}: {{.title}}
Author: {{.author.login}}
---
{{end}}
'
```

**With color:**
```bash
gh api repos/{owner}/{repo}/issues --template '
{{range .}}
{{.title | color "yellow"}} ({{.labels | pluck "name" | join ", " | color "blue"}})
{{end}}
'
```

## HTTP Headers

### Custom Headers

**Set Accept header:**
```bash
gh api repos/{owner}/{repo}/releases \
  -H "Accept: application/vnd.github.v3+json"
```

**Multiple headers:**
```bash
gh api repos/{owner}/{repo}/contents/README.md \
  -H "Accept: application/vnd.github.v3.raw" \
  -H "X-Custom-Header: value"
```

### API Previews

**Opt into preview features:**
```bash
gh api repos/{owner}/{repo}/topics \
  --preview mercy  # Topics API preview
```

**Multiple previews:**
```bash
gh api repos/{owner}/{repo} \
  --preview baptiste \
  --preview nebula
```

## Response Inspection

### Include HTTP Status and Headers

```bash
gh api repos/{owner}/{repo}/issues --include
```

**Output includes:**
```
HTTP/2.0 200 OK
content-type: application/json; charset=utf-8
x-ratelimit-remaining: 4999
...

[JSON response body]
```

### Verbose Output

```bash
gh api repos/{owner}/{repo}/issues --verbose
```

**Shows:**
- Complete HTTP request
- Request headers
- Response status
- Response headers
- Response body

## Authentication and Hostname

### Different GitHub Instance

**GitHub Enterprise:**
```bash
gh api repos/{owner}/{repo} --hostname github.company.com
```

**Environment variable:**
```bash
GH_HOST=github.company.com gh api repos/{owner}/{repo}
```

### Using Different Token

```bash
GH_TOKEN=ghp_xxxxx gh api user
```

## Rate Limiting

### Check Rate Limit

```bash
gh api rate_limit
```

**Extract remaining:**
```bash
gh api rate_limit --jq '.rate.remaining'
```

### Handle Rate Limit Errors

```bash
RESPONSE=$(gh api repos/{owner}/{repo}/issues 2>&1)
if echo "$RESPONSE" | grep -q "API rate limit exceeded"; then
  echo "Rate limited. Waiting..."
  sleep 3600
fi
```

## Caching Responses

### Cache API Responses

```bash
gh api repos/{owner}/{repo}/issues --cache 1h  # Cache for 1 hour
gh api repos/{owner}/{repo}/issues --cache 3600s  # Cache for 3600 seconds
```

**Use cases:**
- Repeated queries in scripts
- Development/testing
- Reduce API calls

## Common API Operations

### Repository Management

**List user repositories:**
```bash
gh api user/repos --jq '.[].full_name'
```

**Create repository from template:**
```bash
gh api repos/{template_owner}/{template_repo}/generate \
  -X POST \
  -f owner={owner} \
  -f name=new-repo-name \
  -F private=true
```

**Update repository settings:**
```bash
gh api repos/{owner}/{repo} \
  -X PATCH \
  -F allow_squash_merge=true \
  -F allow_merge_commit=false \
  -F allow_rebase_merge=false \
  -F delete_branch_on_merge=true
```

**List repository collaborators:**
```bash
gh api repos/{owner}/{repo}/collaborators --jq '.[].login'
```

**Add collaborator:**
```bash
gh api repos/{owner}/{repo}/collaborators/username \
  -X PUT \
  -f permission=push
```

### Branch Protection

**Get branch protection:**
```bash
gh api repos/{owner}/{repo}/branches/main/protection
```

**Update branch protection:**
```bash
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  --input - <<'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["ci/test", "ci/lint"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 2
  },
  "restrictions": null
}
EOF
```

### Labels

**List labels:**
```bash
gh api repos/{owner}/{repo}/labels --jq '.[].name'
```

**Create label:**
```bash
gh api repos/{owner}/{repo}/labels \
  -X POST \
  -f name=priority-high \
  -f color=d73a4a \
  -f description="High priority items"
```

**Bulk create labels:**
```bash
for label in bug enhancement question; do
  gh api repos/{owner}/{repo}/labels \
    -X POST \
    -f name="$label" \
    -f color=0e8a16
done
```

### Milestones

**List milestones:**
```bash
gh api repos/{owner}/{repo}/milestones
```

**Create milestone:**
```bash
gh api repos/{owner}/{repo}/milestones \
  -X POST \
  -f title="v2.0" \
  -f description="Version 2.0 release" \
  -f due_on=2024-12-31T23:59:59Z
```

### Webhooks

**List webhooks:**
```bash
gh api repos/{owner}/{repo}/hooks
```

**Create webhook:**
```bash
gh api repos/{owner}/{repo}/hooks \
  -X POST \
  --input - <<'EOF'
{
  "name": "web",
  "active": true,
  "events": ["push", "pull_request"],
  "config": {
    "url": "https://example.com/webhook",
    "content_type": "json",
    "secret": "super-secret-string"
  }
}
EOF
```

### Deploy Keys

**List deploy keys:**
```bash
gh api repos/{owner}/{repo}/keys
```

**Add deploy key:**
```bash
gh api repos/{owner}/{repo}/keys \
  -X POST \
  -f title="CI/CD Deploy Key" \
  -f key="$(cat ~/.ssh/id_rsa.pub)" \
  -F read_only=false
```

### Repository Topics

**Get topics:**
```bash
gh api repos/{owner}/{repo}/topics --preview mercy --jq '.names'
```

**Set topics:**
```bash
gh api repos/{owner}/{repo}/topics \
  --method PUT \
  --preview mercy \
  -F names='["javascript","nodejs","cli"]'
```

### Secrets and Variables

**List repository secrets:**
```bash
gh api repos/{owner}/{repo}/actions/secrets --jq '.secrets[].name'
```

**Create or update secret:**
```bash
# First, get the public key
PUBLIC_KEY=$(gh api repos/{owner}/{repo}/actions/secrets/public-key)
KEY=$(echo "$PUBLIC_KEY" | jq -r '.key')
KEY_ID=$(echo "$PUBLIC_KEY" | jq -r '.key_id')

# Encrypt secret value (requires libsodium)
# In practice, use gh secret set instead
gh secret set SECRET_NAME --body "secret_value"
```

**List variables:**
```bash
gh api repos/{owner}/{repo}/actions/variables --jq '.variables[].name'
```

## Advanced Patterns

### Batch Operations

**Close multiple issues:**
```bash
for issue in 123 124 125; do
  gh api repos/{owner}/{repo}/issues/$issue \
    -X PATCH \
    -f state=closed \
    -f state_reason=completed
done
```

**Add label to all open issues:**
```bash
gh api repos/{owner}/{repo}/issues --paginate --jq '.[].number' \
  | while read issue; do
    gh api repos/{owner}/{repo}/issues/$issue/labels \
      -X POST \
      -F labels='["needs-triage"]'
  done
```

### Conditional Operations

**Only merge if checks pass:**
```bash
PR=123
MERGEABLE=$(gh api repos/{owner}/{repo}/pulls/$PR --jq '.mergeable_state')

if [ "$MERGEABLE" = "clean" ]; then
  gh api repos/{owner}/{repo}/pulls/$PR/merge \
    -X PUT \
    -f merge_method=squash
else
  echo "PR not ready to merge: $MERGEABLE"
fi
```

### Error Handling

**Check response status:**
```bash
RESPONSE=$(gh api repos/{owner}/{repo} 2>&1)
if [ $? -eq 0 ]; then
  echo "Success"
else
  echo "Error: $RESPONSE"
fi
```

**Extract error message:**
```bash
ERROR=$(gh api repos/{owner}/{repo}/issues/99999 2>&1 | jq -r '.message')
echo "Error: $ERROR"
```

## Best Practices

1. **Use placeholders** (`{owner}`, `{repo}`, `{branch}`) for portability
2. **Prefer core commands** when available (`gh pr` over API for PRs)
3. **Use --jq** for filtering to reduce data transfer
4. **Cache responses** for repeated queries
5. **Handle pagination** for complete datasets
6. **Check rate limits** for batch operations
7. **Use GraphQL** for complex related data (fewer requests)
8. **Test with --verbose** to understand request/response
9. **Read from files** for complex payloads
10. **Check API docs** for endpoint details: https://docs.github.com/en/rest

## Troubleshooting

**404 Not Found:**
- Verify endpoint path
- Check repository name and owner
- Ensure resource exists

**401 Unauthorized:**
- Check authentication with `gh auth status`
- Verify token scopes

**403 Forbidden:**
- Check repository permissions
- Verify rate limit with `gh api rate_limit`
- Check if API requires preview header

**422 Validation Failed:**
- Review request body format
- Check required fields
- Validate field types

## Resources

- REST API Documentation: https://docs.github.com/en/rest
- GraphQL API Documentation: https://docs.github.com/en/graphql
- GraphQL Explorer: https://docs.github.com/en/graphql/overview/explorer
- Rate Limiting: https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting
