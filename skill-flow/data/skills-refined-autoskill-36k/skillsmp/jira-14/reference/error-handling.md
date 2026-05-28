# Jira Error Handling Guide

## Overview

This document provides comprehensive guidance on handling errors when integrating with Jira REST API, including error detection, graceful degradation, and user communication.

## Error Handling Principles

### 1. Graceful Degradation

**Never halt the entire workflow** due to Jira issues:
- Inform user of Jira unavailability
- Offer to proceed without Jira context
- Log error details for troubleshooting
- Continue with requested task when possible

### 2. User-Friendly Messages

**Avoid technical jargon** in user-facing messages:
- ❌ "HTTP 403 Forbidden - Insufficient scopes"
- ✅ "Access denied to PLAT-123. Please check Jira permissions."

### 3. Actionable Guidance

**Tell users what to do next**:
- Verify issue key spelling
- Check Jira permissions
- Contact Jira admin
- Proceed without Jira context
- Retry after waiting

### 4. Privacy & Security

**Never expose sensitive details**:
- Don't show API tokens in error messages
- Don't log credentials in debug output
- Don't reveal internal system details to users

## HTTP Status Codes

### 400 Bad Request

**Meaning**: Invalid request syntax or parameters

**Common Causes**:
- Invalid JQL syntax in search queries
- Malformed JSON in request body (not applicable for read-only)
- Invalid issue key format

**Example Scenarios**:

**Invalid JQL**:
```
URL: /rest/api/3/search?jql=invalid syntax here
Error: JQL query is invalid
```

**User Message**:
```markdown
❌ Invalid search query. Please check your JQL syntax.

You searched for: "invalid syntax here"

Common JQL format:
- project = PLAT AND type = Bug
- assignee = currentUser()
- status != Done
```

**Handling Code**:
```javascript
if (response.status === 400) {
  displayMessage(`
    Invalid Jira search query. The JQL syntax may be incorrect.

    Would you like to:
    1. Try a simpler search
    2. View JQL examples
    3. Proceed without searching
  `);
  // Offer alternatives, don't halt
}
```

### 401 Unauthorized

**Meaning**: Missing, invalid, or expired credentials

**Common Causes**:
- API token not set in environment
- Incorrect email address
- Expired or revoked API token
- Using password instead of API token

**Example Scenarios**:

**Missing Credentials**:
```
Error: JIRA_EMAIL or JIRA_API_TOKEN not found in environment
```

**User Message**:
```markdown
❌ Jira integration not configured.

To enable Jira integration:
1. Generate API token: https://id.atlassian.com/manage-profile/security/api-tokens
2. Add to .env file:
   ```
   JIRA_EMAIL=your.email@resolve.io
   JIRA_API_TOKEN=your_token_here
   ```
3. Restart your terminal/IDE

For now, I'll proceed without Jira context.
```

**Invalid Credentials**:
```
Error: HTTP 401 from Jira API
```

**User Message**:
```markdown
❌ Jira authentication failed. Your credentials may be incorrect or expired.

Please verify:
- JIRA_EMAIL matches your Atlassian account email
- JIRA_API_TOKEN is a valid, active API token
- Token hasn't been revoked

Generate new token: https://id.atlassian.com/manage-profile/security/api-tokens

Proceeding without Jira context for now.
```

**Handling Code**:
```javascript
if (response.status === 401) {
  // Check if credentials are configured at all
  if (!hasJiraCredentials()) {
    displayMessage("Jira integration not configured. See setup instructions.");
  } else {
    displayMessage("Jira authentication failed. Please verify your credentials.");
  }

  // Continue workflow without Jira
  return null; // Indicate no Jira data available
}
```

### 403 Forbidden

**Meaning**: Authenticated but lacks permission

**Common Causes**:
- User lacks permission to view issue
- Issue in restricted project
- User lacks Jira license
- Project permissions changed

**Example Scenarios**:

**Issue in Restricted Project**:
```
Error: You do not have permission to view this issue
Issue: PLAT-123
```

