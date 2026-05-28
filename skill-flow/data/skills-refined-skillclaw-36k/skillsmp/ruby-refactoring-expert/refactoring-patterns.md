# Refactoring Patterns

Detailed catalog of refactoring patterns for Ruby/Rails applications.

## Extract Method

**Problem**: Method is too long or does multiple things

**Solution**: Extract code into a new method with descriptive name

**Steps**:
1. Identify cohesive block of code
2. Extract to new method
3. Replace with method call
4. Name method after what it does, not how

**Example**:
```ruby
# Before
def calculate_invoice
  total = 0
  line_items.each do |item|
    total += item.quantity * item.price
  end

  discount = 0
  if customer.premium?
    discount = total * 0.1
  end

  tax = (total - discount) * 0.08
  total - discount + tax
end

# After
def calculate_invoice
  subtotal - discount + tax
end

private

def subtotal
  line_items.sum { |item| item.quantity * item.price }
end

def discount
  return 0 unless customer.premium?
  subtotal * 0.1
end

def tax
  (subtotal - discount) * 0.08
end
```

## Extract Class

**Problem**: Class has multiple responsibilities

**Solution**: Create new class for distinct responsibility

**When to use**:
- Class > 100 lines
- Multiple reasons to change
- Cohesive subset of data/methods

**Example**:
```ruby
# Before: Person class handling contact info
class Person < ApplicationRecord
  attribute :phone_number
  attribute :phone_type
  attribute :email
  attribute :email_type

  def formatted_phone
    # Phone formatting logic
  end

  def valid_phone?
    # Phone validation
  end

  def formatted_email
    # Email formatting logic
  end
end

# After: Extracted PhoneNumber class
class Person < ApplicationRecord
  has_one :phone_number
  has_one :email_address
end

class PhoneNumber < ApplicationRecord
  belongs_to :person

  attribute :number
  attribute :type

  def formatted
    # Formatting logic
  end

  def valid?
    # Validation logic
  end
end

class EmailAddress < ApplicationRecord
  belongs_to :person

  attribute :address
  attribute :type

  def formatted
    # Formatting logic
  end
end
```

## Extract Module (Concern)

**Problem**: Multiple classes share behavior

**Solution**: Extract to module/concern

**When to use**:
- Behavior used in 2+ classes
- Clear, focused responsibility
- Related methods and attributes

**Example**:
```ruby
# Before: Duplicated archiving logic
class Policy < ApplicationRecord
  scope :archived, -> { where.not(archived_at: nil) }
  scope :active, -> { where(archived_at: nil) }

  def archive!
    update!(archived_at: Time.current)
  end

  def archived?
    archived_at.present?
  end
end

class Claim < ApplicationRecord
  scope :archived, -> { where.not(archived_at: nil) }
  scope :active, -> { where(archived_at: nil) }

  def archive!
    update!(archived_at: Time.current)
  end

  def archived?
    archived_at.present?
  end
end

# After: Extracted Archivable concern
module Archivable
  extend ActiveSupport::Concern

  included do
    scope :archived, -> { where.not(archived_at: nil) }
    scope :active, -> { where(archived_at: nil) }
  end

  def archive!
    update!(archived_at: Time.current)
  end

  def archived?
    archived_at.present?
  end
end

class Policy < ApplicationRecord
  include Archivable
end

class Claim < ApplicationRecord
  include Archivable
end
```

## Extract Service Object

**Problem**: Complex operation spanning multiple models

**Solution**: Create service object to encapsulate operation

**When to use**:
- Logic spans 2+ models
- External API calls
- Complex workflows
- Heavy side effects

**Example**:
```ruby
# Service object pattern
class PolicyRenewalService
  def initialize(policy, new_expiry_date, renewed_by:)
    @policy = policy
    @new_expiry_date = new_expiry_date
    @renewed_by = renewed_by
  end

  def call
    return failure("Not renewable") unless renewable?

    ApplicationRecord.transaction do
      archive_old_policy
      update_policy
      create_invoice
      send_notifications
    end

    success(@policy)
  rescue StandardError => e
    failure(e.message)
  end

  private

  def renewable?
    @policy.active? && @policy.expiry_date > Date.today
  end

  def archive_old_policy
    @archived_policy = @policy.dup
    @archived_policy.update!(status: 'renewed')
  end

  def update_policy
    @policy.update!(
      effective_date: Date.today,
      expiry_date: @new_expiry_date,
      renewed_from_policy: @archived_policy
    )
  end

  def create_invoice
    Invoice.create!(policy: @policy, amount: @policy.total_premium)
  end

  def send_notifications
    PolicyMailer.renewal_confirmation(@policy).deliver_later
  end

  def success(result)
    { success: true, policy: result }
  end

  def failure(error)
    { success: false, error: error }
  end
end
```

## Replace Conditional with Polymorphism

**Problem**: Conditional based on object type

**Solution**: Use polymorphism (subclasses or strategy pattern)

