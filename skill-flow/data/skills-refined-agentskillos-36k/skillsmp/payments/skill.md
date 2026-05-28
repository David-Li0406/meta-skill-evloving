---
name: payments
description: Handle Stripe quotes and invoices for customer billing
---

# Payments Skill

Manage formal quotes and invoices via Stripe integration.

## Available Tools

- `create_quote` - Create formal quote sent to customer email
- `create_invoice` - Create and send invoice after service completion
- `get_quote_status` - Check quote status (draft, sent, accepted, declined)

## Quote vs Invoice Flow

```
Customer inquiry → Estimate (informal) → Quote (formal) → Service → Invoice
```

1. **Estimate**: Informal price shown in chat (`create_estimate` from customer skill)
2. **Quote**: Formal proposal emailed via Stripe
3. **Invoice**: Bill sent after work is completed

## Creating Quotes

Use `create_quote` when customer wants to proceed after seeing estimate.

Required information:
- `customerId` - Database customer ID (create customer first if needed)
- `items` - List of services with:
  - `service` - Service name
  - `description` - Description of work
  - `amount` - Price in dollars
- `expiresInDays` - Quote validity (default: 7 days)

The quote is emailed to the customer with a link to view and accept online.

## Creating Invoices

Use `create_invoice` after service is completed.

Required information:
- `customerId` - Database customer ID
- `items` - List of completed services with final prices
- `bookingId` - (optional) Link to the appointment
- `dueInDays` - Payment deadline (default: 7 days)

The invoice is emailed with a payment link.

## Checking Quote Status

Use `get_quote_status` to check if a customer has:
- Viewed the quote
- Accepted it
- Let it expire
- Declined it

## Best Practices

1. **Itemize clearly** - Break down each service separately
2. **Match estimate** - Invoice should match quoted prices unless scope changed
3. **Explain changes** - If final price differs from quote, explain why
4. **Confirm before sending** - Verify customer email and details before sending
