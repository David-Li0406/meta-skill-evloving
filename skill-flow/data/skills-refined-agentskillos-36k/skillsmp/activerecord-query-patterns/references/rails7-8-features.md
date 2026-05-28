# Rails 7.x/8.x Modern Features Reference

## Composite Primary Keys (Rails 7.1+)

```ruby
# Migration
class CreateBookOrders < ActiveRecord::Migration[7.1]
  def change
    create_table :book_orders, primary_key: [:shop_id, :id] do |t|
      t.integer :shop_id
      t.integer :id
      t.string :status
      t.timestamps
    end
  end
end

# Model
class BookOrder < ApplicationRecord
  self.primary_key = [:shop_id, :id]

  belongs_to :shop
  has_many :line_items, foreign_key: [:shop_id, :order_id]
end

# Usage
order = BookOrder.find([shop_id: 1, id: 100])
order.id # => { shop_id: 1, id: 100 }
```

---

## ActiveRecord::Encryption (Rails 7+)

```ruby
# config/credentials.yml.enc
active_record_encryption:
  primary_key: <%= ENV['AR_ENCRYPTION_PRIMARY_KEY'] %>
  deterministic_key: <%= ENV['AR_ENCRYPTION_DETERMINISTIC_KEY'] %>
  key_derivation_salt: <%= ENV['AR_ENCRYPTION_KEY_DERIVATION_SALT'] %>

# Model
class User < ApplicationRecord
  encrypts :email               # Non-deterministic (can't query)
  encrypts :ssn, deterministic: true  # Deterministic (can query equality)
  encrypts :credit_card, ignore_case: true
end

# Queries with deterministic encryption
User.where(ssn: '123-45-6789')  # Works with deterministic: true
User.where(email: 'user@example.com')  # Doesn't work without deterministic
```

---

## Multi-Database Configuration (Rails 6.1+)

```ruby
# config/database.yml
production:
  primary:
    <<: *default
    database: my_primary_database
  analytics:
    <<: *default
    database: my_analytics_database
    replica: true
    migrations_paths: db/analytics_migrate

# Models
class ApplicationRecord < ActiveRecord::Base
  self.abstract_class = true
  connects_to database: { writing: :primary, reading: :primary }
end

class AnalyticsRecord < ActiveRecord::Base
  self.abstract_class = true
  connects_to database: { writing: :analytics, reading: :analytics }
end

class Event < AnalyticsRecord
end

# Switching databases
ActiveRecord::Base.connected_to(role: :reading) do
  # Read from replica
end

ActiveRecord::Base.connected_to(role: :writing, prevent_writes: true) do
  # Raises error on write
end
```

---

## Horizontal Sharding (Rails 7.1+)

```ruby
# config/database.yml
production:
  primary:
    database: my_primary_database
  shard_one:
    database: my_shard_one_database
  shard_two:
    database: my_shard_two_database

# Model
class ApplicationRecord < ActiveRecord::Base
  self.abstract_class = true
  connects_to shards: {
    shard_one: { writing: :shard_one },
    shard_two: { writing: :shard_two }
  }
end

# Usage
ActiveRecord::Base.connected_to(shard: :shard_one) do
  User.create!(name: "User in shard one")
end

# Switching shards based on data
def with_user_shard(user_id)
  shard = user_id.even? ? :shard_one : :shard_two
  ActiveRecord::Base.connected_to(shard: shard) do
    yield
  end
end
```

---

## Enum Patterns with i18n

```ruby
class Task < ApplicationRecord
  enum status: {
    pending: 0,
    in_progress: 1,
    completed: 2
  }, _prefix: true  # status_pending?, status_completed?

  enum priority: {
    low: 0,
    medium: 1,
    high: 2
  }, _suffix: true  # low_priority?, high_priority?

  # Auto-generated methods:
  # task.status               => "pending"
  # task.pending?             => true
  # Task.pending              => Scope for pending tasks
  # Task.not_pending          => Scope for non-pending tasks
end

# i18n in config/locales/en.yml
en:
  activerecord:
    attributes:
      task:
        status:
          pending: "Pending"
          in_progress: "In Progress"
          completed: "Completed"
```
