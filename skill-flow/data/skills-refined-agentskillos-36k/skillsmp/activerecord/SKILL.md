---
name: activerecord
description: This skill should be used when the user asks about "ActiveRecord", "database queries", "associations", "validations", "migrations", "scopes", "callbacks", "N+1 queries", "eager loading", "includes", "joins", "eager_load", "preload", "database optimization", "model relationships", "has_many", "belongs_to", "has_one", "polymorphic associations", "pluck", "exists", or needs guidance on database-related Rails topics.
version: 1.1.0
---

# ActiveRecord

Comprehensive guide to ActiveRecord associations, queries, validations, and database optimization in Rails.

## Associations

### Association Types

| Type | Description |
|------|-------------|
| `belongs_to` | Foreign key on this model's table |
| `has_one` | Foreign key on other model's table (singular) |
| `has_many` | Foreign key on other model's table (plural) |
| `has_many :through` | Many-to-many via join model |
| `has_one :through` | One-to-one via join model |
| `has_and_belongs_to_many` | Many-to-many via join table (no model) |

### Basic Associations

```ruby
class User < ApplicationRecord
  has_one :profile, dependent: :destroy
  has_many :articles, dependent: :destroy
  has_many :comments, dependent: :destroy
end

class Article < ApplicationRecord
  belongs_to :user
  belongs_to :category, optional: true  # Allow nil
  has_many :comments, dependent: :destroy
  has_many :taggings, dependent: :destroy
  has_many :tags, through: :taggings
end
```

### Association Options

| Option | Purpose |
|--------|---------|
| `dependent: :destroy` | Delete associated records via callbacks |
| `dependent: :delete_all` | Delete directly via SQL (no callbacks) |
| `dependent: :nullify` | Set foreign key to NULL |
| `dependent: :restrict_with_error` | Add error if associated records exist |
| `dependent: :restrict_with_exception` | Raise exception if associated |
| `optional: true` | Allow nil belongs_to (required by default in Rails 5+) |
| `inverse_of` | Specify inverse association for bidirectional optimization |
| `counter_cache: true` | Maintain count column automatically |
| `touch: true` | Update parent's `updated_at` on changes |
| `class_name` | Specify associated class when name differs |
| `foreign_key` | Specify custom foreign key column |

### Has Many Through

```ruby
class Doctor < ApplicationRecord
  has_many :appointments
  has_many :patients, through: :appointments
end

class Patient < ApplicationRecord
  has_many :appointments
  has_many :doctors, through: :appointments
end

class Appointment < ApplicationRecord
  belongs_to :doctor
  belongs_to :patient
  # Join model can have its own attributes: appointment_date, notes, etc.
end
```

### Polymorphic Associations

```ruby
class Comment < ApplicationRecord
  belongs_to :commentable, polymorphic: true
end

class Article < ApplicationRecord
  has_many :comments, as: :commentable
end

class Photo < ApplicationRecord
  has_many :comments, as: :commentable
end

# Migration
create_table :comments do |t|
  t.references :commentable, polymorphic: true, index: true
  t.text :body
  t.timestamps
end
```

### Self-Referential

```ruby
class Employee < ApplicationRecord
  belongs_to :manager, class_name: "Employee", optional: true
  has_many :subordinates, class_name: "Employee", foreign_key: "manager_id"
end
```

## Validations

### Built-in Validation Helpers

