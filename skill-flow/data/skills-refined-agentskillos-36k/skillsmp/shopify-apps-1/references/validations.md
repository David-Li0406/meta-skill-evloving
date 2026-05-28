# Shopify Apps - Validations

## Hardcoded Shopify API Secret

### **Id**
hardcoded-api-secret
### **Severity**
error
### **Description**
API secrets must never be hardcoded
### **Pattern**
  (SHOPIFY_API_SECRET|apiSecretKey)\s*[:=]\s*["'][a-z0-9]{32,}["']
  
### **Message**
Hardcoded Shopify API secret. Use environment variables.
### **Autofix**


## Hardcoded Shopify API Key

### **Id**
hardcoded-api-key
### **Severity**
error
### **Description**
API keys should use environment variables
### **Pattern**
  (SHOPIFY_API_KEY|apiKey)\s*[:=]\s*["'][a-z0-9]{32}["']
  
### **Message**
Hardcoded Shopify API key. Use environment variables.
### **Autofix**


## Missing HMAC Verification

### **Id**
missing-hmac-verification
### **Severity**
error
### **Description**
Webhook endpoints must verify HMAC signature
### **Pattern**
  (webhooks|webhook).*\.(post|action)
  
### **Anti Pattern**
  (authenticate\.webhook|verifyWebhookRequest|X-Shopify-Hmac)
  
### **Message**
Webhook handler without HMAC verification. Use authenticate.webhook().
### **Autofix**


## Synchronous Webhook Processing

### **Id**
sync-webhook-processing
### **Severity**
warning
### **Description**
Webhook handlers should respond quickly
### **Pattern**
  authenticate\.webhook.*await.*await.*await
  
### **Message**
Multiple await calls in webhook handler. Consider async processing.
### **Autofix**


## Missing Webhook Response

### **Id**
missing-webhook-response
### **Severity**
error
### **Description**
Webhooks must return 200 status
### **Pattern**
  authenticate\.webhook.*\n(?!.*return.*Response|.*return.*200)
  
### **Message**
Webhook handler may not return proper response.
### **Autofix**


## Duplicate Webhook Registration

### **Id**
duplicate-webhook-registration
### **Severity**
warning
### **Description**
Webhooks should be defined in TOML only
### **Pattern**
  (afterAuth|registerWebhooks|webhookSubscriptionCreate)
  
### **Message**
Code-based webhook registration. Define webhooks in shopify.app.toml.
### **Autofix**


## REST API Usage

### **Id**
rest-api-usage
### **Severity**
info
### **Description**
REST API is deprecated, use GraphQL
### **Pattern**
  (/admin/api/.*\.json|admin-rest-api|RestApiClient)
  
### **Message**
REST API usage detected. Consider migrating to GraphQL.
### **Autofix**


## Missing Rate Limit Handling

### **Id**
missing-rate-limit-handling
### **Severity**
warning
### **Description**
API calls should handle 429 responses
### **Pattern**
  admin\.graphql\(|fetch\(.*admin
  
### **Anti Pattern**
  (retry|backoff|429|rate.?limit)
  
### **Message**
API call without rate limit handling. Implement retry logic.
### **Autofix**


## In-Memory Session Storage

### **Id**
in-memory-session-storage
### **Severity**
warning
### **Description**
In-memory sessions don't scale
### **Pattern**
  (MemorySessionStorage|new Map\(\)|sessions\s*=\s*\{\})
  
### **Message**
In-memory session storage. Use PrismaSessionStorage or similar.
### **Autofix**


## Missing Session Validation

### **Id**
missing-session-validation
### **Severity**
error
### **Description**
Routes should validate session
### **Pattern**
  export.*loader.*\{(?!.*authenticate)
  
### **Message**
Loader without authentication. Use authenticate.admin(request).
### **Autofix**


## Missing GDPR Webhook Handlers

### **Id**
missing-gdpr-handlers
### **Severity**
error
### **Description**
GDPR webhooks are mandatory
### **Pattern**
  (ORDERS_CREATE|PRODUCTS_UPDATE)
  
### **Anti Pattern**
  (CUSTOMERS_DATA_REQUEST|CUSTOMERS_REDACT|SHOP_REDACT)
  
### **Message**
Missing GDPR webhook handlers. Implement all three GDPR handlers.
### **Autofix**
