# Task Breakdown: Admin Dashboard

## Overview
Ordered task list for implementing the admin dashboard feature following TDD principles and Rails conventions. Each task includes specific files to create/modify and acceptance criteria.

---

## Phase 1: Foundation & Authentication

### Task 1.1: Create Admin Model
**Dependencies**: None  
**Files**:
- `app/models/admin.rb` (create)
- `test/models/admin_test.rb` (create)
- `test/fixtures/admins.yml` (create)
- `db/migrate/YYYYMMDDHHMMSS_create_admins.rb` (create)

**Implementation**:
1. Generate migration: `rails generate migration CreateAdmins`
2. Define migration:
   - `username:string` (NOT NULL, UNIQUE)
   - `password_digest:string` (NOT NULL)
   - Add unique index on `username`
3. Create Admin model with `has_secure_password`
4. Add validations:
   - username: presence, uniqueness, length 3-50
   - password: length minimum 8 (allow_nil for updates)
5. Write tests:
   - Valid admin creation
   - Username uniqueness enforcement
   - Password length validation
   - Password authentication via bcrypt
6. Run migration: `rails db:migrate`

**Acceptance**:
- [ ] Migration creates admins table with correct schema
- [ ] Admin.create! with valid data succeeds
- [ ] Duplicate username fails validation
- [ ] Short password fails validation
- [ ] admin.authenticate(password) works correctly
- [ ] All tests pass

---

### Task 1.2: Update Seeds for Admin Users
**Dependencies**: Task 1.1  
**Files**:
- `db/seeds.rb` (modify)

**Implementation**:
1. Add section for admin users:
   ```ruby
   puts "Creating admin users..."
   Admin.create!(username: 'admin', password: 'password123', password_confirmation: 'password123')
   Admin.create!(username: 'testadmin', password: 'testpass', password_confirmation: 'testpass')
   puts "Created #{Admin.count} admin users"
   ```
2. Run seeds: `rails db:seed`
3. Verify in console: `rails c` → `Admin.all`

**Acceptance**:
- [ ] Seeds run without errors
- [ ] Two admin users exist in database
- [ ] Passwords are hashed (password_digest present)
- [ ] Can authenticate with test credentials

---

### Task 1.3: Create Admin::BaseController
**Dependencies**: Task 1.1  
**Files**:
- `app/controllers/admin/base_controller.rb` (create)
- `test/controllers/admin/base_controller_test.rb` (create)

**Implementation**:
1. Create `app/controllers/admin/` directory
2. Create BaseController:
   - Inherit from ApplicationController
   - Set layout to 'admin'
   - Add `before_action :require_admin`
   - Define `current_admin` method (checks session[:admin_id])
   - Define `require_admin` (redirect if not authenticated)
   - Add helper_method :current_admin
3. Write tests:
   - Unauthenticated access redirects to login
   - Authenticated access allows through
   - current_admin returns correct admin

**Acceptance**:
- [ ] BaseController requires authentication
- [ ] Redirect path is `/admin/login`
- [ ] current_admin helper available in views
- [ ] All tests pass

---

### Task 1.4: Create Admin Sessions Controller (Login/Logout)
**Dependencies**: Task 1.3  
**Files**:
- `app/controllers/admin/sessions_controller.rb` (create)
- `app/views/admin/sessions/new.html.erb` (create)
- `test/controllers/admin/sessions_controller_test.rb` (create)
- `config/routes.rb` (modify)

**Implementation**:
1. Create SessionsController (inherits from ApplicationController, NOT BaseController):
   - `new` action: render login form
   - `create` action: authenticate and set session
   - `destroy` action: clear session, redirect to root
2. Add routes:
   ```ruby
   namespace :admin do
     get 'login', to: 'sessions#new'
     post 'login', to: 'sessions#create'
     delete 'logout', to: 'sessions#destroy'
   end
   ```
3. Create login form view:
   - Username field
   - Password field (type: password)
   - Submit button
   - Use form_with, disable Turbo for initial implementation
4. Session logic:
   - Set `session[:admin_id]` on success
   - Set `session[:admin_expires_at] = 12.hours.from_now`
   - Redirect to admin dashboard
   - Show flash messages for errors
5. Write tests:
   - GET /admin/login shows form
   - POST with valid credentials creates session
   - POST with invalid credentials shows error
   - Already logged in redirects to dashboard
   - DELETE /admin/logout clears session

