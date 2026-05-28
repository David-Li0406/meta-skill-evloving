# 5. Affiliate Link Strategy

Date: 2026-01-18

## Status

Accepted

## Context

The app generates revenue through affiliate referrals (Amazon/iHerb). Users are located globally, and sending a UK user to the US Amazon store results in poor UX and lost revenue.

## Decision

We will implement a **Region-Aware Affiliate Service**.

### Logic
- **Detection**: Detect user region (US/UK/EU) based on device locale (or user selection).
- **Tagging**: Store separate affiliate tags for each region (`adhdsupplements-20`, `adhdsupplements-21`, etc.).
- **Routing**: `AffiliateService` dynamically constructs the URL based on the user's region and the product's ASIN.

### Skill Automation
- An AI skill (`Affiliate Link Finder`) is established to automate the discovery of highest-rated products and generation of multi-region links when adding new supplements to the database.

## Consequences

### Positive
- **Revenue Optimization**: Maximizes conversion by sending users to their local store.
- **User Experience**: Users see correct pricing and shipping information.
- **Automation**: The AI skill reduces manual data entry effort for new products.

### Negative
- **Data Maintenance**: Requires maintaining valid ASINs that exist in all target marketplaces (or handling fallback logic).
