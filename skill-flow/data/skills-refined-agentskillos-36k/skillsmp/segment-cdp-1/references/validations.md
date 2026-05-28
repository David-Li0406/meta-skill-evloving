# Segment Cdp - Validations

## Dynamic Event Name

### **Id**
dynamic-event-name
### **Severity**
error
### **Description**
Event names should be static, not include dynamic values
### **Pattern**
  analytics\.track\(`[^`]*\$\{
  
### **Message**
Dynamic event name detected. Use static event names with dynamic properties.
### **Autofix**


## Inconsistent Event Name Casing

### **Id**
inconsistent-event-casing
### **Severity**
warning
### **Description**
Event names should follow consistent casing convention
### **Pattern**
  analytics\.track\(['"][a-z].*[A-Z]
  
### **Message**
Mixed casing in event name. Use consistent convention (e.g., Title Case).
### **Autofix**


## Track Without Prior Identify

### **Id**
track-without-identify
### **Severity**
warning
### **Description**
Users should be identified before tracking critical events
### **Pattern**
  analytics\.track.*Order|Purchase|Subscribe
  
### **Anti Pattern**
  analytics\.identify
  
### **Message**
Revenue/conversion event without identify. Ensure user is identified.
### **Autofix**


## Missing Analytics Reset on Logout

### **Id**
missing-reset-on-logout
### **Severity**
warning
### **Description**
Analytics should be reset when user logs out
### **Pattern**
  (signOut|logout|handleLogout)
  
### **Anti Pattern**
  analytics\.reset
  
### **Message**
Logout without analytics.reset(). Anonymous ID will persist to next user.
### **Autofix**


## Hardcoded Segment Write Key

### **Id**
hardcoded-write-key
### **Severity**
error
### **Description**
Write key should use environment variables
### **Pattern**
  writeKey\s*[:=]\s*['"][a-zA-Z0-9]{20,}['"]
  
### **Message**
Hardcoded Segment write key. Use environment variables.
### **Autofix**


## PII Sent to All Destinations

### **Id**
pii-without-controls
### **Severity**
warning
### **Description**
PII should have destination controls
### **Pattern**
  analytics\.(track|identify).*email|phone|ssn|address
  
### **Anti Pattern**
  integrations
  
### **Message**
PII in tracking without destination controls. Consider limiting destinations.
### **Autofix**


## Event Without Proper Timestamp

### **Id**
missing-timestamp
### **Severity**
info
### **Description**
Explicit timestamps help with historical data
### **Pattern**
  serverTrack.*\{[^}]*\}
  
### **Anti Pattern**
  timestamp
  
### **Message**
Server track without explicit timestamp. Consider adding timestamp.
### **Autofix**


## Potentially Large Property Values

### **Id**
large-property-values
### **Severity**
warning
### **Description**
Properties over 32KB will be rejected
### **Pattern**
  analytics\.track.*innerHTML|innerText|JSON\.stringify
  
### **Message**
Potentially large property value. Segment has 32KB per event limit.
### **Autofix**


## Tracking Before Consent Check

### **Id**
tracking-before-consent
### **Severity**
error
### **Description**
GDPR requires consent before tracking
### **Pattern**
  analytics\.load.*analytics\.(page|track)
  
### **Anti Pattern**
  consent|wrapper|hasConsent
  
### **Message**
Tracking without consent check. Implement consent management for GDPR.
### **Autofix**
