# Plaid Fintech - Validations

## Access Token Stored in Plain Text

### **Id**
plaintext-access-token
### **Severity**
error
### **Description**
Plaid access tokens must be encrypted at rest
### **Pattern**
  (accessToken|access_token)\s*[:=]\s*[^encrypt][^}]+
  
### **Anti Pattern**
  (encrypt|cipher|kms|vault)
  
### **Message**
Plaid access token appears to be stored unencrypted. Encrypt at rest.
### **Autofix**


## Plaid Secret in Client Code

### **Id**
exposed-plaid-secret
### **Severity**
error
### **Description**
Plaid secret must never be exposed to clients
### **Pattern**
  PLAID_SECRET|plaidSecret
  
### **Message**
Plaid secret may be exposed. Keep server-side only.
### **Autofix**


## Hardcoded Plaid Credentials

### **Id**
hardcoded-credentials
### **Severity**
error
### **Description**
Credentials must use environment variables
### **Pattern**
  (PLAID_CLIENT_ID|PLAID_SECRET)\s*[:=]\s*['"][a-f0-9]{20,}['"]
  
### **Message**
Hardcoded Plaid credentials. Use environment variables.
### **Autofix**


## Missing Webhook Signature Verification

### **Id**
missing-webhook-verification
### **Severity**
error
### **Description**
Plaid webhooks must verify JWT signature
### **Pattern**
  (webhooks?|plaid).*\.(post|action)
  
### **Anti Pattern**
  (plaid-verification|jwt\.verify|verifyWebhook)
  
### **Message**
Webhook handler without signature verification. Verify Plaid-Verification header.
### **Autofix**


## Using Cached Balance for Payment Decision

### **Id**
cached-balance-for-payment
### **Severity**
error
### **Description**
Use real-time balance for payment validation
### **Pattern**
  accountsGet.*payment|transfer|withdraw
  
### **Message**
Using accountsGet (cached) for payment. Use accountsBalanceGet for real-time balance.
### **Autofix**


## Missing Item Error State Handling

### **Id**
missing-item-error-handling
### **Severity**
warning
### **Description**
API calls should handle ITEM_LOGIN_REQUIRED
### **Pattern**
  (transactionsSync|accountsGet|authGet)
  
### **Anti Pattern**
  (ITEM_LOGIN_REQUIRED|item.*error|update.*mode)
  
### **Message**
API call without ITEM_LOGIN_REQUIRED handling. Handle item error states.
### **Autofix**


## Polling for Transactions Instead of Webhooks

### **Id**
polling-instead-of-webhooks
### **Severity**
warning
### **Description**
Use webhooks for transaction updates
### **Pattern**
  (setInterval|setTimeout).*transactionsSync
  
### **Message**
Polling for transactions. Configure webhooks for SYNC_UPDATES_AVAILABLE.
### **Autofix**


## Link Token Cached or Reused

### **Id**
cached-link-token
### **Severity**
warning
### **Description**
Link tokens are single-use and expire in 4 hours
### **Pattern**
  (linkToken|link_token).*(cache|global|static)
  
### **Message**
Link tokens should not be cached. Create fresh token for each session.
### **Autofix**


## Using Deprecated Public Key

### **Id**
deprecated-public-key
### **Severity**
error
### **Description**
Public key integration ended January 2025
### **Pattern**
  (publicKey|public_key|PLAID_PUBLIC_KEY)
  
### **Message**
Public key is deprecated. Use Link tokens instead.
### **Autofix**


## Transaction Sync Without Cursor Storage

### **Id**
missing-cursor-storage
### **Severity**
warning
### **Description**
Store cursor for incremental syncs
### **Pattern**
  transactionsSync.*cursor
  
### **Anti Pattern**
  (save|store|update).*cursor
  
### **Message**
Transaction sync without cursor persistence. Store cursor for incremental sync.
### **Autofix**


## Missing Sync Mutation Error Handling

### **Id**
missing-mutation-handling
### **Severity**
warning
### **Description**
Handle TRANSACTIONS_SYNC_MUTATION_DURING_PAGINATION
### **Pattern**
  transactionsSync.*while
  
### **Anti Pattern**
  MUTATION_DURING_PAGINATION
  
### **Message**
Pagination without mutation handling. Restart sync on mutation error.
### **Autofix**


## Non-Idempotent Webhook Handler

### **Id**
non-idempotent-webhook
### **Severity**
warning
### **Description**
Webhooks may be duplicated, handlers must be idempotent
### **Pattern**
  webhook.*\{.*await
  
### **Anti Pattern**
  (idempoten|duplicate|already.*processed|webhookLog)
  
### **Message**
Webhook handler may not be idempotent. Check for duplicate processing.
### **Autofix**
