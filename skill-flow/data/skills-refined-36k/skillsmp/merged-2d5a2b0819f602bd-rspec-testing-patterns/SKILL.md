---
name: rspec-testing-patterns
description: Use this skill when writing unit tests, integration tests, system tests, or when setting up test infrastructure including factories, shared examples, and mocking strategies for Ruby on Rails applications with RSpec.
---

# RSpec Testing Patterns

This skill provides comprehensive guidance for testing Rails applications with RSpec.

## When to Use This Skill

- Writing new specs (unit, integration, system)
- Setting up test factories
- Creating shared examples
- Mocking external services
- Testing ViewComponents
- Testing background jobs

## Test Type Decision Tree

```
What am I testing?
│
├─ Model validations/associations/scopes?
│   └─ Model Spec (spec/models/)
│       └─ Use shoulda-matchers
│
├─ Service object business logic?
│   └─ Service Spec (spec/services/)
│       └─ Test inputs, outputs, side effects
│
├─ API endpoint behavior?
│   └─ Request Spec (spec/requests/)
│       └─ Test HTTP responses, JSON structure
│
├─ Full user flow with browser?
│   └─ System Spec (spec/system/)
│       └─ Use Capybara + Selenium
│
├─ ViewComponent rendering?
│   └─ Component Spec (spec/components/)
│       └─ Use render_inline
│
├─ Background job?
│   └─ Job Spec (spec/jobs/)
│       └─ Test perform + enqueuing
│
└─ Controller logic? (rare)
    └─ Request Spec preferred
```

## Directory Structure

```
spec/
├── rails_helper.rb
├── spec_helper.rb
├── support/
│   ├── factory_bot.rb
│   ├── database_cleaner.rb
│   ├── shared_contexts/
│   └── shared_examples/
├── factories/
│   ├── tasks.rb
│   ├── users.rb
│   └── ...
├── models/
├── services/
├── controllers/
├── requests/
├── system/
├── components/
└── jobs/
```

## Basic Spec Structure

```ruby
# spec/models/task_spec.rb
require 'rails_helper'

RSpec.describe Task, type: :model do
  describe 'associations' do
    it { is_expected.to belong_to(:account) }
    it { is_expected.to belong_to(:merchant) }
    it { is_expected.to have_many(:timelines) }
  end

  describe 'validations' do
    it { is_expected.to validate_presence_of(:status) }
    it { is_expected.to validate_inclusion_of(:status).in_array(Task::STATUSES) }
  end

  describe 'scopes' do
    describe '.active' do
      let!(:pending_task) { create(:task, status: 'pending') }
      let!(:completed_task) { create(:task, status: 'completed') }

      it 'returns only non-completed tasks' do
        expect(Task.active).to include(pending_task)
        expect(Task.active).not_to include(completed_task)
      end
    end
  end

  describe '#completable?' do
    context 'when task is pending' do
      let(:task) { build(:task, status: 'pending') }

      it 'returns true' do
        expect(task.completable?).to be true
      end
    end

    context 'when task is completed' do
      let(:task) { build(:task, status: 'completed') }

      it 'returns false' do
        expect(task.completable?).to be false
      end
    end
  end
end
```

## FactoryBot Quick Reference

| Method | Use Case |
|--------|----------|
| `build(:task)` | In-memory, no DB |
| `create(:task)` | Persisted to DB |
| `build_stubbed(:task)` | Fake ID, no DB |
| `attributes_for(:task)` | Hash of attributes |

### Basic Factory Example

```ruby
# spec/factories/tasks.rb
FactoryBot.define do
  factory :task do
    account
    merchant
    recipient

    sequence(:tracking_number) { |n| "TRK#{n.to_s.rjust(8, '0')}" }
    status { 'pending' }
    description { Faker::Lorem.sentence }
    amount { Faker::Number.decimal(l_digits: 2, r_digits: 2) }

    # Traits
    trait :completed do
      status { 'completed' }
      completed_at { Time.current }
      carrier
    end

    # Callbacks
    after(:create) do |task|
      task.timelines.create!(status: task.status, created_at: task.created_at)
    end
  end
end
```

## Service Specs

