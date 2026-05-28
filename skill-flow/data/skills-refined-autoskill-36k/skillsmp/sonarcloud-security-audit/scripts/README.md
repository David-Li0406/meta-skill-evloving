# SonarCloud Security Audit Scripts

This directory contains scripts for fetching and analyzing security issues from SonarCloud.

## Prerequisites

- Node.js v18 or higher (uses native `fetch` API)
- SonarCloud API token with read access to your organization

## Scripts

### fetch-security-issues.mjs

Main script that fetches all security vulnerabilities and hotspots for an organization.

**Usage:**
```bash
export SONARCLOUD_TOKEN="your_token_here"
node fetch-security-issues.mjs <organization> [output-file.csv]
```

**Example:**
```bash
node fetch-security-issues.mjs nasa-pds security-issues.csv
```

**Output:**
- CSV file with columns: Project, Type, Severity, Status, Rule, Message, Component, Line, Created, URL
- Console summary with counts and triage suggestions

**Features:**
- Automatic pagination for large result sets
- Rate limit handling (429 responses)
- Retry logic with exponential backoff
- Progress tracking for multi-project scans

## API Token Setup

### Generate Token

1. Go to https://sonarcloud.io/account/security
2. Generate a new token with read permissions
3. Copy the token (you won't be able to see it again)

### Set Environment Variable

**Temporary (current session):**
```bash
export SONARCLOUD_TOKEN="your_token_here"
```

**Permanent (add to ~/.bashrc or ~/.zshrc):**
```bash
echo 'export SONARCLOUD_TOKEN="your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

## Understanding the Output

### Vulnerability Columns

- **Project**: Repository/project key in SonarCloud
- **Type**: Always `VULNERABILITY` for security vulnerabilities
- **Severity**: `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO`
- **Status**: `OPEN`, `CONFIRMED`, `RESOLVED`, `REOPENED`, `CLOSED`
- **Rule**: SonarCloud rule ID (e.g., `java:S4426`, `javascript:S2068`)
- **Message**: Description of the security issue
- **Component**: File path relative to project root
- **Line**: Line number where issue occurs
- **Created**: ISO 8601 timestamp of when issue was detected
- **URL**: Direct link to issue in SonarCloud UI

### Security Hotspot Columns

- **Project**: Repository/project key
- **Type**: Always `SECURITY_HOTSPOT`
- **Severity**: Empty (hotspots don't have severity until reviewed)
- **Status**: `TO_REVIEW`, `REVIEWED`, `ACKNOWLEDGED`, `FIXED`
- **Rule**: Rule ID for the security-sensitive code pattern
- **Message**: Description of what needs to be reviewed
- **Component**: File path
- **Line**: Line number
- **Created**: Detection timestamp
- **URL**: Direct link to hotspot in SonarCloud UI

### Difference: Vulnerabilities vs Hotspots

**Vulnerabilities:**
- Confirmed security issues that need to be fixed
- Have assigned severity levels
- Directly impact security posture

**Security Hotspots:**
- Security-sensitive code that requires manual review
- May or may not be actual vulnerabilities
- Developer must assess if remediation is needed

## Triage Workflow

1. **Import CSV** into your preferred tool (Excel, Google Sheets, Jira, etc.)

2. **Filter by Severity:**
   ```
   BLOCKER → Fix immediately
   CRITICAL → Fix in current sprint
   MAJOR → Fix in next sprint
   MINOR/INFO → Backlog
   ```

3. **Group by Rule** to find patterns:
   - Same rule appearing multiple times = bulk fix opportunity
   - Create team guidelines to prevent recurrence

4. **Assign to Teams** based on Component (file path):
   - Backend issues → backend team
   - Frontend issues → frontend team
   - Infrastructure → DevOps team

5. **Track Progress** by updating Status in your tracking system

## Troubleshooting

### "401 Unauthorized"
- Token expired or invalid
- Token doesn't have access to organization
- Regenerate token and update environment variable

### "429 Rate Limit"
- Script automatically waits 60 seconds
- If persistent, reduce projects or run during off-peak hours

### "No issues found"
- Good news! Your projects are clean
- OR projects haven't been analyzed yet
- Check SonarCloud dashboard to confirm

### Script hangs/times out
- Large organizations (50+ projects) may take 10-15 minutes
- Monitor console output to track progress
- Can interrupt (Ctrl+C) and restart - script handles partial runs

## Advanced Usage

### Filter by Severity

Edit `fetch-security-issues.mjs` to filter specific severities:

```javascript
// After line 140, add:
if (!['BLOCKER', 'CRITICAL'].includes(issue.severity)) {
  return; // Skip low severity issues
}
```

### Date Range Filtering

Add `createdAfter` parameter to API calls:

```javascript
const data = await fetchSonarCloud('/issues/search', {
  organization,
  componentKeys: projectKey,
  types: 'VULNERABILITY',
  createdAfter: '2025-01-01', // YYYY-MM-DD
  p: page,
  ps: pageSize
});
```

### JSON Output

Replace `exportToCSV()` call with:

```javascript
writeFileSync('output.json', JSON.stringify(allRows, null, 2));
```

## API Documentation

- **SonarCloud Web API**: https://sonarcloud.io/web_api
- **Projects**: `/api/projects/search`
- **Issues**: `/api/issues/search`
- **Hotspots**: `/api/hotspots/search`

## Rate Limits

SonarCloud enforces rate limits on API calls. The script includes:
- Automatic retry with exponential backoff
- 60-second wait on 429 responses
- Small delays between project scans (500ms)

This should handle most use cases without hitting limits.
