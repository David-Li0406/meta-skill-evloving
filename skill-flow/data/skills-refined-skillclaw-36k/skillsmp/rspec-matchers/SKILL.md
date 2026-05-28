---
name: RSpec Matchers
description: This skill should be used when the user asks about "RSpec matchers", "expect syntax", "custom matchers", "compound matchers", "should vs expect", mentions "eq", "be", "include", "match", "have_attributes", or needs guidance on RSpec assertions and expectations.
version: 1.0.0
---

# RSpec Matchers

Matchers are the building blocks of RSpec expectations. They define what you're testing and how values should compare.

## Basic Syntax

```ruby
expect(actual).to matcher(expected)
expect(actual).not_to matcher(expected)   # or to_not
```

## Equality Matchers

### eq - Value Equality

Tests value equality using `==`:

```ruby
expect(5).to eq(5)
expect("hello").to eq("hello")
expect([1, 2, 3]).to eq([1, 2, 3])
```

### eql - Value and Type Equality

Tests using `eql?` (same value and type):

```ruby
expect(5).to eql(5)
expect(5.0).not_to eql(5)  # Different types
```

### equal / be - Identity

Tests object identity using `equal?`:

```ruby
a = "hello"
b = a
expect(a).to equal(b)     # Same object
expect(a).to be(b)        # Alias for equal

c = "hello"
expect(a).not_to equal(c) # Different objects, same value
```

## Comparison Matchers

```ruby
expect(10).to be > 5
expect(10).to be >= 10
expect(10).to be < 20
expect(10).to be <= 10
expect(10).to be_between(5, 15).inclusive
expect(10).to be_between(5, 15).exclusive
expect(10).to be_within(0.1).of(10.05)
```

## Truthiness Matchers

```ruby
expect(true).to be true
expect(false).to be false
expect(nil).to be nil
expect(nil).to be_nil

expect(1).to be_truthy      # Truthy (not nil/false)
expect(nil).to be_falsey    # Falsey (nil or false)
```

## Type Matchers

```ruby
expect(user).to be_a(User)
expect(user).to be_an(Admin)        # Alias
expect(user).to be_an_instance_of(User)
expect(user).to be_a_kind_of(User)  # Includes subclasses
```

## Collection Matchers

### include

```ruby
expect([1, 2, 3]).to include(2)
expect([1, 2, 3]).to include(1, 3)
expect("hello world").to include("world")
expect({ a: 1, b: 2 }).to include(a: 1)
expect({ a: 1, b: 2 }).to include(:a)
```

### contain_exactly

Matches array with exact elements, any order:

```ruby
expect([1, 2, 3]).to contain_exactly(3, 2, 1)
expect([1, 2, 3]).to match_array([3, 1, 2])  # Alias
```

### start_with / end_with

```ruby
expect([1, 2, 3]).to start_with(1)
expect([1, 2, 3]).to start_with(1, 2)
expect("hello").to start_with("he")
expect("hello").to end_with("lo")
```

### all

Every element matches:

```ruby
expect([1, 3, 5]).to all(be_odd)
expect(users).to all(be_valid)
expect(numbers).to all(be > 0)
```

### have_attributes

```ruby
expect(user).to have_attributes(name: "John", age: 30)
expect(user).to have_attributes(
  name: a_string_starting_with("J"),
  age: a_value > 18
)
```

## Predicate Matchers

Any method ending in `?` becomes a matcher with `be_`:

```ruby
expect(user).to be_valid       # calls user.valid?
expect(list).to be_empty       # calls list.empty?
expect(user).to be_admin       # calls user.admin?
expect(order).to be_pending    # calls order.pending?
```

For `has_*` methods, use `have_`:

```ruby
expect(hash).to have_key(:name)    # calls hash.has_key?(:name)
expect(user).to have_permissions   # calls user.has_permissions?
```

## String Matchers

```ruby
expect("hello world").to match(/world/)
expect("hello world").to match("world")
expect("hello").to start_with("he")
expect("hello").to end_with("lo")
expect("hello").to include("ell")
```

## Change Matcher

Test side effects:

