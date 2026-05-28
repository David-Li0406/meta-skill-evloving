# Performance Optimization Reference

## Batch Processing

```ruby
# WRONG - Loads all records into memory
Task.all.each { |task| process(task) }

# CORRECT - Batches of 1000
Task.find_each(batch_size: 1000) { |task| process(task) }

# With specific order
Task.order(:id).find_each { |task| process(task) }

# In batches (for batch operations)
Task.in_batches(of: 1000) do |batch|
  batch.update_all(processed: true)
end
```

---

## Select Only Needed Columns

```ruby
# WRONG - Loads all columns
users = User.all
users.each { |u| puts u.email }

# CORRECT - Only needed columns
users = User.select(:id, :email)
users.each { |u| puts u.email }

# With pluck (returns arrays, not AR objects)
emails = User.pluck(:email)
```

---

## Counter Caches

```ruby
# Migration
add_column :merchants, :tasks_count, :integer, default: 0

# Model
class Task < ApplicationRecord
  belongs_to :merchant, counter_cache: true
end

# Now merchant.tasks_count doesn't query
merchant.tasks_count  # Uses cached count
```

---

## Exists? vs Any? vs Present?

| Method | Query | Performance |
|--------|-------|-------------|
| `exists?` | `SELECT 1 ... LIMIT 1` | Best |
| `any?` | May load records | Medium |
| `present?` | `SELECT * ...` | Worst |

```ruby
# EFFICIENT - Stops at first match
Task.where(status: 'pending').exists?
# SELECT 1 FROM tasks WHERE status = 'pending' LIMIT 1

# INEFFICIENT - Loads all records
Task.where(status: 'pending').present?
# SELECT * FROM tasks WHERE status = 'pending'
```

---

## Explain & Analyze

```ruby
# In Rails console
Task.where(status: 'pending').explain
Task.where(status: 'pending').explain(:analyze)

# Look for "Seq Scan" on large tables - may need index
```

---

## Index Strategy

```ruby
# Index columns used in WHERE clauses
add_index :tasks, :status

# Composite index for multi-column queries
add_index :tasks, [:account_id, :status]

# Partial index for common queries
add_index :tasks, :created_at, where: "status = 'pending'"

# Covering index (includes columns to avoid table lookup)
add_index :tasks, [:status, :created_at], include: [:id, :tracking_number]
```

---

## Avoiding N+1 with Bullet

```ruby
# Gemfile
gem 'bullet', group: :development

# config/environments/development.rb
config.after_initialize do
  Bullet.enable = true
  Bullet.alert = true
  Bullet.console = true
end
```

---

## Caching

```ruby
# Fragment caching
Rails.cache.fetch("task_#{task.id}_summary", expires_in: 1.hour) do
  task.calculate_summary
end

# Counter cache reset
Task.reset_counters(merchant.id, :tasks)

# Query caching (automatic in requests)
# Manual:
ActiveRecord::Base.cache do
  User.find(1)  # Cached
  User.find(1)  # Returns cached result
end
```
