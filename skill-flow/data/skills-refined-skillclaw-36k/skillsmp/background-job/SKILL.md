---
name: background-job
description: Generate background jobs for async tasks using Solid Queue. Use when user needs email sending, notifications, data processing, scheduled tasks, or says "send email in background", "process async", "create job", "schedule task", "queue work".
---

# Background Job Generator

Generate background jobs using Solid Queue for asynchronous task processing.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Identify async task needed
- [ ] 2. Create job class
- [ ] 3. Add job logic
- [ ] 4. Enqueue job from controller/model
- [ ] 5. Test job execution
- [ ] 6. Monitor queue dashboard
```

## Project Setup

**Solid Queue** (Rails 8 기본 탑재):
```ruby
# Gemfile (already included)
gem "solid_queue"

# config/queue.yml (already configured)
# Solid Queue runs in-process or separate worker
```

**Queue Dashboard**:
```ruby
# config/routes.rb
require "solid_queue/engine"
mount SolidQueue::Engine => "/queue"
```

## Job Structure

```
app/jobs/
├── application_job.rb      # Base class
├── email_job.rb            # Email sending
├── notification_job.rb     # Push notifications
├── data_import_job.rb      # Data processing
└── cleanup_job.rb          # Scheduled cleanup
```

## Basic Job Template

```ruby
# app/jobs/example_job.rb
class ExampleJob < ApplicationJob
  queue_as :default

  def perform(arg1, arg2)
    # Job logic here
    puts "Processing #{arg1} and #{arg2}"
  end
end
```

**Enqueue**:
```ruby
# Execute immediately (in background)
ExampleJob.perform_later("value1", "value2")

# Execute at specific time
ExampleJob.set(wait: 1.hour).perform_later("value1", "value2")
ExampleJob.set(wait_until: Date.tomorrow.noon).perform_later("value1", "value2")
```

## Common Job Types

### 1. Email Job

```ruby
# app/jobs/send_email_job.rb
class SendEmailJob < ApplicationJob
  queue_as :default

  retry_on Net::SMTPServerBusy, wait: 5.minutes, attempts: 3

  def perform(user_id, email_type)
    user = User.find(user_id)

    case email_type
    when "welcome"
      UserMailer.welcome_email(user).deliver_now
    when "notification"
      UserMailer.notification_email(user).deliver_now
    else
      raise ArgumentError, "Unknown email type: #{email_type}"
    end

    Rails.logger.info "Sent #{email_type} email to user #{user.id}"
  end
end
```

**Usage**:
```ruby
# In controller or model
SendEmailJob.perform_later(user.id, "welcome")
```

### 2. Notification Job

```ruby
# app/jobs/send_notification_job.rb
class SendNotificationJob < ApplicationJob
  queue_as :notifications

  def perform(notification_id)
    notification = Notification.find(notification_id)

    # Send push notification
    send_push_notification(notification)

    # Mark as sent
    notification.update(sent_at: Time.current)
  end

  private

  def send_push_notification(notification)
    # Integration with FCM, APNs, etc.
    Rails.logger.info "Sending notification #{notification.id}"
  end
end
```

### 3. Data Processing Job

```ruby
# app/jobs/process_import_job.rb
class ProcessImportJob < ApplicationJob
  queue_as :heavy

  # Retry with exponential backoff
  retry_on StandardError, wait: :exponentially_longer, attempts: 5

  def perform(file_path)
    CSV.foreach(file_path, headers: true) do |row|
      User.create!(
        email: row["email"],
        name: row["name"]
      )
    end

    # Cleanup temp file
    File.delete(file_path) if File.exist?(file_path)
  rescue StandardError => e
    Rails.logger.error "Import failed: #{e.message}"
    raise
  end
end
```

### 4. Scheduled Job (Cleanup)

```ruby
# app/jobs/cleanup_old_posts_job.rb
class CleanupOldPostsJob < ApplicationJob
  queue_as :maintenance

  def perform
    deleted_count = Post.where("created_at < ?", 1.year.ago)
                        .where(status: :draft)
                        .delete_all

    Rails.logger.info "Cleaned up #{deleted_count} old draft posts"
  end
end
```

**Schedule with cron**:
```ruby
# config/recurring.yml (Solid Queue)
production:
  cleanup_old_posts:
    class: CleanupOldPostsJob
    queue: maintenance
    schedule: "0 2 * * *" # 2 AM daily
```

## Queue Priority

```ruby
# app/jobs/high_priority_job.rb
class HighPriorityJob < ApplicationJob
  queue_as :urgent
  queue_with_priority 10 # Higher = more priority
end

# app/jobs/low_priority_job.rb
class LowPriorityJob < ApplicationJob
  queue_as :background
  queue_with_priority 1
end
```

**Queue Configuration** (config/queue.yml):
```yaml
production:
  dispatchers:
    - polling_interval: 1
      batch_size: 500
  workers:
    - queues: urgent
      threads: 3
      processes: 2
      polling_interval: 0.1
    - queues: default,notifications
      threads: 5
      processes: 3
    - queues: heavy,maintenance
      threads: 2
      processes: 1