**Acceptance**:
- [ ] Can access /admin/login
- [ ] Form submits to correct route
- [ ] Valid login creates session and redirects
- [ ] Invalid login shows error message
- [ ] Logout clears session
- [ ] All tests pass

---

### Task 1.5: Add Session Timeout Middleware
**Dependencies**: Task 1.4  
**Files**:
- `app/middleware/admin_session_timeout.rb` (create)
- `config/application.rb` (modify)
- `test/middleware/admin_session_timeout_test.rb` (create)

**Implementation**:
1. Create middleware class:
   - Check if `session[:admin_expires_at]` exists
   - If expired, clear admin session
   - If valid, refresh expiration (sliding window)
2. Register middleware in `config/application.rb`:
   ```ruby
   config.middleware.use AdminSessionTimeout
   ```
3. Write tests:
   - Expired session clears admin_id
   - Valid session refreshes expiration
   - Activity within 12 hours extends session

**Acceptance**:
- [ ] Session expires after 12 hours of inactivity
- [ ] Activity refreshes expiration time
- [ ] Expired users redirected to login
- [ ] All tests pass

---

### Task 1.6: Create Admin Layout
**Dependencies**: None (can be parallel)  
**Files**:
- `app/views/layouts/admin.html.erb` (create)
- `app/assets/stylesheets/admin.css` (create, optional)

**Implementation**:
1. Create admin layout:
   - Copy structure from application.html.erb
   - Add admin-specific header with:
     - "PromiseKits Admin" branding
     - Navigation links (Dashboard, Coupon Codes, Orders)
     - Current admin username display
     - Logout button
   - Add flash message display
   - Add distinct styling/classes for admin area
2. Style admin area (basic):
   - Different header color/style
   - Admin-specific navigation
   - Form styles
   - Table styles for lists

**Acceptance**:
- [ ] Layout includes admin navigation
- [ ] Logout button works
- [ ] Flash messages display
- [ ] Visually distinct from public site

**Checkpoint**: Can log in, see admin layout, log out

---

## Phase 2: Coupon Code Management

### Task 2.1: Update CouponCode Model
**Dependencies**: None  
**Files**:
- `app/models/coupon_code.rb` (modify)
- `test/models/coupon_code_test.rb` (modify)
- `db/migrate/YYYYMMDDHHMMSS_add_indexes_to_coupon_codes.rb` (create)

**Implementation**:
1. Create migration for index:
   ```ruby
   add_index :coupon_codes, :usage unless index_exists?(:coupon_codes, :usage)
   ```
2. Update model validations:
   - Change code format validation to `/\ASK\d+[A-Z]{3}\z/`
3. Add class method `generate_next_code`:
   - Query all codes, extract integers with regex
   - Find max integer (default 999 if none exist)
   - Increment by 1
   - Generate 3 random letters (A-Z)
   - Return formatted string
4. Add scopes:
   - `unused` -> `where(usage: 'unused')`
   - `used` -> `where(usage: 'used')`
   - `by_cursor(cursor, direction)` for pagination
5. Add `before_destroy :check_not_used` callback:
   - Check if usage == 'used'
   - Add error and throw :abort if used
6. Write tests:
   - Format validation (valid: SK1000AAA, invalid: TEST1)
   - generate_next_code increments correctly
   - generate_next_code starts at SK1000AAA if empty
   - Cannot delete used coupon
   - Can delete unused coupon
   - Scopes filter correctly
   - Cursor pagination works

**Acceptance**:
- [ ] Migration adds usage index
- [ ] Format validation enforces SK[number][3letters]
- [ ] generate_next_code returns correct format
- [ ] Sequential number increments properly
- [ ] Deletion protection works for used coupons
- [ ] All tests pass

---

### Task 2.2: Update Seeds for New Coupon Format
**Dependencies**: Task 2.1  
**Files**:
- `db/seeds.rb` (modify)

**Implementation**:
1. Clear existing coupon codes section
2. Add new format codes:
   ```ruby
   puts "Creating coupon codes with new format..."
   CouponCode.destroy_all
   
   codes = [
     { code: 'SK1000AAA', usage: 'unused' },
     { code: 'SK1001BBB', usage: 'unused' },
     { code: 'SK1002CCC', usage: 'unused' },
     { code: 'SK1003DDD', usage: 'unused' },
     { code: 'SK1004EEE', usage: 'unused' },
     { code: 'SK1005FFF', usage: 'unused' },
     { code: 'SK1006GGG', usage: 'unused' },
     { code: 'SK1007HHH', usage: 'unused' }
   ]
   
   codes.each { |attrs| CouponCode.create!(attrs) }
   ```
