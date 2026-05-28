# Background Job Patterns

Detailed patterns for ActiveJob and Sidekiq in Rails applications.

## Job Structure

### The `_later`/`_now` Convention (37signals Pattern)

**Applicability**: Always applicable - this is a naming convention and architecture pattern

Define both `_later` (queues job) and the synchronous method on the model. Jobs become shallow wrappers that delegate to the model.

```ruby
# Model defines both versions
class Webhook::Delivery < ApplicationRecord
  after_create_commit :deliver_later

  # Asynchronous version - queues the job
  def deliver_later
    Webhook::DeliveryJob.perform_later(self)
  end

  # Synchronous version - does the actual work
  def deliver
    in_progress!
    self.response = perform_request
    completed!
  rescue => e
    failed!(e.message)
  end

  private

  def perform_request
    HTTP.post(webhook.url, json: payload)
  end
end

# Job is now a shallow wrapper
class Webhook::DeliveryJob < ApplicationJob
  queue_as :webhooks

  def perform(delivery)
    delivery.deliver  # Just calls the model method
  end
end
```

**Benefits**:
- Business logic lives in the model (testable, reusable)
- Jobs are thin and focused on infrastructure concerns
- Clear naming convention for async operations
- Easy to call synchronously in tests or console

### Shallow Jobs Delegating to Models (37signals Pattern)

**Applicability**:
- **Use now**: For new jobs you're creating
- **Future direction**: For refactoring existing fat jobs

Keep jobs simple - they handle queuing, retries, and error reporting. Business logic belongs in models or service objects.

```ruby
# ✅ PREFERRED: Shallow job
class Notification::Bundle::DeliverJob < ApplicationJob
  include SmtpDeliveryErrorHandling
  queue_as :backend

  def perform(bundle)
    bundle.deliver  # All logic in the model
  end
end

# Model contains the business logic
class Notification::Bundle < ApplicationRecord
  def deliver
    return if delivered?

    recipients.each do |recipient|
      NotificationMailer.bundle(self, recipient).deliver_now
    end

    update!(delivered_at: Time.current)
  end
end

# ❌ AVOID: Fat job with business logic
class NotificationDeliverJob < ApplicationJob
  def perform(notification)
    user = notification.user
    if user.email_verified?
      NotificationMailer.deliver(notification).deliver_now
      notification.update!(delivered_at: Time.current)
    end
  end
end
```

### Basic Job with Error Handling

```ruby
class ProcessOrderJob < ApplicationJob
  queue_as :default

  # Retry on transient errors
  retry_on ActiveRecord::RecordNotFound, wait: 5.seconds, attempts: 3
  retry_on Net::OpenTimeout, wait: :exponentially_longer, attempts: 5
  retry_on Timeout::Error, wait: 1.minute, attempts: 3

  # Don't retry on permanent failures
  discard_on ActiveJob::DeserializationError do |job, error|
    Rails.logger.error "Failed to deserialize job #{job.job_id}: #{error.message}"
  end

  def perform(order_id)
    order = Order.find(order_id)

    OrderProcessor.new(order).process!
    OrderMailer.confirmation(order).deliver_later
  rescue StandardError => e
    Rails.logger.error "Failed to process order #{order_id}: #{e.message}"
    raise  # Re-raise to trigger retry
  end
end
```

### Dynamic Queue Selection

```ruby
class NotificationJob < ApplicationJob
  queue_as do
    user = arguments.first
    user.premium? ? :high_priority : :default
  end

  def perform(user, message)
    NotificationService.new(user).send(message)
  end
end
```

## Idempotency Patterns

### Status Check Guard

```ruby
class ProcessPaymentJob < ApplicationJob
  def perform(payment_id)
    payment = Payment.find(payment_id)

    # Guard: already processed
    return if payment.completed?

    process_payment(payment)
  end
end
```

### Lock-Based Idempotency

```ruby
class ImportDataJob < ApplicationJob
  def perform(import_id)
    import = Import.find(import_id)

    import.with_lock do
      return if import.completed?

      process_import(import)
      import.update!(status: 'completed', completed_at: Time.current)
    end
  end
end
```

