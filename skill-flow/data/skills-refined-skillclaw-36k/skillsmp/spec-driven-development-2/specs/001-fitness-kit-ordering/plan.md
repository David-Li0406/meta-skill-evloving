# Implementation Plan: Fitness Kit Ordering System

**Feature ID**: 001-fitness-kit-ordering  
**Status**: Planning  
**Created**: 2025-01-XX  
**Last Updated**: 2025-01-XX

---

## Tech Stack

### Core Framework
- **Ruby on Rails 8.0+**
- **Ruby 3.2+**
- **SQLite3** (development/production via constitution)

### Frontend
- **Hotwire Turbo** for page updates and form submissions
- **Hotwire Stimulus** for minimal JavaScript (phone formatting, modal)
- **Tailwind CSS** for styling (if available) or standard Rails CSS
- **ERB templates** for views

### Testing
- **Minitest** (Rails default)
- **System Tests** with Capybara for full workflows
- **FactoryBot** for test data (if not available, use fixtures)

### Additional Gems
- **validates_email_format_of** or custom email validation
- **Bullet** gem (development only, per constitution)

---

## Architecture Overview

### MVC Structure
```
app/
├── models/
│   ├── promise_fitness_kit.rb
│   ├── coupon_code.rb
│   └── order.rb
├── controllers/
│   ├── home_controller.rb           # Homepage with kit listings
│   ├── orders_controller.rb         # RESTful order creation
│   └── concerns/
├── views/
│   ├── home/
│   │   └── index.html.erb          # Kit catalog
│   ├── orders/
│   │   ├── new.html.erb            # Order form
│   │   └── show.html.erb           # Confirmation page
│   └── layouts/
│       └── application.html.erb
├── javascript/
│   └── controllers/
│       ├── phone_format_controller.js   # Format phone input
│       └── coupon_modal_controller.js   # Error popup
└── helpers/
    └── orders_helper.rb

test/
├── models/
│   ├── promise_fitness_kit_test.rb
│   ├── coupon_code_test.rb
│   └── order_test.rb
├── controllers/
│   ├── home_controller_test.rb
│   └── orders_controller_test.rb
└── system/
    └── order_placement_test.rb
```

---

## Database Design

### Migrations

#### 1. Create promise_fitness_kits
```ruby
# db/migrate/YYYYMMDDHHMMSS_create_promise_fitness_kits.rb
create_table :promise_fitness_kits do |t|
  t.string :name, null: false
  t.text :description, null: false
  
  t.timestamps
end

add_index :promise_fitness_kits, :name, unique: true
```

#### 2. Create coupon_codes
```ruby
# db/migrate/YYYYMMDDHHMMSS_create_coupon_codes.rb
create_table :coupon_codes do |t|
  t.string :code, null: false
  t.string :usage, null: false, default: 'unused'
  
  t.timestamps
end

add_index :coupon_codes, :code, unique: true
add_check_constraint :coupon_codes, "usage IN ('unused', 'used')", name: 'usage_check'
```

#### 3. Create orders
```ruby
# db/migrate/YYYYMMDDHHMMSS_create_orders.rb
create_table :orders do |t|
  t.references :promise_fitness_kit, null: false, foreign_key: true
  t.references :coupon_code, null: false, foreign_key: true
  t.integer :order_confirmation, null: false
  t.string :first_name, null: false
  t.string :last_name, null: false
  t.string :address1, null: false
  t.string :address2
  t.string :city, null: false
  t.string :state, null: false, limit: 2
  t.string :zip, null: false
  t.string :phone, null: false, limit: 10
  t.string :email, null: false
  t.text :description
  
  t.timestamps
end

add_index :orders, :order_confirmation, unique: true
add_index :orders, :email
add_index :orders, :created_at
```

---

## Model Implementation

### 1. PromiseFitnessKit Model

**File**: `app/models/promise_fitness_kit.rb`

```ruby
class PromiseFitnessKit < ApplicationRecord
  # Associations
  has_many :orders, dependent: :restrict_with_error
  
  # Validations
  validates :name, presence: true, uniqueness: true
  validates :description, presence: true
  
  # Scopes
  scope :ordered_by_name, -> { order(:name) }
  
  # Instance Methods
  def to_s
    name
  end
end
```

