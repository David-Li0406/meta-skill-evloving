# Implementation Tasks: Fitness Kit Ordering System

**Feature ID**: 001-fitness-kit-ordering  
**Status**: Ready for Implementation  
**Created**: 2025-01-XX  
**Estimated Time**: 8-10 hours

---

## Task Execution Instructions

1. Execute tasks in the order listed (respects dependencies)
2. Tasks marked with `[P]` can be done in parallel with adjacent `[P]` tasks
3. Follow test-first development: write test → implement → verify green
4. Check off tasks as completed: `- [ ]` → `- [x]`
5. Run full test suite after each phase
6. Commit after each completed phase

---

## Phase 1: Database Setup

**Estimated Time**: 30 minutes

### Task 1.1: Create PromiseFitnessKit Migration
- [ ] Create migration: `rails generate migration CreatePromiseFitnessKits`
- [ ] File: `db/migrate/YYYYMMDDHHMMSS_create_promise_fitness_kits.rb`
- [ ] Add columns:
  - `t.string :name, null: false`
  - `t.text :description, null: false`
  - `t.timestamps`
- [ ] Add index: `add_index :promise_fitness_kits, :name, unique: true`

### Task 1.2: Create CouponCode Migration
- [ ] Create migration: `rails generate migration CreateCouponCodes`
- [ ] File: `db/migrate/YYYYMMDDHHMMSS_create_coupon_codes.rb`
- [ ] Add columns:
  - `t.string :code, null: false`
  - `t.string :usage, null: false, default: 'unused'`
  - `t.timestamps`
- [ ] Add index: `add_index :coupon_codes, :code, unique: true`
- [ ] Add check constraint: `add_check_constraint :coupon_codes, "usage IN ('unused', 'used')", name: 'usage_check'`

### Task 1.3: Create Order Migration
- [ ] Create migration: `rails generate migration CreateOrders`
- [ ] File: `db/migrate/YYYYMMDDHHMMSS_create_orders.rb`
- [ ] Add columns:
  - `t.references :promise_fitness_kit, null: false, foreign_key: true`
  - `t.references :coupon_code, null: false, foreign_key: true`
  - `t.integer :order_confirmation, null: false`
  - `t.string :first_name, null: false`
  - `t.string :last_name, null: false`
  - `t.string :address1, null: false`
  - `t.string :address2`
  - `t.string :city, null: false`
  - `t.string :state, null: false, limit: 2`
  - `t.string :zip, null: false`
  - `t.string :phone, null: false, limit: 10`
  - `t.string :email, null: false`
  - `t.text :description`
  - `t.timestamps`
- [ ] Add indexes:
  - `add_index :orders, :order_confirmation, unique: true`
  - `add_index :orders, :email`
  - `add_index :orders, :created_at`

### Task 1.4: Run Migrations
- [ ] Run: `rails db:migrate`
- [ ] Verify: `rails db:migrate:status` shows all migrations up
- [ ] Check schema: `cat db/schema.rb` contains all three tables

**Checkpoint**: Database structure created with proper constraints and indexes

---

## Phase 2: Model Tests (Test-First)

**Estimated Time**: 1.5 hours

### Task 2.1: PromiseFitnessKit Model Tests
- [ ] Create file: `test/models/promise_fitness_kit_test.rb`
- [ ] Write tests for:
  - `test "should not save without name"`
  - `test "should not save without description"`
  - `test "should not save duplicate name"`
  - `test "should have many orders"`
  - `test "should not delete kit with associated orders"`
  - `test "ordered_by_name scope returns kits alphabetically"`
  - `test "to_s returns name"`
- [ ] Run tests: `rails test test/models/promise_fitness_kit_test.rb`
- [ ] Expected: All tests FAIL (red)

### Task 2.2: CouponCode Model Tests
- [ ] Create file: `test/models/coupon_code_test.rb`
- [ ] Write tests for:
  - `test "should not save without code"`
  - `test "should not save duplicate code"`
  - `test "should validate case-insensitive uniqueness"`
  - `test "should normalize code to uppercase"`
  - `test "should default usage to unused"`
  - `test "should validate usage inclusion"`
  - `test "unused? returns true for unused coupons"`
  - `test "used? returns true for used coupons"`
  - `test "mark_as_used! changes usage to used"`
  - `test "unused scope returns only unused coupons"`
  - `test "used scope returns only used coupons"`
  - `test "should not delete coupon with associated orders"`
