# Feature 002: Fitness Kit Slug URLs - Task Breakdown

**Status**: Ready for Implementation  
**Created**: 2025-01-XX  
**Estimated Time**: 2-3 hours

---

## 📋 Task Overview

Total tasks: 28  
Sequential dependencies: Yes  
Parallel opportunities: Limited (tests can be written alongside implementation)

---

## 🔢 Task List

### Phase 1: Database Migration (Tasks 1-5)

#### Task 1.1: Generate Migration File
**File**: `db/migrate/YYYYMMDDHHMMSS_add_slug_to_promise_fitness_kits.rb`  
**Action**: Create  
**Command**: `rails generate migration AddSlugToPromiseFitnessKits`  
**Success Criteria**: Migration file created in `db/migrate/`

---

#### Task 1.2: Write Migration Up Method
**File**: `db/migrate/YYYYMMDDHHMMSS_add_slug_to_promise_fitness_kits.rb`  
**Action**: Edit  
**Details**:
```ruby
def up
  # Add slug column (nullable)
  add_column :promise_fitness_kits, :slug, :string
  
  # Populate existing data
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
      
      # Handle test fixture
      test_kit = PromiseFitnessKit.find_by(name: 'Test Kit')
      test_kit&.update_column(:slug, 'test-kit')
    end
  end
  
  # Add constraints
  change_column_null :promise_fitness_kits, :slug, false
  add_index :promise_fitness_kits, :slug, unique: true
end
```
**Success Criteria**: Up method complete with data population

---

#### Task 1.3: Write Migration Down Method
**File**: `db/migrate/YYYYMMDDHHMMSS_add_slug_to_promise_fitness_kits.rb`  
**Action**: Edit  
**Details**:
```ruby
def down
  remove_index :promise_fitness_kits, :slug
  remove_column :promise_fitness_kits, :slug
end
```
**Success Criteria**: Down method provides clean rollback

---

#### Task 1.4: Run Migration
**Command**: `rails db:migrate`  
**Success Criteria**: 
- Migration runs without errors
- `slug` column exists in schema
- All existing kits have slug values

---

#### Task 1.5: Verify Migration Data
**Command**: `rails runner "PromiseFitnessKit.all.each { |k| puts \"#{k.name} → #{k.slug}\" }"`  
**Expected Output**:
```
SK-1 → strength-kit-1
SK-2 → strength-kit-2
SK-3 → strength-kit-3
SK-4 → strength-kit-4
PK-1 → pilates-kit-1
WK-1 → walking-trekking-kit-1
```
**Success Criteria**: All kits have correct slug values

---

### Phase 2: Model Updates (Tasks 6-8)

#### Task 2.1: Add Slug Validations
**File**: `app/models/promise_fitness_kit.rb`  
**Action**: Edit  
**Details**: Add after existing validations:
```ruby
validates :slug, presence: true, 
                 uniqueness: true,
                 format: { 
                   with: /\A[a-z0-9-]+\z/, 
                   message: "must contain only lowercase letters, numbers, and hyphens" 
                 }
```
**Success Criteria**: Validation code added to model

---

#### Task 2.2: Remove Old Slug Methods
**File**: `app/models/promise_fitness_kit.rb`  
**Action**: Edit  
**Details**: Delete these methods if they exist:
- `to_param` method
- `find_by_slug` class method
**Success Criteria**: Old methods removed, model is clean

---

#### Task 2.3: Verify Model State
**File**: `app/models/promise_fitness_kit.rb`  
**Action**: Review  
**Expected State**:
- Has slug validation
- No `to_param` override
- No custom `find_by_slug` method
**Success Criteria**: Model matches plan specification

---

### Phase 3: Routes Configuration (Tasks 9-11)

