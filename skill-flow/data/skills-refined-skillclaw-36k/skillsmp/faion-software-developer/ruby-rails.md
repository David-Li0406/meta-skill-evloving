# Ruby on Rails Backend Development

**Ruby backend patterns for production-grade applications with Rails and Sidekiq.**

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

---

## ActiveRecord Patterns

### Problem
Efficient database access with proper query optimization.

### Framework: Query Objects

```ruby
# app/queries/users_query.rb
class UsersQuery
  def initialize(relation = User.all)
    @relation = relation
  end

  def active
    @relation = @relation.where(active: true)
    self
  end

  def with_role(role)
    @relation = @relation.where(role: role)
    self
  end

  def created_after(date)
    @relation = @relation.where('created_at > ?', date)
    self
  end

  def search(term)
    return self if term.blank?
    @relation = @relation.where(
      'name ILIKE :term OR email ILIKE :term',
      term: "%#{term}%"
    )
    self
  end

  def ordered
    @relation = @relation.order(created_at: :desc)
    self
  end

  def with_associations
    @relation = @relation.includes(:profile, :roles)
    self
  end

  def paginate(page:, per_page: 20)
    @relation = @relation.page(page).per(per_page)
    self
  end

  def results
    @relation
  end
end

# Usage
users = UsersQuery.new
  .active
  .with_role('admin')
  .search(params[:q])
  .with_associations
  .ordered
  .paginate(page: params[:page])
  .results
```

### Scopes and Callbacks

```ruby
# app/models/user.rb
class User < ApplicationRecord
  # Associations
  has_one :profile, dependent: :destroy
  has_many :orders, dependent: :nullify
  has_many :roles, through: :user_roles

  # Validations
  validates :email, presence: true, uniqueness: { case_sensitive: false }
  validates :name, presence: true, length: { minimum: 2, maximum: 100 }

  # Scopes
  scope :active, -> { where(active: true) }
  scope :admins, -> { joins(:roles).where(roles: { name: 'admin' }) }
  scope :recent, -> { where('created_at > ?', 30.days.ago) }

  # Callbacks
  before_validation :normalize_email
  after_create_commit :send_welcome_email

  private

  def normalize_email
    self.email = email&.downcase&.strip
  end

  def send_welcome_email
    UserMailer.welcome(self).deliver_later
  end
end
```

---

## RSpec Testing

### Problem
Write comprehensive, maintainable tests.

### Framework: Model Specs

```ruby
# spec/models/user_spec.rb
require 'rails_helper'

RSpec.describe User, type: :model do
  describe 'validations' do
    it { is_expected.to validate_presence_of(:email) }
    it { is_expected.to validate_presence_of(:name) }
    it { is_expected.to validate_uniqueness_of(:email).case_insensitive }
    it { is_expected.to validate_length_of(:name).is_at_least(2).is_at_most(100) }
  end

  describe 'associations' do
    it { is_expected.to have_one(:profile).dependent(:destroy) }
    it { is_expected.to have_many(:orders).dependent(:nullify) }
  end

  describe 'scopes' do
    describe '.active' do
      let!(:active_user) { create(:user, active: true) }
      let!(:inactive_user) { create(:user, active: false) }

      it 'returns only active users' do
        expect(User.active).to eq([active_user])
      end
    end
  end

  describe '#full_name' do
    let(:user) { build(:user, first_name: 'John', last_name: 'Doe') }

    it 'returns combined first and last name' do
      expect(user.full_name).to eq('John Doe')
    end
  end
end
```

### Service Specs

```ruby
# spec/services/users/create_service_spec.rb
require 'rails_helper'

RSpec.describe Users::CreateService do
  describe '#call' do
    subject(:service) { described_class.new(params: params) }

    context 'with valid params' do
      let(:params) { { name: 'John', email: 'john@example.com', password: 'secret123' } }

      it 'creates a user' do
        expect { service.call }.to change(User, :count).by(1)
      end

      it 'returns success result' do
        result = service.call
        expect(result).to be_success
        expect(result.data).to be_a(User)
      end

      it 'sends welcome email' do
        expect { service.call }
          .to have_enqueued_mail(UserMailer, :welcome)
      end
    end

    context 'with invalid params' do
      let(:params) { { name: '', email: 'invalid' } }

      it 'does not create a user' do
        expect { service.call }.not_to change(User, :count)
      end

      it 'returns failure result with errors' do
        result = service.call
        expect(result).to be_failure
        expect(result.errors).to include(/Email/)
      end
    end
  end
end
```

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

---

## Sources

- [Ruby on Rails Guides](https://guides.rubyonrails.org/)
- [Sidekiq Documentation](https://github.com/sidekiq/sidekiq/wiki)
