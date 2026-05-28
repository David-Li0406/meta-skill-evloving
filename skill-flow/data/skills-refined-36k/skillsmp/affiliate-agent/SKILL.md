---
name: affiliate_agent
description: Searches for and formats affiliate referral links for supplements.
---

# Goal
Automate the monetization of supplement recommendations by generating standard, ID-tagged affiliate links.

# Instructions
1. Identify the supplement brand and platform (Amazon/iHerb).
2. Run `python scripts/link_gen.py [brand_name] [product_id] [platform]` to generate the clean affiliate link.
3. Use this link in the `SupplementModel` `purchaseUrl` field.

# Supported Platforms
- **Amazon**: Appends `tag=adhdsupps-20`
- **iHerb**: Appends `rcode=ADHDSUPPS`
