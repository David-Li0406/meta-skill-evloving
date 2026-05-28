# Metaprogramming Patterns

Common metaprogramming patterns and when to use them.

## Pattern: Attribute Accessors with Validation

```ruby
module ValidatedAccessors
  def validated_attr(name, &validator)
    define_method(name) do
      instance_variable_get("@#{name}")
    end

    define_method("#{name}=") do |value|
      unless validator.call(value)
        raise ArgumentError, "Invalid value for #{name}: #{value}"
      end
      instance_variable_set("@#{name}", value)
    end
  end
end

class User
  extend ValidatedAccessors

  validated_attr(:email) { |v| v.to_s.include?("@") }
  validated_attr(:age) { |v| v.is_a?(Integer) && v >= 0 }
end
```

## Pattern: Class Macro

```ruby
module Serializable
  def self.included(base)
    base.extend(ClassMethods)
  end

  module ClassMethods
    def serialize(*fields)
      @serialized_fields = fields

      define_method(:to_h) do
        fields.each_with_object({}) do |field, hash|
          hash[field] = send(field)
        end
      end

      define_method(:to_json) do
        require "json"
        to_h.to_json
      end
    end

    def serialized_fields
      @serialized_fields || []
    end
  end
end

class User
  include Serializable

  attr_accessor :name, :email, :password

  serialize :name, :email  # Excludes password
end
```

## Pattern: Method Decoration

```ruby
module Memoizable
  def memoize(method_name)
    original = instance_method(method_name)
    cache_var = "@_memoized_#{method_name}"

    define_method(method_name) do |*args|
      cache = instance_variable_get(cache_var) || {}

      unless cache.key?(args)
        cache[args] = original.bind(self).call(*args)
        instance_variable_set(cache_var, cache)
      end

      cache[args]
    end
  end
end

class Calculator
  extend Memoizable

  def fibonacci(n)
    return n if n <= 1
    fibonacci(n - 1) + fibonacci(n - 2)
  end
  memoize :fibonacci
end
```

## Pattern: Registry

```ruby
module Registry
  def self.included(base)
    base.extend(ClassMethods)
    base.instance_variable_set(:@registry, {})
  end

  module ClassMethods
    def register(key, klass = nil, &block)
      @registry[key] = klass || block
    end

    def lookup(key)
      @registry[key]
    end

    def build(key, *args)
      registered = lookup(key)
      case registered
      when Class then registered.new(*args)
      when Proc then registered.call(*args)
      else raise ArgumentError, "Unknown key: #{key}"
      end
    end
  end
end

class PaymentProcessor
  include Registry

  register :stripe, StripeProcessor
  register :paypal, PaypalProcessor
  register :test do |amount|
    OpenStruct.new(amount: amount, success: true)
  end
end

processor = PaymentProcessor.build(:stripe, api_key: "...")
```

## Anti-Patterns to Avoid

### 1. Overusing method_missing

```ruby
# Bad: Everything goes through method_missing
class BadAPI
  def method_missing(name, *args)
    call_api(name, args)
  end
end

# Good: Define known methods, use method_missing only for truly dynamic cases
class GoodAPI
  ENDPOINTS = %w[users posts comments].freeze

  ENDPOINTS.each do |endpoint|
    define_method(endpoint) do |**params|
      call_api(endpoint, params)
    end
  end

  def method_missing(name, *args)
    if name.to_s.start_with?("find_by_")
      attribute = name.to_s.sub("find_by_", "")
      find_by(attribute, args.first)
    else
      super
    end
  end

  def respond_to_missing?(name, include_private = false)
    name.to_s.start_with?("find_by_") || super
  end
end
```

### 2. String Eval Without Sanitization

```ruby
# Dangerous: Allows code injection
class Bad
  def self.create_method(name, body)
    class_eval("def #{name}; #{body}; end")
  end
end

# Safe: Use blocks instead
class Good
  def self.create_method(name, &body)
    define_method(name, &body)
  end
end
```

### 3. Monkey Patching Core Classes

```ruby
# Bad: Modifies String globally
class String
  def to_slug
    downcase.gsub(/\s+/, "-")
  end
end

# Good: Use refinements for scoped modifications
module StringExtensions
  refine String do
    def to_slug
      downcase.gsub(/\s+/, "-")
    end
  end
end

class BlogPost
  using StringExtensions

  def slug
    title.to_slug
  end
end
```

## Testing Metaprogrammed Code

```ruby
RSpec.describe Serializable do
  let(:klass) do
    Class.new do
      include Serializable

      attr_accessor :name, :secret

      serialize :name
    end
  end

  let(:instance) { klass.new.tap { |i| i.name = "test"; i.secret = "hidden" } }

  it "serializes only specified fields" do
    expect(instance.to_h).to eq({ name: "test" })
    expect(instance.to_h).not_to have_key(:secret)
  end
end
```
