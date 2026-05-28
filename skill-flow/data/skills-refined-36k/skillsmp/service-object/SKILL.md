---
name: service-object
description: Generate service objects for complex business logic. Use when controller/model is too fat, multiple models interaction, external API calls, or says "extract logic", "create service", "business logic", "refactor controller", "complex operation".
---

# Service Object Generator

Extract complex business logic into service objects for better organization and testability.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Identify complex logic to extract
- [ ] 2. Create service class
- [ ] 3. Move business logic to service
- [ ] 4. Add error handling
- [ ] 5. Call from controller/model
- [ ] 6. Add tests
```

## When to Use Service Objects

✅ **Good candidates**:
- Complex multi-step operations
- Multiple model interactions
- External API integration
- Business logic with many conditionals
- Operations requiring transactions
- Reusable business processes

❌ **Don't use for**:
- Simple CRUD operations
- Single model validations
- View helpers

## Service Structure

```
app/services/
├── application_service.rb    # Base class
├── users/
│   ├── create_user_service.rb
│   ├── update_profile_service.rb
│   └── delete_account_service.rb
├── posts/
│   ├── publish_post_service.rb
│   └── archive_post_service.rb
└── payments/
    ├── process_payment_service.rb
    └── refund_service.rb
```

## Base Service Class

```ruby
# app/services/application_service.rb
class ApplicationService
  def self.call(*args, **kwargs, &block)
    new(*args, **kwargs).call(&block)
  end

  private

  attr_reader :errors

  def initialize
    @errors = []
  end

  def success?
    errors.empty?
  end

  def failure?
    !success?
  end

  def add_error(message)
    @errors << message
  end
end
```

## Basic Service Template

```ruby
# app/services/example_service.rb
class ExampleService < ApplicationService
  def initialize(param1, param2)
    super()
    @param1 = param1
    @param2 = param2
  end

  def call
    validate_inputs
    return self if failure?

    perform_operation

    self
  end

  private

  attr_reader :param1, :param2

  def validate_inputs
    add_error("Param1 is required") if param1.blank?
    add_error("Param2 must be positive") if param2 <= 0
  end

  def perform_operation
    # Business logic here
  end
end
```

**Usage**:
```ruby
# In controller
service = ExampleService.call(value1, value2)

if service.success?
  redirect_to root_path, notice: "Success"
else
  flash[:alert] = service.errors.join(", ")
  render :new
end
```

## Common Patterns

### 1. User Registration Service

```ruby
# app/services/users/register_user_service.rb
module Users
  class RegisterUserService < ApplicationService
    def initialize(user_params, ip_address)
      super()
      @user_params = user_params
      @ip_address = ip_address
      @user = nil
    end

    def call
      ActiveRecord::Base.transaction do
        create_user
        return self if failure?

        setup_defaults
        send_welcome_email
        log_registration
      end

      self
    rescue StandardError => e
      add_error("Registration failed: #{e.message}")
      self
    end

    attr_reader :user

    private

    def create_user
      @user = User.new(@user_params)

      unless @user.save
        @user.errors.full_messages.each { |msg| add_error(msg) }
      end
    end

    def setup_defaults
      @user.create_profile!
      @user.update!(last_login_ip: @ip_address)
    end

    def send_welcome_email
      UserMailer.welcome_email(@user).deliver_later
    end

    def log_registration
      Rails.logger.info "New user registered: #{@user.id} from #{@ip_address}"
    end
  end
end
```

**Controller**:
```ruby
class RegistrationsController < ApplicationController
  def create
    service = Users::RegisterUserService.call(
      user_params,
      request.remote_ip
    )

    if service.success?
      session[:user_id] = service.user.id
      redirect_to root_path, notice: "Welcome!"
    else
      flash.now[:alert] = service.errors.join(", ")
      render :new
    end
  end
end
```

### 2. Post Publishing Service

```ruby
# app/services/posts/publish_post_service.rb
module Posts
  class PublishPostService < ApplicationService
    def initialize(post, user)
      super()
      @post = post
      @user = user
    end

    def call
      check_permissions
      return self if failure?

      validate_post_content
      return self if failure?

      publish_post
      notify_followers
      update_user_stats

      self
    end

    private

    def check_permissions
      unless @post.user == @user
        add_error("You don't have permission to publish this post")
      end
    end

    def validate_post_content
      add_error("Title is required") if @post.title.blank?
      add_error("Content is too short") if @post.content.length < 10
    end

    def publish_post
      @post.update!(
        status: :published,
        published_at: Time.current
      )
    end

    def notify_followers
      @user.followers.find_each do |follower|
        Notification.create!(
          user: follower,
          notifiable: @post,
          content: "#{@user.name} published a new post"
        )
      end
    end

    def update_user_stats
      @user.increment!(:posts_count)
    end
  end
