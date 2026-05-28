# Deprecated Files - 2026-01-12

These files have been deprecated and should NOT be used.

## navigation.php.deprecated
- Replaced by: /components/sidebar.php
- Reason: Duplicated navigation logic with inline CSS and SVG icons
- The inline CSS should be in /assets/css/layout.css
- Icons should use hub_icon() from /components/icons.php

## Primary Navigation Files (DO NOT CREATE NEW ONES)

- Navigation definition: /includes/config/admin-tabs-config.php
- Navigation rendering: /components/sidebar.php

If you need to add new menu items, edit admin-tabs-config.php ONLY.
