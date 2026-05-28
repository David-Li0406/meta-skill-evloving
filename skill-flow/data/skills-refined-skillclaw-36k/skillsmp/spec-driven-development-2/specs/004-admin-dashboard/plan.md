# Implementation Plan: Admin Dashboard

## Overview
Build a secure admin dashboard for PromiseKits using Rails 8 conventions, Hotwire for interactivity, and bcrypt for authentication. The admin area will manage coupon codes (with auto-generation) and view orders with cursor-based pagination for performance.

## Technical Stack

### Core Framework
- **Ruby on Rails 8.0+** - Following Rails conventions
- **Ruby 3.2+** - Latest stable Ruby
- **SQLite** - Existing database (development/production)

### Authentication
- **bcrypt** - Password hashing (built into Rails via `has_secure_password`)
- **Session-based authentication** - Rails encrypted cookies
- **No external auth gems** - Keep it simple, Rails native

### Frontend
- **Hotwire Turbo Frames** - Partial page updates (forms, lists)
- **Hotwire Turbo Streams** - Real-time updates (optional for future)
- **Stimulus.js** - Minimal JavaScript (form validation, UX enhancements)
- **Tailwind CSS** - Styling (assuming current project uses this)

### Pagination
- **Pagy gem** - Cursor-based pagination support
- Alternative: Custom cursor pagination implementation
- Cursor field: `id` (primary key) for deterministic ordering

### Testing
- **Minitest** - Rails default testing framework
- **System tests** - Full workflow testing with Capybara
- **Fixtures** - Sample data for tests

## Architecture

### Models

#### 1. Admin (new model)
```ruby
# app/models/admin.rb
class Admin < ApplicationRecord
  has_secure_password
  
  validates :username, presence: true, uniqueness: true, length: { minimum: 3, maximum: 50 }
  validates :password, length: { minimum: 8 }, allow_nil: true
  
  # No associations needed (not tracking attribution)
end
```

**Migration:**
```ruby
create_table :admins do |t|
  t.string :username, null: false, index: { unique: true }
  t.string :password_digest, null: false
  t.timestamps
end
```

#### 2. CouponCode (modifications)
```ruby
# app/models/coupon_code.rb
class CouponCode < ApplicationRecord
  belongs_to :order, optional: true
  
  validates :code, presence: true, 
                   uniqueness: true,
                   format: { with: /\ASK\d+[A-Z]{3}\z/, message: "must follow format SK[number][3 letters]" }
  validates :usage, presence: true, inclusion: { in: %w[unused used] }
  
  scope :unused, -> { where(usage: 'unused') }
  scope :used, -> { where(usage: 'used') }
  scope :by_cursor, ->(cursor, direction = :next) {
    if cursor.present?
      if direction == :next
        where('id > ?', cursor)
      else
        where('id < ?', cursor)
      end
    else
      all
    end
  }
  
  # Auto-generate next sequential code
  def self.generate_next_code
    # Extract integers from existing codes, find max
    max_number = CouponCode.pluck(:code)
                           .map { |code| code.match(/SK(\d+)/)[1].to_i }
                           .max || 999 # Start at 1000 if none exist
    
    next_number = max_number + 1
    random_letters = 3.times.map { ('A'..'Z').to_a.sample }.join
    
    "SK#{next_number}#{random_letters}"
  end
  
  # Prevent deletion if associated with order
  before_destroy :check_not_used
  
  private
  
  def check_not_used
    if used?
      errors.add(:base, "Cannot delete coupon code associated with orders")
      throw(:abort)
    end
  end
end
```

**Migration (modify existing):**
```ruby
# Add index for pagination performance
add_index :coupon_codes, :id
add_index :coupon_codes, :usage
add_index :coupon_codes, :code # Should already exist
```

#### 3. Order (modifications)
```ruby
# app/models/order.rb
class Order < ApplicationRecord
  belongs_to :promise_fitness_kit
  belongs_to :coupon_code
  
  # Existing validations...
  
  scope :newest_first, -> { order(created_at: :desc) }
  scope :by_cursor, ->(cursor, direction = :next) {
    if cursor.present?
      if direction == :next
        where('created_at < ?', Order.find(cursor).created_at)
      else
        where('created_at > ?', Order.find(cursor).created_at)
      end
    else
      all
    end
  }
  
  # Search across multiple fields
  def self.search(term)
    return all if term.blank?
    
    joins(:coupon_code)
      .where(
        "first_name LIKE ? OR last_name LIKE ? OR email LIKE ? OR coupon_codes.code LIKE ?",
        "%#{term}%", "%#{term}%", "%#{term}%", "%#{term}%"
      )
  end
end
```

