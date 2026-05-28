---
name: service-object-patterns
description: Use this skill when implementing Service Objects in Ruby on Rails applications to manage business logic, refactor models/controllers, and design service interfaces.
---

# Service Object Patterns Skill

This skill provides comprehensive guidance for implementing Service Objects in Rails applications following consistent patterns and conventions.

## When to Use This Skill

- Creating new service objects for business logic
- Refactoring fat models or controllers
- Designing service interfaces
- Implementing result objects for service responses
- Organizing services into namespaces

## Service Decision Tree

```
Where should this logic go?
│
├─ Business logic spanning multiple models?
│   └─ Service Object (app/services/)
│
├─ Operation has multiple steps/side effects?
│   └─ Service Object (with transaction)
│
├─ Need to orchestrate external services?
│   └─ Service Object (with error handling)
│
├─ Complex validation or business rules?
│   └─ Service Object (or Form Object for forms)
│
├─ Simple single-model CRUD?
│   └─ Keep in model/controller
│
└─ Single-line delegation?
    └─ Keep in controller
```

## Naming Convention

```ruby
# Pattern: {Domain}Manager::{Action} or {Domain}Manager::{SubDomain}::{Action}

# Examples:
TasksManager::CreateTask
TasksManager::Bundling::BundleTasks
BillingManager::GenerateInvoice
IntegrationsManager::Salla::SyncOrders
```

## Base Service Class

```ruby
# app/services/application_service.rb
class ApplicationService
  def self.call(...)
    new(...).call
  end

  private

  attr_reader :params

  def initialize(**params)
    @params = params
  end
end
```

## Basic Service Pattern

```ruby
# app/services/tasks_manager/create_task.rb
module TasksManager
  class CreateTask < ApplicationService
    def initialize(account:, merchant:, params:)
      @account = account
      @merchant = merchant
      @params = params
    end

    def call
      # Implementation of task creation logic
    end
  end
end
```

## Best Practices

### NEVER Do This

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
  @order = OrdersManager::CreateOrder.call(user: current_user, params: order_params)
  redirect_to @order
end
```

**NEVER** return raw ActiveRecord errors from services:
```ruby
# WRONG - Leaking implementation details
def call
  task.save!
rescue ActiveRecord::RecordInvalid => e
  raise e  # Caller must understand AR errors
end

# RIGHT - Wrap in ServiceResult
def call
  task.save!
  ServiceResult.success(task)
rescue ActiveRecord::RecordInvalid => e
  ServiceResult.failure(e.message, errors: task.errors.full_messages)
end
```

**NEVER** make service methods public except `call`:
```ruby
# WRONG - Exposing internals
class MyService
  def call; end
  def validate_params; end  # Public - shouldn't be
  def process; end          # Public - shouldn't be
end

# RIGHT - Only .call is public
class MyService
  def self.call(...) = new(...).call
  def call; end

  private

  def validate_params; end
  def process; end
end
```

**NEVER** skip transactions for multi-step operations:
```ruby
# WRONG - Partial updates on failure
def call
  task.update
```