### Unique Job Keys (with Sidekiq Enterprise or sidekiq-unique-jobs)

```ruby
class SyncUserJob < ApplicationJob
  # Ensure only one job per user runs at a time
  sidekiq_options lock: :until_executed,
                  lock_args_method: ->(args) { [args.first] }

  def perform(user_id)
    UserSyncService.new(user_id).sync!
  end
end
```

## Concurrency Control

**Context Awareness**: Choose the appropriate approach based on your job adapter.

### Solid Queue (Built-in Concurrency Limits)

**Detection**: Check if `config.active_job.queue_adapter = :solid_queue` or Solid Queue gem is present

```ruby
class Storage::MaterializeJob < ApplicationJob
  queue_as :backend

  # Limit to 1 concurrent job per owner
  # The key lambda determines what to group by
  limits_concurrency to: 1, key: ->(owner) { owner }

  discard_on ActiveJob::DeserializationError

  def perform(owner)
    owner.materialize_storage
  end
end

# Multiple jobs for the same owner will queue, not run concurrently
# Jobs for different owners can run in parallel
```

**Use cases**:
- Prevent race conditions on shared resources
- Limit API rate limits per account
- Control database load per tenant

### Sidekiq with sidekiq-unique-jobs Gem

**Detection**: Check for `sidekiq-unique-jobs` in Gemfile

```ruby
class SyncUserJob < ApplicationJob
  # Lock until job execution completes
  sidekiq_options lock: :until_executed,
                  lock_args_method: ->(args) { [args.first] }

  def perform(user_id)
    UserSyncService.new(user_id).sync!
  end
end

# Alternative: Lock while job is in queue
class ImportJob < ApplicationJob
  sidekiq_options lock: :until_executing,
                  lock_args_method: ->(args) { [args.first, args.second] }

  def perform(account_id, import_type)
    ImportService.new(account_id, import_type).import!
  end
end
```

**Lock types**:
- `:until_executing` - Unique while in queue, allows retries
- `:until_executed` - Unique through completion
- `:until_and_while_executing` - Most restrictive

## Batch Processing

### Find in Batches

```ruby
class BulkEmailJob < ApplicationJob
  BATCH_SIZE = 100

  def perform(campaign_id)
    campaign = Campaign.find(campaign_id)

    campaign.subscribers.find_in_batches(batch_size: BATCH_SIZE) do |batch|
      batch.each do |subscriber|
        SendCampaignEmailJob.perform_later(campaign_id, subscriber.id)
      end

      # Update progress
      campaign.increment!(:processed_count, batch.size)
    end
  end
end
```

### Self-Chaining Batch Job

```ruby
class LargeDataProcessJob < ApplicationJob
  BATCH_SIZE = 1000

  def perform(dataset_id, offset = 0)
    dataset = Dataset.find(dataset_id)
    batch = dataset.records.offset(offset).limit(BATCH_SIZE)

    return if batch.empty?

    process_batch(batch)

    # Queue next batch
    self.class.perform_later(dataset_id, offset + BATCH_SIZE)
  end

  private

  def process_batch(records)
    records.each do |record|
      process_record(record)
    end
  end
end
```

### Parallel Batch Processing

```ruby
class ParallelProcessJob < ApplicationJob
  def perform(ids)
    # Split into smaller batches and process in parallel
    ids.each_slice(100) do |batch_ids|
      ProcessBatchJob.perform_later(batch_ids)
    end
  end
end
```

### Efficient Batch Enqueueing (Rails 7.1+)

**Detection**: Check Rails version >= 7.1

Use `ActiveJob.perform_all_later` to enqueue multiple jobs in a single database operation, reducing overhead.

```ruby
class Notification::Bundle
  class << self
    def deliver_all_later
      # Find all bundles due for delivery
      due.find_in_batches do |batch|
        # Create job instances
        jobs = batch.map { |bundle| DeliverJob.new(bundle) }

        # Enqueue all at once - single DB operation
        ActiveJob.perform_all_later(jobs)
      end
    end
  end
end

# Usage in recurring job
class DeliverNotificationBundlesJob < ApplicationJob
  def perform
    Notification::Bundle.deliver_all_later
  end
end
```