- [ ] Run tests: `rails test test/models/coupon_code_test.rb`
- [ ] Expected: All tests FAIL (red)

### Task 2.3: Order Model Tests (Part 1 - Validations)
- [ ] Create file: `test/models/order_test.rb`
- [ ] Write validation tests:
  - `test "should not save without first_name"`
  - `test "should not save without last_name"`
  - `test "should not save without address1"`
  - `test "should not save without city"`
  - `test "should not save without state"`
  - `test "should not save without zip"`
  - `test "should not save without phone"`
  - `test "should not save without email"`
  - `test "should save without address2 (optional)"`
  - `test "should save without description (optional)"`
  - `test "should validate email format"`
  - `test "should reject invalid email"`
  - `test "should validate state is 2 letters"`
  - `test "should validate state is valid US state"`
  - `test "should reject invalid state code"`
  - `test "should validate zip format 5 digits"`
  - `test "should validate zip format ZIP+4"`
  - `test "should reject invalid zip"`
  - `test "should validate phone is exactly 10 digits"`
  - `test "should reject phone with letters"`
  - `test "should reject phone with wrong length"`
- [ ] Run tests: `rails test test/models/order_test.rb`
- [ ] Expected: All tests FAIL (red)

### Task 2.4: Order Model Tests (Part 2 - Business Logic)
- [ ] Add business logic tests to `test/models/order_test.rb`:
  - `test "should normalize phone to digits only"`
  - `test "should normalize email to lowercase"`
  - `test "should normalize state to uppercase"`
  - `test "should auto-generate order_confirmation"`
  - `test "should increment order_confirmation sequentially"`
  - `test "should validate coupon_code must be unused"`
  - `test "should reject order with used coupon"`
  - `test "should mark coupon as used after order creation"`
  - `test "should rollback coupon if order fails"`
  - `test "formatted_order_confirmation returns 6-digit string"`
  - `test "full_name returns first and last name"`
  - `test "formatted_phone returns formatted phone"`
  - `test "full_address returns complete address"`
  - `test "next_confirmation_number returns next number"`
- [ ] Run tests: `rails test test/models/order_test.rb`
- [ ] Expected: All tests FAIL (red)

**Checkpoint**: All model tests written and failing (red)

---

## Phase 3: Model Implementation

**Estimated Time**: 2 hours

### Task 3.1: Implement PromiseFitnessKit Model
- [ ] Create file: `app/models/promise_fitness_kit.rb`
- [ ] Add class definition: `class PromiseFitnessKit < ApplicationRecord`
- [ ] Add associations: `has_many :orders, dependent: :restrict_with_error`
- [ ] Add validations:
  - `validates :name, presence: true, uniqueness: true`
  - `validates :description, presence: true`
- [ ] Add scope: `scope :ordered_by_name, -> { order(:name) }`
- [ ] Add method: `def to_s; name; end`
- [ ] Run tests: `rails test test/models/promise_fitness_kit_test.rb`
- [ ] Expected: All tests PASS (green)

### Task 3.2: Implement CouponCode Model
- [ ] Create file: `app/models/coupon_code.rb`
- [ ] Add class definition: `class CouponCode < ApplicationRecord`
- [ ] Add associations: `has_many :orders, dependent: :restrict_with_error`
- [ ] Add validations:
  - `validates :code, presence: true, uniqueness: { case_sensitive: false }`
  - `validates :usage, presence: true, inclusion: { in: %w[unused used] }`
- [ ] Add callback: `before_validation :normalize_code`
- [ ] Add scopes:
  - `scope :unused, -> { where(usage: 'unused') }`
  - `scope :used, -> { where(usage: 'used') }`
- [ ] Add methods:
  - `def unused?; usage == 'unused'; end`
  - `def used?; usage == 'used'; end`
  - `def mark_as_used!; update!(usage: 'used'); end`
- [ ] Add private method: `def normalize_code; self.code = code.to_s.upcase.strip if code.present?; end`
- [ ] Run tests: `rails test test/models/coupon_code_test.rb`
- [ ] Expected: All tests PASS (green)

