# Fintech Integration

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Never store raw credentials
    ##### **Reason**
Use tokenization - Plaid/Stripe handle this
  
---
    ##### **Rule**
Idempotency keys always
    ##### **Reason**
Prevents duplicate payments
  
---
    ##### **Rule**
Webhook verification
    ##### **Reason**
Prevent spoofed events
  
---
    ##### **Rule**
Graceful degradation
    ##### **Reason**
Financial services must stay up
  
---
    ##### **Rule**
Audit everything
    ##### **Reason**
Compliance requires paper trail
### **Api Landscape**
  #### **Bank Data**
    - Plaid
    - MX
    - Yodlee
  #### **Payments**
    - Stripe
    - Adyen
    - Square
  #### **Identity**
    - Persona
    - Alloy
    - Jumio
  #### **Lending**
    - Blend
    - Amount
  #### **Crypto**
    - Coinbase
    - Circle
    - Fireblocks
  #### **Infrastructure**
    - Moov
    - Unit
    - Treasury Prime
### **Plaid Flow**
  - Create Link token with products/country
  - User completes Plaid Link
  - Exchange public token for access token
  - Store access token (encrypted)
  - Fetch accounts/transactions
### **Stripe Flow**
  - Create customer with idempotency key
  - Attach payment method (card/bank)
  - Create PaymentIntent with idempotency key
  - Handle webhook confirmation
  - Update internal records
### **Webhook Best Practices**
  - Verify signature before processing
  - Track processed event IDs for idempotency
  - Process asynchronously for reliability
  - Return 200 quickly, process in background
  - Implement retry logic for failures

## Anti-Patterns


---
  #### **Pattern**
No idempotency keys
  #### **Problem**
Duplicate charges possible
  #### **Solution**
Always use unique idempotency keys

---
  #### **Pattern**
Storing credentials
  #### **Problem**
Security breach risk
  #### **Solution**
Use tokenization

---
  #### **Pattern**
Ignoring webhooks
  #### **Problem**
Missed payment updates
  #### **Solution**
Implement robust webhook handling

---
  #### **Pattern**
No retry logic
  #### **Problem**
Failed payments stay failed
  #### **Solution**
Implement exponential backoff

---
  #### **Pattern**
Synchronous only
  #### **Problem**
Timeouts, poor UX
  #### **Solution**
Use webhooks for async updates