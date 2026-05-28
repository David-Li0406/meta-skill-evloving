---
name: Factory Bot
description: This skill should be used when the user asks about "factories", "FactoryBot", "factory_bot", "traits", "sequences", "build vs create", "transient attributes", "associations in factories", or needs guidance on test data generation in RSpec.
version: 1.0.0
---

# Factory Bot

Factory Bot provides a framework for setting up Ruby objects as test data. It replaces fixtures with a more flexible and maintainable approach.

## Setup

```ruby
# Gemfile
group :development, :test do
  gem "factory_bot_rails"
end

# spec/rails_helper.rb
RSpec.configure do |config|
  config.include FactoryBot::Syntax::Methods
end
```

## Basic Factories

### Defining Factories

```ruby
# spec/factories/users.rb
FactoryBot.define do
  factory :user do
    first_name { "John" }
    last_name { "Doe" }
    email { "john@example.com" }
    password { "password123" }
    admin { false }
  end
end
```

### Using Factories

```ruby
# Create and save to database
user = create(:user)

# Build without saving (in-memory)
user = build(:user)

# Create with attribute overrides
user = create(:user, first_name: "Jane", admin: true)

# Build stubbed (fastest, no database)
user = build_stubbed(:user)

# Get attributes as hash
attrs = attributes_for(:user)
```

## Sequences

Generate unique values:

```ruby
factory :user do
  sequence(:email) { |n| "user#{n}@example.com" }
  sequence(:username) { |n| "user_#{n}" }
end

# Creates: user1@example.com, user2@example.com, etc.

# Named sequences (reusable)
sequence :email do |n|
  "person#{n}@example.com"
end

factory :user do
  email { generate(:email) }
end

factory :admin do
  email { generate(:email) }
end
```

## Dynamic Attributes

Use blocks for computed values:

```ruby
factory :user do
  first_name { "John" }
  last_name { "Doe" }
  email { "#{first_name.downcase}.#{last_name.downcase}@example.com" }
  created_at { Time.current }
  birth_date { 25.years.ago }
end

# Faker for realistic data
factory :user do
  first_name { Faker::Name.first_name }
  last_name { Faker::Name.last_name }
  email { Faker::Internet.email }
  phone { Faker::PhoneNumber.phone_number }
  bio { Faker::Lorem.paragraph }
end
```

## Associations

### belongs_to

```ruby
factory :post do
  title { "My Post" }
  body { "Content" }
  user  # Automatically creates associated user
end

# Override association
post = create(:post, user: specific_user)

# Explicit association
factory :post do
  association :user
  # or with factory name different from attribute
  association :author, factory: :user
end
```

### has_many

```ruby
factory :user do
  first_name { "John" }

  # Using transient + callback
  transient do
    posts_count { 0 }
  end

  after(:create) do |user, evaluator|
    create_list(:post, evaluator.posts_count, user: user)
  end
end

# Usage
user = create(:user, posts_count: 3)
user.posts.count  # => 3
```

### has_many with trait

```ruby
factory :user do
  trait :with_posts do
    transient do
      posts_count { 3 }
    end

    after(:create) do |user, evaluator|
      create_list(:post, evaluator.posts_count, user: user)
    end
  end
end

user = create(:user, :with_posts)
user = create(:user, :with_posts, posts_count: 5)
```

## Traits

Define reusable attribute sets:

```ruby
factory :user do
  first_name { "John" }
  email { "john@example.com" }
  admin { false }

  trait :admin do
    admin { true }
    email { "admin@example.com" }
  end

  trait :with_avatar do
    after(:create) do |user|
      user.avatar.attach(
        io: File.open(Rails.root.join("spec/fixtures/avatar.png")),
        filename: "avatar.png"
      )
    end
  end

  trait :inactive do
    active { false }
    deactivated_at { 1.day.ago }
  end
end

# Usage
admin = create(:user, :admin)
inactive_admin = create(:user, :admin, :inactive)
user_with_avatar = create(:user, :with_avatar)
```

### Combining Traits

```ruby
# Multiple traits
create(:user, :admin, :with_avatar, :inactive)

# Traits with overrides
create(:user, :admin, first_name: "Super Admin")

# Factory inheriting traits
factory :admin, traits: [:admin]
factory :inactive_user, traits: [:inactive]
```

