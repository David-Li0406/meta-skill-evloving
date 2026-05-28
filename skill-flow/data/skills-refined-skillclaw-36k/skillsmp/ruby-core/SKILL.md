---
name: ruby-core
description: This skill should be used when the user asks about "Ruby basics", "blocks", "procs", "lambdas", "enumerables", "iterators", "pattern matching", "error handling", "exceptions", "Ruby 3 features", "Ractors", "Data class", "endless methods", "refinements", or needs guidance on Ruby language features and idioms.
version: 1.0.0
---

# Ruby Core Language Features

Comprehensive guide to Ruby 3.x core language features, idioms, and best practices.

## Blocks, Procs, and Lambdas

### Blocks

Blocks are anonymous functions passed to methods:

```ruby
# Block with do...end (multi-line)
[1, 2, 3].each do |n|
  puts n * 2
end

# Block with braces (single-line, returns value)
doubled = [1, 2, 3].map { |n| n * 2 }

# Yielding to blocks
def with_timing
  start = Time.now
  result = yield
  puts "Took #{Time.now - start}s"
  result
end

with_timing { expensive_operation }

# Block with arguments
def transform(value)
  yield(value) if block_given?
end

transform(5) { |n| n * 2 }  # => 10

# Capturing blocks as Proc
def save_block(&block)
  @callback = block
end
```

### Procs vs Lambdas

```ruby
# Proc - flexible argument handling, returns from enclosing method
my_proc = Proc.new { |a, b| a + b }
my_proc = proc { |a, b| a + b }

my_proc.call(1, 2)     # => 3
my_proc.call(1, 2, 3)  # => 3 (extra args ignored)
my_proc.call(1)        # => TypeError (nil + 1)

# Lambda - strict argument checking, returns to caller
my_lambda = ->(a, b) { a + b }
my_lambda = lambda { |a, b| a + b }

my_lambda.call(1, 2)     # => 3
my_lambda.call(1, 2, 3)  # ArgumentError
my_lambda.call(1)        # ArgumentError

# Key difference: return behavior
def proc_return
  p = Proc.new { return "from proc" }
  p.call
  "after proc"  # Never reached
end

def lambda_return
  l = -> { return "from lambda" }
  l.call
  "after lambda"  # This executes
end
```

### Method Objects

```ruby
# Convert method to proc
def double(n) = n * 2

[1, 2, 3].map(&method(:double))  # => [2, 4, 6]

# Unbound methods
unbound = String.instance_method(:upcase)
bound = unbound.bind("hello")
bound.call  # => "HELLO"
```

## Enumerables

### Core Enumerable Methods

```ruby
numbers = [1, 2, 3, 4, 5]

# Transformation
numbers.map { |n| n * 2 }           # => [2, 4, 6, 8, 10]
numbers.flat_map { |n| [n, n * 2] } # => [1, 2, 2, 4, 3, 6, 4, 8, 5, 10]

# Filtering
numbers.select { |n| n.even? }      # => [2, 4]
numbers.reject { |n| n.even? }      # => [1, 3, 5]
numbers.filter_map { |n| n * 2 if n.even? }  # => [4, 8]

# Reduction
numbers.reduce(0) { |sum, n| sum + n }  # => 15
numbers.reduce(:+)                       # => 15
numbers.sum                              # => 15

# Searching
numbers.find { |n| n > 3 }          # => 4
numbers.find_index { |n| n > 3 }    # => 3
numbers.any? { |n| n > 3 }          # => true
numbers.all? { |n| n > 0 }          # => true
numbers.none? { |n| n > 10 }        # => true
numbers.one? { |n| n == 3 }         # => true

# Grouping
numbers.group_by { |n| n % 2 }      # => {1=>[1,3,5], 0=>[2,4]}
numbers.partition { |n| n.even? }   # => [[2,4], [1,3,5]]
numbers.tally                        # Count occurrences

# Ordering
numbers.sort_by { |n| -n }          # => [5, 4, 3, 2, 1]
numbers.max_by { |n| n % 3 }        # => 2
numbers.min_by { |n| n % 3 }        # => 3

# Chaining
numbers.lazy.select { |n| n.even? }.map { |n| n * 2 }.first(2)
```

### Lazy Enumerables

```ruby
# Process large/infinite sequences efficiently
(1..Float::INFINITY)
  .lazy
  .select { |n| n % 3 == 0 }
  .map { |n| n * 2 }
  .first(5)
# => [6, 12, 18, 24, 30]

# Memory-efficient file processing
File.foreach("large_file.txt")
    .lazy
    .map(&:chomp)
    .select { |line| line.include?("ERROR") }
    .first(10)
```

