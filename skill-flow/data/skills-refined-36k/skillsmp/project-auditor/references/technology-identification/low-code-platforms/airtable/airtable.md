# Airtable

**Category**: low-code-platforms
**Description**: Cloud-based spreadsheet-database hybrid with automation capabilities
**Homepage**: https://airtable.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Airtable SDK and utilities*

- `airtable` - Official Airtable JavaScript SDK
- `@airtable/blocks` - Airtable Blocks SDK (apps)
- `@airtable/blocks-testing` - Blocks testing utilities

#### PYPI
*Airtable Python SDK*

- `pyairtable` - Modern Python SDK
- `airtable-python-wrapper` - Alternative Python wrapper
- `airtable` - Simple Python client

#### RUBYGEMS
*Airtable Ruby SDK*

- `airtable` - Ruby client for Airtable
- `airrecord` - Alternative Ruby ORM

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Airtable usage*

- `.airtablerc` - Airtable CLI configuration
- `block.json` - Airtable Block configuration

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`, `.jsx`, `.tsx`

**Pattern**: `from\s+['"]airtable['"]`
- Airtable SDK import
- Example: `import Airtable from 'airtable';`

**Pattern**: `require\(['"]airtable['"]\)`
- Airtable CommonJS require
- Example: `const Airtable = require('airtable');`

**Pattern**: `from\s+['"]@airtable/blocks`
- Airtable Blocks import
- Example: `import { useBase } from '@airtable/blocks/ui';`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+pyairtable\s+import`
- pyairtable import
- Example: `from pyairtable import Api, Table`

**Pattern**: `^import\s+airtable`
- airtable import
- Example: `import airtable`

### Code Patterns

**Pattern**: `airtable\.com/|api\.airtable\.com`
- Airtable URLs
- Example: `https://api.airtable.com/v0/`

**Pattern**: `AIRTABLE_API_KEY|AIRTABLE_BASE_ID`
- Airtable environment variables
- Example: `AIRTABLE_API_KEY=key...`

**Pattern**: `new\s+Airtable\(|Airtable\.configure\(`
- Airtable client initialization
- Example: `const base = new Airtable({apiKey}).base(baseId);`

**Pattern**: `app[a-zA-Z0-9]{14}`
- Airtable base ID pattern
- Example: `appABC123DEF456GH`

---

## Environment Variables

- `AIRTABLE_API_KEY` - Personal API key (deprecated)
- `AIRTABLE_ACCESS_TOKEN` - Personal access token (new)
- `AIRTABLE_BASE_ID` - Base identifier
- `AIRTABLE_TABLE_NAME` - Table name

## Detection Notes

- Base IDs start with "app" followed by 14 characters
- Table IDs start with "tbl" followed by 14 characters
- Record IDs start with "rec" followed by 14 characters
- Personal access tokens replace legacy API keys
- Blocks (apps) run inside Airtable's environment

---

## Secrets Detection

### API Keys and Tokens

#### Airtable Personal Access Token
**Pattern**: `pat[a-zA-Z0-9]{14}\.[a-f0-9]{64}`
**Severity**: critical
**Description**: Airtable personal access token (new format)
**Example**: `patABC123DEF456GH.abc123def456...`

#### Airtable Legacy API Key
**Pattern**: `key[a-zA-Z0-9]{14}`
**Severity**: critical
**Description**: Legacy Airtable API key (deprecated)
**Example**: `keyABC123DEF456GH`

#### Airtable OAuth Token
**Pattern**: `(?:AIRTABLE|airtable).*(?:token|TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9._-]{50,})['"]?`
**Severity**: critical
**Description**: Airtable OAuth access token

### Validation

#### API Documentation
- **REST API**: https://airtable.com/developers/web/api/introduction
- **Authentication**: https://airtable.com/developers/web/api/authentication

#### Validation Endpoint
**API**: List Bases
**Endpoint**: `https://api.airtable.com/v0/meta/bases`
**Method**: GET
**Headers**: `Authorization: Bearer {token}`
**Purpose**: Validates token and lists accessible bases

```bash
# Validate Airtable token
curl -H "Authorization: Bearer $AIRTABLE_ACCESS_TOKEN" \
     "https://api.airtable.com/v0/meta/bases"
```

---

## TIER 3: Configuration Extraction

### Base ID Extraction

**Pattern**: `(?:base[_-]?id|AIRTABLE_BASE_ID)\s*[=:]\s*['"]?(app[a-zA-Z0-9]{14})['"]?`
- Airtable base identifier
- Extracts: `base_id`
- Example: `AIRTABLE_BASE_ID=appABC123DEF456GH`

### Table Name Extraction

**Pattern**: `(?:table[_-]?(?:name|id)|AIRTABLE_TABLE)\s*[=:]\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Airtable table name or ID
- Extracts: `table_name`
- Example: `AIRTABLE_TABLE_NAME=Users`
