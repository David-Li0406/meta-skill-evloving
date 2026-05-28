# Analytics Architecture - Validations

## PII in Analytics Events

### **Id**
analytics-pii-in-events
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - track\([^)]*email\s*:
  - track\([^)]*phone\s*:
  - track\([^)]*ssn\s*:
  - track\([^)]*address\s*:
  - analytics\.identify\([^)]*email\s*:
### **Message**
Potential PII (email, phone, SSN, address) in analytics events. Hash or exclude PII.
### **Fix Action**
Hash PII before tracking: { emailHash: hashEmail(email) }
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Unstructured Event Data

### **Id**
analytics-no-schema
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - track\(['"][^'"]+['"]\s*,\s*\{[^}]*\}\)(?!.*\bschema\b)
  - analytics\.track\([^)]*\)(?!.*validate)
### **Message**
Analytics event without schema validation. Define event schema.
### **Fix Action**
Create schema: const PageViewSchema = z.object({ ... })
### **Applies To**
  - **/*.ts
  - **/*.js

## Client-Side Only Tracking

### **Id**
analytics-client-side-only
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - analytics\.track\(
### **Message**
Client-side analytics can be blocked by ad blockers. Implement server-side tracking.
### **Fix Action**
Add server-side tracking endpoint: POST /api/track
### **Applies To**
  - app/**/*.tsx
  - app/**/*.jsx
  - pages/**/*.tsx
  - pages/**/*.jsx

## Events Without User Identification

### **Id**
analytics-no-user-id
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - track\(['"][^'"]+['"]\s*,\s*\{(?!.*userId)(?!.*anonymousId)
### **Message**
Analytics event without user identification. Add userId or anonymousId.
### **Fix Action**
Include: { userId: user.id, anonymousId: getAnonymousId() }
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Hardcoded Analytics API Keys

### **Id**
analytics-hardcoded-keys
### **Severity**
critical
### **Type**
regex
### **Pattern**
  - writeKey:\s*['"][a-zA-Z0-9]{20,}['"]
  - apiKey:\s*['"]AIza[a-zA-Z0-9_-]{35}['"]
  - mixpanel\.init\(['"][a-f0-9]{32}['"]
### **Message**
Analytics API key hardcoded in client code. Use environment variables.
### **Fix Action**
Use process.env.NEXT_PUBLIC_ANALYTICS_KEY
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Missing Error Tracking

### **Id**
analytics-missing-error-tracking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - catch\s*\([^)]*\)\s*\{(?!.*track|.*captureException|.*logError)
### **Message**
Error not tracked in analytics. Add error tracking.
### **Fix Action**
Add: analytics.track('Error Occurred', { error: e.message })
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Magic String Event Names

### **Id**
analytics-magic-event-names
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - track\(['"][^'"]+['"]
### **Message**
Event name is magic string. Use constants for type safety.
### **Fix Action**
Define: const EVENTS = { PAGE_VIEW: 'Page Viewed' } as const
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Tracking Without Consent

### **Id**
analytics-no-consent
### **Severity**
error
### **Type**
regex
### **Pattern**
  - analytics\.track\((?!.*hasConsent|.*cookieConsent)
  - gtag\((?!.*consent)
### **Message**
Analytics tracking without consent check. Add GDPR/CCPA compliance.
### **Fix Action**
Check consent: if (hasAnalyticsConsent()) { analytics.track(...) }
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Synchronous Analytics Blocking Render

### **Id**
analytics-sync-blocking
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - const\s+\w+\s*=\s*analytics\.track\(
  - await\s+analytics\.track\(
### **Message**
Analytics blocking code execution. Track asynchronously without await.
### **Fix Action**
Fire and forget: analytics.track(...) // no await
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## No Retry Logic for Failed Events

### **Id**
analytics-no-retry
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - fetch\([^)]*\/track[^)]*\)(?!.*retry|.*catch)
### **Message**
Analytics request without retry logic. Events may be lost.
### **Fix Action**
Add retry: await retryWithBackoff(() => fetch('/track', ...))
### **Applies To**
  - **/*.ts
  - **/*.js

## Excessive Event Tracking

### **Id**
analytics-excessive-events
### **Severity**
info
### **Type**
regex
### **Pattern**
  - onMouseMove.*track\(
  - onScroll.*track\(
  - onChange.*track\(
### **Message**
High-frequency events can overwhelm analytics. Debounce or sample.
### **Fix Action**
Use debounce: const trackScroll = debounce(() => analytics.track(...), 1000)
### **Applies To**
  - **/*.tsx
  - **/*.jsx

## Development Events to Production

### **Id**
analytics-no-environment-filter
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - analytics\.track\((?!.*process\.env\.NODE_ENV)
### **Message**
Analytics may send dev events to production. Filter by environment.
### **Fix Action**
Add check: if (process.env.NODE_ENV === 'production') { track(...) }
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx