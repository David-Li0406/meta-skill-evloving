---
name: payment-integration
description: Use this skill when implementing payment processing solutions with SePay and Polar, including checkout flows, subscription management, and automated benefit delivery.
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
- **Overview & Auth**: Overview of platform capabilities, API/OAuth2 authentication, and supported banks.
- **API Reference**: Endpoints for transactions, bank accounts, and virtual accounts.
- **Webhooks**: Setup, payload structure, verification, and retry logic.
- **SDK Usage**: Implementations in Node.js, PHP, Laravel.
- **QR Codes**: VietQR generation and integration templates.
- **Best Practices**: Security, patterns, and monitoring.

### Polar Integration
- **Overview & Auth**: Platform capabilities, authentication methods, and the Merchant of Record concept.
- **Products & Pricing**: Information on product offerings and pricing structures.