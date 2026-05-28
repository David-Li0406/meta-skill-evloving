---
name: "Service Object Patterns"
description: "Complete guide to implementing Service Objects in Ruby on Rails applications. Use when: (1) Creating business logic services, (2) Refactoring fat models/controllers, (3) Organizing service namespaces, (4) Handling service results, (5) Designing service interfaces. Trigger keywords: service objects, business logic, use cases, operations, command pattern, interactors, PORO, application services"
version: 1.1.0
---

# Service Object Patterns

Comprehensive guidance for implementing Service Objects in Rails applications.

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

---

## NEVER Do This

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
  task.update!(status: 'completed')
  create_invoice(task)  # If this fails, task is still completed
  notify_customer(task)
end

# RIGHT - All or nothing
def call
  ActiveRecord::Base.transaction do
    task.update!(status: 'completed')
    create_invoice(task)
    notify_customer(task)
  end
end
```

---

## Directory Structure

```
app/services/
├── application_service.rb          # Base class
├── tasks_manager/
│   ├── create_task.rb
│   ├── assign_carrier.rb
│   └── complete_task.rb
├── billing_manager/
│   ├── generate_invoice.rb
│   └── process_payment.rb
├── notifications_manager/
│   └── send_sms.rb
└── integrations/
    └── shipping/
        └── create_label.rb
```

**Naming Convention**: `{Domain}Manager::{Action}`

---

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

---

## Basic Service Pattern

```ruby
module TasksManager
  class CreateTask < ApplicationService
    def initialize(account:, merchant:, params:)
      @account = account
      @merchant = merchant
      @params = params
    end

    def call
      validate_params!

      ActiveRecord::Base.transaction do
        task = build_task
        task.save!
        schedule_notifications(task)
        task
      end
    end

    private

    attr_reader :account, :merchant, :params

    def validate_params!
      raise ArgumentError, "Recipient required" unless params[:recipient_id]
    end

    def build_task
      account.tasks.build(
        merchant: merchant,
        recipient_id: params[:recipient_id],
        status: 'pending'
      )
    end

    def schedule_notifications(task)
      TaskNotificationJob.perform_later(task.id)
    end
  end
end
```

---

## ServiceResult Pattern

```ruby
class ServiceResult
  attr_reader :data, :error, :errors

  def initialize(success:, data: nil, error: nil, errors: [])
    @success = success
    @data = data
    @error = error
    @errors = errors
  end

  def success? = @success
  def failure? = !@success

  def self.success(data = nil)
    new(success: true, data: data)
  end

  def self.failure(error = nil, errors: [])
    new(success: false, error: error, errors: errors)
  end
end
```

### Usage in Controller

```ruby
result = TasksManager::AssignCarrier.call(task: @task, carrier: @carrier)

if result.success?
  render json: result.data, status: :ok
else
  render json: { error: result.error, errors: result.errors }, status: :unprocessable_entity
end
```

---

## Service Interface Guidelines

| Aspect | Rule |
|--------|------|
| Entry point | Only `.call` is public |
| Dependencies | Pass via constructor |
| Return | ServiceResult or domain object |
| Side effects | Wrap in transactions |
| Validation | Fail fast with clear errors |
| External APIs | Handle timeouts, retries |

---

## Error Handling Strategy

| Error Type | Handling |
|------------|----------|
| Validation errors | Return ServiceResult.failure |
| Authorization | Raise custom AuthorizationError |
| External API | Retry with backoff, then failure |
| Database | Transaction rollback |
| Unexpected | Log, track, return generic failure |

---

## Service Checklist

Before creating a service:

```bash
# Check existing service structure
ls app/services/
ls app/services/*/ 2>/dev/null

# Review existing patterns
head -50 $(find app/services -name '*.rb' | head -1)

# Check naming conventions
grep -r 'class.*Manager' app/services/ --include='*.rb' | head -5

# Verify namespace exists
ls app/services/{namespace}/ 2>/dev/null
```

Before shipping:

- [ ] Only `.call` is public
- [ ] All side effects in transaction
- [ ] Returns ServiceResult (not raw errors)
- [ ] Dependencies injected via constructor
- [ ] Input validated at start
- [ ] Specs cover success and failure cases

---

## Quick Reference

| Pattern | Use Case |
|---------|----------|
| Basic Service | Single business operation |
| ServiceResult | Operations that can fail gracefully |
| Dry::Monads | Complex multi-step with pattern matching |
| Service Composition | Orchestrating multiple services |
| Retriable | External API calls |
| Circuit Breaker | Protect against cascading failures |

---

## References

Detailed patterns and examples in `references/`:
- `result-patterns.md` - ServiceResult, Dry::Monads, fluent API
- `error-handling.md` - Custom errors, retry, circuit breaker
- `instrumentation.md` - Logging, metrics, error tracking
- `testing.md` - RSpec patterns, shared examples, mocking
- `examples.md` - Complete service implementations