**Example**:
```ruby
# Before: Type checking
class Policy < ApplicationRecord
  def calculate_premium
    case insurance_type
    when 'auto'
      base_rate * vehicle_factor * driver_age_factor
    when 'home'
      base_rate * property_value_factor * location_risk
    when 'life'
      base_rate * age_factor * health_factor
    end
  end

  def required_documents
    case insurance_type
    when 'auto'
      ['drivers_license', 'vehicle_registration']
    when 'home'
      ['property_deed', 'home_inspection']
    when 'life'
      ['medical_exam', 'beneficiary_form']
    end
  end
end

# After: Polymorphism with STI
class Policy < ApplicationRecord
  # Base class - shared behavior
end

class AutoPolicy < Policy
  def calculate_premium
    base_rate * vehicle_factor * driver_age_factor
  end

  def required_documents
    ['drivers_license', 'vehicle_registration']
  end
end

class HomePolicy < Policy
  def calculate_premium
    base_rate * property_value_factor * location_risk
  end

  def required_documents
    ['property_deed', 'home_inspection']
  end
end

class LifePolicy < Policy
  def calculate_premium
    base_rate * age_factor * health_factor
  end

  def required_documents
    ['medical_exam', 'beneficiary_form']
  end
end
```

## Introduce Parameter Object

**Problem**: Methods take same group of parameters

**Solution**: Group parameters into object

**Example**:
```ruby
# Before
class ReportGenerator
  def generate_policy_report(start_date, end_date, format, include_archived)
    # ...
  end

  def export_claims(start_date, end_date, format, include_archived)
    # ...
  end

  def analyze_premiums(start_date, end_date, format, include_archived)
    # ...
  end
end

# After
class ReportParams
  attr_reader :start_date, :end_date, :format, :include_archived

  def initialize(start_date:, end_date:, format: :pdf, include_archived: false)
    @start_date = start_date
    @end_date = end_date
    @format = format
    @include_archived = include_archived
  end

  def date_range
    start_date..end_date
  end

  def valid?
    start_date.present? && end_date.present? && start_date <= end_date
  end
end

class ReportGenerator
  def generate_policy_report(params)
    return unless params.valid?
    # Use params.date_range, params.format, etc.
  end

  def export_claims(params)
    return unless params.valid?
    # ...
  end

  def analyze_premiums(params)
    return unless params.valid?
    # ...
  end
end
```

## Replace Method with Method Object

**Problem**: Long method with many local variables

**Solution**: Turn method into its own class

**When to use**:
- Method too long to easily extract
- Many local variables needed
- Complex algorithm

**Example**:
```ruby
# Before: Complex calculation with many locals
class Policy < ApplicationRecord
  def calculate_complex_premium
    base = base_rate
    risk_factor = calculate_risk_factor
    age_factor = calculate_age_factor
    location_factor = calculate_location_factor
    discount = calculate_discount(base, risk_factor)
    surcharge = calculate_surcharge(location_factor)

    final = base * risk_factor * age_factor * location_factor
    final -= discount
    final += surcharge
    apply_minimum_maximum(final)
  end
end

# After: Method object
class PremiumCalculator
  def initialize(policy)
    @policy = policy
    @base = policy.base_rate
    @risk_factor = calculate_risk_factor
    @age_factor = calculate_age_factor
    @location_factor = calculate_location_factor
  end

  def calculate
    premium = base_premium
    premium = apply_discount(premium)
    premium = apply_surcharge(premium)
    apply_limits(premium)
  end

  private

  def base_premium
    @base * @risk_factor * @age_factor * @location_factor
  end

  def apply_discount(premium)
    discount = calculate_discount(premium, @risk_factor)
    premium - discount
  end

  def apply_surcharge(premium)
    surcharge = calculate_surcharge(@location_factor)
    premium + surcharge
  end

  def apply_limits(premium)
    [[premium, @policy.minimum_premium].max, @policy.maximum_premium].min
  end

  # ... helper methods
end

class Policy < ApplicationRecord
  def calculate_complex_premium
    PremiumCalculator.new(self).calculate
  end
end
```

## Form Template Method

**Problem**: Similar algorithms in subclasses with variations

**Solution**: Define template method in superclass

**Example**:
```ruby
# Before: Duplicated structure
class EmailNotifier
  def send_welcome_email(user)
    prepare_email
    add_welcome_content(user)
    add_footer
    send_email
  end

  def send_renewal_email(policy)
    prepare_email
    add_renewal_content(policy)
    add_footer
    send_email
  end
end

# After: Template method
class EmailNotifier
  def send_email(recipient, content_builder)
    prepare_email
    add_content(recipient, content_builder)
    add_footer
    deliver
  end

  private

  def prepare_email
    # Common setup
  end

  def add_content(recipient, content_builder)
    # Calls specific content builder
    content_builder.call(recipient)
  end

  def add_footer
    # Common footer
  end

  def deliver
    # Common delivery
  end
end
```

## Summary Table

| Pattern | Problem | When to Use |
|---------|---------|-------------|
| Extract Method | Long method | Method > 10-15 lines |
| Extract Class | Too many responsibilities | Class > 100 lines |
| Extract Module | Duplicated behavior | Used in 2+ classes |
| Extract Service | Complex operation | Spans multiple models |
| Replace Conditional | Type checking | Many type-based conditionals |
| Parameter Object | Long parameter list | > 3 parameters |
| Method Object | Complex method | Many local variables |
| Template Method | Similar algorithms | Common structure, different steps |

## Refactoring Safety

Before refactoring:
1. ✅ Ensure tests exist and pass
2. ✅ Make small, incremental changes
3. ✅ Run tests after each change
4. ✅ Commit working states frequently
5. ✅ Don't change behavior (unless explicitly intended)

Remember: Refactoring should improve code structure **without** changing functionality!
