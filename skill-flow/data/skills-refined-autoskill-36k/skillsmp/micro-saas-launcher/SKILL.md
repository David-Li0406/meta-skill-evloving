---
name: micro-saas-launcher
description: Guidelines for Micro-SaaS architecture, Stripe integration, and launch checklists.
---

# Micro-SaaS & Stripe Launcher

## When to use this skill
- Building a new SaaS product or adding subscription features.
- Integrating Stripe Checkout or Webhooks.
- Planning a product launch.

## 1. Stripe Integration
- **Checkout**: Use Stripe Checkout (hosted page) for simplest PCI compliance.
- **Webhooks**: Always verify webhook signatures. Handle `checkout.session.completed` for provisioning access and `customer.subscription.deleted` for revocation.
- **Idempotency**: Ensure webhook handlers are idempotent (handle the same event twice without side effects).

## 2. Architecture (SaaS)
- **Tenancy**: Decide early: Single DB with `tenant_id` column (easiest) vs Database-per-tenant (complex).
- **Onboarding**: Create a friction-free onboarding flow. Minimizing steps to "Aha!" moment is critical.

## 3. Launch Checklist
- **Legal**: Terms of Service & Privacy Policy pages exist.
- **Email**: Transactional emails (Postmark/Resend) configured (SPF/DKIM/DMARC).
- **Analytics**: Basic tracking (PostHog/Plausible) to measure conversion.
