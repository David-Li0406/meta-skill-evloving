---
id: ruby-sidekiq-jobs
name: "Sidekiq Background Jobs"
domain: RUBY
skill: faion-software-developer
category: "backend"
---

## Sidekiq Background Jobs

### Problem
Process tasks asynchronously for better performance.

### Framework: Job Structure

```ruby
# app/jobs/process_order_job.rb
class ProcessOrderJob
  include Sidekiq::Job

  sidekiq_options queue: :default, retry: 3, dead: true

  sidekiq_retry_in do |count, exception|
    case exception
    when PaymentGatewayError
      (count + 1) * 60 # Linear backoff for payment issues
    else
      (count ** 4) + 15 # Exponential backoff
    end
  end

  def perform(order_id)
    order = Order.find(order_id)

    return if order.processed?

    OrderProcessor.new(order).process!

    NotifyCustomerJob.perform_async(order_id)
  rescue ActiveRecord::RecordNotFound
    # Order deleted, nothing to do
    Sidekiq.logger.warn "Order #{order_id} not found"
  rescue PaymentGatewayError => e
    # Will retry with custom backoff
    raise
  rescue StandardError => e
    ErrorTracker.capture(e, order_id: order_id)
    raise
  end
end

# app/jobs/notify_customer_job.rb
class NotifyCustomerJob
  include Sidekiq::Job

  sidekiq_options queue: :notifications, retry: 5

  def perform(order_id)
    order = Order.find(order_id)
    OrderMailer.confirmation(order).deliver_now
  end
end
```

### Batch Processing

```ruby
# app/jobs/batch_export_job.rb
class BatchExportJob
  include Sidekiq::Job

  sidekiq_options queue: :exports, retry: 1

  def perform(export_id)
    export = Export.find(export_id)
    export.update!(status: :processing)

    records = export.query_records

    CSV.open(export.file_path, 'wb') do |csv|
      csv << export.headers
      records.find_each(batch_size: 1000) do |record|
        csv << export.row_for(record)
      end
    end

    export.update!(status: :completed, completed_at: Time.current)
    ExportMailer.ready(export).deliver_later
  rescue StandardError => e
    export.update!(status: :failed, error_message: e.message)
    raise
  end
end
```

### Agent

faion-backend-agent
