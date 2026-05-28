# Browser Extension Builder - Validations

## Using Deprecated Manifest V2

### **Id**
manifest-v2
### **Severity**
high
### **Type**
pattern
### **Check**
Should use Manifest V3 for new extensions
### **Pattern**
"manifest_version":\s*2
### **Indicators**
  - manifest_version: 2
  - Using background pages
  - Legacy extension
### **Message**
Using Manifest V2 - Chrome requires V3 for new extensions.
### **Fix Action**
Migrate to Manifest V3 with service worker

## Excessive Permissions Requested

### **Id**
excessive-permissions
### **Severity**
high
### **Type**
pattern
### **Check**
Should only request necessary permissions
### **Pattern**
<all_urls>|\*://\*
### **Indicators**
  - All URLs permission
  - Wildcard host permissions
  - Many permissions listed
### **Message**
Requesting broad permissions - may cause store rejection.
### **Fix Action**
Use specific host_permissions and optional_permissions

## No Error Handling in Extension

### **Id**
no-error-handling
### **Severity**
medium
### **Type**
pattern
### **Check**
Should handle chrome API errors
### **Pattern**
chrome\.runtime\.lastError
### **Indicators**
  - No lastError checks
  - Unhandled promise rejections
  - Silent failures
### **Message**
Not checking chrome.runtime.lastError for errors.
### **Fix Action**
Check chrome.runtime.lastError after API calls

## Hardcoded URLs in Extension

### **Id**
hardcoded-urls
### **Severity**
medium
### **Type**
pattern
### **Check**
URLs should be configurable or use manifest
### **Pattern**
https?://[^"'\s]+(?:api|backend|server)
### **Indicators**
  - API URLs hardcoded
  - No configuration
  - Dev URLs in production
### **Message**
Hardcoded URLs may cause issues in production.
### **Fix Action**
Use chrome.storage or manifest for configuration

## Missing Extension Icons

### **Id**
no-icons
### **Severity**
low
### **Type**
conceptual
### **Check**
Should have icons in multiple sizes
### **Indicators**
  - No icons folder
  - Missing icon sizes
  - Default Chrome icon
### **Message**
Missing extension icons - affects store listing.
### **Fix Action**
Add icons in 16, 48, and 128 pixel sizes