#### Task 3.1: Update Routes File
**File**: `config/routes.rb`  
**Action**: Edit  
**Details**: Replace existing content with:
```ruby
Rails.application.routes.draw do
  # Health check
  get "up" => "rails/health#show", as: :rails_health_check

  # Root path
  root "home#index"

  # Order confirmation (must be before catch-all)
  resources :orders, only: [:show]

  # Fitness kit order pages (MUST BE LAST)
  get '/:slug', to: 'orders#new', as: :fitness_kit_order, 
                constraints: { slug: /[a-z0-9\-]+/ }
  post '/:slug', to: 'orders#create', as: :create_fitness_kit_order, 
                 constraints: { slug: /[a-z0-9\-]+/ }
end
```
**Success Criteria**: Routes updated, old nested routes removed

---

#### Task 3.2: Verify Route Configuration
**Command**: `rails routes | grep -E "(fitness_kit|orders)"`  
**Expected Output**:
```
fitness_kit_order GET  /:slug(.:format)     orders#new {slug: /[a-z0-9\-]+/}
create_fitness_kit_order POST /:slug(.:format)     orders#create {slug: /[a-z0-9\-]+/}
order GET  /orders/:id(.:format)    orders#show
```
**Success Criteria**: Routes match expected output

---

#### Task 3.3: Test Route Matching
**Command**: Test specific routes work:
```bash
# Should match
rails runner "puts Rails.application.routes.recognize_path('/pilates-kit-1', method: :get)"
# Should not match (no slug route for root)
rails runner "puts Rails.application.routes.recognize_path('/', method: :get)"
```
**Success Criteria**: Correct route matching behavior

---

### Phase 4: Controller Updates (Tasks 12-14)

#### Task 4.1: Update set_promise_fitness_kit Method
**File**: `app/controllers/orders_controller.rb`  
**Action**: Edit  
**Current Method Name**: `set_promise_fitness_kit_from_slug`  
**New Method**:
```ruby
def set_promise_fitness_kit
  @promise_fitness_kit = PromiseFitnessKit.find_by(slug: params[:slug])
  
  if @promise_fitness_kit.nil?
    redirect_to root_path, alert: 'Fitness kit not found'
  end
end
```
**Success Criteria**: Method uses `find_by(slug: ...)` and handles nil case

---

#### Task 4.2: Update Before Action Callback
**File**: `app/controllers/orders_controller.rb`  
**Action**: Edit  
**Change**: Update callback at top of controller:
```ruby
# FROM:
before_action :set_promise_fitness_kit_from_slug, only: [:new, :create]

# TO:
before_action :set_promise_fitness_kit, only: [:new, :create]
```
**Success Criteria**: Callback name matches method name

---

#### Task 4.3: Verify Controller State
**File**: `app/controllers/orders_controller.rb`  
**Action**: Review  
**Checklist**:
- [ ] `before_action :set_promise_fitness_kit` at top
- [ ] Private method `set_promise_fitness_kit` uses `params[:slug]`
- [ ] Redirect to root_path if kit not found
- [ ] All other methods unchanged (new, create, show)
**Success Criteria**: Controller matches plan specification

---

### Phase 5: View Updates (Tasks 15-16)

#### Task 5.1: Update Homepage Kit Links
**File**: `app/views/home/index.html.erb`  
**Action**: Edit  
**Find**: `<%= link_to 'Order This Kit', fitness_kit_order_path(kit), class: 'btn btn-primary' %>`  
**Replace With**: `<%= link_to 'Order This Kit', fitness_kit_order_path(slug: kit.slug), class: 'btn btn-primary' %>`  
**Success Criteria**: Link uses explicit slug parameter

---

#### Task 5.2: Update Order Form URL
**File**: `app/views/orders/new.html.erb`  
**Action**: Edit  
**Find**: `url: create_fitness_kit_order_path(@promise_fitness_kit)`  
**Replace With**: `url: create_fitness_kit_order_path(slug: @promise_fitness_kit.slug)`  
**Success Criteria**: Form URL uses slug parameter

---