**Tests Required**:
- Validates presence of name
- Validates uniqueness of name
- Validates presence of description
- Cannot delete kit with associated orders
- Factory/fixture for test data

---

### 2. CouponCode Model

**File**: `app/models/coupon_code.rb`

```ruby
class CouponCode < ApplicationRecord
  # Associations
  has_many :orders, dependent: :restrict_with_error
  
  # Validations
  validates :code, presence: true, uniqueness: { case_sensitive: false }
  validates :usage, presence: true, inclusion: { in: %w[unused used] }
  
  # Callbacks
  before_validation :normalize_code
  
  # Scopes
  scope :unused, -> { where(usage: 'unused') }
  scope :used, -> { where(usage: 'used') }
  
  # Instance Methods
  def unused?
    usage == 'unused'
  end
  
  def used?
    usage == 'used'
  end
  
  def mark_as_used!
    update!(usage: 'used')
  end
  
  private
  
  def normalize_code
    self.code = code.to_s.upcase.strip if code.present?
  end
end
```

**Tests Required**:
- Validates presence of code
- Validates uniqueness (case-insensitive)
- Normalizes code to uppercase
- Validates usage inclusion
- `unused?` and `used?` methods work
- `mark_as_used!` changes status
- Scopes filter correctly
- Cannot delete code with associated orders

---

### 3. Order Model

**File**: `app/models/order.rb`

```ruby
class Order < ApplicationRecord
  # Associations
  belongs_to :promise_fitness_kit
  belongs_to :coupon_code
  
  # Constants
  US_STATES = %w[
    AL AK AZ AR CA CO CT DE FL GA HI ID IL IN IA KS KY LA ME MD
    MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR PA RI SC
    SD TN TX UT VT VA WA WV WI WY DC
  ].freeze
  
  # Validations
  validates :first_name, presence: true
  validates :last_name, presence: true
  validates :address1, presence: true
  validates :city, presence: true
  validates :state, presence: true, 
                    inclusion: { in: US_STATES, message: 'must be a valid US state' }
  validates :zip, presence: true, 
                  format: { with: /\A\d{5}(-\d{4})?\z/, message: 'must be 5 digits or ZIP+4' }
  validates :phone, presence: true,
                    length: { is: 10, message: 'must be exactly 10 digits' },
                    format: { with: /\A\d{10}\z/, message: 'must contain only digits' }
  validates :email, presence: true,
                    format: { with: URI::MailTo::EMAIL_REGEXP, message: 'must be a valid email' }
  validates :order_confirmation, presence: true, uniqueness: true
  
  # Custom validations
  validate :coupon_code_must_be_unused, on: :create
  
  # Callbacks
  before_validation :normalize_attributes
  before_create :generate_order_confirmation
  after_create :mark_coupon_as_used
  
  # Scopes
  scope :recent, -> { order(created_at: :desc) }
  
  # Class Methods
  def self.next_confirmation_number
    maximum(:order_confirmation).to_i + 1
  end
  
  # Instance Methods
  def formatted_order_confirmation
    sprintf("%06d", order_confirmation)
  end
  
  def full_name
    "#{first_name} #{last_name}"
  end
  
  def formatted_phone
    "(#{phone[0..2]}) #{phone[3..5]}-#{phone[6..9]}"
  end
  
  def full_address
    [address1, address2, "#{city}, #{state} #{zip}"].compact.join("\n")
  end
  
  private
  
  def normalize_attributes
    self.state = state.to_s.upcase.strip if state.present?
    self.email = email.to_s.downcase.strip if email.present?
    self.phone = phone.to_s.gsub(/\D/, '') if phone.present? # Remove non-digits
    self.zip = zip.to_s.strip if zip.present?
  end
  
  def generate_order_confirmation
    self.order_confirmation = self.class.next_confirmation_number
  end
  
  def coupon_code_must_be_unused
    return unless coupon_code
    
    if coupon_code.used?
      errors.add(:coupon_code, 'has already been used')
    end
  end
  
  def mark_coupon_as_used
    coupon_code.mark_as_used!
  end
end
```