### Controllers

#### Admin Namespace Structure
```
app/controllers/
├── admin/
│   ├── base_controller.rb          # Authentication & authorization
│   ├── sessions_controller.rb      # Login/logout
│   ├── dashboard_controller.rb     # Admin homepage with stats
│   ├── coupon_codes_controller.rb  # Coupon CRUD
│   ├── orders_controller.rb        # Order viewing & search
│   └── passwords_controller.rb     # Password change
```

#### 1. Admin::BaseController
```ruby
# app/controllers/admin/base_controller.rb
class Admin::BaseController < ApplicationController
  before_action :require_admin
  layout 'admin'
  
  private
  
  def require_admin
    unless current_admin
      redirect_to admin_login_path, alert: "Please log in to access admin area"
    end
  end
  
  def current_admin
    @current_admin ||= Admin.find_by(id: session[:admin_id]) if session[:admin_id]
  end
  helper_method :current_admin
end
```

#### 2. Admin::SessionsController
```ruby
# app/controllers/admin/sessions_controller.rb
class Admin::SessionsController < ApplicationController
  layout 'admin'
  
  def new
    # Login form
    redirect_to admin_dashboard_path if current_admin
  end
  
  def create
    admin = Admin.find_by(username: params[:username])
    
    if admin&.authenticate(params[:password])
      session[:admin_id] = admin.id
      session[:admin_expires_at] = 12.hours.from_now
      redirect_to admin_dashboard_path, notice: "Welcome back, #{admin.username}!"
    else
      flash.now[:alert] = "Invalid username or password"
      render :new, status: :unprocessable_entity
    end
  end
  
  def destroy
    session[:admin_id] = nil
    session[:admin_expires_at] = nil
    redirect_to root_path, notice: "Logged out successfully"
  end
  
  private
  
  def current_admin
    @current_admin ||= Admin.find_by(id: session[:admin_id]) if session[:admin_id]
  end
  helper_method :current_admin
end
```

#### 3. Admin::DashboardController
```ruby
# app/controllers/admin/dashboard_controller.rb
class Admin::DashboardController < Admin::BaseController
  def index
    @total_orders = Order.count
    @orders_by_kit = Order.joins(:promise_fitness_kit)
                          .group('promise_fitness_kits.name')
                          .count
    @total_coupons = CouponCode.count
    @unused_coupons = CouponCode.unused.count
    @recent_orders = Order.newest_first.limit(5)
  end
end
```

#### 4. Admin::CouponCodesController
```ruby
# app/controllers/admin/coupon_codes_controller.rb
class Admin::CouponCodesController < Admin::BaseController
  PER_PAGE = 25
  
  def index
    @coupons = CouponCode.all
    
    # Filter by status
    @coupons = @coupons.send(params[:status]) if params[:status].in?(['unused', 'used'])
    
    # Search
    @coupons = @coupons.where('code LIKE ?', "%#{params[:search]}%") if params[:search].present?
    
    # Cursor pagination
    @coupons = @coupons.by_cursor(params[:cursor], params[:direction] || :next)
                       .order(:id)
                       .limit(PER_PAGE + 1) # +1 to check if more exist
    
    @has_more = @coupons.size > PER_PAGE
    @coupons = @coupons.first(PER_PAGE)
  end
  
  def create
    code = CouponCode.generate_next_code
    @coupon = CouponCode.new(code: code, usage: 'unused')
    
    if @coupon.save
      redirect_to admin_coupon_codes_path, notice: "Coupon code #{code} created successfully"
    else
      redirect_to admin_coupon_codes_path, alert: "Error creating coupon: #{@coupon.errors.full_messages.join(', ')}"
    end
  end
  
  def destroy
    @coupon = CouponCode.find(params[:id])
    
    if @coupon.destroy
      redirect_to admin_coupon_codes_path, notice: "Coupon code deleted successfully"
    else
      redirect_to admin_coupon_codes_path, alert: @coupon.errors.full_messages.join(', ')
    end
  end
end
```