**User Message**:
```markdown
❌ Access denied to [PLAT-123](https://resolvesys.atlassian.net/browse/PLAT-123).

This could mean:
- The issue is in a restricted project
- You don't have permission to view this issue
- The project permissions recently changed

Please:
- Verify you can access the issue in Jira web UI
- Request access from your Jira administrator
- Double-check the issue key

Would you like to proceed without this issue's context?
```

**Handling Code**:
```javascript
if (response.status === 403) {
  displayMessage(`
    Access denied to ${issueKey}.

    You may not have permission to view this issue.
    You can still view it in Jira web UI if accessible:
    ${jiraUrl}/browse/${issueKey}

    Proceed without Jira context? (y/n)
  `);

  // Wait for user decision
  // Continue without Jira or halt if user requests
}
```

### 404 Not Found

**Meaning**: Issue does not exist

**Common Causes**:
- Typo in issue key
- Issue was deleted
- Issue moved to different project (key changed)
- Wrong Jira instance

**Example Scenarios**:

**Non-Existent Issue**:
```
Error: Issue does not exist
Issue: PLAT-9999
```

**User Message**:
```markdown
❌ Could not find Jira issue [PLAT-9999](https://resolvesys.atlassian.net/browse/PLAT-9999).

Possible reasons:
- Typo in issue key (check spelling and number)
- Issue was deleted or moved
- Issue is in a different project

Would you like to:
1. Search for similar issues
2. Verify the issue key
3. Proceed without Jira context
```

**Typo Detection**:
```javascript
if (response.status === 404) {
  // Suggest likely corrections
  const suggestions = findSimilarIssueKeys(issueKey);

  displayMessage(`
    Issue ${issueKey} not found.

    Did you mean:
    ${suggestions.map(s => `- ${s}`).join('\n')}

    Or proceed without Jira context?
  `);
}
```

### 429 Too Many Requests

**Meaning**: Rate limit exceeded

**Common Causes**:
- Exceeded 300 requests per minute (per user)
- Multiple rapid fetches in short time
- Shared API token hitting combined limits

**Example Scenarios**:

**Rate Limit Hit**:
```
Error: Rate limit exceeded
Retry-After: 60 seconds
```

**User Message**:
```markdown
⏱️ Jira rate limit reached. Please wait a moment.

Jira Cloud limits requests to 300 per minute per user.

I'll automatically retry in 60 seconds, or you can:
- Wait and try again manually
- Proceed without fetching additional Jira issues
- Use cached issue data if available
```

**Handling Code**:
```javascript
if (response.status === 429) {
  const retryAfter = response.headers['Retry-After'] || 60;

  displayMessage(`
    Jira rate limit exceeded.
    Waiting ${retryAfter} seconds before retry...
  `);

  // Implement exponential backoff
  await sleep(retryAfter * 1000);

  // Retry request
  return retryRequest(url, maxRetries - 1);
}
```

**Prevention**:
- Cache fetched issues for conversation session
- Batch operations when possible
- Avoid fetching same issue multiple times
- Use search queries to fetch multiple issues at once

### 500 Internal Server Error

**Meaning**: Jira service error

**Common Causes**:
- Jira service temporarily down
- Database issues on Jira side
- Unexpected server error
- Maintenance window

**Example Scenarios**:

**Service Outage**:
```
Error: HTTP 500 Internal Server Error
```

**User Message**:
```markdown
⚠️ Jira service error. The Jira server may be temporarily unavailable.

This is typically a temporary issue on Jira's side.

You can:
- Check Jira status: https://status.atlassian.com/
- Retry in a few minutes
- Proceed without Jira context for now

I'll continue with your request using available information.
```

**Handling Code**:
```javascript
if (response.status >= 500) {
  displayMessage(`
    Jira service is temporarily unavailable.
    Check status: https://status.atlassian.com/

    Proceeding without Jira context.
  `);

  // Log error for troubleshooting
  logError('Jira 500 error', { issueKey, timestamp: new Date() });

  // Continue workflow without Jira
  return null;
}
```

### 502/503/504 Gateway/Service Errors

**Meaning**: Jira proxy or gateway issues

**Common Causes**:
- Network connectivity issues
- Jira proxy/gateway timeout
- Temporary service degradation

**User Message**:
```markdown
⚠️ Unable to reach Jira. Network or service issue detected.

This is usually temporary. You can:
- Retry in a few moments
- Check your network connection
- Check Jira status: https://status.atlassian.com/
- Proceed without Jira context

Continuing with available information...
```

