# Class vs Module Decision Guide

Detailed guidance for choosing between class and module in Ruby.

## Decision Table

| Scenario | Use | Detection | Example |
|----------|-----|-----------|---------|
| Multiple instances with state | Class | Has `initialize` with instance variables | `Policy.new(holder: user)` |
| Stateless utility methods | Module with `extend self` | Class with only `self.` methods | `StringUtils.titleize(str)` |
| Named after design pattern | Rethink design | Grep for Factory/Decorator/Builder | `UserFactory` |
| Invalid after `.new` | Not a class | Required setter before use | `report.set_data(x)` |
| Simple data container | Struct or Data | Only `attr_accessor` and initialize | `Point.new(x: 1, y: 2)` |
| Shared behavior across classes | Module (mixin) | Duplicated methods in multiple classes | `include Archivable` |
| Namespace for constants/methods | Module | No instances needed | `Insurance::Rates::AUTO` |

## Scenario 1: Stateless Utility Classes

**Detection**: Classes with only class methods (`self.method_name`) and no instance variables.

```ruby
# Smell: Stateless class
class Formatter
  def self.currency(amount)
    "$#{'%.2f' % amount}"
  end

  def self.percentage(value)
    "#{(value * 100).round(1)}%"
  end

  def self.phone(number)
    number.gsub(/(\d{3})(\d{3})(\d{4})/, '(\1) \2-\3')
  end
end

# Better: Module with extend self
module Formatter
  extend self

  def currency(amount)
    "$#{'%.2f' % amount}"
  end

  def percentage(value)
    "#{(value * 100).round(1)}%"
  end

  def phone(number)
    number.gsub(/(\d{3})(\d{3})(\d{4})/, '(\1) \2-\3')
  end
end

# Usage remains the same
Formatter.currency(99.5)  # => "$99.50"
```

**Why Module is Better**:
- Clearer intent: "This is a namespace for functions"
- Can be included in other modules if needed
- No misleading `new` method available
- Methods can be called with or without the module prefix when included

## Scenario 2: Single-Method Service Classes

**Detection**: Classes with only `initialize` + one public method (usually `call`, `perform`, or `execute`).

```ruby
# Common pattern - but is it the right abstraction?
class SendWelcomeEmail
  def initialize(user)
    @user = user
  end

  def call
    UserMailer.welcome(@user).deliver_later
    track_onboarding_email
  end

  private

  def track_onboarding_email
    Analytics.track(@user, 'welcome_email_sent')
  end
end

# Usage
SendWelcomeEmail.new(user).call
```

**Questions to Ask**:
1. Will there ever be multiple instances alive simultaneously?
2. Does the object need to maintain state between method calls?
3. Is the `initialize` + `call` pattern adding clarity or ceremony?

**Alternative: Module Function**:
```ruby
module Onboarding
  extend self

  def send_welcome_email(user)
    UserMailer.welcome(user).deliver_later
    track_email(user, 'welcome_email_sent')
  end

  private

  def track_email(user, event)
    Analytics.track(user, event)
  end
end

# Usage
Onboarding.send_welcome_email(user)
```

**When Service Class IS Appropriate**:
```ruby
# Good: Maintains state across multiple operations
class BatchEmailSender
  def initialize(users)
    @users = users
    @sent_count = 0
    @failed = []
  end

  def send_all
    @users.each { |user| send_to(user) }
    self  # Returns self for chaining or inspection
  end

  def report
    { sent: @sent_count, failed: @failed }
  end

  private

  def send_to(user)
    UserMailer.welcome(user).deliver_later
    @sent_count += 1
  rescue => e
    @failed << { user: user, error: e.message }
  end
end
```

## Scenario 3: Classes Named After Design Patterns

**Detection**: `grep -r "class.*\(Factory\|Builder\|Decorator\|Adapter\|Strategy\)" app/`

Most Gang of Four patterns were workarounds for C++ and Java limitations. Ruby has built-in features that make many patterns unnecessary.

### Factory Pattern

```ruby
# Unnecessary in Ruby
class NotificationFactory
  def self.create(type, message)
    case type
    when :email then EmailNotification.new(message)
    when :sms then SmsNotification.new(message)
    when :push then PushNotification.new(message)
    end
  end
end

# Ruby way: Just use the classes directly
EmailNotification.new(message)

# Or if you need dynamic dispatch
NOTIFICATION_TYPES = {
  email: EmailNotification,
  sms: SmsNotification,
  push: PushNotification
}.freeze

def create_notification(type, message)
  NOTIFICATION_TYPES.fetch(type).new(message)
end
```

### Decorator Pattern