**Tests Required**:
- All validations (presence, format, inclusion)
- Phone normalization (removes dashes)
- Email normalization (lowercase)
- State normalization (uppercase)
- Order confirmation auto-generation
- Coupon validation (must be unused)
- Coupon marked as used after order creation
- Transaction rollback if order creation fails
- Concurrent order creation doesn't duplicate confirmation numbers
- All helper methods (formatted_order_confirmation, full_name, etc.)

---

## Controller Implementation

### 1. HomeController

**File**: `app/controllers/home_controller.rb`

```ruby
class HomeController < ApplicationController
  def index
    @promise_fitness_kits = PromiseFitnessKit.ordered_by_name
  end
end
```

**Tests Required**:
- GET index returns 200
- Assigns @promise_fitness_kits
- Orders kits by name

---

### 2. OrdersController

**File**: `app/controllers/orders_controller.rb`

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
      # TODO: Send confirmation email (OrderMailer.confirmation(@order).deliver_later)
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
    @promise_fitness_kit = PromiseFitnessKit.find(params[:promise_fitness_kit_id])
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

**Tests Required**:
- GET new returns 200
- GET new assigns order and fitness kit
- POST create with valid params creates order
- POST create with valid params marks coupon as used
- POST create with invalid coupon shows error
- POST create with used coupon shows specific error message
- POST create with missing fields shows validation errors
- POST create with invalid email shows error
- POST create with invalid phone shows error
- POST create redirects to show on success
- GET show displays order details

---

## Routes

**File**: `config/routes.rb`

```ruby
Rails.application.routes.draw do
  root 'home#index'
  
  resources :promise_fitness_kits, only: [] do
    resources :orders, only: [:new, :create]
  end
  
  resources :orders, only: [:show]
end
```

**Routes Generated**:
- `GET /` → home#index
- `GET /promise_fitness_kits/:promise_fitness_kit_id/orders/new` → orders#new
- `POST /promise_fitness_kits/:promise_fitness_kit_id/orders` → orders#create
- `GET /orders/:id` → orders#show

---

## View Implementation

### 1. Home Page

**File**: `app/views/home/index.html.erb`

```erb
<div class="container">
  <h1>Available Fitness Kits</h1>
  
  <% if @promise_fitness_kits.empty? %>
    <p>No fitness kits available at this time.</p>
  <% else %>
    <div class="fitness-kits">
      <% @promise_fitness_kits.each do |kit| %>
        <div class="kit-card">
          <h2><%= kit.name %></h2>
          <p><%= kit.description %></p>
          <%= link_to 'Order This Kit', 
                      new_promise_fitness_kit_order_path(kit), 
                      class: 'btn btn-primary' %>
        </div>
      <% end %>
    </div>
  <% end %>
</div>
```

---

### 2. Order Form

**File**: `app/views/orders/new.html.erb`

