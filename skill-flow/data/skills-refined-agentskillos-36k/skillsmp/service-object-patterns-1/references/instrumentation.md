# Instrumentation & Monitoring Reference

## Structured Logging Concern

```ruby
# app/services/concerns/loggable.rb
module Services
  module Concerns
    module Loggable
      extend ActiveSupport::Concern

      private

      def log_info(message, context = {})
        log(:info, message, context)
      end

      def log_warn(message, context = {})
        log(:warn, message, context)
      end

      def log_error(message, context = {})
        log(:error, message, context)
      end

      def log_debug(message, context = {})
        log(:debug, message, context)
      end

      def log(level, message, context = {})
        Rails.logger.public_send(level, {
          service: self.class.name,
          message: message,
          timestamp: Time.current.iso8601,
          **context
        }.to_json)
      end

      def log_service_start(context = {})
        log_info("Service started", {
          params: sanitized_params,
          **context
        })
      end

      def log_service_complete(result, context = {})
        log_info("Service completed", {
          success: result.success?,
          duration_ms: context[:duration_ms],
          **context
        })
      end

      def log_external_api_call(api_name, endpoint, context = {})
        log_info("External API call", {
          api: api_name,
          endpoint: endpoint,
          **context
        })
      end
    end
  end
end
```

---

## Metrics Collection Concern

```ruby
# app/services/concerns/metrics.rb
module Services
  module Concerns
    module Metrics
      extend ActiveSupport::Concern

      def track_counter(metric_name, value = 1, tags: {})
        if defined?(StatsD)
          StatsD.increment(
            "service.#{metric_name}",
            value,
            tags: format_tags(tags)
          )
        end
      end

      def track_gauge(metric_name, value, tags: {})
        if defined?(StatsD)
          StatsD.gauge(
            "service.#{metric_name}",
            value,
            tags: format_tags(tags)
          )
        end
      end

      def track_timing(metric_name, duration_ms, tags: {})
        if defined?(StatsD)
          StatsD.timing(
            "service.#{metric_name}",
            duration_ms,
            tags: format_tags(tags)
          )
        end
      end

      def track_histogram(metric_name, value, tags: {})
        if defined?(StatsD)
          StatsD.histogram(
            "service.#{metric_name}",
            value,
            tags: format_tags(tags)
          )
        end
      end

      private

      def format_tags(tags)
        default_tags.merge(tags).map { |k, v| "#{k}:#{v}" }
      end

      def default_tags
        {
          service: self.class.name.underscore.tr('/', '.'),
          environment: Rails.env
        }
      end
    end
  end
end
```

---

## ActiveSupport Notifications

```ruby
# In service
module TasksManager
  class CreateTask < ApplicationService
    def call
      ActiveSupport::Notifications.instrument(
        "task.create",
        account_id: @account.id,
        merchant_id: @merchant.id
      ) do |payload|
        task = build_and_save_task

        payload[:task_id] = task.id
        payload[:zone_id] = task.zone_id

        ServiceResult.success(task)
      end
    end
  end
end

# config/initializers/service_notifications.rb
ActiveSupport::Notifications.subscribe("task.create") do |name, start, finish, id, payload|
  duration = (finish - start) * 1000

  Rails.logger.info({
    event: name,
    duration_ms: duration.round(2),
    account_id: payload[:account_id],
    task_id: payload[:task_id]
  }.to_json)

  if defined?(StatsD)
    StatsD.increment("task.created", tags: [
      "account:#{payload[:account_id]}",
      "merchant:#{payload[:merchant_id]}"
    ])

    StatsD.timing("task.creation_duration", duration, tags: [
      "account:#{payload[:account_id]}"
    ])
  end
end
```

---

## Error Tracking Integration

```ruby
# app/services/concerns/error_tracking.rb
module Services
  module Concerns
    module ErrorTracking
      extend ActiveSupport::Concern

      private

      def capture_exception(exception, context: {})
        # Sentry
        if defined?(Sentry)
          Sentry.capture_exception(exception, extra: {
            service: self.class.name,
            context: context,
            params: sanitized_params
          })
        end

        # Rollbar
        if defined?(Rollbar)
          Rollbar.error(exception, {
            service: self.class.name,
            context: context,
            params: sanitized_params
          })
        end

        # Airbrake
        if defined?(Airbrake)
          Airbrake.notify(exception, {
            service: self.class.name,
            context: context,
            params: sanitized_params
          })
        end
      end

      def capture_message(message, level: :info, context: {})
        if defined?(Sentry)
          Sentry.capture_message(message, level: level, extra: {
            service: self.class.name,
            context: context
          })
        end
      end
    end
  end
end
```

---

## Performance Instrumentation

```ruby
# app/services/concerns/instrumentation.rb
module Services
  module Concerns
    module Instrumentation
      extend ActiveSupport::Concern

      private

      def instrument_service_call
        start_time = Time.current
        service_name = self.class.name.underscore.tr('/', '.')

        ActiveSupport::Notifications.instrument(
          "service.call",
          service: service_name,
          params: sanitized_params
        ) do
          result = yield

          duration = (Time.current - start_time) * 1000

          log_performance(service_name, duration, result)
          track_metrics(service_name, duration, result)

          result
        end
      end

      def log_performance(service_name, duration, result)
        Rails.logger.info({
          service: service_name,
          duration_ms: duration.round(2),
          success: result.success?,
          timestamp: Time.current.iso8601
        }.to_json)
      end

      def track_metrics(service_name, duration, result)
        if defined?(StatsD)
          StatsD.increment("service.calls", tags: [
            "service:#{service_name}",
            "status:#{result.success? ? 'success' : 'failure'}"
          ])

          StatsD.timing("service.duration", duration, tags: [
            "service:#{service_name}"
          ])
        end

        if defined?(PrometheusExporter)
          PrometheusExporter::Client.default.send_json(
            type: "service_call",
            service: service_name,
            duration: duration,
            success: result.success?
          )
        end
      end
    end
  end
end
```
