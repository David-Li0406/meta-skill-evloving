# Result Object Patterns Reference

## ServiceResult Class

```ruby
# app/services/service_result.rb
class ServiceResult
  attr_reader :data, :error, :errors

  def initialize(success:, data: nil, error: nil, errors: [])
    @success = success
    @data = data
    @error = error
    @errors = errors
  end

  def success?
    @success
  end

  def failure?
    !@success
  end

  def self.success(data = nil)
    new(success: true, data: data)
  end

  def self.failure(error = nil, errors: [])
    new(success: false, error: error, errors: errors)
  end
end
```

---

## Usage in Services

```ruby
# app/services/tasks_manager/assign_carrier.rb
module TasksManager
  class AssignCarrier < ApplicationService
    def initialize(task:, carrier:)
      @task = task
      @carrier = carrier
    end

    def call
      return ServiceResult.failure("Task already assigned") if task.carrier.present?
      return ServiceResult.failure("Carrier not available") unless carrier_available?
      return ServiceResult.failure("Carrier not in zone") unless carrier_in_zone?

      ActiveRecord::Base.transaction do
        task.update!(carrier: carrier, assigned_at: Time.current)
        notify_carrier
        notify_recipient
      end

      ServiceResult.success(task.reload)
    rescue ActiveRecord::RecordInvalid => e
      ServiceResult.failure(e.message, errors: task.errors.full_messages)
    end

    private

    attr_reader :task, :carrier

    def carrier_available?
      carrier.active? && carrier.available?
    end

    def carrier_in_zone?
      return true unless task.zone
      carrier.zones.include?(task.zone)
    end

    def notify_carrier
      CarrierNotificationJob.perform_later(carrier.id, task.id)
    end

    def notify_recipient
      RecipientNotificationJob.perform_later(task.id, :carrier_assigned)
    end
  end
end
```

---

## Controller Usage

```ruby
result = TasksManager::AssignCarrier.call(task: @task, carrier: @carrier)

if result.success?
  render json: result.data, status: :ok
else
  render json: { error: result.error, errors: result.errors }, status: :unprocessable_entity
end
```

---

## Dry-Monads Pattern (Alternative)

```ruby
# Gemfile
gem 'dry-monads'

# app/services/tasks_manager/complete_task.rb
module TasksManager
  class CompleteTask
    include Dry::Monads[:result, :do]

    def initialize(task:, otp:, photos: [])
      @task = task
      @otp = otp
      @photos = photos
    end

    def call
      yield validate_otp
      yield validate_photos
      yield complete_task
      yield process_payment
      yield notify_parties

      Success(task.reload)
    end

    private

    attr_reader :task, :otp, :photos

    def validate_otp
      return Failure(:invalid_otp) unless task.otp == otp
      Success()
    end

    def validate_photos
      return Failure(:photos_required) if task.requires_photos? && photos.empty?
      Success()
    end

    def complete_task
      task.update!(
        status: 'completed',
        completed_at: Time.current
      )
      Success()
    rescue ActiveRecord::RecordInvalid => e
      Failure(e.message)
    end

    def process_payment
      # Payment processing logic
      Success()
    end

    def notify_parties
      TaskCompletionNotificationJob.perform_later(task.id)
      Success()
    end
  end
end
```

---

## Pattern Matching with Dry-Monads

```ruby
result = TasksManager::CompleteTask.new(task: @task, otp: params[:otp]).call

case result
in Success(task)
  render json: task
in Failure(:invalid_otp)
  render json: { error: "Invalid OTP" }, status: :unprocessable_entity
in Failure(error)
  render json: { error: error }, status: :unprocessable_entity
end
```

---

## Enhanced Result with Context

```ruby
class ServiceResult
  attr_reader :data, :error, :errors, :context

  def initialize(success:, data: nil, error: nil, errors: [], context: {})
    @success = success
    @data = data
    @error = error
    @errors = errors
    @context = context
  end

  def success?
    @success
  end

  def failure?
    !@success
  end

  def self.success(data = nil, context: {})
    new(success: true, data: data, context: context)
  end

  def self.failure(error = nil, errors: [], context: {})
    new(success: false, error: error, errors: errors, context: context)
  end

  # Chain methods for fluent API
  def on_success
    yield data if success?
    self
  end

  def on_failure
    yield error, errors if failure?
    self
  end
end

# Usage
result = MyService.call(params)
result
  .on_success { |data| redirect_to data }
  .on_failure { |error, errors| render :new }
```
