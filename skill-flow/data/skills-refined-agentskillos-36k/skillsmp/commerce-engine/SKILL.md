---
name: commerce-engine
description: Governs the shop, product catalog, and transaction logic. Use when working on Shop.tsx, PaymentSuccess.tsx, or PayPal integrations.
---

# Commerce Engine Skill

This skill manages the commercial "Noir" marketplace and financial transactions.

## Shop & Product Hygiene
- **Product Definition**: Every product in the shop must have a "Noir" aesthetic image, clear description, and pricing tied to the `products` table in Supabase.
- **Shadow Board**: Use the "Shadow Board" pipeline logic from `CRM_PRD_NOIR.md` to move leads/orders through `DISCOVERY` → `WON`.

## Transaction Flow (PayPal)
- **Security**: Always capture payments before granting access or calculating commissions.
- **Redirection**: Handle `/payment-success` and `/payment-cancel` with stark, mechanical UI feedback.
- **Taxes**: Ensure tax calculations follow the country-specific rules defined in the checkout logic.

## UI/UX Rules
- **Direct Action**: Minimize friction. One-click transitions between pipeline stages.
- **Card Styling**: Every product card is a simple white outline box (`border: 1px solid white`). Inactive states are `opacity: 0.6`. Hover state border glows pure white.
- **Forms**: Use simple white bottom-border only for inputs. Labels are small and uppercase.
