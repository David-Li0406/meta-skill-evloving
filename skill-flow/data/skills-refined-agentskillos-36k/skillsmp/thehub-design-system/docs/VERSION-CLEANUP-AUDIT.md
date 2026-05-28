# Version Reference Cleanup Audit for TheHUB

**Audit Date:** 2025-12-18
**Cleanup Completed:** 2025-12-22
**Status:** ✅ COMPLETED

**Purpose:** Identify all version number references requiring cleanup before 1.0 launch

---

## CLEANUP SUMMARY

The following cleanup actions were completed:

### Phase 1: Deleted backup files and obsolete docs
- Deleted `assets/css/theme-base.css.backup-v2`
- Deleted `assets/css/tokens.css.backup-v2`
- Deleted `assets/css/responsive.css.backup-v2`
- Deleted `includes/navigation.php.backup-v1`
- Deleted `docs/V2-vs-V3-analysis.md`
- Deleted `assets/thehub-v3-pwa-prompt.md`

### Phase 2: Updated service worker cache names
- Updated `sw.js`: `thehub-v3-cache-v2` → `thehub-cache-v1`
- Updated `offline.html`: `thehub-v3-cache-v1` → `thehub-cache-v1`

### Phase 3: Renamed CSS classes (rider-v3.css)
- Renamed `assets/css/pages/rider-v3.css` → `rider.css`
- Removed `-v3` suffix from 42 CSS classes
- Updated all corresponding HTML classes in `pages/rider.php`

### Phase 4: Renamed v3-config.php and constants
- Renamed `v3-config.php` → `hub-config.php`
- Added new constants: `HUB_ROOT`, `HUB_URL` (version 1.0.0)
- Added backward compatibility aliases for `HUB_V3_ROOT`, `HUB_V3_URL`
- Updated all 12 files referencing the config file

### Phase 5: Renamed navigation-v3.php
- Renamed `includes/navigation-v3.php` → `navigation.php`
- Updated reference in `includes/layout-header.php`

---

## 1. SUMMARY

| Category | Count | Risk Level |
|----------|-------|------------|
| Versioned filenames | 8 files | HIGH |
| CSS classes with version suffixes | 42+ classes | HIGH |
| PHP/JS variables with version names | 12 variables | HIGH |
| Version comments in code | 25+ comments | LOW |
| Service worker cache names | 2 references | MEDIUM |
| HUB_V3/HUB_V2 constants | 50+ usages | HIGH |
| Backup files with version suffix | 4 files | LOW |
| Documentation files | 2 files | LOW |

**Total estimated references: 145+**

---

## 2. VERSIONED FILENAMES

### Files requiring rename/removal:

| Current Name | Recommendation | Risk |
|--------------|----------------|------|
| `v3-config.php` | Rename to `hub-config.php` or merge into `config.php` | HIGH - Core file, many dependencies |
| `includes/navigation-v3.php` | Rename to `navigation.php` | MEDIUM - Used by layout-header.php |
| `assets/css/pages/rider-v3.css` | Rename to `rider.css` | MEDIUM - Used by rider.php |
| `admin/migrations/add_series_format_v2.php` | Keep (database migration) | EXCLUDE |
| `docs/V2-vs-V3-analysis.md` | Archive or delete | LOW |
| `assets/thehub-v3-pwa-prompt.md` | Delete (obsolete documentation) | LOW |

### Backup files (can be deleted):

| File | Recommendation |
|------|----------------|
| `assets/css/theme-base.css.backup-v2` | Delete |
| `assets/css/tokens.css.backup-v2` | Delete |
| `assets/css/responsive.css.backup-v2` | Delete |
| `includes/navigation.php.backup-v1` | Delete |

---

## 3. CSS CLASSES WITH VERSION SUFFIXES

**File: `assets/css/pages/rider-v3.css` (42 classes)**

| Class Name | Line | Suggested New Name |
|------------|------|-------------------|
| `.profile-card-v3` | 30 | `.profile-card` |
| `.form-card-v3` | 271, 757 | `.form-card` |
| `.form-result-row-v3` | 341, 351 | `.form-result-row` |
| `.form-avg-v3` | 378 | `.form-avg` |
| `.series-card-v3` | 405 | `.series-card` |
| `.series-tabs-v3` | 411 | `.series-tabs` |
| `.series-panel-v3` | 453, 458 | `.series-panel` |
| `.ranking-card-v3` | 666 | `.ranking-card` |
| `.ranking-progress-bar-v3` | 728 | `.ranking-progress-bar` |
| `.highlights-card-v3` | 860 | `.highlights-card` |
| `.highlights-list-v3` | 869 | `.highlights-list` |
| `.highlight-item-v3` | 875, 889, 893 | `.highlight-item` |
| `.achievements-card-v3` | 901, 910, 916, 922, 927, 931 | `.achievements-card` |
| `.form-points-card-v3` | 1234 | `.form-points-card` |

