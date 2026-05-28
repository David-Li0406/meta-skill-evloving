# FactoryBot Patterns Reference

## Basic Factory

```ruby
# spec/factories/tasks.rb
FactoryBot.define do
  factory :task do
    account
    merchant
    recipient

    sequence(:tracking_number) { |n| "TRK#{n.to_s.rjust(8, '0')}" }
    status { 'pending' }
    description { Faker::Lorem.sentence }
    amount { Faker::Number.decimal(l_digits: 2, r_digits: 2) }

    # Traits
    trait :completed do
      status { 'completed' }
      completed_at { Time.current }
      carrier
    end

    trait :with_carrier do
      carrier
    end

    trait :express do
      task_type { 'express' }
    end

    trait :with_photos do
      after(:create) do |task|
        create_list(:photo, 2, task: task)
      end
    end

    # Callbacks
    after(:create) do |task|
      task.timelines.create!(status: task.status, created_at: task.created_at)
    end
  end
end
```

---

## Factory with Associations

```ruby
# spec/factories/accounts.rb
FactoryBot.define do
  factory :account do
    sequence(:name) { |n| "Account #{n}" }
    subdomain { name.parameterize }
    active { true }
  end
end

# spec/factories/merchants.rb
FactoryBot.define do
  factory :merchant do
    account
    sequence(:name) { |n| "Merchant #{n}" }
    email { Faker::Internet.email }

    trait :with_branches do
      after(:create) do |merchant|
        create_list(:branch, 2, merchant: merchant)
      end
    end
  end
end
```

---

## Transient Attributes

```ruby
FactoryBot.define do
  factory :bundle do
    account
    carrier

    transient do
      task_count { 5 }
    end

    after(:create) do |bundle, evaluator|
      create_list(:task, evaluator.task_count, bundle: bundle, account: bundle.account)
    end
  end
end

# Usage
create(:bundle, task_count: 10)
```

---

## Trait Combinations

```ruby
# Multiple traits
create(:task, :completed, :express, :with_photos)

# Trait with override
create(:task, :completed, completed_at: 1.day.ago)
```

---

## Factory Inheritance

```ruby
FactoryBot.define do
  factory :user do
    email { Faker::Internet.email }
    password { 'password123' }

    factory :admin do
      admin { true }
    end

    factory :verified_user do
      verified_at { Time.current }
    end
  end
end

# Usage
create(:admin)
create(:verified_user)
```

---

## Sequences

```ruby
# Global sequence
sequence :email do |n|
  "user#{n}@example.com"
end

# Factory-specific sequence
factory :order do
  sequence(:order_number, 1000) { |n| "ORD-#{n}" }
end
```

---

## Build vs Create

```ruby
# build - in-memory only, no DB write
task = build(:task)
task.persisted? # => false

# create - saved to database
task = create(:task)
task.persisted? # => true

# build_stubbed - stubs ID without DB
task = build_stubbed(:task)
task.id # => assigned fake ID
task.persisted? # => true (lies)

# Use build_stubbed for faster tests when DB not needed
```
