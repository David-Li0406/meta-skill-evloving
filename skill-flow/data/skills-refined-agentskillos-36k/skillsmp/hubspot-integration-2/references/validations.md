# Hubspot Integration - Validations

## Hardcoded HubSpot API Key

### **Id**
hardcoded-api-key
### **Severity**
error
### **Description**
API keys must never be hardcoded
### **Pattern**
  (hapikey|HUBSPOT.*KEY)\s*[:=]\s*["'][a-f0-9-]{36}["']
  
### **Message**
Hardcoded HubSpot API key detected. Use environment variables. Note: API keys are deprecated - use Private App tokens.
### **Autofix**


## Hardcoded HubSpot Access Token

### **Id**
hardcoded-access-token
### **Severity**
error
### **Description**
Access tokens must use environment variables
### **Pattern**
  (accessToken|HUBSPOT.*TOKEN)\s*[:=]\s*["']pat-[a-zA-Z0-9-]+["']
  
### **Message**
Hardcoded HubSpot access token. Use environment variables.
### **Autofix**


## Hardcoded Client Secret

### **Id**
hardcoded-client-secret
### **Severity**
error
### **Description**
OAuth client secrets must be secured
### **Pattern**
  (clientSecret|CLIENT_SECRET)\s*[:=]\s*["'][a-f0-9-]{36}["']
  
### **Message**
Hardcoded client secret. Use environment variables.
### **Autofix**


## Missing Webhook Signature Validation

### **Id**
missing-webhook-validation
### **Severity**
error
### **Description**
Webhook endpoints must validate HubSpot signatures
### **Pattern**
  (webhooks?.*hubspot|hubspot.*webhooks?).*\.(post|action)
  
### **Anti Pattern**
  (X-HubSpot-Signature|validateSignature|hubspot.*signature)
  
### **Message**
Webhook endpoint without signature validation. Validate X-HubSpot-Signature-v3.
### **Autofix**


## Missing Rate Limit Handling

### **Id**
missing-rate-limit-handling
### **Severity**
warning
### **Description**
API calls should handle 429 responses
### **Pattern**
  hubspotClient\.crm\.|hubspotClient\.marketing\.
  
### **Anti Pattern**
  (retry|429|rate.?limit|Bottleneck|limiter)
  
### **Message**
HubSpot API calls without rate limit handling. Implement retry logic with backoff.
### **Autofix**


## Unthrottled Parallel API Calls

### **Id**
parallel-api-calls
### **Severity**
warning
### **Description**
Parallel calls can exceed rate limits
### **Pattern**
  Promise\.all\(.*hubspotClient
  
### **Anti Pattern**
  (Bottleneck|limiter|throttle)
  
### **Message**
Parallel HubSpot API calls without throttling. Use rate limiter.
### **Autofix**


## Missing Pagination for List Calls

### **Id**
missing-pagination
### **Severity**
warning
### **Description**
List endpoints return paginated results
### **Pattern**
  \.(getPage|getAll|search)\(\)
  
### **Anti Pattern**
  (while|paging|after)
  
### **Message**
API call without pagination handling. Implement cursor-based pagination.
### **Autofix**


## Individual Operations in Loop

### **Id**
individual-operations-loop
### **Severity**
info
### **Description**
Use batch operations for multiple items
### **Pattern**
  (for|forEach|map).*hubspotClient\.(crm|marketing)\.[^.]+\.(basicApi|searchApi)\.(create|update|getById)
  
### **Message**
Individual API calls in loop. Consider batch operations for better performance.
### **Autofix**


## Token Storage Without Expiry

### **Id**
token-without-expiry
### **Severity**
warning
### **Description**
OAuth tokens expire and need refresh logic
### **Pattern**
  (accessToken|hubspotToken)\s*[:=]
  
### **Anti Pattern**
  (expir|refresh|expiresAt|expiresIn)
  
### **Message**
Token storage without expiry tracking. Store expiresAt for refresh logic.
### **Autofix**


## Deprecated API Key Usage

### **Id**
deprecated-api-key
### **Severity**
error
### **Description**
API keys are deprecated
### **Pattern**
  (hapikey|apiKey.*hubspot|new.*Client\(\{.*apiKey)
  
### **Message**
Using deprecated API key. Migrate to Private App token or OAuth 2.0.
### **Autofix**


## Missing Error Handling for API Calls

### **Id**
missing-error-handling
### **Severity**
warning
### **Description**
HubSpot API calls should handle errors
### **Pattern**
  await\s+hubspotClient\.
  
### **Anti Pattern**
  (try|catch|\.catch|userErrors)
  
### **Message**
API call without error handling. Wrap in try/catch.
### **Autofix**


## Silently Swallowing Errors

### **Id**
silent-error-swallow
### **Severity**
warning
### **Description**
Errors should be logged or handled
### **Pattern**
  catch\s*\([^)]*\)\s*\{\s*(return|continue|\})
  
### **Message**
Catching error without logging or handling. Log errors for debugging.
### **Autofix**


## Using v3 Associations API

### **Id**
v3-associations-api
### **Severity**
warning
### **Description**
Associations v4 is current, v3 is deprecated
### **Pattern**
  associations\.(batchApi|basicApi)\.(?!v4)
  
### **Message**
Using v3 associations API. Upgrade to v4 with associationCategory.
### **Autofix**


## Missing Association Category

### **Id**
missing-association-category
### **Severity**
warning
### **Description**
v4 associations require category field
### **Pattern**
  associationTypeId(?!.*associationCategory)
  
### **Message**
Association without category. Add associationCategory for v4 API.
### **Autofix**
