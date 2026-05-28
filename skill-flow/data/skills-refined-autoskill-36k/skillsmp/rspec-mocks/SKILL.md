---
name: RSpec Mocks
description: This skill should be used when the user asks about "test doubles", "mocking", "stubbing", "spies", "verifying doubles", "partial doubles", "allow", "receive", "have_received", or needs guidance on isolating tests and mocking dependencies in RSpec.
version: 1.0.0
---

# RSpec Mocks

RSpec Mocks provides test doubles for isolating code under test from external dependencies.

## Test Double Types

| Type | Purpose |
|------|---------|
| **Double** | Pure test object with no connection to real class |
| **Verifying Double** | Double that validates against real class interface |
| **Partial Double** | Real object with some methods stubbed |
| **Spy** | Records method calls for later verification |

## Basic Doubles

### Creating Doubles

```ruby
# Anonymous double
user = double

# Named double (better error messages)
user = double("user")

# Double with stubs
user = double("user", name: "John", email: "john@example.com")
```

### Stubbing Methods

```ruby
user = double("user")
allow(user).to receive(:name).and_return("John")
allow(user).to receive(:save).and_return(true)

# Multiple stubs at once
allow(user).to receive_messages(name: "John", email: "john@example.com")
```

### Return Values

```ruby
allow(service).to receive(:call).and_return("result")

# Return different values on consecutive calls
allow(service).to receive(:call).and_return(1, 2, 3)
# First call returns 1, second returns 2, third+ returns 3

# Return value from block
allow(service).to receive(:call) { |arg| arg.upcase }

# Raise error
allow(service).to receive(:call).and_raise(StandardError, "error message")
allow(service).to receive(:call).and_raise(CustomError.new("message"))

# Throw symbol
allow(service).to receive(:call).and_throw(:abort)

# Yield to block
allow(service).to receive(:call).and_yield("value")
allow(service).to receive(:call).and_yield(1).and_yield(2)

# Call original implementation (partial doubles)
allow(service).to receive(:call).and_call_original
```

## Verifying Doubles

Verifying doubles check that stubbed methods exist on the real class. **Always prefer verifying doubles over plain doubles.**

```ruby
# instance_double - verifies against instance methods
user = instance_double(User)
allow(user).to receive(:name).and_return("John")
allow(user).to receive(:nonexistent)  # Raises error!

# class_double - verifies against class methods
UserService = class_double(UserService)
allow(UserService).to receive(:find).and_return(user)

# object_double - verifies against specific object
original_user = User.new
user = object_double(original_user, name: "John")
```

### Verifying Double Benefits

```ruby
# If User class changes and removes `name` method:
# - Plain double: Tests pass but code is broken
# - Verifying double: Tests fail, alerting to the issue

user = instance_double(User)
allow(user).to receive(:fullname)  # Typo! Raises:
# User does not implement #fullname
```

### Null Object Doubles

Return nil for unstubbed methods instead of raising:

```ruby
user = instance_double(User).as_null_object
user.anything  # Returns nil instead of error
```

## Message Expectations

### expect vs allow

```ruby
# allow - Stub without requiring call (test setup)
allow(service).to receive(:call)

# expect - Must be called or test fails (behavior verification)
expect(service).to receive(:call)
```

### Verifying Calls

```ruby
# Must be called
expect(mailer).to receive(:send_email)

# Must be called with specific arguments
expect(mailer).to receive(:send_email).with("user@example.com", "Welcome!")

# Must be called specific number of times
expect(mailer).to receive(:send_email).once
expect(mailer).to receive(:send_email).twice
expect(mailer).to receive(:send_email).exactly(3).times
expect(mailer).to receive(:send_email).at_least(:once)
expect(mailer).to receive(:send_email).at_most(5).times

# Must not be called
expect(mailer).not_to receive(:send_spam)
```

### Argument Matchers

```ruby
expect(service).to receive(:call).with("exact value")
expect(service).to receive(:call).with(anything)
expect(service).to receive(:call).with(any_args)
expect(service).to receive(:call).with(no_args)

# Type matching
expect(service).to receive(:call).with(instance_of(User))
expect(service).to receive(:call).with(kind_of(Numeric))

# Pattern matching
expect(service).to receive(:call).with(/pattern/)
expect(service).to receive(:call).with(hash_including(key: "value"))
expect(service).to receive(:call).with(array_including(1, 2))

# Custom matching
expect(service).to receive(:call).with(satisfy { |arg| arg.valid? })

# Combining matchers
expect(service).to receive(:process).with(
  instance_of(User),
  hash_including(notify: true)
)
```

