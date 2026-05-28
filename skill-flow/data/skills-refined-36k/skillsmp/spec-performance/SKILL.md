---
name: Spec Performance
description: This skill should be used when the user asks about "slow specs", "test performance", "parallel tests", "spec profiling", "let vs let!", "build vs create", "test optimization", or needs guidance on making RSpec tests faster.
version: 1.0.0
---

# Spec Performance

Slow tests reduce productivity and discourage running tests frequently. This skill covers techniques for optimizing RSpec test suite performance.

## Profiling Slow Tests

### Built-in Profiler

```bash
# Show 10 slowest examples
rspec --profile 10

# In spec_helper.rb for always-on profiling
RSpec.configure do |config|
  config.profile_examples = 10
end
```

### Detailed Timing

```ruby
# spec/support/timing.rb
RSpec.configure do |config|
  config.around(:each) do |example|
    start = Time.now
    example.run
    elapsed = Time.now - start
    puts "#{example.full_description}: #{elapsed.round(2)}s" if elapsed > 1
  end
end
```

## Database Optimization

### Prefer build Over create

```ruby
# Slow - hits database
let(:user) { create(:user) }

# Fast - in memory only
let(:user) { build(:user) }

# Fastest - stubbed, no DB
let(:user) { build_stubbed(:user) }
```

### When to Use Each Strategy

| Strategy | Use When |
|----------|----------|
| `build` | Testing validations, object behavior |
| `build_stubbed` | Need ID, testing presentation |
| `create` | Testing DB queries, associations, callbacks |

### Minimize Database Writes

```ruby
# Slow - creates 3 users
it "lists users" do
  create(:user)
  create(:user)
  create(:user)
  expect(User.count).to eq(3)
end

# Better - single batch insert
it "lists users" do
  User.insert_all([
    { email: "a@test.com" },
    { email: "b@test.com" },
    { email: "c@test.com" }
  ])
  expect(User.count).to eq(3)
end
```

### Use before(:all) Carefully

```ruby
# Creates user once for all examples
before(:all) do
  @user = create(:user)
end

after(:all) do
  @user.destroy
end

# Warning: shared state between examples
# Use only for read-only data
```

## let vs let!

### let - Lazy Evaluation

```ruby
let(:user) { create(:user) }

it "does something" do
  # User created here, when first accessed
  user.name
end

it "does something else" do
  # User not created if not referenced
  expect(true).to be true
end
```

### let! - Eager Evaluation

```ruby
let!(:user) { create(:user) }

it "has a user in database" do
  # User already created before this runs
  expect(User.count).to eq(1)
end
```

### When to Use let!

```ruby
# Use let! when:
# 1. Callback side effects needed
let!(:user) { create(:user) }  # Triggers after_create callbacks

# 2. Database state must exist before test
let!(:existing_user) { create(:user, email: "taken@test.com") }

it "validates uniqueness" do
  new_user = build(:user, email: "taken@test.com")
  expect(new_user).not_to be_valid
end
```

### Avoid Unnecessary let!

```ruby
# Bad - always creates even when not needed
let!(:user) { create(:user) }
let!(:post) { create(:post, user: user) }
let!(:comment) { create(:comment, post: post) }

# Good - only create what's needed per test
let(:user) { create(:user) }

context "with posts" do
  let(:post) { create(:post, user: user) }

  it "lists posts" do
    post  # Triggers creation
    expect(user.posts).to include(post)
  end
end
```

## Parallel Testing

### parallel_tests Gem

```ruby
# Gemfile
gem "parallel_tests", group: [:development, :test]

# Setup
rake parallel:setup
rake parallel:create
rake parallel:migrate

# Run tests
rake parallel:spec
# or
parallel_rspec spec/
```

### Database Configuration

```yaml
# config/database.yml
test:
  database: myapp_test<%= ENV['TEST_ENV_NUMBER'] %>
```

### Avoiding Parallelization Issues

```ruby
# Use unique data per process
let(:email) { "user#{Process.pid}@test.com" }

# Avoid shared files
let(:file_path) { Rails.root.join("tmp/test_#{Process.pid}.txt") }
```

## Mocking and Stubbing for Speed

