---
name: rspec-testing-patterns
description: Use this skill when writing tests for Ruby on Rails applications with RSpec, including unit, integration, and system tests, as well as setting up test infrastructure.
---

# RSpec Testing Patterns

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
```