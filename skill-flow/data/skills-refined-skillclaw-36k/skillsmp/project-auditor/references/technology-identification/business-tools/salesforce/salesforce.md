# Salesforce

**Category**: business-tools
**Description**: Cloud-based CRM platform
**Homepage**: https://salesforce.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Salesforce JavaScript packages*

- `jsforce` - JavaScript library for Salesforce
- `@salesforce/core` - Salesforce Core library
- `@salesforce/sfdx-core` - SFDX Core library
- `@salesforce/cli` - Salesforce CLI
- `@salesforce/apex` - Apex language support
- `@salesforce/lightning-base-components` - Lightning components
- `@lwc/engine` - Lightning Web Components engine
- `forcedotcom-sfdx-cli` - Legacy SFDX CLI

#### PYPI
*Salesforce Python packages*

- `simple-salesforce` - Simple Salesforce REST API client
- `salesforce-bulk` - Bulk API client
- `salesforce-reporting` - Reporting API client
- `cumulusci` - Salesforce automation
- `django-salesforce` - Django integration

#### RUBYGEMS
*Salesforce Ruby packages*

- `restforce` - Ruby client for Salesforce
- `databasedotcom` - Legacy Salesforce client

#### GO
*Salesforce Go packages*

- `github.com/simpleforce/simpleforce` - Go Salesforce client

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Salesforce usage*

- `sfdx-project.json` - SFDX project configuration
- `.sfdx/` - SFDX configuration directory
- `force-app/` - Salesforce source directory
- `project-scratch-def.json` - Scratch org definition
- `cumulusci.yml` - CumulusCI configuration
- `permissionsets/` - Permission sets

### Configuration Directories
*Known directories that indicate Salesforce usage*

- `force-app/` - Salesforce DX source
- `.sfdx/` - SFDX config
- `lwc/` - Lightning Web Components

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]jsforce['"]`
- JSForce import
- Example: `import jsforce from 'jsforce';`

**Pattern**: `from\s+['"]@salesforce/`
- Salesforce package import
- Example: `import { LightningElement } from 'lwc';`

**Pattern**: `import\s+.*\s+from\s+['"]@lwc/`
- LWC import
- Example: `import { createElement } from '@lwc/engine';`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+simple_salesforce\s+import`
- simple-salesforce import
- Example: `from simple_salesforce import Salesforce`

### Code Patterns

**Pattern**: `\.salesforce\.com|\.force\.com|\.lightning\.force\.com`
- Salesforce URLs
- Example: `https://myorg.salesforce.com`

**Pattern**: `SALESFORCE_|SF_|SFDX_`
- Salesforce environment variables
- Example: `SALESFORCE_ACCESS_TOKEN`

**Pattern**: `jsforce\.Connection|Salesforce\(|new\s+Connection\(`
- Salesforce connection creation
- Example: `new jsforce.Connection({...})`

**Pattern**: `@AuraEnabled|@wire\(|@api`
- Salesforce Apex/LWC decorators
- Example: `@AuraEnabled(cacheable=true)`

**Pattern**: `SELECT.*FROM.*WHERE|SOQL|SOSL`
- SOQL/SOSL queries
- Example: `SELECT Id, Name FROM Account WHERE ...`

**Pattern**: `/services/data/v[0-9]+\.[0-9]+/`
- Salesforce REST API versioned endpoints
- Example: `/services/data/v58.0/sobjects/Account`

---

## Environment Variables

- `SALESFORCE_ACCESS_TOKEN` - OAuth access token
- `SALESFORCE_REFRESH_TOKEN` - OAuth refresh token
- `SALESFORCE_INSTANCE_URL` - Instance URL
- `SALESFORCE_USERNAME` - Username
- `SALESFORCE_PASSWORD` - Password
- `SALESFORCE_SECURITY_TOKEN` - Security token
- `SALESFORCE_CLIENT_ID` - Connected app client ID
- `SALESFORCE_CLIENT_SECRET` - Connected app client secret
- `SF_ACCESS_TOKEN` - Short form access token
- `SFDX_AUTH_URL` - SFDX auth URL

## Detection Notes

- SFDX (Salesforce DX) is the modern development approach
- Lightning Web Components (LWC) for UI development
- Apex is the server-side programming language
- Connected Apps for OAuth authentication
- Scratch orgs for development environments

---

## Secrets Detection

### Credentials

#### Salesforce Access Token
**Pattern**: `(?:salesforce|SALESFORCE|SF).*(?:access[_-]?token|ACCESS[_-]?TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9!._]+)['"]?`
**Severity**: critical
**Description**: Salesforce OAuth access token
**Example**: `SALESFORCE_ACCESS_TOKEN=00D...!abc...`

#### Salesforce Refresh Token
**Pattern**: `(?:salesforce|SALESFORCE|SF).*(?:refresh[_-]?token|REFRESH[_-]?TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9._]+)['"]?`
**Severity**: critical
**Description**: Salesforce OAuth refresh token
**Example**: `SALESFORCE_REFRESH_TOKEN=5Aep...`

#### Salesforce Security Token
**Pattern**: `(?:salesforce|SALESFORCE|SF).*(?:security[_-]?token|SECURITY[_-]?TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9]{20,})['"]?`
**Severity**: critical
**Description**: Salesforce security token
**Example**: `SALESFORCE_SECURITY_TOKEN=abc123...`

#### Salesforce Client Secret
**Pattern**: `(?:salesforce|SALESFORCE|SF).*(?:client[_-]?secret|CLIENT[_-]?SECRET)\s*[=:]\s*['"]?([A-F0-9]{64})['"]?`
**Severity**: critical
**Description**: Connected App client secret
**Example**: `SALESFORCE_CLIENT_SECRET=ABC123...`

#### SFDX Auth URL
**Pattern**: `force://([^:]+):([^@]+)@([^/]+)`
**Severity**: critical
**Description**: SFDX authentication URL with credentials
**Example**: `force://PlatformCLI::refresh_token@org.my.salesforce.com`

### Validation

#### API Documentation
- **REST API**: https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/
- **SFDX CLI**: https://developer.salesforce.com/tools/sfdxcli

#### Validation Endpoint
**API**: User Info
**Endpoint**: `{instance_url}/services/oauth2/userinfo`
**Method**: GET
**Headers**: `Authorization: Bearer {access_token}`
**Purpose**: Validates token and returns user info

```bash
# Validate Salesforce token
curl -H "Authorization: Bearer $SALESFORCE_ACCESS_TOKEN" \
     "$SALESFORCE_INSTANCE_URL/services/oauth2/userinfo"
```

---

## TIER 3: Configuration Extraction

### Instance URL Extraction

**Pattern**: `(?:instance[_-]?url|loginUrl|SALESFORCE_INSTANCE_URL)\s*[=:]\s*['"]?(https://[^'"]+\.salesforce\.com)['"]?`
- Salesforce instance URL
- Extracts: `instance_url`
- Example: `SALESFORCE_INSTANCE_URL=https://myorg.salesforce.com`

### API Version Extraction

**Pattern**: `/services/data/(v[0-9]+\.[0-9]+)/`
- Salesforce API version
- Extracts: `api_version`
- Example: `/services/data/v58.0/`

### Client ID Extraction

**Pattern**: `(?:client[_-]?id|consumer[_-]?key|SALESFORCE_CLIENT_ID)\s*[=:]\s*['"]?([a-zA-Z0-9._]+)['"]?`
- Connected App client ID
- Extracts: `client_id`
- Example: `SALESFORCE_CLIENT_ID=3MVG9...`
