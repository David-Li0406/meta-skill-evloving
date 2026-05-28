# Complete Service Examples Reference

## Service Composition Pattern

```ruby
# app/services/tasks_manager/process_delivery.rb
module TasksManager
  class ProcessDelivery < ApplicationService
    def initialize(task:, carrier:, params:)
      @task = task
      @carrier = carrier
      @params = params
    end

    def call
      ActiveRecord::Base.transaction do
        validate_delivery!
        complete_task!
        process_cod! if task.cod?
        generate_invoice!
        notify_all_parties!
      end

      ServiceResult.success(task.reload)
    rescue StandardError => e
      ServiceResult.failure(e.message)
    end

    private

    attr_reader :task, :carrier, :params

    def validate_delivery!
      result = DeliveryValidator.call(task: task, params: params)
      raise result.error unless result.success?
    end

    def complete_task!
      result = CompleteTask.call(
        task: task,
        otp: params[:otp],
        photos: params[:photos]
      )
      raise result.error unless result.success?
    end

    def process_cod!
      result = BillingManager::ProcessCod.call(
        task: task,
        carrier: carrier,
        amount: task.cod_amount
      )
      raise result.error unless result.success?
    end

    def generate_invoice!
      BillingManager::GenerateInvoice.call(task: task)
    end

    def notify_all_parties!
      NotificationsManager::DeliveryComplete.call(task: task)
    end
  end
end
```

---

## External API Integration

```ruby
# app/services/integrations/shipping/create_label.rb
module Integrations
  module Shipping
    class CreateLabel < ApplicationService
      TIMEOUT = 30.seconds

      def initialize(task:, shipping_company:)
        @task = task
        @shipping_company = shipping_company
      end

      def call
        response = make_api_request

        if response.success?
          label = create_label_record(response.body)
          ServiceResult.success(label)
        else
          handle_error(response)
        end
      rescue Faraday::TimeoutError
        ServiceResult.failure("Shipping API timeout")
      rescue Faraday::ConnectionFailed
        ServiceResult.failure("Unable to connect to shipping API")
      end

      private

      attr_reader :task, :shipping_company

      def make_api_request
        client.post('/labels', label_payload)
      end

      def client
        @client ||= Faraday.new(url: shipping_company.api_url) do |f|
          f.request :json
          f.response :json
          f.options.timeout = TIMEOUT
          f.headers['Authorization'] = "Bearer #{shipping_company.api_key}"
        end
      end

      def label_payload
        {
          sender: sender_details,
          recipient: recipient_details,
          package: package_details
        }
      end

      def create_label_record(response_body)
        task.create_shipping_label!(
          tracking_number: response_body['tracking_number'],
          label_url: response_body['label_url'],
          shipping_company: shipping_company
        )
      end

      def handle_error(response)
        error_message = response.body['error'] || "API Error: #{response.status}"
        Rails.logger.error("Shipping API Error: #{error_message}")
        ServiceResult.failure(error_message)
      end
    end
  end
end
```

---

## Bulk Import with Background Jobs

```ruby
# app/services/tasks_manager/bulk_import.rb
module TasksManager
  class BulkImport < ApplicationService
    def initialize(account:, file:, user:)
      @account = account
      @file = file
      @user = user
    end

    def call
      import = create_import_record
      schedule_processing(import)
      ServiceResult.success(import)
    end

    private

    attr_reader :account, :file, :user

    def create_import_record
      account.task_imports.create!(
        file: file,
        user: user,
        status: 'pending',
        total_rows: count_rows
      )
    end

    def schedule_processing(import)
      BulkImportJob.perform_later(import.id)
    end

    def count_rows
      CSV.read(file.path).count - 1  # Minus header
    end
  end
end
```

---

## Comprehensive Service Template

```ruby
# app/services/tasks_manager/create_task.rb
module TasksManager
  class CreateTask < ApplicationService
    include Services::Concerns::ErrorHandling
    include Services::Concerns::Retriable
    include Services::Concerns::Loggable
    include Services::Concerns::Metrics
    include Services::Concerns::ErrorTracking

    def initialize(account:, merchant:, params:, user:)
      @account = account
      @merchant = merchant
      @params = params
      @user = user
    end

    def call
      log_service_start(account_id: @account.id, merchant_id: @merchant.id)
      start_time = Time.current

      validate_authorization!
      validate_params!

      task = with_retry(max_attempts: 3) do
        build_and_save_task
      end

      track_counter("task.created", tags: { merchant_id: @merchant.id })
      duration = (Time.current - start_time) * 1000
      track_timing("task.creation_time", duration)

      log_service_complete(ServiceResult.success(task), duration_ms: duration)

      ServiceResult.success(task)
    rescue Services::Errors::ServiceError => e
      capture_exception(e, context: { account_id: @account.id })
      ServiceResult.failure(e.message, context: e.context)
    rescue StandardError => e
      log_error("Unexpected error", error: e.message, backtrace: e.backtrace.first(5))
      capture_exception(e, context: { account_id: @account.id })
      ServiceResult.failure("An unexpected error occurred")
    end

    private

    attr_reader :account, :merchant, :params, :user

    def validate_authorization!
      unless user.can?(:create_task, account)
        raise Services::Errors::AuthorizationError.new(
          "User not authorized",
          context: { user_id: user.id, account_id: account.id }
        )
      end
    end

    def validate_params!
      errors = []
      errors << "Recipient required" unless params[:recipient_id]
      errors << "Address required" unless params[:address]

      if errors.any?
        raise Services::Errors::ValidationError.new(
          "Validation failed",
          context: { errors: errors }
        )
      end
    end

    def build_and_save_task
      ActiveRecord::Base.transaction do
        task = account.tasks.build(
          merchant: merchant,
          recipient_id: params[:recipient_id],
          description: params[:description],
          amount: params[:amount],
          status: 'pending'
        )

        assign_zone(task)
        task.save!

        log_info("Task created", task_id: task.id)
        schedule_notifications(task)

        task
      end
    end

    def assign_zone(task)
      zone = ZoneFinder.new(account, params[:address]).find
      task.zone = zone
      log_debug("Zone assigned", zone_id: zone&.id)
    end

    def schedule_notifications(task)
      TaskNotificationJob.perform_later(task.id)
      log_debug("Notifications scheduled", task_id: task.id)
    end
  end
end
```
