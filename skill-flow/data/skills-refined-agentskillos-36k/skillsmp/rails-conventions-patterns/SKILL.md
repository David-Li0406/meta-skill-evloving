---
name: "Rails Conventions & Patterns"
description: "Ruby on Rails conventions, design patterns, and idiomatic code standards. Use when: (1) Writing controllers/models/services, (2) Choosing patterns (Service, Form, Query objects), (3) Making architectural decisions, (4) Reviewing code for conventions. Trigger keywords: rails conventions, design patterns, idiomatic code, best practices, code organization, naming conventions, MVC patterns"
version: 1.1.0
---

# Rails Conventions & Patterns

Authoritative guidance on Ruby on Rails conventions and design patterns.

## Pattern Decision Tree

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

---

## NEVER Do This

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
  def to_slug
    downcase.gsub(' ', '-')
  end
end

# RIGHT - Create utility method
module StringUtils
  def self.slugify(text)
    text.downcase.gsub(' ', '-')
  end
end
```

---

## File Organization Standards

| Type | Location | Max Lines | Purpose |
|------|----------|-----------|---------|
| Models | app/models/ | 200 | Associations, validations, scopes |
| Controllers | app/controllers/ | 100 | REST actions, request handling |
| Services | app/services/ | 150 | Business logic, orchestration |
| Forms | app/forms/ | 100 | Multi-model forms, complex validation |
| Queries | app/queries/ | 100 | Complex reusable queries |
| Presenters | app/presenters/ | 100 | View-specific logic |
| Jobs | app/jobs/ | 50 | Background processing |
| Mailers | app/mailers/ | 50 | Email generation |

---

## Naming Conventions

```yaml
classes: "PascalCase"         # UserProfile, OrderService
methods: "snake_case"         # create_order, find_by_email
predicates: "end with ?"      # active?, valid?, admin?
dangerous_methods: "end with !" # save!, destroy!, update!
constants: "SCREAMING_SNAKE"  # MAX_RETRIES, DEFAULT_LIMIT
private_methods: "descriptive" # NOT underscore prefix
```

---

## Ruby Idioms

### Prefer

| Pattern | Example |
|---------|---------|
| Guard clauses | `return unless user.active?` |
| Safe navigation | `user&.profile&.avatar` |
| Keyword arguments (2+ params) | `def call(user:, params:)` |
| `Struct`/`Data` for value objects | `User = Data.define(:id, :name)` |
| `frozen_string_literal: true` | At top of every file |
| Explicit returns for clarity | `return Result.failure(errors)` |

### Avoid

| Anti-Pattern | Why |
|--------------|-----|
| `unless` with `else` | Confusing logic |
| Nested ternaries | Hard to read |
| `and`/`or` for control flow | Unexpected precedence |
| Monkey patching | Maintenance nightmare |
| More than 15 lines/method | Single responsibility |

---

## Service Object Template

```ruby
class CreateOrderService
  def initialize(user:, params:)
    @user = user
    @params = params
  end

  def call
    validate_params
    order = build_order
    process_payment
    send_confirmation
    Result.success(order)
  rescue PaymentError => e
    Result.failure(e.message)
  end

  private

  attr_reader :user, :params

  def validate_params
    # ...
  end

  def build_order
    # ...
  end
end
```

---

## Implementation Order

Always implement bottom-up (dependencies first):

```
1. Database migrations
2. Models (foundation)
3. Services (business logic)
4. Components (presentation wrappers)
5. Controllers (orchestration)
6. Views (final layer)
7. Tests (verify everything)
```

---

## Code Quality Checklist

Before shipping any code:

- [ ] Methods ≤ 15 lines
- [ ] Max 4 parameters (use keyword args)
- [ ] No business logic in controllers
- [ ] No view logic in models
- [ ] Concerns used by 3+ models
- [ ] Guard clauses used
- [ ] Tests exist for new code

---

## Quick Reference

**Before Writing Any Code:**
```bash
# Check existing patterns
ls app/services/
ls app/forms/ 2>/dev/null

# Check naming conventions
head -30 $(find app/services -name '*.rb' | head -1)

# Check dependencies
grep -v '^#' Gemfile | grep -v '^$'
```

---

## References

Detailed patterns and examples in `references/`:
- `controllers.md` - RESTful, API, Hotwire, nested resource controllers
- `design-patterns.md` - Form objects, decorators, presenters, repositories, DTOs
- `background-jobs-mailers.md` - ActiveJob, Sidekiq, mailers, Action Cable
- `modern-rails.md` - Rails 7.1+/8.0+ features, Ruby 3.3+, concerns, visibility
