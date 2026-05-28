# Feature 002: Fitness Kit Slug URLs

**Status**: Specification  
**Created**: 2025-01-XX  
**Priority**: High  
**Dependencies**: Feature 001 (Fitness Kit Ordering System)

---

## 📋 Overview

Add dedicated URL slugs to fitness kits to enable clean, SEO-friendly URLs for order pages. Instead of `/promise_fitness_kits/11/orders/new`, users will access order forms via descriptive slugs like `/pilates-kit-1/`.

---

## 🎯 Problem Statement

Currently, fitness kit order URLs use database IDs in a nested resource structure:
- `/promise_fitness_kits/11/orders/new`

**Issues:**
1. Not user-friendly or memorable
2. Exposes internal database structure
3. Poor for SEO and marketing
4. Breaks if database IDs change during data migration

**Desired URLs:**
- `/strength-kit-1/`
- `/pilates-kit-1/`
- `/yoga-kit-1/`
- `/walking-trekking-kit-1/`

---

## 👥 User Stories

### Story 1: Clean URL Access
**As a** customer  
**I want** to access fitness kit order pages via clean, descriptive URLs  
**So that** I can easily remember and share links

**Acceptance Criteria:**
- [ ] Order form accessible at `/:slug` (e.g., `/pilates-kit-1/`)
- [ ] Slug appears in browser address bar
- [ ] Direct navigation to slug URL loads correct order form
- [ ] Invalid slug redirects to homepage with error message

### Story 2: Marketing Link Compatibility
**As a** marketing team member  
**I want** to use descriptive URLs in campaigns  
**So that** customers can easily type or click promotional links

