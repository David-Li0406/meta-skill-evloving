---
name: active-record-query-patterns
description: Use this skill when writing database queries, designing model associations, creating migrations, optimizing query performance, or debugging N+1 queries and GROUP BY errors.
---

# ActiveRecord Query Patterns

This skill provides comprehensive guidance for writing efficient, correct ActiveRecord queries in Rails applications with PostgreSQL.

## When to Use This Skill

- Writing complex ActiveRecord queries
- Designing model associations
- Creating database migrations
- Optimizing query performance
- Debugging N+1 queries
- Working with GROUP BY operations
- Implementing scopes and query objects

## Query Decision Tree

```
What do I need?
│
├─ Find records by ID or attributes?
│   ├─ Single record: find(id), find_by(attrs)
│   └─ Multiple records: where(conditions)
│
├─ Access associated records?
│   ├─ Just filtering? → joins(:association)
│   └─ Loading data? → includes(:association)
│
├─ Aggregate data (count, sum, avg)?
│   └─ GROUP BY query
│       └─ REMEMBER: Every SELECT column must be in GROUP BY or aggregate
│
├─ Complex multi-step query?
│   └─ Query Object pattern (app/queries/)
│
├─ Hierarchical/recursive data?
│   └─ CTE (Common Table Expression)
│
└─ Full-text search?
    └─ pg_search gem with tsvector indexes
```

## Model Structure

### Standard Model Template

```ruby
class Task < ApplicationRecord
  # == Constants ============================================================
  STATUSES = %w[pending in_progress completed failed cancelled].freeze

  # == Associations =========================================================
  belongs_to :account
  belongs_to :merchant
  belongs_to :carrier, optional: true
  belongs_to :recipient
  belongs_to :zone, optional: true
  
  has_many :timelines, dependent: :destroy
  has_many :task_actions, dependent: :destroy
  has_many :photos, dependent: :destroy

  # == Validations ==========================================================
  validates :status, presence: true, inclusion: { in: STATUSES }
  validates :tracking_number, presence: true, uniqueness: { scope: :account_id }

  # == Scopes ===============================================================
  scope :active, -> { where.not(status: %w[completed failed cancelled]) }
  scope :completed, -> { where(status: 'completed') }
  scope :for_carrier, ->(carrier) { where(carrier: carrier) }
  scope :created_between, ->(start_date, end_date) { where(created_at: start_date..end_date) }
  scope :by_status, ->(status) { where(status: status) if status.present? }

  # == Callbacks ============================================================
  before_validation :generate_tracking_number, on: :create
  after_commit :notify_recipient, on: :create

  # == Class Methods ========================================================
  def self.search(query)
    where("tracking_number ILIKE :q OR description ILIKE :q", q: "%#{query}%")
  end

  # == Instance Methods =====================================================
  def completable?
    %w[pending in_progress].include?(status)
  end

  def complete!
    update!(status: 'completed', completed_at: Time.current)
  end

  private

  def generate_tracking_number
    self.tracking_number ||= SecureRandom.hex(8).upcase
  end

  def notify_recipient
    TaskNotificationJob.perform_later(id)
  end
end
```

## Eager Loading Quick Reference

| Method | Query Type | Use Case |
|--------|-----------|----------|
| `includes` | Smart (auto-selects) | Default choice |
| `preload` | Separate queries | Can't filter on association |
| `eager_load` | LEFT JOIN | Need to filter on association |
| `joins` | INNER JOIN | Filtering only, no data loading |

## Avoiding N+1 Queries

```ruby
# WRONG - N+1 query
tasks = Task.all
tasks.each { |t| puts t.carrier.name }  # Query per task!

# CORRECT - Eager loading
tasks = Task.includes(:carrier)
tasks.each { |t| puts t.carrier.name }  # Single query
```

## GROUP BY Queries (Critical for PostgreSQL)

**Rule**: Every non-aggregated column in SELECT must appear in GROUP BY.

```ruby
# CORRECT - Only grouped columns and aggregates
Task.group(:status).count
# => { "pending" => 10, "completed" => 25 }

# CORRECT - Multiple GROUP BY columns
Task.group(:status, :task_type).count

# CORRECT - Explicit select with aggregates
Task.select(:status, 'COUNT(*) as task_count', 'AVG(amount) as avg_amount').group(:status)

# WRONG - includes with group
Task.includes(:carrier).group(:status).count  # ERROR!
```

## Migration Patterns

### Create Table

```ruby
class CreateTasks < ActiveRecord::Migration[7.1]
  def change
    create_table :tasks do |t|
      t.references :account, null: false, foreign_key: true
      t.references :merchant, null: false, foreign_key: true
      t.references :carrier, foreign_key: true  # nullable
      
      t.string :tracking_number, null: false
      t.string :status, null: false, default: 'pending'
      t.decimal :amount, precision: 10, scale: 2
      t.jsonb :metadata, default: {}
      
      t.datetime :completed_at
      t.timestamps
      
      t.index :tracking_number, unique: true
      t.index :status
      t.index [:account_id, :status]
      t.index [:merchant_id, :created_at]
      t.index :metadata, using: :gin  # For JSONB queries
    end
  end
end
```

## Performance Optimization

### Batch Processing

```ruby
# WRONG - Loads all records into memory
Task.all.each { |task| process(task) }

# CORRECT - Batches of 1000
Task.find_each(batch_size: 1000) { |task| process(task) }
```

### Select Only Needed Columns

```ruby
# WRONG - Loads all columns
users = User.all
users.each { |u| puts u.email }

# CORRECT - Only needed columns
users = User.select(:id, :email)
users.each { |u| puts u.email }
```

## Debugging Queries

```ruby
# Enable logging
ActiveRecord::Base.logger = Logger.new(STDOUT)

# Explain query plan
Task.where(status: 'pending').explain(:analyze)

# Use Bullet gem for N+1 detection
# Gemfile: gem 'bullet', group: :development
```

## Pre-Query Checklist

Before writing any complex query:

```
[ ] What columns am I selecting?
[ ] Am I using GROUP BY? If so, is every SELECT column grouped or aggregated?
[ ] Am I using includes/preload with GROUP BY? (DON'T!)
[ ] Will this query run on a large table? Do indexes exist?
[ ] Am I iterating and accessing associations? Use includes.
[ ] Am I loading more data than needed? Use select/pluck.
[ ] Is this sensitive data? Consider ActiveRecord::Encryption.
[ ] Should this be in a separate database? (multi-database)
[ ] Is this a hierarchical query? Consider CTEs.
[ ] Need full-text search? Use pg_search.
```

## References

Detailed patterns and examples in `references/`:
- `associations.md` - Association types, options, polymorphic
- `query-patterns.md` - Basic queries, eager loading, subqueries
- `scopes-query-objects.md` - Scope patterns, query objects
- `migrations.md` - Create table, safe migrations, JSONB
- `performance.md` - Batch processing, counter caches, indexes
- `rails7-8-features.md` - Composite keys, encryption, multi-db
- `advanced-patterns.md` - Enums, database views, CTEs, STI
- `postgresql-features.md` - Full-text search, JSONB, arrays