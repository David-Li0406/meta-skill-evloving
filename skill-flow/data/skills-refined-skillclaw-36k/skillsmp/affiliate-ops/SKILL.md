---
name: affiliate-ops
description: Manages the affiliate program, link tracking, and commission logic. Use when working on AdminAffiliates.tsx, AffiliateDashboard.tsx, or Amazon link formatting.
---

# Affiliate Ops Skill

This skill governs the growth and referral engine of THE LOST+UNFOUNDS.

## Amazon Affiliate Logic (Critical)
- **Formatting**: Book titles must be **bold**. Amazon links are **underlined**.
- **Constraints**: Max 2 links per book per article.
- **Disclosure**: Author names in disclosure must be **UPPERCASE BOLD**.
- **Fuzzy Matching**: Use `normalizeBookTitle` logic to match titles across content and database.

## Program Management
- **Tracking**: Ensure all external links include the correctly mapped affiliate tag or slug.
- **Commission Flow**: 
  - Verify purchase → capture → commission update.
  - Test the "Customer Lifetime Tie" (attaching customers to the referring affiliate for life).
- **MLM Bonuses**: Handle tiered bonus calculations for multi-level referrals.

## UI Standards
- **Mechanical Dashboards**: Use high-contrast headers, sharp borders, and tabular data.
- **Withdrawals**: The "Request Payout" flow must be stark and require explicit admin approval via the `AdminAffiliates` dashboard.
