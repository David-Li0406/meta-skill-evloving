# SOLID Principles Reference

## Single Responsibility Principle (SRP)

A class should have only one reason to change.

```ruby
# Bad: Multiple responsibilities
class User
  def authenticate(password); end
  def send_welcome_email; end
  def calculate_subscription_price; end
end

# Good: Single responsibility each
class User
  def authenticate(password); end
end

class UserMailer
  def send_welcome_email(user); end
end

class SubscriptionPricing
  def calculate(user); end
end
```

## Open/Closed Principle (OCP)

Open for extension, closed for modification.

```ruby
# Bad: Modifying existing code for new types
class PriceCalculator
  def calculate(item)
    case item.type
    when 'standard' then item.price
    when 'premium' then item.price * 1.2
    when 'vip' then item.price * 1.5  # Added later, modifies class
    end
  end
end

# Good: Extend via new classes
class StandardPricing
  def calculate(item) = item.price
end

class PremiumPricing
  def calculate(item) = item.price * 1.2
end

class VipPricing  # Added without modifying existing code
  def calculate(item) = item.price * 1.5
end
```

## Liskov Substitution Principle (LSP)

Subtypes must be substitutable for their base types.

```ruby
# Bad: Subtype changes expected behavior
class Bird
  def fly = "flying"
end

class Penguin < Bird
  def fly = raise "Penguins can't fly!"  # Violates LSP
end

# Good: Proper abstraction
class Bird
  def move = raise NotImplementedError
end

class FlyingBird < Bird
  def move = "flying"
end

class Penguin < Bird
  def move = "swimming"
end
```

## Interface Segregation Principle (ISP)

Prefer small, specific interfaces over large general ones.

```ruby
# Bad: Fat interface forcing empty implementations
module Worker
  def work; end
  def eat; end
  def sleep; end
end

class Robot
  include Worker
  def work = "working"
  def eat = nil  # Robots don't eat
  def sleep = nil  # Robots don't sleep
end

# Good: Segregated interfaces
module Workable
  def work; end
end

module Eatable
  def eat; end
end

class Robot
  include Workable
  def work = "working"
end

class Human
  include Workable, Eatable
  def work = "working"
  def eat = "eating"
end
```

## Dependency Inversion Principle (DIP)

Depend on abstractions, not concretions.

```ruby
# Bad: High-level depends on low-level
class OrderProcessor
  def initialize
    @notifier = EmailNotifier.new  # Direct dependency
  end

  def process(order)
    # process order
    @notifier.notify(order)
  end
end

# Good: Depend on abstraction (injection)
class OrderProcessor
  def initialize(notifier:)
    @notifier = notifier  # Injected abstraction
  end

  def process(order)
    # process order
    @notifier.notify(order)
  end
end

# Usage: inject any notifier that responds to #notify
OrderProcessor.new(notifier: EmailNotifier.new)
OrderProcessor.new(notifier: SmsNotifier.new)
OrderProcessor.new(notifier: NullNotifier.new)  # For testing
```
