# Design Pattern Examples

Extended examples and common anti-patterns.

## Null Object Pattern

Avoid nil checks throughout code:

```ruby
class NullUser
  def name = "Guest"
  def email = nil
  def admin? = false
  def can?(_permission) = false
  def notify(_message) = nil  # No-op
end

class UserRepository
  def find(id)
    User.find_by(id: id) || NullUser.new
  end
end

# No nil checks needed
user = UserRepository.new.find(params[:id])
puts "Hello, #{user.name}"  # Works for real or null user
user.notify("Welcome!")      # Safe to call
```

## Service Object Pattern

Encapsulate business logic in dedicated classes:

```ruby
class CreateOrder
  def initialize(user:, cart:, payment_method:)
    @user = user
    @cart = cart
    @payment_method = payment_method
  end

  def call
    validate!
    order = build_order
    charge_payment(order)
    send_confirmation(order)
    Result.success(order)
  rescue ValidationError => e
    Result.failure(e.message)
  rescue PaymentError => e
    Result.failure("Payment failed: #{e.message}")
  end

  private

  def validate!
    raise ValidationError, "Cart is empty" if @cart.empty?
    raise ValidationError, "User not verified" unless @user.verified?
  end

  def build_order
    Order.create!(
      user: @user,
      items: @cart.items,
      total: @cart.total
    )
  end

  def charge_payment(order)
    PaymentGateway.charge(@payment_method, order.total)
  end

  def send_confirmation(order)
    OrderMailer.confirmation(order).deliver_later
  end
end

class Result
  attr_reader :value, :error

  def self.success(value) = new(value: value)
  def self.failure(error) = new(error: error)

  def initialize(value: nil, error: nil)
    @value = value
    @error = error
  end

  def success? = @error.nil?
  def failure? = !success?
end

# Usage
result = CreateOrder.new(
  user: current_user,
  cart: shopping_cart,
  payment_method: credit_card
).call

if result.success?
  redirect_to result.value
else
  flash[:error] = result.error
  render :checkout
end
```

## Query Object Pattern

Encapsulate complex queries:

```ruby
class UserQuery
  def initialize(relation = User.all)
    @relation = relation
  end

  def active
    chain { @relation.where(active: true) }
  end

  def created_after(date)
    chain { @relation.where("created_at > ?", date) }
  end

  def with_role(role)
    chain { @relation.joins(:roles).where(roles: { name: role }) }
  end

  def search(term)
    return self if term.blank?
    chain { @relation.where("name ILIKE ? OR email ILIKE ?", "%#{term}%", "%#{term}%") }
  end

  def ordered_by_recent
    chain { @relation.order(created_at: :desc) }
  end

  def to_a
    @relation.to_a
  end

  def each(&block)
    @relation.each(&block)
  end

  private

  def chain
    self.class.new(yield)
  end
end

# Composable queries
users = UserQuery.new
  .active
  .created_after(1.month.ago)
  .with_role("admin")
  .search(params[:q])
  .ordered_by_recent
  .to_a
```

## Form Object Pattern

Handle complex form logic:

```ruby
class RegistrationForm
  include ActiveModel::Model
  include ActiveModel::Attributes

  attribute :email, :string
  attribute :password, :string
  attribute :password_confirmation, :string
  attribute :terms_accepted, :boolean
  attribute :newsletter, :boolean, default: false

  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :password, presence: true, length: { minimum: 8 }
  validates :terms_accepted, acceptance: true
  validate :passwords_match

  def save
    return false unless valid?

    ActiveRecord::Base.transaction do
      user = User.create!(email: email, password: password)
      Newsletter.subscribe(user) if newsletter
      WelcomeMailer.deliver_later(user)
    end

    true
  rescue ActiveRecord::RecordInvalid => e
    errors.add(:base, e.message)
    false
  end

  private

  def passwords_match
    return if password == password_confirmation
    errors.add(:password_confirmation, "doesn't match password")
  end
end

# In controller
def create
  @form = RegistrationForm.new(registration_params)

  if @form.save
    redirect_to dashboard_path
  else
    render :new
  end
end
```

## Value Object Pattern

Immutable objects representing values:

```ruby
class Money
  include Comparable

  attr_reader :amount, :currency

  def initialize(amount, currency = "USD")
    @amount = BigDecimal(amount.to_s)
    @currency = currency.to_s.upcase
    freeze
  end

  def +(other)
    ensure_same_currency!(other)
    Money.new(amount + other.amount, currency)
  end

  def -(other)
    ensure_same_currency!(other)
    Money.new(amount - other.amount, currency)
  end

  def *(multiplier)
    Money.new(amount * multiplier, currency)
  end

  def <=>(other)
    ensure_same_currency!(other)
    amount <=> other.amount
  end

  def to_s
    format("%.2f %s", amount, currency)
  end

  def ==(other)
    other.is_a?(Money) &&
      amount == other.amount &&
      currency == other.currency
  end
  alias eql? ==

  def hash
    [amount, currency].hash
  end

  private

  def ensure_same_currency!(other)
    return if currency == other.currency
    raise ArgumentError, "Currency mismatch: #{currency} vs #{other.currency}"
  end
end

price = Money.new(100, "USD")
tax = Money.new(8.5, "USD")
total = price + tax  # => Money.new(108.5, "USD")
```

## Anti-Patterns to Avoid

### God Object

```ruby
# Bad: One class does everything
class User
  def save; end
  def send_email; end
  def generate_report; end
  def calculate_taxes; end
  def export_to_csv; end
  def sync_with_crm; end
end

# Good: Split into focused classes
class User; end
class UserMailer; end
class UserReport; end
class TaxCalculator; end
class UserExporter; end
class CrmSync; end
```

### Shotgun Surgery

When one change requires modifications in many places:

```ruby
# Bad: Price formatting scattered everywhere
class Product
  def display_price
    "$#{price.round(2)}"
  end
end

class Order
  def display_total
    "$#{total.round(2)}"
  end
end

# Good: Centralized formatting
class MoneyFormatter
  def self.format(amount, currency = "$")
    "#{currency}#{amount.round(2)}"
  end
end
```

### Feature Envy

Method more interested in another class's data:

```ruby
# Bad: Order knows too much about User
class Order
  def shipping_cost
    if user.address.country == "US"
      if user.address.state == "CA"
        10.0
      else
        15.0
      end
    else
      50.0
    end
  end
end

# Good: User/Address handles its own logic
class Address
  def domestic?
    country == "US"
  end

  def california?
    state == "CA" && domestic?
  end
end

class Order
  def shipping_cost
    ShippingCalculator.for(user.address).cost
  end
end
```
