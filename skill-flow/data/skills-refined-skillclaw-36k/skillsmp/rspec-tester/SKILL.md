---
name: rspec-tester
description: Generate RSpec test files for Ruby on Rails code. Creates model specs, request specs, service specs, and other test types. Uses FactoryBot when available in the project. Use when asked to write tests, create specs, add test coverage, or generate RSpec files.
---

# RSpec Test Generator

Generate comprehensive RSpec tests for Rails applications following Even Better Specs guidelines.

## Overview

This skill creates well-structured RSpec test files that prioritize self-contained, readable tests over DRY principles. Each test should be independently understandable without jumping to shared setup code.

## Core Principles

1. **Tests must be self-contained** - Each test should be readable on its own
2. **Follow Arrange-Act-Assert** - Clear structure in every example
3. **Clarity over DRY** - Duplicate code when it improves readability

## Instructions

### 1. Analyze the target code

Before generating tests:
- Read the file or class to be tested
- Identify public methods, associations, validations, and callbacks
- Check for existing specs to avoid duplication
- Look for existing factories in `spec/factories/`

### 2. Determine spec type

Based on the code location, create the appropriate spec:

| Source Location | Spec Location | Spec Type |
|-----------------|---------------|-----------|
| `app/models/` | `spec/models/` | Model spec |
| `app/controllers/` | `spec/requests/` | Request spec (NOT controller spec) |
| `app/services/` | `spec/services/` | Service spec |
| `app/jobs/` | `spec/jobs/` | Job spec |
| `app/mailers/` | `spec/mailers/` | Mailer spec |
| `app/helpers/` | `spec/helpers/` | Helper spec |

**Important**: Always use request specs over controller specs. Request specs involve the router, middleware, and full rack requests/responses.

### 3. Check for FactoryBot

Look for `spec/factories/` directory or `factory_bot_rails` in Gemfile:
- If present: Use `create()`, `build()`, `build_stubbed()` helpers
- If absent: Use direct `Model.new()` / `Model.create()`
- Prefer `build_stubbed` when tests don't need database persistence

### 4. Naming conventions

Use Ruby documentation conventions for describe blocks:
- `.method_name` for class methods: `describe '.authenticate'`
- `#method_name` for instance methods: `describe '#admin?'`
- For requests: `describe 'GET /users'` or `describe 'POST /users'`

### 5. Structure guidelines

```ruby
# frozen_string_literal: true

require "rails_helper"

RSpec.describe ClassName, type: :spec_type do
  describe "#method_name" do
    context "when some condition" do
      it "does expected behavior" do
        # Arrange - set up test data directly here
        user = build_stubbed(:user, name: "Alice")

        # Act - call the method
        result = user.greeting

        # Assert - verify the result
        expect(result).to eq("Hello, Alice!")
      end
    end
  end
end
```

### 6. Writing self-contained tests

**Avoid `let` and `let!`** - Declare variables directly in each test:

```ruby
# Bad - requires jumping to let block to understand
let(:user) { create(:user) }

it "returns the full name" do
  expect(user.full_name).to eq("John Doe")
end

# Good - self-contained and clear
it "returns the full name" do
  user = build_stubbed(:user, first_name: "John", last_name: "Doe")

  expect(user.full_name).to eq("John Doe")
end
```

**Avoid `before` hooks** - Include setup directly in each test:

```ruby
# Bad - shared setup obscures test requirements
before { sign_in(user) }

it "shows the dashboard" do
  get dashboard_path
  expect(response).to have_http_status(:ok)
end

# Good - explicit about what the test needs
it "shows the dashboard for authenticated users" do
  user = create(:user)
  sign_in(user)

  get dashboard_path

  expect(response).to have_http_status(:ok)
end
```

**Avoid shared examples** - Duplicate test code for clarity:

```ruby
# Bad - requires finding shared example definition
it_behaves_like "a paginated endpoint"

# Good - explicit about what's being tested
it "returns paginated results" do
  create_list(:post, 30)

  get posts_path, params: { page: 1, per_page: 10 }

  expect(json_response["data"].size).to eq(10)
  expect(json_response["meta"]["total"]).to eq(30)
end
```

### 7. Use described_class and subject

Replace hardcoded class names for maintainability:

