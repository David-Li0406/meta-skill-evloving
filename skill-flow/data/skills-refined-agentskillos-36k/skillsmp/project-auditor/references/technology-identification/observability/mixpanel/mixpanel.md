# Mixpanel

**Category**: observability
**Description**: Product analytics platform for tracking user interactions
**Homepage**: https://mixpanel.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Mixpanel JavaScript SDKs*

- `mixpanel-browser` - Browser SDK
- `mixpanel` - Node.js SDK
- `@mixpanel/mixpanel-react-native` - React Native SDK
- `mixpanel-react-native` - Alternative React Native SDK

#### PYPI
*Mixpanel Python SDK*

- `mixpanel` - Official Python SDK

#### RUBYGEMS
*Mixpanel Ruby SDK*

- `mixpanel-ruby` - Official Ruby SDK
- `mixpanel_client` - Ruby API client

#### GO
*Mixpanel Go SDK*

- `github.com/mixpanel/mixpanel-go` - Official Go SDK

#### MAVEN
*Mixpanel Java SDK*

- `com.mixpanel:mixpanel-java` - Official Java SDK

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`, `.jsx`, `.tsx`

**Pattern**: `from\s+['"]mixpanel-browser['"]`
- Mixpanel browser SDK import
- Example: `import mixpanel from 'mixpanel-browser';`

**Pattern**: `require\(['"]mixpanel['"]\)`
- Mixpanel Node.js require
- Example: `const Mixpanel = require('mixpanel');`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+mixpanel\s+import`
- Mixpanel Python import
- Example: `from mixpanel import Mixpanel`

**Pattern**: `^import\s+mixpanel`
- Mixpanel Python import
- Example: `import mixpanel`

### Code Patterns

**Pattern**: `mixpanel\.init\(|Mixpanel\.init\(`
- Mixpanel initialization
- Example: `mixpanel.init('PROJECT_TOKEN');`

**Pattern**: `mixpanel\.track\(|mixpanel\.identify\(`
- Mixpanel tracking calls
- Example: `mixpanel.track('Button Clicked');`

**Pattern**: `api\.mixpanel\.com|cdn\.mxpnl\.com`
- Mixpanel API URLs
- Example: `https://api.mixpanel.com/track`

**Pattern**: `MIXPANEL_TOKEN|MIXPANEL_PROJECT_TOKEN`
- Mixpanel environment variables
- Example: `MIXPANEL_TOKEN=abc123...`

**Pattern**: `[a-f0-9]{32}`
- Mixpanel project token pattern
- Context Required: Near mixpanel references

---

## Environment Variables

- `MIXPANEL_TOKEN` - Mixpanel project token
- `MIXPANEL_PROJECT_TOKEN` - Alternative token variable
- `MIXPANEL_API_SECRET` - API secret for server-side
- `MIXPANEL_SERVICE_ACCOUNT` - Service account credentials
- `NEXT_PUBLIC_MIXPANEL_TOKEN` - Next.js Mixpanel token
- `REACT_APP_MIXPANEL_TOKEN` - Create React App token
- `VITE_MIXPANEL_TOKEN` - Vite Mixpanel token

## Detection Notes

- Project token is a 32-character hex string
- Browser SDK is for client-side tracking
- Node.js SDK is for server-side tracking
- API secret is required for server-side data export
- Service accounts are used for automation

---

## Secrets Detection

### Tokens and Secrets

#### Mixpanel Project Token
**Pattern**: `(?:mixpanel|MIXPANEL).*(?:token|TOKEN)\s*[=:]\s*['"]?([a-f0-9]{32})['"]?`
**Severity**: medium
**Description**: Mixpanel project token (public, but identifies project)
**Example**: `MIXPANEL_TOKEN=abc123def456789...`
**Note**: Project tokens are designed to be public in client-side code

#### Mixpanel API Secret
**Pattern**: `(?:mixpanel|MIXPANEL).*(?:secret|SECRET)\s*[=:]\s*['"]?([a-f0-9]{32})['"]?`
**Severity**: critical
**Description**: Mixpanel API secret for server-side operations
**Example**: `MIXPANEL_API_SECRET=abc123...`

#### Mixpanel Service Account
**Pattern**: `(?:mixpanel|MIXPANEL).*(?:service[_-]?account|SERVICE[_-]?ACCOUNT)\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Mixpanel service account credentials

### Validation

#### API Documentation
- **API Reference**: https://developer.mixpanel.com/reference/overview
- **SDKs**: https://developer.mixpanel.com/docs/sdks

#### Validation Endpoint
**API**: Track
**Endpoint**: `https://api.mixpanel.com/track`
**Method**: POST
**Purpose**: Send tracking events (validates token)

---

## TIER 3: Configuration Extraction

### Project Token Extraction

**Pattern**: `(?:token|project[_-]?token)\s*[=:]\s*['"]?([a-f0-9]{32})['"]?`
- Mixpanel project token
- Extracts: `project_token`
- Example: `token: 'abc123def456...'`

### API Host Extraction

**Pattern**: `(?:api[_-]?host|MIXPANEL_API_HOST)\s*[=:]\s*['"]?(https?://[^\s'"]+)['"]?`
- Custom API host (EU data residency)
- Extracts: `api_host`
- Example: `api_host: 'https://api-eu.mixpanel.com'`