### Task 3.3: Implement Order Model (Part 1 - Setup)
- [ ] Create file: `app/models/order.rb`
- [ ] Add class definition: `class Order < ApplicationRecord`
- [ ] Add associations:
  - `belongs_to :promise_fitness_kit`
  - `belongs_to :coupon_code`
- [ ] Add constant with US states array (50 states + DC)
- [ ] Run tests: `rails test test/models/order_test.rb`
- [ ] Expected: Some tests pass (associations)

### Task 3.4: Implement Order Model (Part 2 - Validations)
- [ ] Add validations to `app/models/order.rb`:
  - `validates :first_name, presence: true`
  - `validates :last_name, presence: true`
  - `validates :address1, presence: true`
  - `validates :city, presence: true`
  - `validates :state, presence: true, inclusion: { in: US_STATES, message: 'must be a valid US state' }`
  - `validates :zip, presence: true, format: { with: /\A\d{5}(-\d{4})?\z/, message: 'must be 5 digits or ZIP+4' }`
  - `validates :phone, presence: true, length: { is: 10, message: 'must be exactly 10 digits' }, format: { with: /\A\d{10}\z/, message: 'must contain only digits' }`
  - `validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP, message: 'must be a valid email' }`
  - `validates :order_confirmation, presence: true, uniqueness: true`
- [ ] Add custom validation: `validate :coupon_code_must_be_unused, on: :create`
- [ ] Run tests: `rails test test/models/order_test.rb`
- [ ] Expected: More tests pass (validations)

### Task 3.5: Implement Order Model (Part 3 - Callbacks & Methods)
- [ ] Add callbacks to `app/models/order.rb`:
  - `before_validation :normalize_attributes`
  - `before_create :generate_order_confirmation`
  - `after_create :mark_coupon_as_used`
- [ ] Add class method: `def self.next_confirmation_number; maximum(:order_confirmation).to_i + 1; end`
- [ ] Add instance methods:
  - `def formatted_order_confirmation; sprintf("%06d", order_confirmation); end`
  - `def full_name; "#{first_name} #{last_name}"; end`
  - `def formatted_phone; "(#{phone[0..2]}) #{phone[3..5]}-#{phone[6..9]}"; end`
  - `def full_address; [address1, address2, "#{city}, #{state} #{zip}"].compact.join("\n"); end`
- [ ] Add private methods:
  - `def normalize_attributes` (normalize state, email, phone, zip)
  - `def generate_order_confirmation` (set order_confirmation)
  - `def coupon_code_must_be_unused` (validation method)
  - `def mark_coupon_as_used` (call coupon.mark_as_used!)
- [ ] Add scope: `scope :recent, -> { order(created_at: :desc) }`
- [ ] Run tests: `rails test test/models/order_test.rb`
- [ ] Expected: All tests PASS (green)

**Checkpoint**: All model tests passing (green), 90%+ coverage on models

---

## Phase 4: Seed Data

**Estimated Time**: 20 minutes

### Task 4.1: Create Seed Data
- [ ] Edit file: `db/seeds.rb`
- [ ] Add development environment check
- [ ] Add code to destroy existing data (development only)
- [ ] Create 3 fitness kits:
  - Beginner Strength Kit
  - Cardio Endurance Kit
  - Flexibility & Recovery Kit
- [ ] Create 10 coupon codes:
  - 5 unused: WELCOME2024, FITNESS50, NEWYEAR, SPRING25, HEALTH100
  - 5 used: USED001, USED002, USED003, USED004, USED005
- [ ] Create 5 sample orders with varied data
- [ ] Add output messages showing counts
- [ ] Run: `rails db:seed`
- [ ] Verify in console:
  - `PromiseFitnessKit.count` → 3
  - `CouponCode.unused.count` → 5
  - `Order.count` → 5

**Checkpoint**: Database populated with sample data

---

## Phase 5: Routes & Controller Tests

**Estimated Time**: 1 hour

### Task 5.1: Define Routes
- [ ] Edit file: `config/routes.rb`
- [ ] Add root route: `root 'home#index'`
- [ ] Add nested resources: `resources :promise_fitness_kits, only: [] do resources :orders, only: [:new, :create]; end`
- [ ] Add orders show route: `resources :orders, only: [:show]`
- [ ] Verify routes: `rails routes | grep -E "(home|order)"`
- [ ] Expected: 4 routes (root, new_order, create_order, show_order)

