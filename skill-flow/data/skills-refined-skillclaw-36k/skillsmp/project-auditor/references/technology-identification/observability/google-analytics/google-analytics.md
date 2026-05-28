# Google Analytics

**Category**: observability
**Description**: Web analytics service for tracking website and app traffic
**Homepage**: https://analytics.google.com

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Google Analytics packages*

- `@google-analytics/data` - Google Analytics Data API
- `analytics` - Analytics.js library
- `react-ga` - React Google Analytics (legacy UA)
- `react-ga4` - React Google Analytics 4
- `vue-gtag` - Vue.js Google Tag
- `@types/gtag.js` - TypeScript definitions
- `gtag` - Global Site Tag wrapper
- `universal-analytics` - Universal Analytics (deprecated)

#### PYPI
*Google Analytics Python packages*

- `google-analytics-data` - GA4 Data API
- `google-api-python-client` - Google API client (includes GA)
- `analytics-python` - Segment Analytics (often paired)

#### RUBYGEMS
*Google Analytics Ruby packages*

- `google-analytics-data` - GA4 Data API
- `google-apis-analyticsreporting_v4` - Analytics Reporting API
- `staccato` - Ruby UA tracking

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Google Analytics usage*

- `gtag.js` - Google Tag configuration
- `analytics.js` - Analytics.js configuration

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`, `.jsx`, `.tsx`

**Pattern**: `from\s+['"]react-ga4?['"]`
- React GA import
- Example: `import ReactGA from 'react-ga4';`

**Pattern**: `from\s+['"]@google-analytics/data['"]`
- GA Data API import
- Example: `import { BetaAnalyticsDataClient } from '@google-analytics/data';`

### Code Patterns

**Pattern**: `gtag\(['"]config['"],\s*['"]G-[A-Z0-9]+['"]|gtag\(['"]config['"],\s*['"]UA-[0-9]+-[0-9]+['"]`
- Google Analytics initialization
- Example: `gtag('config', 'G-XXXXXXXXXX');`

**Pattern**: `G-[A-Z0-9]{10}|UA-[0-9]{6,}-[0-9]`
- Google Analytics Measurement/Tracking ID
- Example: `G-ABC123DEF4` or `UA-123456-1`

**Pattern**: `googletagmanager\.com/gtag|google-analytics\.com/analytics`
- Google Analytics script URLs
- Example: `https://www.googletagmanager.com/gtag/js`

**Pattern**: `GA_MEASUREMENT_ID|GA_TRACKING_ID|GOOGLE_ANALYTICS`
- Google Analytics environment variables
- Example: `GA_MEASUREMENT_ID=G-ABC123DEF4`

**Pattern**: `ReactGA\.initialize|gtag\(['"]event['"]`
- Google Analytics API calls
- Example: `ReactGA.initialize('G-XXXXXXXXXX');`

---

## Environment Variables

- `GA_MEASUREMENT_ID` - GA4 measurement ID
- `GA_TRACKING_ID` - Universal Analytics ID (deprecated)
- `GOOGLE_ANALYTICS_ID` - Generic GA ID
- `NEXT_PUBLIC_GA_ID` - Next.js GA ID
- `REACT_APP_GA_ID` - Create React App GA ID
- `VITE_GA_ID` - Vite GA ID
- `GATSBY_GA_ID` - Gatsby GA ID

## Detection Notes

- GA4 uses Measurement IDs (G-XXXXXXXXXX)
- Universal Analytics IDs (UA-XXXXXX-X) are deprecated
- gtag.js is the modern implementation
- analytics.js is the legacy Universal Analytics
- Often integrated via Google Tag Manager
- Server-side tracking uses Measurement Protocol

---

## Secrets Detection

### API Keys and Credentials

#### Google Analytics API Secret
**Pattern**: `(?:ga|GA|analytics).*(?:api[_-]?secret|API[_-]?SECRET)\s*[=:]\s*['"]?([a-zA-Z0-9_-]{20,})['"]?`
**Severity**: high
**Description**: Google Analytics Measurement Protocol API secret
**Example**: `GA_API_SECRET=abc123def456...`

#### Google Service Account Key
**Pattern**: `"type":\s*"service_account".*"project_id":\s*"[^"]+".*"private_key":`
**Severity**: critical
**Description**: Google Cloud service account JSON key (used for GA Data API)
**Multiline**: true

### Validation

#### API Documentation
- **GA4 Data API**: https://developers.google.com/analytics/devguides/reporting/data/v1
- **Measurement Protocol**: https://developers.google.com/analytics/devguides/collection/protocol/ga4

---

## TIER 3: Configuration Extraction

### Measurement ID Extraction

**Pattern**: `(?:measurementId|measurement[_-]?id|GA_MEASUREMENT_ID|GA_ID)\s*[=:]\s*['"]?(G-[A-Z0-9]{10})['"]?`
- GA4 Measurement ID
- Extracts: `measurement_id`
- Example: `GA_MEASUREMENT_ID=G-ABC123DEF4`

### Property ID Extraction

**Pattern**: `(?:propertyId|property[_-]?id)\s*[=:]\s*['"]?([0-9]{9})['"]?`
- GA4 Property ID (numeric)
- Extracts: `property_id`
- Example: `propertyId: '123456789'`

### Stream ID Extraction

**Pattern**: `(?:streamId|stream[_-]?id)\s*[=:]\s*['"]?([0-9]+)['"]?`
- GA4 Data Stream ID
- Extracts: `stream_id`
- Example: `streamId: '1234567890'`
