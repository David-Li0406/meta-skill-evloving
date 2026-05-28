# GRASP Principles Reference

## Information Expert

Assign responsibility to the class with the information needed.

```ruby
# Bad: External class calculates order total
class OrderCalculator
  def total(order)
    order.items.sum { |i| i.price * i.quantity }
  end
end

# Good: Order calculates its own total (it has the items)
class Order
  def total
    items.sum { |i| i.price * i.quantity }
  end
end
```

## Creator

Create objects where they're contained, aggregated, or closely used.

```ruby
# Good: Order creates its own items (contains them)
class Order
  def add_item(product, quantity)
    items << OrderItem.new(product: product, quantity: quantity)
  end
end

# Good: Factory creates when creation is complex
class WorkoutFactory
  def create_for_client(client, template)
    workout = Workout.new(client: client)
    template.exercises.each do |ex|
      workout.add_exercise(ex.dup)
    end
    workout
  end
end
```

## Low Coupling

Minimize dependencies between classes.

```ruby
# Bad: High coupling - Order knows too much about Payment
class Order
  def process
    payment = StripePayment.new(
      api_key: ENV['STRIPE_KEY'],
      amount: total,
      currency: 'USD'
    )
    payment.charge(customer.stripe_id)
    payment.create_invoice
    payment.send_receipt_email
  end
end

# Good: Low coupling - Order uses abstraction
class Order
  def process(payment_processor)
    payment_processor.charge(total)
  end
end
```

## High Cohesion

Keep class responsibilities focused and related.

```ruby
# Bad: Low cohesion - User does too many unrelated things
class User
  def authenticate(password); end
  def send_email(subject, body); end
  def generate_pdf_report; end
  def calculate_taxes; end
end

# Good: High cohesion - Each class has one focus
class User
  def authenticate(password); end
end

class UserMailer
  def send(user, subject, body); end
end

class ReportGenerator
  def generate_pdf(user); end
end
```

## Controller

Delegate system events to controller objects.

```ruby
# In Rails, controllers handle HTTP events
class WorkoutsController
  def create
    # Controller receives event, delegates to service
    CreateWorkout.new(
      current_coach: current_coach,
      client: @client,
      workout_params: workout_params
    ).execute
  end
end
```

## Polymorphism

Use polymorphic methods instead of conditionals on type.

```ruby
# Bad: Type checking with conditionals
def calculate_price(item)
  case item.type
  when 'standard' then item.base_price
  when 'premium' then item.base_price * 1.5
  when 'enterprise' then item.base_price * 2.0
  end
end

# Good: Polymorphic pricing
class StandardItem
  def price = base_price
end

class PremiumItem
  def price = base_price * 1.5
end

class EnterpriseItem
  def price = base_price * 2.0
end

# Usage: No conditionals needed
item.price
```

## Pure Fabrication

Create a class when no domain class fits the responsibility.

```ruby
# No natural domain object for persistence
class WorkoutRepository
  def save(workout)
    # Handle database persistence
  end

  def find_by_client(client)
    # Query and return workouts
  end
end

# No natural domain object for external API communication
class StripeGateway
  def charge(amount, customer_id)
    # Handle Stripe API interaction
  end
end
```

## Protected Variations

Isolate change-prone areas behind stable interfaces.

```ruby
# Interface protects against notification implementation changes
class NotificationService
  def initialize(notifier)
    @notifier = notifier
  end

  def notify(user, message)
    @notifier.send(user, message)
  end
end

# Implementations can change without affecting callers
class EmailNotifier
  def send(user, message)
    # Email implementation
  end
end

class PushNotifier
  def send(user, message)
    # Push notification implementation
  end
end

# If we switch from email to push, only configuration changes
```

## Indirection

Use intermediary objects to decouple components.

```ruby
# Direct coupling
class Order
  def save
    Database.insert(self)  # Direct dependency
  end
end

# Indirection via repository
class Order
  def save(repository)
    repository.save(self)  # Indirect, decoupled
  end
end

class OrderRepository
  def save(order)
    Database.insert(order.to_hash)
  end
end
```
