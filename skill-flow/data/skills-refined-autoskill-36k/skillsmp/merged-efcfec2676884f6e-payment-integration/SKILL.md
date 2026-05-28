---
name: payment-integration
description: Use this skill when integrating payment processing with SePay (Vietnamese payment gateway) and Polar (global SaaS monetization platform) for managing subscriptions, handling webhooks, and automating benefit delivery.
---

# Payment Integration

Implement payment processing with SePay (Vietnamese payments) and Polar (global SaaS monetization).

## When to Use

Use when implementing:
- Payment gateway integration (checkout, processing)
- Subscription management (trials, upgrades, billing)
- Webhook handling (payment notifications)
- QR code payments (VietQR, NAPAS)
- Usage-based billing (metering, credits)
- Automated benefit delivery (licenses, GitHub access, Discord roles)
- Customer portals (self-service management)
- Bank transfer automation (Vietnamese banks)
- Product catalogs with pricing

## Platform Selection

**Choose SePay for:**
- Vietnamese market (VND currency)
- Bank transfer automation
- VietQR/NAPAS payments
- Local payment methods
- Direct bank account monitoring

**Choose Polar for:**
- Global SaaS products
- Subscription management
- Usage-based billing
- Automated benefits (GitHub, Discord, licenses)
- Merchant of Record (tax compliance)
- Digital product sales

## Quick Reference

### SePay Integration
- **Overview & Auth**: Overview of platform capabilities, API/OAuth2 auth, supported banks
- **API Reference**: Endpoints, transactions, bank accounts, virtual accounts
- **Webhooks**: Setup, payload structure, verification, retry logic
- **SDK Usage**: Implementations for Node.js, PHP, Laravel
- **QR Codes**: VietQR generation, templates, integration
- **Best Practices**: Security, patterns, monitoring

### Polar Integration
- **Overview & Auth**: Platform capabilities, authentication methods, MoR concept
- **Products & Pricing**: Product types, pricing models, usage-based billing
- **Checkouts**: Checkout flows, embedded checkout, links
- **Subscriptions**: Lifecycle, upgrades, downgrades, trials
- **Webhooks**: Event types, signature verification, monitoring
- **Benefits**: Automated delivery (GitHub, Discord, licenses, files)
- **SDK Usage**: TypeScript, Python, PHP, Go, framework adapters
- **Best Practices**: Security, patterns, monitoring

### Integration Scripts
- **SePay Webhook Verification**: Verify SePay webhook authenticity
- **Polar Webhook Verification**: Verify Polar webhook signatures
- **Checkout Helper**: Generate checkout sessions for both platforms

## Implementation Workflow

### SePay Implementation
1. Load overview for auth setup
2. Load API or SDK for integration
3. Load webhooks for payment notifications
4. Use webhook verification script
5. Load best practices for production readiness

### Polar Implementation
1. Load overview for auth and concepts
2. Load products for product setup
3. Load checkouts for payment flows
4. Load webhooks for event handling
5. Use webhook verification script
6. Load benefits if automating delivery
7. Load best practices for production readiness

## Key Capabilities

**SePay:**
- Payment gateway (QR, bank transfer, cards)
- Bank account monitoring with webhooks
- Order-based virtual accounts
- VietQR generation API
- 44+ Vietnamese banks supported
- Rate limit: 2 calls/second

**Polar:**
- Merchant of Record (global tax compliance)
- Subscription lifecycle management
- Usage-based billing (events, meters)
- Automated benefits (GitHub, Discord, licenses)
- Customer portal (self-service)
- Multi-language SDKs
- Rate limit: 300 req/min

## Instructions

When implementing payment integration:

1. **Identify platform** based on requirements (Vietnamese vs global, payment types)
2. **Load relevant references** progressively as needed
3. **Implement authentication** using platform-specific methods
4. **Set up products/pricing** according to business model
5. **Implement checkout flow** (hosted, embedded, or API-driven)
6. **Configure webhooks** with proper verification
7. **Handle payment events** (success, failure, refund)
8. **Test thoroughly** in sandbox before production
9. **Monitor and optimize** using platform analytics

Load only the references needed for current implementation step to maintain context efficiency.