## Transient Attributes

Pass data to factory without setting attributes:

```ruby
factory :user do
  transient do
    upcased { false }
    skip_confirmation { false }
  end

  first_name { "John" }

  after(:create) do |user, evaluator|
    user.update!(first_name: user.first_name.upcase) if evaluator.upcased
    user.confirm! if evaluator.skip_confirmation
  end
end

create(:user, upcased: true)
create(:user, skip_confirmation: true)
```

## Callbacks

Execute code at different lifecycle points:

```ruby
factory :user do
  after(:build) do |user|
    # After building, before save
  end

  before(:create) do |user|
    # Just before save
  end

  after(:create) do |user|
    # After save
  end

  after(:stub) do |user|
    # After build_stubbed
  end
end

# Callback with evaluator (access transient attributes)
after(:create) do |user, evaluator|
  create_list(:post, evaluator.posts_count, user: user)
end
```

## Inheritance

```ruby
factory :user do
  first_name { "John" }
  email { "john@example.com" }

  factory :admin do
    admin { true }
    email { "admin@example.com" }
  end

  factory :super_admin, parent: :admin do
    super_admin { true }
  end
end

create(:user)        # Regular user
create(:admin)       # Admin user
create(:super_admin) # Super admin
```

## Build Strategies

| Strategy | Database | ID | Best For |
|----------|----------|-----|----------|
| `create` | Yes | Real | Integration tests |
| `build` | No | nil | Unit tests, validations |
| `build_stubbed` | No | Fake | Fastest, isolated tests |
| `attributes_for` | No | - | Controller params |

```ruby
# Performance comparison
build(:user)          # Fast, no database
build_stubbed(:user)  # Fastest, fake persistence
create(:user)         # Slowest, hits database
```

### When to Use Each

```ruby
# build - testing object behavior without persistence
user = build(:user)
expect(user).to be_valid

# build_stubbed - mocking persisted objects
user = build_stubbed(:user)
expect(user.id).to be_present  # Has fake ID

# create - testing database interactions
user = create(:user)
expect(User.find(user.id)).to eq(user)

# attributes_for - controller params
post users_path, params: { user: attributes_for(:user) }
```

## Factory Lists

```ruby
# Create multiple records
users = create_list(:user, 3)
users = create_list(:user, 3, admin: true)

# Build multiple (no save)
users = build_list(:user, 5)

# With different attributes
users = create_list(:user, 3) do |user, i|
  user.update!(position: i)
end
```

## Linting Factories

Validate all factories are correctly defined:

```ruby
# spec/factories_spec.rb
RSpec.describe "Factories" do
  it "has valid factories" do
    FactoryBot.lint
  end

  # Faster: only lint traits
  it "has valid factories" do
    FactoryBot.lint(traits: true)
  end
end
```

## Best Practices

### Minimal Factories

Define only required attributes:

```ruby
# Good - minimal
factory :user do
  email { generate(:email) }
  password { "password" }
end

# Avoid - too much default data
factory :user do
  email { generate(:email) }
  password { "password" }
  first_name { "John" }
  last_name { "Doe" }
  phone { "555-1234" }
  address { "123 Main St" }
  # ... lots more
end
```

### Use Traits for Variations

```ruby
# Good - traits for specific states
factory :order do
  trait :pending do
    status { "pending" }
  end

  trait :shipped do
    status { "shipped" }
    shipped_at { 1.day.ago }
  end
end

# Avoid - many separate factories
factory :pending_order
factory :shipped_order
factory :cancelled_order
```

### Avoid Building What You Don't Need

```ruby
# Good - build associations only when needed
let(:user) { create(:user) }
let(:post) { create(:post, user: user) }

# Avoid - creating unused associated records
let(:user) { create(:user, :with_posts, :with_comments) }
```

## Additional Resources

### Reference Files

- **`references/factory-patterns.md`** - Advanced factory patterns
- **`references/faker-examples.md`** - Faker gem examples

### Example Files

- **`examples/factories/users.rb`** - Complete user factory
- **`examples/factories/orders.rb`** - Complex association example
