# RSpec Hooks Deep Dive

## Hook Execution Order

Understanding hook execution order is critical for proper test setup and teardown.

### Complete Execution Order

```
1. before(:suite)         - Once at start
2. before(:all/:context)  - Once per describe/context
3. before(:each/:example) - Before each example
4. around(:each) start    - Wraps example
5. Example runs
6. around(:each) end      - Completes wrap
7. after(:each/:example)  - After each example
8. after(:all/:context)   - Once after all in describe/context
9. after(:suite)          - Once at end
```

### Nested Hooks

```ruby
RSpec.describe "Outer" do
  before(:all) { puts "1. Outer before(:all)" }
  before(:each) { puts "2. Outer before(:each)" }
  after(:each) { puts "5. Outer after(:each)" }
  after(:all) { puts "6. Outer after(:all)" }

  context "Inner" do
    before(:all) { puts "1a. Inner before(:all)" }
    before(:each) { puts "3. Inner before(:each)" }
    after(:each) { puts "4. Inner after(:each)" }
    after(:all) { puts "6a. Inner after(:all)" }

    it "example" { puts "   Example runs" }
  end
end

# Output:
# 1. Outer before(:all)
# 1a. Inner before(:all)
# 2. Outer before(:each)
# 3. Inner before(:each)
#    Example runs
# 4. Inner after(:each)
# 5. Outer after(:each)
# 6a. Inner after(:all)
# 6. Outer after(:all)
```

## around Hooks

### Basic Usage

```ruby
around(:each) do |example|
  # Setup
  puts "Before example"

  example.run

  # Teardown
  puts "After example"
end
```

### Common Patterns

#### Database Transaction Wrapping

```ruby
around(:each) do |example|
  ActiveRecord::Base.transaction do
    example.run
    raise ActiveRecord::Rollback
  end
end
```

#### Time Freezing

```ruby
around(:each) do |example|
  travel_to(Time.zone.local(2024, 1, 1)) do
    example.run
  end
end
```

#### Temporary Environment

```ruby
around(:each) do |example|
  original_env = ENV.to_hash
  example.run
ensure
  ENV.replace(original_env)
end
```

#### Timeout

```ruby
around(:each, timeout: true) do |example|
  Timeout.timeout(5) { example.run }
end
```

## Hook Scopes

### :suite Scope

Runs once for entire test run:

```ruby
RSpec.configure do |config|
  config.before(:suite) do
    # Database setup
    DatabaseCleaner.clean_with(:truncation)
  end

  config.after(:suite) do
    # Generate coverage report
    SimpleCov.result
  end
end
```

### :all/:context Scope

Runs once per describe/context block:

```ruby
RSpec.describe User do
  before(:all) do
    # Expensive setup - shared by all examples
    @api_client = ExpensiveApiClient.new
  end

  after(:all) do
    @api_client.disconnect
  end
end
```

**Warning:** State is shared between examples. Use only for:
- Read-only data
- Expensive immutable resources
- External connections

### :each/:example Scope

Default. Runs for every example:

```ruby
before(:each) do
  @user = create(:user)
end

after(:each) do
  @user.destroy
end
```

## Hook Configuration

### Metadata Filtering

```ruby
# Only run for specific metadata
config.before(:each, type: :system) do
  driven_by(:selenium_chrome_headless)
end

config.around(:each, :freeze_time) do |example|
  travel_to(Time.current) { example.run }
end

# Usage
it "does something", :freeze_time do
  # Time is frozen
end
```

### Conditional Hooks

```ruby
config.before(:each) do |example|
  if example.metadata[:js]
    Capybara.current_driver = :selenium
  end
end
```

## Hook Gotchas

### Instance Variables in before(:all)

```ruby
before(:all) do
  @user = create(:user)  # Created once
end

it "modifies user" do
  @user.update!(name: "Changed")  # Persists to next example!
end

it "expects original" do
  expect(@user.name).to eq("Original")  # FAILS
end
```

**Solution:** Use `let` or create fresh data per example.

### Hook Exceptions

Exceptions in before hooks skip the example:

```ruby
before(:each) do
  raise "Setup failed"
end

it "never runs" do
  # This example is skipped with error
end
```

Exceptions in after hooks still run remaining after hooks:

```ruby
after(:each) { raise "Error 1" }  # Runs
after(:each) { puts "Still runs" }  # Also runs
# Both errors reported
```

### Hook Order with Inheritance

```ruby
RSpec.configure do |config|
  config.before(:each) { puts "1. Global" }
end

RSpec.describe "Parent" do
  before(:each) { puts "2. Parent" }

  context "Child" do
    before(:each) { puts "3. Child" }
    it "example" { }
  end
end

# Order: 1. Global, 2. Parent, 3. Child
```

## Prepend vs Append

```ruby
config.before(:each) { puts "1" }
config.prepend_before(:each) { puts "0" }  # Runs first
config.append_before(:each) { puts "2" }   # Runs after default

# Output: 0, 1, 2
```

## Example Metadata Access

```ruby
before(:each) do |example|
  puts example.description
  puts example.full_description
  puts example.metadata[:type]
  puts example.file_path
  puts example.location
end
```