3. Update order seeds to use new coupon codes (SK1003DDD, SK1004EEE, SK1005FFF)
4. Run: `rails db:reset`

**Acceptance**:
- [ ] Seeds create coupons in new format
- [ ] Orders reference new format coupons
- [ ] No errors during seeding
- [ ] CouponCode.count returns 8

---

### Task 2.3: Create Admin::CouponCodesController
**Dependencies**: Task 2.1, 1.3  
**Files**:
- `app/controllers/admin/coupon_codes_controller.rb` (create)
- `test/controllers/admin/coupon_codes_controller_test.rb` (create)

**Implementation**:
1. Create controller inheriting from Admin::BaseController
2. Define constant `PER_PAGE = 25`
3. Implement `index` action:
   - Load all coupons
   - Filter by status if params[:status] present
   - Search by code if params[:search] present
   - Apply cursor pagination with params[:cursor] and params[:direction]
   - Eager load to prevent N+1
   - Set @has_more flag (fetch PER_PAGE + 1)
4. Implement `create` action:
   - Call CouponCode.generate_next_code
   - Create new coupon with generated code, usage: 'unused'
   - Redirect with success/error message
5. Implement `destroy` action:
   - Find coupon by id
   - Attempt destroy (callback handles validation)
   - Redirect with success/error message
6. Write tests:
   - Index requires authentication
   - Index loads coupons
   - Filter by status works
   - Search by code works
   - Cursor pagination works
   - Create generates and saves new code
   - Destroy unused succeeds
   - Destroy used fails with error

**Acceptance**:
- [ ] All actions require admin authentication
- [ ] Index shows coupon list
- [ ] Filters and search work correctly
- [ ] Pagination maintains state
- [ ] Create generates sequential codes
- [ ] Delete protection works
- [ ] All tests pass

---

### Task 2.4: Create Coupon Code Views
**Dependencies**: Task 2.3  
**Files**:
- `app/views/admin/coupon_codes/index.html.erb` (create)
- `app/views/admin/coupon_codes/_coupon.html.erb` (create)
- `app/views/admin/shared/_cursor_pagination.html.erb` (create)

**Implementation**:
1. Create index view:
   - Page title "Coupon Codes"
   - Filter buttons: All, Unused, Used (links with ?status=)
   - Search form (text input + submit)
   - Create new coupon button (form POST to create action)
   - Table with columns: Code, Status, Associated Order, Actions
   - Render coupon partial for each record
   - Include pagination partial
2. Create coupon partial:
   - Display code, usage status
   - If used, show link to associated order
   - Delete button (only if unused)
   - Use Turbo Frame for inline updates (future)
3. Create pagination partial:
   - Previous button (disabled if first page)
   - Next button (disabled if no more)
   - Pass cursor from first/last record IDs

**Acceptance**:
- [ ] Index page displays coupon list
- [ ] Filter buttons work
- [ ] Search form works
- [ ] Create button generates new coupon
- [ ] Delete button shows for unused only
- [ ] Pagination links work
- [ ] Mobile responsive

---

### Task 2.5: System Test for Coupon Management
**Dependencies**: Task 2.4  
**Files**:
- `test/system/admin/coupon_management_test.rb` (create)

**Implementation**:
1. Write system tests for full workflows:
   - Admin logs in
   - Creates new coupon code
   - Verifies code follows format SK[num][3letters]
   - Filters by unused status
   - Searches for specific code
   - Attempts to delete unused (succeeds)
   - Attempts to delete used (fails with error)
   - Navigates through pagination

**Acceptance**:
- [ ] All workflows complete successfully
- [ ] Error messages display correctly
- [ ] Pagination works end-to-end
- [ ] Tests pass

**Checkpoint**: Can manage coupon codes from UI

---

## Phase 3: Order Viewing

### Task 3.1: Update Order Model
**Dependencies**: None  
**Files**:
- `app/models/order.rb` (modify)
- `test/models/order_test.rb` (modify)
- `db/migrate/YYYYMMDDHHMMSS_add_indexes_to_orders.rb` (create)

**Implementation**:
1. Create migration:
   ```ruby
   add_index :orders, :created_at
   add_index :orders, [:created_at, :id], name: 'index_orders_on_created_at_and_id'
   ```
