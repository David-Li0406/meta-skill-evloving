---
name: design-patterns
description: This skill should be used when the user asks about "design patterns", "SOLID", "factory pattern", "singleton", "observer", "strategy", "decorator", "adapter", "facade", "command pattern", "builder pattern", "dependency injection", "composition", "Ruby patterns", or needs guidance on implementing design patterns in Ruby.
version: 1.0.0
---

# Design Patterns in Ruby

Idiomatic Ruby implementations of common design patterns.

## SOLID Principles in Ruby

### Single Responsibility Principle

```ruby
# Bad: User handles too many concerns
class User
  def save
    validate!
    Database.insert(self)
    Mailer.send_welcome_email(self)
    Analytics.track("user_created", self)
  end
end

# Good: Each class has one reason to change
class User
  def save
    validate!
    UserRepository.save(self)
  end
end

class UserRegistrationService
  def initialize(user)
    @user = user
  end

  def call
    @user.save
    WelcomeMailer.deliver(@user)
    Analytics.track("user_created", @user)
  end
end
```

### Open/Closed Principle

```ruby
# Open for extension, closed for modification
class PaymentProcessor
  def initialize(strategy)
    @strategy = strategy
  end

  def process(amount)
    @strategy.charge(amount)
  end
end

class StripePayment
  def charge(amount)
    Stripe::Charge.create(amount: amount)
  end
end

class PaypalPayment
  def charge(amount)
    Paypal::Payment.execute(amount)
  end
end

# Add new payment methods without modifying PaymentProcessor
class CryptoPayment
  def charge(amount)
    Crypto::Transaction.send(amount)
  end
end
```

### Liskov Substitution Principle

```ruby
# Subtypes must be substitutable for their base types
class Bird
  def fly
    raise NotImplementedError
  end
end

# Bad: Penguin can't fly, violates LSP
class Penguin < Bird
  def fly
    raise "Penguins can't fly!"
  end
end

# Good: Separate flying capability
module Flyable
  def fly
    raise NotImplementedError
  end
end

class Bird; end

class Sparrow < Bird
  include Flyable

  def fly
    "Flying high!"
  end
end

class Penguin < Bird
  def swim
    "Swimming fast!"
  end
end
```

### Interface Segregation Principle

```ruby
# Prefer small, focused interfaces
# Bad: One big interface
module Worker
  def work; end
  def eat; end
  def sleep; end
end

# Good: Separate concerns
module Workable
  def work
    raise NotImplementedError
  end
end

module Feedable
  def eat
    raise NotImplementedError
  end
end

class Human
  include Workable
  include Feedable

  def work = "Working..."
  def eat = "Eating..."
end

class Robot
  include Workable

  def work = "Processing..."
  # Robots don't need to eat
end
```

### Dependency Inversion Principle

```ruby
# Depend on abstractions, not concretions
# Bad: High-level module depends on low-level module
class Report
  def initialize
    @formatter = HTMLFormatter.new
  end

  def generate(data)
    @formatter.format(data)
  end
end

# Good: Depend on abstraction (duck typing in Ruby)
class Report
  def initialize(formatter)
    @formatter = formatter
  end

  def generate(data)
    @formatter.format(data)
  end
end

class HTMLFormatter
  def format(data) = "<html>#{data}</html>"
end

class JSONFormatter
  def format(data) = data.to_json
end

Report.new(HTMLFormatter.new).generate(data)
Report.new(JSONFormatter.new).generate(data)
```

## Creational Patterns

### Factory Method

```ruby
class DocumentFactory
  def self.create(type, **options)
    case type
    when :pdf then PDFDocument.new(**options)
    when :word then WordDocument.new(**options)
    when :html then HTMLDocument.new(**options)
    else raise ArgumentError, "Unknown document type: #{type}"
    end
  end
end

document = DocumentFactory.create(:pdf, title: "Report")
```

### Abstract Factory

```ruby
class UIFactory
  def create_button
    raise NotImplementedError
  end

  def create_input
    raise NotImplementedError
  end
end

class DarkThemeFactory < UIFactory
  def create_button = DarkButton.new
  def create_input = DarkInput.new
end

class LightThemeFactory < UIFactory
  def create_button = LightButton.new
  def create_input = LightInput.new
end

def build_form(factory)
  button = factory.create_button
  input = factory.create_input
  Form.new(button, input)
end
```

### Builder

```ruby
class QueryBuilder
  def initialize
    @select = "*"
    @from = nil
    @where = []
    @order = nil
    @limit = nil
  end

  def select(*columns)
    @select = columns.join(", ")
    self
  end

  def from(table)
    @from = table
    self
  end

  def where(condition)
    @where << condition
    self
  end

  def order(column, direction = :asc)
    @order = "#{column} #{direction.upcase}"
    self
  end

  def limit(n)
    @limit = n
    self
  end

  def to_sql
    sql = "SELECT #{@select} FROM #{@from}"
    sql += " WHERE #{@where.join(' AND ')}" if @where.any?
    sql += " ORDER BY #{@order}" if @order
    sql += " LIMIT #{@limit}" if @limit
    sql
  end
end

query = QueryBuilder.new
  .select(:id, :name, :email)
  .from(:users)
  .where("active = true")
  .where("created_at > '2024-01-01'")
  .order(:created_at, :desc)
  .limit(10)
  .to_sql
```