```ruby
# spec/services/tasks_manager/create_task_spec.rb
require 'rails_helper'

RSpec.describe TasksManager::CreateTask do
  let(:account) { create(:account) }
  let(:merchant) { create(:merchant, account: account) }
  let(:recipient) { create(:recipient, account: account) }

  let(:valid_params) do
    {
      recipient_id: recipient.id,
      description: "Test delivery",
      amount: 100.00,
      address: "123 Test St"
    }
  end

  describe '.call' do
    subject(:service_call) do
      described_class.call(
        account: account,
        merchant: merchant,
        params: valid_params
      )
    end

    context 'with valid params' do
      it 'creates a task' do
        expect { service_call }.to change(Task, :count).by(1)
      end

      it 'returns the created task' do
        expect(service_call).to be_a(Task)
        expect(service_call).to be_persisted
      end

      it 'associates with correct account' do
        expect(service_call.account).to eq(account)
      end
    end

    context 'with invalid params' do
      context 'when recipient is missing' do
        let(:valid_params) { super().except(:recipient_id) }

        it 'raises ArgumentError' do
          expect { service_call }.to raise_error(ArgumentError, /Recipient required/)
        end
      end
    end
  end
end
```

## Request Specs

```ruby
# spec/requests/api/v1/tasks_spec.rb
require 'rails_helper'

RSpec.describe "Api::V1::Tasks", type: :request do
  let(:account) { create(:account) }
  let(:user) { create(:user, account: account) }
  let(:headers) { auth_headers(user) }

  describe "GET /api/v1/tasks" do
    let!(:tasks) { create_list(:task, 3, account: account) }
    let!(:other_task) { create(:task) }  # Different account

    before { get api_v1_tasks_path, headers: headers }

    it "returns success" do
      expect(response).to have_http_status(:ok)
    end

    it "returns tasks for current account only" do
      expect(json_response['data'].size).to eq(3)
    end
  end
end
```

## System Specs (Capybara)

```ruby
# spec/system/tasks_spec.rb
require 'rails_helper'

RSpec.describe "Tasks", type: :system do
  let(:account) { create(:account) }
  let(:user) { create(:user, account: account) }

  before do
    sign_in(user)
  end

  describe "viewing tasks" do
    let!(:tasks) { create_list(:task, 5, account: account) }

    it "displays all tasks" do
      visit tasks_path

      tasks.each do |task|
        expect(page).to have_content(task.tracking_number)
      end
    end
  end
end
```

## Job Specs

```ruby
# spec/jobs/task_notification_job_spec.rb
require 'rails_helper'

RSpec.describe TaskNotificationJob, type: :job do
  let(:task) { create(:task) }

  describe "#perform" do
    it "sends SMS notification" do
      expect(SmsService).to receive(:send).with(
        to: task.recipient.phone,
        message: include(task.tracking_number)
      )

      described_class.perform_now(task.id)
    end
  end
end
```

## Mocking External Services

```ruby
# spec/support/webmock_helpers.rb
module WebmockHelpers
  def stub_shipping_api_success
    stub_request(:post, "https://shipping.example.com/api/labels")
      .to_return(
        status: 200,
        body: { tracking_number: "SHIP123", label_url: "https://..." }.to_json,
        headers: { 'Content-Type' => 'application/json' }
      )
  end
end

RSpec.configure do |config|
  config.include WebmockHelpers
end
```

## Configuration

```ruby
# spec/rails_helper.rb
require 'spec_helper'
ENV['RAILS_ENV'] ||= 'test'
require_relative '../config/environment'

abort("Running in production!") if Rails.env.production?

require 'rspec/rails'

Dir[Rails.root.join('spec/support/**/*.rb')].sort.each { |f| require f }

RSpec.configure do |config|
  config.fixture_path = Rails.root.join('spec/fixtures')
  config.use_transactional_fixtures = true
  config.infer_spec_type_from_file_location!
  config.filter_rails_from_backtrace!

  # FactoryBot
  config.include FactoryBot::Syntax::Methods
end
```

## References

Detailed patterns and examples in `references/`:
- `factories.md` - FactoryBot patterns, traits, transients
- `model-specs.md` - Shoulda matchers, callbacks, scopes
- `request-specs.md` - API testing, pagination, rate limiting
- `system-specs.md` - Capybara, Turbo testing
- `service-specs.md` - Service object testing patterns
- `shared-examples.md` - Shared examples and contexts
- `component-job-specs.md` - ViewComponent and job testing
- `helpers-mocking.md` - Test helpers, WebMock, VCR