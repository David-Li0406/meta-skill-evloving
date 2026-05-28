# FullStory

**Category**: observability
**Description**: Digital experience analytics with session replay
**Homepage**: https://fullstory.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*FullStory packages*

- `@fullstory/browser` - Browser SDK
- `@fullstory/server-api-client` - Server API client
- `@fullstory/react-native` - React Native SDK
- `@fullstory/snippet` - Snippet generator

#### PYPI
*FullStory Python packages*

- `fullstory` - Python API client

---

## TIER 2: Deep Detection (File-based)

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`, `.jsx`, `.tsx`

**Pattern**: `from\s+['"]@fullstory/browser['"]`
- FullStory browser SDK import
- Example: `import * as FullStory from '@fullstory/browser';`

### Code Patterns

**Pattern**: `FullStory\.init\(|FS\.init\(`
- FullStory initialization
- Example: `FullStory.init({ orgId: 'ABC123' });`

**Pattern**: `FullStory\.identify\(|FS\.identify\(`
- FullStory identify call
- Example: `FullStory.identify(userId);`

**Pattern**: `fullstory\.com|edge\.fullstory\.com|rs\.fullstory\.com`
- FullStory URLs
- Example: `https://edge.fullstory.com/s/fs.js`

**Pattern**: `FULLSTORY_ORG_ID|FS_ORG|FULLSTORY_API_KEY`
- FullStory environment variables
- Example: `FULLSTORY_ORG_ID=ABC123`

**Pattern**: `window\['_fs_org'\]|_fs_org\s*=`
- FullStory organization ID variable
- Example: `window['_fs_org'] = 'ABC123';`

---

## Environment Variables

- `FULLSTORY_ORG_ID` - FullStory organization ID
- `FULLSTORY_API_KEY` - FullStory API key
- `FS_ORG` - Alternative org ID variable
- `NEXT_PUBLIC_FULLSTORY_ORG` - Next.js FullStory org
- `REACT_APP_FULLSTORY_ORG` - Create React App org

## Detection Notes

- Org ID is a short alphanumeric string (e.g., "ABC123")
- API key is required for server-side API access
- Session replay captures all user interactions
- Privacy controls can exclude sensitive data

---

## Secrets Detection

### API Keys

#### FullStory Org ID
**Pattern**: `(?:fullstory|FULLSTORY|_fs_org).*(?:org[_-]?id|ORG[_-]?ID|org)\s*[=:]\s*['"]?([A-Z0-9]{5,10})['"]?`
**Severity**: low
**Description**: FullStory organization ID (public)
**Example**: `FULLSTORY_ORG_ID=ABC123`

#### FullStory API Key
**Pattern**: `(?:fullstory|FULLSTORY).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{30,})['"]?`
**Severity**: critical
**Description**: FullStory server-side API key
**Example**: `FULLSTORY_API_KEY=abc123def456...`

### Validation

#### API Documentation
- **Browser API**: https://developer.fullstory.com/browser/getting-started/
- **Server API**: https://developer.fullstory.com/server/getting-started/

---

## TIER 3: Configuration Extraction

### Org ID Extraction

**Pattern**: `(?:orgId|org[_-]?id|_fs_org)\s*[=:]\s*['"]?([A-Z0-9]{5,10})['"]?`
- FullStory organization ID
- Extracts: `org_id`
- Example: `orgId: 'ABC123'`