### Task 5.2: HomeController Tests
- [ ] Create file: `test/controllers/home_controller_test.rb`
- [ ] Write tests:
  - `test "should get index"`
  - `test "should assign promise_fitness_kits"`
  - `test "should order kits by name"`
- [ ] Run tests: `rails test test/controllers/home_controller_test.rb`
- [ ] Expected: All tests FAIL (red)

### Task 5.3: OrdersController Tests (Part 1 - New)
- [ ] Create file: `test/controllers/orders_controller_test.rb`
- [ ] Add setup method with test data (kit, coupon, valid params)
- [ ] Write tests for new action:
  - `test "should get new"`
  - `test "should assign order and fitness kit"`
  - `test "should return 404 for invalid kit"`
- [ ] Run tests: `rails test test/controllers/orders_controller_test.rb`
- [ ] Expected: All tests FAIL (red)

### Task 5.4: OrdersController Tests (Part 2 - Create Success)
- [ ] Add tests for create action (success cases):
  - `test "should create order with valid params"`
  - `test "should redirect to order show on success"`
  - `test "should mark coupon as used after order creation"`
  - `test "should increment order confirmation number"`
  - `test "should set success flash message"`
- [ ] Run tests: `rails test test/controllers/orders_controller_test.rb`
- [ ] Expected: All tests FAIL (red)

### Task 5.5: OrdersController Tests (Part 3 - Create Errors)
- [ ] Add tests for create action (error cases):
  - `test "should not create order with invalid coupon"`
  - `test "should render new with error for invalid coupon"`
  - `test "should not create order with used coupon"`
  - `test "should show specific error for used coupon"`
  - `test "should not create order with missing fields"`
  - `test "should render new with validation errors"`
  - `test "should return 422 for validation errors"`
  - `test "should preserve form data on errors"`
- [ ] Run tests: `rails test test/controllers/orders_controller_test.rb`
- [ ] Expected: All tests FAIL (red)

### Task 5.6: OrdersController Tests (Part 4 - Show)
- [ ] Add tests for show action:
  - `test "should get show"`
  - `test "should assign order"`
  - `test "should return 404 for invalid order"`
- [ ] Run tests: `rails test test/controllers/orders_controller_test.rb`
- [ ] Expected: All tests FAIL (red)

**Checkpoint**: All controller tests written and failing (red)

---

## Phase 6: Controller Implementation

**Estimated Time**: 1 hour

### Task 6.1: Implement HomeController
- [ ] Create file: `app/controllers/home_controller.rb`
- [ ] Add class definition: `class HomeController < ApplicationController`
- [ ] Add index action:
  - Assign `@promise_fitness_kits = PromiseFitnessKit.ordered_by_name`
- [ ] Run tests: `rails test test/controllers/home_controller_test.rb`
- [ ] Expected: All tests PASS (green)

### Task 6.2: Implement OrdersController (Part 1 - Setup)
- [ ] Create file: `app/controllers/orders_controller.rb`
- [ ] Add class definition: `class OrdersController < ApplicationController`
- [ ] Add before_action: `before_action :set_promise_fitness_kit, only: [:new, :create]`
- [ ] Add private method `set_promise_fitness_kit`
- [ ] Add private method `order_params` with strong parameters
- [ ] Run tests: `rails test test/controllers/orders_controller_test.rb`
- [ ] Expected: Some setup tests may pass

### Task 6.3: Implement OrdersController (Part 2 - New Action)
- [ ] Add new action:
  - Initialize `@order = Order.new(promise_fitness_kit: @promise_fitness_kit)`
  - Initialize `@coupon_code = CouponCode.new` (for form)
- [ ] Run tests: `rails test test/controllers/orders_controller_test.rb -n /new/`
- [ ] Expected: New action tests PASS (green)