## Network Errors

### Connection Timeout

**Meaning**: Request took too long to complete

**User Message**:
```markdown
⏱️ Jira request timed out. The service may be slow or unreachable.

You can:
- Retry the request
- Check your network connection
- Proceed without Jira context

Continuing without Jira data...
```

**Handling Code**:
```javascript
try {
  const response = await fetchWithTimeout(url, 30000); // 30s timeout
} catch (error) {
  if (error.name === 'TimeoutError') {
    displayMessage('Jira request timed out. Proceeding without Jira context.');
    return null;
  }
  throw error;
}
```

### Connection Refused

**Meaning**: Cannot connect to Jira server

**User Message**:
```markdown
❌ Cannot connect to Jira. Network issue detected.

Please check:
- Your internet connection
- VPN connection (if required)
- Firewall settings
- Jira base URL in core-config.yaml

Proceeding without Jira integration.
```

### DNS Resolution Failed

**Meaning**: Cannot resolve Jira hostname

**User Message**:
```markdown
❌ Cannot resolve Jira hostname.

Please verify:
- Jira base URL in core-config.yaml: https://resolvesys.atlassian.net
- DNS settings
- Network connectivity

Proceeding without Jira context.
```

## Configuration Errors

### Missing Configuration

**Scenario**: Jira not configured in core-config.yaml

**Detection**:
```javascript
if (!config.jira || !config.jira.enabled) {
  // Jira integration disabled or not configured
}
```

**User Message**:
```markdown
ℹ️ Jira integration is not enabled.

To enable:
1. Set `jira.enabled: true` in core-config.yaml
2. Configure JIRA_EMAIL and JIRA_API_TOKEN in .env
3. See: .prism/skills/jira/reference/authentication.md

Proceeding without Jira integration.
```

### Invalid Base URL

**Scenario**: Malformed Jira base URL

**User Message**:
```markdown
❌ Invalid Jira base URL in configuration.

Current: {current_url}
Expected format: https://your-domain.atlassian.net

Please correct in core-config.yaml.
```

### Missing Environment Variables

**Scenario**: JIRA_EMAIL or JIRA_API_TOKEN not set

**Detection**:
```javascript
if (!process.env.JIRA_EMAIL || !process.env.JIRA_API_TOKEN) {
  // Credentials not configured
}
```

**User Message**:
```markdown
❌ Jira credentials not configured.

Required environment variables:
- JIRA_EMAIL
- JIRA_API_TOKEN

Setup instructions: .prism/skills/jira/reference/authentication.md

Proceeding without Jira integration.
```

## Issue-Specific Errors

### Invalid Issue Key Format

**Scenario**: Issue key doesn't match expected pattern

**Detection**:
```javascript
const issueKeyPattern = /^[A-Z]+-\d+$/;
if (!issueKeyPattern.test(issueKey)) {
  // Invalid format
}
```

**User Message**:
```markdown
❌ Invalid issue key format: "{issueKey}"

Jira issue keys follow this pattern:
- PROJECT-123
- ABC-456
- PLAT-789

Format: {PROJECT_KEY}-{NUMBER}
All letters uppercase, hyphen, then numbers.
```

### Custom Field Not Found

**Scenario**: Expected custom field missing from issue

**Handling**:
```javascript
const storyPoints = issue.fields.customfield_10016 ||
                    issue.fields.storyPoints ||
                    null;

if (!storyPoints) {
  // Handle gracefully - don't error, just note missing
  displayField('Story Points', 'Not set');
}
```

**User Message**:
```markdown
## [PLAT-123] Story Title

...
- **Story Points**: Not set
...
```

## Error Recovery Strategies

### 1. Retry with Exponential Backoff

For transient errors (429, 500, 503):

```javascript
async function fetchWithRetry(url, maxRetries = 3) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url);

      if (response.ok) {
        return response;
      }

      // Retry on 429, 500, 503
      if ([429, 500, 503].includes(response.status)) {
        const delay = Math.pow(2, i) * 1000; // 1s, 2s, 4s
        await sleep(delay);
        continue;
      }

      // Don't retry on 401, 403, 404
      return response;

    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(Math.pow(2, i) * 1000);
    }
  }
}
```

