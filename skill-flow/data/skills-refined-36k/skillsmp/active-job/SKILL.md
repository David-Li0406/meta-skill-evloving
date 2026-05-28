---
name: active-job
description: This skill should be used when the user asks about "background jobs", "Active Job", "perform_later", "perform_now", "queue adapters", "job retries", "job callbacks", "async tasks", "scheduled jobs", "job queues", or needs guidance on background processing in Rails applications.
version: 1.0.0
---

# Active Job

Comprehensive guide to background job processing in Rails with Active Job.

## Creating Jobs

```bash
rails generate job ProcessOrder
```

```ruby
# app/jobs/process_order_job.rb
class ProcessOrderJob < ApplicationJob
  queue_as :default

  def perform(order)
    # Process the order
    order.process!
    OrderMailer.confirmation(order).deliver_now
  end
end
```

## Enqueueing Jobs

### Immediate Enqueue

```ruby
# Enqueue to run as soon as possible
ProcessOrderJob.perform_later(order)

# Enqueue multiple jobs at once
ActiveJob.perform_all_later(
  ProcessOrderJob.new(order1),
  ProcessOrderJob.new(order2)
)
```

### Scheduled Execution

```ruby
# Run at specific time
ProcessOrderJob.set(wait_until: Date.tomorrow.noon).perform_later(order)

# Run after delay
ProcessOrderJob.set(wait: 1.hour).perform_later(order)
ProcessOrderJob.set(wait: 5.minutes).perform_later(order)

# Run immediately (blocking, no queue)
ProcessOrderJob.perform_now(order)
```

### Queue Selection

```ruby
class ProcessOrderJob < ApplicationJob
  queue_as :high_priority
end

# Or dynamically
ProcessOrderJob.set(queue: :urgent).perform_later(order)
```

### Priority

```ruby
class LowPriorityJob < ApplicationJob
  queue_as :default
  queue_with_priority 50  # Higher number = lower priority
end

# Dynamic priority
ImportantJob.set(priority: 10).perform_later(data)
```

## Queue Adapters

### Configuration

```ruby
# config/application.rb or config/environments/*.rb
config.active_job.queue_adapter = :async
```

### Common Adapters

| Adapter | Best For | Notes |
|---------|----------|-------|
| `:async` | Development | In-process, not for production |
| `:inline` | Testing | Runs immediately |
| `:test` | Testing | Stores jobs for assertions |

## Retries and Error Handling

### Automatic Retries

```ruby
class ExternalApiJob < ApplicationJob
  retry_on Net::OpenTimeout, wait: :polynomially_longer, attempts: 5
  retry_on CustomTransientError, wait: 5.seconds, attempts: 3

  def perform(record)
    ExternalApi.sync(record)
  end
end
```

### Retry Options

| Option | Description |
|--------|-------------|
| `wait` | Seconds to wait (`:polynomially_longer` for backoff) |
| `attempts` | Number of retry attempts |
| `queue` | Queue for retried job |
| `priority` | Priority for retried job |

### Discard on Error

```ruby
class DataImportJob < ApplicationJob
  discard_on ActiveJob::DeserializationError
  discard_on CustomPermanentError

  def perform(record_id)
    record = Record.find(record_id)
    # ...
  end
end
```

### Custom Error Handling

```ruby
class ProcessOrderJob < ApplicationJob
  rescue_from(PaymentError) do |exception|
    order = arguments.first
    order.mark_payment_failed!(exception.message)
    OrderMailer.payment_failed(order).deliver_later
  end

  def perform(order)
    PaymentService.charge(order)
  end
end
```

## Callbacks

```ruby
class ImportJob < ApplicationJob
  before_enqueue :log_enqueue
  after_enqueue :notify_enqueued

  before_perform :setup
  around_perform :measure_time
  after_perform :cleanup

  after_discard :log_discard

  private

  def log_enqueue
    Rails.logger.info "Enqueueing import job"
  end

  def setup
    @start_time = Time.current
  end

  def measure_time
    start = Time.current
    yield
    duration = Time.current - start
    Rails.logger.info "Job completed in #{duration}s"
  end

  def cleanup
    # Clean up resources
  end

  def log_discard(job, exception)
    Rails.logger.error "Job discarded: #{exception.message}"
  end
end
```

## Job Arguments

### Supported Types

Active Job automatically serializes:
- Basic types (String, Integer, Float, NilClass, TrueClass, FalseClass, BigDecimal)
- Symbol (as String)
- Date, Time, DateTime
- ActiveSupport::TimeWithZone
- ActiveSupport::Duration
- Hash (keys as strings)
- ActiveSupport::HashWithIndifferentAccess
- Array
- Range
- Module/Class
- ActiveRecord objects (via GlobalID)

### GlobalID Serialization

```ruby
# ActiveRecord models are serialized via GlobalID
class NotifyUserJob < ApplicationJob
  def perform(user)
    # user is automatically deserialized from GlobalID
    UserNotifier.send_notification(user)
  end
end

NotifyUserJob.perform_later(User.find(1))
# Serialized as: "gid://myapp/User/1"
```

### Custom Serializers

```ruby
# app/serializers/money_serializer.rb
class MoneySerializer < ActiveJob::Serializers::ObjectSerializer
  def serialize(money)
    super("amount" => money.amount, "currency" => money.currency)
  end

  def deserialize(hash)
    Money.new(hash["amount"], hash["currency"])
  end

  private

  def klass
    Money
  end
end

# config/initializers/active_job.rb
Rails.application.config.active_job.custom_serializers << MoneySerializer
```

## Mailer Integration

```ruby
# Async email delivery
UserMailer.welcome(user).deliver_later
UserMailer.welcome(user).deliver_later(wait: 1.hour)
UserMailer.welcome(user).deliver_later(wait_until: Date.tomorrow.noon)

# Sync delivery (use in jobs)
UserMailer.welcome(user).deliver_now
```

## Testing Jobs

### Test Helper Methods

```ruby
# test/jobs/process_order_job_test.rb
require "test_helper"

class ProcessOrderJobTest < ActiveJob::TestCase
  test "processes the order" do
    order = orders(:pending)

    ProcessOrderJob.perform_now(order)

    assert order.reload.processed?
  end

  test "enqueues job" do
    order = orders(:pending)

    assert_enqueued_with(job: ProcessOrderJob, args: [order]) do
      ProcessOrderJob.perform_later(order)
    end
  end

  test "sends confirmation email" do
    order = orders(:pending)

    assert_enqueued_emails 1 do
      ProcessOrderJob.perform_now(order)
    end
  end
end
```

## Best Practices

1. **Keep jobs idempotent** - Safe to run multiple times
2. **Use small arguments** - Pass IDs, not large objects
3. **Handle missing records** - Records may be deleted before job runs
4. **Set appropriate queues** - Separate critical from low-priority work
5. **Monitor failed jobs** - Use adapter's UI or custom monitoring
6. **Test with `perform_now`** - Test job logic synchronously
