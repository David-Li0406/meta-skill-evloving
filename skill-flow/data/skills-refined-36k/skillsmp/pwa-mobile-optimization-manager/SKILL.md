---
name: pwa-mobile-optimization-manager
description: Skill for managing mobile-specific capabilities like PWA assets and viewport optimization.
---

# PWA & Mobile Optimization Manager

This skill helps ensure the "app-like" feel of the web application and optimizes it for mobile operating systems.

## Critical Meta Tags

### 1. Viewport Meta
Ensure users can zoom but the layout remains stable.
```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes" />
```

### 2. iOS Specifics
```html
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="FlyerBoard">
```

## PWA Health Check

### `manifest.json` Requirements:
- `short_name` and `name` are set.
- `start_url` points to `/`.
- `display` is `standalone` or `minimal-ui`.
- `icons` include at least 192x192 and 512x512 versions.
- `theme_color` and `background_color` are defined.

## Scripts

### `check-pwa-health.sh`
A basic verification script for manifest and meta tags.

**Command**:
```bash
./.agent/skills/pwa-mobile-optimization-manager/scripts/check-pwa-health.sh
```

## Resources
- [web.dev: PWA Checklist](https://web.dev/pwa-checklist/)
- [Apple: Web App Manifest](https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/ConfiguringWebApplications/ConfiguringWebApplications.html)
