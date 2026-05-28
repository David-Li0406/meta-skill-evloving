# Slack

**Category**: business-tools
**Description**: Business communication and collaboration platform
**Homepage**: https://slack.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Slack JavaScript packages*

- `@slack/bolt` - Slack Bolt framework
- `@slack/web-api` - Web API client
- `@slack/events-api` - Events API
- `@slack/interactive-messages` - Interactive messages
- `@slack/webhook` - Incoming webhooks
- `@slack/rtm-api` - Real-time messaging

#### PYPI
*Slack Python packages*

- `slack-sdk` - Official Python SDK
- `slack-bolt` - Bolt framework for Python
- `slackclient` - Legacy Python client

#### GO
*Slack Go packages*

- `github.com/slack-go/slack` - Go Slack client

#### RUBYGEMS
*Slack Ruby packages*

- `slack-ruby-client` - Ruby client
- `slack-ruby-bot` - Bot framework

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Slack usage*

- `manifest.json` - Slack app manifest
- `slack.json` - Slack configuration

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@slack/bolt['"]`
- Slack Bolt import
- Example: `import { App } from '@slack/bolt';`

**Pattern**: `from\s+['"]@slack/web-api['"]`
- Web API import
- Example: `import { WebClient } from '@slack/web-api';`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+slack_sdk\s+import`
- Slack SDK import
- Example: `from slack_sdk import WebClient`

**Pattern**: `^from\s+slack_bolt\s+import`
- Slack Bolt import
- Example: `from slack_bolt import App`

### Code Patterns

**Pattern**: `slack\.com|api\.slack\.com|hooks\.slack\.com`
- Slack URLs

**Pattern**: `SLACK_|slack_`
- Slack environment variables
- Example: `SLACK_BOT_TOKEN`

**Pattern**: `xoxb-[0-9]+-[0-9]+-[a-zA-Z0-9]+`
- Slack bot token format

**Pattern**: `xoxp-[0-9]+-[0-9]+-[0-9]+-[a-f0-9]+`
- Slack user token format

**Pattern**: `xapp-[0-9]+-[A-Z0-9]+-[0-9]+-[a-z0-9]+`
- Slack app token format

**Pattern**: `hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[a-zA-Z0-9]+`
- Slack webhook URL

**Pattern**: `chat\.postMessage|conversations\.list|users\.list`
- Slack API methods

---

## Environment Variables

- `SLACK_BOT_TOKEN` - Bot token (xoxb-)
- `SLACK_USER_TOKEN` - User token (xoxp-)
- `SLACK_APP_TOKEN` - App token (xapp-)
- `SLACK_SIGNING_SECRET` - Request signing secret
- `SLACK_CLIENT_ID` - OAuth client ID
- `SLACK_CLIENT_SECRET` - OAuth client secret
- `SLACK_WEBHOOK_URL` - Incoming webhook URL

## Detection Notes

- Bot tokens start with xoxb-
- User tokens start with xoxp-
- App-level tokens start with xapp-
- Signing secret for request verification
- Bolt is the recommended framework

---

## Secrets Detection

### Tokens and Secrets

#### Slack Bot Token
**Pattern**: `xoxb-[0-9]+-[0-9]+-[a-zA-Z0-9]{24}`
**Severity**: critical
**Description**: Slack bot user OAuth token
**Example**: `xoxb-123456789-987654321-abc123...`

#### Slack User Token
**Pattern**: `xoxp-[0-9]+-[0-9]+-[0-9]+-[a-f0-9]{32}`
**Severity**: critical
**Description**: Slack user OAuth token
**Example**: `xoxp-0000000000-0000000000-0000000000-EXAMPLE`

#### Slack App Token
**Pattern**: `xapp-[0-9]+-[A-Z0-9]+-[0-9]+-[a-z0-9]{64}`
**Severity**: critical
**Description**: Slack app-level token
**Example**: `xapp-1-A0123456789-123456789-abc123...`

#### Slack Webhook URL
**Pattern**: `https://hooks\.slack\.com/services/T[A-Z0-9]+/B[A-Z0-9]+/[a-zA-Z0-9]{24}`
**Severity**: high
**Description**: Slack incoming webhook URL
**Example**: `https://hooks.slack.com/services/T00000000/B00000000/abc123...`

#### Slack Signing Secret
**Pattern**: `(?:slack|SLACK).*(?:signing[_-]?secret|SIGNING[_-]?SECRET)\s*[=:]\s*['"]?([a-f0-9]{32})['"]?`
**Severity**: critical
**Description**: Slack request signing secret

#### Slack Client Secret
**Pattern**: `(?:slack|SLACK).*(?:client[_-]?secret|CLIENT[_-]?SECRET)\s*[=:]\s*['"]?([a-f0-9]{32})['"]?`
**Severity**: critical
**Description**: Slack OAuth client secret

### Validation

#### API Documentation
- **Web API**: https://api.slack.com/web
- **Bolt**: https://api.slack.com/bolt

#### Validation Endpoint
**API**: Auth Test
**Endpoint**: `https://slack.com/api/auth.test`
**Method**: POST
**Headers**: `Authorization: Bearer {token}`
**Purpose**: Validates token

```bash
curl -X POST "https://slack.com/api/auth.test" \
     -H "Authorization: Bearer $SLACK_BOT_TOKEN"
```

---

## TIER 3: Configuration Extraction

### Team/Workspace ID Extraction

**Pattern**: `xox[bp]-([0-9]+)-`
- Workspace ID from token
- Extracts: `workspace_id`

### Webhook Channel Extraction

**Pattern**: `hooks\.slack\.com/services/(T[A-Z0-9]+)/`
- Team ID from webhook
- Extracts: `team_id`
