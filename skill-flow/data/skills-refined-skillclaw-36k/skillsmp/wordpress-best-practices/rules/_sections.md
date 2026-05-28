# Sections

## 1. Security Hardening (security)

**Impact:** CRITICAL
**Description:** Output escaping, input sanitization, nonce verification, capability checks. WordPress provides security functions that must be used correctly to prevent XSS, SQL injection, and CSRF attacks.

## 2. Database Optimization (database)

**Impact:** HIGH
**Description:** Autoload options, transient caching, meta query optimization. Improper database usage causes slow page loads and increased server load.

## 3. Performance (perf)

**Impact:** HIGH
**Description:** Asset enqueuing, lazy loading, heartbeat control. Performance optimizations that significantly improve page speed and server efficiency.

## 4. Plugin Development (plugin)

**Impact:** MEDIUM-HIGH
**Description:** Function prefixing, hooks/filters, activation/deactivation hooks, uninstall cleanup. Following plugin standards ensures compatibility and maintainability.

## 5. Theme Development (theme)

**Impact:** MEDIUM
**Description:** Template hierarchy, child themes, customizer integration, proper enqueuing. Theme development patterns for maintainable, updatable themes.

## 6. REST API (api)

**Impact:** MEDIUM
**Description:** Permission callbacks, schema validation, namespace versioning. Building secure, well-documented REST API endpoints.

## 7. Multisite (multisite)

**Impact:** LOW-MEDIUM
**Description:** Network admin operations, site switching, blog-specific options. Patterns for WordPress multisite development.

## 8. Gutenberg/Blocks (blocks)

**Impact:** LOW-MEDIUM
**Description:** Block patterns, InnerBlocks, server-side rendering. Modern WordPress block editor development.