```ruby
RSpec.describe UserService do
  describe ".call" do
    it "creates a user" do
      # Use described_class instead of UserService
      result = described_class.call(name: "Alice")

      expect(result).to be_a(User)
    end
  end
end
```

Use `subject` for simple cases:

```ruby
RSpec.describe User do
  subject { described_class.new }

  it { is_expected.to respond_to(:email) }
end
```

### 8. Context naming

Always start context descriptions with "when", "with", or "without":

```ruby
describe "#publish" do
  context "when the post is valid" do
    it "marks it as published" do
      # ...
    end
  end

  context "when the post has no title" do
    it "returns an error" do
      # ...
    end
  end
end
```

### 9. Keep descriptions short

Limit descriptions to 100 characters. Split long descriptions using contexts:

```ruby
# Bad
it "returns an error message indicating the user cannot perform this action because they lack permissions" do

# Good
context "when user lacks permissions" do
  it "returns an error message" do
```

### 10. Group related expectations

Combine assertions that share similar data setup:

```ruby
it "returns user attributes" do
  user = create(:user, name: "Alice", email: "alice@example.com")

  get user_path(user)

  expect(response).to have_http_status(:ok)
  expect(json_response["name"]).to eq("Alice")
  expect(json_response["email"]).to eq("alice@example.com")
end
```

### 11. Test coverage

Test valid, edge, and invalid cases:

```ruby
describe "#age" do
  it "calculates age from birthdate" do
    user = build_stubbed(:user, birthdate: 30.years.ago)

    expect(user.age).to eq(30)
  end

  it "returns nil when birthdate is missing" do
    user = build_stubbed(:user, birthdate: nil)

    expect(user.age).to be_nil
  end

  it "handles future birthdates" do
    user = build_stubbed(:user, birthdate: 1.year.from_now)

    expect(user.age).to eq(-1)
  end
end
```

### 12. Mocking and stubbing

**Use `instance_double` over `double`** - Verifies mocked methods exist:

```ruby
# Bad - won't catch typos or removed methods
payment_gateway = double("PaymentGateway")
allow(payment_gateway).to receive(:proccess)  # typo won't be caught

# Good - verifies the method exists on the class
payment_gateway = instance_double(PaymentGateway)
allow(payment_gateway).to receive(:process)
```

**Mock external dependencies** - Keep tests fast and isolated:

```ruby
it "sends a welcome email" do
  mailer = instance_double(UserMailer)
  allow(UserMailer).to receive(:welcome).and_return(mailer)
  allow(mailer).to receive(:deliver_later)

  described_class.call(email: "user@example.com")

  expect(mailer).to have_received(:deliver_later)
end
```

**Stub HTTP requests** - Use webmock or VCR:

```ruby
it "fetches user data from external API" do
  stub_request(:get, "https://api.example.com/users/1")
    .to_return(body: { name: "Alice" }.to_json)

  result = described_class.fetch(user_id: 1)

  expect(result.name).to eq("Alice")
end
```

### 13. Syntax requirements

Always use `expect` syntax, never `should`:

```ruby
# Bad
user.should be_valid

# Good
expect(user).to be_valid
```

### 14. Create only necessary data

Minimize test data creation for performance:

```ruby
# Bad - creates unnecessary records
it "finds active users" do
  create_list(:user, 100, status: :active)
  create_list(:user, 100, status: :inactive)

  expect(User.active.count).to eq(100)
end

# Good - creates only what's needed
it "finds active users" do
  active_user = create(:user, status: :active)
  create(:user, status: :inactive)

  expect(User.active).to contain_exactly(active_user)
end
```

## Model Spec Coverage

For model specs, test:
- Validations (presence, uniqueness, format, custom)
- Associations (belongs_to, has_many, has_one)
- Scopes
- Instance methods
- Class methods
- Callbacks (when they have observable side effects)

## Request Spec Coverage

For request specs, test:
- HTTP response status codes
- Response body content/structure
- Authentication/authorization
- Parameter handling
- Error responses

## Example Usage

User: "Write tests for the User model"
Action: Read `app/models/user.rb`, check for existing factory, generate `spec/models/user_spec.rb`

User: "Add request specs for the posts controller"
Action: Read `app/controllers/posts_controller.rb`, generate `spec/requests/posts_spec.rb`

User: "Create specs for the OrderProcessor service"
Action: Read `app/services/order_processor.rb`, generate `spec/services/order_processor_spec.rb`
