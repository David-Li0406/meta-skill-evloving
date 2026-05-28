# Design Patterns

## Form Objects

### Basic Form Object

```ruby
# app/forms/user_registration_form.rb
class UserRegistrationForm
  include ActiveModel::Model
  include ActiveModel::Attributes

  attribute :email, :string
  attribute :password, :string
  attribute :password_confirmation, :string
  attribute :first_name, :string
  attribute :last_name, :string
  attribute :accept_terms, :boolean

  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :password, presence: true, length: { minimum: 8 }
  validates :password_confirmation, presence: true
  validates :first_name, :last_name, presence: true
  validates :accept_terms, acceptance: true
  validate :passwords_match

  def save
    return false unless valid?

    ActiveRecord::Base.transaction do
      @user = User.create!(
        email: email,
        password: password,
        first_name: first_name,
        last_name: last_name
      )
      SendWelcomeEmailJob.perform_later(@user)
    end

    true
  rescue ActiveRecord::RecordInvalid => e
    errors.add(:base, e.message)
    false
  end

  attr_reader :user

  private

  def passwords_match
    return if password == password_confirmation
    errors.add(:password_confirmation, "doesn't match password")
  end
end
```

### Multi-Step Wizard Form

```ruby
class CheckoutWizard
  include ActiveModel::Model

  STEPS = [:shipping, :payment, :confirmation].freeze

  attr_accessor :current_step
  attr_reader :order

  validates :shipping_address, presence: true, if: :shipping_step?
  validates :payment_method, presence: true, if: :payment_step?

  def initialize(order, current_step: :shipping)
    @order = order
    @current_step = current_step.to_sym
  end

  def next_step
    return if last_step?
    self.current_step = STEPS[STEPS.index(current_step) + 1]
  end

  def last_step?
    current_step == STEPS.last
  end

  private

  def shipping_step?
    current_step == :shipping
  end

  def payment_step?
    current_step == :payment
  end
end
```

---

## Decorators

### Draper Pattern

```ruby
# app/decorators/user_decorator.rb
class UserDecorator < Draper::Decorator
  delegate_all

  def full_name
    "#{object.first_name} #{object.last_name}"
  end

  def profile_link
    h.link_to full_name, h.user_path(object), class: 'user-link'
  end

  def avatar
    if object.avatar.attached?
      h.image_tag object.avatar.variant(resize_to_limit: [100, 100])
    else
      h.image_tag 'default-avatar.png', alt: full_name
    end
  end

  def status_badge
    css_class = object.active? ? 'badge-success' : 'badge-secondary'
    status_text = object.active? ? 'Active' : 'Inactive'
    h.content_tag(:span, status_text, class: "badge #{css_class}")
  end
end

# Controller: @user = User.find(params[:id]).decorate
# View: <%= @user.profile_link %>
```

### SimpleDelegator Pattern (No Gems)

```ruby
class UserDecorator < SimpleDelegator
  def initialize(user, view_context)
    super(user)
    @view_context = view_context
  end

  def full_name
    "#{first_name} #{last_name}"
  end

  def profile_link
    h.link_to full_name, h.user_path(self)
  end

  private

  def h
    @view_context
  end
end

# Controller: @user = UserDecorator.new(User.find(params[:id]), view_context)
```

---

## Presenters

```ruby
# app/presenters/dashboard_presenter.rb
class DashboardPresenter
  def initialize(user, view_context)
    @user = user
    @view_context = view_context
  end

  def welcome_message
    time_of_day = Time.current.hour < 12 ? 'Morning' : 'Afternoon'
    "Good #{time_of_day}, #{@user.first_name}!"
  end

  def recent_orders
    @user.orders.recent.limit(5)
  end

  def total_spent
    h.number_to_currency(@user.orders.sum(:total))
  end

  def stats
    {
      total_orders: @user.orders.count,
      total_spent: total_spent,
      member_since: @user.created_at.year
    }
  end

  private

  def h
    @view_context
  end
end

# Controller: @presenter = DashboardPresenter.new(current_user, view_context)
# View: <%= @presenter.welcome_message %>
```

---

## Repository Pattern

```ruby
# app/repositories/user_repository.rb
class UserRepository
  class << self
    def find(id)
      User.find(id)
    end

    def find_by_email(email)
      User.find_by(email: email)
    end

    def active_users
      User.where(active: true).order(created_at: :desc)
    end

    def search(query)
      User.where('name ILIKE ? OR email ILIKE ?', "%#{query}%", "%#{query}%")
    end

    def create(attributes)
      User.create(attributes)
    end
  end
end
```

---

## Value Objects

```ruby
class Money
  include Comparable

  attr_reader :amount, :currency

  def initialize(amount, currency: 'USD')
    @amount = BigDecimal(amount.to_s)
    @currency = currency
  end

  def +(other)
    validate_currency!(other)
    Money.new(amount + other.amount, currency: currency)
  end

  def to_s
    format('%s%.2f', currency_symbol, amount)
  end

  private

  def validate_currency!(other)
    raise ArgumentError, "Cannot operate on different currencies" if currency != other.currency
  end

  def currency_symbol
    { 'USD' => '$', 'EUR' => '€', 'GBP' => '£' }[currency] || currency
  end
end
```

---

## Result Objects

```ruby
class Result
  attr_reader :value, :error

  def self.success(value = nil)
    new(success: true, value: value)
  end

  def self.failure(error)
    new(success: false, error: error)
  end

  def success?
    @success
  end

  def failure?
    !@success
  end

  def on_success
    yield value if success?
    self
  end

  def on_failure
    yield error if failure?
    self
  end

  private

  def initialize(success:, value: nil, error: nil)
    @success = success
    @value = value
    @error = error
  end
end

# Usage
result = CreateUserService.new.call(user_params)
result
  .on_success { |user| redirect_to user }
  .on_failure { |errors| render :new }
```

---

## DTOs (Ruby 3.2+)

```ruby
UserDTO = Data.define(:id, :email, :full_name, :role) do
  def self.from_model(user)
    new(
      id: user.id,
      email: user.email,
      full_name: "#{user.first_name} #{user.last_name}",
      role: user.role
    )
  end
end
```
