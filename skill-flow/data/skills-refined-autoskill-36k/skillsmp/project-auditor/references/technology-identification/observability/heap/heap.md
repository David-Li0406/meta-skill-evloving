# Heap

**Category**: observability
**Description**: Digital insights platform with auto-capture analytics
**Homepage**: https://heap.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Heap packages*

- `heap-api` - Heap Server-side API
- `@heap/heap-react-native-bridge` - React Native bridge
- `@heap/heap-node` - Node.js SDK

---

## TIER 2: Deep Detection (File-based)

### Code Patterns

**Pattern**: `heap\.load\(|heap\.track\(|heap\.identify\(`
- Heap JavaScript API calls
- Example: `heap.load('APP_ID');`

**Pattern**: `heapanalytics\.com|cdn\.heapanalytics\.com`
- Heap CDN/API URLs
- Example: `https://cdn.heapanalytics.com/js/heap-`

**Pattern**: `HEAP_APP_ID|HEAP_API_KEY`
- Heap environment variables
- Example: `HEAP_APP_ID=1234567890`

**Pattern**: `heap-[0-9]{10}\.js`
- Heap script filename pattern
- Example: `heap-1234567890.js`

**Pattern**: `window\.heap|heap\s*=\s*window\.heap`
- Heap global object reference
- Example: `window.heap = window.heap || [];`

---

## Environment Variables

- `HEAP_APP_ID` - Heap application ID
- `HEAP_API_KEY` - Heap API key (server-side)
- `NEXT_PUBLIC_HEAP_ID` - Next.js Heap ID
- `REACT_APP_HEAP_ID` - Create React App Heap ID
- `VITE_HEAP_ID` - Vite Heap ID

## Detection Notes

- App ID is a 10-digit number
- Auto-capture tracks all interactions automatically
- Server-side API requires separate API key
- Heap uses a snippet similar to Google Analytics

---

## Secrets Detection

### API Keys

#### Heap App ID
**Pattern**: `(?:heap|HEAP).*(?:app[_-]?id|APP[_-]?ID)\s*[=:]\s*['"]?([0-9]{10})['"]?`
**Severity**: low
**Description**: Heap application ID (public identifier)
**Example**: `HEAP_APP_ID=1234567890`

#### Heap API Key
**Pattern**: `(?:heap|HEAP).*(?:api[_-]?key|API[_-]?KEY)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{20,})['"]?`
**Severity**: critical
**Description**: Heap server-side API key
**Example**: `HEAP_API_KEY=abc123...`

### Validation

#### API Documentation
- **Server-side API**: https://developers.heap.io/reference/track-1

---

## TIER 3: Configuration Extraction

### App ID Extraction

**Pattern**: `heap\.load\(['"]([0-9]{10})['"]\)`
- Heap App ID from load call
- Extracts: `app_id`
- Example: `heap.load('1234567890');`