```ruby
expect { user.save }.to change(User, :count).by(1)
expect { user.save }.to change(User, :count).from(0).to(1)
expect { user.activate! }.to change(user, :active).from(false).to(true)

# Block syntax for complex changes
expect { order.complete! }.to change { order.reload.status }.to("completed")
```

## Raise and Throw Matchers

```ruby
expect { raise "error" }.to raise_error
expect { raise "error" }.to raise_error("error")
expect { raise ArgumentError }.to raise_error(ArgumentError)
expect { raise ArgumentError, "bad arg" }.to raise_error(ArgumentError, "bad arg")
expect { raise ArgumentError, "bad arg" }.to raise_error(ArgumentError, /bad/)

# Throw
expect { throw :done }.to throw_symbol
expect { throw :done }.to throw_symbol(:done)
expect { throw :done, 42 }.to throw_symbol(:done, 42)
```

## Output Matchers

```ruby
expect { puts "hello" }.to output("hello\n").to_stdout
expect { warn "error" }.to output(/error/).to_stderr
expect { print "hi" }.to output("hi").to_stdout
```

## Compound Matchers

Combine matchers with `and` / `or`:

```ruby
expect(user.age).to be >= 18 and be < 65
expect(string).to start_with("Hello").and end_with("!")
expect(result).to eq(1).or eq(2)

# Using described_as for better failure messages
expect(value).to(be > 0).and(be < 100).described_as("between 0 and 100")
```

## Composable Matchers

Use matchers as arguments to other matchers:

```ruby
expect(users).to include(
  a_user_with(name: "John"),
  a_user_with(name: "Jane")
)

expect([1, 2, 3]).to include(a_value > 2)
expect(response).to have_attributes(
  status: a_value_between(200, 299),
  body: a_string_including("success")
)
```

### Built-in Aliases

```ruby
a_string_starting_with("hello")
a_string_ending_with("world")
a_string_including("test")
a_string_matching(/pattern/)
a_value_between(1, 10)
a_value_within(0.1).of(5.0)
a_hash_including(key: value)
an_instance_of(User)
a_kind_of(User)
an_object_eq_to(expected)
```

## Custom Matchers

### Simple Custom Matcher

```ruby
RSpec::Matchers.define :be_a_multiple_of do |expected|
  match do |actual|
    actual % expected == 0
  end
end

expect(9).to be_a_multiple_of(3)
```

### With Failure Messages

```ruby
RSpec::Matchers.define :be_valid_email do
  match do |actual|
    actual =~ /\A[\w+\-.]+@[a-z\d\-]+(\.[a-z\d\-]+)*\.[a-z]+\z/i
  end

  failure_message do |actual|
    "expected #{actual.inspect} to be a valid email address"
  end

  failure_message_when_negated do |actual|
    "expected #{actual.inspect} not to be a valid email address"
  end
end
```

### With Chain Methods

```ruby
RSpec::Matchers.define :have_errors_on do |attribute|
  match do |model|
    model.valid?
    @errors = model.errors[attribute]
    @errors.present? && (@message.nil? || @errors.include?(@message))
  end

  chain :with_message do |message|
    @message = message
  end

  failure_message do |model|
    "expected #{model.class} to have errors on #{attribute}"
  end
end

expect(user).to have_errors_on(:email).with_message("is invalid")
```

## Matcher Cheat Sheet

| Matcher | Description |
|---------|-------------|
| `eq(x)` | Value equality (==) |
| `eql(x)` | Value + type equality |
| `equal(x)` / `be(x)` | Object identity |
| `be_truthy` | Not nil/false |
| `be_falsey` | Nil or false |
| `be > x` | Comparison |
| `include(x)` | Contains element |
| `match(/x/)` | Regex match |
| `raise_error(E)` | Raises exception |
| `change { }` | Side effect |
| `have_attributes(h)` | Object attributes |
| `all(matcher)` | All elements match |
| `contain_exactly(...)` | Exact elements, any order |

## Additional Resources

### Reference Files

For advanced patterns:
- **`references/custom-matchers.md`** - Complete custom matcher guide
- **`references/matcher-aliases.md`** - Full list of matcher aliases

### Example Files

- **`examples/custom_matchers.rb`** - Working custom matcher examples
