# Data Structures: Struct, Data, and Hash

Choosing the right data container in Ruby.

## Overview

| Construct | Use Case | Mutability | Ruby Version |
|-----------|----------|------------|--------------|
| Hash | Ad-hoc, temporary data | Mutable | All |
| Struct | Simple data with optional behavior | Mutable | All |
| Data | Immutable value objects | Immutable | 3.2+ |
| Class | Complex objects with state + behavior | Configurable | All |

## Hash

**Best for**: Ad-hoc data grouping, configuration, temporary structures.

```ruby
# Good uses of Hash
config = { host: 'localhost', port: 3000, ssl: true }

api_response = { status: 200, body: data, headers: headers }

options = { format: :json, include: [:author, :comments] }
```

**Advantages**:
- No class definition needed
- Flexible structure
- Easy to construct inline
- Great for one-off data

**Disadvantages**:
- No type checking
- Easy to misspell keys
- No methods/behavior
- No documentation of expected keys

### When to Graduate from Hash

Consider upgrading to Struct when:
- You access the same keys repeatedly
- You pass the hash to multiple methods
- You want to add behavior
- You need documentation of the structure

```ruby
# Time to upgrade: Hash used everywhere
def process_order(order_data)
  validate(order_data[:items], order_data[:total])
  ship_to(order_data[:address])
  charge(order_data[:payment])
end

# Better: Struct with clear structure
OrderData = Struct.new(:items, :total, :address, :payment, keyword_init: true)

def process_order(order)
  validate(order.items, order.total)
  ship_to(order.address)
  charge(order.payment)
end
```

## Struct

**Best for**: Simple data containers, potentially with behavior.

### Basic Struct

```ruby
# Define with positional arguments
Point = Struct.new(:x, :y)
point = Point.new(10, 20)
point.x  # => 10

# Define with keyword arguments (recommended)
Point = Struct.new(:x, :y, keyword_init: true)
point = Point.new(x: 10, y: 20)
```

### Struct with Behavior

```ruby
Point = Struct.new(:x, :y, keyword_init: true) do
  def distance_from_origin
    Math.sqrt(x**2 + y**2)
  end

  def translate(dx, dy)
    Point.new(x: x + dx, y: y + dy)
  end

  def to_s
    "(#{x}, #{y})"
  end
end

point = Point.new(x: 3, y: 4)
point.distance_from_origin  # => 5.0
point.translate(1, 1)       # => Point(x: 4, y: 5)
```

### Struct vs Class Comparison

```ruby
# Class version (verbose)
class Person
  attr_accessor :name, :email, :age

  def initialize(name:, email:, age:)
    @name = name
    @email = email
    @age = age
  end

  def ==(other)
    name == other.name && email == other.email && age == other.age
  end

  def to_s
    "Person(name: #{name}, email: #{email}, age: #{age})"
  end
end

# Struct version (concise)
Person = Struct.new(:name, :email, :age, keyword_init: true) do
  def to_s
    "Person(name: #{name}, email: #{email}, age: #{age})"
  end
end

# Both work the same way
person = Person.new(name: "Alice", email: "alice@example.com", age: 30)
```

### Frozen Struct (Pre-Ruby 3.2 Immutability)

```ruby
# For immutable value objects before Ruby 3.2
Point = Struct.new(:x, :y, keyword_init: true) do
  def initialize(*)
    super
    freeze
  end

  def translate(dx, dy)
    Point.new(x: x + dx, y: y + dy)  # Returns new instance
  end
end

point = Point.new(x: 1, y: 2)
point.x = 5  # => FrozenError: can't modify frozen Point
```

## Data (Ruby 3.2+)

**Best for**: Immutable value objects.

### Checking Ruby Version

Before using Data, verify Ruby version:

```ruby
# Check in code
if RUBY_VERSION >= '3.2'
  # Can use Data
end

# Check .ruby-version file
# Check Gemfile for ruby version constraint
```

**Detection for this skill**:
```bash
# Check Ruby version in project
cat .ruby-version 2>/dev/null || grep "ruby" Gemfile | head -1
```

### Basic Data Usage

```ruby
# Define immutable value object
Point = Data.define(:x, :y)

point = Point.new(x: 10, y: 20)
point.x  # => 10

# Immutable by default
point.x = 5  # => NoMethodError (no setter!)
```

### Data with Behavior

```ruby
Point = Data.define(:x, :y) do
  def distance_from_origin
    Math.sqrt(x**2 + y**2)
  end

  def translate(dx, dy)
    with(x: x + dx, y: y + dy)  # Built-in method to create modified copy
  end

  def to_s
    "(#{x}, #{y})"
  end
end

point = Point.new(x: 3, y: 4)
point.distance_from_origin  # => 5.0

moved = point.translate(1, 1)  # => Point(x: 4, y: 5)
point  # => Point(x: 3, y: 4) - unchanged!
```

### Data vs Struct

| Feature | Struct | Data |
|---------|--------|------|
| Mutable | Yes | No |
| `with` method | No | Yes |
| Setters | Yes | No |
| `keyword_init` | Must specify | Default |
| Ruby version | All | 3.2+ |

