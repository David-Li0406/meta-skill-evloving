# Error Handling Patterns Reference

## Custom Error Classes

```ruby
# app/services/errors.rb
module Services
  module Errors
    class ServiceError < StandardError
      attr_reader :context

      def initialize(message = nil, context: {})
        @context = context
        super(message)
      end
    end

    class ValidationError < ServiceError; end
    class AuthorizationError < ServiceError; end
    class ExternalServiceError < ServiceError; end
    class TimeoutError < ServiceError; end
    class RateLimitError < ServiceError; end
    class ResourceNotFoundError < ServiceError; end
  end
end

# Usage in service
module TasksManager
  class CreateTask < ApplicationService
    def call
      validate_authorization!
      validate_params!

      task = build_and_save_task
      ServiceResult.success(task)
    rescue Services::Errors::ValidationError => e
      ServiceResult.failure(e.message, errors: e.context[:errors])
    rescue Services::Errors::AuthorizationError => e
      ServiceResult.failure("Not authorized", context: e.context)
    end

    private

    def validate_authorization!
      unless @user.can?(:create_task, @account)
        raise Services::Errors::AuthorizationError.new(
          "User not authorized to create tasks",
          context: { user_id: @user.id, account_id: @account.id }
        )
      end
    end

    def validate_params!
      errors = []
      errors << "Recipient required" unless @params[:recipient_id]
      errors << "Address required" unless @params[:address]

      if errors.any?
        raise Services::Errors::ValidationError.new(
          "Validation failed",
          context: { errors: errors }
        )
      end
    end
  end
end
```

---

## Error Handler Concern

```ruby
# app/services/concerns/error_handling.rb
module Services
  module Concerns
    module ErrorHandling
      extend ActiveSupport::Concern

      included do
        rescue_from StandardError, with: :handle_standard_error
        rescue_from ActiveRecord::RecordInvalid, with: :handle_record_invalid
        rescue_from Services::Errors::ServiceError, with: :handle_service_error
      end

      private

      def handle_standard_error(exception)
        log_error(exception)
        track_error(exception)
        ServiceResult.failure("An unexpected error occurred")
      end

      def handle_record_invalid(exception)
        log_error(exception)
        ServiceResult.failure(
          "Validation failed",
          errors: exception.record.errors.full_messages
        )
      end

      def handle_service_error(exception)
        log_error(exception, context: exception.context)
        ServiceResult.failure(exception.message, context: exception.context)
      end

      def log_error(exception, context: {})
        Rails.logger.error({
          error_class: exception.class.name,
          error_message: exception.message,
          backtrace: exception.backtrace.first(5),
          context: context,
          service: self.class.name
        }.to_json)
      end

      def track_error(exception)
        if defined?(Sentry)
          Sentry.capture_exception(exception, extra: {
            service: self.class.name,
            params: sanitized_params
          })
        end
      end

      def sanitized_params
        @params.except(:password, :token, :api_key)
      end
    end
  end
end
```

---

## Retry Mechanism

```ruby
# app/services/concerns/retriable.rb
module Services
  module Concerns
    module Retriable
      extend ActiveSupport::Concern

      RETRYABLE_ERRORS = [
        Faraday::TimeoutError,
        Faraday::ConnectionFailed,
        Services::Errors::TimeoutError,
        ActiveRecord::Deadlocked
      ].freeze

      def with_retry(max_attempts: 3, backoff: 2, &block)
        attempt = 1

        begin
          yield
        rescue *RETRYABLE_ERRORS => e
          if attempt < max_attempts
            sleep_duration = backoff**attempt
            Rails.logger.warn(
              "Retrying after error (attempt #{attempt}/#{max_attempts}): #{e.message}. " \
              "Sleeping #{sleep_duration}s"
            )
            sleep(sleep_duration)
            attempt += 1
            retry
          else
            Rails.logger.error("Max retry attempts (#{max_attempts}) exceeded: #{e.message}")
            raise
          end
        end
      end
    end
  end
end

# Usage
module Integrations
  module Shipping
    class CreateLabel < ApplicationService
      include Services::Concerns::Retriable

      def call
        with_retry(max_attempts: 3, backoff: 2) do
          response = make_api_request
          process_response(response)
        end
      rescue Faraday::TimeoutError => e
        ServiceResult.failure("Shipping API timeout after retries")
      end
    end
  end
end
```

---

## Circuit Breaker Pattern

```ruby
# app/services/concerns/circuit_breaker.rb
module Services
  module Concerns
    module CircuitBreaker
      extend ActiveSupport::Concern

      class_methods do
        def circuit_breaker(service_name, failure_threshold: 5, timeout: 60)
          @circuit_state ||= {}
          @circuit_state[service_name] ||= {
            failures: 0,
            last_failure_time: nil,
            state: :closed,  # :closed, :open, :half_open
            failure_threshold: failure_threshold,
            timeout: timeout
          }
        end

        def circuit_open?(service_name)
          circuit = @circuit_state[service_name]
          return false unless circuit

          if circuit[:state] == :open
            if Time.current - circuit[:last_failure_time] > circuit[:timeout]
              circuit[:state] = :half_open
              false
            else
              true
            end
          else
            false
          end
        end

        def record_success(service_name)
          circuit = @circuit_state[service_name]
          return unless circuit

          circuit[:failures] = 0
          circuit[:state] = :closed
        end

        def record_failure(service_name)
          circuit = @circuit_state[service_name]
          return unless circuit

          circuit[:failures] += 1
          circuit[:last_failure_time] = Time.current

          if circuit[:failures] >= circuit[:failure_threshold]
            circuit[:state] = :open
            Rails.logger.warn("Circuit breaker opened for #{service_name}")
          end
        end
      end

      def with_circuit_breaker(service_name, &block)
        if self.class.circuit_open?(service_name)
          raise Services::Errors::ExternalServiceError.new(
            "Circuit breaker open for #{service_name}",
            context: { service: service_name }
          )
        end

        result = yield
        self.class.record_success(service_name)
        result
      rescue StandardError => e
        self.class.record_failure(service_name)
        raise
      end
    end
  end
end

# Usage
module Integrations
  module Shipping
    class CreateLabel < ApplicationService
      include Services::Concerns::CircuitBreaker

      circuit_breaker :shipping_api, failure_threshold: 5, timeout: 60

      def call
        with_circuit_breaker(:shipping_api) do
          response = make_api_request
          process_response(response)
        end
      rescue Services::Errors::ExternalServiceError => e
        ServiceResult.failure(e.message)
      end
    end
  end
end
```