**Benefits**:
- Reduces database round trips
- Atomic enqueueing of related jobs
- Better performance for bulk operations

## Scheduled Jobs

### Context Awareness for Recurring Jobs

**Detection**: Check for existing scheduling infrastructure:
- `config/recurring.yml` → Solid Queue recurring jobs
- `config/sidekiq_schedule.yml` → sidekiq-cron or sidekiq-scheduler
- `config/schedule.rb` → whenever gem (cron-based)

**If existing scheduler found**: Work within that system
**If none exists**: Suggest based on ActiveJob adapter

### Solid Queue Recurring Jobs

**Detection**: Check for Solid Queue adapter and `config/recurring.yml`

```yaml
# config/recurring.yml
production: &production
  # Run every 30 minutes
  deliver_bundled_notifications:
    command: "Notification::Bundle.deliver_all_later"
    schedule: every 30 minutes

  # Cron-style scheduling
  auto_postpone_all_due:
    command: "Card.auto_postpone_all_due"
    schedule: every hour at minute 50

  # Job class with arguments
  delete_unused_tags:
    class: DeleteUnusedTagsJob
    schedule: every day at 04:02

  # With queue specification
  weekly_report:
    class: WeeklyReportJob
    args: ["summary"]
    schedule: every monday at 9am
    queue: low

development:
  <<: *production

test:
  # Usually empty or minimal in test
```

**Schedule formats**:
- `every 30 minutes`
- `every hour at minute 15`
- `every day at 2:30am`
- `every monday at 9am`
- `every 1st day of month at 3am`

### Recurring Job Pattern

```ruby
class DailyReportJob < ApplicationJob
  def perform(date = Date.current)
    # Idempotency: check if already run
    return if Report.exists?(date: date, type: 'daily')

    report = Report.create!(
      date: date,
      type: 'daily',
      data: generate_report_data(date)
    )

    ReportMailer.daily_report(report).deliver_later
  end

  private

  def generate_report_data(date)
    {
      orders: Order.where(created_at: date.all_day).count,
      revenue: Order.where(created_at: date.all_day).sum(:total),
      new_users: User.where(created_at: date.all_day).count
    }
  end
end
```

### With sidekiq-cron or sidekiq-scheduler

```yaml
# config/sidekiq_schedule.yml
daily_report:
  cron: "0 2 * * *"  # 2 AM daily
  class: DailyReportJob
  queue: low

hourly_sync:
  every: "1h"
  class: SyncDataJob
  queue: default
```

## Error Handling Strategies

### Custom Error Types

```ruby
class PaymentError < StandardError; end
class InsufficientFundsError < PaymentError; end
class CardExpiredError < PaymentError; end

class ProcessPaymentJob < ApplicationJob
  # Retry billing errors
  retry_on PaymentError, wait: :exponentially_longer, attempts: 5

  # Don't retry card issues - user needs to update
  discard_on CardExpiredError do |job, error|
    payment = Payment.find(job.arguments.first)
    payment.update!(status: 'card_expired')
    PaymentMailer.card_expired(payment).deliver_later
  end

  def perform(payment_id)
    payment = Payment.find(payment_id)
    PaymentProcessor.charge!(payment)
  end
end
```

### Dead Letter Queue Pattern

```ruby
class ReliableJob < ApplicationJob
  retry_on StandardError, attempts: 5

  after_discard do |job, error|
    # Record failed job for manual review
    FailedJob.create!(
      job_class: job.class.name,
      arguments: job.arguments,
      error_class: error.class.name,
      error_message: error.message,
      failed_at: Time.current
    )

    # Alert team
    SlackNotifier.notify("Job failed: #{job.class.name} - #{error.message}")
  end
end
```

## Monitoring and Logging

### Instrumented Job

