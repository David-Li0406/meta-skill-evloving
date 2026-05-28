# Association Patterns Reference

## Basic Associations

```ruby
# One-to-Many
class Account < ApplicationRecord
  has_many :users, dependent: :destroy
  has_many :tasks, dependent: :destroy
end

class User < ApplicationRecord
  belongs_to :account
end

# Many-to-Many (with join table)
class Task < ApplicationRecord
  has_many :task_tags, dependent: :destroy
  has_many :tags, through: :task_tags
end

class Tag < ApplicationRecord
  has_many :task_tags, dependent: :destroy
  has_many :tasks, through: :task_tags
end

class TaskTag < ApplicationRecord
  belongs_to :task
  belongs_to :tag
end

# Polymorphic
class Comment < ApplicationRecord
  belongs_to :commentable, polymorphic: true
end

class Task < ApplicationRecord
  has_many :comments, as: :commentable
end

class Invoice < ApplicationRecord
  has_many :comments, as: :commentable
end
```

---

## Association Options

```ruby
class Task < ApplicationRecord
  # Foreign key specification
  belongs_to :creator, class_name: 'User', foreign_key: 'created_by_id'

  # Optional association
  belongs_to :carrier, optional: true

  # Counter cache
  belongs_to :merchant, counter_cache: true

  # Dependent options
  has_many :photos, dependent: :destroy      # Delete associated records
  has_many :logs, dependent: :nullify        # Set foreign key to NULL
  has_many :exports, dependent: :restrict_with_error  # Prevent deletion

  # Scoped association
  has_many :active_timelines, -> { where(active: true) }, class_name: 'Timeline'

  # Touch parent on update
  belongs_to :bundle, touch: true
end
```

---

## Dependent Options

| Option | Behavior |
|--------|----------|
| `:destroy` | Call destroy on each associated record |
| `:delete_all` | Delete directly via SQL (no callbacks) |
| `:nullify` | Set foreign keys to NULL |
| `:restrict_with_error` | Add error if associated records exist |
| `:restrict_with_exception` | Raise exception if associated exist |

---

## Self-Referential Associations

```ruby
class Employee < ApplicationRecord
  belongs_to :manager, class_name: 'Employee', optional: true
  has_many :subordinates, class_name: 'Employee', foreign_key: 'manager_id'
end
```

---

## Has One Through

```ruby
class Supplier < ApplicationRecord
  has_one :account
  has_one :account_history, through: :account
end

class Account < ApplicationRecord
  belongs_to :supplier
  has_one :account_history
end
```