## Spies

Spies verify calls after they happen (more natural test flow):

```ruby
# Setup: allow the call
mailer = instance_double(Mailer)
allow(mailer).to receive(:send_email)

# Exercise: run the code
user_service = UserService.new(mailer)
user_service.register(user)

# Verify: check it was called
expect(mailer).to have_received(:send_email).with(user.email)
```

### Spy vs Mock Style

```ruby
# Mock style (expect before action)
expect(mailer).to receive(:send_email)
user_service.register(user)

# Spy style (verify after action) - often clearer
allow(mailer).to receive(:send_email)
user_service.register(user)
expect(mailer).to have_received(:send_email)
```

### Spy Helpers

```ruby
# Create a spy that tracks all calls
user = spy("user")
user.name
user.email
user.save

expect(user).to have_received(:name)
expect(user).to have_received(:save)

# Verifying spy
user = instance_spy(User)
```

## Partial Doubles

Stub methods on real objects:

```ruby
user = User.new(name: "John")
allow(user).to receive(:premium?).and_return(true)

user.name       # Returns "John" (real method)
user.premium?   # Returns true (stubbed)
```

### Class Method Stubbing

```ruby
allow(User).to receive(:find).and_return(user)
allow(Time).to receive(:now).and_return(frozen_time)
allow(ENV).to receive(:[]).with("API_KEY").and_return("test-key")
```

### Dangerous: Stubbing Any Instance

```ruby
# Avoid when possible - makes tests brittle
allow_any_instance_of(User).to receive(:premium?).and_return(true)
expect_any_instance_of(User).to receive(:save)
```

**Better alternative: Dependency injection**

```ruby
# Instead of stubbing any instance
class UserService
  def initialize(user_class: User)
    @user_class = user_class
  end

  def create(attrs)
    @user_class.new(attrs)
  end
end

# Test with injected double
user_class = class_double(User)
service = UserService.new(user_class: user_class)
```

## Ordering

Enforce call order:

```ruby
expect(logger).to receive(:start).ordered
expect(processor).to receive(:process).ordered
expect(logger).to receive(:finish).ordered
```

## Configuration

```ruby
# spec/spec_helper.rb
RSpec.configure do |config|
  config.mock_with :rspec do |mocks|
    # Verify partial doubles against real methods
    mocks.verify_partial_doubles = true

    # Verify doubles in before/after hooks
    mocks.verify_doubled_constant_names = true
  end
end
```

## Best Practices

### Use Verifying Doubles

```ruby
# Good - catches interface changes
user = instance_double(User, name: "John")

# Avoid - doesn't verify interface
user = double("user", name: "John")
```

### Prefer Spies for Verification

```ruby
# Good - arrange, act, assert order
allow(mailer).to receive(:send)
service.process
expect(mailer).to have_received(:send)

# Harder to read - expect before action
expect(mailer).to receive(:send)
service.process
```

### Don't Over-Mock

```ruby
# Too much mocking - testing implementation
allow(user).to receive(:first_name).and_return("John")
allow(user).to receive(:last_name).and_return("Doe")
expect(user.full_name).to eq("John Doe")  # Just testing string concat

# Better - test real behavior
user = build(:user, first_name: "John", last_name: "Doe")
expect(user.full_name).to eq("John Doe")
```

### Mock at Boundaries

Mock external services, not internal collaborators:

```ruby
# Good - mocking external HTTP
allow(HTTPClient).to receive(:get).and_return(response)

# Questionable - mocking internal service
allow(UserValidator).to receive(:validate)  # Maybe just use real one?
```

## Additional Resources

### Reference Files

- **`references/mock-patterns.md`** - Common mocking patterns
- **`references/test-isolation.md`** - When and what to mock

### Example Files

- **`examples/service_with_mocks.rb`** - Service testing with mocks
- **`examples/api_client_spec.rb`** - Mocking HTTP clients
