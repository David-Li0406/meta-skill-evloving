# HubSpot

**Category**: business-tools
**Description**: CRM, marketing, sales, and customer service platform
**Homepage**: https://hubspot.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*HubSpot JavaScript packages*

- `@hubspot/api-client` - Official HubSpot API client
- `hubspot` - Legacy HubSpot client

#### PYPI
*HubSpot Python packages*

- `hubspot-api-client` - Official Python client
- `hubspot` - Legacy Python client

#### RUBYGEMS
*HubSpot Ruby packages*

- `hubspot-api-client` - Official Ruby client
- `hubspot-ruby` - Alternative client

#### GO
*HubSpot Go packages*

- `github.com/clarkmcc/go-hubspot` - Go HubSpot client

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]@hubspot/api-client['"]`
- HubSpot API client import
- Example: `import { Client } from '@hubspot/api-client';`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+hubspot\s+import`
- HubSpot Python import
- Example: `from hubspot import HubSpot`

**Pattern**: `^import\s+hubspot`
- HubSpot Python import
- Example: `import hubspot`

### Code Patterns

**Pattern**: `api\.hubspot\.com|api\.hubapi\.com`
- HubSpot API URLs
- Example: `https://api.hubapi.com/crm/v3/objects/contacts`

**Pattern**: `HUBSPOT_API_KEY|HUBSPOT_ACCESS_TOKEN|HUBSPOT_PRIVATE_APP`
- HubSpot environment variables
- Example: `HUBSPOT_API_KEY=abc123...`

**Pattern**: `hubspot\.Client\(|HubSpot\(|Client\(\{.*accessToken`
- HubSpot client creation
- Example: `new Client({ accessToken: '...' })`

**Pattern**: `/crm/v[0-9]+/objects/|/marketing/v[0-9]+/`
- HubSpot API versioned endpoints
- Example: `/crm/v3/objects/contacts`

---

## Environment Variables

- `HUBSPOT_API_KEY` - HubSpot API key (deprecated)
- `HUBSPOT_ACCESS_TOKEN` - Private app access token
- `HUBSPOT_PRIVATE_APP_TOKEN` - Private app token
- `HUBSPOT_CLIENT_ID` - OAuth client ID
- `HUBSPOT_CLIENT_SECRET` - OAuth client secret
- `HUBSPOT_REFRESH_TOKEN` - OAuth refresh token
- `HUBSPOT_PORTAL_ID` - HubSpot portal/hub ID

## Detection Notes

- API keys are deprecated, private app tokens preferred
- OAuth for installed apps
- CRM, Marketing, CMS, and Service APIs available
- Portal ID identifies the HubSpot account

---

## Secrets Detection

### API Keys and Tokens

#### HubSpot API Key (Deprecated)
**Pattern**: `(?:hubspot|HUBSPOT).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})['"]?`
**Severity**: critical
**Description**: HubSpot API key (deprecated format)
**Example**: `HUBSPOT_API_KEY=12345678-1234-1234-1234-123456789012`

#### HubSpot Private App Token
**Pattern**: `pat-[a-z]{2}[0-9]+-[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}`
**Severity**: critical
**Description**: HubSpot private app access token
**Example**: `pat-xx0-00000000-0000-0000-0000-000000000000`

#### HubSpot Access Token
**Pattern**: `(?:hubspot|HUBSPOT).*(?:access[_-]?token|ACCESS[_-]?TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{30,})['"]?`
**Severity**: critical
**Description**: HubSpot OAuth access token

#### HubSpot Client Secret
**Pattern**: `(?:hubspot|HUBSPOT).*(?:client[_-]?secret|CLIENT[_-]?SECRET)\s*[=:]\s*['"]?([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})['"]?`
**Severity**: critical
**Description**: HubSpot OAuth client secret

### Validation

#### API Documentation
- **API Reference**: https://developers.hubspot.com/docs/api/overview
- **Authentication**: https://developers.hubspot.com/docs/api/oauth-quickstart-guide

#### Validation Endpoint
**API**: Access Token Info
**Endpoint**: `https://api.hubapi.com/oauth/v1/access-tokens/{token}`
**Method**: GET
**Purpose**: Validates OAuth token

---

## TIER 3: Configuration Extraction

### Portal ID Extraction

**Pattern**: `(?:portal[_-]?id|hub[_-]?id|HUBSPOT_PORTAL_ID)\s*[=:]\s*['"]?([0-9]+)['"]?`
- HubSpot portal/hub ID
- Extracts: `portal_id`
- Example: `HUBSPOT_PORTAL_ID=12345678`