2. Add scopes:
   - `newest_first` -> `order(created_at: :desc)`
   - `by_cursor(cursor, direction)` using created_at comparison
3. Add class method `search(term)`:
   - Return all if term blank
   - Search first_name, last_name, email, coupon_code.code
   - Use LIKE with wildcards
   - Join with coupon_codes table
4. Write tests:
   - newest_first orders by created_at desc
   - search finds by name
   - search finds by email
   - search finds by coupon code
   - cursor pagination works

**Acceptance**:
- [ ] Migration adds indexes
- [ ] newest_first scope works
- [ ] search method finds orders correctly
- [ ] Cursor pagination works
- [ ] All tests pass

---

### Task 3.2: Create Admin::OrdersController
**Dependencies**: Task 3.1, 1.3  
**Files**:
- `app/controllers/admin/orders_controller.rb` (create)
- `test/controllers/admin/orders_controller_test.rb` (create)

**Implementation**:
1. Create controller inheriting from Admin::BaseController
2. Define constant `PER_PAGE = 25`
3. Implement `index` action:
   - Load orders with includes for associations
   - Apply newest_first scope
   - Search if params[:search] present
   - Apply cursor pagination
   - Set @has_more flag
4. Implement `show` action:
   - Find order by ID
   - Eager load associations
5. Write tests:
   - Index requires authentication
   - Index loads orders newest first
   - Search works correctly
   - Pagination works
   - Show displays order details
   - All tests pass

**Acceptance**:
- [ ] Index shows order list
- [ ] Orders sorted newest first
- [ ] Search functionality works
- [ ] Pagination works
- [ ] Show page displays full details
- [ ] No N+1 queries (check with Bullet)
- [ ] All tests pass

---

### Task 3.3: Create Order Views
**Dependencies**: Task 3.2  
**Files**:
- `app/views/admin/orders/index.html.erb` (create)
- `app/views/admin/orders/show.html.erb` (create)
- `app/views/admin/orders/_order.html.erb` (create)

**Implementation**:
1. Create index view:
   - Page title "Orders"
   - Search form (text input + submit)
   - Table with columns: Order ID, Customer, Kit, Coupon, Date
   - Each row links to show page
   - Render order partial for each record
   - Include pagination partial
2. Create order partial:
   - Display order summary info
   - Click to view details
3. Create show view:
   - Order ID and date
   - Customer information section (name, email, phone, address)
   - Order details section (kit, coupon code)
   - Special instructions (if any)
   - Back to list link

**Acceptance**:
- [ ] Index displays order list
- [ ] Search form works
- [ ] Clicking order goes to details
- [ ] Show page displays all information
- [ ] Navigation works
- [ ] Mobile responsive

---

### Task 3.4: System Test for Order Viewing
**Dependencies**: Task 3.3  
**Files**:
- `test/system/admin/order_viewing_test.rb` (create)

**Implementation**:
1. Write system tests:
   - Admin logs in
   - Views order list
   - Searches for customer by name
   - Searches by email
   - Searches by coupon code
   - Clicks order to view details
   - Verifies all information displayed
   - Navigates through pagination

**Acceptance**:
- [ ] All workflows complete successfully
- [ ] Search returns correct results
- [ ] Order details show correctly
- [ ] Tests pass

**Checkpoint**: Can view and search orders from UI

---

## Phase 4: Dashboard & Statistics

### Task 4.1: Create Admin::DashboardController
**Dependencies**: Task 1.3  
**Files**:
- `app/controllers/admin/dashboard_controller.rb` (create)
- `test/controllers/admin/dashboard_controller_test.rb` (create)
- `config/routes.rb` (modify)

**Implementation**:
1. Create controller inheriting from Admin::BaseController
2. Implement `index` action:
   - Calculate total orders count
   - Calculate orders grouped by kit name
   - Calculate total coupons and unused coupons
   - Load 5 most recent orders
3. Add route:
   ```ruby
   namespace :admin do
     root to: 'dashboard#index', as: :dashboard
   end
   ```
4. Write tests:
   - Requires authentication
   - Loads statistics correctly
   - Shows recent orders

**Acceptance**:
- [ ] /admin redirects to dashboard
- [ ] Dashboard loads statistics
- [ ] No N+1 queries
- [ ] All tests pass

---

### Task 4.2: Create Dashboard View
**Dependencies**: Task 4.1  
**Files**:
- `app/views/admin/dashboard/index.html.erb` (create)