### 2. Fallback to Cached Data

If fresh fetch fails, use cached data:

```javascript
try {
  const freshData = await fetchIssue(issueKey);
  cacheIssue(issueKey, freshData);
  return freshData;
} catch (error) {
  const cached = getCachedIssue(issueKey);
  if (cached) {
    displayMessage('⚠️ Using cached issue data (Jira temporarily unavailable)');
    return cached;
  }
  // No cached data, proceed without Jira
  return null;
}
```

### 3. Partial Success

For batch operations, handle individual failures:

```javascript
async function fetchMultipleIssues(issueKeys) {
  const results = [];
  const failed = [];

  for (const key of issueKeys) {
    try {
      const issue = await fetchIssue(key);
      results.push(issue);
    } catch (error) {
      failed.push({ key, error: error.message });
    }
  }

  if (failed.length > 0) {
    displayMessage(`
      ⚠️ Failed to fetch ${failed.length} issues:
      ${failed.map(f => `- ${f.key}: ${f.error}`).join('\n')}

      Continuing with ${results.length} successfully fetched issues.
    `);
  }

  return results;
}
```

### 4. Degrade Feature

If Jira unavailable, continue with reduced functionality:

```javascript
if (!jiraAvailable) {
  displayMessage(`
    ℹ️ Jira integration unavailable. Continuing with limited context.

    Please provide issue details manually if needed:
    - Summary
    - Acceptance Criteria
    - Technical requirements
  `);

  // Continue workflow, prompt user for manual input
  return promptForManualIssueDetails();
}
```

## Logging & Debugging

### User-Facing Messages

**Keep concise and actionable**:
```markdown
✅ Good: "Access denied to PLAT-123. Please check permissions."
❌ Bad: "HTTPError: 403 Forbidden - insufficient_scope - user lacks jira.issue.read"
```

### Debug Logging

**Log details for troubleshooting** (not shown to user):

```javascript
function logJiraError(error, context) {
  console.error('[Jira Integration Error]', {
    timestamp: new Date().toISOString(),
    issueKey: context.issueKey,
    url: context.url,
    status: error.status,
    message: error.message,
    // Never log credentials!
  });
}
```

### Error Telemetry

**Track error patterns** for improvement:

```javascript
function trackJiraError(errorType) {
  // Increment error counter
  // Store in session metrics
  // Help identify systemic issues
}
```

## Testing Error Scenarios

### Manual Testing

Test each error condition:

```bash
# 401 - Invalid credentials
JIRA_EMAIL=wrong@email.com JIRA_API_TOKEN=invalid jira PLAT-123

# 403 - Access denied (use issue you don't have access to)
jira RESTRICTED-999

# 404 - Not found
jira PLAT-99999999

# Invalid format
jira plat-123
jira PLAT123
jira 123
```

### Automated Testing

Mock error responses:

```javascript
describe('Jira Error Handling', () => {
  test('401 shows auth help message', async () => {
    mockFetch.mockResolvedValue({ status: 401 });
    const result = await fetchIssue('PLAT-123');
    expect(result).toBeNull();
    expect(displayedMessage).toContain('authentication failed');
  });

  test('404 offers to search', async () => {
    mockFetch.mockResolvedValue({ status: 404 });
    await fetchIssue('PLAT-999');
    expect(displayedMessage).toContain('search for similar issues');
  });
});
```

## Best Practices Summary

### ✅ DO

- Provide clear, actionable error messages
- Degrade gracefully (never halt entire workflow)
- Offer alternatives (search, manual input, proceed without)
- Cache data to reduce API calls and handle failures
- Log errors for debugging (without exposing credentials)
- Retry transient errors with exponential backoff
- Respect rate limits

### ❌ DON'T

- Expose API tokens or credentials in errors
- Show technical jargon to users
- Halt workflow on Jira errors
- Retry non-transient errors (401, 403, 404)
- Ignore errors silently
- Spam API with rapid retries
- Assume Jira is always available

## References

- [Jira REST API Errors](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/#error-responses)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [Atlassian Status Page](https://status.atlassian.com/)
