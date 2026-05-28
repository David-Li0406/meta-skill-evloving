# Zendesk

**Category**: business-tools
**Description**: Customer service and engagement platform
**Homepage**: https://zendesk.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Zendesk JavaScript packages*

- `node-zendesk` - Node.js Zendesk client
- `zendesk-node-api` - Alternative Node.js client
- `@zendesk/sell-zaf-app-toolbox` - Zendesk App Framework

#### PYPI
*Zendesk Python packages*

- `zenpy` - Python Zendesk client
- `zdesk` - Alternative Python client

#### RUBYGEMS
*Zendesk Ruby packages*

- `zendesk_api` - Official Ruby client
- `zendesk2` - Alternative Ruby client

#### GO
*Zendesk Go packages*

- `github.com/nukosuke/go-zendesk` - Go Zendesk client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Zendesk usage*

- `manifest.json` - Zendesk App manifest
- `zcli.apps.config.json` - Zendesk CLI configuration

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `require\(['"]node-zendesk['"]\)`
- node-zendesk require
- Example: `const zendesk = require('node-zendesk');`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+zenpy\s+import`
- zenpy import
- Example: `from zenpy import Zenpy`

**Pattern**: `^import\s+zenpy`
- zenpy import
- Example: `import zenpy`

### Code Patterns

**Pattern**: `\.zendesk\.com`
- Zendesk URLs
- Example: `https://mycompany.zendesk.com`

**Pattern**: `ZENDESK_|ZD_`
- Zendesk environment variables
- Example: `ZENDESK_API_TOKEN`

**Pattern**: `/api/v2/|/api/sunshine/`
- Zendesk API endpoints
- Example: `https://mycompany.zendesk.com/api/v2/tickets`

**Pattern**: `zendesk\.createClient|Zenpy\(`
- Zendesk client creation
- Example: `zendesk.createClient({...})`

---

## Environment Variables

- `ZENDESK_SUBDOMAIN` - Zendesk subdomain
- `ZENDESK_EMAIL` - Zendesk user email
- `ZENDESK_API_TOKEN` - API token
- `ZENDESK_PASSWORD` - User password
- `ZENDESK_OAUTH_TOKEN` - OAuth access token
- `ZD_SUBDOMAIN` - Short form subdomain
- `ZD_TOKEN` - Short form token

## Detection Notes

- Subdomain identifies the Zendesk account
- API tokens are associated with user accounts
- OAuth for installed apps
- Support, Chat, Sell, and Sunshine APIs available

---

## Secrets Detection

### API Keys and Tokens

#### Zendesk API Token
**Pattern**: `(?:zendesk|ZENDESK|ZD).*(?:api[_-]?token|API[_-]?TOKEN|token)\s*[=:]\s*['"]?([a-zA-Z0-9]{40})['"]?`
**Severity**: critical
**Description**: Zendesk API token
**Example**: `ZENDESK_API_TOKEN=abc123def456...`

#### Zendesk OAuth Token
**Pattern**: `(?:zendesk|ZENDESK|ZD).*(?:oauth[_-]?token|access[_-]?token)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{40,})['"]?`
**Severity**: critical
**Description**: Zendesk OAuth access token

### Validation

#### API Documentation
- **API Reference**: https://developer.zendesk.com/api-reference/
- **Authentication**: https://developer.zendesk.com/api-reference/introduction/security-and-auth/

#### Validation Endpoint
**API**: Current User
**Endpoint**: `https://{subdomain}.zendesk.com/api/v2/users/me.json`
**Method**: GET
**Headers**: `Authorization: Basic {base64(email/token:api_token)}`
**Purpose**: Validates credentials and returns user info

---

## TIER 3: Configuration Extraction

### Subdomain Extraction

**Pattern**: `(?:subdomain|ZENDESK_SUBDOMAIN)\s*[=:]\s*['"]?([a-z0-9-]+)['"]?`
- Zendesk subdomain
- Extracts: `subdomain`
- Example: `ZENDESK_SUBDOMAIN=mycompany`

**Pattern**: `https?://([a-z0-9-]+)\.zendesk\.com`
- Zendesk subdomain from URL
- Extracts: `subdomain`
- Example: `https://mycompany.zendesk.com`
