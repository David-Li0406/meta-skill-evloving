# Analytics - Validations

## Missing Event Naming Convention

### **Id**
analytics-no-naming-convention
### **Severity**
error
### **Type**
regex
### **Pattern**
  - track\(['"](?![A-Z][a-z]+(?:[A-Z][a-z]+)*)['"]
  - trackEvent\(['"](?!\w+_\w+)['"]
### **Message**
Event name doesn't follow naming convention. Inconsistent naming makes analysis impossible.
### **Fix Action**
Use consistent convention: PascalCase (ButtonClicked) or snake_case (button_clicked). Document in analytics spec.
### **Applies To**
  - *.js
  - *.jsx
  - *.ts
  - *.tsx

## PII in Event Properties

### **Id**
analytics-pii-in-events
### **Severity**
error
### **Type**
regex
### **Pattern**
  - \b(email|password|ssn|social_security|credit_card|phone)\b.{0,50}:
  - properties.{0,50}\b(firstName|lastName|name|address|dob|birthdate)\b
### **Message**
Potential PII in event properties. This violates privacy regulations (GDPR, CCPA) and analytics ToS.
### **Fix Action**
Use anonymized IDs instead. Hash or encrypt if user-specific tracking needed. Never track passwords.
### **Applies To**
  - *.js
  - *.jsx
  - *.ts
  - *.tsx
  - *.py

## Client-Side Only Tracking

### **Id**
analytics-client-only
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - track\(['"](?:Purchase|Payment|Transaction|Checkout)\w*['"]\)(?!.{0,500}//.*server)
  - analytics\.track.{0,100}\b(revenue|payment|order)\b(?!.{0,500}//.*server-side)
### **Message**
Critical business event tracked only on client. Client-side tracking is unreliable (ad blockers, errors).
### **Fix Action**
Implement server-side tracking for revenue/conversion events as source of truth
### **Applies To**
  - *.js
  - *.jsx
  - *.ts
  - *.tsx

## Missing User Identification

### **Id**
analytics-no-user-id
### **Severity**
error
### **Type**
regex
### **Pattern**
  - analytics\.track\((?!.{0,200}userId)
  - track\(['"]\w+['"]\s*,\s*\{(?!.{0,200}\buser_id\b)
### **Message**
Event tracked without user ID. Can't build user journey or retention analysis without user identification.
### **Fix Action**
Include userId in all events after login. Use anonymous_id for pre-login tracking.
### **Applies To**
  - *.js
  - *.jsx
  - *.ts
  - *.tsx

## Hardcoded Event Properties

### **Id**
analytics-hardcoded-properties
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - track\(['"]\w+['"]\s*,\s*\{\s*['"]\w+['"]\s*:\s*['"]\w+['"]\s*\}
### **Message**
Event properties appear hardcoded. Properties should be dynamic to capture actual state.
### **Fix Action**
Use variables for properties to capture real values: { buttonText: button.innerText, pageUrl: window.location.href }
### **Applies To**
  - *.js
  - *.jsx
  - *.ts
  - *.tsx

## Missing Contextual Properties

### **Id**
analytics-no-context
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - track\(['"]\w+['"]\s*,\s*\{\s*\}\s*\)
  - track\(['"]\w+['"]\s*\)(?!.{0,100}\{)
### **Message**
Event tracked with no properties. Context is essential for analysis (what, where, when, how).
### **Fix Action**
Add properties: page, section, item_id, source, timestamp, etc.
### **Applies To**
  - *.js
  - *.jsx
  - *.ts
  - *.tsx

## Missing Analytics Error Handling

### **Id**
analytics-no-error-handling
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - analytics\.track\((?!.{0,500}\btry\b)(?!.{0,500}\bcatch\b)
  - track\(['"]\w+['"](?!.{0,500}\.catch)
### **Message**
No error handling for analytics calls. Failed tracking calls can crash app or go unnoticed.
### **Fix Action**
Wrap analytics calls in try-catch or use .catch() for promise-based tracking
### **Applies To**
  - *.js
  - *.jsx
  - *.ts
  - *.tsx

## Synchronous Analytics Blocking UI

### **Id**
analytics-sync-blocking
### **Severity**
error
### **Type**
regex
### **Pattern**
  - await\s+analytics\.track
  - track\(['"]\w+['"].*\)\.then\(.*=>.*\{[^}]{100,}\}
### **Message**
Synchronous or blocking analytics call. Analytics should never block user interactions.
### **Fix Action**
Make analytics fire-and-forget. Don't await unless critical for UX (e.g., navigation tracking)
### **Applies To**
  - *.js
  - *.jsx
  - *.ts
  - *.tsx

## Missing Page View Tracking

### **Id**
analytics-no-page-tracking
### **Severity**
error
### **Type**
regex
### **Pattern**
  - function\s+\w*Router\w*|<Router|useRouter\(\)(?!.{0,500}analytics\.page)
  - Route\s+path=(?!.{0,500}analytics\.page)
### **Message**
Router setup without page view tracking. Page views are fundamental for understanding user flow.
### **Fix Action**
Add analytics.page() call in router middleware or useEffect on route changes
### **Applies To**
  - *.js
  - *.jsx
  - *.ts
  - *.tsx

## Inconsistent Property Casing

### **Id**
analytics-inconsistent-casing
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - \{\s*[A-Z]\w+:
  - \{\s*\w+-\w+:
### **Message**
Inconsistent property casing detected. Mix of camelCase, PascalCase, or kebab-case makes querying difficult.
### **Fix Action**
Standardize on one convention across all events (recommend snake_case or camelCase)
### **Applies To**
  - *.js
  - *.jsx
  - *.ts
  - *.tsx

## Missing Privacy Consent Check

### **Id**
analytics-no-consent-check
### **Severity**
error
### **Type**
regex
### **Pattern**
  - analytics\.track\((?!.{0,200}\bconsentGiven\b)(?!.{0,200}\bhasConsent\b)
  - track\(['"]\w+['"](?!.{0,300}if\s*\(.{0,50}consent)
### **Message**
Analytics tracking without consent check. Required for GDPR compliance in EU.
### **Fix Action**
Check consent status before tracking: if (hasConsent()) { analytics.track(...) }
### **Applies To**
  - *.js
  - *.jsx
  - *.ts
  - *.tsx

## Potentially Undefined Properties

### **Id**
analytics-undefined-properties
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - track\(['"]\w+['"]\s*,\s*\{[^}]*\buser\.\w+[^}]*\}\)(?!.{0,100}\?)
  - properties:\s*\{[^}]*\w+\.\w+\.\w+[^}]*\}(?!.{0,100}\?)
### **Message**
Nested object properties without null checks may cause tracking errors.
### **Fix Action**
Use optional chaining: { userName: user?.name, orgId: user?.org?.id }
### **Applies To**
  - *.js
  - *.jsx
  - *.ts
  - *.tsx