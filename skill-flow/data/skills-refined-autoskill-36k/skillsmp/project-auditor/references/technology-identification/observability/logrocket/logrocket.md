# LogRocket

**Category**: observability
**Description**: Session replay and frontend monitoring platform
**Homepage**: https://logrocket.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*LogRocket packages*

- `logrocket` - Core LogRocket SDK
- `logrocket-react` - React integration
- `@logrocket/react-native` - React Native SDK
- `logrocket-vuex` - Vuex plugin
- `logrocket-ngrx` - NgRx plugin

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`, `.jsx`, `.tsx`

**Pattern**: `from\s+['"]logrocket['"]`
- LogRocket SDK import
- Example: `import LogRocket from 'logrocket';`

**Pattern**: `from\s+['"]logrocket-react['"]`
- LogRocket React import
- Example: `import setupLogRocketReact from 'logrocket-react';`

### Code Patterns

**Pattern**: `LogRocket\.init\(`
- LogRocket initialization
- Example: `LogRocket.init('app-id/project');`

**Pattern**: `LogRocket\.identify\(|LogRocket\.track\(`
- LogRocket API calls
- Example: `LogRocket.identify('user-id');`

**Pattern**: `cdn\.logrocket\.io|cdn\.lr-ingest\.io`
- LogRocket CDN URLs
- Example: `https://cdn.logrocket.io/LogRocket.min.js`

**Pattern**: `LOGROCKET_APP_ID|LOGROCKET_PROJECT`
- LogRocket environment variables
- Example: `LOGROCKET_APP_ID=abc123/my-project`

**Pattern**: `[a-z0-9]+/[a-z0-9-]+`
- LogRocket app ID pattern
- Context Required: Near logrocket references
- Example: `abc123/my-project`

---

## Environment Variables

- `LOGROCKET_APP_ID` - LogRocket application ID
- `LOGROCKET_PROJECT` - LogRocket project identifier
- `NEXT_PUBLIC_LOGROCKET_APP_ID` - Next.js LogRocket ID
- `REACT_APP_LOGROCKET_ID` - Create React App ID
- `VITE_LOGROCKET_ID` - Vite LogRocket ID

## Detection Notes

- App ID format: "org-slug/project-slug"
- Session replay captures DOM and network requests
- Integrates with Redux, Vuex, NgRx for state tracking
- Privacy masking available for sensitive data

---

## Secrets Detection

### API Keys

#### LogRocket App ID
**Pattern**: `(?:logrocket|LOGROCKET).*(?:app[_-]?id|APP[_-]?ID)\s*[=:]\s*['"]?([a-z0-9]+/[a-z0-9-]+)['"]?`
**Severity**: low
**Description**: LogRocket application ID (public)
**Example**: `LOGROCKET_APP_ID=abc123/my-project`

#### LogRocket API Key
**Pattern**: `(?:logrocket|LOGROCKET).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{30,})['"]?`
**Severity**: high
**Description**: LogRocket API key for data export
**Example**: `LOGROCKET_API_KEY=abc123...`

### Validation

#### API Documentation
- **SDK Reference**: https://docs.logrocket.com/reference/
- **JavaScript SDK**: https://docs.logrocket.com/docs/javascript-sdk

---

## TIER 3: Configuration Extraction

### App ID Extraction

**Pattern**: `LogRocket\.init\(['"]([a-z0-9]+/[a-z0-9-]+)['"]\)`
- LogRocket app ID from init call
- Extracts: `app_id`
- Example: `LogRocket.init('abc123/my-project');`
