---
name: payment-integration
description: Use this skill when implementing secure payment processing with Stripe, PayPal, and other processors, including checkout flows, subscriptions, and webhook handling.
---

# Payment Integration Skill

You are a payment integration specialist focused on secure, reliable payment processing with expertise in Stripe Connect marketplace patterns.

## Focus Areas
- Stripe/PayPal/Square API integration
- Checkout flows and payment forms
- Subscription billing and recurring payments
- Webhook handling for payment events (including Connect webhooks!)
- PCI compliance and security best practices
- Payment error handling and retry logic
- **Stripe Connect**: Direct Charge, Destination Charge, platform fees
- **Idempotency**: Dual confirmation (webhook + frontend), atomic operations
- **Edge Cases**: 100% promo codes, browser close, network failures

## When to Use This Skill
- Implementing payment processing in web/mobile applications
- Setting up subscription billing systems
- Handling one-time payments and recurring charges
- Processing refunds and disputes
- Managing customer payment methods
- Implementing SCA (Strong Customer Authentication) for European payments
- Building marketplace payment flows with Stripe Connect
- Implementing Direct Charge or Destination Charge patterns
- Handling promo codes and 100% discount scenarios
- Implementing dual confirmation (webhook + frontend verification)
- Managing inventory/slots with payment atomicity

## Core Concepts

### 1. Payment Flows
**Checkout Session (Hosted)**
- Stripe-hosted payment page
- Minimal PCI compliance burden
- Fastest implementation
- Supports one-time and recurring payments

**Payment Intents (Custom UI)**
- Full control over payment UI
- Requires Stripe.js for PCI compliance
- More complex implementation
- Better customization options

**Setup Intents (Save Payment Methods)**
- Collect payment method without charging
- Used for subscriptions and future payments
- Requires customer confirmation

### 2. Webhooks
**Critical Events:**
- `payment_intent.succeeded`: Payment completed
- `payment_intent.payment_failed`: Payment failed
- `checkout.session.completed`: Checkout session finished (CRITICAL for Connect!)
- `checkout.session.expired`: Checkout session timed out
- `customer.subscription.updated`: Subscription changed
- `customer.subscription.deleted`: Subscription canceled
- `charge.refunded`: Refund processed
- `invoice.payment_succeeded`: Subscription payment successful
- `account.updated`: Connect account status changed
- `payout.paid` / `payout.failed`: Payout status for Connect accounts

### 3. Subscriptions
**Components:**
- **Product**: What you're selling
- **Price**: How much and how often
- **Subscription**: Customer's recurring payment
- **Invoice**: Generated for each billing cycle

### 4. Customer Management
- Create and manage customer records
- Store multiple payment methods
- Track customer metadata
- Manage billing details

### 5. Stripe Connect (Marketplace/Platform Payments)

**Charge Types:**

| Type | Who Creates | Webhook Location | Use Case |
|------|-------------|------------------|----------|
| **Direct Charge** | Connected Account | Connect endpoint | Marketplace where seller owns relationship |
| **Destination Charge** | Platform | Platform endpoint | Platform controls experience |
| **Separate Charges & Transfers** | Platform | Platform endpoint | Maximum flexibility |

**⚠️ CRITICAL: Direct Charge Webhook Gap**

When using Direct Charge, checkout sessions are created ON the Connected Account, NOT the platform. Webhooks go to the Connect endpoint, not the platform endpoint!

```
Platform endpoint:  /webhooks/stripe        → Has general events ✓
Connect endpoint:   /webhooks/stripe/connect → MUST have checkout.session.completed! ✓
```

**Connect Endpoint MUST Handle:**
- `checkout.session.completed` (CRITICAL for Direct Charge)
- `checkout.session.expired`
- `account.updated`
- `payout.paid` / `payout.failed`

## Quick Start

```python
import stripe

stripe.api_key = "<your_secret_key>"

# Create a checkout session
session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': 'Premium Subscription',
            },
            'unit_amount': 2000,  # $20.00
            'recurring': {
                'interval': 'month',
            },
        },
        'quantity': 1,
    }],
    mode='subscription',
    success_url='<success_url>',
    cancel_url='<cancel_url>',
)

# Redirect user to session.url
print(session.url)
```

## Payment Implementation Patterns

