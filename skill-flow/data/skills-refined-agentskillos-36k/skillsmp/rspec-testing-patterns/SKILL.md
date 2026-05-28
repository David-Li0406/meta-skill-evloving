---
name: "RSpec Testing Patterns"
description: "Complete guide to testing Ruby on Rails applications with RSpec. Use when: (1) Writing unit tests, integration tests, system tests, (2) Setting up test factories, (3) Creating shared examples, (4) Mocking external services, (5) Testing ViewComponents and background jobs. Trigger keywords: tests, specs, RSpec, TDD, testing, test coverage, FactoryBot, fixtures, mocks, stubs, shoulda-matchers"
version: 1.1.0
---

# RSpec Testing Patterns

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

---

## NEVER Do This

**NEVER** use `create` when `build` works:
```ruby
# WRONG - unnecessary DB writes
it 'validates presence of email' do
  user = create(:user, email: nil)
  expect(user.valid?).to be false
end

# RIGHT - use build for validation tests
it 'validates presence of email' do
  user = build(:user, email: nil)
  expect(user.valid?).to be false
end
```

**NEVER** test implementation, test behavior:
```ruby
# WRONG - testing implementation details
it 'calls private method' do
  expect(service).to receive(:calculate_total)
  service.call
end

# RIGHT - test observable behavior
it 'returns correct total' do
  result = service.call
  expect(result.total).to eq(100)
end
```

**NEVER** use mystery guests (undefined variables):
```ruby
# WRONG - where does user come from?
it 'creates task for user' do
  task = TasksManager::CreateTask.call(user: user)
  expect(task.user).to eq(user)
end

# RIGHT - explicit setup with let
let(:user) { create(:user) }

it 'creates task for user' do
  task = TasksManager::CreateTask.call(user: user)
  expect(task.user).to eq(user)
end
```

**NEVER** skip testing edge cases:
```ruby
# WRONG - only happy path
describe '.call' do
  it 'creates task' do
    expect { service.call }.to change(Task, :count).by(1)
  end
end

# RIGHT - cover failure cases too
describe '.call' do
  context 'with valid params' do
    it 'creates task' do
      expect { service.call }.to change(Task, :count).by(1)
    end
  end

  context 'with invalid params' do
    it 'raises error' do
      expect { service.call(nil) }.to raise_error(ArgumentError)
    end
  end

  context 'when external API fails' do
    before { stub_api_failure }

    it 'returns failure result' do
      expect(service.call).to be_failure
    end
  end
end
```

**NEVER** forget cleanup in `before` blocks:
```ruby
# WRONG - state leaks between tests
before(:all) do
  @user = create(:user)
end

# RIGHT - use transactional fixtures or per-test setup
let(:user) { create(:user) }
```

---

## Directory Structure

```
spec/
├── rails_helper.rb
├── spec_helper.rb
├── support/
│   ├── factory_bot.rb
│   ├── shared_contexts/
│   └── shared_examples/
├── factories/
├── models/
├── services/
├── requests/
├── system/
├── components/
└── jobs/
```

---

## FactoryBot Quick Reference

| Method | Use Case |
|--------|----------|
| `build(:task)` | In-memory, no DB |
| `create(:task)` | Persisted to DB |
| `build_stubbed(:task)` | Fake ID, no DB |
| `attributes_for(:task)` | Hash of attributes |

```ruby
# Traits
create(:task, :completed, :express)

# Override attributes
create(:task, status: 'cancelled')

# Transient attributes
create(:bundle, task_count: 10)
```

---

## Shoulda Matchers Quick Reference

### Associations
```ruby
it { is_expected.to belong_to(:account) }
it { is_expected.to have_many(:tasks).dependent(:destroy) }
it { is_expected.to have_one(:profile) }
```

### Validations
```ruby
it { is_expected.to validate_presence_of(:email) }
it { is_expected.to validate_uniqueness_of(:email).case_insensitive }
it { is_expected.to validate_length_of(:password).is_at_least(8) }
it { is_expected.to validate_numericality_of(:amount).is_greater_than(0) }
```

### Enums
```ruby
it { is_expected.to define_enum_for(:status).with_values([:pending, :active]) }
```

---

## Common Matchers

| Matcher | Example |
|---------|---------|
| Change count | `expect { }.to change(Task, :count).by(1)` |
| Raise error | `expect { }.to raise_error(ArgumentError)` |
| Enqueue job | `expect { }.to have_enqueued_job(NotifyJob)` |
| Include | `expect(result).to include('success')` |
| Match | `expect(json).to match(hash_including(id: 1))` |
| Be truthy | `expect(result.success?).to be true` |

---

## Request Spec Pattern

```ruby
RSpec.describe "Api::V1::Tasks", type: :request do
  let(:user) { create(:user) }
  let(:headers) { auth_headers(user) }

  describe "POST /api/v1/tasks" do
    let(:params) { { task: { title: "New" } } }

    it "creates task" do
      expect {
        post api_v1_tasks_path, params: params, headers: headers
      }.to change(Task, :count).by(1)

      expect(response).to have_http_status(:created)
    end
  end

  def json_response
    JSON.parse(response.body)
  end
end
```

---

## System Spec Pattern

```ruby
RSpec.describe "Tasks", type: :system do
  before { driven_by(:selenium_chrome_headless) }

  let(:user) { create(:user) }

  before { sign_in(user) }

  it "creates task with Turbo" do
    visit tasks_path

    fill_in "Title", with: "New Task"
    click_button "Create"

    expect(page).to have_content("New Task")
    expect(page).to have_current_path(tasks_path) # No redirect
  end
end
```

---

## Service Spec Pattern

```ruby
RSpec.describe TasksManager::CreateTask do
  let(:account) { create(:account) }
  let(:params) { { title: "Test" } }

  describe '.call' do
    subject(:result) { described_class.call(account: account, params: params) }

    context 'with valid params' do
      it { is_expected.to be_success }
      it { expect(result.data).to be_a(Task) }
    end

    context 'with invalid params' do
      let(:params) { {} }

      it { is_expected.to be_failure }
      it { expect(result.error).to include("required") }
    end
  end
end
```

---

## Testing Async Jobs

```ruby
# Test enqueuing
expect { service.call }.to have_enqueued_job(NotifyJob).with(task.id)

# Test execution
described_class.perform_now(task.id)
expect(task.reload.notified?).to be true

# Test inline
perform_enqueued_jobs { service.call }
expect(Notification.count).to eq(1)
```

---

## Mocking External APIs

```ruby
before do
  stub_request(:post, "https://api.example.com/endpoint")
    .to_return(status: 200, body: { success: true }.to_json)
end

# Test timeout
stub_request(:post, url).to_timeout

# Test error
stub_request(:post, url).to_return(status: 500)
```

---

## Configuration

```ruby
# spec/rails_helper.rb
RSpec.configure do |config|
  config.include FactoryBot::Syntax::Methods
  config.use_transactional_fixtures = true
  config.infer_spec_type_from_file_location!
end

Shoulda::Matchers.configure do |config|
  config.integrate do |with|
    with.test_framework :rspec
    with.library :rails
  end
end
```

---

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
