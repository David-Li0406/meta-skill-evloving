---
name: sidekiq-async-patterns
description: Use this skill when implementing background job processing with Sidekiq in Ruby on Rails, including creating jobs, configuring queues, handling retries, and optimizing performance.
---

# Sidekiq & Async Patterns Skill

This skill provides comprehensive guidance for implementing background jobs with Sidekiq in Rails applications.

## When to Use This Skill

- Creating new background jobs
- Configuring Sidekiq queues
- Implementing retry strategies
- Designing idempotent operations
- Setting up scheduled jobs
- Handling job failures
- Optimizing async processing

## External Documentation

**Official Wiki**: [Sidekiq Wiki](https://github.com/sidekiq/sidekiq/wiki)

```bash
# Always check the official wiki for latest patterns
# Key wiki pages:
# - Best Practices: https://github.com/sidekiq/sidekiq/wiki/Best-Practices
# - Error Handling: https://github.com/sidekiq/sidekiq/wiki/Error-Handling
# - Scheduled Jobs: https://github.com/sidekiq/sidekiq/wiki/Scheduled-Jobs
```

## Pre-Work Inspection

```bash
# Check existing jobs
ls app/jobs/ app/sidekiq/ app/workers/ 2>/dev/null

# Check job naming conventions
head -30 $(find app/jobs -name '*.rb' | head -1) 2>/dev/null

# Check Sidekiq configuration
cat config/sidekiq.yml 2>/dev/null
cat config/initializers/sidekiq.rb 2>/dev/null

# Check queue configuration
grep -r 'queue_as\|sidekiq_options' app/jobs/ --include='*.rb' | head -10

# Check scheduled jobs
cat config/schedule.yml 2>/dev/null
cat config/recurring.yml 2>/dev/null
```

## Core Principles

### 1. Idempotency (CRITICAL)

**Jobs MUST be idempotent** - running the same job multiple times produces the same result.

```ruby
# WRONG - Not idempotent (sends duplicate emails)
class SendWelcomeEmailJob < ApplicationJob
  def perform(user_id)
    user = User.find(user_id)
    UserMailer.welcome(user).deliver_now
  end
end

# CORRECT - Idempotent (checks before sending)
class SendWelcomeEmailJob < ApplicationJob
  def perform(user_id)
    user = User.find(user_id)
    return if user.welcome_email_sent_at.present?
    
    UserMailer.welcome(user).deliver_now
    user.update!(welcome_email_sent_at: Time.current)
  end
end
```

### 2. Small Payloads

**Pass IDs, not objects** - objects serialize and can become stale.

```ruby
# WRONG - Object serialization
NotificationJob.perform_later(@user)  # Serializes entire user object

# CORRECT - Pass ID
NotificationJob.perform_later(@user.id)
```

### 3. Fail Fast

**Find records early** - fail immediately if data doesn't exist.

```ruby
class ProcessTaskJob < ApplicationJob
  def perform(task_id)
    task = Task.find(task_id)  # Raises if not found
    # ... process task
  end
end
```

## Job Structure Template

```ruby
# app/jobs/task_notification_job.rb
class TaskNotificationJob < ApplicationJob
  queue_as :notifications
  
  # Retry configuration
  retry_on ActiveRecord::RecordNotFound, wait: 5.seconds, attempts: 3
  retry_on Net::OpenTimeout, wait: :polynomially_longer, attempts: 5
  discard_on ActiveJob::DeserializationError

  def perform(task_id, notification_type = :created)
    task = Task.find(task_id)
    
    case notification_type.to_sym
    when :created
      send_creation_notification(task)
    when :completed
      send_completion_notification(task)
    end
  end

  private

  def send_creation_notification(task)
    return unless task.recipient.phone.present?
    return if task.notification_sent_at.present?  # Idempotency check
    
    SmsService.send(
      to: task.recipient.phone,
      message: I18n.t('sms.task_created', tracking: task.tracking_number)
    )
    
    task.update!(notification_sent_at: Time.current)
  end

  def send_completion_notification(task)
    # Implementation
  end
end
```

## Sidekiq Configuration

### config/sidekiq.yml

```yaml
---
:concurrency: <%= ENV.fetch('SIDEKIQ_CONCURRENCY', 10) %>
:timeout: 25
:max_retries: 5

:queues:
  - [critical, 6]      # Highest priority
  - [default, 5]
  - [notifications, 4]
  - [integrations, 3]  # External API calls
  - [bulk, 2]          # Batch processing
  - [scheduled, 1]
  - [low, 1]           # Lowest priority

production:
  :concurrency: 20

development:
  :concurrency: 5
```

### config/initializers/sidekiq.rb

```ruby
Sidekiq.configure_server do |config|
  config.redis = {
    url: ENV.fetch('REDIS_URL', 'redis://localhost:6379/0'),
    network_timeout: 5,
    pool_timeout: 5
  }

  # Death handler - job exhausted all retries
  config.death_handlers << ->(job, ex) do
    Rails.logger.error("Job #{job['class']} died: #{ex.message}")
    Sentry.capture_exception(ex, extra: { job: job })
  end
end

Sidekiq.configure_client do |config|
  config.redis = {
    url: ENV.fetch('REDIS_URL', 'redis://localhost:6379/0'),
    network_timeout: 5,
    pool_timeout: 5
  }
end

# Recommended: strict argument mode
Sidekiq.strict_args!
```

## Queue Strategy

### Priority Guidelines

| Queue | Priority | Use For |
|-------|----------|---------|
| `critical` | 6 | Payment processing, time-sensitive operations |
| `default` | 5 | Standard operations |
| `notifications` | 4 | User notifications (SMS, email, push) |
| `integrations` | 3 | External API calls (may be slow) |
| `bulk` | 2 | Batch processing, imports |
| `scheduled` | 1 | Scheduled/recurring tasks |
| `low` | 1 | Non-urgent, can wait |

### Setting Queue in Jobs

```ruby
class PaymentProcessingJob < ApplicationJob
  queue_as :critical
  
  def perform(payment_id)
    # Critical payment processing
  end
end

class SendNewsletterJob < ApplicationJob
  queue_as :low
  
  def perform(user_ids)
    # Low priority newsletter
  end
end

# Dynamic queue selection
class FlexibleJob < ApplicationJob
  queue_as do
    if self.arguments.first.priority == 'high'
      :critical
    else
      :default
    end
  end
end
```

## Retry Strategies

### Built-in Retry Configuration

```ruby
class ExternalApiJob < ApplicationJob
  # Retry specific exceptions
  retry_on Net::OpenTimeout, wait: 5.seconds, attempts: 3
  retry_on Faraday::TimeoutError, wait: :polynomially_longer, attempts: 5
  
  # Exponential backoff: 3s, 18s, 83s, 258s, 627s
  retry_on ApiRateLimitError, wait: :polynomially_longer, attempts: 5
  
  # Custom wait calculation
  retry_on CustomError, wait: ->(executions) { executions * 10.seconds }
  
  # Don't retry these - discard instead
  discard_on ActiveJob::DeserializationError
  discard_on UnrecoverableError
  
  def perform(task_id)
    # Implementation
  end
end
```

### Manual Retry Control

```ruby
class ManualRetryJob < ApplicationJob
  def perform(task_id)
    task = Task.find(task_id)
    
    begin
      external_service.process(task)
    rescue RateLimitError => e
      # Re-enqueue with delay
      self.class.set(wait: 1.minute).perform_later(task_id)
    rescue PermanentError => e
      # Don't retry, log and notify
      Rails.logger.error("Permanent failure: #{e.message}")
      Sentry.capture_exception(e)
    end
  end
end
```

## Common Job Patterns

### Batch Processing

```ruby
class BulkUpdateJob < ApplicationJob
  queue_as :bulk

  def perform(record_ids, attributes)
    Model.where(id: record_ids).find_each(batch_size: 100) do |record|
      record.update!(attributes)
    rescue ActiveRecord::RecordInvalid => e
      Rails.logger.error("Failed to update #{record.id}: #{e.message}")
      # Continue with next record
    end
  end
end
```

### Progress Tracking

```ruby
class ImportJob < ApplicationJob
  queue_as :bulk

  def perform(import_id)
    import = Import.find(import_id)
    import.update!(status: 'processing', started_at: Time.current)

    total = import.rows.count
    processed = 0
    errors = []

    import.rows.each do |row|
      begin
        process_row(row, import)
        processed += 1
      rescue StandardError => e
        errors << { row: row[:number], error: e.message }
      end

      # Update progress every 10 rows
      if processed % 10 == 0
        import.update!(
          progress: (processed.to_f / total * 100).round(1),
          processed_count: processed
        )
      end
    end

    import.update!(
      status: errors.empty? ? 'completed' : 'completed_with_errors',
      completed_at: Time.current,
      error_details: errors
    )
  end
end
```

### External API Calls

```ruby
class SyncExternalDataJob < ApplicationJob
  queue_as :integrations

  retry_on Faraday::TimeoutError, wait: 1.minute, attempts: 3
  retry_on Faraday::ConnectionFailed, wait: 5.minutes, attempts: 3
  discard_on ExternalApi::ClientError  # 4xx errors - don't retry

  def perform(resource_id)
    resource = Resource.find(resource_id)
    
    data = ExternalApi.fetch(resource.external_id)
    
    resource.update!(
      external_data: data,
      synced_at: Time.current
    )
  end
end
```

### Scheduled Jobs (with sidekiq-scheduler)

```yaml
# config/recurring.yml
daily_cleanup:
  cron: '0 2 * * *'  # 2 AM daily
  class: DailyCleanupJob
  queue: scheduled

hourly_sync:
  cron: '0 * * * *'  # Every hour
  class: HourlySyncJob
  queue: integrations

weekly_report:
  cron: '0 9 * * 1'  # Monday 9 AM
  class: WeeklyReportJob
  queue: low
```

### Unique Jobs (with sidekiq-unique-jobs)

```ruby
class UniqueProcessingJob < ApplicationJob
  queue_as :default

  # Prevent duplicate jobs for same arguments
  sidekiq_options lock: :until_executed,
                  lock_args_method: :lock_args

  def self.lock_args(args)
    [args[0]]  # Lock on first argument only
  end

  def perform(resource_id, options = {})
    # Only one job per resource_id at a time
  end
end
```

## Error Handling

### Comprehensive Error Wrapper

```ruby
# app/jobs/concerns/error_handling.rb
module ErrorHandling
  extend ActiveSupport::Concern

  included do
    around_perform :with_error_handling
  end

  private

  def with_error_handling
    yield
  rescue ActiveRecord::RecordNotFound => e
    # Log but don't re-raise (job completes)
    Rails.logger.warn("#{self.class.name}: Record not found - #{e.message}")
  rescue StandardError => e
    # Log, notify, and re-raise (triggers retry)
    Rails.logger.error("#{self.class.name} failed: #{e.message}")
    Sentry.capture_exception(e, extra: { job_args: arguments })
    raise
  end
end

# Usage
class MyJob < ApplicationJob
  include ErrorHandling
  
  def perform(task_id)
    # Implementation
  end
end
```

## Testing Jobs

```ruby
# spec/jobs/task_notification_job_spec.rb
require 'rails_helper'

RSpec.describe TaskNotificationJob, type: :job do
  include ActiveJob::TestHelper

  let(:task) { create(:task) }

  describe '#perform' do
    it 'sends notification' do
      expect(SmsService).to receive(:send).with(
        to: task.recipient.phone,
        message: include(task.tracking_number)
      )

      described_class.perform_now(task.id)
    end

    it 'is idempotent' do
      allow(SmsService).to receive(:send)
      
      # First call
      described_class.perform_now(task.id)
      
      # Second call should not send again
      expect(SmsService).not_to receive(:send)
      described_class.perform_now(task.id)
    end

    context 'when task not found' do
      it 'raises error' do
        expect {
          described_class.perform_now(0)
        }.to raise_error(ActiveRecord::RecordNotFound)
      end
    end
  end

  describe 'queueing' do
    it 'queues on correct queue' do
      expect {
        described_class.perform_later(task.id)
      }.to have_enqueued_job.on_queue('notifications')
    end
  end
end
```

## Monitoring & Debugging

### Sidekiq Web UI

```ruby
# config/routes.rb
require 'sidekiq/web'

Rails.application.routes.draw do
  # Protect with authentication
  authenticate :user, ->(u) { u.admin? } do
    mount Sidekiq::Web => '/sidekiq'
  end
end
```

### Useful Commands

```bash
# Check queue sizes
redis-cli LLEN queue:default
redis-cli LLEN queue:critical

# Monitor Sidekiq processes
bundle exec sidekiq -q critical -q default

# Clear all queues (DANGEROUS)
redis-cli FLUSHDB

# Check scheduled jobs
redis-cli ZRANGE schedule 0 -1
```

## Anti-Patterns to Avoid

### ❌ Non-Idempotent Jobs

```ruby
# WRONG
def perform(user_id)
  User.find(user_id).increment!(:login_count)
end
```

### ❌ Large Payloads

```ruby
# WRONG
def perform(user_data)  # Passing full hash
  User.create!(user_data)
end

# CORRECT
def perform(user_id)
  user = User.find(user_id)
  # Process user
end
```

### ❌ Long-Running Jobs

```ruby
# WRONG - Job runs for hours
def perform
  User.all.each { |u| process(u) }
end

# CORRECT - Batch into smaller jobs
def perform(user_ids)
  User.where(id: user_ids).find_each { |u| process(u) }
end
```

### ❌ No Error Handling

```ruby
# WRONG
def perform(task_id)
  external_api.call(task_id)  # May fail silently
end

# CORRECT
def perform(task_id)
  result = external_api.call(task_id)
  raise "API failed: #{result.error}" unless result.success?
end
```

## Sidekiq 7.x Modern Features

### Capsules (Sidekiq 7.2+)
```ruby
# config/initializers/sidekiq.rb
Sidekiq.configure_server do |config|
  # Define separate thread pools for different workloads
  config.capsule("default") do |cap|
    cap.concurrency = 5
    cap.queues = %w[default low]
  end

  config.capsule("