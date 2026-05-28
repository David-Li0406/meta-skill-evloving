# Amplitude

**Category**: observability
**Description**: Product analytics and event tracking platform
**Homepage**: https://amplitude.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Amplitude JavaScript SDKs*

- `@amplitude/analytics-browser` - Browser SDK (latest)
- `@amplitude/analytics-node` - Node.js SDK
- `@amplitude/analytics-react-native` - React Native SDK
- `amplitude-js` - Legacy browser SDK
- `@amplitude/experiment-js-client` - Experiment client
- `@amplitude/plugin-session-replay-browser` - Session replay

#### PYPI
*Amplitude Python SDK*

- `amplitude-analytics` - Official Python SDK

#### GO
*Amplitude Go SDK*

- `github.com/amplitude/analytics-go` - Official Go SDK

#### MAVEN
*Amplitude Java/Kotlin SDK*

- `com.amplitude:java-sdk` - Java SDK
- `com.amplitude:analytics-connector` - Analytics connector

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`, `.jsx`, `.tsx`

**Pattern**: `from\s+['"]@amplitude/analytics-browser['"]`
- Amplitude browser SDK import
- Example: `import * as amplitude from '@amplitude/analytics-browser';`

**Pattern**: `from\s+['"]amplitude-js['"]`
- Legacy Amplitude SDK import
- Example: `import amplitude from 'amplitude-js';`

**Pattern**: `require\(['"]@amplitude/analytics-node['"]\)`
- Amplitude Node.js require
- Example: `const { init } = require('@amplitude/analytics-node');`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+amplitude\s+import`
- Amplitude Python import
- Example: `from amplitude import Amplitude, BaseEvent`

### Code Patterns

**Pattern**: `amplitude\.init\(|Amplitude\.getInstance\(\)\.init\(`
- Amplitude initialization
- Example: `amplitude.init('API_KEY');`

**Pattern**: `amplitude\.track\(|amplitude\.logEvent\(`
- Amplitude tracking calls
- Example: `amplitude.track('Button Clicked');`

**Pattern**: `api\.amplitude\.com|cdn\.amplitude\.com`
- Amplitude API URLs
- Example: `https://api2.amplitude.com/2/httpapi`

**Pattern**: `AMPLITUDE_API_KEY|AMPLITUDE_SECRET_KEY`
- Amplitude environment variables
- Example: `AMPLITUDE_API_KEY=abc123...`

---

## Environment Variables

- `AMPLITUDE_API_KEY` - Amplitude API key (client-side)
- `AMPLITUDE_SECRET_KEY` - Amplitude secret key (server-side)
- `AMPLITUDE_SERVER_URL` - Custom server URL
- `NEXT_PUBLIC_AMPLITUDE_API_KEY` - Next.js Amplitude key
- `REACT_APP_AMPLITUDE_API_KEY` - Create React App key
- `VITE_AMPLITUDE_API_KEY` - Vite Amplitude key

## Detection Notes

- API key is a 32-character hex string
- Secret key is required for server-side operations
- @amplitude/analytics-* is the latest SDK generation
- amplitude-js is the legacy SDK
- EU data residency uses different endpoints

---

## Secrets Detection

### API Keys

#### Amplitude API Key
**Pattern**: `(?:amplitude|AMPLITUDE).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?([a-f0-9]{32})['"]?`
**Severity**: medium
**Description**: Amplitude API key (designed for client-side use)
**Example**: `AMPLITUDE_API_KEY=abc123def456...`
**Note**: API keys are designed to be public in client-side code

#### Amplitude Secret Key
**Pattern**: `(?:amplitude|AMPLITUDE).*(?:secret[_-]?key|SECRET[_-]?KEY)\s*[=:]\s*['"]?([a-f0-9]{32})['"]?`
**Severity**: critical
**Description**: Amplitude secret key for server-side operations
**Example**: `AMPLITUDE_SECRET_KEY=abc123...`

#### Amplitude Experiment Key
**Pattern**: `(?:amplitude|AMPLITUDE).*(?:deployment[_-]?key|experiment[_-]?key)\s*[=:]\s*['"]?([a-zA-Z0-9_-]+)['"]?`
**Severity**: high
**Description**: Amplitude Experiment deployment key

### Validation

#### API Documentation
- **HTTP API**: https://www.docs.developers.amplitude.com/analytics/apis/http-v2-api/
- **SDKs**: https://www.docs.developers.amplitude.com/data/sdks/

#### Validation Endpoint
**API**: HTTP V2 API
**Endpoint**: `https://api2.amplitude.com/2/httpapi`
**Method**: POST
**Headers**: `Content-Type: application/json`
**Purpose**: Send events (validates API key)

---

## TIER 3: Configuration Extraction

### API Key Extraction

**Pattern**: `(?:apiKey|api[_-]?key)\s*[=:]\s*['"]?([a-f0-9]{32})['"]?`
- Amplitude API key
- Extracts: `api_key`
- Example: `apiKey: 'abc123def456...'`

### Server URL Extraction

**Pattern**: `(?:serverUrl|server[_-]?url|AMPLITUDE_SERVER_URL)\s*[=:]\s*['"]?(https?://[^\s'"]+)['"]?`
- Custom server URL
- Extracts: `server_url`
- Example: `serverUrl: 'https://api.eu.amplitude.com'`
