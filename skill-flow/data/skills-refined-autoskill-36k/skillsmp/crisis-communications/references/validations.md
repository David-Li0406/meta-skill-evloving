# Crisis Communications - Validations

## Service Without Status Page

### **Id**
no-status-page-integration
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - healthCheck|health-check|healthEndpoint
  - monitoring|uptime|availability
### **Message**
Health monitoring without status page integration detected.
### **Fix Action**
Integrate with a status page (Statuspage.io, Instatus, BetterUptime) for incident communications
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.js
### **Exceptions**
  - statuspage|status-page|instatus|betteruptime|cachet

## Error Handling Without Incident Logging

### **Id**
no-incident-logging
### **Severity**
info
### **Type**
regex
### **Pattern**
  - catch.*Error|catch.*error|catch.*e\)
  - onError|handleError|errorHandler
### **Message**
Error handling without incident logging system.
### **Fix Action**
Add incident logging (PagerDuty, Opsgenie, Sentry) for critical errors
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - pagerduty|opsgenie|sentry|incident|alert

## Hardcoded User-Facing Error Messages

### **Id**
hardcoded-error-messages
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - message:.*['"].*error.*['"]
  - toast\(.*['"].*failed.*['"]
  - alert\(.*['"].*error.*['"]
### **Message**
Hardcoded error messages may be inconsistent during incidents.
### **Fix Action**
Use centralized error message system for consistent incident communications
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - i18n|t\(|intl|messages\.|ERROR_MESSAGES

## App Without Maintenance Mode

### **Id**
no-maintenance-mode
### **Severity**
info
### **Type**
regex
### **Pattern**
  - isLoading|loading.*true|LoadingSpinner
  - fallback|Fallback|ErrorBoundary
### **Message**
Loading/error states without maintenance mode capability.
### **Fix Action**
Add maintenance mode feature for planned outages and incident communications
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - maintenance|MAINTENANCE|maintenanceMode|isMaintenanceMode

## API Failure Without User Notification

### **Id**
silent-api-failure
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - fetch\(|axios\.|api\.
  - \.catch.*=>.*\{\s*\}
  - catch.*console\.(log|error)
### **Message**
API calls may fail silently without user notification.
### **Fix Action**
Show user-friendly error messages when APIs fail during incidents
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - toast|notification|alert|showError|displayError

## API Calls Without Retry Logic

### **Id**
no-retry-logic
### **Severity**
info
### **Type**
regex
### **Pattern**
  - fetch\(|axios\.|useSWR|useQuery
### **Message**
API calls without retry logic may cause poor UX during partial outages.
### **Fix Action**
Add retry with exponential backoff for resilience during incidents
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - retry|Retry|attempts|maxRetries|exponentialBackoff

## API Calls Without Timeout

### **Id**
missing-timeout
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - fetch\(|axios\(
### **Message**
API calls without explicit timeout may hang during incidents.
### **Fix Action**
Set explicit timeouts to fail fast during outages
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - timeout|Timeout|signal|AbortController|AbortSignal

## External Calls Without Circuit Breaker

### **Id**
no-circuit-breaker
### **Severity**
info
### **Type**
regex
### **Pattern**
  - externalApi|thirdParty|external.*service
  - stripe|twilio|sendgrid|aws
### **Message**
External service calls without circuit breaker pattern.
### **Fix Action**
Implement circuit breaker for graceful degradation during third-party outages
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - circuitBreaker|CircuitBreaker|breaker|fallback.*external

## Generic Error Page Without Status Link

### **Id**
generic-error-page
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ErrorPage|error-page|500|ServerError
  - Something went wrong|Oops|Error occurred
### **Message**
Error page without link to status page.
### **Fix Action**
Include status page link on error pages for incident visibility
### **Applies To**
  - **/*.tsx
  - **/*.jsx
### **Exceptions**
  - status\..*\.com|statuspage|status-link|checkStatus

## Feature Without Graceful Degradation

### **Id**
no-graceful-degradation
### **Severity**
info
### **Type**
regex
### **Pattern**
  - feature.*enabled|isEnabled|featureFlag
  - enabled:.*true|toggle
### **Message**
Feature flags without graceful degradation handling.
### **Fix Action**
Add fallback behavior when features are disabled during incidents
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - fallback|graceful|degraded|offlineMode

## Service Without Health Check Endpoint

### **Id**
no-health-endpoint
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - app\.(get|post)|router\.(get|post)
  - createServer|express\(\)|fastify
### **Message**
Server without health check endpoint for monitoring.
### **Fix Action**
Add /health or /status endpoint for uptime monitoring and incident detection
### **Applies To**
  - **/*.ts
  - **/server*.ts
  - **/app*.ts
### **Exceptions**
  - /health|/status|healthCheck|readiness|liveness

## Scheduled Jobs Without Notification

### **Id**
no-downtime-notification
### **Severity**
info
### **Type**
regex
### **Pattern**
  - cron|schedule|setInterval
  - migration|migrate|seed
### **Message**
Scheduled operations without downtime notification system.
### **Fix Action**
Add notification system for scheduled maintenance and migrations
### **Applies To**
  - **/*.ts
  - **/cron*.ts
  - **/job*.ts
### **Exceptions**
  - notify|notification|announcement|statusUpdate

## Error Logs Without Request Context

### **Id**
log-without-context
### **Severity**
info
### **Type**
regex
### **Pattern**
  - console\.error|logger\.error|log\.error
### **Message**
Error logging without request context for incident debugging.
### **Fix Action**
Include request ID, user context, and timestamp in error logs
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - requestId|correlationId|traceId|userId|context

## Weasel Word - "Inconvenience"

### **Id**
weasel-word-inconvenience
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - ['"].*inconvenience.*['"]
  - any inconvenience|for the inconvenience
### **Message**
Using 'inconvenience' minimizes customer impact in error messages.
### **Fix Action**
Replace with specific impact acknowledgment (e.g., 'disruption to your work')
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.md
### **Exceptions**


## Weasel Word - "Some Users"

### **Id**
weasel-word-some-users
### **Severity**
info
### **Type**
regex
### **Pattern**
  - ['"].*some users.*['"]
  - ['"].*a small number.*['"]
### **Message**
Vague language 'some users' dismisses affected customers.
### **Fix Action**
Use specific numbers or 'many of you' to acknowledge impact
### **Applies To**
  - **/*.ts
  - **/*.tsx
  - **/*.md
### **Exceptions**
  - \d+.*users|percentage|%

## Passive Voice in Error Messages

### **Id**
passive-voice-error
### **Severity**
info
### **Type**
regex
### **Pattern**
  - was discovered|has been found|were affected
  - an error occurred|a problem was detected
### **Message**
Passive voice in errors obscures responsibility.
### **Fix Action**
Use active voice: 'We discovered...' or 'We detected...'
### **Applies To**
  - **/*.ts
  - **/*.tsx
### **Exceptions**
  - we discovered|we found|we detected|our team