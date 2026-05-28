---
name: rails-conventions-patterns
description: Use this skill when writing or reviewing Ruby on Rails code, including controllers, models, services, and making architectural decisions about code organization and best practices.
---

# Rails Conventions & Patterns

This skill provides comprehensive guidance on Ruby on Rails conventions, design patterns, and idiomatic code standards for production applications.

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

## Rails 7.x/8.x Modern Features

### Rails 7.1+ Features
```ruby
# Composite Primary Keys
class BookOrder < ApplicationRecord
  self.primary_key = [:shop_id, :id]
  belongs_to :shop
  has_many :line_items, foreign_key: [:shop_id, :order_id]
end

# ActiveRecord::Encryption (sensitive data)
class User < ApplicationRecord
  encrypts :email, deterministic: true
  encrypts :ssn, :credit_card
end

# Horizontal Sharding
class ApplicationRecord < ActiveRecord::Base
  connects_to shards: {
    default: { writing: :primary, reading: :primary_replica },
    shard_two: { writing: :primary_shard_two }
  }
end

# Async Query Loading
posts = Post.where(published: true).load_async
# Do other work
posts.to_a # Wait for results

# Normalize values before validation
class User < ApplicationRecord
  normalizes :email, with: -> { _1.strip.downcase }
  normalizes :phone, with: -> { _1.gsub(/\D/, '') }
end
```

### Rails 8.0+ Features
```ruby
# Improved Solid Queue (built-in job backend)
# config/application.rb
config.active_job.queue_adapter = :solid_queue

# Solid Cache (built-in caching)
# config/application.rb
config.cache_store = :solid_cache_store

# Authentication generator
rails generate authentication

# Built-in rate limiting
class Api::PostsController < Api::BaseController
  rate_limit to: 10, within: 1.minute, only: :create
end

# Per-environment credentials
rails credentials:edit --environment production
```

### Modern Ruby 3.3+ Features
```ruby
# Pattern matching in case expressions
case user
in { role: "admin", active: true }
  grant_full_access
in { role: "user", active: true }
  grant_standard_access
else
  deny_access
end

# Endless method definitions (one-liners)
def full_name = "#{first_name} #{last_name}"
def published? = published_at.present?

# Data class (immutable value objects, Ruby 3.2+)
User = Data.define(:id, :name, :email)
user = User.new(id: 1, name: "Alice", email: "alice@example.com")

# YJIT optimization (Ruby 3.3+)
# config/application.rb
if defined?(RubyVM::YJIT.enable)
  RubyVM::YJIT.enable
end
```

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

## Naming Conventions

```yaml
classes: "PascalCase"         # UserProfile, OrderService
methods: "snake_case"         # create_order, find_by_email
predicates: "end with ?"      # active?, valid?, admin?
dangerous_methods: "end with !" # save!, destroy!, update!
constants: "SCREAMING_SNAKE"  # MAX_RETRIES, DEFAULT_LIMIT
private_methods: "descriptive" # NOT underscore prefix
```

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

## Code Quality Checklist

Before shipping any code:

- [ ] Methods ≤ 15 lines
- [ ] Max 4 parameters (use keyword args)
- [ ] No business logic in controllers
- [ ] No view logic in models
- [ ] Concerns used by 3+ models
- [ ] Guard clauses used
- [ ] Tests exist for new code

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

## References

Detailed patterns and examples in `references/`:
- `controllers.md` - RESTful, API, Hotwire, nested resource controllers
- `design-patterns.md` - Form objects, decorators, presenters, repositories, DTOs
- `background-jobs-mailers.md` - ActiveJob, Sidekiq, mailers, Action Cable
- `modern-rails.md` - Rails 7.1+/8.0+ features, Ruby 3.3+, concerns, visibility