```erb
<div class="container">
  <h1>Order: <%= @promise_fitness_kit.name %></h1>
  <p><%= @promise_fitness_kit.description %></p>
  
  <%= form_with model: @order, 
                url: promise_fitness_kit_orders_path(@promise_fitness_kit),
                data: { turbo: true } do |f| %>
    
    <% if flash[:error] %>
      <div class="alert alert-error" role="alert">
        <%= flash[:error] %>
      </div>
    <% end %>
    
    <% if @order.errors.any? %>
      <div class="alert alert-error">
        <h3><%= pluralize(@order.errors.count, "error") %> prohibited this order:</h3>
        <ul>
          <% @order.errors.full_messages.each do |message| %>
            <li><%= message %></li>
          <% end %>
        </ul>
      </div>
    <% end %>
    
    <fieldset>
      <legend>Personal Information</legend>
      
      <div class="field">
        <%= f.label :first_name, 'First Name *' %>
        <%= f.text_field :first_name, required: true %>
      </div>
      
      <div class="field">
        <%= f.label :last_name, 'Last Name *' %>
        <%= f.text_field :last_name, required: true %>
      </div>
      
      <div class="field">
        <%= f.label :email, 'Email *' %>
        <%= f.email_field :email, required: true, placeholder: 'user@example.com' %>
      </div>
      
      <div class="field" data-controller="phone-format">
        <%= f.label :phone, 'Phone Number * (10 digits with area code)' %>
        <%= f.text_field :phone, 
                         required: true, 
                         placeholder: '123-456-7890',
                         data: { phone_format_target: 'input' } %>
        <small>Format: 123-456-7890</small>
      </div>
    </fieldset>
    
    <fieldset>
      <legend>Shipping Address</legend>
      
      <div class="field">
        <%= f.label :address1, 'Address Line 1 *' %>
        <%= f.text_field :address1, required: true %>
      </div>
      
      <div class="field">
        <%= f.label :address2, 'Address Line 2' %>
        <%= f.text_field :address2 %>
      </div>
      
      <div class="field">
        <%= f.label :city, 'City *' %>
        <%= f.text_field :city, required: true %>
      </div>
      
      <div class="field">
        <%= f.label :state, 'State * (2-letter code)' %>
        <%= f.text_field :state, 
                         required: true, 
                         maxlength: 2, 
                         placeholder: 'CA' %>
      </div>
      
      <div class="field">
        <%= f.label :zip, 'ZIP Code *' %>
        <%= f.text_field :zip, required: true, placeholder: '12345' %>
      </div>
    </fieldset>
    
    <fieldset>
      <legend>Coupon Code</legend>
      
      <div class="field">
        <%= label_tag 'order[coupon_code_input]', 'Coupon Code *' %>
        <%= text_field_tag 'order[coupon_code_input]', 
                           params[:order]&.dig(:coupon_code_input),
                           required: true,
                           placeholder: 'Enter your coupon code' %>
      </div>
    </fieldset>
    
    <fieldset>
      <legend>Additional Information (Optional)</legend>
      
      <div class="field">
        <%= f.label :description, 'Order Notes' %>
        <%= f.text_area :description, rows: 4 %>
      </div>
    </fieldset>
    
    <div class="actions">
      <%= f.submit 'Place Order', class: 'btn btn-primary' %>
      <%= link_to 'Cancel', root_path, class: 'btn btn-secondary' %>
    </div>
  <% end %>
</div>
```

---

### 3. Order Confirmation Page

**File**: `app/views/orders/show.html.erb`

```erb
<div class="container">
  <div class="success-message">
    <h1>✓ Order Confirmed!</h1>
    <p class="confirmation-number">
      Your order confirmation number is: 
      <strong><%= @order.formatted_order_confirmation %></strong>
    </p>
    <p>A confirmation email has been sent to <strong><%= @order.email %></strong></p>
  </div>
  
  <div class="order-summary">
    <h2>Order Summary</h2>
    
    <div class="summary-section">
      <h3>Fitness Kit</h3>
      <p><strong><%= @order.promise_fitness_kit.name %></strong></p>
    </div>
    
    <div class="summary-section">
      <h3>Shipping To</h3>
      <p>
        <%= @order.full_name %><br>
        <%= simple_format(@order.full_address) %>
      </p>
    </div>
    
    <div class="summary-section">
      <h3>Contact Information</h3>
      <p>
        Email: <%= @order.email %><br>
        Phone: <%= @order.formatted_phone %>
      </p>
    </div>
    
    <% if @order.description.present? %>
      <div class="summary-section">
        <h3>Order Notes</h3>
        <p><%= @order.description %></p>
      </div>
    <% end %>
  </div>
  
  <div class="actions">
    <%= link_to 'Back to Home', root_path, class: 'btn btn-primary' %>
  </div>
</div>
```

---

## JavaScript Implementation (Stimulus)

### 1. Phone Formatting Controller

**File**: `app/javascript/controllers/phone_format_controller.js`

```javascript
import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = ["input"]
  
  connect() {
    this.inputTarget.addEventListener('input', this.format.bind(this))
  }
  
  format(event) {
    let value = event.target.value.replace(/\D/g, '')
    
    if (value.length > 10) {
      value = value.slice(0, 10)
    }
    
    if (value.length >= 6) {
      value = value.slice(0, 3) + '-' + value.slice(3, 6) + '-' + value.slice(6)
    } else if (value.length >= 3) {
      value = value.slice(0, 3) + '-' + value.slice(3)
    }
    
    event.target.value = value
  }
}
```

---

## Seed Data

**File**: `db/seeds.rb`

