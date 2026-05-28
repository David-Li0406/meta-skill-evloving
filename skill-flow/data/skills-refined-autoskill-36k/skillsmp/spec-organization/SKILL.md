---
name: Spec Organization
description: This skill should be used when the user asks about "shared examples", "shared contexts", "spec structure", "test organization", "describe blocks", "RSpec tagging", "spec file layout", or needs guidance on organizing and structuring RSpec test suites.
version: 1.0.0
---

# Spec Organization

Well-organized specs are easier to maintain, faster to run, and clearer to read. This skill covers patterns for structuring RSpec test suites.

## Directory Structure

Standard Rails RSpec layout:

```
spec/
├── spec_helper.rb        # Pure RSpec config
├── rails_helper.rb       # Rails-specific config
├── support/              # Shared helpers and config
│   ├── factory_bot.rb
│   ├── capybara.rb
│   └── shared_examples/
├── factories/            # Factory Bot definitions
│   ├── users.rb
│   └── posts.rb
├── models/               # Model specs
├── requests/             # Request specs (API)
├── system/               # Browser/system specs
├── services/             # Service object specs
├── jobs/                 # Background job specs
├── mailers/              # Mailer specs
└── lib/                  # Library code specs
```

## Shared Examples

Reuse test logic across multiple specs:

### Defining Shared Examples

```ruby
# spec/support/shared_examples/soft_deletable.rb
RSpec.shared_examples "soft deletable" do
  describe "#soft_delete" do
    it "sets deleted_at timestamp" do
      expect { subject.soft_delete }.to change(subject, :deleted_at).from(nil)
    end

    it "does not actually destroy record" do
      subject.soft_delete
      expect(described_class.unscoped.find(subject.id)).to be_present
    end
  end

  describe "#deleted?" do
    it "returns true when soft deleted" do
      subject.soft_delete
      expect(subject).to be_deleted
    end

    it "returns false when not deleted" do
      expect(subject).not_to be_deleted
    end
  end
end
```

### Using Shared Examples

```ruby
# spec/models/user_spec.rb
RSpec.describe User, type: :model do
  subject { create(:user) }

  it_behaves_like "soft deletable"
end

# spec/models/post_spec.rb
RSpec.describe Post, type: :model do
  subject { create(:post) }

  it_behaves_like "soft deletable"
end
```

### Shared Examples with Parameters

```ruby
RSpec.shared_examples "publishable" do |factory_name|
  let(:resource) { create(factory_name) }

  describe "#publish" do
    it "sets published_at" do
      resource.publish
      expect(resource.published_at).to be_present
    end
  end
end

# Usage
it_behaves_like "publishable", :post
it_behaves_like "publishable", :article
```

### Block Form for Context

```ruby
RSpec.shared_examples "requires authentication" do
  context "when not authenticated" do
    before { sign_out }

    it "redirects to login" do
      subject
      expect(response).to redirect_to(login_path)
    end
  end
end

# Usage with block to define subject
it_behaves_like "requires authentication" do
  subject { get protected_path }
end
```

## Shared Contexts

Share setup across specs:

### Defining Shared Context

```ruby
# spec/support/shared_contexts/authenticated_user.rb
RSpec.shared_context "authenticated user" do
  let(:current_user) { create(:user) }

  before do
    sign_in current_user
  end
end

# With parameters
RSpec.shared_context "with admin user" do |role|
  let(:current_user) { create(:user, role: role || :admin) }

  before do
    sign_in current_user
  end
end
```

### Using Shared Context

```ruby
RSpec.describe "Dashboard", type: :request do
  include_context "authenticated user"

  it "shows user dashboard" do
    get dashboard_path
    expect(response).to have_http_status(:ok)
  end
end

# Include in all specs with metadata
RSpec.configure do |config|
  config.include_context "authenticated user", authenticated: true
end

# Then use metadata
RSpec.describe "Admin Panel", type: :request, authenticated: true do
  # Context automatically included
end
```

## Tagging and Filtering

### Adding Tags

