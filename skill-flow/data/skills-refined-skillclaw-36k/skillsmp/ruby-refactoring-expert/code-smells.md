# Code Smells Catalog

Comprehensive guide to identifying code smells in Ruby/Rails applications.

## Large Class

**Description**: Class has too many responsibilities or instance variables

**Detection**:
- Class > 100 lines
- More than 7-10 instance variables
- Many unrelated methods

**Symptoms**:
- Difficult to understand
- Changes for multiple reasons
- Hard to test

**Refactoring**: Extract Class, Extract Module

```ruby
# Smell: Too many responsibilities
class User < ApplicationRecord
  # Authentication
  def authenticate(password)
    # ...
  end

  # Profile management
  def update_profile(params)
    # ...
  end

  # Billing
  def charge_subscription
    # ...
  end

  # Notifications
  def send_welcome_email
    # ...
  end
end

# Fixed: Separated concerns
class User < ApplicationRecord
  has_one :user_profile
  has_one :subscription

  def authenticate(password)
    # Authentication only
  end
end

class UserProfile < ApplicationRecord
  belongs_to :user
end

class Subscription < ApplicationRecord
  belongs_to :user

  def charge
    # Billing logic
  end
end
```

## Long Method

**Description**: Method does too many things

**Detection**:
- Method > 10-15 lines
- Requires scrolling to understand
- Contains multiple levels of abstraction
- Has comments explaining sections

**Refactoring**: Extract Method

```ruby
# Smell: Too long
def process_order
  # Validate items
  return false if items.empty?

  # Calculate totals
  subtotal = items.sum(&:price)
  tax = subtotal * 0.08
  shipping = calculate_shipping(subtotal)
  total = subtotal + tax + shipping

  # Process payment
  payment = Payment.new(total: total)
  return false unless payment.process!

  # Create order
  order = Order.create!(
    items: items,
    subtotal: subtotal,
    tax: tax,
    shipping: shipping,
    total: total
  )

  # Send confirmation
  OrderMailer.confirmation(order).deliver_later

  true
end

# Fixed: Extracted methods
def process_order
  return false unless valid_order?

  process_payment || return
  create_order
  send_confirmation

  true
end

private

def valid_order?
  items.present?
end

def calculate_order_total
  @total ||= subtotal + tax + shipping_cost
end

def subtotal
  @subtotal ||= items.sum(&:price)
end

def tax
  @tax ||= subtotal * 0.08
end

def shipping_cost
  @shipping_cost ||= calculate_shipping(subtotal)
end

def process_payment
  Payment.new(total: calculate_order_total).process!
end

def create_order
  @order = Order.create!(
    items: items,
    subtotal: subtotal,
    tax: tax,
    shipping: shipping_cost,
    total: calculate_order_total
  )
end

def send_confirmation
  OrderMailer.confirmation(@order).deliver_later
end
```

## Long Parameter List

**Description**: Method takes too many parameters

**Detection**:
- More than 3 parameters
- Same parameters appear together frequently

**Refactoring**: Introduce Parameter Object

```ruby
# Smell: Too many parameters
def create_policy(policy_number, effective_date, expiry_date, premium,
                  person_id, company_id, branch_id, producer_id)
  # ...
end

# Fixed: Parameter object
class PolicyParams
  attr_reader :policy_number, :effective_date, :expiry_date, :premium,
              :person_id, :company_id, :branch_id, :producer_id

  def initialize(params)
    @policy_number = params[:policy_number]
    @effective_date = params[:effective_date]
    @expiry_date = params[:expiry_date]
    @premium = params[:premium]
    @person_id = params[:person_id]
    @company_id = params[:company_id]
    @branch_id = params[:branch_id]
    @producer_id = params[:producer_id]
  end

  def valid?
    policy_number.present? && effective_date.present? && expiry_date.present?
  end
end

def create_policy(params)
  policy_params = PolicyParams.new(params)
  return unless policy_params.valid?
  # ...
end
```

## Feature Envy

**Description**: Method uses another object's data more than its own

**Detection**:
- Many method calls to another object
- Minimal use of own instance variables
- Logic naturally belongs elsewhere

**Refactoring**: Move Method