```

## Error Handling

### Retry Strategies

```ruby
class RetryableJob < ApplicationJob
  # Retry specific errors
  retry_on ConnectionError, wait: 5.seconds, attempts: 3

  # Exponential backoff
  retry_on TimeoutError, wait: :exponentially_longer, attempts: 10

  # Custom retry logic
  retry_on CustomError do |job, exception|
    Rails.logger.error "Job #{job.class} failed: #{exception.message}"
    Sentry.capture_exception(exception)
  end

  # Discard on certain errors
  discard_on ActiveJob::DeserializationError

  def perform
    # Job logic
  end
end
```

### Error Callbacks

```ruby
class MonitoredJob < ApplicationJob
  around_perform :log_execution

  rescue_from StandardError do |exception|
    Rails.logger.error "Job failed: #{exception.message}"
    # Send to error tracking service
    Sentry.capture_exception(exception)
  end

  def perform
    # Job logic
  end

  private

  def log_execution
    start_time = Time.current
    Rails.logger.info "Starting job: #{self.class.name}"

    yield

    duration = Time.current - start_time
    Rails.logger.info "Job completed in #{duration}s"
  end
end
```

## Testing

```ruby
# test/jobs/send_email_job_test.rb
require "test_helper"

class SendEmailJobTest < ActiveJob::TestCase
  test "enqueues email job" do
    assert_enqueued_with(job: SendEmailJob, args: [users(:one).id, "welcome"]) do
      SendEmailJob.perform_later(users(:one).id, "welcome")
    end
  end

  test "sends welcome email" do
    assert_emails 1 do
      SendEmailJob.perform_now(users(:one).id, "welcome")
    end
  end

  test "handles missing user gracefully" do
    assert_raises(ActiveRecord::RecordNotFound) do
      SendEmailJob.perform_now(99999, "welcome")
    end
  end
end
```

## Monitoring

### Dashboard
```
Visit: http://localhost:3000/queue
- View pending jobs
- Monitor failed jobs
- See queue statistics
```

### Logging
```ruby
# config/environments/production.rb
config.active_job.logger = ActiveSupport::Logger.new("log/jobs.log")

# In jobs
Rails.logger.info "Job started: #{job_id}"
Rails.logger.error "Job failed: #{error_message}"
```

### Metrics
```ruby
# app/jobs/application_job.rb
class ApplicationJob < ActiveJob::Base
  around_perform :track_performance

  private

  def track_performance
    start_time = Time.current
    yield
  ensure
    duration = Time.current - start_time
    Rails.logger.info "Job #{self.class.name} took #{duration}s"
    # Send to monitoring service (e.g., StatsD)
  end
end
```

## Best Practices

1. **Idempotent Jobs**: Jobs should be safe to run multiple times
2. **Small Arguments**: Pass IDs, not full objects
3. **Queue Separation**: Different queues for different priorities
4. **Error Handling**: Always handle errors gracefully
5. **Logging**: Log important events for debugging
6. **Timeouts**: Set appropriate timeouts for long-running jobs
7. **Monitoring**: Track job performance and failures

## Integration Examples

### After Create Hook
```ruby
# app/models/user.rb
class User < ApplicationRecord
  after_create_commit :send_welcome_email

  private

  def send_welcome_email
    SendEmailJob.perform_later(id, "welcome")
  end
end
```

### Controller Action
```ruby
# app/controllers/imports_controller.rb
class ImportsController < ApplicationController
  def create
    file = params[:file]
    temp_path = Rails.root.join("tmp", "import_#{Time.current.to_i}.csv")

    File.open(temp_path, "wb") do |f|
      f.write(file.read)
    end

    ProcessImportJob.perform_later(temp_path.to_s)

    redirect_to root_path, notice: "Import started. You'll be notified when complete."
  end
end
```

### Batch Processing
```ruby
# app/jobs/batch_notification_job.rb
class BatchNotificationJob < ApplicationJob
  queue_as :notifications

  def perform(user_ids)
    User.where(id: user_ids).find_each do |user|
      SendNotificationJob.perform_later(user.id)
    end
  end
end

# Usage
user_ids = User.active.pluck(:id)
user_ids.each_slice(100) do |batch|
  BatchNotificationJob.perform_later(batch)
end
```

## Troubleshooting

**Jobs not processing?**
```bash
# Check Solid Queue is running
bin/rails solid_queue:start

# Or in separate process
bundle exec rake solid_queue:work
```

**Failed jobs?**
- Check `/queue` dashboard
- Review logs: `tail -f log/jobs.log`
- Retry manually: `SolidQueue::Job.find(id).retry`

**Performance issues?**
- Increase worker threads in config/queue.yml
- Split heavy jobs into smaller ones
- Use queue priorities effectively

## Examples

- [Email Job Example](examples/send_email_job.rb)
- [Data Processing Example](examples/process_data_job.rb)
- [Scheduled Job Example](examples/cleanup_job.rb)

## Checklist

- [ ] Job class created in app/jobs/
- [ ] Inherits from ApplicationJob
- [ ] Queue specified with `queue_as`
- [ ] Error handling added (retry_on/discard_on)
- [ ] Enqueued from appropriate location
- [ ] Tested with perform_now
- [ ] Logged important events
- [ ] Monitored in /queue dashboard
