# Code Organization in Large Rails Applications

## Signs Your Model Is Too Big

- Over 300 lines
- More than 20 public methods
- Multiple unrelated responsibilities
- Hard to test in isolation
- Developers afraid to modify it

## Strategies for Breaking Up Large Models

### 1. Extract Concerns for Shared Behavior

```ruby
# Before: 500-line User model
class User < ApplicationRecord
  # Authentication code (100 lines)
  # Profile code (80 lines)
  # Notification preferences (60 lines)
  # Billing code (120 lines)
  # Activity tracking (80 lines)
end

# After: Concerns extract cohesive behavior
class User < ApplicationRecord
  include Authentication      # app/models/concerns/authentication.rb
  include HasProfile         # app/models/concerns/has_profile.rb
  include Notifiable         # app/models/concerns/notifiable.rb
  include Billable           # app/models/concerns/billable.rb
  include Trackable          # app/models/concerns/trackable.rb
end
```

### 2. Extract Service Objects for Operations

```ruby
# Before: Fat method in model
class Order < ApplicationRecord
  def process_payment
    # 50 lines of payment processing
  end
end

# After: Service object
class Orders::PaymentProcessor
  def initialize(order)
    @order = order
  end

  def call
    # Clean, focused logic
  end
end
```

### 3. Extract Query Objects for Complex Queries

```ruby
# Before: Complex scope chain in model
class Product < ApplicationRecord
  scope :available_for_user, ->(user) {
    # 30 lines of complex query logic
  }
end

# After: Query object
class Products::AvailableForUserQuery
  def initialize(user)
    @user = user
  end

  def call
    # Complex query with clear intent
  end
end
```

### 4. Use Aggregates for Related Models

```ruby
# Domain aggregate: Shopping Cart
# app/models/shopping_cart.rb (aggregate root)
class ShoppingCart < ApplicationRecord
  has_many :line_items, dependent: :destroy

  def add_product(product, quantity: 1)
    # Coordinating logic lives here
  end

  def total
    line_items.sum(&:subtotal)
  end
end

# app/models/line_item.rb (child entity)
class LineItem < ApplicationRecord
  belongs_to :shopping_cart
  belongs_to :product

  def subtotal
    unit_price * quantity
  end
end
```

## Directory Structure for Large Apps

```
app/
├── controllers/
│   ├── admin/              # Admin namespace
│   │   └── users_controller.rb
│   ├── api/
│   │   └── v1/             # API versioning
│   │       └── articles_controller.rb
│   └── concerns/
├── models/
│   ├── concerns/
│   │   ├── authentication.rb
│   │   ├── publishable.rb
│   │   └── searchable.rb
│   └── [domain models]
├── services/
│   ├── articles/
│   │   ├── creator.rb
│   │   ├── publisher.rb
│   │   └── archiver.rb
│   └── users/
│       ├── registrar.rb
│       └── authenticator.rb
├── queries/
│   ├── articles/
│   │   └── search_query.rb
│   └── users/
│       └── active_query.rb
├── forms/
│   ├── registration_form.rb
│   └── checkout_form.rb
├── presenters/
│   ├── article_presenter.rb
│   └── user_presenter.rb
├── policies/
│   ├── article_policy.rb
│   └── application_policy.rb
└── validators/
    └── email_format_validator.rb
```

## Autoloading Custom Directories

```ruby
# config/application.rb
config.autoload_paths += %w[
  #{config.root}/app/services
  #{config.root}/app/queries
  #{config.root}/app/forms
  #{config.root}/app/presenters
  #{config.root}/app/policies
  #{config.root}/app/validators
]
```

## Module Namespacing

```ruby
# app/services/articles/creator.rb
module Articles
  class Creator
    def initialize(user, params)
      @user = user
      @params = params
    end

    def call
      # Create article logic
    end
  end
end

# Usage
Articles::Creator.new(current_user, article_params).call
```

## When to Use Each Pattern

| Pattern | Use When |
|---------|----------|
| **Concern** | Behavior is shared across multiple models |
| **Service** | Complex operation spanning multiple objects |
| **Query** | Complex database query used in multiple places |
| **Form** | Form handles multiple models or complex validation |
| **Presenter** | View needs formatted/computed data |
| **Policy** | Authorization logic is complex |

## Anti-Patterns to Avoid

### 1. Concern Abuse
```ruby
# BAD: Concern just to shrink the file
module UserMethods
  # Everything from User model dumped here
end

# GOOD: Concern for cohesive, reusable behavior
module Authenticatable
  # Only authentication-related code
end
```

### 2. Anemic Domain Models
```ruby
# BAD: Model is just data, logic in services
class Article < ApplicationRecord
  # Only associations and validations
end

# GOOD: Model has behavior
class Article < ApplicationRecord
  def publish!
    update!(status: "published", published_at: Time.current)
  end
end
```

### 3. Service Object Overuse
```ruby
# BAD: Simple operation in service
class Users::NameUpdater
  def call(user, name)
    user.update!(name: name)
  end
end

# GOOD: Just use the model
user.update!(name: params[:name])
```
