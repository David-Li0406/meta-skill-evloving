# Deprecated Files - 2026-01-12

These files have been deprecated and should NOT be used.

## admin-sidebar.php.deprecated
- Replaced by: /components/sidebar.php
- Reason: Duplicated navigation logic, now using single source of truth

## admin-layout.php.deprecated
- Replaced by: /admin/components/unified-layout.php
- Reason: No pages were using this layout, all migrated to unified-layout.php

## Primary Navigation Files (DO NOT CREATE NEW ONES)

- Navigation definition: /includes/config/admin-tabs-config.php
- Navigation rendering: /components/sidebar.php
- Mobile navigation: /admin/components/admin-mobile-nav.php (keep in sync with config)

If you need to add new menu items, edit admin-tabs-config.php ONLY.