#### 5. Admin::OrdersController
```ruby
# app/controllers/admin/orders_controller.rb
class Admin::OrdersController < Admin::BaseController
  PER_PAGE = 25
  
  def index
    @orders = Order.includes(:promise_fitness_kit, :coupon_code).newest_first
    
    # Search
    @orders = @orders.search(params[:search]) if params[:search].present?
    
    # Cursor pagination
    @orders = @orders.by_cursor(params[:cursor], params[:direction] || :next)
                     .limit(PER_PAGE + 1)
    
    @has_more = @orders.size > PER_PAGE
    @orders = @orders.first(PER_PAGE)
  end
  
  def show
    @order = Order.includes(:promise_fitness_kit, :coupon_code).find(params[:id])
  end
end
```

#### 6. Admin::PasswordsController
```ruby
# app/controllers/admin/passwords_controller.rb
class Admin::PasswordsController < Admin::BaseController
  def edit
    @admin = current_admin
  end
  
  def update
    @admin = current_admin
    
    if @admin.authenticate(params[:current_password])
      if params[:password] == params[:password_confirmation]
        if @admin.update(password: params[:password])
          redirect_to admin_dashboard_path, notice: "Password updated successfully"
        else
          flash.now[:alert] = @admin.errors.full_messages.join(', ')
          render :edit, status: :unprocessable_entity
        end
      else
        flash.now[:alert] = "New password and confirmation don't match"
        render :edit, status: :unprocessable_entity
      end
    else
      flash.now[:alert] = "Current password is incorrect"
      render :edit, status: :unprocessable_entity
    end
  end
end
```

### Routes

```ruby
# config/routes.rb
Rails.application.routes.draw do
  # Admin namespace
  namespace :admin do
    # Login/logout
    get 'login', to: 'sessions#new'
    post 'login', to: 'sessions#create'
    delete 'logout', to: 'sessions#destroy'
    
    # Dashboard
    root to: 'dashboard#index', as: :dashboard
    
    # Coupon codes
    resources :coupon_codes, only: [:index, :create, :destroy]
    
    # Orders (read-only)
    resources :orders, only: [:index, :show]
    
    # Password management
    resource :password, only: [:edit, :update]
  end
  
  # Redirect /admin to /admin/dashboard or login
  get 'admin', to: redirect('/admin')
  
  # Existing public routes...
end
```

### Views Structure

```
app/views/
├── layouts/
│   ├── admin.html.erb              # Admin layout with header/nav
│   └── application.html.erb         # Public layout (existing)
├── admin/
│   ├── sessions/
│   │   └── new.html.erb            # Login form
│   ├── dashboard/
│   │   └── index.html.erb          # Dashboard with stats
│   ├── coupon_codes/
│   │   ├── index.html.erb          # Coupon list with filters
│   │   └── _coupon.html.erb        # Partial for single coupon row
│   ├── orders/
│   │   ├── index.html.erb          # Order list with search
│   │   ├── show.html.erb           # Order details
│   │   └── _order.html.erb         # Partial for single order row
│   └── passwords/
│       └── edit.html.erb           # Password change form
```

### View Implementation Details

#### Admin Layout
```erb
<!-- app/views/layouts/admin.html.erb -->
<!DOCTYPE html>
<html>
  <head>
    <title>Admin - PromiseKits</title>
    <%= csrf_meta_tags %>
    <%= csp_meta_tag %>
    <%= stylesheet_link_tag "application" %>
    <%= javascript_importmap_tags %>
  </head>
  <body class="admin-layout">
    <header class="admin-header">
      <div class="container">
        <h1>PromiseKits Admin</h1>
        <nav>
          <%= link_to "Dashboard", admin_dashboard_path %>
          <%= link_to "Coupon Codes", admin_coupon_codes_path %>
          <%= link_to "Orders", admin_orders_path %>
          <% if current_admin %>
            <span>Logged in as: <%= current_admin.username %></span>
            <%= link_to "Change Password", edit_admin_password_path %>
            <%= button_to "Logout", admin_logout_path, method: :delete %>
          <% end %>
        </nav>
      </div>
    </header>
    
    <main class="admin-main">
      <div class="container">
        <% if flash[:notice] %>
          <div class="alert alert-success"><%= flash[:notice] %></div>
        <% end %>
        <% if flash[:alert] %>
          <div class="alert alert-error"><%= flash[:alert] %></div>
        <% end %>
        
        <%= yield %>
      </div>
    </main>
  </body>
</html>
```

