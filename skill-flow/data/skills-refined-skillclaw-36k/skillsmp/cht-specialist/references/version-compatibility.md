# CHT Version Compatibility and Migration Reference

## Supported Versions

| Version | Status | Release Date |
|---------|--------|--------------|
| 5.0.x | Supported | Nov 20, 2025 |
| 4.22.x | Supported | Oct 10, 2025 |
| 4.21.x | Supported | Jun 25, 2025 |
| 4.20.x | EOL | Jun 04, 2025 |
| 3.17.x | EOL | Oct 11, 2022 |

**Support Policy:** Minor versions are supported for 3 months after the next minor release. The latest minor of a major version is supported for 12 months after the next major release.

---

## Dependency Matrix

| CHT Version | Browser | Android OS | CHT Android | CHT Sync |
|-------------|---------|------------|-------------|----------|
| 5.x | Chrome 107+, Firefox latest | 5.0+ | 1.5.2+ | 1.1.0+ |
| 4.16-4.22.x | Chrome 90+, Firefox latest | 5.0+ | 1.0+ | 1.1.0+ |
| 4.0-4.15.x | Chrome 90+, Firefox latest | 5.0+ | 1.0+ | 1.1.0+ |
| 3.x | Chrome 53+, Firefox latest | 4.4+ | 0.4.5+ | 1.1.0+ |

---

## Feature Timeline

### CHT 5.x Features

| Version | Feature |
|---------|---------|
| 5.0.0 | CouchDB Nouveau, 30%+ disk savings, 69% faster sync |

### CHT 4.x Key Features

| Version | Feature |
|---------|---------|
| 4.0.0 | Enketo upgrade, new hosting infrastructure |
| 4.2.0 | Training Cards, Auto-create users, Extension Libraries |
| 4.3.0 | Prometheus API, Phone number registration via SMS |
| 4.12.0 | Material Design navigation |
| 4.15.0 | Training Materials page |
| 4.16.0 | CouchDB 3.4.2, Arabic language support |
| 4.21.0 | Task priority sorting, User contact summary in forms |
| 4.22.0 | Nepal DoIT SMS gateway support |

### CHT 3.x Key Features

| Version | Feature |
|---------|---------|
| 3.0.0 | CouchDB 2.2, Docker support, Horticulturalist |
| 3.7.0 | Configurable contact types |
| 3.9.0 | Target aggregates |
| 3.10.0 | Linked documents |
| 3.11.0 | Angular v10 upgrade, RapidPro SMS gateway |
| 3.12.0 | CHT API (cht.v1) |
| 3.17.0 | Material Design search/filter UI |

---

## Feature Compatibility Table

| Feature | Minimum Version |
|---------|-----------------|
| Configurable contact types | 3.7.0 |
| Target aggregates | 3.9.0 |
| Linked documents | 3.10.0 |
| CHT API (cht.v1) | 3.12.0 |
| Extension libraries | 4.2.0 |
| Training cards | 4.2.0 |
| `add-date` XPath function | 4.0.0 |
| `cht:difference-in-*` XPath functions | 4.7.0 |
| `trigger` countdown timer | 4.7.0 |
| `cht:strip-whitespace` | 4.10.0 |
| `cht:validate-luhn` | 4.10.0 |
| `string` tel input | 4.11.0 |
| `cht.v1.analytics.getTargetDocs()` | 4.11.0 |
| `duplicate_check` in contact forms | 4.19.0 |
| Task priority scoring | 4.21.0 |
| Contact form task actions | 4.21.0 |
| `user-contact-summary` instance | 4.21.0 |
| `userSummary` in expressions | 4.21.0 |
| CouchDB Nouveau | 5.0.0 |

---

## Breaking Changes by Version

### 3.x to 4.0.0 Breaking Changes

**Enketo XPath Changes:**
- `+` operator cannot concatenate strings (use `concat()`)
- Invalid XPath paths no longer equal empty string
- Unanswered number questions return `NaN` instead of `0`

**Date Function Changes:**
- `format-date`/`format-date-time` reject month values <= 0
- `today` returns midnight instead of current time
- `decimal-date-time` uses local timezone instead of UTC

**Layout Changes:**
- `horizontal`/`horizontal-compact` appearances deprecated
- Use `columns`, `columns-pack`, `columns-n` instead
- Markdown syntax supported in all question labels

**Requirements:**
- CHT Android 1.0.0+
- Chrome 90+

### 4.x to 5.0.0 Breaking Changes

**Kubernetes:**
- Upgrade button removed from admin app (Stage only)
- Must use Helm charts from cht-core repository

**Configuration:**
- `app_url` required for token login
- Languages must be configured in app_settings
- Declarative configuration mandatory
- `needs_signoff` must be boolean, not string
- CHT 4.0-4.4 must upgrade to 4.5+ first

**Browser:**
- Chrome 107+ required

**Removed Views:**
- `contacts_by_freetext`
- `contacts_by_type_freetext`
- `reports_by_freetext`

**Disk Space:**
- 5x current space required for upgrade

---

## Migration Checklists

### Upgrading to CHT 4.x

1. [ ] Update CHT Android to 1.0.0+ in Play Store
2. [ ] Notify users to update from Play Store
3. [ ] Upgrade CHT Conf
4. [ ] Test all forms with cht-conf-test-harness 3.x
5. [ ] Review XPath expressions for deprecated syntax
6. [ ] Update date calculations using new functions
7. [ ] Replace `horizontal`/`horizontal-compact` with `columns`
8. [ ] Test on non-production CHT 4.x instance

### Upgrading to CHT 5.x

1. [ ] Ensure on CHT 4.5+ (upgrade first if on 4.0-4.4)
2. [ ] Verify 5x disk space available
3. [ ] Update CHT Conf to latest version
4. [ ] Recompile and upload app settings
5. [ ] Add `app_url` if using token login
6. [ ] Configure `languages` in app_settings
7. [ ] Verify `needs_signoff` uses boolean values
8. [ ] Check all users have Chrome 107+
9. [ ] For Kubernetes: Use Stage button only, then upgrade via Helm
10. [ ] Schedule maintenance window
11. [ ] Test in non-production environment
12. [ ] Backup data before upgrade

---

## Deprecation Notices

### Deprecated in 4.x

| Item | Status |
|------|--------|
| `can_view_old_action_bar` permission | Removed in 4.12.0 |
| `can_view_old_filter_and_search` permission | Removed in 4.12.0 |
| `can_view_old_navigation` permission | To be removed |
| `horizontal`/`horizontal-compact` appearances | Deprecated |
| Language enabling via web interface | Removed in 5.0.0 |

### Removed in 5.x

| Item | Reason |
|------|--------|
| Kubernetes upgrade button | Prevent version mismatch |
| Legacy Helm charts (medic/helm-charts) | Migrated to cht-core |
| `contacts_by_freetext` view | Replaced by Nouveau |
| `contacts_by_type_freetext` view | Replaced by Nouveau |
| `reports_by_freetext` view | Replaced by Nouveau |
| Pre-3.x database migrations | Legacy code cleanup |
