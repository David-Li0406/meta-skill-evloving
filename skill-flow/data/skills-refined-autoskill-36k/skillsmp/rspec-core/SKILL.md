---
name: RSpec Core
description: This skill should be used when the user asks to "write an RSpec test", "create a spec", "use describe blocks", "set up let variables", "use before hooks", "understand RSpec structure", mentions "subject", "context", "it blocks", or needs guidance on RSpec 3.x fundamentals and test structure.
version: 1.0.0
---

# RSpec Core Fundamentals

RSpec is a behavior-driven development (BDD) testing framework for Ruby. This skill covers the core DSL for structuring and writing specs.

## Example Group Structure

### describe and context

Use `describe` for the thing being tested (class, method, behavior). Use `context` for different scenarios or states:

```ruby
RSpec.describe User do
  describe "#full_name" do
    context "when user has both names" do
      it "returns first and last name" do
        user = User.new(first_name: "John", last_name: "Doe")
        expect(user.full_name).to eq("John Doe")
      end
    end

    context "when user has no last name" do
      it "returns only first name" do
        user = User.new(first_name: "John", last_name: nil)
        expect(user.full_name).to eq("John")
      end
    end
  end
end
```

**Naming conventions:**
- `describe` with class name: `RSpec.describe User`
- `describe` with method: `describe "#instance_method"` or `describe ".class_method"`
- `context` starts with "when", "with", "without", "given": `context "when logged in"`

### it and specify

Use `it` for individual test cases. The description should complete the sentence "it...":

```ruby
it "returns the user's email" do
  expect(user.email).to eq("test@example.com")
end

# For complex descriptions, use specify
specify "the total includes tax and shipping" do
  expect(order.total).to eq(110.00)
end
```

**One expectation per example** (generally): Each `it` block should test one behavior. Multiple expectations are acceptable when testing related aspects of a single behavior.

## Subject and Let

### subject

Defines the primary object under test:

```ruby
RSpec.describe User do
  subject { User.new(name: "John") }

  it { is_expected.to be_valid }

  # Named subject for clarity
  subject(:user) { User.new(name: "John") }

  it "has the correct name" do
    expect(user.name).to eq("John")
  end
end
```

### let and let!

Use `let` for lazy-evaluated memoized helpers:

```ruby
RSpec.describe Order do
  let(:user) { User.create!(name: "John") }
  let(:product) { Product.create!(name: "Widget", price: 10) }
  let(:order) { Order.new(user: user, product: product) }

  it "calculates total correctly" do
    expect(order.total).to eq(10)
  end
end
```

**let vs let!:**
- `let` - Lazy evaluation, created when first referenced
- `let!` - Eager evaluation, created before each example

```ruby
let(:user) { User.create!(name: "John") }    # Created only if referenced
let!(:admin) { User.create!(admin: true) }   # Always created before each test
```

**When to use let!:**
- Database records that must exist for callbacks/associations
- Setup that has side effects needed by other code
- When order of creation matters

## Hooks

### before and after

Execute code before or after examples:

```ruby
RSpec.describe User do
  before(:each) do    # or just `before do`
    @user = User.new
  end

  after(:each) do
    # Cleanup after each example
  end

  before(:all) do     # or before(:context)
    # Run once before all examples in this group
    # Be careful: shared state between examples
  end

  after(:all) do
    # Run once after all examples
  end
end
```

**Hook execution order:**
1. `before(:all)` - once per describe/context block
2. `before(:each)` - before every example
3. The example runs
4. `after(:each)` - after every example
5. `after(:all)` - once after all examples

### around

Wrap examples with custom logic:

```ruby
around(:each) do |example|
  Timecop.freeze(Time.now) do
    example.run
  end
end

# Useful for database transactions
around(:each) do |example|
  ActiveRecord::Base.transaction do
    example.run
    raise ActiveRecord::Rollback
  end
end
```

## Pending and Skipping

### pending

Mark examples as not yet implemented or temporarily broken:

```ruby
it "sends welcome email" do
  pending "email service not implemented"
  expect(user.send_welcome_email).to be_truthy
end

# Or mark entire example as pending
pending "calculates complex tax" do
  expect(order.tax).to eq(15.00)
end
```

### skip

Skip examples entirely:

```ruby
it "requires external service", skip: "API not available in test" do
  # This won't run
end

# Conditional skip
it "runs on CI only", skip: !ENV["CI"] do
  # Skipped locally
end

# Skip with xit
xit "not implemented yet" do
  # Skipped
end
```

## Metadata and Filtering

Add metadata to examples and filter runs:

```ruby
RSpec.describe User, type: :model do
  it "validates email", :slow do
    # Tagged with :slow
  end

  it "processes payment", :integration, timeout: 30 do
    # Multiple tags
  end
end

# Run filtered specs:
# rspec --tag slow
# rspec --tag ~slow  (exclude slow)
# rspec --tag type:model
```

### Focus

Temporarily run only specific examples:

```ruby
fit "only this test runs" do     # focus + it
  expect(true).to be true
end

fdescribe User do                 # focus + describe
  # Only examples in this block run
end

fcontext "when focused" do        # focus + context
end
```

**Important:** Remove focus tags before committing. Configure CI to fail on focus:

```ruby
# spec/spec_helper.rb
RSpec.configure do |config|
  config.filter_run_when_matching :focus
  config.run_all_when_everything_filtered = true
end
```

## Configuration

### spec_helper.rb vs rails_helper.rb

- `spec_helper.rb` - Pure RSpec configuration, no Rails
- `rails_helper.rb` - Rails-specific setup, requires spec_helper

```ruby
# spec/spec_helper.rb
RSpec.configure do |config|
  config.expect_with :rspec do |expectations|
    expectations.include_chain_clauses_in_custom_matcher_descriptions = true
  end

  config.mock_with :rspec do |mocks|
    mocks.verify_partial_doubles = true
  end

  config.shared_context_metadata_behavior = :apply_to_host_groups
  config.filter_run_when_matching :focus
  config.example_status_persistence_file_path = "spec/examples.txt"
  config.disable_monkey_patching!
  config.order = :random
  Kernel.srand config.seed
end
```

## Best Practices

### Describe What, Not How

```ruby
# Good - describes behavior
it "returns user's full name" do
  expect(user.full_name).to eq("John Doe")
end

# Avoid - describes implementation
it "concatenates first_name and last_name with space" do
  expect(user.full_name).to eq("John Doe")
end
```

### Use Descriptive Context Names

```ruby
# Good
context "when user is an admin"
context "with valid attributes"
context "without a password"

# Avoid
context "admin case"
context "valid"
context "test 1"
```

### Prefer let Over Instance Variables

```ruby
# Good
let(:user) { create(:user) }

# Avoid
before { @user = create(:user) }
```

### Keep Examples Independent

Each example should be able to run in isolation. Avoid dependencies between examples.

## Additional Resources

### Reference Files

For advanced patterns and detailed examples:
- **`references/hooks-deep-dive.md`** - Comprehensive hook patterns and execution order
- **`references/configuration.md`** - Full RSpec configuration options

### Example Files

Working examples in `examples/`:
- **`examples/model_spec.rb`** - Complete model spec example
- **`examples/service_spec.rb`** - Service object testing patterns
