# Intercom

**Category**: business-tools
**Description**: Customer messaging platform
**Homepage**: https://intercom.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Intercom JavaScript packages*

- `intercom-client` - Intercom Node.js SDK
- `react-intercom` - React Intercom widget
- `@intercom/messenger-js-sdk` - Messenger SDK

#### PYPI
*Intercom Python packages*

- `python-intercom` - Python SDK

#### RUBYGEMS
*Intercom Ruby packages*

- `intercom` - Ruby SDK

#### GO
*Intercom Go packages*

- `github.com/intercom/intercom-go` - Go SDK

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]intercom-client['"]`
- Intercom SDK import

**Pattern**: `Intercom\(['"]boot['"]|window\.Intercom`
- Intercom widget initialization

### Code Patterns

**Pattern**: `intercom\.io|api\.intercom\.io|widget\.intercom\.io`
- Intercom URLs

**Pattern**: `INTERCOM_|intercom_app_id`
- Intercom environment variables

**Pattern**: `app_id:\s*['"]?[a-z0-9]+['"]?`
- Intercom app ID in config
- Context Required: Near intercom references

---

## Environment Variables

- `INTERCOM_APP_ID` - Intercom App ID
- `INTERCOM_ACCESS_TOKEN` - Access token
- `INTERCOM_SECRET_KEY` - Identity verification secret

## Detection Notes

- Messenger widget for user communication
- API for programmatic access
- Identity verification for security
- Custom attributes for user data

---

## Secrets Detection

### Credentials

#### Intercom Access Token
**Pattern**: `(?:intercom|INTERCOM).*(?:access[_-]?token|ACCESS[_-]?TOKEN)\s*[=:]\s*['"]?([a-zA-Z0-9=_-]{40,})['"]?`
**Severity**: critical
**Description**: Intercom API access token

#### Intercom Secret Key
**Pattern**: `(?:intercom|INTERCOM).*(?:secret[_-]?key|SECRET[_-]?KEY)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{40,})['"]?`
**Severity**: critical
**Description**: Identity verification secret key

---

## TIER 3: Configuration Extraction

### App ID Extraction

**Pattern**: `(?:app_id|INTERCOM_APP_ID)\s*[=:]\s*['"]?([a-z0-9]+)['"]?`
- Intercom App ID
- Extracts: `app_id`