```ruby
# Smell: Person class envying Policy data
class Person < ApplicationRecord
  has_many :policies

  def total_annual_premium
    policies.sum do |policy|
      policy.premium * 12
    end
  end

  def active_policies_count
    policies.count { |p| p.status == 'active' }
  end
end

# Fixed: Moved to Policy
class Person < ApplicationRecord
  has_many :policies

  def total_annual_premium
    policies.sum(&:annual_premium)
  end

  def active_policies_count
    policies.active.count
  end
end

class Policy < ApplicationRecord
  belongs_to :person

  scope :active, -> { where(status: 'active') }

  def annual_premium
    premium * 12
  end
end
```

## Data Clumps

**Description**: Same group of data items appear together repeatedly

**Detection**:
- Same 2-3 variables passed together
- Variables always used as a group

**Refactoring**: Extract Class

```ruby
# Smell: Date range clump
def policies_expiring(start_date, end_date)
  Policy.where(expiry_date: start_date..end_date)
end

def claims_filed(start_date, end_date)
  Claim.where(filed_at: start_date..end_date)
end

def premiums_collected(start_date, end_date)
  Payment.where(paid_at: start_date..end_date).sum(:amount)
end

# Fixed: Extract DateRange class
class DateRange
  attr_reader :start_date, :end_date

  def initialize(start_date, end_date)
    @start_date = start_date
    @end_date = end_date
  end

  def to_range
    start_date..end_date
  end

  def self.this_month
    new(Date.today.beginning_of_month, Date.today.end_of_month)
  end

  def self.last_30_days
    new(30.days.ago.to_date, Date.today)
  end
end

def policies_expiring(date_range)
  Policy.where(expiry_date: date_range.to_range)
end

def claims_filed(date_range)
  Claim.where(filed_at: date_range.to_range)
end

def premiums_collected(date_range)
  Payment.where(paid_at: date_range.to_range).sum(:amount)
end
```

## Primitive Obsession

**Description**: Using primitives (strings, integers) instead of small objects

**Detection**:
- String used for states/types
- Multiple related primitives
- Validation/behavior attached to primitives

**Refactoring**: Extract Value Object

```ruby
# Smell: Primitive obsession with money
class Policy < ApplicationRecord
  # premium stored as integer cents
  attribute :premium, :integer

  def premium_in_dollars
    premium / 100.0
  end

  def formatted_premium
    "$#{premium_in_dollars}"
  end

  def increase_premium(percentage)
    self.premium = (premium * (1 + percentage / 100.0)).round
  end
end

# Fixed: Money value object
class Money
  attr_reader :cents

  def initialize(cents)
    @cents = cents
  end

  def self.from_dollars(dollars)
    new((dollars * 100).round)
  end

  def to_dollars
    cents / 100.0
  end

  def to_s
    "$#{'%.2f' % to_dollars}"
  end

  def +(other)
    Money.new(cents + other.cents)
  end

  def *(multiplier)
    Money.new((cents * multiplier).round)
  end

  def increase_by_percentage(percentage)
    self * (1 + percentage / 100.0)
  end
end

class Policy < ApplicationRecord
  def premium
    Money.new(self[:premium])
  end

  def premium=(money)
    self[:premium] = money.cents
  end
end
```

## Shotgun Surgery

**Description**: Change requires many small edits across many classes

**Detection**:
- Single change touches many files
- Related code scattered across codebase
- Difficult to ensure all changes made

**Refactoring**: Move Method, Extract Class

## Divergent Change

**Description**: Class changes for multiple different reasons

**Detection**:
- "When X changes, we modify this class"
- "When Y changes, we also modify this class"
- Multiple axes of change

**Refactoring**: Extract Class

## Lazy Class

**Description**: Class doesn't do enough to justify existence

**Detection**:
- Very few methods
- Simple delegation
- Could be absorbed by another class

**Refactoring**: Inline Class, Collapse Hierarchy

## Summary

| Smell | Detection | Refactoring |
|-------|-----------|-------------|
| Large Class | > 100 lines, many instance vars | Extract Class |
| Long Method | > 10-15 lines | Extract Method |
| Long Parameter List | > 3 parameters | Parameter Object |
| Feature Envy | Uses other object's data | Move Method |
| Data Clumps | Same vars together | Extract Class |
| Primitive Obsession | Primitives with behavior | Value Object |
| Shotgun Surgery | Many files for one change | Move Method |
| Divergent Change | Multiple reasons to change | Extract Class |

Remember: These are **guidelines**, not strict rules. Context matters!