### Task 6.4: Implement OrdersController (Part 3 - Create Action)
- [ ] Add create action:
  - Initialize `@order = Order.new(order_params)`
  - Set `@order.promise_fitness_kit = @promise_fitness_kit`
  - Find coupon by code from params
  - Validate coupon exists (nil check)
  - Validate coupon is unused
  - Set `@order.coupon_code = coupon`
  - Save order
  - Redirect to `order_path(@order)` on success
  - Render `:new` with status `:unprocessable_entity` on failure
- [ ] Add flash messages for errors
- [ ] Run tests: `rails test test/controllers/orders_controller_test.rb -n /create/`
- [ ] Expected: Create action tests PASS (green)

### Task 6.5: Implement OrdersController (Part 4 - Show Action)
- [ ] Add show action:
  - Assign `@order = Order.find(params[:id])`
- [ ] Run tests: `rails test test/controllers/orders_controller_test.rb -n /show/`
- [ ] Expected: Show action tests PASS (green)

### Task 6.6: Run Full Controller Test Suite
- [ ] Run: `rails test test/controllers/`
- [ ] Expected: All controller tests PASS (green)

**Checkpoint**: All controller tests passing (green)

---

## Phase 7: Views

**Estimated Time**: 1.5 hours

### Task 7.1: Create Application Layout (if needed)
- [ ] Check file exists: `app/views/layouts/application.html.erb`
- [ ] Verify includes:
  - `<%= csrf_meta_tags %>`
  - `<%= csp_meta_tag %>`
  - `<%= stylesheet_link_tag "application" %>`
  - `<%= javascript_importmap_tags %>`
  - Flash message rendering
- [ ] If missing, create basic layout

### Task 7.2: [P] Create Home Index View
- [ ] Create file: `app/views/home/index.html.erb`
- [ ] Add container div
- [ ] Add heading: "Available Fitness Kits"
- [ ] Add empty state check: `if @promise_fitness_kits.empty?`
- [ ] Add empty message: "No fitness kits available at this time."
- [ ] Add else block with iteration over kits
- [ ] For each kit, display:
  - Kit name in heading
  - Kit description in paragraph
  - Link to order form: `link_to 'Order This Kit', new_promise_fitness_kit_order_path(kit)`
- [ ] Add basic CSS classes for styling
- [ ] Test in browser: Visit `http://localhost:3000`
- [ ] Expected: See 3 fitness kits with order buttons

### Task 7.3: [P] Create Orders New View
- [ ] Create directory: `app/views/orders/`
- [ ] Create file: `app/views/orders/new.html.erb`
- [ ] Add container and heading with kit name
- [ ] Add kit description
- [ ] Add `form_with` for order:
  - Set model: `@order`
  - Set url: `promise_fitness_kit_orders_path(@promise_fitness_kit)`
  - Set data: `{ turbo: true }`
- [ ] Add flash error display
- [ ] Add validation errors display
- [ ] Add fieldsets:
  - Personal Information (first_name, last_name, email, phone)
  - Shipping Address (address1, address2, city, state, zip)
  - Coupon Code (text field with name: `order[coupon_code_input]`)
  - Additional Information (description textarea)
- [ ] Add submit button and cancel link
- [ ] Mark required fields with asterisk
- [ ] Add placeholder text for formatting hints
- [ ] Test in browser: Click "Order This Kit"
- [ ] Expected: See complete order form

### Task 7.4: [P] Create Orders Show View
- [ ] Create file: `app/views/orders/show.html.erb`
- [ ] Add container div
- [ ] Add success message section:
  - Heading: "✓ Order Confirmed!"
  - Order confirmation number: `@order.formatted_order_confirmation`
  - Email confirmation message
- [ ] Add order summary section:
  - Heading: "Order Summary"
  - Fitness kit name
  - Shipping address with `full_address`
  - Contact info with `formatted_phone`
  - Order notes (if present)
- [ ] Add link back to home
- [ ] Test in browser: Submit valid order
- [ ] Expected: See confirmation page with order details

### Task 7.5: Add Basic Styling
- [ ] Edit file: `app/assets/stylesheets/application.css` (or create if missing)
- [ ] Add basic styles:
  - Container max-width and centering
  - Form field layout (margin, padding)
  - Button styles (primary and secondary)
  - Alert styles (error and success)
  - Kit card layout
  - Success message styling
- [ ] Test in browser: Refresh pages
- [ ] Expected: Forms and pages look presentable

**Checkpoint**: All views created and working in browser