```ruby
RSpec.describe User, type: :model do
  it "validates email", :slow do
    # Tagged as slow
  end

  it "sends notification", :external, :email do
    # Multiple tags
  end

  context "with external API", :integration do
    # All examples inherit :integration tag
  end
end
```

### Running with Tags

```bash
# Run only tagged specs
rspec --tag slow
rspec --tag integration
rspec --tag type:model

# Exclude tagged specs
rspec --tag ~slow
rspec --tag ~external

# Multiple tags (AND)
rspec --tag slow --tag integration

# Tag in .rspec file
# --tag ~slow
```

### Metadata Configuration

```ruby
# spec/spec_helper.rb
RSpec.configure do |config|
  # Skip slow tests unless CI
  config.filter_run_excluding :slow unless ENV["CI"]

  # Include helpers based on metadata
  config.include ApiHelpers, type: :request
  config.include SystemHelpers, type: :system

  # Run around hook for specific tags
  config.around(:each, :freeze_time) do |example|
    travel_to(Time.zone.local(2024, 1, 1)) { example.run }
  end
end
```

## Custom Matchers in Support

```ruby
# spec/support/matchers/json_matchers.rb
RSpec::Matchers.define :have_json_key do |expected|
  match do |response|
    body = JSON.parse(response.body)
    body.key?(expected.to_s)
  end

  failure_message do |response|
    "expected response to have JSON key '#{expected}'"
  end
end

# Usage
expect(response).to have_json_key(:data)
```

## Helper Modules

```ruby
# spec/support/helpers/authentication_helpers.rb
module AuthenticationHelpers
  def sign_in_as(user)
    post login_path, params: { email: user.email, password: "password" }
  end

  def current_user
    User.find(session[:user_id])
  end
end

# Include in specific spec types
RSpec.configure do |config|
  config.include AuthenticationHelpers, type: :request
  config.include AuthenticationHelpers, type: :system
end
```

## Describe and Context Best Practices

### Describe Block Naming

```ruby
RSpec.describe User do
  # Class/module under test at top level

  describe ".class_method" do
    # Class methods with dot prefix
  end

  describe "#instance_method" do
    # Instance methods with hash prefix
  end

  describe "validations" do
    # Logical groupings for multiple behaviors
  end
end
```

### Context Block Naming

Start with "when", "with", "without", "given":

```ruby
context "when user is an admin" do
  # State-based context
end

context "with valid attributes" do
  # Input-based context
end

context "without a password" do
  # Absence-based context
end

context "given a holiday schedule" do
  # Precondition-based context
end
```

### Nested Context Guidelines

Keep nesting to 3 levels maximum:

```ruby
# Good - clear and shallow
RSpec.describe Order do
  describe "#complete" do
    context "when payment succeeds" do
      it "marks order as completed" do
      end
    end

    context "when payment fails" do
      it "keeps order pending" do
      end
    end
  end
end

# Avoid - too deep
RSpec.describe Order do
  context "when user is logged in" do
    context "when cart has items" do
      context "when payment method is credit card" do
        context "when card is valid" do
          # Too many levels
        end
      end
    end
  end
end
```

## File Organization Patterns

### One Spec File Per Class

```ruby
# spec/models/user_spec.rb - tests User
# spec/models/post_spec.rb - tests Post
# spec/services/user_registration_spec.rb - tests UserRegistration
```

### Spec Mirrors App Structure

```
app/models/user.rb           → spec/models/user_spec.rb
app/services/orders/create.rb → spec/services/orders/create_spec.rb
app/controllers/api/v1/users_controller.rb → spec/requests/api/v1/users_spec.rb
```

### Feature-Based Organization (Alternative)

```
spec/
├── features/
│   ├── authentication/
│   │   ├── login_spec.rb
│   │   └── logout_spec.rb
│   └── checkout/
│       ├── add_to_cart_spec.rb
│       └── payment_spec.rb
```

## Additional Resources

### Reference Files

- **`references/shared-examples-patterns.md`** - Advanced shared example patterns
- **`references/support-structure.md`** - Support directory organization

### Example Files

- **`examples/support/shared_examples/`** - Reusable shared examples
- **`examples/support/helpers/`** - Custom helper modules
