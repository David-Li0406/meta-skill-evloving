# Modern Rails & Ruby Features

## Rails 7.1+ Features

### Composite Primary Keys

```ruby
class BookOrder < ApplicationRecord
  self.primary_key = [:shop_id, :id]
  belongs_to :shop
  has_many :line_items, foreign_key: [:shop_id, :order_id]
end
```

### ActiveRecord Encryption

```ruby
class User < ApplicationRecord
  encrypts :email, deterministic: true
  encrypts :ssn, :credit_card
end
```

### Horizontal Sharding

```ruby
class ApplicationRecord < ActiveRecord::Base
  connects_to shards: {
    default: { writing: :primary, reading: :primary_replica },
    shard_two: { writing: :primary_shard_two }
  }
end
```

### Async Query Loading

```ruby
posts = Post.where(published: true).load_async
# Do other work while query runs
posts.to_a # Wait for results
```

### Normalize Values

```ruby
class User < ApplicationRecord
  normalizes :email, with: -> { _1.strip.downcase }
  normalizes :phone, with: -> { _1.gsub(/\D/, '') }
end
```

---

## Rails 8.0+ Features

### Built-in Queue (Solid Queue)

```ruby
# config/application.rb
config.active_job.queue_adapter = :solid_queue
```

### Built-in Cache (Solid Cache)

```ruby
# config/application.rb
config.cache_store = :solid_cache_store
```

### Authentication Generator

```bash
rails generate authentication
```

### Built-in Rate Limiting

```ruby
class Api::PostsController < Api::BaseController
  rate_limit to: 10, within: 1.minute, only: :create
end
```

### Per-Environment Credentials

```bash
rails credentials:edit --environment production
```

---

## Modern Ruby 3.3+ Features

### Pattern Matching

```ruby
case user
in { role: "admin", active: true }
  grant_full_access
in { role: "user", active: true }
  grant_standard_access
else
  deny_access
end
```

### Endless Method Definitions

```ruby
def full_name = "#{first_name} #{last_name}"
def published? = published_at.present?
def admin? = role == 'admin'
```

### Data Class (Ruby 3.2+)

```ruby
User = Data.define(:id, :name, :email)
user = User.new(id: 1, name: "Alice", email: "alice@example.com")

# Immutable
user.id = 2 # raises FrozenError
```

### YJIT Optimization (Ruby 3.3+)

```ruby
# config/application.rb
if defined?(RubyVM::YJIT.enable)
  RubyVM::YJIT.enable
end
```

---

## Model Concerns Best Practices

### Good: Truly Shared Behavior

```ruby
# app/models/concerns/publishable.rb
module Publishable
  extend ActiveSupport::Concern

  included do
    scope :published, -> { where(published: true) }
    scope :draft, -> { where(published: false) }

    validates :published_at, presence: true, if: :published?
  end

  def publish!
    update!(published: true, published_at: Time.current)
  end

  def unpublish!
    update!(published: false, published_at: nil)
  end
end

# Used in 3+ unrelated models
class Post < ApplicationRecord
  include Publishable
end

class Video < ApplicationRecord
  include Publishable
end
```

### Concern with Dependencies

```ruby
# app/models/concerns/taggable.rb
module Taggable
  extend ActiveSupport::Concern

  included do
    has_many :taggings, as: :taggable, dependent: :destroy
    has_many :tags, through: :taggings

    scope :tagged_with, ->(tag_name) {
      joins(:tags).where(tags: { name: tag_name })
    }
  end

  def tag_names=(names)
    self.tags = names.map { |n| Tag.find_or_create_by(name: n.strip) }
  end

  def tag_names
    tags.pluck(:name)
  end

  class_methods do
    def most_tagged(limit = 10)
      select('taggable_id, COUNT(*) as tags_count')
        .group('taggable_id')
        .order('tags_count DESC')
        .limit(limit)
    end
  end
end
```

---

## Method Visibility Rules

### Public

```ruby
# Callable from anywhere, defines the API
# - Controller actions must be public
# - Methods called from views must be public
# - Service interface methods
```

### Private

```ruby
# Implementation details, helper methods
# - Controller: before_action callbacks, helper methods
# - Service: internal computation methods
# - Model: internal validation helpers

# CRITICAL: Private methods CANNOT be called from outside the class
# If a view needs data, the component MUST have a public method
```

### Protected

```ruby
# Callable from same class or subclasses
# - Occasionally in base controllers/models for shared behavior
# - Rare in typical Rails apps
```

---

## Delegation Patterns

### Using delegate

```ruby
# Creates public forwarding methods
delegate :total, :count, to: :@service

class Component < ViewComponent::Base
  delegate :total, :count, to: :@service

  def initialize(service:)
    @service = service
  end
end
# Now view can call component.total
```

### Wrapper Methods

```ruby
# Use when:
# - Need to transform data
# - Need to add caching
# - Need different method names
# - Need to handle errors

class Component < ViewComponent::Base
  def total
    @service.calculate_total
  rescue ServiceError
    0
  end
end
```