```ruby
class InstrumentedJob < ApplicationJob
  around_perform do |job, block|
    start_time = Time.current

    Rails.logger.info({
      event: 'job_started',
      job_class: job.class.name,
      job_id: job.job_id,
      arguments: job.arguments
    }.to_json)

    block.call

    duration = Time.current - start_time
    Rails.logger.info({
      event: 'job_completed',
      job_class: job.class.name,
      job_id: job.job_id,
      duration_ms: (duration * 1000).round
    }.to_json)

    # Track metrics
    StatsD.timing("jobs.#{job.class.name.underscore}.duration", duration)
    StatsD.increment("jobs.#{job.class.name.underscore}.success")
  rescue StandardError => e
    StatsD.increment("jobs.#{job.class.name.underscore}.failure")
    raise
  end
end
```

## Multi-Tenant Context Serialization

**Applicability**: Multi-tenant applications using `CurrentAttributes` pattern

**Detection**:
1. Check for `app/models/current.rb` with `CurrentAttributes`
2. Check for multi-tenant architecture (e.g., `account_id` on tables)
3. If single-tenant app: Skip this pattern

**When not applicable**: Single-tenant applications don't need context serialization

### Automatic Account Context (37signals Pattern)

For multi-tenant apps, automatically serialize and restore the current account context across job execution:

```ruby
# config/initializers/active_job_extensions.rb
module FizzyActiveJobExtensions
  extend ActiveSupport::Concern

  prepended do
    attr_reader :account
    # Ensure jobs are only enqueued after transaction commits
    self.enqueue_after_transaction_commit = true
  end

  # Capture current account when job is enqueued
  def initialize(...)
    super
    @account = Current.account
  end

  # Serialize account reference
  def serialize
    super.merge({ "account" => @account&.to_gid })
  end

  # Deserialize account reference
  def deserialize(job_data)
    super
    if _account = job_data.fetch("account", nil)
      @account = GlobalID::Locator.locate(_account)
    end
  end

  # Restore account context during execution
  def perform_now
    if account.present?
      Current.with_account(account) { super }
    else
      super
    end
  end
end

# Apply to all jobs
ActiveSupport.on_load(:active_job) do
  prepend FizzyActiveJobExtensions
end
```

### Usage in Multi-Tenant App

```ruby
# app/models/current.rb
class Current < ActiveSupport::CurrentAttributes
  attribute :account, :user

  def self.with_account(account)
    set(account: account) { yield }
  end
end

# Jobs automatically capture and restore account context
class ProcessInvoiceJob < ApplicationJob
  def perform(invoice)
    # Current.account is automatically set from job initialization
    invoice.process!

    # All queries are scoped to the account
    notifications = Notification.where(invoice: invoice)
  end
end

# When enqueued, captures current account
Current.set(account: @account) do
  ProcessInvoiceJob.perform_later(invoice)
end
```

**Benefits**:
- No manual account passing to jobs
- Prevents cross-tenant data leaks
- Consistent context across async operations
- Works with existing `Current` pattern

**Detection checklist**:
```ruby
# Check for CurrentAttributes
File.exist?('app/models/current.rb')

# Check for multi-tenancy indicators
grep -r "account_id" db/schema.rb
grep -r "Current.account" app/
```

## Queue Configuration

### Sidekiq Configuration

```yaml
# config/sidekiq.yml
:concurrency: 10

:queues:
  - [critical, 6]    # 6x weight
  - [default, 3]     # 3x weight
  - [low, 1]         # 1x weight
  - [mailers, 2]     # For ActionMailer

# Production with memory limits
:max_retries: 25
:dead_max_jobs: 10000
```

### Queue-Specific Workers

```ruby
# Critical operations
class ChargePaymentJob < ApplicationJob
  queue_as :critical
end

# Default priority
class SendNotificationJob < ApplicationJob
  queue_as :default
end

# Background cleanup
class CleanupJob < ApplicationJob
  queue_as :low
end
```

## Testing Patterns

### Test Job Execution

```ruby
RSpec.describe ProcessOrderJob, type: :job do
  include ActiveJob::TestHelper

  describe '#perform' do
    let(:order) { create(:order, status: 'pending') }

    it 'processes the order' do
      expect {
        described_class.perform_now(order.id)
      }.to change { order.reload.status }.to('processed')
    end

    it 'sends confirmation email' do
      expect {
        described_class.perform_now(order.id)
      }.to have_enqueued_job(ActionMailer::MailDeliveryJob)
    end
  end

  describe 'error handling' do
    it 'retries on network errors' do
      allow(OrderProcessor).to receive(:new).and_raise(Net::OpenTimeout)

      assert_performed_jobs 0 do
        described_class.perform_later(create(:order).id)
      end
    end
  end
end
```

