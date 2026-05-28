# Fintech Integration - Sharp Edges

## Missing Idempotency Key Causes Duplicate Charges

### **Id**
missing-idempotency-key
### **Severity**
critical
### **Summary**
Network retries without idempotency create duplicate payments
### **Symptoms**
  - Customer charged multiple times
  - Support tickets for double charges
  - Refund requests spike after outages
### **Why**
  Network failures happen. When a payment request times out, the client
  retries. Without an idempotency key, Stripe processes each retry as
  a new payment. Customer gets charged 2-3x.
  
### **Gotcha**
  # No idempotency key
  payment_intent = stripe.PaymentIntent.create(
      amount=5000,
      currency='usd',
      customer=customer_id
  )
  
  # If this times out and retries, customer charged twice!
  
### **Solution**
  # Always include idempotency key
  idempotency_key = f"{user_id}:{order_id}:{uuid.uuid4().hex[:8]}"
  
  payment_intent = stripe.PaymentIntent.create(
      amount=5000,
      currency='usd',
      customer=customer_id,
      idempotency_key=idempotency_key  # Safe to retry
  )
  
  # Stripe returns same result for same idempotency key
  

## Unverified Webhooks Enable Spoofing

### **Id**
webhook-signature-skip
### **Severity**
critical
### **Summary**
Attackers can fake payment confirmations
### **Symptoms**
  - Orders marked paid without actual payment
  - Fraudulent refund requests
  - Inventory discrepancies
### **Why**
  Webhook endpoints are public URLs. Anyone can POST to them.
  Without signature verification, attackers can send fake
  payment.succeeded events and get products for free.
  
### **Gotcha**
  @app.post("/webhooks/stripe")
  async def stripe_webhook(request: Request):
      payload = await request.json()
      event_type = payload['type']  # Trusting unverified data!
  
      if event_type == 'payment_intent.succeeded':
          fulfill_order(payload['data']['object'])  # Fraud!
  
### **Solution**
  @app.post("/webhooks/stripe")
  async def stripe_webhook(request: Request):
      payload = await request.body()
      signature = request.headers.get('stripe-signature')
  
      try:
          event = stripe.Webhook.construct_event(
              payload,
              signature,
              webhook_secret  # From Stripe Dashboard
          )
      except stripe.error.SignatureVerificationError:
          raise HTTPException(status_code=400, detail="Invalid signature")
  
      # Now safe to process
      if event.type == 'payment_intent.succeeded':
          fulfill_order(event.data.object)
  

## Plaid Access Tokens Expire Without Warning

### **Id**
plaid-token-expiry
### **Severity**
high
### **Summary**
Bank connections break and users must relink
### **Symptoms**
  - Transaction sync stops working
  - Users complain about 'disconnected' banks
  - ITEM_LOGIN_REQUIRED errors
### **Why**
  Plaid access tokens can expire when banks require re-authentication.
  This happens after password changes, security updates, or bank
  policy changes. Without handling, your app silently loses access.
  
### **Gotcha**
  # Assuming token works forever
  transactions = plaid_client.transactions_get(access_token, ...)
  
  # Works for months... then suddenly fails
  # No notification to user, data goes stale
  
### **Solution**
  # Handle Plaid webhooks for token issues
  @app.post("/webhooks/plaid")
  async def plaid_webhook(request: Request):
      payload = await request.json()
  
      if payload['webhook_type'] == 'ITEM':
          if payload['webhook_code'] == 'ERROR':
              # Token needs refresh
              await notify_user_relink(payload['item_id'])
  
          elif payload['webhook_code'] == 'PENDING_EXPIRATION':
              # Proactive warning
              await send_relink_reminder(payload['item_id'])
  
      elif payload['webhook_type'] == 'TRANSACTIONS':
          if payload['webhook_code'] == 'SYNC_UPDATES_AVAILABLE':
              await sync_transactions(payload['item_id'])
  

## ACH Transfers Take 3-5 Business Days

### **Id**
ach-not-instant
### **Severity**
medium
### **Summary**
Treating ACH as instant leads to premature fulfillment
### **Symptoms**
  - Orders shipped before payment clears
  - Returns create negative balances
  - Fraud via 'succeeded' status confusion
### **Why**
  ACH bank transfers are not instant. A 'pending' charge can fail
  days later due to insufficient funds, closed account, or fraud.
  Treating 'pending' as 'succeeded' leads to losses.
  
### **Gotcha**
  charge = stripe.Charge.create(
      amount=10000,
      currency='usd',
      source=bank_account_id
  )
  
  if charge.status == 'pending':
      fulfill_order()  # Dangerous! Payment hasn't cleared
  
### **Solution**
  # Wait for actual settlement via webhook
  @app.post("/webhooks/stripe")
  async def handle_ach(request: Request):
      event = verify_webhook(request)
  
      if event.type == 'charge.succeeded':
          # ACH has actually cleared
          await fulfill_order(event.data.object)
  
      elif event.type == 'charge.failed':
          # ACH failed after days
          await cancel_order(event.data.object)
          await notify_customer_payment_failed()
  
  # For high-value orders, consider waiting for settlement
  

## Storing Raw Card Numbers Violates PCI

### **Id**
storing-credentials
### **Severity**
critical
### **Summary**
Handling card data directly creates compliance nightmare
### **Symptoms**
  - PCI DSS audit failures
  - Security breach liability
  - Massive fines and reputation damage
### **Why**
  PCI DSS compliance for storing card numbers is extremely expensive
  and complex. One breach can cost millions. Stripe and Plaid handle
  this so you don't have to.
  
### **Gotcha**
  # Never do this
  card_number = request.form['card_number']
  cvv = request.form['cvv']
  
  # Store in database
  db.execute("INSERT INTO cards (number, cvv) VALUES (?, ?)",
             card_number, cvv)  # Massive liability!
  
### **Solution**
  # Use Stripe.js to tokenize on frontend
  # Card numbers never touch your server
  
  // Frontend (Stripe.js)
  const {token} = await stripe.createToken(cardElement);
  // Send only token.id to your server
  
  // Backend
  customer = stripe.Customer.create(source=token_id)
  # Stripe stores card securely, you store customer_id
  
  # Never log card data
  logger.info(f"Created customer {customer.id}")  # OK
  # logger.info(f"Card: {card_number}")  # NEVER
  