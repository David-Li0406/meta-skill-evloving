# Atlassian Jira

**Category**: business-tools
**Description**: Project and issue tracking platform
**Homepage**: https://atlassian.com/software/jira

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Jira JavaScript packages*

- `jira-client` - Jira API client
- `jira.js` - Modern Jira client
- `@atlassian/aui` - Atlassian UI kit
- `@forge/api` - Atlassian Forge API

#### PYPI
*Jira Python packages*

- `jira` - Official JIRA Python library
- `atlassian-python-api` - Atlassian API wrapper

#### RUBYGEMS
*Jira Ruby packages*

- `jira-ruby` - Ruby client

#### GO
*Jira Go packages*

- `github.com/andygrunwald/go-jira` - Go Jira client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Jira usage*

- `atlassian-connect.json` - Connect app manifest
- `.jira.d/` - Jira CLI configuration
- `manifest.yml` - Forge app manifest

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]jira\.js['"]`
- jira.js import
- Example: `import { Version3Client } from 'jira.js';`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+jira\s+import`
- JIRA Python import
- Example: `from jira import JIRA`

**Pattern**: `^from\s+atlassian\s+import`
- Atlassian API import
- Example: `from atlassian import Jira`

### Code Patterns

**Pattern**: `atlassian\.net|atlassian\.com|jira\.[a-z0-9-]+\.(com|net)`
- Atlassian/Jira URLs
- Example: `https://mycompany.atlassian.net`

**Pattern**: `JIRA_|ATLASSIAN_`
- Jira/Atlassian environment variables
- Example: `JIRA_API_TOKEN`

**Pattern**: `/rest/api/[0-9]+/|/rest/agile/`
- Jira REST API endpoints
- Example: `/rest/api/3/issue`

**Pattern**: `[A-Z]+-[0-9]+`
- Jira issue key format
- Example: `PROJ-123`

---

## Environment Variables

- `JIRA_URL` - Jira instance URL
- `JIRA_USERNAME` - Jira username/email
- `JIRA_API_TOKEN` - API token
- `JIRA_PASSWORD` - Password (deprecated)
- `ATLASSIAN_API_TOKEN` - Atlassian API token
- `JIRA_PROJECT_KEY` - Default project key

## Detection Notes

- Cloud uses .atlassian.net domain
- Server/DC uses custom domains
- API tokens for cloud authentication
- Basic auth with API token for REST API
- Forge for app development

---

## Secrets Detection

### Credentials

#### Jira/Atlassian API Token
**Pattern**: `(?:jira|JIRA|atlassian|ATLASSIAN).*(?:api[_-]?token|API[_-]?TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9]{24})['"]?`
**Severity**: critical
**Description**: Atlassian API token
**Example**: `JIRA_API_TOKEN=abc123def456...`

#### Jira OAuth Token
**Pattern**: `(?:jira|JIRA|atlassian|ATLASSIAN).*(?:oauth[_-]?token|access[_-]?token)\s*[=:]\s*['"]?([a-zA-Z0-9_-]+)['"]?`
**Severity**: critical
**Description**: Jira OAuth access token

### Validation

#### API Documentation
- **REST API v3**: https://developer.atlassian.com/cloud/jira/platform/rest/v3/
- **Authentication**: https://developer.atlassian.com/cloud/jira/platform/basic-auth-for-rest-apis/

---

## TIER 3: Configuration Extraction

### Instance URL Extraction

**Pattern**: `(?:url|JIRA_URL|baseUrl)\s*[=:]\s*['"]?(https?://[^\s'"]+\.atlassian\.net|https?://[^\s'"]+/jira)['"]?`
- Jira instance URL
- Extracts: `jira_url`

### Project Key Extraction

**Pattern**: `(?:project|projectKey|JIRA_PROJECT)\s*[=:]\s*['"]?([A-Z][A-Z0-9]{1,9})['"]?`
- Jira project key
- Extracts: `project_key`
- Example: `PROJ`
