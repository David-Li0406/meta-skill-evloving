---
id: ruby-rails-patterns
name: "Rails Patterns"
domain: RUBY
skill: faion-software-developer
category: "backend"
---

## Rails Patterns

### Problem
Structure Rails applications for scalability and maintainability.

### Framework: Service Objects

```ruby
# app/services/users/create_service.rb
module Users
  class CreateService
    def initialize(params:, current_user: nil)
      @params = params
      @current_user = current_user
    end

    def call
      user = User.new(user_params)

      ActiveRecord::Base.transaction do
        user.save!
        send_welcome_email(user)
        create_audit_log(user)
      end

      ServiceResult.success(user)
    rescue ActiveRecord::RecordInvalid => e
      ServiceResult.failure(e.record.errors.full_messages)
    end

    private

    def user_params
      @params.slice(:name, :email, :password)
    end

    def send_welcome_email(user)
      UserMailer.welcome(user).deliver_later
    end

    def create_audit_log(user)
      AuditLog.create!(
        action: 'user.created',
        resource: user,
        actor: @current_user
      )
    end
  end
end

# app/services/service_result.rb
class ServiceResult
  attr_reader :data, :errors

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

### Controller Usage

```ruby
# app/controllers/api/v1/users_controller.rb
module Api
  module V1
    class UsersController < ApplicationController
      def create
        result = Users::CreateService.new(
          params: user_params,
          current_user: current_user
        ).call

        if result.success?
          render json: UserSerializer.new(result.data), status: :created
        else
          render json: { errors: result.errors }, status: :unprocessable_entity
        end
      end

      private

      def user_params
        params.require(:user).permit(:name, :email, :password)
      end
    end
  end
end
```

### Agent

faion-backend-agent
