# Service Specs Reference

## Basic Service Spec

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

      it 'schedules notification job' do
        expect { service_call }
          .to have_enqueued_job(TaskNotificationJob)
                .with(kind_of(Integer))
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

---

## Testing ServiceResult Pattern

```ruby
describe '.call' do
  subject(:result) { described_class.call(params) }

  context 'on success' do
    it 'returns success result' do
      expect(result).to be_success
    end

    it 'includes the task in data' do
      expect(result.data).to be_a(Task)
    end
  end

  context 'on failure' do
    let(:params) { invalid_params }

    it 'returns failure result' do
      expect(result).to be_failure
    end

    it 'includes error message' do
      expect(result.error).to eq("Expected error message")
    end

    it 'includes validation errors' do
      expect(result.errors).to include("Recipient required")
    end
  end
end
```

---

## Testing External API Calls

```ruby
RSpec.describe Integrations::Shipping::CreateLabel do
  let(:task) { create(:task) }
  let(:shipping_company) { create(:shipping_company) }

  describe '.call' do
    context 'when API succeeds' do
      before do
        stub_request(:post, "#{shipping_company.api_url}/labels")
          .to_return(
            status: 200,
            body: { tracking_number: "TRACK123", label_url: "https://..." }.to_json,
            headers: { 'Content-Type' => 'application/json' }
          )
      end

      it 'returns success with label' do
        result = described_class.call(task: task, shipping_company: shipping_company)

        expect(result).to be_success
        expect(result.data.tracking_number).to eq("TRACK123")
      end
    end

    context 'when API times out' do
      before do
        stub_request(:post, "#{shipping_company.api_url}/labels").to_timeout
      end

      it 'returns failure' do
        result = described_class.call(task: task, shipping_company: shipping_company)

        expect(result).to be_failure
        expect(result.error).to eq("Shipping API timeout")
      end
    end

    context 'when API returns error' do
      before do
        stub_request(:post, "#{shipping_company.api_url}/labels")
          .to_return(status: 422, body: { error: "Invalid address" }.to_json)
      end

      it 'returns failure with error message' do
        result = described_class.call(task: task, shipping_company: shipping_company)

        expect(result).to be_failure
        expect(result.error).to eq("Invalid address")
      end
    end
  end
end
```

---

## Testing Transaction Rollback

```ruby
describe 'transaction handling' do
  context 'when second step fails' do
    before do
      allow(NotificationService).to receive(:notify).and_raise(StandardError)
    end

    it 'rolls back the task creation' do
      expect {
        described_class.call(params) rescue nil
      }.not_to change(Task, :count)
    end
  end
end
```
