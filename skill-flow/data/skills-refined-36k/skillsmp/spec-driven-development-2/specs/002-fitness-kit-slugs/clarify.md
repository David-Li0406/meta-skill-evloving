# Feature 002: Fitness Kit Slug URLs - Clarification

**Status**: Clarified ✅  
**Date**: 2025-01-XX

---

## 🤔 Questions & Answers

### Q1: Should slugs be editable after creation?
**Answer:** No, slugs should be immutable once set. This prevents breaking existing marketing links or bookmarks. If a slug needs to change, it should require a manual database update by an administrator, not through the application UI.

**Impact on Implementation:**
- No admin UI for slug editing required
- Validation only matters at creation/seed time
- No slug history or redirect tracking needed

---

### Q2: What happens if YK-1 (Yoga Kit) doesn't exist in the database?
**Answer:** The spec lists YK-1 with slug "yoga-kit-1" but we need to verify it exists. If it doesn't exist:
- Migration should only populate slugs for existing kits
- Spec example includes it for completeness
- No error if YK-1 is missing

**Impact on Implementation:**
- Migration uses `find_by` instead of `find` (no error if missing)
- Data migration skips missing kits gracefully

---

### Q3: Should the old nested resource routes be completely removed?
**Answer:** Yes. The old routes `/promise_fitness_kits/:id/orders/new` will be completely removed and replaced with `/:slug`. This is acceptable because:
- Internal application only (no external API consumers)
- No public bookmarks to preserve
- Clean break, simpler codebase

**Impact on Implementation:**
- Delete old nested resource routes entirely
- Update all route helpers in views and tests
- No need to maintain backward compatibility

---

### Q4: How should route precedence work to avoid conflicts?
**Answer:** The slug routes should be defined LAST in routes.rb, after all other explicit routes. This ensures:
- `/` (root) matches first
- `/orders/:id` matches before slug pattern
- `/up` (health check) matches before slug pattern
- `/:slug` acts as catch-all for remaining paths

**Impact on Implementation:**
- Position slug routes at bottom of routes.rb
- Route constraint prevents matching non-slug patterns
- Order matters: specific routes before catch-all

---

### Q5: Should we validate slug format on update or only on create?
**Answer:** Since slugs are immutable (see Q1), validation only matters on creation. However, for data integrity, validations should run on both create and update (even though updates won't happen in practice).

**Impact on Implementation:**
- Standard Rails validations (validates :slug, presence: true, uniqueness: true, format: ...)
- No special handling for updates vs creates

---

### Q6: What should the regex constraint in routes be?
**Answer:** Route constraint should match valid slugs: `/[a-z0-9\-]+/`
- Lowercase letters a-z
- Digits 0-9
- Hyphens (escaped as `\-`)
- Must have at least one character (+ quantifier)

**Impact on Implementation:**
- Use this exact regex in routes.rb constraint
- Prevents matching empty path or root
- Prevents matching uppercase or special characters

---

### Q7: Should the slug be part of URL generation or a parameter?
**Answer:** The slug should be passed as the `:slug` parameter to route helpers:
- `fitness_kit_order_path("pilates-kit-1")` or `fitness_kit_order_path(slug: "pilates-kit-1")`
- Can pass the kit object if we make `to_param` return the slug
- Simpler approach: pass slug string directly

**Impact on Implementation:**
- Views use: `fitness_kit_order_path(@kit.slug)` or `fitness_kit_order_path(slug: @kit.slug)`
- Controller gets slug from `params[:slug]`
- Cleaner than overriding `to_param`

---

### Q8: Should invalid slug redirect preserve the attempted slug in error message?
**Answer:** No, keep error message generic: "Fitness kit not found". Don't echo back user input to avoid:
- Potential XSS if slug not sanitized in flash message
- Confusing messages for typos
- Keep it simple

**Impact on Implementation:**
- Flash message: `flash[:alert] = 'Fitness kit not found'`
- No need to interpolate slug value
- Redirect to `root_path`

---

### Q9: What about Test Kit fixture?
**Answer:** The test helper creates a kit with name "Test Kit" for testing. This needs a slug too.

**Impact on Implementation:**
- Test fixtures should specify slug: "test-kit"
- Update test setup to include slug
- Verify "Test Kit.png" image works with slug-based lookup (or update image reference logic if needed)

---

### Q10: Should we index the slug column?
**Answer:** Yes, absolutely. The slug will be used in WHERE clauses for every order page load.

**Impact on Implementation:**
- Migration includes: `add_index :promise_fitness_kits, :slug, unique: true`
- Database performs index lookup (O(log n) instead of O(n))
- Essential for performance

---

## ✅ Clarification Checklist

- [x] Slug mutability defined (immutable)
- [x] Missing YK-1 kit handled (graceful skip)
- [x] Old routes removal confirmed (yes, delete them)
- [x] Route precedence strategy defined (slug routes last)
- [x] Validation timing clarified (create and update)
- [x] Route regex constraint specified
- [x] URL generation approach chosen (pass slug as param)
- [x] Error message format decided (generic, no echo)
- [x] Test fixture slug requirement identified
- [x] Database indexing requirement confirmed

---

## 📋 Updated Requirements Summary

### Database
- Add `slug` column: string, not null, indexed, unique
- Index for performance: `add_index :promise_fitness_kits, :slug, unique: true`
- Gracefully handle missing YK-1 in migration

### Model
- Validate presence, uniqueness, format on all operations
- Format regex: `/\A[a-z0-9-]+\z/`
- No special `to_param` override (keep simple)

### Routes
- Place slug routes LAST in routes.rb
- Constraint: `constraints: { slug: /[a-z0-9\-]+/ }`
- Named routes: `fitness_kit_order_path`, `create_fitness_kit_order_path`
- Delete old nested resource routes entirely

### Controller
- Find kit by slug: `PromiseFitnessKit.find_by(slug: params[:slug])`
- Redirect if not found: `redirect_to root_path, alert: 'Fitness kit not found'`
- All other logic unchanged

### Views
- Use: `fitness_kit_order_path(@kit.slug)`
- Use: `create_fitness_kit_order_path(@kit.slug)`

### Tests
- Update test fixtures with slug values
- Update all test URLs to use slug paths
- Test invalid slug redirect behavior
- Verify all existing tests still pass

---

**Ready for:** Implementation Plan (`/speckit.plan`)