**Implementation**:
1. Create dashboard view:
   - Welcome message with admin username
   - Statistics cards:
     - Total orders
     - Total coupons
     - Unused coupons
   - Orders by kit breakdown (table or list)
   - Recent orders section (mini table)
   - Quick links to main sections

**Acceptance**:
- [ ] Dashboard shows statistics
- [ ] All numbers are accurate
- [ ] Links navigate correctly
- [ ] Visually organized and clear

---

### Task 4.3: System Test for Dashboard
**Dependencies**: Task 4.2  
**Files**:
- `test/system/admin/dashboard_test.rb` (create)

**Implementation**:
1. Write system test:
   - Admin logs in
   - Sees dashboard with correct stats
   - Clicks links to navigate to sections
   - Returns to dashboard

**Acceptance**:
- [ ] Dashboard displays on login
- [ ] Statistics are correct
- [ ] Navigation works
- [ ] Test passes

**Checkpoint**: Dashboard shows admin overview

---

## Phase 5: Password Management

### Task 5.1: Create Admin::PasswordsController
**Dependencies**: Task 1.3  
**Files**:
- `app/controllers/admin/passwords_controller.rb` (create)
- `test/controllers/admin/passwords_controller_test.rb` (create)
- `config/routes.rb` (modify)

**Implementation**:
1. Create controller inheriting from Admin::BaseController
2. Implement `edit` action:
   - Set @admin = current_admin
3. Implement `update` action:
   - Verify current password
   - Check new password matches confirmation
   - Update password if valid
   - Show success message, remain on dashboard
   - Show errors if invalid
4. Add route:
   ```ruby
   namespace :admin do
     resource :password, only: [:edit, :update]
   end
   ```
5. Write tests:
   - Requires authentication
   - GET edit shows form
   - POST update with correct current password succeeds
   - POST update with incorrect current password fails
   - POST update with mismatched confirmation fails
   - POST update with short password fails
   - Session persists after password change

**Acceptance**:
- [ ] Edit page shows form
- [ ] Correct password change succeeds
- [ ] Invalid changes show errors
- [ ] Admin remains logged in
- [ ] All tests pass

---

### Task 5.2: Create Password Change View
**Dependencies**: Task 5.1  
**Files**:
- `app/views/admin/passwords/edit.html.erb` (create)

**Implementation**:
1. Create form:
   - Current password field (password type)
   - New password field (password type)
   - Confirm new password field (password type)
   - Submit button
   - Cancel link (back to dashboard)
   - Display validation errors

**Acceptance**:
- [ ] Form displays correctly
- [ ] Fields are password type (hidden)
- [ ] Submit works
- [ ] Errors display clearly
- [ ] Mobile responsive

---

### Task 5.3: System Test for Password Change
**Dependencies**: Task 5.2  
**Files**:
- `test/system/admin/password_change_test.rb` (create)

**Implementation**:
1. Write system test:
   - Admin logs in
   - Navigates to password change page
   - Enters incorrect current password (sees error)
   - Enters correct current password
   - Enters mismatched new passwords (sees error)
   - Enters matching new passwords (succeeds)
   - Logs out and logs back in with new password

**Acceptance**:
- [ ] Full workflow completes
- [ ] Errors display correctly
- [ ] New password works for login
- [ ] Test passes

**Checkpoint**: Admin can change own password

---

## Phase 6: Polish & Final Testing

### Task 6.1: Add Link to Admin in Public Layout
**Dependencies**: None  
**Files**:
- `app/views/layouts/application.html.erb` (modify, optional)

**Implementation**:
1. Add subtle link to /admin/login in footer or header
2. Style as small/discrete link

**Acceptance**:
- [ ] Link exists but not prominent
- [ ] Navigates to admin login

---

### Task 6.2: Comprehensive System Tests
**Dependencies**: All previous tasks  
**Files**:
- `test/system/admin/full_workflow_test.rb` (create)

**Implementation**:
1. Write end-to-end test covering:
   - Login
   - View dashboard
   - Create 3 coupon codes
   - Filter coupons by unused
   - Search for specific coupon
   - View orders
   - Search for order by customer name
   - View order details
   - Change password
   - Logout
   - Login with new password

**Acceptance**:
- [ ] Complete workflow passes
- [ ] No JavaScript errors
- [ ] No broken links

---

### Task 6.3: Security Audit
**Dependencies**: All previous tasks  
**Files**:
- N/A (review only)