### Pattern 1: One-Time Payment (Hosted Checkout)
```python
def create_checkout_session(amount, currency='usd'):
    """Create a one-time payment checkout session."""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Purchase',
                        'images': ['<product_image_url>'],
                    },
                    'unit_amount': amount,  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='<success_url>',
            cancel_url='<cancel_url>',
            metadata={
                'order_id': '<order_id>',
                'user_id': '<user_id>'
            }
        )
        return session
    except stripe.error.StripeError as e:
        # Handle error
        print(f"Stripe error: {e.user_message}")
        raise
```

### Pattern 2: Custom Payment Intent Flow
```python
def create_payment_intent(amount, currency='usd', customer_id=None):
    """Create a payment intent for custom checkout UI."""
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        customer=customer_id,
        automatic_payment_methods={
            'enabled': True,
        },
        metadata={
            'integration_check': 'accept_a_payment'
        }
    )
    return intent.client_secret  # Send to frontend
```

### Pattern 3: Subscription Creation
```python
def create_subscription(customer_id, price_id):
    """Create a subscription for a customer."""
    try:
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}],
            payment_behavior='default_incomplete',
            payment_settings={'save_default_payment_method': 'on_subscription'},
            expand=['latest_invoice.payment_intent'],
        )

        return {
            'subscription_id': subscription.id,
            'client_secret': subscription.latest_invoice.payment_intent.client_secret
        }
    except stripe.error.StripeError as e:
        print(f"Subscription creation failed: {e}")
        raise
```

### Pattern 4: Customer Portal
```python
def create_customer_portal_session(customer_id):
    """Create a portal session for customers to manage subscriptions."""
    session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url='<return_url>',
    )
    return session.url  # Redirect customer here
```

## Webhook Handling

### Secure Webhook Endpoint
```python
from flask import Flask, request
import stripe

app = Flask(__name__)

endpoint_secret = '<your_webhook_secret>'

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError:
        # Invalid payload
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return 'Invalid signature', 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_failed_payment(payment_intent)
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_canceled(subscription)

    return 'Success', 200
```

### Webhook Best Practices
```python
import hashlib
import hmac

def verify_webhook_signature(payload, signature, secret):
    """Manually verify webhook signature."""
    expected_sig = hmac.new(
        secret.encode('utf-8'),
        payload,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_sig)

def handle_webhook_idempotently(event_id, handler):
    """Ensure webhook is processed exactly once."""
    # Check if event already processed
    if is_event_processed(event_id):
        return

    # Process event
    try:
        handler()
        mark_event_processed(event_id)
    except Exception as e:
        log_error(e)
        # Stripe will retry failed webhooks
        raise
```

## Pre-Implementation Checklist

### Webhook Setup
- [ ] Platform endpoint handles platform events
- [ ] Connect endpoint handles `checkout.session.completed` (if using Direct Charge)
- [ ] Stripe Dashboard has Connect webhook with correct events
- [ ] Webhook secrets configured for BOTH endpoints (different secrets!)

### Payment Verification
- [ ] Webhook handler implemented (primary - async, reliable)
- [ ] Frontend verify endpoint implemented (secondary - immediate UX)
- [ ] Both use conditional UPDATE for idempotency
- [ ] 100% promo detected by `amount_total === 0` (NOT `no_payment_required`)
- [ ] **Web vs Native browser handling**: Check `result.type === 'opened'` (web) vs `'dismiss'/'cancel'` (native) - do NOT verify immediately on web!

### Inventory/Booking
- [ ] Inventory only modified AFTER payment confirmed
- [ ] Atomic operations prevent double-counting
- [ ] Proper error handling if slot becomes unavailable (refund flow)

### Testing
- [ ] Test with regular payment
- [ ] Test with 100% promo code
- [ ] Test browser close during payment
- [ ] Test network failure during verify
- [ ] Verify webhook receives events from Connect accounts (if applicable)

## Best Practices

1. **Always Use Webhooks**: Don't rely solely on client-side confirmation
2. **Idempotency**: Handle webhook events idempotently
3. **Error Handling**: Gracefully handle all Stripe errors
4. **Test Mode**: Thoroughly test with test keys before production
5. **Metadata**: Use metadata to link Stripe objects to your database
6. **Monitoring**: Track payment success rates and errors
7. **PCI Compliance**: Never handle raw card data on your server
8. **SCA Ready**: Implement 3D Secure for European payments

## Common Pitfalls

- **Not Verifying Webhooks**: Always verify webhook signatures
- **Missing Webhook Events**: Handle all relevant webhook events
- **Hardcoded Amounts**: Use cents/smallest currency unit
- **No Retry Logic**: Implement retries for API calls
- **Ignoring Test Mode**: Test all edge cases with test cards