```ruby
# Clear existing data (development only)
if Rails.env.development?
  Order.destroy_all
  CouponCode.destroy_all
  PromiseFitnessKit.destroy_all
end

# Create Fitness Kits
puts "Creating fitness kits..."

kit1 = PromiseFitnessKit.create!(
  name: 'Beginner Strength Kit',
  description: 'Perfect for those starting their fitness journey. Includes resistance bands, workout guide, and nutrition plan.'
)

kit2 = PromiseFitnessKit.create!(
  name: 'Cardio Endurance Kit',
  description: 'Boost your cardiovascular health. Includes jump rope, interval timer, and 30-day cardio challenge guide.'
)

kit3 = PromiseFitnessKit.create!(
  name: 'Flexibility & Recovery Kit',
  description: 'Essential tools for mobility and recovery. Includes foam roller, stretching guide, and recovery protocols.'
)

puts "Created #{PromiseFitnessKit.count} fitness kits"

# Create Coupon Codes
puts "Creating coupon codes..."

unused_codes = %w[WELCOME2024 FITNESS50 NEWYEAR SPRING25 HEALTH100]
used_codes = %w[USED001 USED002 USED003 USED004 USED005]

unused_codes.each do |code|
  CouponCode.create!(code: code, usage: 'unused')
end

used_codes.each do |code|
  CouponCode.create!(code: code, usage: 'used')
end

puts "Created #{CouponCode.count} coupon codes (#{CouponCode.unused.count} unused, #{CouponCode.used.count} used)"

# Create Sample Orders
puts "Creating sample orders..."

sample_orders = [
  {
    promise_fitness_kit: kit1,
    coupon_code: CouponCode.find_by(code: 'USED001'),
    first_name: 'John',
    last_name: 'Doe',
    address1: '123 Main St',
    city: 'San Francisco',
    state: 'CA',
    zip: '94102',
    phone: '4155551234',
    email: 'john.doe@example.com'
  },
  {
    promise_fitness_kit: kit2,
    coupon_code: CouponCode.find_by(code: 'USED002'),
    first_name: 'Jane',
    last_name: 'Smith',
    address1: '456 Oak Ave',
    address2: 'Apt 3B',
    city: 'Austin',
    state: 'TX',
    zip: '78701',
    phone: '5125555678',
    email: 'jane.smith@example.com',
    description: 'Please leave at front door'
  },
  {
    promise_fitness_kit: kit3,
    coupon_code: CouponCode.find_by(code: 'USED003'),
    first_name: 'Michael',
    last_name: 'Johnson',
    address1: '789 Pine St',
    city: 'Seattle',
    state: 'WA',
    zip: '98101',
    phone: '2065559012',
    email: 'michael.j@example.com'
  },
  {
    promise_fitness_kit: kit1,
    coupon_code: CouponCode.find_by(code: 'USED004'),
    first_name: 'Sarah',
    last_name: 'Williams',
    address1: '321 Elm St',
    city: 'Boston',
    state: 'MA',
    zip: '02101',
    phone: '6175553456',
    email: 'sarah.w@example.com'
  },
  {
    promise_fitness_kit: kit2,
    coupon_code: CouponCode.find_by(code: 'USED005'),
    first_name: 'David',
    last_name: 'Brown',
    address1: '654 Maple Dr',
    city: 'Denver',
    state: 'CO',
    zip: '80202',
    phone: '7205557890',
    email: 'david.brown@example.com',
    description: 'Birthday gift - please include gift wrap'
  }
]

sample_orders.each do |order_attrs|
  Order.create!(order_attrs)
end

puts "Created #{Order.count} sample orders"
puts "\nSeed data complete!"
puts "Fitness Kits: #{PromiseFitnessKit.count}"
puts "Coupon Codes: #{CouponCode.count} (#{CouponCode.unused.count} available)"
puts "Orders: #{Order.count}"
```

---

## Testing Strategy

### Test-First Development (Per Constitution)

#### Model Tests (Unit)
1. **PromiseFitnessKit**
   - Validations
   - Associations
   - Cannot delete with orders

2. **CouponCode**
   - Validations (presence, uniqueness, inclusion)
   - Code normalization
   - State methods (unused?, used?)
   - Scopes
   - Cannot delete with orders