end
```

### 3. Payment Processing Service

```ruby
# app/services/payments/process_payment_service.rb
module Payments
  class ProcessPaymentService < ApplicationService
    def initialize(order, payment_params)
      super()
      @order = order
      @payment_params = payment_params
      @payment = nil
    end

    def call
      validate_order
      return self if failure?

      ActiveRecord::Base.transaction do
        create_payment_record
        charge_payment_gateway
        return self if failure?

        fulfill_order
        send_receipt
      end

      self
    rescue StandardError => e
      add_error("Payment processing failed: #{e.message}")
      @payment&.update(status: :failed)
      self
    end

    attr_reader :payment

    private

    def validate_order
      add_error("Order already paid") if @order.paid?
      add_error("Order amount is invalid") if @order.amount <= 0
    end

    def create_payment_record
      @payment = @order.payments.create!(
        amount: @order.amount,
        payment_method: @payment_params[:method],
        status: :pending
      )
    end

    def charge_payment_gateway
      # External API call
      result = StripeService.charge(
        amount: @order.amount,
        token: @payment_params[:token]
      )

      if result.success?
        @payment.update!(
          status: :completed,
          transaction_id: result.transaction_id
        )
      else
        add_error(result.error_message)
        @payment.update!(status: :failed)
      end
    end

    def fulfill_order
      @order.update!(
        status: :paid,
        paid_at: Time.current
      )
    end

    def send_receipt
      OrderMailer.receipt_email(@order).deliver_later
    end
  end
end
```

### 4. Data Import Service

```ruby
# app/services/imports/import_users_service.rb
module Imports
  class ImportUsersService < ApplicationService
    def initialize(file)
      super()
      @file = file
      @success_count = 0
      @failed_count = 0
      @failed_rows = []
    end

    def call
      validate_file
      return self if failure?

      process_file

      log_results
      self
    end

    attr_reader :success_count, :failed_count, :failed_rows

    private

    def validate_file
      add_error("File is required") unless @file.present?
      add_error("Invalid file format") unless valid_csv?
    end

    def valid_csv?
      @file.path.end_with?(".csv")
    end

    def process_file
      CSV.foreach(@file.path, headers: true).with_index(1) do |row, line_number|
        process_row(row, line_number)
      end
    end

    def process_row(row, line_number)
      User.create!(
        email: row["email"],
        name: row["name"],
        role_title: row["role"]
      )

      @success_count += 1
    rescue StandardError => e
      @failed_count += 1
      @failed_rows << { line: line_number, error: e.message }
    end

    def log_results
      Rails.logger.info "Import completed: #{@success_count} success, #{@failed_count} failed"
    end
  end
end
```

## Result Object Pattern

```ruby
# app/services/result.rb
class ServiceResult
  attr_reader :success, :data, :errors

  def initialize(success:, data: nil, errors: [])
    @success = success
    @data = data
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

  def self.failure(errors)
    new(success: false, errors: Array(errors))
  end
end
```

**Service with Result**:
```ruby
class ModernService
  def self.call(*args)
    new(*args).call
  end

  def call
    # Logic here

    if condition
      ServiceResult.success(data: @result)
    else
      ServiceResult.failure("Error message")
    end
  end
end
```

**Usage**:
```ruby
result = ModernService.call(params)

if result.success?
  @data = result.data
  render :success
else
  @errors = result.errors
  render :error
end
```

## Testing

```ruby
# test/services/users/register_user_service_test.rb
require "test_helper"

module Users
  class RegisterUserServiceTest < ActiveSupport::TestCase
    test "successfully registers user with valid params" do
      params = {
        email: "test@example.com",
        name: "Test User",
        password: "password"
      }

      service = RegisterUserService.call(params, "127.0.0.1")

      assert service.success?
      assert_not_nil service.user
      assert_equal "test@example.com", service.user.email
    end

    test "fails with invalid email" do
      params = {
        email: "invalid",
        name: "Test",
        password: "password"
      }

      service = RegisterUserService.call(params, "127.0.0.1")

      assert service.failure?
      assert_includes service.errors.join, "Email"
    end

    test "sends welcome email" do
      params = {
        email: "test@example.com",
        name: "Test",
        password: "password"
      }

      assert_enqueued_with(job: ActionMailer::MailDeliveryJob) do
        RegisterUserService.call(params, "127.0.0.1")
      end
    end

    test "rolls back on error" do
      # Stub to raise error
      UserMailer.stub :welcome_email, -> { raise "Email error" } do
        assert_no_difference "User.count" do
          RegisterUserService.call(valid_params, "127.0.0.1")
        end
      end
    end
  end
end
```

## Best Practices

1. **Single Responsibility**: One service = one business operation
2. **Immutable Inputs**: Don't modify input parameters
3. **Return Self**: Always return self or result object
4. **Error Collection**: Collect all errors, don't raise
5. **Transaction Safety**: Use transactions for multi-model operations
6. **Logging**: Log important business events
7. **Testing**: Test happy path and all error scenarios

## Integration Examples

### From Controller
```ruby
class PostsController < ApplicationController
  def publish
    @post = Post.find(params[:id])
    service = Posts::PublishPostService.call(@post, current_user)

    if service.success?
      redirect_to @post, notice: "Post published successfully"
    else
      redirect_to @post, alert: service.errors.join(", ")
    end
  end
end
```

### From Model Callback
```ruby
class Order < ApplicationRecord
  after_commit :process_payment, on: :create

  private

  def process_payment
    Payments::ProcessPaymentService.call(self, payment_info)
  end
end
```

### From Background Job
```ruby
class ProcessOrderJob < ApplicationJob
  def perform(order_id)
    order = Order.find(order_id)
    service = Orders::ProcessOrderService.call(order)

    unless service.success?
      Rails.logger.error "Order processing failed: #{service.errors.join(', ')}"
    end
  end
end
```

## Checklist

- [ ] Service class created in app/services/
- [ ] Inherits from ApplicationService
- [ ] Single responsibility
- [ ] Returns self or result object
- [ ] Error handling implemented
- [ ] Transactions for multi-model ops
- [ ] Tested thoroughly
- [ ] Logged important events
- [ ] Called from appropriate location