**File: `pages/rider.php` (corresponding HTML classes)**

All usages in rider.php must be updated when CSS classes are renamed.

---

## 4. PHP/JS VARIABLES WITH VERSION NAMES

### PHP Variables:

| Location | Variable | Line | Recommendation |
|----------|----------|------|----------------|
| `index.php` | `$v3ConfigPath` | 16-18 | Rename to `$hubConfigPath` |
| `router.php` | `$v3ConfigPath` | 10-12 | Rename to `$hubConfigPath` |
| `components/sidebar.php` | `$v3Config` | 10-12 | Rename to `$hubConfig` |
| `components/mobile-nav.php` | `$v3Config` | 9-11 | Rename to `$hubConfig` |

### Constants (v3-config.php):

| Constant | Line | Recommendation |
|----------|------|----------------|
| `HUB_VERSION` (3.6.0) | 31 | Change to `1.0.0` |
| `CSS_VERSION` (3.6.0) | 32 | Change to `1.0.0` |
| `JS_VERSION` (3.6.0) | 33 | Change to `1.0.0` |
| `HUB_V3_ROOT` | 35 | Rename to `HUB_ROOT` |
| `HUB_V3_URL` | 36 | Rename to `HUB_URL` |
| `HUB_V2_ROOT` | 37 | Remove if V2 no longer exists |

---

## 5. VERSION COMMENTS IN CODE

### Comments referencing V2/V3 (LOW priority - cosmetic):

| File | Line | Comment |
|------|------|---------|
| `components/sidebar.php` | 8 | `// Ensure v3-config is loaded` |
| `components/mobile-nav.php` | 7 | `// Ensure v3-config is loaded (may already be loaded by parent)` |
| `router.php` | 9 | `// Ensure v3-config is loaded` |
| `router.php` | 22 | `// Ensure HUB_V3_ROOT is defined` |
| `router.php` | 83 | `// New V1.0 section-based routing` |
| `router.php` | 120 | `// Check if this is a V1.0 section route` |
| `api/search.php` | 27 | `// Use global $pdo from config.php (hub_db() is only in v3-config.php)` |
| `pages/ranking.php` | 9 | `// Include ranking functions - try multiple paths for V3 routing compatibility` |
| `pages/series/show.php` | 117 | `// Build standings with per-event points (like V2)` |
| `admin/point-scales.php` | 238 | `// Page config for V3 admin layout` |
| `pages/calendar/event.php` | 52 | `// Fetch event details (same as V2)` |
| `pages/series-single.php` | 50 | `// Get all events in this series (using series_events junction table like V2)` |
| `v3-config.php` | 29 | `// V3.6 VERSION INFO` |
| `v3-config.php` | 60 | `// V1.0 NAVIGATION (6 main sections)` |
| `v3-config.php` | 181-251 | Multiple V2/V3 session compatibility comments |
| `v3-config.php` | 526-588 | Multiple V2/V3 session comments |
| `admin/point-templates.php` | 140 | `// Page config for V3 admin layout` |
| `pages/riders.php` | 31 | `// Fetch riders with stats - matching v2 structure` |

---

## 6. SERVICE WORKER CACHE NAMES

| File | Line | Current Value | Recommendation |
|------|------|---------------|----------------|
| `sw.js` | 6 | `thehub-v3-cache-v2` | Change to `thehub-cache-v1` |
| `offline.html` | 114 | `thehub-v3-cache-v1` | Change to `thehub-cache-v1` |
| `organizer/sw.js` | 6 | `organizer-v1` | OK - no version prefix in app name |

**Note:** Cache names will need version bumping on updates, but should not include "v3" prefix.

---

## 7. HUB_V3/HUB_V2 CONSTANT USAGES (50+ occurrences)

### Files using HUB_V3_ROOT (rename to HUB_ROOT):