### Stub External Services

```ruby
# Slow - real HTTP call
it "fetches data" do
  result = ExternalApi.fetch(id: 1)
  expect(result).to be_present
end

# Fast - stubbed response
it "fetches data" do
  allow(ExternalApi).to receive(:fetch).and_return({ data: "test" })
  result = ExternalApi.fetch(id: 1)
  expect(result).to eq({ data: "test" })
end
```

### Use WebMock for HTTP

```ruby
# Gemfile
gem "webmock", group: :test

# spec/spec_helper.rb
require "webmock/rspec"
WebMock.disable_net_connect!(allow_localhost: true)

# In specs
stub_request(:get, "https://api.example.com/users")
  .to_return(status: 200, body: { users: [] }.to_json)
```

### Stub Time-Consuming Methods

```ruby
# Slow - actual file processing
it "processes file" do
  result = FileProcessor.process(large_file)
  expect(result).to be_present
end

# Fast - stub the slow method
it "processes file" do
  allow(FileProcessor).to receive(:process).and_return({ success: true })
  result = FileProcessor.process(large_file)
  expect(result).to eq({ success: true })
end
```

## Test Data Optimization

### Use build_stubbed for Speed

```ruby
# build_stubbed creates objects with:
# - Fake IDs (but not nil)
# - Fake timestamps
# - No database writes

user = build_stubbed(:user)
user.id        # => 1001 (fake but present)
user.persisted? # => true (pretends to be saved)
```

### Minimal Factory Attributes

```ruby
# Slow - lots of associations
factory :order do
  user
  shipping_address
  billing_address
  coupon
  association :items, count: 5
end

# Fast - minimal required attributes
factory :order do
  status { "pending" }
  total { 100 }

  trait :with_user do
    user
  end
end
```

### Avoid N+1 in Test Setup

```ruby
# Slow - N+1 queries in setup
let(:users) { create_list(:user, 10) }

before do
  users.each { |u| create(:post, user: u) }
end

# Better - batch operations
before do
  users = create_list(:user, 10)
  Post.insert_all(users.map { |u| { user_id: u.id, title: "Post" } })
end
```

## CI Optimization

### Fail Fast

```ruby
# spec/spec_helper.rb
RSpec.configure do |config|
  config.fail_fast = ENV["CI"].present?
end
```

### Bisect for Flaky Tests

```bash
# Find minimal set that reproduces failure
rspec --bisect
```

### Example Status Persistence

```ruby
# spec/spec_helper.rb
RSpec.configure do |config|
  # Re-run only failed specs first
  config.example_status_persistence_file_path = "spec/examples.txt"
end
```

## Performance Checklist

### Quick Wins

- [ ] Use `build` instead of `create` when possible
- [ ] Use `build_stubbed` for presentation tests
- [ ] Stub external HTTP calls
- [ ] Avoid `let!` when `let` works

### Medium Effort

- [ ] Set up parallel testing
- [ ] Profile and fix slowest specs
- [ ] Minimize factory associations
- [ ] Use `before(:all)` for read-only setup

### Advanced

- [ ] Database cleaner strategy optimization
- [ ] Shared database connections for system specs
- [ ] Spring preloader for development
- [ ] CI caching for gems and assets

## Benchmarking Helpers

```ruby
# spec/support/benchmark_helper.rb
module BenchmarkHelper
  def measure(label = "Block", &block)
    start = Process.clock_gettime(Process::CLOCK_MONOTONIC)
    result = block.call
    elapsed = Process.clock_gettime(Process::CLOCK_MONOTONIC) - start
    puts "#{label}: #{(elapsed * 1000).round(2)}ms"
    result
  end
end

# Usage in specs
include BenchmarkHelper

it "performs quickly" do
  measure("User creation") { create(:user) }
  measure("User build") { build(:user) }
end
```

## Additional Resources

### Reference Files

- **`references/parallel-testing.md`** - Parallel test configuration
- **`references/ci-optimization.md`** - CI-specific optimizations

### Example Files

- **`examples/fast_spec.rb`** - Optimized spec patterns
- **`examples/slow_spec.rb`** - Anti-patterns to avoid
