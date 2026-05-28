# Feature 002: Fitness Kit Slug URLs - Implementation Plan

**Status**: Planning  
**Created**: 2025-01-XX  
**Tech Stack**: Rails 8.1, SQLite3, Minitest  
**Dependencies**: Feature 001 (Fitness Kit Ordering System)

---

## 📋 Overview

Add a `slug` column to the `promise_fitness_kits` table and update routing to use clean URLs (`/pilates-kit-1/`) instead of nested resource paths (`/promise_fitness_kits/11/orders/new`).

---

## 🏗️ Architecture

### Current State
```
Routes: /promise_fitness_kits/:id/orders/new
        /promise_fitness_kits/:id/orders (POST)

Controller: OrdersController#new
            OrdersController#create
            - Finds kit via params[:promise_fitness_kit_id]

Views: new_promise_fitness_kit_order_path(@kit)
       promise_fitness_kit_orders_path(@kit)
```

### Target State
```
Routes: /:slug (GET)  → OrdersController#new
        /:slug (POST) → OrdersController#create

Controller: OrdersController#new
            OrdersController#create
            - Finds kit via PromiseFitnessKit.find_by(slug: params[:slug])

Views: fitness_kit_order_path(@kit.slug)
       create_fitness_kit_order_path(@kit.slug)
```

---

## 🗄️ Database Changes

### Migration: Add Slug Column

**File**: `db/migrate/YYYYMMDDHHMMSS_add_slug_to_promise_fitness_kits.rb`

```ruby
class AddSlugToPromiseFitnessKits < ActiveRecord::Migration[8.1]
  def up
    # Step 1: Add column (nullable initially)
    add_column :promise_fitness_kits, :slug, :string

    # Step 2: Populate slugs for existing kits
    reversible do |dir|
      dir.up do
        mapping = {
          'SK-1' => 'strength-kit-1',
          'SK-2' => 'strength-kit-2',
          'SK-3' => 'strength-kit-3',
          'SK-4' => 'strength-kit-4',
          'PK-1' => 'pilates-kit-1',
          'YK-1' => 'yoga-kit-1',
          'WK-1' => 'walking-trekking-kit-1'
        }

        mapping.each do |name, slug|
          kit = PromiseFitnessKit.find_by(name: name)
          kit&.update_column(:slug, slug)
        end

        # Handle Test Kit if it exists (from test fixtures)
        test_kit = PromiseFitnessKit.find_by(name: 'Test Kit')
        test_kit&.update_column(:slug, 'test-kit')
      end
    end

    # Step 3: Add constraints
    change_column_null :promise_fitness_kits, :slug, false
    add_index :promise_fitness_kits, :slug, unique: true
  end

  def down
    remove_index :promise_fitness_kits, :slug
    remove_column :promise_fitness_kits, :slug
  end
end
```

