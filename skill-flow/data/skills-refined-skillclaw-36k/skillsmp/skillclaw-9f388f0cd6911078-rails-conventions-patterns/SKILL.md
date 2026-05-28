---
name: rails-conventions-patterns
description: Use this skill when writing or refactoring Ruby on Rails code, making architectural decisions, or ensuring adherence to Rails conventions and best practices.
---

# Rails Conventions & Patterns Skill

This skill provides authoritative guidance on Ruby on Rails conventions, design patterns, and idiomatic code standards for production applications.

## When to Use This Skill

- Writing new Rails controllers, models, or services
- Refactoring existing Rails code
- Making decisions about code organization
- Choosing between different Rails patterns
- Ensuring code follows Rails conventions
- Reviewing Rails code for convention compliance

## Ruby & Rails Versions

```yaml
ruby: "3.2+ (prefer 3.3+ for YJIT benefits)"
rails: "7.1+ (prefer 8.0+ for new projects)"
```

## Rails Conventions Decision Tree

```
What are you building?
│
├─ Business logic spanning multiple models?
│   └─ Service Object (app/services/)
│
├─ Form spanning multiple models or complex validation?
│   └─ Form Object (app/forms/)
│
├─ Complex queries with multiple conditions?
│   └─ Query Object (app/queries/)
│
├─ View logic becoming complex?
│   └─ Decorator/Presenter (app/decorators/, app/presenters/)
│
├─ Truly shared behavior across 3+ unrelated models?
│   └─ Concern (app/models/concerns/)
│
└─ Simple single-model operation?
    └─ Keep in model/controller (no extra pattern)
```

## Best Practices

### NEVER Do This

**NEVER** use concerns for 1-2 models:
```ruby
# WRONG - Concern for single model
module UserHelpers
  def full_name
    "#{first_name} #{last_name}"
  end
end

# RIGHT - Keep in model if only used there
class User < ApplicationRecord
  def full_name
    "#{first_name} #{last_name}"
  end
end
```

**NEVER** put business logic in controllers:
```ruby
# WRONG - Fat controller
def create
  @order = Order.new(order_params)
  @order.calculate_tax
  @order.apply_discount(params[:coupon])
  @order.reserve_inventory
  PaymentGateway.charge(@order.total)
  @order.save
end

# RIGHT - Delegate to service
def create
  @order = CreateOrderService.call(current_user, order_params)
  redirect_to @order
end
```

**NEVER** use `unless` with `else`:
```ruby
# WRONG
unless user.admin?
  deny_access
else
  grant_access
end

# RIGHT
if user.admin?
  grant_access
else
  deny_access
end
```

**NEVER** exceed 4 parameters without keyword arguments:
```ruby
# WRONG
def create_user(email, password, name, role, department, manager_id)

# RIGHT - Use keyword arguments
def create_user(email:, password:, name:, role:, department:, manager_id:)

# RIGHT - Use parameter object for many params
def create_user(user_params)
```

**NEVER** monkey patch in application code:
```ruby
# WRONG - Monkey patching String
class String
  def
```