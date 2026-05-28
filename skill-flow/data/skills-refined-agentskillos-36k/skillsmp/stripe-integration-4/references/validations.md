# Stripe Integration - Validations

## Webhook signature verification

### **Id**
stripe-webhook-signature
### **Severity**
critical
### **Type**
regex
### **Pattern**
stripe\.webhooks\.constructEvent
### **Message**
Stripe webhooks must verify signatures with constructEvent()
### **Fix Action**
Add signature verification: stripe.webhooks.constructEvent(rawBody, sig, secret)
### **Applies To**
  - **/webhook*.ts
  - **/webhook*.js
  - **/stripe*.ts
  - **/stripe*.js
### **Inverse**


## Webhook using raw body

### **Id**
stripe-raw-body
### **Severity**
critical
### **Type**
regex
### **Pattern**
req\.json\(\).*stripe|stripe.*req\.json\(\)
### **Message**
Webhook handlers must use raw body, not parsed JSON
### **Fix Action**
Use req.text() for App Router or express.raw() for Express
### **Applies To**
  - **/webhook*.ts
  - **/webhook*.js

## Idempotency key on payment creation

### **Id**
stripe-idempotency-payments
### **Severity**
error
### **Type**
regex
### **Pattern**
paymentIntents\.create\([^)]+\)(?!.*idempotencyKey)
### **Message**
Payment creation should use idempotency keys to prevent duplicates
### **Fix Action**
Add idempotencyKey option: { idempotencyKey: `payment_${orderId}` }
### **Applies To**
  - **/*.ts
  - **/*.js

## Idempotency key on subscription creation

### **Id**
stripe-idempotency-subscriptions
### **Severity**
error
### **Type**
regex
### **Pattern**
subscriptions\.create\([^)]+\)(?!.*idempotencyKey)
### **Message**
Subscription creation should use idempotency keys
### **Fix Action**
Add idempotencyKey option to prevent duplicate subscriptions
### **Applies To**
  - **/*.ts
  - **/*.js

## Checkout session metadata

### **Id**
stripe-checkout-metadata
### **Severity**
warning
### **Type**
regex
### **Pattern**
checkout\.sessions\.create\([^)]+\)(?!.*metadata)
### **Message**
Checkout sessions should include metadata to identify user/order in webhooks
### **Fix Action**
Add metadata: { userId, orderId } to checkout session
### **Applies To**
  - **/*.ts
  - **/*.js

## Test keys hardcoded

### **Id**
stripe-test-keys-in-code
### **Severity**
critical
### **Type**
regex
### **Pattern**
sk_test_[a-zA-Z0-9]+|pk_test_[a-zA-Z0-9]+
### **Message**
Stripe test keys should not be hardcoded - use environment variables
### **Fix Action**
Use process.env.STRIPE_SECRET_KEY and process.env.STRIPE_PUBLISHABLE_KEY
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Live keys hardcoded

### **Id**
stripe-live-keys-in-code
### **Severity**
critical
### **Type**
regex
### **Pattern**
sk_live_[a-zA-Z0-9]+|pk_live_[a-zA-Z0-9]+
### **Message**
CRITICAL: Live Stripe keys must NEVER be in code
### **Fix Action**
Remove immediately and rotate keys in Stripe dashboard
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Webhook secret hardcoded

### **Id**
stripe-webhook-secret-hardcoded
### **Severity**
critical
### **Type**
regex
### **Pattern**
whsec_[a-zA-Z0-9]+
### **Message**
Webhook secrets must not be hardcoded
### **Fix Action**
Use process.env.STRIPE_WEBHOOK_SECRET
### **Applies To**
  - **/*.ts
  - **/*.js

## Currency hardcoded as USD