```ruby
# Struct is mutable
StructPoint = Struct.new(:x, :y, keyword_init: true)
sp = StructPoint.new(x: 1, y: 2)
sp.x = 10  # Works

# Data is immutable
DataPoint = Data.define(:x, :y)
dp = DataPoint.new(x: 1, y: 2)
dp.x = 10  # NoMethodError

# Data has `with` for creating modified copies
DataPoint.new(x: 1, y: 2).with(x: 10)  # => DataPoint(x: 10, y: 2)
```

### Fallback Strategy for Pre-3.2 Ruby

```ruby
# Pattern: Conditional definition
if RUBY_VERSION >= '3.2'
  Point = Data.define(:x, :y) do
    def translate(dx, dy)
      with(x: x + dx, y: y + dy)
    end
  end
else
  Point = Struct.new(:x, :y, keyword_init: true) do
    def initialize(*)
      super
      freeze
    end

    def translate(dx, dy)
      Point.new(x: x + dx, y: y + dy)
    end
  end
end
```

## Graduation Path: Hash -> Struct -> Data -> Class

### Level 1: Hash
```ruby
# Start simple
point = { x: 10, y: 20 }
```

### Level 2: Struct (add structure)
```ruby
# Need clearer interface
Point = Struct.new(:x, :y, keyword_init: true)
```

### Level 3: Struct with Behavior
```ruby
# Need methods
Point = Struct.new(:x, :y, keyword_init: true) do
  def distance_from_origin
    Math.sqrt(x**2 + y**2)
  end
end
```

### Level 4: Data (need immutability)
```ruby
# Ruby 3.2+, need immutability
Point = Data.define(:x, :y) do
  def distance_from_origin
    Math.sqrt(x**2 + y**2)
  end
end
```

### Level 5: Class (need full control)
```ruby
# Need private state, complex initialization, or lifecycle
class Point
  def initialize(x:, y:)
    @x = x.to_f
    @y = y.to_f
    validate!
    freeze
  end

  attr_reader :x, :y

  def distance_from_origin
    Math.sqrt(x**2 + y**2)
  end

  private

  def validate!
    raise ArgumentError, "Coordinates must be numeric" unless @x.is_a?(Numeric)
  end
end
```

## Common Patterns

### Value Objects

```ruby
# Money value object (Data for Ruby 3.2+)
Money = Data.define(:amount, :currency) do
  def +(other)
    raise "Currency mismatch" unless currency == other.currency
    with(amount: amount + other.amount)
  end

  def to_s
    "#{currency} #{amount}"
  end
end

# For pre-3.2
Money = Struct.new(:amount, :currency, keyword_init: true) do
  def initialize(*)
    super
    freeze
  end

  def +(other)
    raise "Currency mismatch" unless currency == other.currency
    Money.new(amount: amount + other.amount, currency: currency)
  end
end
```

### Parameter Objects

```ruby
# Group related parameters
SearchParams = Struct.new(:query, :page, :per_page, :filters, keyword_init: true) do
  def offset
    (page - 1) * per_page
  end

  def to_query_string
    "q=#{query}&page=#{page}&per_page=#{per_page}"
  end
end

def search(params)
  results = Model.where(params.filters)
                 .search(params.query)
                 .offset(params.offset)
                 .limit(params.per_page)
end
```

### Configuration Objects

```ruby
# Immutable configuration
AppConfig = Data.define(:database_url, :redis_url, :api_key, :environment) do
  def production?
    environment == 'production'
  end

  def test?
    environment == 'test'
  end
end

CONFIG = AppConfig.new(
  database_url: ENV['DATABASE_URL'],
  redis_url: ENV['REDIS_URL'],
  api_key: ENV['API_KEY'],
  environment: ENV['RAILS_ENV']
)
```

### Result Objects

```ruby
# Operation result (success/failure)
Result = Data.define(:success, :value, :error) do
  def self.success(value)
    new(success: true, value: value, error: nil)
  end

  def self.failure(error)
    new(success: false, value: nil, error: error)
  end

  def success?
    success
  end

  def failure?
    !success
  end
end

def divide(a, b)
  return Result.failure("Division by zero") if b.zero?
  Result.success(a / b)
end
```

## Quick Decision Guide

```
Is this temporary/one-off data?
└── YES → Hash

Do you need a named structure with accessors?
├── Is immutability important?
│   ├── Ruby 3.2+? → Data
│   └── Pre-3.2? → Frozen Struct
└── Mutability OK? → Struct

Do you need complex initialization, private state, or lifecycle?
└── YES → Class
```

## Context Awareness

| Pattern | Detection | Ruby Version | Recommendation |
|---------|-----------|--------------|----------------|
| Hash everywhere | Same keys in multiple places | Any | Upgrade to Struct |
| Mutable data objects | Struct without freeze | Any | Consider Data (3.2+) |
| PORO with only attrs | Class with only attr_* | Any | Use Struct instead |
| Value object | Needs immutability | 3.2+ | Use Data |
| Value object | Needs immutability | < 3.2 | Use frozen Struct |
| Complex object | State + behavior + lifecycle | Any | Class is appropriate |