**Checklist**:
- [ ] All admin routes require authentication
- [ ] Passwords stored as bcrypt hashes
- [ ] No passwords in logs or error messages
- [ ] CSRF protection enabled on all forms
- [ ] SQL injection prevented (parameterized queries)
- [ ] XSS prevented (ERB escaping)
- [ ] Session timeout works (12 hours)
- [ ] Session cookies are HTTP-only and encrypted
- [ ] Strong parameters used in all controllers

---

### Task 6.4: Performance Testing
**Dependencies**: All previous tasks  
**Files**:
- N/A (review only)

**Checklist**:
- [ ] No N+1 queries (run Bullet gem if available)
- [ ] All foreign keys indexed
- [ ] created_at indexed for sorting
- [ ] usage indexed for filtering
- [ ] Eager loading used in list views (includes)
- [ ] Pagination limits large result sets
- [ ] Dashboard queries under 50ms

---

### Task 6.5: Accessibility & UX Polish
**Dependencies**: All previous tasks  
**Files**:
- Various view files (modify)
- `app/assets/stylesheets/admin.css` (modify)

**Implementation**:
1. Add proper HTML semantics
2. Add ARIA labels where needed
3. Ensure keyboard navigation works
4. Add loading states for forms
5. Improve error message clarity
6. Add confirmation dialogs for destructive actions (delete)
7. Ensure mobile responsive design
8. Test in multiple browsers

**Checklist**:
- [ ] Forms have proper labels
- [ ] Buttons have clear text/icons
- [ ] Error messages are helpful
- [ ] Success messages are visible
- [ ] Tables are responsive
- [ ] Works on mobile devices
- [ ] Works in Chrome, Firefox, Safari

---

### Task 6.6: Documentation
**Dependencies**: All previous tasks  
**Files**:
- `specs/004-admin-dashboard/IMPLEMENTATION_SUMMARY.md` (create)
- `README.md` (update, optional)

**Implementation**:
1. Document:
   - How to create new admin users
   - How to access admin area
   - Coupon code format and generation logic
   - Cursor pagination implementation
   - Session timeout behavior
2. Update README with admin section if needed

**Acceptance**:
- [ ] Summary document created
- [ ] Clear instructions for creating admins
- [ ] Technical details documented

---

## Final Verification

### All Acceptance Criteria from Spec
- [ ] Admin login page exists at `/admin/login`
- [ ] Unauthenticated users redirected to login
- [ ] Valid credentials grant access
- [ ] Invalid credentials show error
- [ ] Logout functionality works
- [ ] Admin session persists across requests
- [ ] Admin can view coupon codes list with pagination
- [ ] Coupon list shows code, status, order ID
- [ ] Admin can create new coupon code (auto-generated)
- [ ] New codes follow SK[integer][3letters] format
- [ ] System finds highest integer and increments
- [ ] New codes default to 'unused' status
- [ ] Admin can delete unused coupon codes
- [ ] Cannot delete used coupon codes (error shown)
- [ ] Filter by status works (all/unused/used)
- [ ] Search by code text works
- [ ] Cursor pagination works for coupons
- [ ] Admin can view orders list (newest first)
- [ ] Order list uses cursor pagination
- [ ] Order list shows ID, customer, kit, coupon, date
- [ ] Orders sorted by created_at descending
- [ ] Admin can view individual order details
- [ ] Order details show complete information
- [ ] Search works for name, email, coupon code
- [ ] Dashboard shows summary statistics
- [ ] Admin can change own password
- [ ] Password change requires current password
- [ ] New password must meet requirements (8+ chars)
- [ ] Success message after password change
- [ ] Admin remains logged in after password change
- [ ] Admin area has distinct visual identity
- [ ] Forms have proper validation with errors
- [ ] Success messages appear after actions
- [ ] Navigation between sections works
- [ ] Mobile-responsive design
- [ ] Admin credentials stored securely (bcrypt)
- [ ] CSRF protection enabled
- [ ] Admin routes require authentication
- [ ] Non-admin users cannot access
- [ ] Session timeout after 12 hours

### Test Coverage
- [ ] All model tests pass
- [ ] All controller tests pass
- [ ] All system tests pass
- [ ] Test coverage >= 90%

### Performance
- [ ] No N+1 queries
- [ ] All queries under 50ms
- [ ] Page loads under 200ms

---

**Total Estimated Tasks**: 29  
**Estimated Time**: 10-14 hours  
**Priority**: High  
**Feature ID**: 004-admin-dashboard