### **Id**
stripe-currency-hardcoded
### **Severity**
warning
### **Type**
regex
### **Pattern**
currency:\s*['"]usd['"]
### **Message**
Consider making currency configurable for international support
### **Fix Action**
Use a price object or make currency a parameter
### **Applies To**
  - **/*.ts
  - **/*.js

## Amount not in cents

### **Id**
stripe-amount-cents
### **Severity**
warning
### **Type**
regex
### **Pattern**
amount:\s*(?!.*\*\s*100)[0-9]+(?!00\b)
### **Message**
Stripe amounts are in cents - ensure you're not passing dollars
### **Fix Action**
Multiply dollar amount by 100: amount: dollars * 100
### **Applies To**
  - **/*.ts
  - **/*.js

## Refund without reason

### **Id**
stripe-refund-without-reason
### **Severity**
warning
### **Type**
regex
### **Pattern**
refunds\.create\([^)]*\)(?!.*reason)
### **Message**
Refunds should include a reason for audit purposes
### **Fix Action**
Add reason parameter: reason: 'requested_by_customer'
### **Applies To**
  - **/*.ts
  - **/*.js

## Stripe API call without error handling

### **Id**
stripe-error-handling
### **Severity**
error
### **Type**
regex
### **Pattern**
await stripe\.[a-zA-Z]+\.[a-zA-Z]+\([^)]+\)(?![^;]*catch)
### **Message**
Stripe API calls should have error handling
### **Fix Action**
Wrap in try/catch and handle StripeError appropriately
### **Applies To**
  - **/*.ts
  - **/*.js

## Webhook handler without constructEvent

### **Id**
stripe-webhook-missing-construct-event
### **Severity**
critical
### **Type**
regex
### **Pattern**
stripe-signature|stripe_signature
### **Inverse**

### **Message**
Webhook handlers must verify signatures with stripe.webhooks.constructEvent()
### **Fix Action**
  Add signature verification:
  const sig = req.headers.get('stripe-signature');
  const event = stripe.webhooks.constructEvent(rawBody, sig, webhookSecret);
  
### **Applies To**
  - **/webhook*.ts
  - **/webhook*.js
  - **/api/stripe/**/*.ts

## Parsing JSON before signature verification

### **Id**
stripe-webhook-json-parse-before-verify
### **Severity**
critical
### **Type**
regex
### **Pattern**
(JSON\.parse|req\.json\(\)).*constructEvent|await req\.json\(\).*stripe
### **Message**
CRITICAL: JSON parsing before signature verification defeats security
### **Fix Action**
Use req.text() to get raw body, then verify signature, then parse if needed
### **Applies To**
  - **/webhook*.ts
  - **/webhook*.js

## Charge creation without idempotency key

### **Id**
stripe-idempotency-charges
### **Severity**
error
### **Type**
regex
### **Pattern**
charges\.create\([^)]+\)(?!.*idempotencyKey)
### **Message**
Charge creation should use idempotency keys to prevent duplicate charges
### **Fix Action**
Add { idempotencyKey: `charge_${orderId}` } as second argument
### **Applies To**
  - **/*.ts
  - **/*.js

## Refund creation without idempotency key

### **Id**
stripe-idempotency-refunds
### **Severity**
warning
### **Type**
regex
### **Pattern**
refunds\.create\([^)]+\)(?!.*idempotencyKey)
### **Message**
Refund creation should use idempotency keys to prevent duplicate refunds
### **Fix Action**
Add { idempotencyKey: `refund_${paymentId}` } as second argument
### **Applies To**
  - **/*.ts
  - **/*.js

## Transfer creation without idempotency key

### **Id**
stripe-idempotency-transfers
### **Severity**
error
### **Type**
regex
### **Pattern**
transfers\.create\([^)]+\)(?!.*idempotencyKey)
### **Message**
Transfer creation should use idempotency keys
### **Fix Action**
Add { idempotencyKey: `transfer_${id}` } as second argument
### **Applies To**
  - **/*.ts
  - **/*.js

## Test key without environment check