#### Cursor Pagination Partial
```erb
<!-- app/views/admin/shared/_cursor_pagination.html.erb -->
<div class="pagination">
  <% if local_assigns[:prev_cursor] %>
    <%= link_to "← Previous", url_for(cursor: prev_cursor, direction: :prev), class: "btn" %>
  <% else %>
    <span class="btn disabled">← Previous</span>
  <% end %>
  
  <% if local_assigns[:has_more] && local_assigns[:next_cursor] %>
    <%= link_to "Next →", url_for(cursor: next_cursor, direction: :next), class: "btn" %>
  <% else %>
    <span class="btn disabled">Next →</span>
  <% end %>
</div>
```

### Session Timeout Middleware

```ruby
# config/application.rb
config.middleware.use ActionDispatch::Session::CookieStore, expire_after: 12.hours
```

Or implement custom middleware:

```ruby
# app/middleware/admin_session_timeout.rb
class AdminSessionTimeout
  def initialize(app)
    @app = app
  end
  
  def call(env)
    request = ActionDispatch::Request.new(env)
    
    if request.session[:admin_expires_at]
      if Time.current > request.session[:admin_expires_at]
        request.session[:admin_id] = nil
        request.session[:admin_expires_at] = nil
      else
        # Refresh expiration on activity
        request.session[:admin_expires_at] = 12.hours.from_now
      end
    end
    
    @app.call(env)
  end
end

# config/application.rb
config.middleware.use AdminSessionTimeout
```

## Database Migrations

### Migration 1: Create Admins Table
```ruby
class CreateAdmins < ActiveRecord::Migration[8.0]
  def change
    create_table :admins do |t|
      t.string :username, null: false
      t.string :password_digest, null: false
      t.timestamps
    end
    
    add_index :admins, :username, unique: true
  end
end
```

### Migration 2: Update Coupon Codes
```ruby
class UpdateCouponCodesForNewFormat < ActiveRecord::Migration[8.0]
  def up
    # Add indexes for performance
    add_index :coupon_codes, :usage unless index_exists?(:coupon_codes, :usage)
    
    # Update existing coupon codes to new format (if migrating existing data)
    # This is optional - could also just delete old codes and create new ones
    execute <<-SQL
      -- Update existing codes to new format for development
      -- In production, you might want to keep old codes for historical orders
    SQL
  end
  
  def down
    remove_index :coupon_codes, :usage if index_exists?(:coupon_codes, :usage)
  end
end
```

### Migration 3: Add Indexes for Orders Pagination
```ruby
class AddIndexesForOrdersPagination < ActiveRecord::Migration[8.0]
  def change
    add_index :orders, :created_at unless index_exists?(:orders, :created_at)
    add_index :orders, [:created_at, :id] unless index_exists?(:orders, [:created_at, :id])
  end
end
```

## Seeds Update

```ruby
# db/seeds.rb - Add admin users section

# Create Admin Users
puts "Creating admin users..."
Admin.create!(username: 'admin', password: 'password123', password_confirmation: 'password123')
Admin.create!(username: 'testadmin', password: 'testpass', password_confirmation: 'testpass')
puts "Created #{Admin.count} admin users"

# Update Coupon Codes section
puts "Creating coupon codes with new format..."
CouponCode.destroy_all # Clear old format codes

coupon_codes = [
  { code: 'SK1000AAA', usage: 'unused' },
  { code: 'SK1001BBB', usage: 'unused' },
  { code: 'SK1002CCC', usage: 'unused' },
  { code: 'SK1003DDD', usage: 'unused' }, # Will be marked 'used' when order created
  { code: 'SK1004EEE', usage: 'unused' },
  { code: 'SK1005FFF', usage: 'unused' },
  { code: 'SK1006GGG', usage: 'unused' },
  { code: 'SK1007HHH', usage: 'unused' }
]

coupon_codes.each do |attrs|
  CouponCode.create!(attrs)
end

# Update sample orders to use new coupon codes
# ... (existing order creation logic but with new coupon codes)
```

## Testing Strategy

### Test Coverage Requirements
- **Models**: 90%+ coverage
- **Controllers**: 90%+ coverage  
- **System Tests**: Critical user workflows

### Test Files

