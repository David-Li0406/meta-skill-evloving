---
name: metaprogramming
description: This skill should be used when the user asks about "metaprogramming", "DSL", "domain-specific language", "method_missing", "define_method", "class_eval", "instance_eval", "module_eval", "hooks", "included", "extended", "inherited", "singleton class", "eigenclass", "dynamic methods", "eval", or needs guidance on Ruby metaprogramming techniques.
version: 1.0.0
---

# Ruby Metaprogramming

Guide to Ruby metaprogramming techniques, DSL creation, and dynamic code generation.

## When to Use Metaprogramming

Use metaprogramming when:
- Building DSLs for configuration or testing
- Reducing repetitive code patterns
- Creating flexible APIs
- Implementing frameworks

Avoid when:
- Simple methods would suffice
- Code clarity is more important than conciseness
- Debugging would become difficult

## Dynamic Method Definition

### define_method

```ruby
class Calculator
  OPERATIONS = { add: :+, subtract: :-, multiply: :*, divide: :/ }.freeze

  OPERATIONS.each do |operation, operator|
    define_method(operation) do |a, b|
      a.send(operator, b)
    end
  end
end

calc = Calculator.new
calc.add(2, 3)       # => 5
calc.multiply(4, 5)  # => 20
```

### method_missing and respond_to_missing?

```ruby
class FlexibleStruct
  def initialize(attributes = {})
    @attributes = attributes
  end

  def method_missing(name, *args)
    attribute = name.to_s.chomp("=").to_sym

    if name.to_s.end_with?("=")
      @attributes[attribute] = args.first
    elsif @attributes.key?(attribute)
      @attributes[attribute]
    else
      super
    end
  end

  def respond_to_missing?(name, include_private = false)
    attribute = name.to_s.chomp("=").to_sym
    @attributes.key?(attribute) || super
  end
end

person = FlexibleStruct.new(name: "Alice")
person.name       # => "Alice"
person.age = 30
person.age        # => 30
person.respond_to?(:name)  # => true
```

## Class and Module Evaluation

### class_eval / module_eval

```ruby
# Add methods to a class dynamically
String.class_eval do
  def shout
    upcase + "!"
  end
end

"hello".shout  # => "HELLO!"

# With string evaluation (use sparingly)
klass.class_eval <<-RUBY, __FILE__, __LINE__ + 1
  def #{method_name}
    @#{attribute}
  end
RUBY
```

### instance_eval

```ruby
# Evaluate in context of an object
class Config
  attr_accessor :host, :port

  def configure(&block)
    instance_eval(&block)
  end
end

config = Config.new
config.configure do
  self.host = "localhost"
  self.port = 3000
end
```

## Hooks and Callbacks

### Module Hooks

```ruby
module Trackable
  def self.included(base)
    base.extend(ClassMethods)
    base.class_eval do
      # Add instance-level behavior
      attr_accessor :tracked_at
    end
  end

  def self.extended(base)
    # Called when module is extended
  end

  module ClassMethods
    def track_creation
      define_method(:initialize) do |*args|
        super(*args)
        @tracked_at = Time.now
      end
    end
  end
end

class User
  include Trackable
  track_creation
end
```

### Class Hooks

```ruby
class BaseModel
  def self.inherited(subclass)
    subclass.instance_variable_set(:@fields, [])
    subclass.extend(ClassMethods)
  end

  module ClassMethods
    def field(name)
      @fields << name
      attr_accessor name
    end

    def fields
      @fields
    end
  end
end

class User < BaseModel
  field :name
  field :email
end

User.fields  # => [:name, :email]
```

### Method Hooks

```ruby
module MethodLogger
  def self.included(base)
    base.extend(ClassMethods)
  end

  module ClassMethods
    def method_added(name)
      return if @_adding_method
      return if name == :initialize

      @_adding_method = true
      original = instance_method(name)

      define_method(name) do |*args, &block|
        puts "Calling #{name} with #{args}"
        original.bind(self).call(*args, &block)
      end

      @_adding_method = false
    end
  end
end
```

## DSL Creation

### Configuration DSL

```ruby
class ServerConfig
  attr_reader :settings

  def initialize
    @settings = {}
  end

  def self.configure(&block)
    config = new
    config.instance_eval(&block)
    config
  end

  def host(value)
    @settings[:host] = value
  end

  def port(value)
    @settings[:port] = value
  end

  def ssl(enabled: true, &block)
    @settings[:ssl] = { enabled: enabled }
    SSLConfig.new(@settings[:ssl]).instance_eval(&block) if block
  end

  class SSLConfig
    def initialize(settings)
      @settings = settings
    end

    def certificate(path)
      @settings[:certificate] = path
    end

    def key(path)
      @settings[:key] = path
    end
  end
end

config = ServerConfig.configure do
  host "localhost"
  port 3000
  ssl enabled: true do
    certificate "/path/to/cert.pem"
    key "/path/to/key.pem"
  end
end
```

### Builder DSL

```ruby
class HTMLBuilder
  def initialize
    @html = []
  end

  def method_missing(tag, content = nil, **attrs, &block)
    attr_str = attrs.map { |k, v| %( #{k}="#{v}") }.join
    @html << "<#{tag}#{attr_str}>"

    if block
      nested = HTMLBuilder.new
      nested.instance_eval(&block)
      @html << nested.to_s
    elsif content
      @html << content
    end

    @html << "</#{tag}>"
    self
  end

  def respond_to_missing?(*)
    true
  end

  def to_s
    @html.join
  end
end

html = HTMLBuilder.new
html.div(class: "container") do
  h1 "Welcome"
  p "Hello, World!"
  ul do
    li "Item 1"
    li "Item 2"
  end
end

puts html.to_s
# <div class="container"><h1>Welcome</h1><p>Hello, World!</p>...
```

## The Object Model

### Singleton Classes

```ruby
obj = Object.new

# Access singleton class
obj.singleton_class

# Define singleton methods
def obj.greet
  "Hello!"
end

# Or using singleton_class
obj.singleton_class.define_method(:farewell) { "Goodbye!" }

# Class methods are singleton methods on Class objects
class User
  def self.count  # Defined on User's singleton class
    @count ||= 0
  end
end
```

### Ancestors and Method Lookup

```ruby
module A; end
module B; end
module C; end

class Parent
  include A
end

class Child < Parent
  include B
  prepend C  # Prepend inserts before the class
end

Child.ancestors
# => [C, Child, B, Parent, A, Object, Kernel, BasicObject]

# Method lookup follows ancestors chain
```

### Prepend vs Include

```ruby
module Logging
  def save
    puts "Before save"
    super
    puts "After save"
  end
end

class Record
  prepend Logging  # Logging#save called before Record#save

  def save
    puts "Saving..."
  end
end

Record.new.save
# Before save
# Saving...
# After save
```

## Additional Resources

### Reference Files

- **`references/metaprogramming-patterns.md`** - Common metaprogramming patterns and anti-patterns
