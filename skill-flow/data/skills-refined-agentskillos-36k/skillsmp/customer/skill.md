---
name: customer
description: Customer management, service catalog, and informal estimates
---

# Customer Skill

Manage customer records and provide service information for HMLS Mobile Mechanic.

## Available Tools

- `get_customer` - Look up existing customer by phone or email
- `create_customer` - Create new customer record
- `get_services` - Get service catalog with pricing
- `create_estimate` - Generate informal price estimate

## Customer Lookup

Always check for existing customer before creating a new one:
1. Ask for phone number or email
2. Use `get_customer` to search
3. If not found, use `create_customer` with their details

## Service Information

Use `get_services` to retrieve the current service catalog with:
- Service name and description
- Price range (min/max)
- Estimated duration
- Category (maintenance, repair, diagnostic)

## Creating Estimates

When a customer asks "how much for X?":

1. **Ask about the vehicle first** - Make, model, year affect pricing
2. **Use `create_estimate`** to generate an informal quote
3. **Adjust pricing** based on:
   - Vehicle type (luxury/European cars cost more)
   - Vehicle age/condition
   - Issue complexity
   - Parts cost

### Pricing Adjustments

- **Luxury/European vehicles** (BMW, Mercedes, Audi): +15-30% from base
- **Older vehicles** (10+ years): May need additional work
- **Complex issues**: Higher end of range or above

### Example

Customer: "How much for brakes on my 2019 BMW X5?"

1. Base brake service: $150-300
2. BMW adjustment: +20-30%
3. Estimate: $280-350

Always explain your reasoning when price differs from base range.

## Estimate vs Quote

- **Estimate** (`create_estimate`): Informal, shown in chat, quick reference
- **Quote** (`create_quote`): Formal, emailed via Stripe, customer can accept online

Only proceed to formal quote when customer confirms they want to move forward.