- `router.php` (10 usages)
- `v3-config.php` (5 usages)
- `index.php` (3 usages)
- `pages/login.php` (2 usages)
- `pages/welcome.php` (2 usages)
- `pages/dashboard.php` (1 usage)
- `pages/club.php` (4 usages)
- `pages/event.php` (3 usages)
- `pages/logout.php` (2 usages)
- `pages/riders.php` (1 usage)
- `pages/series-single.php` (4 usages)
- `pages/activate-account.php` (1 usage)
- `pages/forgot-password.php` (1 usage)
- `pages/database/index.php` (1 usage)
- `pages/series/index.php` (1 usage)
- `pages/series/show.php` (3 usages)
- `pages/calendar/event.php` (2 usages)
- `pages/profile/children.php` (1 usage)
- `components/sidebar.php` (2 usages)
- `components/mobile-nav.php` (1 usage)
- `components/header.php` (2 usages)
- `components/head.php` (1 usage)
- `admin/components/*.php` (8 usages)
- `test-minimal.php` (2 usages)

### Files using HUB_V3_URL (rename to HUB_URL):

- `v3-config.php` (6 usages)
- `components/header.php` (1 usage)
- `components/head.php` (1 usage)
- `pages/login.php` (1 usage)

### Files using HUB_V2_ROOT (remove if V2 is deprecated):

- `v3-config.php` (1 definition)
- `api/registration.php` (1 usage - references V2 registration validator)

---

## 8. RISK ASSESSMENT

### HIGH RISK (Require careful refactoring):

1. **`v3-config.php` rename** - 40+ files depend on this file
2. **`HUB_V3_ROOT` constant rename** - 50+ usages across the codebase
3. **CSS class renames in rider-v3.css** - Must update both CSS and PHP simultaneously

### MEDIUM RISK:

1. **Service worker cache names** - Users may need to clear cache
2. **`navigation-v3.php` rename** - Used by layout-header.php

### LOW RISK (Safe to change):

1. **Backup files deletion** - No longer referenced
2. **Documentation updates** - No functional impact
3. **Comment cleanups** - Cosmetic only

---

## 9. RECOMMENDED CLEANUP ORDER

### Phase 1: Safe Deletions (No risk)
1. Delete backup files (`*.backup-v1`, `*.backup-v2`)
2. Archive/delete `docs/V2-vs-V3-analysis.md`
3. Delete `assets/thehub-v3-pwa-prompt.md`

### Phase 2: Comment Cleanup (Low risk)
1. Update version comments to remove V2/V3 references
2. Update inline comments mentioning version numbers

### Phase 3: Service Worker Update (Medium risk)
1. Update cache names in `sw.js` and `offline.html`
2. Bump cache version to force refresh

### Phase 4: CSS Class Renaming (High risk)
1. Create new CSS file without version suffixes
2. Update `pages/rider.php` to use new class names
3. Test rider page thoroughly
4. Remove old `rider-v3.css`

### Phase 5: Config File Refactoring (Highest risk)
1. Create `hub-config.php` with renamed constants
2. Update all 40+ files referencing `v3-config.php`
3. Update all 50+ usages of `HUB_V3_ROOT` to `HUB_ROOT`
4. Update all usages of `HUB_V3_URL` to `HUB_URL`
5. Remove V2 backward compatibility code if no longer needed
6. Test entire application

### Phase 6: Final Cleanup
1. Rename `navigation-v3.php` to `navigation.php`
2. Update version numbers in `config.php` to 1.0
3. Remove `HUB_V2_ROOT` constant and V2 compatibility code

---

## 10. FILES EXCLUDED FROM CLEANUP

| File | Reason |
|------|--------|
| `admin/migrations/add_series_format_v2.php` | Database migration - version indicates schema version |
| `database/migrations/*.sql` | Database schema versions |
| External libraries | Third-party version numbers |
| `config.php` APP_VERSION | Intentional versioning system |

---

## 11. SEARCH COMMANDS USED

```bash
# Versioned filenames
glob **/*v2* **/*v3* **/*v4* **/*-v* **/*_v*

# CSS classes with version suffixes
grep -r "\-v[234]" --include="*.css" --include="*.php"

# PHP variables with version names
grep -r "\$v[234]" --include="*.php"

# Version comments
grep -r "//.*v[234]\|#.*v[234]\|/\*.*v[234]" --include="*.php" --include="*.css" --include="*.js"

# Constants
grep -r "HUB_V[234]" --include="*.php"
```

---

## 12. CONCLUSION

The codebase has significant version number references that should be cleaned up for a professional 1.0 release. The most critical changes involve:

1. **Renaming `v3-config.php`** - This is the central configuration file with 40+ dependencies
2. **Renaming `HUB_V3_*` constants** - 50+ usages throughout the codebase
3. **CSS class cleanup** - 42 classes in rider-v3.css need renaming

**Estimated effort:** 2-4 hours for a complete cleanup with testing

**Recommendation:** Perform changes in phases with thorough testing between each phase. Consider creating a migration script for the constant renames to ensure consistency.
