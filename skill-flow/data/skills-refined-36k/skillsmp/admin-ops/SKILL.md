---
name: admin-ops
description: Orchestrates the management of the admin dashboard, ensuring live data integrity and Noir design compliance for THE LOST+UNFOUNDS.
---

# Admin Operations Skill

This skill governs the maintenance, data integrity, and visual excellence of the Admin Dashboard (`/admin`).

## Core Responsibilities

### 1. Data Integrity & Live Feeds
- **No Placeholders**: ALWAYS replace hardcoded placeholders with live data from Supabase.
- **Data Freshness**: Ensure the auto-refresh mechanism (default 30s) is working and covers all critical stats.
- **Robustness**: Maintain fallback states for cases where database tables might not exist or are empty.
- **Accuracy**: Use the most accurate source of truth for stats (e.g., combining `platform_subscriptions`, `user_roles`, and `user_subdomains` for user counts).

### 2. UI & Noir Aesthetic
- **Monochrome**: Pure black background (`#000000`) and pure white text/borders.
- **Rigid Geometry**: STRICTLY enforce `border-radius: 0 !important`. No rounded corners on buttons, cards, or inputs.
- **Typography**: Headers (h1, h2, Bento titles) MUST be **UPPERCASE**.
- **Alignment**: Standardize on `text-left` for body content and lists.
- **Bento Grid**: Maintain the Bento-style layout for the overview, ensuring responsiveness and proper alignment.

### 3. Management Modules
- **User Management**: Ensure the user details side panel provides actionable data (tier, status, subdomain).
- **Blog Oversight**: Monitor pending submissions and active post counts.
- **Commerce Tracking**: Track product inventory, costs, and subscription revenue (MRR).
- **Outreach Monitoring**: Integration with Zoho Mail status and newsletter subscriber growth.

## Dashboard Components

### Bento Grid Layout
The dashboard uses a 4-column Bento grid:
- **Platform Overview**: 3x2 (Large chart + key stats)
- **System Alerts**: 1x2 (Scrollable alert list)
- **Small Cards**: 1x1 (Users, Subscriptions, Products, Blog, Newsletter, Mail, System)

### Standard Styles
- Cards: `.noir-card` or custom Bento card with white border.
- Buttons: White background with black text for primary actions; transparent with white border for secondary.
- Stats: Use `AnimatedNumber` for all numeric values.

## Verification Checklist
- [ ] No "coming soon" or static "--%" placeholders.
- [ ] No `rounded` or `rounded-*` classes (except for profile avatars if absolutely necessary).
- [ ] All headers are uppercase.
- [ ] All data is fetched from Supabase.
- [ ] Desktop and mobile layouts are aligned correctly.