## Pattern Matching (Ruby 3.x)

### Basic Patterns

```ruby
case value
in Integer => n if n > 0
  "positive integer: #{n}"
in Integer
  "non-positive integer"
in String => s
  "string: #{s}"
in [first, *rest]
  "array starting with #{first}"
in { name:, age: }
  "person: #{name}, #{age}"
in nil
  "nothing"
else
  "unknown"
end
```

### Array Patterns

```ruby
case [1, 2, 3]
in [a, b, c]
  "three elements: #{a}, #{b}, #{c}"
in [head, *tail]
  "head: #{head}, tail: #{tail}"
in [*, last]
  "last element: #{last}"
in [first, *, last]
  "first: #{first}, last: #{last}"
end
```

### Hash Patterns

```ruby
case { name: "Alice", age: 30, role: "admin" }
in { name: "Alice", role: }
  "Alice is #{role}"
in { name:, age: 18.. }
  "#{name} is an adult"
in { **rest }
  "other: #{rest}"
end
```

### Guard Clauses

```ruby
case number
in n if n.negative?
  "negative"
in n if n.zero?
  "zero"
in n if n.positive?
  "positive"
end
```

### Pinning

```ruby
expected = 42

case value
in ^expected
  "matched expected value"
in other
  "got #{other} instead of #{expected}"
end
```

## Error Handling

### Exception Basics

```ruby
begin
  risky_operation
rescue SpecificError => e
  handle_specific_error(e)
rescue StandardError => e
  handle_general_error(e)
else
  # Runs if no exception
  success_callback
ensure
  # Always runs
  cleanup
end

# Inline rescue (use sparingly)
value = risky_operation rescue default_value

# Retry pattern
attempts = 0
begin
  attempts += 1
  unreliable_api_call
rescue NetworkError
  retry if attempts < 3
  raise
end
```

### Custom Exceptions

```ruby
class ApplicationError < StandardError; end

class ValidationError < ApplicationError
  attr_reader :field, :value

  def initialize(message, field:, value:)
    @field = field
    @value = value
    super(message)
  end
end

raise ValidationError.new("Invalid email", field: :email, value: input)
```

### Exception Hierarchy

```
Exception
├── NoMemoryError
├── ScriptError
├── SignalException
├── SystemExit
└── StandardError (catch this, not Exception)
    ├── ArgumentError
    ├── IOError
    ├── NameError
    │   └── NoMethodError
    ├── RangeError
    ├── RuntimeError (default for `raise`)
    ├── TypeError
    └── ZeroDivisionError
```

## Ruby 3.x Features

### Data Classes (Ruby 3.2+)

```ruby
# Immutable value objects
Point = Data.define(:x, :y)

p = Point.new(1, 2)
p.x           # => 1
p.with(x: 10) # => Point(x: 10, y: 2)

# With methods
Point = Data.define(:x, :y) do
  def distance_from_origin
    Math.sqrt(x**2 + y**2)
  end
end
```

### Ractors (Parallel Execution)

```ruby
# True parallelism without GVL
ractors = 4.times.map do |i|
  Ractor.new(i) do |n|
    # Runs in parallel
    heavy_computation(n)
  end
end

results = ractors.map(&:take)
```

### Endless Methods

```ruby
# Single-expression method shorthand
def double(n) = n * 2
def greet(name) = "Hello, #{name}!"
def square(n) = n ** 2
```

### Refinements

```ruby
module StringExtensions
  refine String do
    def shout
      upcase + "!"
    end
  end
end

class Greeter
  using StringExtensions

  def greet(name)
    "hello #{name}".shout  # => "HELLO NAME!"
  end
end

# Outside the class, shout is not available
"test".shout  # NoMethodError
```

### Numbered Block Parameters

```ruby
# Use _1, _2, etc. for simple blocks
[1, 2, 3].map { _1 * 2 }           # => [2, 4, 6]
[[1, 2], [3, 4]].map { _1 + _2 }   # => [3, 7]
```

## Best Practices

### Guard Clauses

```ruby
# Prefer
def process(value)
  return if value.nil?
  return "empty" if value.empty?

  # main logic
end

# Over
def process(value)
  if value
    if value.empty?
      "empty"
    else
      # main logic
    end
  end
end
```

### Safe Navigation

```ruby
# Safe navigation operator
user&.profile&.avatar&.url

# With default
user&.profile&.avatar&.url || "default.png"
```

### Frozen String Literals

```ruby
# frozen_string_literal: true

# All string literals are frozen, improving performance
name = "Alice"  # Frozen, cannot be mutated
name << " Bob"  # FrozenError

# Use +@ to get mutable copy
mutable = +name
mutable << " Bob"  # OK
```