3. **Order**
   - All validations (20+ test cases)
   - Phone normalization
   - Email normalization
   - State normalization
   - Order confirmation generation
   - Coupon validation (unused only)
   - Coupon marked as used after creation
   - Transaction rollback on failure
   - Helper methods

#### Controller Tests (Integration)
1. **HomeController**
   - Index action
   - Kit listing

2. **OrdersController**
   - New action
   - Create action (success)
   - Create action (invalid coupon)
   - Create action (used coupon)
   - Create action (validation errors)
   - Show action

#### System Tests (End-to-End)
1. **Happy Path**: Browse → Select Kit → Fill Form → Submit → See Confirmation
2. **Used Coupon**: Submit with used coupon → See error
3. **Invalid Coupon**: Submit with invalid coupon → See error
4. **Validation Errors**: Submit incomplete form → See errors
5. **Phone Formatting**: Type phone number → See formatting

---

## Implementation Sequence

### Phase 1: Database & Models (Test-First)
1. Create migrations
2. Write model tests
3. Implement models
4. Run tests until green
5. Run `rails db:migrate`

### Phase 2: Seeds & Manual Testing
1. Create seed file
2. Run `rails db:seed`
3. Verify data in console

### Phase 3: Controllers & Routes (Test-First)
1. Define routes
2. Write controller tests
3. Implement controllers
4. Run tests until green

### Phase 4: Views
1. Create layout
2. Implement home page
3. Implement order form
4. Implement confirmation page
5. Add basic styling

### Phase 5: JavaScript (Stimulus)
1. Implement phone formatting controller
2. Test in browser

### Phase 6: System Tests
1. Write end-to-end tests
2. Run and verify
3. Fix any integration issues

### Phase 7: Polish & Validation
1. Check Rubocop compliance
2. Check Bullet gem for N+1 queries
3. Manual QA in browser
4. Verify all acceptance criteria

---

## Performance Considerations

### Database Queries
- Eager load `promise_fitness_kit` when displaying orders
- Index on `order_confirmation` for lookups
- Index on `email` for potential admin searches

### Caching (Future)
- Fragment cache fitness kit listings
- Counter cache if showing "X orders placed"

### N+1 Prevention
- Use `includes(:promise_fitness_kit, :coupon_code)` when listing orders
- Bullet gem will catch issues in development

---

## Security Checklist

- [x] Strong parameters in controller
- [x] CSRF protection (Rails default)
- [x] SQL injection prevention (ActiveRecord parameterization)
- [x] XSS prevention (ERB auto-escaping)
- [x] Mass assignment protection (permit whitelist)
- [x] Email validation
- [x] Input sanitization (phone, zip, state)
- [x] No sensitive data in logs
- [x] Unique constraint on order_confirmation

---

## Deployment Notes

### Database
- SQLite3 configured (per constitution)
- Migrations must run before deploy
- Seed data for production (manual admin task)

### Environment Variables
- None required for MVP
- Email delivery (future): SMTP credentials

### Pre-Deploy Checklist
- [ ] All tests passing
- [ ] Migrations run successfully
- [ ] Seed data loaded
- [ ] Manual QA completed
- [ ] Rubocop clean
- [ ] No N+1 queries

---

## Future Enhancements (Out of Scope)

1. Admin portal for managing kits/orders/coupons
2. Email delivery with ActionMailer
3. Order status tracking
4. Payment processing
5. User authentication
6. PDF invoice generation
7. Inventory management
8. Analytics dashboard
9. Bulk coupon generation
10. Order editing/cancellation

---

## Acceptance Criteria Validation

- [ ] Three tables created with correct schema
- [ ] Foreign keys established
- [ ] All validations working
- [ ] Homepage displays kits
- [ ] Order form captures all data
- [ ] Coupon validation prevents reuse
- [ ] Order confirmation auto-generates (6-digit)
- [ ] Success page displays after order
- [ ] Phone accepts dashes, stores digits
- [ ] State validates US codes only
- [ ] 90%+ test coverage
- [ ] No Rubocop violations
- [ ] No N+1 queries
- [ ] Manual QA passed

---

**Ready for Task Breakdown**: Yes  
**Next Step**: `/speckit.tasks`
