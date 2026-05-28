# Scopes & Query Objects Reference

## Simple Scopes

```ruby
class Task < ApplicationRecord
  scope :active, -> { where.not(status: %w[completed cancelled]) }
  scope :completed, -> { where(status: 'completed') }
  scope :recent, -> { order(created_at: :desc) }
  scope :today, -> { where(created_at: Time.current.all_day) }
end
```

---

## Parameterized Scopes

```ruby
class Task < ApplicationRecord
  scope :by_status, ->(status) { where(status: status) }
  scope :created_after, ->(date) { where('created_at >= ?', date) }
  scope :for_carrier, ->(carrier_id) { where(carrier_id: carrier_id) }

  # With default
  scope :recent, ->(limit = 10) { order(created_at: :desc).limit(limit) }

  # Conditional scope
  scope :by_status_if_present, ->(status) { where(status: status) if status.present? }
end
```

---

## Chainable Scopes

```ruby
# All scopes are chainable
Task.active.recent.by_status('pending').for_carrier(123)

# Combine with where
Task.active.where(merchant_id: 456)
```

---

## Query Objects Pattern

For complex queries that don't fit in scopes:

```ruby
# app/queries/tasks/pending_delivery_query.rb
module Tasks
  class PendingDeliveryQuery
    def initialize(relation = Task.all)
      @relation = relation
    end

    def call(zone_id: nil, since: 24.hours.ago)
      result = @relation
        .where(status: 'pending')
        .where('created_at >= ?', since)
        .includes(:carrier, :recipient)

      result = result.where(zone_id: zone_id) if zone_id.present?
      result.order(created_at: :asc)
    end
  end
end

# Usage
Tasks::PendingDeliveryQuery.new.call(zone_id: 123)
Tasks::PendingDeliveryQuery.new(account.tasks).call(since: 1.hour.ago)
```

---

## Scope vs Class Method

```ruby
# Scope - returns relation even if nil
scope :by_status, ->(status) { where(status: status) if status.present? }
Task.by_status(nil)  # Returns Task.all (not nil)

# Class method - may return nil
def self.by_status(status)
  where(status: status) if status.present?  # Returns nil!
end
Task.by_status(nil)  # Returns nil - breaks chaining

# CORRECT class method
def self.by_status(status)
  return all unless status.present?
  where(status: status)
end
```

---

## Merging Scopes

```ruby
class Task < ApplicationRecord
  scope :active, -> { where(status: %w[pending in_progress]) }
end

class Carrier < ApplicationRecord
  scope :verified, -> { where(verified: true) }
end

# Merge scopes from different models
Task.joins(:carrier).merge(Carrier.verified).active
```
