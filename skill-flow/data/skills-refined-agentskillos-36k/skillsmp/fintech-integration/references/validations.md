# Fintech Integration - Validations

## Stripe Call Without Idempotency Key

### **Id**
missing-idempotency-key
### **Severity**
error
### **Type**
regex
### **Pattern**
  - stripe\.PaymentIntent\.create\((?!.*idempotency_key)
  - stripe\.Charge\.create\((?!.*idempotency_key)
  - stripe\.Subscription\.create\((?!.*idempotency_key)
### **Message**
Stripe payment calls need idempotency keys to prevent duplicates.
### **Fix Action**
Add: idempotency_key=f'{user_id}:{order_id}:{uuid}'
### **Applies To**
  - **/*stripe*.py
  - **/*payment*.py

## Webhook Without Signature Verification

### **Id**
webhook-no-signature
### **Severity**
error
### **Type**
regex
### **Pattern**
  - webhook.*json\(\)(?!.*verify|.*signature|.*construct_event)
  - @.*post.*webhook(?!.*SignatureVerification|.*verify)
### **Message**
Webhooks must verify signatures to prevent spoofing.
### **Fix Action**
Use stripe.Webhook.construct_event() with signature header
### **Applies To**
  - **/*webhook*.py

## Hardcoded API Key

### **Id**
hardcoded-api-key
### **Severity**
error
### **Type**
regex
### **Pattern**
  - sk_live_[a-zA-Z0-9]{24}
  - sk_test_[a-zA-Z0-9]{24}
  - access-sandbox-[a-z0-9-]{36}
### **Message**
API keys must not be hardcoded in source code.
### **Fix Action**
Use environment variables: os.environ['STRIPE_API_KEY']
### **Applies To**
  - **/*.py

## Potential Card Number in Logs

### **Id**
card-number-logged
### **Severity**
error
### **Type**
regex
### **Pattern**
  - log.*card.*number
  - print.*\d{16}
  - logger.*cvv|cvc
### **Message**
Never log card numbers or CVV - PCI violation.
### **Fix Action**
Log only last 4 digits or token IDs
### **Applies To**
  - **/*.py

## ACH Treated as Instant

### **Id**
ach-treated-instant
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - charge.*pending.*fulfill
  - bank.*transfer.*status.*ship
### **Message**
ACH transfers take 3-5 days - don't fulfill on 'pending'.
### **Fix Action**
Wait for charge.succeeded webhook before fulfillment
### **Applies To**
  - **/*payment*.py
  - **/*order*.py

## Webhook Processing Without Idempotency

### **Id**
no-webhook-idempotency
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - def.*webhook(?!.*processed|.*idempotent|.*event_id)
### **Message**
Webhooks can be sent multiple times - track processed events.
### **Fix Action**
Store event_id and check before processing
### **Applies To**
  - **/*webhook*.py