### **Id**
stripe-test-key-production-check
### **Severity**
error
### **Type**
regex
### **Pattern**
sk_test_[a-zA-Z0-9]{20,}|pk_test_[a-zA-Z0-9]{20,}
### **Message**
Test keys detected - ensure these are not used in production
### **Fix Action**
  Use environment-based key loading:
  const stripe = new Stripe(
    process.env.NODE_ENV === 'production'
      ? process.env.STRIPE_SECRET_KEY  // Live key
      : process.env.STRIPE_TEST_SECRET_KEY  // Test key
  );
  
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx
### **Exclude**
  - **/*.test.ts
  - **/*.test.js
  - **/*.spec.ts
  - **/__tests__/**

## Both test and live keys in same file

### **Id**
stripe-mixed-mode-detection
### **Severity**
critical
### **Type**
regex
### **Pattern**
(sk_test.*sk_live|sk_live.*sk_test)
### **Message**
CRITICAL: Both test and live keys in same file - potential mode confusion
### **Fix Action**
Use single environment variable STRIPE_SECRET_KEY that differs per environment
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.env*

## Hardcoded Stripe price ID

### **Id**
stripe-hardcoded-price-id
### **Severity**
warning
### **Type**
regex
### **Pattern**
price_[a-zA-Z0-9]{20,}
### **Message**
Hardcoded price IDs make updates difficult - consider using config or database
### **Fix Action**
Store price IDs in environment variables or database for easy updates
### **Applies To**
  - **/*.ts
  - **/*.js
### **Exclude**
  - **/*.env*
  - **/config.*

## Checkout success URL granting access directly

### **Id**
stripe-success-url-grants-access
### **Severity**
critical
### **Type**
regex
### **Pattern**
success.*url.*\?.*grant|success.*url.*\?.*activate|success.*url.*\?.*premium
### **Message**
CRITICAL: Never grant access from success URL - it can be visited directly
### **Fix Action**
Grant access from webhook only (checkout.session.completed event)
### **Applies To**
  - **/*.ts
  - **/*.js

## Customer ID exposed in URL

### **Id**
stripe-customer-id-in-url
### **Severity**
warning
### **Type**
regex
### **Pattern**
\?.*customer.*cus_[a-zA-Z0-9]+|cus_[a-zA-Z0-9]+.*\?
### **Message**
Customer IDs in URLs may leak via referrer headers
### **Fix Action**
Use session tokens instead of exposing Stripe IDs in URLs
### **Applies To**
  - **/*.ts
  - **/*.js

## Attempting to store card details

### **Id**
stripe-card-storage-attempt
### **Severity**
critical
### **Type**
regex
### **Pattern**
card_number|cardNumber|cc_number|cvv|cvc.*=.*req\.|card\.number
### **Message**
CRITICAL: Never store card details - use Stripe Elements and tokens
### **Fix Action**
Use Stripe.js Elements for secure card collection - never touch raw card data
### **Applies To**
  - **/*.ts
  - **/*.js

## Missing invoice.payment_failed webhook handler

### **Id**
stripe-missing-payment-failed-handler
### **Severity**
warning
### **Type**
regex
### **Pattern**
invoice\.payment_failed
### **Inverse**

### **Message**
No payment failure handler - you may lose recoverable revenue
### **Fix Action**
Add invoice.payment_failed handler to send dunning emails
### **Applies To**
  - **/webhook*.ts
  - **/webhook*.js
  - **/stripe*.ts

## Webhook returns 200 only after processing

### **Id**
stripe-webhook-200-after-processing
### **Severity**
warning
### **Type**
regex
### **Pattern**
constructEvent.*await.*return.*200|constructEvent.*process.*return.*200
### **Message**
Consider returning 200 immediately and processing asynchronously
### **Fix Action**
Queue webhook for processing, return 200 immediately to avoid Stripe retries
### **Applies To**
  - **/webhook*.ts
  - **/webhook*.js

## Amount divided for display without currency format

### **Id**
stripe-amount-division-display
### **Severity**
warning
### **Type**
regex
### **Pattern**
amount\s*/\s*100(?!.*Intl|.*toLocaleString|.*formatCurrency)
### **Message**
Dividing by 100 for display - use proper currency formatting
### **Fix Action**
  Use Intl.NumberFormat for proper currency display:
  new Intl.NumberFormat('en-US', { style: 'currency', currency }).format(amount / 100)
  
### **Applies To**
  - **/*.ts
  - **/*.js
  - **/*.tsx
  - **/*.jsx

## Connect operation without stripeAccount header

### **Id**
stripe-connect-missing-stripe-account
### **Severity**
warning
### **Type**
regex
### **Pattern**
(paymentIntents|charges|customers)\.create.*destination(?!.*stripeAccount)
### **Message**
Connect operations may need stripeAccount header for proper routing
### **Fix Action**
Add { stripeAccount: connectedAccountId } for connected account operations
### **Applies To**
  - **/*.ts
  - **/*.js