### Singleton (Using Module)

```ruby
# Ruby-idiomatic singleton using module
module Configuration
  class << self
    attr_accessor :api_key, :environment

    def configure
      yield self
    end

    def production?
      environment == :production
    end
  end
end

Configuration.configure do |config|
  config.api_key = "secret"
  config.environment = :production
end

Configuration.api_key  # => "secret"
```

## Structural Patterns

### Decorator (Using Modules)

```ruby
class Coffee
  def cost = 2.0
  def description = "Coffee"
end

module Milk
  def cost = super + 0.5
  def description = "#{super} with milk"
end

module Sugar
  def cost = super + 0.25
  def description = "#{super} with sugar"
end

module Whip
  def cost = super + 0.75
  def description = "#{super} with whip"
end

coffee = Coffee.new
coffee.extend(Milk)
coffee.extend(Sugar)
coffee.extend(Whip)

coffee.description  # => "Coffee with milk with sugar with whip"
coffee.cost         # => 3.5
```

### Adapter

```ruby
# Existing interface
class OldPrinter
  def print_document(text)
    puts "Printing: #{text}"
  end
end

# New interface we want to use
class ModernPrinter
  def render(document)
    puts "Rendering: #{document.content}"
  end
end

# Adapter
class PrinterAdapter
  def initialize(modern_printer)
    @printer = modern_printer
  end

  def print_document(text)
    document = OpenStruct.new(content: text)
    @printer.render(document)
  end
end

# Usage
printer = PrinterAdapter.new(ModernPrinter.new)
printer.print_document("Hello")  # Works with old interface
```

### Facade

```ruby
class OrderFacade
  def initialize(user)
    @user = user
    @cart = ShoppingCart.new(user)
    @inventory = InventoryService.new
    @payment = PaymentService.new
    @shipping = ShippingService.new
  end

  def place_order(payment_details)
    items = @cart.items

    # Complex subsystem interactions hidden
    @inventory.reserve(items)
    @payment.charge(@user, @cart.total, payment_details)
    order = Order.create(user: @user, items: items)
    @shipping.schedule(order)
    @cart.clear

    order
  rescue PaymentError => e
    @inventory.release(items)
    raise
  end
end

# Simple interface for clients
facade = OrderFacade.new(current_user)
order = facade.place_order(credit_card_info)
```

## Behavioral Patterns

### Strategy (Using Blocks/Procs)

```ruby
class Sorter
  def initialize(&strategy)
    @strategy = strategy || ->(a, b) { a <=> b }
  end

  def sort(items)
    items.sort(&@strategy)
  end
end

# Different strategies
by_name = Sorter.new { |a, b| a.name <=> b.name }
by_price = Sorter.new { |a, b| a.price <=> b.price }
by_date_desc = Sorter.new { |a, b| b.date <=> a.date }

by_name.sort(products)
by_price.sort(products)
```

### Observer

```ruby
module Observable
  def add_observer(observer)
    observers << observer
  end

  def remove_observer(observer)
    observers.delete(observer)
  end

  def notify_observers(event, data = nil)
    observers.each { |o| o.update(event, data) }
  end

  private

  def observers
    @observers ||= []
  end
end

class Order
  include Observable

  attr_reader :status

  def complete!
    @status = :completed
    notify_observers(:order_completed, self)
  end
end

class EmailNotifier
  def update(event, order)
    case event
    when :order_completed
      send_confirmation_email(order)
    end
  end
end

class InventoryTracker
  def update(event, order)
    case event
    when :order_completed
      reduce_stock(order.items)
    end
  end
end

order = Order.new
order.add_observer(EmailNotifier.new)
order.add_observer(InventoryTracker.new)
order.complete!
```

### Command

```ruby
class Command
  def execute
    raise NotImplementedError
  end

  def undo
    raise NotImplementedError
  end
end

class AddItemCommand < Command
  def initialize(cart, item)
    @cart = cart
    @item = item
  end

  def execute
    @cart.add(@item)
  end

  def undo
    @cart.remove(@item)
  end
end

class CommandHistory
  def initialize
    @history = []
  end

  def execute(command)
    command.execute
    @history.push(command)
  end

  def undo
    command = @history.pop
    command&.undo
  end
end

history = CommandHistory.new
history.execute(AddItemCommand.new(cart, item1))
history.execute(AddItemCommand.new(cart, item2))
history.undo  # Removes item2
```

## Additional Resources

### Reference Files

- **`references/pattern-examples.md`** - Extended examples and anti-patterns

