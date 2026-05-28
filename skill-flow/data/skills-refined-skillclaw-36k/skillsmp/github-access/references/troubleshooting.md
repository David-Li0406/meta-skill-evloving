# Troubleshooting GitHub API Authentication

This document covers common authentication issues when using the GitHub REST API with curl.

## Test Your Token

Before troubleshooting, verify that your token is working correctly:

```bash
# Test token with the /user endpoint
curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user
```

A successful response will show your user information. If you get an error, see the common issues below.

## Common Issues

### 401 Bad credentials

**Cause**: Token expired, invalid, or lacks required scopes

**Solutions**:
- Generate a new token at https://github.com/settings/tokens
- Ensure the token has the necessary scopes (repo, workflow, etc.)
- Verify the token string is copied correctly (no extra spaces or newlines)
- Check that `GH_TOKEN` environment variable is set correctly

### 403 Forbidden

**Cause**: Token valid but lacks permission for the resource

**Solutions**:
- Check that your token has access to the repository
- For private repositories, ensure the token has appropriate scopes
- For organization repositories, verify you have the necessary organization permissions
- Check if the repository has specific branch protection rules

### 404 Not Found

**Cause**: Repository is private and token can't access it, or resource doesn't exist

**Solutions**:
- Verify the repository name is correct (OWNER/REPO)
- Check that the repository exists and you have permission to view it
- Ensure you're not trying to access a deleted resource (issue, PR, etc.)
- For private repositories, verify your token has access

## Authorization Header Format

Both formats work for personal access tokens:

- `Authorization: token $GH_TOKEN` - Legacy format (recommended for consistency)
- `Authorization: Bearer $GH_TOKEN` - OAuth 2.0 standard

**Note**: If one format fails, try the other - some GitHub API configurations may prefer one over the other. The examples in this skill use `token` format for consistency and reliability.

## Rate Limiting

If you're making many requests, you might hit rate limits:

```bash
# Check rate limit status
curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: token $GH_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/rate_limit
```

Authenticated requests have a rate limit of 5,000 requests per hour.