**Rationale:**
- Add column nullable first to avoid constraint violation
- Populate existing data before making it required
- Use `update_column` to bypass validations (they don't exist yet)
- Use `find_by` to gracefully handle missing kits
- Add unique index for performance and data integrity

---

## 📦 Model Changes

### Update: PromiseFitnessKit Model

**File**: `app/models/promise_fitness_kit.rb`

```ruby
class PromiseFitnessKit < ApplicationRecord
  # Associations
  has_many :orders, dependent: :restrict_with_error

  # Validations
  validates :name, presence: true, uniqueness: true
  validates :description, presence: true
  validates :slug, presence: true, 
                   uniqueness: true,
                   format: { 
                     with: /\A[a-z0-9-]+\z/, 
                     message: "must contain only lowercase letters, numbers, and hyphens" 
                   }

  # Scopes
  scope :ordered_by_name, -> { order(:name) }

  # Instance Methods
  def to_s
    name
  end
end
```

**Changes:**
- Add slug validation: presence, uniqueness, format
- Remove `to_param` override (not needed - pass slug explicitly)
- Remove `find_by_slug` method (use standard `find_by(slug: ...)`)

**Removed (from previous partial implementation):**
```ruby
# DELETE THESE:
def to_param
  name.parameterize
end

def self.find_by_slug(slug)
  all.find { |kit| kit.to_param == slug }
end
```

---

## 🛣️ Routes Changes

### Update: config/routes.rb

**File**: `config/routes.rb`
this only affects 6 kits.

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
```ruby
Rails.application.routes.draw do
  # Health check
  get "up" => "rails/health#show", as: :rails_health_check

  # Root path
  root "home#index"

  # Order confirmation (specific route before catch-all)
  resources :orders, only: [:show]

  # Fitness kit order pages (catch-all slug routes - MUST BE LAST)
  get '/:slug', to: 'orders#new', as: :fitness_kit_order, 
                constraints: { slug: /[a-z0-9\-]+/ }
  post '/:slug', to: 'orders#create', as: :create_fitness_kit_order, 
                 constraints: { slug: /[a-z0-9\-]+/ }
end
```

**Key Points:**
- Slug routes MUST be last (after all other routes)
- Constraint prevents matching root path or other routes
- Named routes for easy view updates
- Old nested resource routes completely removed

**Route Precedence:**
1. `GET /up` → health check
2. `GET /` → root
3. `GET /orders/:id` → order show
4. `GET /:slug` → fitness kit order form
5. `POST /:slug` → create order

---

## 🎮 Controller Changes

### Update: OrdersController

**File**: `app/controllers/orders_controller.rb`

**Changes Required:**

1. **Update before_action callback name:**
```ruby
# BEFORE:
before_action :set_promise_fitness_kit_from_slug, only: [:new, :create]

# AFTER (rename for clarity):
before_action :set_promise_fitness_kit, only: [:new, :create]
```

2. **Update private method:**
```ruby
# BEFORE:
def set_promise_fitness_kit_from_slug
  @promise_fitness_kit = PromiseFitnessKit.find_by_slug(params[:slug])

  if @promise_fitness_kit.nil?
    redirect_to root_path, alert: 'Fitness kit not found'
  end
end

# AFTER:
def set_promise_fitness_kit
  @promise_fitness_kit = PromiseFitnessKit.find_by(slug: params[:slug])
  
  if @promise_fitness_kit.nil?
    redirect_to root_path, alert: 'Fitness kit not found'
  end
end
```

**Complete Updated File:**
```ruby
class OrdersController < ApplicationController
  before_action :set_promise_fitness_kit, only: [:new, :create]

  def new
    @order = Order.new(promise_fitness_kit: @promise_fitness_kit)
    @coupon_code = CouponCode.new
  end

  def create
    @order = Order.new(order_params)
    @order.promise_fitness_kit = @promise_fitness_kit

    # Find and validate coupon code
    coupon = CouponCode.find_by(code: params[:order][:coupon_code_input]&.upcase&.strip)

    if coupon.nil?
      flash.now[:error] = 'Invalid coupon code'
      render :new, status: :unprocessable_entity
      return
    end

    if coupon.used?
      flash.now[:error] = 'This code has been used before and can no longer be used to place an order'
      render :new, status: :unprocessable_entity
      return
    end

    @order.coupon_code = coupon

    if @order.save
      redirect_to order_path(@order), notice: 'Order placed successfully!'
    else
      flash.now[:error] = 'Please correct the errors below'
      render :new, status: :unprocessable_entity
    end
  end

  def show
    @order = Order.find(params[:id])
  end

  private

  def set_promise_fitness_kit
    @promise_fitness_kit = PromiseFitnessKit.find_by(slug: params[:slug])
    
    if @promise_fitness_kit.nil?
      redirect_to root_path, alert: 'Fitness kit not found'
    end
  end

  def order_params
    params.require(:order).permit(
      :first_name,
      :last_name,
      :address1,
      :address2,
      :city,
      :state,
      :zip,
      :phone,
      :email,
      :description
    )
  end
end
```

---

## 🎨 View Changes

### Update: app/views/home/index.html.erb

**Change:** Update link helper

```erb
<!-- BEFORE: -->
<%= link_to 'Order This Kit', fitness_kit_order_path(kit), class: 'btn btn-primary' %>

<!-- AFTER (explicit slug parameter): -->
<%= link_to 'Order This Kit', fitness_kit_order_path(slug: kit.slug), class: 'btn btn-primary' %>
```

### Update: app/views/orders/new.html.erb

**Change:** Update form URL

```erb
<!-- BEFORE: -->
<%= form_with model: @order, url: create_fitness_kit_order_path(@promise_fitness_kit), ... %>

<!-- AFTER: -->
<%= form_with model: @order, url: create_fitness_kit_order_path(slug: @promise_fitness_kit.slug), ... %>
```

---

## 🧪 Test Changes

### Update: test/models/promise_fitness_kit_test.rb

**File**: `test/models/promise_fitness_kit_test.rb`

**Add slug validation tests:**

```ruby
class PromiseFitnessKitTest < ActiveSupport::TestCase
  # ... existing tests ...

  test "should not save without slug" do
    kit = PromiseFitnessKit.new(name: "Test Kit", description: "Test Description")
    assert_not kit.save, "Saved kit without slug"
    assert_includes kit.errors[:slug], "can't be blank"
  end

  test "should not save with duplicate slug" do
    PromiseFitnessKit.create!(name: "Kit 1", description: "Desc 1", slug: "test-slug")
    kit = PromiseFitnessKit.new(name: "Kit 2", description: "Desc 2", slug: "test-slug")
    assert_not kit.save, "Saved kit with duplicate slug"
    assert_includes kit.errors[:slug], "has already been taken"
  end

  test "should not save slug with uppercase letters" do
    kit = PromiseFitnessKit.new(name: "Test", description: "Test", slug: "Test-Kit")
    assert_not kit.save, "Saved kit with uppercase in slug"
    assert_includes kit.errors[:slug], "must contain only lowercase letters, numbers, and hyphens"
  end

  test "should not save slug with spaces" do
    kit = PromiseFitnessKit.new(name: "Test", description: "Test", slug: "test kit")
    assert_not kit.save, "Saved kit with spaces in slug"
    assert_includes kit.errors[:slug], "must contain only lowercase letters, numbers, and hyphens"
  end

  test "should not save slug with underscores" do
    kit = PromiseFitnessKit.new(name: "Test", description: "Test", slug: "test_kit")
    assert_not kit.save, "Saved kit with underscores in slug"
    assert_includes kit.errors[:slug], "must contain only lowercase letters, numbers, and hyphens"
  end

  test "should save valid slug" do
    kit = PromiseFitnessKit.new(name: "Test", description: "Test", slug: "test-kit-123")
    assert kit.save, "Could not save kit with valid slug"
  end
end
```

### Update: test/controllers/orders_controller_test.rb

**File**: `test/controllers/orders_controller_test.rb`

**Changes:**

1. **Update setup to include slug:**
```ruby
def setup
  @kit = PromiseFitnessKit.create!(
    name: "Test Kit", 
    description: "Test Description",
    slug: "test-kit"  # ADD THIS
  )
  # ... rest of setup
end
```

2. **Update all route helpers to use slug parameter:**
```ruby
# BEFORE:
get fitness_kit_order_url(slug: @kit.to_param)

# AFTER:
get fitness_kit_order_url(slug: @kit.slug)
```

3. **Update all POST requests:**
```ruby
# BEFORE:
post create_fitness_kit_order_url(slug: @kit.to_param), params: @valid_params

# AFTER:
post create_fitness_kit_order_url(slug: @kit.slug), params: @valid_params
```

4. **Update invalid kit test:**
```ruby
# EXISTING (already correct from previous implementation):
test "should redirect to root for invalid kit" do
  get fitness_kit_order_url(slug: "invalid-kit-slug")
  assert_redirected_to root_path
  assert_equal "Fitness kit not found", flash[:alert]
end
```

### Update: test/fixtures/promise_fitness_kits.yml

**File**: `test/fixtures/promise_fitness_kits.yml`

**Add slug to fixtures:**

```yaml
sk1:
  name: SK-1
  description: Strength Kit 1
  slug: strength-kit-1

sk2:
  name: SK-2
  description: Strength Kit 2
  slug: strength-kit-2

# ... add slug to all fixtures
```

---

## 📊 Data Migration Strategy

### Step-by-Step Execution

1. **Create migration:**
```bash
rails generate migration AddSlugToPromiseFitnessKits
```

2. **Edit migration file** (see Database Changes section above)

3. **Run migration:**
```bash
rails db:migrate
```

4. **Verify data:**
```bash
rails runner "PromiseFitnessKit.all.each { |k| puts '#{k.name} → #{k.slug}' }"
```

5. **Test rollback:**
```bash
rails db:rollback
rails db:migrate
```

---

## ✅ Implementation Checklist

### Phase 1: Database
- [ ] Generate migration file
- [ ] Write migration with up/down methods
- [ ] Include slug population for existing kits
- [ ] Add unique index
- [ ] Run migration successfully
- [ ] Verify all kits have slugs
- [ ] Test rollback and re-migrate

### Phase 2: Model
- [ ] Add slug validations to PromiseFitnessKit
- [ ] Remove old `to_param` and `find_by_slug` methods
- [ ] Write model tests for slug validations
- [ ] Run model tests (should pass)

### Phase 3: Routes
- [ ] Update routes.rb with slug routes
- [ ] Remove old nested resource routes
- [ ] Position slug routes LAST
- [ ] Add route constraints
- [ ] Verify routes with `rails routes | grep fitness`

### Phase 4: Controller
- [ ] Update `set_promise_fitness_kit` method
- [ ] Use `find_by(slug: params[:slug])`
- [ ] Ensure redirect for invalid slug
- [ ] No other controller changes needed

### Phase 5: Views
- [ ] Update home/index.html.erb link
- [ ] Update orders/new.html.erb form URL
- [ ] Use `slug: kit.slug` in path helpers

### Phase 6: Tests
- [ ] Add slug to test fixtures
- [ ] Update test setup to include slug
- [ ] Update all route helpers in tests
- [ ] Add model tests for slug validation
- [ ] Verify invalid slug redirect test
- [ ] Run full test suite
- [ ] Achieve 0 failures, 0 errors

### Phase 7: Manual Testing
- [ ] Start server: `rails server`
- [ ] Visit homepage: `http://localhost:3000`
- [ ] Click kit link, verify URL is `/:slug`
- [ ] Submit order form, verify success
- [ ] Test invalid slug: `http://localhost:3000/bad-slug`
- [ ] Verify redirect to root with flash message

---

## 🚀 Deployment Notes

### Pre-Deployment Checklist
- [ ] All tests passing locally
- [ ] Migration tested on development database
- [ ] No breaking changes to other features

### Deployment Steps
1. Run migration: `rails db:migrate`
2. Verify slug data populated
3. Restart application
4. Smoke test: visit one kit URL
5. Monitor logs for routing errors

### Rollback Plan
If issues arise:
```bash
rails db:rollback
# Restore old routes.rb from git
git checkout HEAD -- config/routes.rb
# Restart application
```

---

## 📝 Notes

- **Image references:** Order form uses `image_tag "#{@promise_fitness_kit.name}.png"`. This is unaffected by slug changes (still uses name).
- **Order model:** No changes needed. Still references `promise_fitness_kit_id`.
- **Coupon logic:** Completely unchanged.
- **Performance:** Slug lookup with index should be as fast as ID lookup.

---

## 🔗 References

- Feature 001 Spec: `../001-fitness-kit-ordering/spec.md`
- Rails Routing Guide: https://guides.rubyonrails.org/routing.html
- ActiveRecord Migrations: https://guides.rubyonrails.org/active_record_migrations.html
- Constitution: `../../.specify/memory/constitution.md`

---

**Status**: Ready for task breakdown (`/speckit.tasks`)
