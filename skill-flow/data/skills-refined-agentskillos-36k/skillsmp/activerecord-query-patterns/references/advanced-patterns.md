# Advanced ActiveRecord Patterns Reference

## Database Views

```ruby
# Migration
class CreateActiveTasksView < ActiveRecord::Migration[7.1]
  def up
    execute <<-SQL
      CREATE VIEW active_tasks AS
      SELECT
        tasks.*,
        merchants.name AS merchant_name,
        carriers.name AS carrier_name
      FROM tasks
      INNER JOIN merchants ON merchants.id = tasks.merchant_id
      LEFT JOIN carriers ON carriers.id = tasks.carrier_id
      WHERE tasks.status IN ('pending', 'in_progress')
    SQL
  end

  def down
    execute "DROP VIEW IF EXISTS active_tasks"
  end
end

# Model (read-only)
class ActiveTask < ApplicationRecord
  self.primary_key = :id

  def readonly?
    true
  end
end

# Usage
ActiveTask.all
ActiveTask.where(merchant_name: "ACME Corp")
```

---

## Materialized Views

```ruby
# Migration
class CreateTaskSummaryView < ActiveRecord::Migration[7.1]
  def up
    execute <<-SQL
      CREATE MATERIALIZED VIEW task_summaries AS
      SELECT
        DATE(created_at) as date,
        status,
        COUNT(*) as count,
        AVG(amount) as average_amount
      FROM tasks
      GROUP BY DATE(created_at), status
    SQL

    add_index :task_summaries, :date
  end
end

# Refresh (schedule this)
ActiveRecord::Base.connection.execute("REFRESH MATERIALIZED VIEW task_summaries")

# Concurrent refresh (non-blocking)
ActiveRecord::Base.connection.execute("REFRESH MATERIALIZED VIEW CONCURRENTLY task_summaries")
```

---

## Common Table Expressions (CTEs)

```ruby
# Simple CTE
Task.with(
  active_merchants: Merchant.where(active: true).select(:id)
).joins("INNER JOIN active_merchants ON tasks.merchant_id = active_merchants.id")

# Recursive CTE for hierarchical data
sql = <<-SQL
  WITH RECURSIVE subordinates AS (
    SELECT id, name, manager_id, 1 as level
    FROM employees
    WHERE id = ?

    UNION ALL

    SELECT e.id, e.name, e.manager_id, s.level + 1
    FROM employees e
    INNER JOIN subordinates s ON e.manager_id = s.id
  )
  SELECT * FROM subordinates
SQL

Employee.find_by_sql([sql, manager_id])
```

---

## Single Table Inheritance (STI)

```ruby
# Base model (has `type` column)
class Vehicle < ApplicationRecord
  validates :name, presence: true
end

class Car < Vehicle
  def drive
    "Driving #{name}"
  end
  validates :num_doors, presence: true
end

class Motorcycle < Vehicle
  def ride
    "Riding #{name}"
  end
end

# Usage
car = Car.create!(name: "Tesla", num_doors: 4)
Vehicle.all  # Returns mix of cars and motorcycles
Car.all      # Returns only cars
car.type     # => "Car"
```

**STI Best Practices:**
- Use when subclasses share 80%+ of attributes
- Avoid if types have very different attributes
- Watch for sparse tables (lots of nulls)
- Consider delegated_type for diverse attributes

---

## Delegated Types (Rails 6.1+)

Alternative to STI for polymorphic models:

```ruby
# Migration
create_table :entries do |t|
  t.string :entryable_type
  t.bigint :entryable_id
  t.timestamps
end

create_table :messages do |t|
  t.string :subject
  t.text :body
end

create_table :comments do |t|
  t.text :body
end

# Models
class Entry < ApplicationRecord
  delegated_type :entryable, types: %w[Message Comment]
end

class Message < ApplicationRecord
  has_one :entry, as: :entryable, touch: true
end

class Comment < ApplicationRecord
  has_one :entry, as: :entryable, touch: true
end

# Usage
Entry.messages  # Only message entries
entry.message?  # true if Message
entry.entryable # Returns the Message or Comment
```

---

## Callbacks Best Practices

```ruby
class Task < ApplicationRecord
  # GOOD - Simple callbacks
  before_validation :normalize_tracking_number, on: :create
  after_commit :notify_recipient, on: :create

  # BAD - Side effects in callbacks
  # after_save :send_email  # May fail silently, hard to test

  # BETTER - Use service objects
  # TasksManager::CreateTask handles notifications

  private

  def normalize_tracking_number
    self.tracking_number = tracking_number&.upcase&.strip
  end

  def notify_recipient
    TaskNotificationJob.perform_later(id)
  end
end
```

**Callback Order:**
1. before_validation
2. after_validation
3. before_save
4. before_create/before_update
5. after_create/after_update
6. after_save
7. after_commit (only after transaction commits)
