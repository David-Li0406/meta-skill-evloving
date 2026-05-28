# Service Object Patterns

Detailed implementations for common service patterns in Rails.

## Basic Service Pattern

Standard service with transaction handling:

```ruby
class CreateOrder
  def initialize(user, cart_items, payment_method)
    @user = user
    @cart_items = cart_items
    @payment_method = payment_method
  end

  def call
    ActiveRecord::Base.transaction do
      order = create_order
      create_order_items(order)
      process_payment(order)
      send_confirmation_email(order)
      order
    end
  rescue PaymentError => e
    handle_payment_error(e)
  end

  private

  def create_order
    @user.orders.create!(
      total: calculate_total,
      status: 'pending'
    )
  end

  def calculate_total
    @cart_items.sum { |item| item.price * item.quantity }
  end
end

# Usage
order = CreateOrder.new(user, cart_items, payment_method).call
```

## Result Object Pattern

When callers need to know success/failure with data:

```ruby
class AuthenticateUser
  Result = Struct.new(:success?, :user, :error, keyword_init: true)

  def initialize(email, password)
    @email = email
    @password = password
  end

  def call
    user = User.find_by(email: @email)

    if user&.authenticate(@password)
      Result.new(success?: true, user: user)
    else
      Result.new(success?: false, error: 'Invalid credentials')
    end
  end
end

# Usage
result = AuthenticateUser.new(email, password).call
if result.success?
  sign_in(result.user)
else
  flash[:error] = result.error
end
```

### Enhanced Result with Monad Pattern

```ruby
class ServiceResult
  attr_reader :value, :error

  def self.success(value)
    new(value: value, success: true)
  end

  def self.failure(error)
    new(error: error, success: false)
  end

  def initialize(value: nil, error: nil, success:)
    @value = value
    @error = error
    @success = success
  end

  def success?
    @success
  end

  def failure?
    !@success
  end

  def on_success
    yield(value) if success?
    self
  end

  def on_failure
    yield(error) if failure?
    self
  end
end

# Usage with chaining
ProcessPayment.new(order).call
  .on_success { |payment| redirect_to payment }
  .on_failure { |error| render :new, alert: error }
```

## Form Object Pattern

For complex forms spanning multiple models:

```ruby
class RegistrationForm
  include ActiveModel::Model
  include ActiveModel::Validations

  attr_accessor :email, :password, :password_confirmation,
                :company_name, :company_size

  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :password, presence: true, length: { minimum: 8 }
  validates :password, confirmation: true
  validates :company_name, presence: true

  def save
    return false unless valid?

    ActiveRecord::Base.transaction do
      user = User.create!(email: email, password: password)
      Company.create!(name: company_name, size: company_size, owner: user)
      true
    end
  rescue ActiveRecord::RecordInvalid => e
    errors.add(:base, e.message)
    false
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

## Query Object Pattern

For complex database queries:

```ruby
class ExpiredPoliciesQuery
  def initialize(relation = Policy.all)
    @relation = relation
  end

  def call(grace_period: 30.days)
    @relation
      .where(status: 'active')
      .where('expiry_date < ?', grace_period.ago)
      .includes(:holder, :agent)
      .order(expiry_date: :asc)
  end
end

# Usage
expired = ExpiredPoliciesQuery.new.call
expired_for_agent = ExpiredPoliciesQuery.new(agent.policies).call(grace_period: 15.days)
```

### Composable Query Objects

```ruby
class PolicySearch
  def initialize(relation = Policy.all)
    @relation = relation
  end

  def by_status(status)
    @relation = @relation.where(status: status)
    self
  end

  def expiring_within(days)
    @relation = @relation.where('expiry_date < ?', days.from_now)
    self
  end

  def for_agent(agent)
    @relation = @relation.where(agent: agent)
    self
  end

  def results
    @relation
  end
end

# Chainable usage
PolicySearch.new
  .by_status('active')
  .expiring_within(30.days)
  .for_agent(current_agent)
  .results
```

## Policy Object Pattern

For authorization logic (similar to Pundit):

```ruby
class PolicyPolicy  # Naming: ResourcePolicy
  attr_reader :user, :policy

  def initialize(user, policy)
    @user = user
    @policy = policy
  end

  def show?
    owner? || agent? || admin?
  end

  def update?
    agent? || admin?
  end

  def destroy?
    admin?
  end

  private

  def owner?
    policy.holder == user
  end

  def agent?
    policy.agent == user
  end

  def admin?
    user.admin?
  end
end

# Usage
def show
  @policy = Policy.find(params[:id])
  authorize(@policy) # Raises if PolicyPolicy.new(current_user, @policy).show? is false
end
```

## External API Integration Service

```ruby
class WeatherService
  include HTTParty
  base_uri 'api.weather.com'

  def initialize(api_key = ENV['WEATHER_API_KEY'])
    @options = { query: { api_key: api_key } }
  end

  def current_weather(city)
    response = self.class.get("/current/#{city}", @options)

    if response.success?
      parse_weather_data(response)
    else
      raise WeatherAPIError, response.message
    end
  rescue HTTParty::Error => e
    Rails.logger.error "Weather API error: #{e.message}"
    raise WeatherAPIError, "Unable to fetch weather data"
  end

  private

  def parse_weather_data(response)
    WeatherData.new(
      temperature: response['temp'],
      conditions: response['conditions'],
      humidity: response['humidity']
    )
  end
end
```

## Error Handling Patterns

### Custom Exception Classes

```ruby
# app/errors/service_errors.rb
module ServiceErrors
  class BaseError < StandardError
    attr_reader :code, :details

    def initialize(message, code: nil, details: {})
      super(message)
      @code = code
      @details = details
    end
  end

  class ValidationError < BaseError; end
  class NotFoundError < BaseError; end
  class AuthorizationError < BaseError; end
  class ExternalServiceError < BaseError; end
end

# Usage in service
class ProcessPayment
  def call
    raise ServiceErrors::ValidationError.new(
      "Invalid amount",
      code: :invalid_amount,
      details: { amount: @amount }
    ) if @amount <= 0

    # ...
  end
end
```

## Directory Organization

```
app/services/
├── application_service.rb      # Base class (optional)
├── concerns/                   # Shared service concerns
│   └── transactional.rb
├── orders/                     # Domain-grouped services
│   ├── create_order.rb
│   ├── process_order.rb
│   └── cancel_order.rb
├── payments/
│   ├── process_payment.rb
│   └── refund_payment.rb
└── notifications/
    ├── send_email.rb
    └── send_sms.rb
```

## Base Service Class (Optional)

```ruby
class ApplicationService
  def self.call(...)
    new(...).call
  end

  private

  def success(data = nil)
    ServiceResult.success(data)
  end

  def failure(error)
    ServiceResult.failure(error)
  end
end

# Usage
class CreateOrder < ApplicationService
  def initialize(user, params)
    @user = user
    @params = params
  end

  def call
    order = @user.orders.create!(@params)
    success(order)
  rescue ActiveRecord::RecordInvalid => e
    failure(e.message)
  end
end

# Call without .new
result = CreateOrder.call(user, params)
```