### Phase 6: Test Fixtures (Tasks 17-18)

#### Task 6.1: Update Test Fixtures with Slugs
**File**: `test/fixtures/promise_fitness_kits.yml`  
**Action**: Edit  
**Details**: Add `slug:` field to each fixture. Example:
```yaml
sk1:
  name: SK-1
  description: Strength Kit 1
  slug: strength-kit-1

sk2:
  name: SK-2
  description: Strength Kit 2
  slug: strength-kit-2
```
**Success Criteria**: All fixtures have slug values

---

#### Task 6.2: Verify Fixtures Load
**Command**: `rails test:prepare`  
**Success Criteria**: Test database loads without errors

---

### Phase 7: Model Tests (Tasks 19-22)

#### Task 7.1: Add Slug Presence Test
**File**: `test/models/promise_fitness_kit_test.rb`  
**Action**: Edit  
**Add Test**:
```ruby
test "should not save without slug" do
  kit = PromiseFitnessKit.new(name: "Test Kit", description: "Test Description")
  assert_not kit.save, "Saved kit without slug"
  assert_includes kit.errors[:slug], "can't be blank"
end
```
**Success Criteria**: Test added

---

#### Task 7.2: Add Slug Uniqueness Test
**File**: `test/models/promise_fitness_kit_test.rb`  
**Action**: Edit  
**Add Test**:
```ruby
test "should not save with duplicate slug" do
  PromiseFitnessKit.create!(name: "Kit 1", description: "Desc 1", slug: "test-slug")
  kit = PromiseFitnessKit.new(name: "Kit 2", description: "Desc 2", slug: "test-slug")
  assert_not kit.save, "Saved kit with duplicate slug"
  assert_includes kit.errors[:slug], "has already been taken"
end
```
**Success Criteria**: Test added

---

#### Task 7.3: Add Slug Format Tests
**File**: `test/models/promise_fitness_kit_test.rb`  
**Action**: Edit  
**Add Tests**:
```ruby
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
```
**Success Criteria**: All format tests added

---

#### Task 7.4: Add Valid Slug Test
**File**: `test/models/promise_fitness_kit_test.rb`  
**Action**: Edit  
**Add Test**:
```ruby
test "should save valid slug" do
  kit = PromiseFitnessKit.new(name: "Test", description: "Test", slug: "test-kit-123")
  assert kit.save, "Could not save kit with valid slug"
end
```
**Success Criteria**: Test added

---

### Phase 8: Controller Tests (Tasks 23-25)

#### Task 8.1: Update Test Setup with Slug
**File**: `test/controllers/orders_controller_test.rb`  
**Action**: Edit  
**Find**: `@kit = PromiseFitnessKit.create!(name: "Test Kit", description: "Test Description")`  
**Replace With**:
```ruby
@kit = PromiseFitnessKit.create!(
  name: "Test Kit", 
  description: "Test Description",
  slug: "test-kit"
)
```
**Success Criteria**: Test setup includes slug

---

#### Task 8.2: Update All GET Request Tests
**File**: `test/controllers/orders_controller_test.rb`  
**Action**: Edit  
**Find All**: `fitness_kit_order_url(slug: @kit.to_param)`  
**Replace With**: `fitness_kit_order_url(slug: @kit.slug)`  
**Count**: ~3 occurrences  
**Success Criteria**: All GET tests use `.slug`

---

#### Task 8.3: Update All POST Request Tests
**File**: `test/controllers/orders_controller_test.rb`  
**Action**: Edit  
**Find All**: `create_fitness_kit_order_url(slug: @kit.to_param)`  
**Replace With**: `create_fitness_kit_order_url(slug: @kit.slug)`  
**Count**: ~15 occurrences  
**Success Criteria**: All POST tests use `.slug`

---

### Phase 9: Test Execution (Tasks 26-27)

