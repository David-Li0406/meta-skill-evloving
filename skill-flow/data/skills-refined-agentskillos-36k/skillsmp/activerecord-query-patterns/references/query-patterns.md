# Query Patterns Reference

## Basic Queries

```ruby
# Find
Task.find(1)                    # Raises RecordNotFound
Task.find_by(id: 1)             # Returns nil if not found
Task.find_by!(id: 1)            # Raises RecordNotFound

# Where
Task.where(status: 'pending')
Task.where(status: %w[pending in_progress])  # IN query
Task.where.not(status: 'completed')
Task.where(created_at: 1.week.ago..)         # Range (>= date)
Task.where(created_at: ..1.week.ago)         # Range (<= date)
Task.where(created_at: 1.month.ago..1.week.ago)  # Between

# Order
Task.order(created_at: :desc)
Task.order(:status, created_at: :desc)

# Limit & Offset
Task.limit(10).offset(20)

# Distinct
Task.distinct.pluck(:status)
```

---

## Eager Loading Strategies

| Method | Query Type | Use Case |
|--------|-----------|----------|
| `includes` | Smart (preload or eager_load) | Default choice |
| `preload` | Separate queries | Large result sets |
| `eager_load` | LEFT JOIN | Need to filter on association |
| `joins` | INNER JOIN | Filtering only, no data loading |

```ruby
# includes - Smart loading
Task.includes(:carrier)

# preload - Separate queries (can't filter on association)
Task.preload(:carrier)
# SELECT * FROM tasks
# SELECT * FROM carriers WHERE id IN (...)

# eager_load - Single LEFT JOIN query
Task.eager_load(:carrier)
# SELECT tasks.*, carriers.* FROM tasks LEFT JOIN carriers...

# joins - INNER JOIN (no loading, just filtering)
Task.joins(:carrier).where(carriers: { active: true })
```

---

## Multiple/Nested Associations

```ruby
# Multiple associations
Task.includes(:carrier, :merchant, :recipient)

# Nested associations
Task.includes(merchant: :branches)

# With conditions on association
Task.includes(:carrier).where(carriers: { active: true }).references(:carriers)
```

---

## Subqueries

```ruby
# Subquery in WHERE
active_carrier_ids = Carrier.where(active: true).select(:id)
Task.where(carrier_id: active_carrier_ids)
# SELECT * FROM tasks WHERE carrier_id IN (SELECT id FROM carriers WHERE active = true)

# Subquery with join
Task.where(carrier_id: Carrier.active.select(:id))
    .where(merchant_id: Merchant.premium.select(:id))
```

---

## Raw SQL (Safe)

```ruby
# Safe with sanitization
Task.where("created_at > ?", 1.week.ago)
Task.where("description ILIKE ?", "%#{query}%")

# Named bindings
Task.where("status = :status AND amount > :min", status: 'pending', min: 100)

# Select with raw SQL
Task.select("*, amount * 0.1 as commission")

# Find by SQL
Task.find_by_sql(["SELECT * FROM tasks WHERE status = ?", 'pending'])
```

---

## GROUP BY Queries

**PostgreSQL Rule**: Every non-aggregated column in SELECT must appear in GROUP BY.

```ruby
# CORRECT - Only grouped columns and aggregates
Task.group(:status).count
# => { "pending" => 10, "completed" => 25 }

Task.group(:status).sum(:amount)
# => { "pending" => 1000, "completed" => 5000 }

# CORRECT - Multiple GROUP BY columns
Task.group(:status, :task_type).count
# => { ["pending", "express"] => 5, ["completed", "standard"] => 10 }

# CORRECT - Explicit select with aggregates
Task.select(:status, 'COUNT(*) as task_count', 'AVG(amount) as avg_amount')
    .group(:status)

# CORRECT - Date grouping
Task.group("DATE(created_at)").count

# WRONG - includes with group
Task.includes(:carrier).group(:status).count  # ERROR!

# CORRECT - Separate queries if you need associated data
status_counts = Task.group(:status).count
tasks_by_status = status_counts.keys.each_with_object({}) do |status, hash|
  hash[status] = Task.where(status: status).includes(:carrier).limit(5)
end
```