---

## Phase 8: JavaScript (Stimulus)

**Estimated Time**: 30 minutes

### Task 8.1: Create Phone Format Controller
- [ ] Create directory: `app/javascript/controllers/` (if not exists)
- [ ] Create file: `app/javascript/controllers/phone_format_controller.js`
- [ ] Import Stimulus Controller
- [ ] Define targets: `input`
- [ ] Add connect method with event listener
- [ ] Add format method:
  - Remove non-digits
  - Limit to 10 characters
  - Add dashes: XXX-XXX-XXXX
  - Update input value
- [ ] Register controller in `app/javascript/controllers/index.js` (if needed)

### Task 8.2: Add Phone Controller to Form
- [ ] Edit file: `app/views/orders/new.html.erb`
- [ ] Add to phone field wrapper: `data-controller="phone-format"`
- [ ] Add to phone input: `data: { phone_format_target: 'input' }`
- [ ] Test in browser: Type phone number
- [ ] Expected: Dashes appear automatically as you type

**Checkpoint**: Phone formatting works in real-time

---

## Phase 9: System Tests

**Estimated Time**: 1.5 hours

### Task 9.1: System Test Setup
- [ ] Check file exists: `test/application_system_test_case.rb`
- [ ] Verify driven_by is configured (likely :selenium)
- [ ] Install system test dependencies if needed

### Task 9.2: Happy Path System Test
- [ ] Create file: `test/system/order_placement_test.rb`
- [ ] Add test: `test "successfully placing an order"`
- [ ] Steps:
  - Visit root_path
  - Assert page has "Available Fitness Kits"
  - Click first "Order This Kit" link
  - Assert page has order form
  - Fill in all required fields
  - Fill in coupon code (unused)
  - Click "Place Order"
  - Assert page has "Order Confirmed"
  - Assert page has confirmation number
  - Verify order created in database
  - Verify coupon marked as used
- [ ] Run: `rails test:system test/system/order_placement_test.rb -n /successfully/`
- [ ] Expected: Test PASS (green)

### Task 9.3: Used Coupon System Test
- [ ] Add test: `test "attempting to use an already used coupon"`
- [ ] Steps:
  - Visit order form
  - Fill in all fields
  - Fill in used coupon code
  - Click "Place Order"
  - Assert page has error message
  - Assert message includes "has been used before"
  - Verify no new order created
- [ ] Run: `rails test:system test/system/order_placement_test.rb -n /used/`
- [ ] Expected: Test PASS (green)

### Task 9.4: Invalid Coupon System Test
- [ ] Add test: `test "attempting to use invalid coupon code"`
- [ ] Steps:
  - Visit order form
  - Fill in all fields
  - Fill in non-existent coupon
  - Click "Place Order"
  - Assert page has "Invalid coupon code"
  - Verify no new order created
- [ ] Run: `rails test:system test/system/order_placement_test.rb -n /invalid/`
- [ ] Expected: Test PASS (green)

### Task 9.5: Validation Errors System Test
- [ ] Add test: `test "displaying validation errors for incomplete form"`
- [ ] Steps:
  - Visit order form
  - Fill in only first_name
  - Click "Place Order"
  - Assert page has multiple error messages
  - Assert page has "can't be blank" messages
  - Verify form data preserved
- [ ] Run: `rails test:system test/system/order_placement_test.rb -n /validation/`
- [ ] Expected: Test PASS (green)

### Task 9.6: Phone Formatting System Test
- [ ] Add test: `test "phone number formatting works"`
- [ ] Steps:
  - Visit order form
  - Fill in phone field: "4155551234"
  - Assert field value includes dashes
  - Submit valid order
  - Visit confirmation page
  - Assert phone displays as "(415) 555-1234"
- [ ] Run: `rails test:system test/system/order_placement_test.rb -n /phone/`
- [ ] Expected: Test PASS (green)

### Task 9.7: Run Full System Test Suite
- [ ] Run: `rails test:system`
- [ ] Expected: All system tests PASS (green)

**Checkpoint**: All system tests passing (green)

---

## Phase 10: Quality Assurance

**Estimated Time**: 1 hour