```
test/
├── models/
│   ├── admin_test.rb
│   ├── coupon_code_test.rb (update)
│   └── order_test.rb (update)
├── controllers/
│   └── admin/
│       ├── sessions_controller_test.rb
│       ├── dashboard_controller_test.rb
│       ├── coupon_codes_controller_test.rb
│       ├── orders_controller_test.rb
│       └── passwords_controller_test.rb
├── system/
│   └── admin/
│       ├── authentication_test.rb
│       ├── coupon_management_test.rb
│       ├── order_viewing_test.rb
│       └── password_change_test.rb
└── fixtures/
    ├── admins.yml
    ├── coupon_codes.yml (update)
    └── orders.yml (update)
```

### Key Test Scenarios

1. **Authentication**
   - Login with valid credentials
   - Login with invalid credentials
   - Access admin page without login (redirect)
   - Session timeout after 12 hours
   - Logout functionality

2. **Coupon Code Generation**
   - Auto-generate sequential code
   - Format validation (SK[number][3letters])
   - Uniqueness enforcement
   - First code starts at SK1000AAA

3. **Coupon Code Deletion**
   - Delete unused coupon successfully
   - Prevent deletion of used coupon
   - Error message shown on deletion failure

4. **Cursor Pagination**
   - Navigate forward through pages
   - Navigate backward through pages
   - Disable buttons at boundaries
   - Maintain cursor state with filters/search

5. **Password Change**
   - Change password successfully
   - Require current password
   - Validate new password confirmation
   - Remain logged in after change

## Implementation Order

### Phase 1: Foundation (TDD)
1. Create Admin model with tests
2. Add authentication to ApplicationController
3. Create Admin::BaseController
4. Build login/logout functionality
5. Add session timeout middleware
6. **Checkpoint**: Can log in and out

### Phase 2: Coupon Management
1. Update CouponCode model with generation logic
2. Add tests for auto-generation
3. Build Admin::CouponCodesController
4. Create coupon index view with Turbo Frame
5. Implement cursor pagination
6. Add filter and search
7. **Checkpoint**: Can create, view, filter, delete coupons

### Phase 3: Order Viewing
1. Update Order model with search scope
2. Build Admin::OrdersController
3. Create order index view with pagination
4. Create order show view
5. Implement search functionality
6. **Checkpoint**: Can view and search orders

### Phase 4: Dashboard & Stats
1. Build Admin::DashboardController
2. Create dashboard view with statistics
3. Add navigation to layout
4. **Checkpoint**: Dashboard shows stats

### Phase 5: Password Management
1. Build Admin::PasswordsController
2. Create password change form
3. Add validation and tests
4. **Checkpoint**: Can change password

### Phase 6: Polish & Testing
1. Add system tests for full workflows
2. Styling and responsive design
3. Error handling and edge cases
4. Security audit
5. Performance testing (N+1 queries check)
6. **Final Checkpoint**: All acceptance criteria met

## Security Considerations

1. **Password Storage**: bcrypt with cost factor 12 (Rails default)
2. **Session Security**: Encrypted cookies, HTTP-only
3. **CSRF Protection**: Enabled by default in Rails
4. **SQL Injection**: Use parameterized queries (ActiveRecord)
5. **XSS Prevention**: Auto-escaping in ERB (Rails default)
6. **Authorization**: before_action in Admin::BaseController
7. **Session Timeout**: 12 hours, sliding window on activity

## Performance Considerations

1. **N+1 Queries**: Use `includes` for associations in list views
2. **Database Indexes**: 
   - `admins.username` (unique)
   - `coupon_codes.usage`
   - `orders.created_at`
   - Foreign keys already indexed
3. **Cursor Pagination**: More efficient than offset for large datasets
4. **Eager Loading**: Load associations in controllers
5. **Caching**: Fragment cache for dashboard stats (future optimization)

## Deployment Checklist

- [ ] Migrations run successfully
- [ ] Seeds create admin users
- [ ] All tests passing
- [ ] No N+1 query warnings (Bullet gem)
- [ ] Security headers configured
- [ ] Admin credentials changed in production
- [ ] Session secret key set in credentials
- [ ] SSL enforced in production
- [ ] Error monitoring configured

## Future Enhancements (Out of Scope)

- Bulk coupon generation
- Export orders to CSV
- Email notifications
- Two-factor authentication
- Admin activity audit log
- Password reset via email
- Multi-admin role support
- Analytics dashboard with charts

---

**Feature**: 004-admin-dashboard  
**Planning Date**: 2025-01-08  
**Tech Stack**: Rails 8, Hotwire, bcrypt, cursor pagination  
**Estimated Effort**: 8-12 hours  
**Dependencies**: Existing Order, CouponCode models