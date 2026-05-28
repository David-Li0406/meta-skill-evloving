# PostHog

**Category**: observability
**Description**: Open-source product analytics with session replay and feature flags
**Homepage**: https://posthog.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*PostHog JavaScript SDKs*

- `posthog-js` - Browser JavaScript SDK
- `posthog-node` - Node.js SDK
- `posthog-react-native` - React Native SDK
- `@posthog/plugin-scaffold` - Plugin development

#### PYPI
*PostHog Python SDK*

- `posthog` - Official Python SDK

#### GO
*PostHog Go SDK*

- `github.com/posthog/posthog-go` - Official Go SDK

#### RUBYGEMS
*PostHog Ruby SDK*

- `posthog-ruby` - Official Ruby SDK

#### MAVEN
*PostHog Java SDK*

- `com.posthog.java:posthog` - Official Java SDK

#### PACKAGIST
*PostHog PHP SDK*

- `posthog/posthog-php` - Official PHP SDK

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`, `.jsx`, `.tsx`

**Pattern**: `from\s+['"]posthog-js['"]`
- PostHog browser SDK import
- Example: `import posthog from 'posthog-js';`

**Pattern**: `require\(['"]posthog-node['"]\)`
- PostHog Node.js require
- Example: `const { PostHog } = require('posthog-node');`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+posthog\s+import`
- PostHog Python import
- Example: `from posthog import Posthog`

**Pattern**: `^import\s+posthog`
- PostHog Python import
- Example: `import posthog`

### Code Patterns

**Pattern**: `posthog\.init\(|new\s+PostHog\(`
- PostHog initialization
- Example: `posthog.init('API_KEY', { api_host: '...' });`

**Pattern**: `posthog\.capture\(|posthog\.identify\(`
- PostHog tracking calls
- Example: `posthog.capture('user_signed_up');`

**Pattern**: `app\.posthog\.com|eu\.posthog\.com`
- PostHog cloud URLs
- Example: `https://app.posthog.com`

**Pattern**: `POSTHOG_API_KEY|POSTHOG_HOST|NEXT_PUBLIC_POSTHOG`
- PostHog environment variables
- Example: `POSTHOG_API_KEY=phc_...`

**Pattern**: `phc_[a-zA-Z0-9]{32,}`
- PostHog Cloud API key pattern
- Example: `phc_abc123def456...`

---

## Environment Variables

- `POSTHOG_API_KEY` - PostHog API key
- `POSTHOG_HOST` - PostHog instance URL
- `POSTHOG_PROJECT_API_KEY` - Project API key
- `POSTHOG_PERSONAL_API_KEY` - Personal API key
- `NEXT_PUBLIC_POSTHOG_KEY` - Next.js PostHog key
- `NEXT_PUBLIC_POSTHOG_HOST` - Next.js PostHog host
- `REACT_APP_POSTHOG_KEY` - Create React App key
- `VITE_POSTHOG_KEY` - Vite PostHog key

## Detection Notes

- PostHog Cloud keys start with "phc_"
- Self-hosted instances use custom hosts
- Personal API keys are for API access (different from project keys)
- Feature flags and experiments are built-in
- Session replay requires additional configuration

---

## Secrets Detection

### API Keys

#### PostHog Project API Key
**Pattern**: `phc_[a-zA-Z0-9]{32,}`
**Severity**: medium
**Description**: PostHog Cloud project API key
**Example**: `phc_abc123def456ghi789...`
**Note**: Project API keys are designed for client-side use

#### PostHog Personal API Key
**Pattern**: `phx_[a-zA-Z0-9]{32,}`
**Severity**: critical
**Description**: PostHog personal API key for admin operations
**Example**: `phx_abc123def456...`

#### PostHog Self-Hosted Key
**Pattern**: `(?:posthog|POSTHOG).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{32,})['"]?`
**Severity**: medium
**Description**: PostHog self-hosted API key
**Context Required**: Not matching phc_ or phx_ prefix

### Validation

#### API Documentation
- **API Reference**: https://posthog.com/docs/api
- **SDKs**: https://posthog.com/docs/libraries

#### Validation Endpoint
**API**: Capture
**Endpoint**: `{host}/capture/`
**Method**: POST
**Purpose**: Send events (validates API key)

```bash
# Validate PostHog API key
curl -X POST "$POSTHOG_HOST/capture/" \
     -H "Content-Type: application/json" \
     -d '{"api_key": "'"$POSTHOG_API_KEY"'", "event": "test"}'
```

---

## TIER 3: Configuration Extraction

### API Key Extraction

**Pattern**: `(?:api_key|apiKey)\s*[=:]\s*['"]?(phc_[a-zA-Z0-9]+)['"]?`
- PostHog Cloud API key
- Extracts: `api_key`
- Example: `api_key: 'phc_abc123...'`

### Host Extraction

**Pattern**: `(?:api_host|host|POSTHOG_HOST)\s*[=:]\s*['"]?(https?://[^\s'"]+)['"]?`
- PostHog instance host
- Extracts: `host`
- Example: `api_host: 'https://app.posthog.com'`