### Task 10.1: Run Full Test Suite
- [ ] Run: `rails test`
- [ ] Expected: All tests pass
- [ ] Check coverage: Should be 90%+ for models and controllers
- [ ] If failures, debug and fix

### Task 10.2: Rubocop Check
- [ ] Run: `rubocop`
- [ ] Fix any offenses
- [ ] Common issues: line length, trailing whitespace, method complexity
- [ ] Run again until clean

### Task 10.3: Check for N+1 Queries
- [ ] Start server: `rails server`
- [ ] Visit homepage
- [ ] Check logs for Bullet warnings
- [ ] Visit order confirmation page
- [ ] Check logs for N+1 queries
- [ ] If warnings, add `.includes()` to queries
- [ ] Expected: No Bullet warnings

### Task 10.4: Manual Browser Testing
- [ ] Follow scenarios in `quickstart.md`:
  - Scenario 1: Happy Path ✅
  - Scenario 2: Used Coupon ❌
  - Scenario 3: Invalid Coupon ❌
  - Scenario 4: Phone Validation 📞
  - Scenario 5: Email Validation 📧
  - Scenario 6: State Validation 🗺️
  - Scenario 7: ZIP Validation 📮
  - Scenario 8: Required Fields 📝
  - Scenario 9: Confirmation Numbers 🔢
- [ ] Open browser console (F12)
- [ ] Check for JavaScript errors
- [ ] Expected: No console errors

### Task 10.5: Database Inspection
- [ ] Open console: `rails console`
- [ ] Check data integrity:
  - `Order.count` matches expected
  - `CouponCode.unused.count` decreases after orders
  - `Order.pluck(:order_confirmation).uniq.count == Order.count` (no duplicates)
  - All orders have associated kit and coupon
  - Phone numbers stored as 10 digits
  - Emails stored lowercase
- [ ] Run: `Order.includes(:promise_fitness_kit, :coupon_code).last`
- [ ] Verify associations load without extra queries

### Task 10.6: Performance Check
- [ ] Check Rails logs for query times
- [ ] Homepage load: Should be < 200ms
- [ ] Order creation: Should be < 500ms
- [ ] If slow, add missing indexes or optimize queries

**Checkpoint**: All quality checks pass

---

## Phase 11: Documentation & Cleanup

**Estimated Time**: 30 minutes

### Task 11.1: Update README (if applicable)
- [ ] Document how to set up the project
- [ ] Document how to seed data
- [ ] Document how to run tests
- [ ] Document available endpoints

### Task 11.2: Verify Acceptance Criteria
- [ ] Review `spec.md` acceptance criteria
- [ ] Check off completed items:
  - [x] Three tables created
  - [x] Foreign keys established
  - [x] All validations working
  - [x] Homepage displays kits
  - [x] Order form functional
  - [x] Coupon validation works
  - [x] Order confirmation auto-generates
  - [x] Success page displays
  - [x] Phone formatting works
  - [x] State validation works
  - [x] 90%+ test coverage
  - [x] No Rubocop violations
  - [x] No N+1 queries
  - [x] Manual QA passed

### Task 11.3: Final Commit
- [ ] Review git status
- [ ] Stage all files: `git add .`
- [ ] Commit: `git commit -m "Complete fitness kit ordering system - Feature 001"`
- [ ] Verify all files committed

**Checkpoint**: Feature complete and documented

---

## Summary

**Total Tasks**: 70+  
**Estimated Time**: 8-10 hours  
**Test Coverage Target**: 90%+

### Phases Overview:
1. ✅ Database Setup (30 min)
2. ✅ Model Tests (1.5 hrs)
3. ✅ Model Implementation (2 hrs)
4. ✅ Seed Data (20 min)
5. ✅ Routes & Controller Tests (1 hr)
6. ✅ Controller Implementation (1 hr)
7. ✅ Views (1.5 hrs)
8. ✅ JavaScript (30 min)
9. ✅ System Tests (1.5 hrs)
10. ✅ Quality Assurance (1 hr)
11. ✅ Documentation (30 min)

### Success Criteria:
- All tests passing (green)
- 90%+ code coverage
- No Rubocop violations
- No N+1 queries
- Manual QA completed
- All acceptance criteria met

---

**Status**: Ready for Implementation  
**Next Step**: Begin Phase 1 - Database Setup