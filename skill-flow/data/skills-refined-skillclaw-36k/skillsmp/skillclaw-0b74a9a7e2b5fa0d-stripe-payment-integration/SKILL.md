---
name: stripe-payment-integration
description: Use this skill when implementing Stripe payment processing for secure, PCI-compliant payment flows, including checkout, subscriptions, webhooks, and marketplace patterns.
---

# Stripe Payment Integration

Master Stripe payment processing integration for robust, PCI-compliant payment flows including checkout, subscriptions, webhooks, and refunds.

## When to Use This Skill

- Implementing payment processing in web/mobile applications
- Setting up subscription billing systems
- Handling one-time payments and recurring charges
- Processing refunds and disputes
- Managing customer payment methods
- Implementing SCA (Strong Customer Authentication) for European payments
- Building marketplace payment flows with Stripe Connect
- Implementing dual confirmation (webhook + frontend verification)
- Handling promo codes and 100% discount scenarios
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

## Quick Start

```python
import stripe

stripe.api_key = "sk_test_..."

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
    success_url='https://example.com/success',
    cancel_url='https://example.com/cancel',
)
```