#### Task 9.1: Run Model Tests
**Command**: `rails test test/models/promise_fitness_kit_test.rb`  
**Expected Result**: All tests pass (0 failures, 0 errors)  
**Success Criteria**: Green test output

---

#### Task 9.2: Run Controller Tests
**Command**: `rails test test/controllers/orders_controller_test.rb`  
**Expected Result**: All tests pass (0 failures, 0 errors)  
**Success Criteria**: Green test output

---

#### Task 9.3: Run Full Test Suite
**Command**: `rails test`  
**Expected Result**: All tests pass across entire application  
**Success Criteria**: 
- 0 failures
- 0 errors
- No skipped tests
- Coverage ≥90%

---

### Phase 10: Manual Validation (Task 28)

#### Task 10.1: Manual Testing Checklist
**Commands**:
1. `rails server`
2. Open browser to `http://localhost:3000`

**Test Scenarios**:
- [ ] Homepage loads successfully
- [ ] Click "Order This Kit" for any kit
- [ ] URL bar shows `/:slug` format (e.g., `/pilates-kit-1`)
- [ ] Order form displays correct kit information
- [ ] Fill form with valid data and unused coupon
- [ ] Submit form
- [ ] Redirects to order confirmation page
- [ ] Order confirmation shows correct details
- [ ] Navigate to `http://localhost:3000/invalid-slug-999`
- [ ] Redirects to homepage
- [ ] Flash message displays: "Fitness kit not found"

**Success Criteria**: All manual test scenarios pass

---

## 📊 Task Dependencies

```
Phase 1 (Database)
  ├─ Task 1.1 → 1.2 → 1.3 → 1.4 → 1.5

Phase 2 (Model) [depends on Phase 1]
  ├─ Task 2.1 → 2.2 → 2.3

Phase 3 (Routes) [can run parallel to Phase 2]
  ├─ Task 3.1 → 3.2 → 3.3

Phase 4 (Controller) [depends on Phase 2, 3]
  ├─ Task 4.1 → 4.2 → 4.3

Phase 5 (Views) [depends on Phase 3]
  ├─ Task 5.1
  └─ Task 5.2

Phase 6 (Fixtures) [depends on Phase 1]
  ├─ Task 6.1 → 6.2

Phase 7 (Model Tests) [depends on Phase 2, 6]
  ├─ Task 7.1
  ├─ Task 7.2
  ├─ Task 7.3
  └─ Task 7.4

Phase 8 (Controller Tests) [depends on Phase 4, 6]
  ├─ Task 8.1 → 8.2 → 8.3

Phase 9 (Test Execution) [depends on Phase 7, 8]
  ├─ Task 9.1 → 9.2 → 9.3

Phase 10 (Manual Testing) [depends on Phase 9]
  └─ Task 10.1
```

---

## ⚡ Quick Reference

**Total Phases**: 10  
**Total Tasks**: 28  
**Critical Path**: Phase 1 → Phase 2 → Phase 4 → Phase 9 → Phase 10  
**Estimated Time**: 2-3 hours

**Parallel Opportunities**:
- Phase 3 (Routes) can run with Phase 2 (Model)
- Phase 5 (Views) can run after Phase 3
- Phase 7 tests can be written while implementing Phases 2-5

---

## 🚦 Implementation Order

**Recommended execution order**:
1. Database (Tasks 1.1-1.5) - 20 min
2. Model (Tasks 2.1-2.3) - 10 min
3. Routes (Tasks 3.1-3.3) - 10 min
4. Controller (Tasks 4.1-4.3) - 10 min
5. Views (Tasks 5.1-5.2) - 5 min
6. Fixtures (Tasks 6.1-6.2) - 5 min
7. Model Tests (Tasks 7.1-7.4) - 20 min
8. Controller Tests (Tasks 8.1-8.3) - 20 min
9. Test Execution (Tasks 9.1-9.3) - 10 min
10. Manual Validation (Task 10.1) - 10 min

---

**Status**: Ready for `/speckit.implement`
