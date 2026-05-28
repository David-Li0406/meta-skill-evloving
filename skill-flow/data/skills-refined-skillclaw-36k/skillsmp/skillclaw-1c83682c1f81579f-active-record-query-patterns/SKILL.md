---
name: active-record-query-patterns
description: Use this skill when writing database queries, designing model associations, creating migrations, optimizing query performance, or debugging N+1 queries and GROUP BY errors.
---

# ActiveRecord Query Patterns

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

## Common Pitfalls

**NEVER** use `includes` with `group`:
```ruby
# WRONG - PostgreSQL error
Task.includes(:carrier).group(:status).count

# RIGHT - Separate queries
status_counts = Task.group(:status).count
tasks = Task.where(status: status_counts.keys.first).includes(:carrier)
```

**NEVER** iterate without eager loading:
```ruby
# WRONG - N+1 queries
tasks = Task.all
tasks.each { |t| puts t.carrier.name }  # Query per task!

# RIGHT - Eager load
tasks = Task.includes(:carrier)
tasks.each { |t| puts t.carrier.name }  # Single query
```

**NEVER** load all records into memory:
```ruby
# WRONG - Memory explosion
Task.all.each { |task| process(task) }

# RIGHT - Batch processing
Task.find_each(batch_size: 1000) { |task| process(task) }
```

**NEVER** use `present?` to check existence:
```ruby
# WRONG - Loads all records
Task.where(status: 'pending').present?

# RIGHT - Efficient existence check
Task.where(status: 'pending').exists?
```

**NEVER** forget indexes on foreign keys:
```ruby
# WRONG - No index
t.references :merchant, foreign_key: true, index: false

# RIGHT - Always index foreign keys
t.references :merchant, null: false, foreign_key: true  # index: true is default
```

## Model Template

```ruby
# app/models/task.rb
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
end
```