### Test Enqueuing

```ruby
it 'enqueues with correct arguments' do
  expect {
    ProcessOrderJob.perform_later(order.id)
  }.to have_enqueued_job(ProcessOrderJob)
    .with(order.id)
    .on_queue('default')
end
```

## Directory Organization

```
app/jobs/
├── application_job.rb
├── concerns/
│   ├── idempotent.rb
│   └── instrumented.rb
├── orders/
│   ├── process_order_job.rb
│   └── cancel_order_job.rb
├── payments/
│   └── process_payment_job.rb
├── notifications/
│   └── send_notification_job.rb
└── maintenance/
    ├── cleanup_job.rb
    └── daily_report_job.rb
```

## Context Awareness Guide

When suggesting job patterns, detect the project context first:

| Pattern | Detection Strategy | Conflicts | Applicability |
|---------|-------------------|-----------|---------------|
| **`_later`/`_now` convention** | Check existing job naming patterns | None - naming convention only | ✅ **Always applicable** |
| **Shallow jobs** | Check existing job complexity (lines in `perform`) | Fat jobs with embedded business logic | ✅ **Use now** for new jobs<br>📋 **Future direction** for refactoring |
| **Context serialization** | Check for `app/models/current.rb`<br>Check for `account_id` in schema<br>Check for `Current.account` usage | Single-tenant apps | ⚠️ **Multi-tenant only**<br>❌ Skip if single-tenant |
| **`limits_concurrency`** | Check `config.active_job.queue_adapter`<br>Look for Solid Queue gem | Sidekiq (needs extension) | ✅ **Use now** if Solid Queue<br>🔧 Check adapter otherwise |
| **Recurring jobs** | Check for `config/recurring.yml`<br>Check for `sidekiq-cron`/`sidekiq-scheduler`<br>Check for `config/schedule.rb` (whenever) | Existing scheduler choice | 🎯 **Respect existing choice**<br>Suggest based on adapter if none |
| **Batch enqueueing** | Check Rails version in `Gemfile.lock` | Rails < 7.1 | ✅ Rails 7.1+<br>❌ Use `.each` for older versions |

### Detection Commands

```ruby
# Check job adapter
# config/application.rb or config/environments/production.rb
grep -r "config.active_job.queue_adapter" config/

# Check for multi-tenancy
File.exist?('app/models/current.rb')
grep -r "account_id" db/schema.rb

# Check for existing schedulers
File.exist?('config/recurring.yml')        # Solid Queue
File.exist?('config/sidekiq_schedule.yml') # sidekiq-cron
File.exist?('config/schedule.rb')          # whenever

# Check Rails version
grep "^  rails " Gemfile.lock

# Check for unique jobs gem
grep "sidekiq-unique-jobs" Gemfile
```

### Context-Aware Recommendations

**When analyzing a project**:
1. Run detection checks first
2. Suggest patterns that match the existing infrastructure
3. Note patterns that would require additional setup
4. Flag patterns that don't apply to this architecture

**Example**:
```
✅ Solid Queue detected → Suggest `limits_concurrency`
⚠️ No multi-tenancy detected → Skip context serialization pattern
✅ Rails 7.1+ → Suggest `perform_all_later` for batch enqueueing
📋 Fat jobs detected → Suggest shallow job refactoring as future improvement
```

## Best Practices Summary

### Do
- Make jobs idempotent (safe to retry)
- Pass IDs, not objects
- Use appropriate queues
- Handle errors explicitly
- Log job execution
- Test thoroughly
- Use `_later`/`_now` naming convention
- Keep jobs shallow, logic in models
- Detect project context before suggesting patterns

### Don't
- Store state in instance variables
- Perform synchronous operations that could be async
- Create jobs with large payloads
- Ignore failed jobs
- Skip idempotency guards
- Suggest multi-tenant patterns to single-tenant apps
- Recommend Solid Queue features to Sidekiq projects
