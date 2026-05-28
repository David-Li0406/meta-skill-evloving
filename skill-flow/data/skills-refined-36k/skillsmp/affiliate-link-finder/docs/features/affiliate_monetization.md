# Affiliate & Monetization System

This document describes the affiliate link logic for supplement purchases.

## Overview
The app generates revenue through Amazon Associates affiliate links when users purchase recommended supplements.

## Components

### 1. `AffiliateService` (Domain Service)
**Location**: `lib/domain/services/affiliate_service.dart`

Responsible for generating region-aware affiliate links.

**Key Concepts:**
- `UserRegion` enum: `us`, `uk`, `eu`.
- Each region has a specific Amazon store URL and affiliate tag.

**Key Methods:**
- `getTaggedAffiliateLink({supplementId, region, customProductPath})`: Returns a full URL.
- `getAllRegionLinks(supplementId)`: Returns a map of all regional links.
- `detectRegionFromLocale(String localeCode)`: Infers region from device locale.

**Affiliate Tags:**
| Region | Tag | Store URL |
|--------|-----|-----------|
| US | `adhdsupplements-20` | amazon.com |
| UK | `adhdsupplements-21` | amazon.co.uk |
| EU | `adhdsupplements-22` | amazon.de |

### 2. `UrlService` (Infrastructure Service)
**Location**: `lib/infrastructure/services/url_service.dart`

A thin wrapper around `url_launcher` to open external links.

**Usage:**
```dart
final affiliateUrl = AffiliateService().getTaggedAffiliateLink(
  supplementId: 'B0000XYZ123', // Amazon ASIN
  region: UserRegion.us,
);
await UrlService().launchUrl(affiliateUrl);
```

## Future Enhancements (See Task.md Phase 14)
- [ ] **Deep Linking**: Universal Links for a smoother UX.
- [ ] **Safety Intercept**: Show a warning modal before redirecting if there's a known interaction.
- [ ] **Compliance UI**: Add "Affiliate Disclosure" text near buy buttons.
