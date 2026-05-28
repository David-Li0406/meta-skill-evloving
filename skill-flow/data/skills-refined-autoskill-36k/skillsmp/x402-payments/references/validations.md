# X402 Payments - Validations

## Payment Verification Before Serving

### **Id**
check-payment-verification
### **Description**
Ensure payment is verified before content delivery
### **Pattern**
(res\.send|res\.json|return.*content)(?!.*await.*verify)
### **File Glob**
**/*.{ts,js}
### **Match**
present
### **Context Pattern**
402|payment|paywall|gate
### **Message**
Verify payment before serving content - never serve first and verify later
### **Severity**
critical
### **Autofix**


## Proper 402 Status Code Usage

### **Id**
check-402-status-code
### **Description**
Use HTTP 402 for payment required responses
### **Pattern**
status\(402\)|402.*Payment.*Required
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
payment.*required|paywall|gate.*content
### **Message**
Use HTTP 402 Payment Required status for payment-gated content
### **Severity**
error
### **Autofix**


## L402 Authentication Header

### **Id**
check-payment-header-format
### **Description**
Use proper WWW-Authenticate header for 402 responses
### **Pattern**
WWW-Authenticate.*L402|Authorization.*L402
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
402|payment.*header
### **Message**
Include WWW-Authenticate: L402 header in 402 responses
### **Severity**
warning
### **Autofix**


## Macaroon Secret in Environment

### **Id**
check-macaroon-secret
### **Description**
Macaroon secret should not be hardcoded
### **Pattern**
(macaroon|MACAROON).*(secret|SECRET|key|KEY).*['"][a-zA-Z0-9]{20,}['"]
### **File Glob**
**/*.{ts,js}
### **Match**
present
### **Message**
Macaroon secrets must be in environment variables, not hardcoded
### **Severity**
critical
### **Autofix**


## Lightning Invoice Expiry Handling

### **Id**
check-invoice-expiry
### **Description**
Check for invoice expiration before processing
### **Pattern**
expir(y|es)|creation_date.*\+.*expiry
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
invoice|bolt11|lnbc
### **Message**
Always check invoice expiration before accepting payment
### **Severity**
error
### **Autofix**


## Preimage Not Logged

### **Id**
check-preimage-logging
### **Description**
Never log payment preimages
### **Pattern**
(console|logger|log)\.(log|info|debug|warn|error).*preimage
### **File Glob**
**/*.{ts,js}
### **Match**
present
### **Message**
CRITICAL: Never log preimages - they are payment proof secrets
### **Severity**
critical
### **Autofix**


## Preimage Storage Safety

### **Id**
check-preimage-storage
### **Description**
Store hashed preimages, not raw values
### **Pattern**
preimage.*=.*save|store.*preimage|insert.*preimage
### **File Glob**
**/*.{ts,js}
### **Match**
present
### **Message**
Store sha256(preimage) not raw preimage - raw preimages are payment proof
### **Severity**
error
### **Autofix**


## Payment Idempotency Handling

### **Id**
check-idempotency-key
### **Description**
Prevent double-processing of payments
### **Pattern**
idempoten|setnx|unique.*constraint|upsert
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
payment|webhook|process
### **Message**
Implement idempotency to prevent double-processing payments
### **Severity**
error
### **Autofix**


## Exchange Rate Locking

### **Id**
check-exchange-rate-lock
### **Description**
Lock exchange rates at quote time
### **Pattern**
rate.*lock|quote.*expire|price.*valid
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
exchange|convert|price.*crypto
### **Message**
Lock exchange rates at quote time to prevent rate manipulation
### **Severity**
warning
### **Autofix**


## Testnet Configuration Detection

### **Id**
check-testnet-detection
### **Description**
Detect accidental testnet usage in production
### **Pattern**
testnet|signet|lntb|sepolia|goerli|84532
### **File Glob**
**/*.{ts,js,env}
### **Match**
present
### **Context Pattern**
production|mainnet|PROD
### **Message**
Testnet configuration detected - verify this is intentional
### **Severity**
warning
### **Autofix**


## Webhook Signature Verification

### **Id**
check-webhook-signature
### **Description**
Verify webhook signatures before processing
### **Pattern**
verify.*signature|signature.*verify|hmac
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
webhook|callback|notify
### **Message**
Always verify webhook signatures before processing payment events
### **Severity**
critical
### **Autofix**


## Payment Amount Validation

### **Id**
check-amount-validation
### **Description**
Validate payment amounts match expected values
### **Pattern**
amount.*>=|amount.*===|validateAmount
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
payment|invoice|verify
### **Message**
Validate payment amount matches expected value
### **Severity**
error
### **Autofix**


## Refund Address Collection

### **Id**
check-refund-address
### **Description**
Collect refund address for non-Lightning payments
### **Pattern**
refund.*address|return.*address
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
l2|erc20|usdc|eth.*payment
### **Message**
Consider collecting refund address for L2 payments
### **Severity**
info
### **Autofix**


## Payment Timeout Handling

### **Id**
check-timeout-handling
### **Description**
Handle payment verification timeouts gracefully
### **Pattern**
timeout|AbortController|Promise\.race
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
payment.*verif|check.*paid
### **Message**
Implement timeout handling for payment verification
### **Severity**
warning
### **Autofix**


## Chain ID Validation for L2 Payments

### **Id**
check-chain-id-validation
### **Description**
Validate user is on correct chain
### **Pattern**
chainId|chain_id|getChainId
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
l2|layer.*2|connect.*wallet
### **Message**
Validate chain ID to prevent payments on wrong network
### **Severity**
error
### **Autofix**


## Transaction Confirmation Waiting

### **Id**
check-confirmation-wait
### **Description**
Wait for sufficient confirmations on L2
### **Pattern**
waitForTransaction|confirmations|blockNumber
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
l2.*payment|onchain.*verify
### **Message**
Wait for transaction confirmations before granting access
### **Severity**
error
### **Autofix**


## Minimum Payment Amount

### **Id**
check-dust-limit
### **Description**
Enforce minimum payment amounts
### **Pattern**
minimum|MIN_AMOUNT|dust|too.*small
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
payment.*amount|create.*invoice
### **Message**
Enforce minimum payment amounts to avoid dust transactions
### **Severity**
warning
### **Autofix**


## Payment Request Rate Limiting

### **Id**
check-rate-limiting
### **Description**
Rate limit invoice/quote generation
### **Pattern**
rateLimit|rate.*limit|throttle
### **File Glob**
**/*.{ts,js}
### **Match**
absent_in_context
### **Context Pattern**
generate.*invoice|create.*quote|402.*response
### **Message**
Rate limit payment request generation to prevent abuse
### **Severity**
warning
### **Autofix**