**Acceptance Criteria:**
- [ ] Slugs are short, memorable, and descriptive
- [ ] Slugs contain only lowercase letters, numbers, and hyphens
- [ ] Each kit has a unique slug
- [ ] Slugs remain stable (don't change automatically)

### Story 3: Existing Functionality Preserved
**As a** system administrator  
**I want** all existing order functionality to continue working  
**So that** the URL change doesn't break any features

**Acceptance Criteria:**
- [ ] Order creation still works via slug URLs
- [ ] Coupon validation unchanged
- [ ] Order confirmation page still accessible
- [ ] All validations and business logic preserved
- [ ] Existing tests pass with updated routes

---

## 🔧 Functional Requirements

### FR-1: Slug Field
**Description:** Add a `slug` field to `promise_fitness_kits` table  
**Rules:**
- String type, indexed for fast lookup
- Unique constraint at database level
- Not nullable (required field)
- Maximum length: 100 characters
- Format: lowercase letters, numbers, hyphens only (regex: `/^[a-z0-9-]+$/`)

### FR-2: URL Routing
**Description:** Map slug URLs to order controller actions  
**Routes:**
- `GET /:slug` → Show order form for fitness kit with matching slug
- `POST /:slug` → Create order for fitness kit with matching slug
- Route constraint: slug must match `/[a-z0-9\-]+/` pattern

### FR-3: Slug Lookup
**Description:** Find fitness kits by slug instead of ID  
**Behavior:**
- Controller finds kit using `PromiseFitnessKit.find_by(slug: params[:slug])`
- If slug not found, redirect to root path with flash message: "Fitness kit not found"
- Do not raise 404 exception (soft fail with redirect)

### FR-4: View Updates
**Description:** Update all views to use slug-based URLs  
**Changes Required:**
- Homepage kit links: `fitness_kit_order_path(kit.slug)`
- Order form submission: `create_fitness_kit_order_path(@promise_fitness_kit.slug)`
- Any other internal links referencing fitness kits

### FR-5: Data Migration
**Description:** Populate slug values for existing fitness kits  
**Mapping:**
```
SK-1 → strength-kit-1
SK-2 → strength-kit-2
SK-3 → strength-kit-3
SK-4 → strength-kit-4
PK-1 → pilates-kit-1
YK-1 → yoga-kit-1
WK-1 → walking-trekking-kit-1
```

---

## 🚫 Non-Functional Requirements

### Performance
- Slug lookup must use database index (no full table scan)
- No performance degradation vs. ID-based lookup
- Route matching must be O(1) with regex constraint

### Security
- Slug validation prevents SQL injection
- Route constraint prevents path traversal attempts
- No sensitive data exposed in URLs

### Maintainability
- Slug updates require explicit action (no auto-generation)
- Clear error messages for duplicate slugs
- Model validation ensures slug format compliance

---

## 📊 Data Requirements

### Existing Fitness Kits (6 total)
| ID | Name | New Slug |
|----|------|----------|
| 7  | SK-1 | strength-kit-1 |
| 8  | SK-2 | strength-kit-2 |
| 9  | SK-3 | strength-kit-3 |
| 10 | SK-4 | strength-kit-4 |
| 11 | PK-1 | pilates-kit-1 |
| 12 | WK-1 | walking-trekking-kit-1 |
| ?  | YK-1 | yoga-kit-1 |

**Note:** Verify YK-1 exists in database. If not, then update the seed script file to add the YK-1 kit.

---

## ✅ Acceptance Criteria

### Database Schema
- [ ] `promise_fitness_kits` table has `slug` column (string, not null, unique, indexed)
- [ ] Migration successfully runs and rolls back cleanly
- [ ] All existing kits have populated slug values
- [ ] Database constraint prevents duplicate slugs
- [ ] Database constraint prevents null slugs

### Model Validation
- [ ] `PromiseFitnessKit` validates slug presence
- [ ] `PromiseFitnessKit` validates slug uniqueness
- [ ] `PromiseFitnessKit` validates slug format (only lowercase letters, numbers, hyphens)
- [ ] Invalid slug formats rejected with clear error messages
- [ ] Model tests cover all slug validations

### Routing
- [ ] `GET /strength-kit-1` loads order form for SK-1
- [ ] `POST /pilates-kit-1` creates order for PK-1
- [ ] `GET /invalid-slug` redirects to homepage
- [ ] Route helper `fitness_kit_order_path("pilates-kit-1")` generates `/pilates-kit-1`
- [ ] Route helper `create_fitness_kit_order_path("yoga-kit-1")` generates `/yoga-kit-1`
- [ ] Routes do NOT match root path (`/`)
- [ ] Routes do NOT match other application paths (`/orders`, `/up`, etc.)

### Controller Behavior
- [ ] `OrdersController#new` finds kit by slug
- [ ] `OrdersController#create` finds kit by slug
- [ ] Invalid slug redirects to root with flash alert
- [ ] `@promise_fitness_kit` correctly assigned in both actions
- [ ] All existing controller logic unchanged (coupon validation, order creation)

### Views
- [ ] Homepage links use slug-based paths
- [ ] Order form submits to slug-based path
- [ ] No broken links or missing route errors
- [ ] All views render correctly with slug URLs

### Tests
- [ ] Model tests for slug validations
- [ ] Controller tests updated to use slug parameters
- [ ] Controller test for invalid slug redirect
- [ ] Integration tests verify end-to-end slug functionality
- [ ] All existing tests pass with 0 failures, 0 errors
- [ ] Test coverage remains ≥90%

### User Experience
- [ ] Order flow works identically to before (just different URL)
- [ ] Error messages clear and helpful
- [ ] No visual changes to UI
- [ ] Page load times unchanged

---

## 🔍 Edge Cases

### EC-1: Slug Conflicts
**Scenario:** Two kits attempt to use same slug  
**Expected:** Second kit validation fails with error: "Slug has already been taken"

### EC-2: Invalid Slug Format
**Scenario:** Kit created with slug "Pilates Kit 1" (spaces, capitals)  
**Expected:** Validation fails with error: "Slug must contain only lowercase letters, numbers, and hyphens"

### EC-3: Empty Slug
**Scenario:** Kit created without slug value  
**Expected:** Validation fails with error: "Slug can't be blank"

### EC-4: Slug Matches Other Routes
**Scenario:** Kit with slug "orders" or "up"  
**Expected:** Works correctly (slug routes have higher precedence via ordering)

### EC-5: SQL Injection Attempt
**Scenario:** URL like `/'; DROP TABLE orders; --/`  
**Expected:** Route constraint rejects (doesn't match pattern), 404 not found

### EC-6: Path Traversal Attempt
**Scenario:** URL like `/../../../etc/passwd`  
**Expected:** Route constraint rejects, 404 not found

---

## 📝 Implementation Notes

### Migration Strategy
1. Add `slug` column (allow null temporarily)
2. Populate slug values for existing kits
3. Add not-null constraint
4. Add unique constraint
5. Add database index

### Backward Compatibility
- Old nested resource URLs (`/promise_fitness_kits/:id/orders/new`) will be removed
- No backward compatibility needed (internal app, no external integrations)
- Update any bookmarks or saved links manually

### Future Considerations
- **Not in scope:** Admin UI for editing slugs
- **Not in scope:** Automatic slug generation from names
- **Not in scope:** Slug history or redirects from old slugs

---

## 🧪 Testing Scenarios

### Scenario 1: Happy Path
1. Visit homepage at `/`
2. Click "Order This Kit" for "Pilates Kit 1"
3. URL should be `/pilates-kit-1`
4. Order form displays with PK-1 details
5. Fill form with valid data and coupon
6. Submit form
7. Redirects to order confirmation page
8. Order created successfully

### Scenario 2: Direct URL Access
1. Navigate directly to `/yoga-kit-1`
2. Order form loads immediately
3. YK-1 kit details displayed
4. Form functions normally

### Scenario 3: Invalid Slug
1. Navigate to `/nonexistent-kit-99`
2. Redirects to `/` (homepage)
3. Flash message: "Fitness kit not found"
4. Homepage loads normally

### Scenario 4: Case Sensitivity
1. Navigate to `/Pilates-Kit-1` (capital P)
2. Route does NOT match (constraint requires lowercase)
3. 404 or routing error (caught by Rails)

### Scenario 5: Special Characters
1. Navigate to `/pilates_kit_1` (underscore instead of hyphen)
2. Route does NOT match
3. 404 or routing error

---

## 📚 References

- Feature 001: Fitness Kit Ordering System
- Rails Routing Guide: https://guides.rubyonrails.org/routing.html
- Slugs Best Practices: lowercase, hyphens, SEO-friendly
- Project Constitution: `.specify/memory/constitution.md`

---

## ✨ Success Metrics

- [ ] All 6 fitness kits accessible via slug URLs
- [ ] Zero routing errors in production logs
- [ ] Order conversion rate unchanged
- [ ] Page load times ≤ current performance
- [ ] Test suite passes with 100% success rate
- [ ] Marketing team confirms links work in campaigns

---

**Next Steps:**
1. Clarify any ambiguities (`/speckit.clarify`)
2. Create technical implementation plan (`/speckit.plan`)
3. Generate task breakdown (`/speckit.tasks`)
4. Execute implementation (`/speckit.implement`)