```ruby
# Java-style decorator
class LoggingDecorator
  def initialize(service)
    @service = service
  end

  def call(args)
    Rails.logger.info("Calling service with #{args}")
    result = @service.call(args)
    Rails.logger.info("Service returned #{result}")
    result
  end
end

# Ruby way: Use modules or SimpleDelegator
module Logging
  def call(args)
    Rails.logger.info("Calling with #{args}")
    super.tap { |result| Rails.logger.info("Returned #{result}") }
  end
end

class MyService
  prepend Logging
  # ...
end
```

### Strategy Pattern

```ruby
# Verbose strategy pattern
class PricingStrategy
  def calculate(order); raise NotImplementedError; end
end

class RegularPricing < PricingStrategy
  def calculate(order)
    order.subtotal
  end
end

class PremiumPricing < PricingStrategy
  def calculate(order)
    order.subtotal * 0.9
  end
end

# Ruby way: Use procs/lambdas or method objects
PRICING = {
  regular: ->(order) { order.subtotal },
  premium: ->(order) { order.subtotal * 0.9 }
}.freeze

def calculate_price(order, tier)
  PRICING.fetch(tier).call(order)
end
```

## Scenario 4: Abstract Base Classes

**Detection**: Classes with methods that raise `NotImplementedError` or "must override" comments.

```ruby
# Bad: Abstract base class (inheritance for method injection)
class BaseProcessor
  def process
    validate
    execute  # Must be implemented by subclass
    notify
  end

  def execute
    raise NotImplementedError, "Subclass must implement"
  end

  private

  def validate; end
  def notify; end
end

class OrderProcessor < BaseProcessor
  def execute
    # Actual implementation
  end
end
```

**Problem**: Using inheritance just to "inject" shared methods leads to:
- Tight coupling between parent and child
- Fragile base class problem
- Bloated objects with methods they don't need

**Better: Use Mixins**

```ruby
# Good: Composition with modules
module Processable
  def process
    validate
    execute
    notify
  end

  private

  def validate; end
  def notify; end
end

class OrderProcessor
  include Processable

  def execute
    # Implementation
  end
end

class RefundProcessor
  include Processable

  def execute
    # Different implementation
  end
end
```

## Scenario 5: Objects Invalid After Initialization

**Detection**: Look for patterns like:
- Required setter calls after `new`
- `setup` or `configure` methods
- Guards like `raise unless @configured`

```ruby
# Bad: Object invalid after .new
class ReportGenerator
  def initialize
    @template = nil
    @data = nil
  end

  def set_template(template)
    @template = template
    self
  end

  def set_data(data)
    @data = data
    self
  end

  def generate
    raise "Template required!" unless @template
    raise "Data required!" unless @data
    # ...
  end
end

# Usage requires ceremony
report = ReportGenerator.new
report.set_template(template)
report.set_data(data)
report.generate

# Good: Valid at birth
class ReportGenerator
  def initialize(template:, data:)
    @template = template
    @data = data
  end

  def generate
    # @template and @data guaranteed to exist
  end
end

# Clean usage
ReportGenerator.new(template: tmpl, data: d).generate
```

**If You Need Optional Configuration**:

```ruby
class ReportGenerator
  def initialize(template:, data:, options: {})
    @template = template
    @data = data
    @options = default_options.merge(options)
  end

  private

  def default_options
    { format: :pdf, include_header: true }
  end
end
```

## When to Use Class

Classes ARE appropriate when you need:

1. **Multiple instances with distinct state**
```ruby
policy1 = Policy.new(holder: alice, coverage: 100_000)
policy2 = Policy.new(holder: bob, coverage: 50_000)
```

2. **Behavior that operates on encapsulated state**
```ruby
class Account
  def initialize(balance:)
    @balance = balance
  end

  def deposit(amount)
    @balance += amount
  end

  def withdraw(amount)
    raise InsufficientFunds if amount > @balance
    @balance -= amount
  end
end
```

3. **Identity that matters**
```ruby
# Same data, different objects
user1 = User.new(name: "Alice")
user2 = User.new(name: "Alice")
user1 == user2  # Could be true or false depending on design
user1.object_id == user2.object_id  # Always false
```

4. **Lifecycle management**
```ruby
class DatabaseConnection
  def initialize(config)
    @connection = establish_connection(config)
  end

  def query(sql)
    @connection.execute(sql)
  end

  def close
    @connection.disconnect
    @connection = nil
  end
end
```

## Quick Reference

```
Is it stateless?
└── YES → Module with extend self

Does it have only one method?
└── Consider if a module function is clearer

Is it named Factory/Builder/Decorator/etc?
└── Rethink - Ruby probably has a simpler way

Must you call setters after .new?
└── Fix the initialize to require all dependencies

Is it just holding data?
└── Use Struct, Data, or Hash

Does it create multiple instances with state + behavior?
└── YES → Use Class (this is what classes are for!)
```