```ruby
class User < ApplicationRecord
  # Presence - not empty (uses Object#blank?)
  validates :name, presence: true

  # Absence - must be blank
  validates :spam_flag, absence: true

  # Acceptance - checkbox must be checked
  validates :terms_of_service, acceptance: true

  # Confirmation - two fields must match
  validates :email, confirmation: true
  # Requires email_confirmation field in form

  # Uniqueness (case-insensitive)
  validates :email, uniqueness: { case_sensitive: false, scope: :account_id }

  # Format - regex match
  validates :email, format: { with: URI::MailTo::EMAIL_REGEXP }

  # Length
  validates :password, length: { minimum: 8, maximum: 72 }
  validates :bio, length: { maximum: 500, too_long: "%{count} characters max" }
  validates :code, length: { is: 6 }
  validates :name, length: { in: 2..50 }

  # Numericality
  validates :age, numericality: { only_integer: true, greater_than: 0 }
  validates :price, numericality: { greater_than_or_equal_to: 0 }

  # Inclusion - value must be in list
  validates :role, inclusion: { in: %w[admin editor viewer] }

  # Exclusion - value must NOT be in list
  validates :subdomain, exclusion: { in: %w[www admin api] }

  # Comparison - compare to another attribute or value
  validates :end_date, comparison: { greater_than: :start_date }
  validates :age, comparison: { greater_than_or_equal_to: 18 }

  # Associated records must also be valid
  validates_associated :profile
end
```

### Common Validation Options

| Option | Purpose |
|--------|---------|
| `:message` | Custom error message (supports `%{value}`, `%{attribute}`, `%{model}`) |
| `:on` | When to validate: `:create`, `:update`, or custom context |
| `:allow_nil` | Skip validation if value is `nil` |
| `:allow_blank` | Skip validation if value is blank |
| `:if` / `:unless` | Conditional validation (symbol, proc, or array) |
| `:strict` | Raise `ActiveModel::StrictValidationFailed` instead of adding error |

### Conditional Validations

```ruby
class Order < ApplicationRecord
  validates :shipping_address, presence: true, if: :requires_shipping?
  validates :credit_card, presence: true, unless: :free_order?

  # Proc
  validates :coupon_code, presence: true, if: -> { discount_percentage.present? }

  # Multiple conditions (all :if must pass AND none of :unless)
  validates :phone, presence: true, if: [:contact_by_phone?, :phone_required?]

  # Group validations
  with_options if: :premium_user? do
    validates :credit_card, presence: true
    validates :billing_address, presence: true
  end
end
```

### Custom Validations

```ruby
class User < ApplicationRecord
  validate :email_domain_allowed
  validates_with EmailValidator

  private

  def email_domain_allowed
    return if email.blank?
    domain = email.split("@").last
    errors.add(:email, "must be from an allowed domain") unless allowed_domain?(domain)
  end
end

# Custom validator class
class EmailValidator < ActiveModel::Validator
  def validate(record)
    unless record.email.include?("@")
      record.errors.add(:email, "must contain @")
    end
  end
end
```

## Scopes

```ruby
class Article < ApplicationRecord
  scope :published, -> { where(status: "published") }
  scope :draft, -> { where(status: "draft") }
  scope :recent, -> { order(created_at: :desc) }

  # With arguments
  scope :by_author, ->(author) { where(author: author) }
  scope :created_after, ->(date) { where(created_at: date..) }

  # With defaults
  scope :limit_recent, ->(count = 10) { recent.limit(count) }

  # Combining
  scope :featured, -> { published.where(featured: true).recent }
end

# Chainable
Article.published.by_author(user).recent.limit(5)
```

## Queries

### Finding Records

```ruby
# Single record
User.find(1)                        # Raises RecordNotFound if missing
User.find_by(email: "a@b.com")      # Returns nil if missing
User.find_by!(email: "a@b.com")     # Raises if missing
User.first                          # First by primary key
User.last                           # Last by primary key
User.take                           # Any record (no ordering)

# Collections
User.where(status: "active")
User.where.not(role: "admin")
User.where(created_at: 1.week.ago..)  # Range (>= 1 week ago)
User.where(age: 18..65)               # BETWEEN

# OR conditions
User.where(role: "admin").or(User.where(role: "editor"))

# Selection
User.select(:id, :email, :name)     # Specific columns
User.distinct                        # Remove duplicates
```

### Efficient Data Extraction

