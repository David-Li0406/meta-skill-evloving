# Jira Authentication Guide

## Overview

The Jira integration uses Basic Authentication with API tokens to securely access Jira Cloud. This document covers setup, security best practices, and troubleshooting.

## Authentication Method

**Jira Cloud REST API v3** uses Basic Authentication:

```
Authorization: Basic base64(email:api_token)
```

**NOT** username/password (deprecated and insecure).

## Setup Instructions

### Step 1: Generate API Token

1. Log in to your Atlassian account
2. Visit: https://id.atlassian.com/manage-profile/security/api-tokens
3. Click **"Create API token"**
4. Give it a name (e.g., "PRISM Local Development")
5. Copy the generated token (you won't see it again!)

### Step 2: Configure Environment Variables

1. Navigate to your project repository root
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

3. Edit `.env` and add your credentials:
   ```env
   JIRA_EMAIL=your.email@resolve.io
   JIRA_API_TOKEN=your_generated_api_token_here
   ```

4. Verify `.env` is in `.gitignore` (it should be!)

### Step 3: Verify Configuration

Test your credentials:

```bash
# Unix/Linux/Mac
curl -u $JIRA_EMAIL:$JIRA_API_TOKEN \
  https://resolvesys.atlassian.net/rest/api/3/myself

# Windows PowerShell
$env:JIRA_EMAIL
$env:JIRA_API_TOKEN
curl.exe -u "${env:JIRA_EMAIL}:${env:JIRA_API_TOKEN}" `
  https://resolvesys.atlassian.net/rest/api/3/myself
```

**Expected Response**: JSON with your user details
**Error Response**: 401 Unauthorized (check credentials)

## core-config.yaml Configuration

The Jira configuration in [core-config.yaml](../../../core-config.yaml):

```yaml
jira:
  enabled: true
  baseUrl: https://resolvesys.atlassian.net
  email: ${JIRA_EMAIL}
  token: ${JIRA_API_TOKEN}
  defaultProject: PLAT
  issueKeyPattern: "[A-Z]+-\\d+"
```

**Field Descriptions**:
- `enabled`: Master switch for Jira integration
- `baseUrl`: Your Jira Cloud instance URL
- `email`: Environment variable reference for email
- `token`: Environment variable reference for API token
- `defaultProject`: Default project key for issue detection
- `issueKeyPattern`: Regex pattern for detecting issue keys

**Placeholders** (`${VARIABLE}`):
- Automatically replaced with environment variable values
- Keeps secrets out of version control
- Allows per-developer configuration

## Security Best Practices

### ✅ DO

**Store Credentials Securely:**
- Use environment variables (`JIRA_EMAIL`, `JIRA_API_TOKEN`)
- Use `.env` file for local development (gitignored)
- Use secure secrets management for production (if applicable)

**Protect API Tokens:**
- Treat API tokens like passwords
- Never commit to version control
- Rotate tokens periodically (every 90 days recommended)
- Use descriptive token names (e.g., "PRISM Dev - John Laptop")
- Revoke unused tokens immediately

**Limit Token Scope:**
- Use account with read-only Jira access if possible
- Create dedicated "service account" for integrations
- Request minimum necessary permissions

**In Code:**
- Never hardcode credentials in source files
- Never embed credentials in URLs (`https://user:pass@domain.com`)
- Use WebFetch tool which handles auth headers securely
- Never log credentials in debug output

### ❌ DON'T

**Never:**
- Commit `.env` file to git
- Hardcode credentials in code
- Share API tokens in chat, email, or docs
- Use passwords (use API tokens only)
- Embed credentials in URLs
- Log credentials in debug output
- Share credentials between developers (each gets their own)

**Avoid:**
- Using personal accounts for shared integrations
- Storing tokens in plaintext outside `.env`
- Reusing tokens across multiple projects
- Leaving old tokens active after switching machines

## WebFetch Authentication

Claude Code's WebFetch tool handles authentication automatically:

### How It Works

1. WebFetch reads `core-config.yaml`
2. Resolves `${JIRA_EMAIL}` and `${JIRA_API_TOKEN}` from environment
3. Constructs `Authorization: Basic base64(email:token)` header
4. Includes header in all Jira API requests
5. Credentials never exposed in logs or output

### Usage Example

```javascript
// You don't need to handle auth manually!
WebFetch({
  url: "https://resolvesys.atlassian.net/rest/api/3/issue/PLAT-123",
  prompt: "Extract issue details"
})

// WebFetch automatically:
// 1. Reads JIRA_EMAIL and JIRA_API_TOKEN from env
// 2. Adds Authorization header
// 3. Makes authenticated request
```

### What You Don't Need to Do

❌ **Don't do this** (WebFetch handles it):
```javascript
// WRONG - Don't manually construct auth
const auth = btoa(`${email}:${token}`);
const headers = { Authorization: `Basic ${auth}` };
```

✅ **Do this** (let WebFetch handle it):
```javascript
// RIGHT - Just provide the URL
WebFetch({ url: jiraUrl, prompt: "..." })
```

## Environment Variable Loading

### Local Development

**.env File** (in repository root):
```env
# Jira Integration
JIRA_EMAIL=john.doe@resolve.io
JIRA_API_TOKEN=ATATT3xFfGF0abc123xyz...

# Other services
GITHUB_TOKEN=ghp_abc123...
```

**Loading Priority**:
1. System environment variables (if set)
2. `.env` file in current directory
3. `.env` file in parent directories (searches up)

**dotenv Support**:
PRISM uses dotenv-style loading. Ensure your environment supports it.

### CI/CD / Production

For automated environments:

**GitHub Actions**:
```yaml
env:
  JIRA_EMAIL: ${{ secrets.JIRA_EMAIL }}
  JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
```

**Docker**:
```bash
docker run \
  -e JIRA_EMAIL=$JIRA_EMAIL \
  -e JIRA_API_TOKEN=$JIRA_API_TOKEN \
  your-image
```

**AWS/Cloud**:
Use secure secrets management (AWS Secrets Manager, etc.)

## Troubleshooting

### 401 Unauthorized

**Symptoms**:
- "Invalid credentials" error
- API returns 401 status code

**Causes**:
1. Incorrect email address
2. Incorrect or expired API token
3. Token revoked in Atlassian account
4. Using password instead of API token

**Solutions**:
1. Verify `JIRA_EMAIL` matches your Atlassian account email
2. Generate new API token and update `.env`
3. Check token is active at https://id.atlassian.com/manage-profile/security/api-tokens
4. Ensure using API token, not password

### 403 Forbidden

**Symptoms**:
- "Access denied" error
- API returns 403 status code

**Causes**:
1. Account lacks permission to view issue
2. Issue in restricted project
3. Account lacks Jira license

**Solutions**:
1. Verify you can view the issue in Jira web UI
2. Request access to the project from Jira admin
3. Ensure account has Jira Software license

### Environment Variables Not Found

**Symptoms**:
- `${JIRA_EMAIL}` not replaced in config
- Undefined variable errors

**Causes**:
1. `.env` file missing
2. `.env` in wrong location
3. Environment variables not exported
4. Typo in variable names

**Solutions**:
1. Create `.env` file in repository root
2. Verify `.env` contains `JIRA_EMAIL=...` and `JIRA_API_TOKEN=...`
3. Restart terminal/IDE to reload environment
4. Check variable names match exactly (case-sensitive)

**Test Variables**:
```bash
# Unix/Linux/Mac
echo $JIRA_EMAIL
echo $JIRA_API_TOKEN

# Windows PowerShell
echo $env:JIRA_EMAIL
echo $env:JIRA_API_TOKEN

# Windows CMD
echo %JIRA_EMAIL%
echo %JIRA_API_TOKEN%
```

### Rate Limiting (429)

**Symptoms**:
- "Rate limit exceeded" error
- API returns 429 status code

**Causes**:
- Too many requests in short time
- Exceeded 300 requests/minute limit

**Solutions**:
- Wait 60 seconds before retrying
- Implement session caching to reduce duplicate requests
- Batch operations when possible

## Permissions Required

**Minimum Jira Permissions**:
- **Browse Projects**: View issues in project
- **View Issues**: Read issue details
- **View Comments**: Read issue comments

**NOT Required**:
- Create/Edit issues (read-only integration)
- Assign issues
- Transition issues
- Admin permissions

**Recommended Setup**:
- Use account with "Jira Software" license
- Ensure access to all projects you need to integrate
- Consider dedicated "integration" account for team use

## Token Management

### Rotation Schedule

**Recommended**:
- Rotate tokens every 90 days
- Rotate immediately if:
  - Token potentially exposed
  - Developer leaves team
  - Device lost or stolen

**Rotation Process**:
1. Generate new token in Atlassian
2. Update `.env` with new token
3. Test integration
4. Revoke old token in Atlassian
5. Document rotation in team wiki

### Multiple Tokens

You can create multiple tokens for different purposes:

**Example**:
- "PRISM Dev - Laptop" (local development)
- "PRISM Dev - Desktop" (work machine)
- "PRISM CI/CD" (automated testing)

**Benefits**:
- Revoke specific token without affecting others
- Identify which integration is making requests
- Isolate security incidents

## Team Collaboration

### Individual Credentials

**Each developer should**:
1. Generate their own API token
2. Configure their own `.env` file
3. Never share tokens with teammates

**Why**:
- Audit trail (know who accessed what)
- Security (revoke individual access)
- Accountability (track API usage per person)

### Shared Documentation

**Team wiki should include**:
1. Link to this authentication guide
2. Link to generate API tokens
3. Where to put `.env` file
4. Who to contact for access issues
5. Jira projects available for integration

**Do NOT include**:
- Actual API tokens
- Actual email/password combinations
- Shared credentials

## References

- [Atlassian API Token Management](https://id.atlassian.com/manage-profile/security/api-tokens)
- [Jira Cloud REST API Authentication](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#authentication)
- [Basic Authentication RFC 7617](https://tools.ietf.org/html/rfc7617)
