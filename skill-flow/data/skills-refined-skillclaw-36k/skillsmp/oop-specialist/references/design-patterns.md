# Design Patterns Reference

## Factory Pattern

Encapsulate object creation logic.

```ruby
class NotificationFactory
  def self.create(type, recipient)
    case type
    when :email then EmailNotification.new(recipient)
    when :sms then SmsNotification.new(recipient)
    when :push then PushNotification.new(recipient)
    else raise ArgumentError, "Unknown type: #{type}"
    end
  end
end

# Usage
notification = NotificationFactory.create(:email, user)
```

## Builder Pattern

Construct complex objects step-by-step.

```ruby
class WorkoutBuilder
  def initialize
    @workout = Workout.new
  end

  def with_warmup(exercises)
    @workout.warmup = exercises
    self
  end

  def with_main_sets(sets)
    @workout.main_sets = sets
    self
  end

  def with_cooldown(exercises)
    @workout.cooldown = exercises
    self
  end

  def build
    @workout
  end
end

# Usage
workout = WorkoutBuilder.new
  .with_warmup(warmup_exercises)
  .with_main_sets(strength_sets)
  .with_cooldown(stretches)
  .build
```

## Strategy Pattern

Interchangeable algorithms.

```ruby
class PricingStrategy
  def calculate(order)
    raise NotImplementedError
  end
end

class StandardPricing < PricingStrategy
  def calculate(order)
    order.items.sum(&:price)
  end
end

class DiscountPricing < PricingStrategy
  def initialize(discount_percent)
    @discount = discount_percent / 100.0
  end

  def calculate(order)
    order.items.sum(&:price) * (1 - @discount)
  end
end

class Order
  def initialize(pricing_strategy:)
    @pricing_strategy = pricing_strategy
  end

  def total
    @pricing_strategy.calculate(self)
  end
end

# Usage
order = Order.new(pricing_strategy: DiscountPricing.new(20))
```

## State Pattern

Behavior changes based on internal state.

```ruby
class SubscriptionState
  def activate(subscription); end
  def cancel(subscription); end
  def renew(subscription); end
end

class ActiveState < SubscriptionState
  def cancel(subscription)
    subscription.state = CancelledState.new
  end

  def renew(subscription)
    subscription.extend_by(30.days)
  end
end

class CancelledState < SubscriptionState
  def activate(subscription)
    subscription.state = ActiveState.new
  end

  def cancel(subscription)
    # Already cancelled, no-op
  end
end

class Subscription
  attr_accessor :state

  def initialize
    @state = ActiveState.new
  end

  def cancel
    @state.cancel(self)
  end
end
```

## Facade Pattern

Simplify complex subsystem interfaces.

```ruby
class PaymentFacade
  def initialize(user)
    @user = user
    @stripe = StripeClient.new
    @tax_calculator = TaxCalculator.new
    @invoice_generator = InvoiceGenerator.new
  end

  def process_payment(amount)
    tax = @tax_calculator.calculate(amount, @user.region)
    total = amount + tax

    charge = @stripe.charge(@user.payment_method, total)
    @invoice_generator.create(@user, charge)

    charge
  end
end

# Usage: Simple interface hiding complexity
PaymentFacade.new(user).process_payment(100)
```

## Template Method Pattern

Define algorithm skeleton, let subclasses override steps.

```ruby
class DataExporter
  def export(data)
    validate(data)
    formatted = format(data)
    write(formatted)
    notify_completion
  end

  private

  def validate(data)
    raise ArgumentError if data.empty?
  end

  def format(data)
    raise NotImplementedError  # Subclasses implement
  end

  def write(formatted)
    raise NotImplementedError  # Subclasses implement
  end

  def notify_completion
    # Default: do nothing, subclasses can override
  end
end

class CsvExporter < DataExporter
  def format(data)
    data.map { |row| row.join(',') }.join("\n")
  end

  def write(formatted)
    File.write('export.csv', formatted)
  end
end

class JsonExporter < DataExporter
  def format(data)
    data.to_json
  end

  def write(formatted)
    File.write('export.json', formatted)
  end
end
```

## Null Object Pattern

Avoid nil checks with default behavior objects.

```ruby
class NullNotifier
  def notify(message)
    # Do nothing - intentionally empty
  end
end

class EmailNotifier
  def notify(message)
    # Send actual email
  end
end

class Order
  def initialize(notifier: NullNotifier.new)
    @notifier = notifier
  end

  def complete
    # process order
    @notifier.notify("Order completed")  # No nil check needed
  end
end

# Usage
Order.new.complete  # Uses NullNotifier, no notification
Order.new(notifier: EmailNotifier.new).complete  # Sends email
```

## Delegation Pattern

Forward messages to collaborating objects.

```ruby
class Client
  def initialize(coach)
    @coach = coach
  end

  def coach_name
    @coach.name  # Delegation
  end

  def coach_email
    @coach.email  # Delegation
  end
end

# With Ruby's Forwardable
require 'forwardable'

class Client
  extend Forwardable

  def_delegators :@coach, :name, :email

  def initialize(coach)
    @coach = coach
  end
end
```