```ruby
# pluck - returns array of values (no model instantiation)
User.pluck(:email)                    # ["a@b.com", "c@d.com"]
User.pluck(:id, :email)               # [[1, "a@b.com"], [2, "c@d.com"]]
User.where(active: true).pluck(:id)

# ids - shortcut for pluck(:id)
User.where(active: true).ids          # [1, 2, 3]

# exists? - boolean check without loading records
User.exists?(email: "a@b.com")        # true/false
User.where(role: "admin").exists?     # true/false

# count/sum/average/minimum/maximum
Order.count
Order.sum(:total)
Order.average(:total)
Order.maximum(:created_at)
```

### Ordering and Limiting

```ruby
User.order(created_at: :desc)
User.order(last_name: :asc, first_name: :asc)
User.order(Arel.sql("LOWER(name)"))   # Raw SQL (use carefully)

User.limit(10)
User.offset(20).limit(10)             # Pagination
```

### Complex Conditions

```ruby
# Parameterized SQL (prevents injection)
User.where("created_at > ? AND role = ?", 1.week.ago, "admin")

# Named parameters
User.where("name LIKE :q OR email LIKE :q", q: "%#{search}%")

# Subqueries
active_ids = User.where(active: true).select(:id)
Article.where(user_id: active_ids)

# Group and having
Order.group(:status).count                    # { "pending" => 5, "shipped" => 10 }
Order.group(:user_id).having("COUNT(*) > 5")
```

## Eager Loading (N+1 Prevention)

### The Problem

```ruby
# BAD: N+1 queries (1 + 10 = 11 queries)
articles = Article.limit(10)
articles.each { |a| puts a.author.name }

# GOOD: 2 queries total
articles = Article.includes(:author).limit(10)
articles.each { |a| puts a.author.name }
```

### Methods Comparison

| Method | Strategy | Use When |
|--------|----------|----------|
| `includes` | Rails decides (2 queries OR JOIN) | General use |
| `preload` | Always separate queries | Large datasets, simpler queries |
| `eager_load` | Always LEFT OUTER JOIN | Need to filter/order by association |

```ruby
# includes - default choice
Article.includes(:author, :tags)
Article.includes(comments: :user)

# preload - separate queries
Article.preload(:author, :comments)

# eager_load - single JOIN query (required for filtering)
Article.eager_load(:author).where(users: { role: "admin" })

# joins - INNER JOIN for filtering only (doesn't load association)
Article.joins(:author).where(users: { active: true })
# Note: joins doesn't prevent N+1 if you access the association!
```

## Callbacks

```ruby
class Article < ApplicationRecord
  # Lifecycle order: validation → save → create/update → commit
  before_validation :normalize_title
  before_save :sanitize_content
  after_create :notify_subscribers
  after_commit :update_search_index, on: :create

  private

  def notify_subscribers
    # Use jobs for external operations
    NotifySubscribersJob.perform_later(id)
  end
end
```

**Best practices:**
- Keep callbacks simple and synchronous
- Use `after_commit` for external services (email, webhooks)
- Move complex logic to service objects
- Avoid callbacks that trigger other callbacks

## Migrations

### Common Operations

```ruby
class CreateArticles < ActiveRecord::Migration[7.1]
  def change
    create_table :articles do |t|
      t.string :title, null: false
      t.text :body
      t.integer :view_count, default: 0
      t.boolean :published, default: false
      t.decimal :price, precision: 10, scale: 2
      t.datetime :published_at
      t.references :user, null: false, foreign_key: true
      t.timestamps
    end

    add_index :articles, :title
    add_index :articles, [:user_id, :published_at]
  end
end
```

### Safe Migrations

```ruby
# Add index concurrently (PostgreSQL, no locks)
class AddIndexToArticles < ActiveRecord::Migration[7.1]
  disable_ddl_transaction!

  def change
    add_index :articles, :title, algorithm: :concurrently
  end
end
```

## Batch Processing

```ruby
# find_each - loads in batches, yields one at a time
User.find_each(batch_size: 1000) { |user| process(user) }

# in_batches - yields batches as relations
User.in_batches(of: 1000) do |batch|
  batch.update_all(processed: true)
end
```

## Additional Resources

### Reference Files

- **`references/query-optimization.md`** - N+1 detection, indexing strategies
