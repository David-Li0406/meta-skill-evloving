# Service Testing Patterns Reference

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
      amount: 100,
      address: "123 Test St"
    }
  end

  describe '.call' do
    context 'with valid params' do
      it 'creates a task' do
        expect {
          described_class.call(
            account: account,
            merchant: merchant,
            params: valid_params
          )
        }.to change(Task, :count).by(1)
      end

      it 'assigns the zone' do
        task = described_class.call(
          account: account,
          merchant: merchant,
          params: valid_params
        )

        expect(task.zone).to be_present
      end

      it 'schedules notification' do
        expect {
          described_class.call(
            account: account,
            merchant: merchant,
            params: valid_params
          )
        }.to have_enqueued_job(TaskNotificationJob)
      end
    end

    context 'with invalid params' do
      it 'raises error without recipient' do
        invalid_params = valid_params.except(:recipient_id)

        expect {
          described_class.call(
            account: account,
            merchant: merchant,
            params: invalid_params
          )
        }.to raise_error(ArgumentError, "Recipient required")
      end
    end
  end
end
```

---

## Testing Services with Results

```ruby
# spec/services/tasks_manager/assign_carrier_spec.rb
require 'rails_helper'

RSpec.describe TasksManager::AssignCarrier do
  let(:task) { create(:task, :pending) }
  let(:carrier) { create(:carrier, :active, :available) }

  describe '.call' do
    context 'when successful' do
      it 'returns success result' do
        result = described_class.call(task: task, carrier: carrier)

        expect(result).to be_success
        expect(result.data).to eq(task.reload)
      end

      it 'assigns carrier to task' do
        described_class.call(task: task, carrier: carrier)

        expect(task.reload.carrier).to eq(carrier)
      end
    end

    context 'when task already assigned' do
      before { task.update!(carrier: create(:carrier)) }

      it 'returns failure result' do
        result = described_class.call(task: task, carrier: carrier)

        expect(result).to be_failure
        expect(result.error).to eq("Task already assigned")
      end
    end

    context 'when carrier not available' do
      before { carrier.update!(available: false) }

      it 'returns failure result' do
        result = described_class.call(task: task, carrier: carrier)

        expect(result).to be_failure
        expect(result.error).to eq("Carrier not available")
      end
    end
  end
end
```

---

## Testing External API Services

```ruby
# spec/services/integrations/shipping/create_label_spec.rb
require 'rails_helper'

RSpec.describe Integrations::Shipping::CreateLabel do
  let(:task) { create(:task) }
  let(:shipping_company) { create(:shipping_company) }

  describe '.call' do
    context 'when API succeeds' do
      before do
        stub_request(:post, "#{shipping_company.api_url}/labels")
          .to_return(
            status: 200,
            body: {
              tracking_number: "TRACK123",
              label_url: "https://example.com/label.pdf"
            }.to_json,
            headers: { 'Content-Type' => 'application/json' }
          )
      end

      it 'returns success with label' do
        result = described_class.call(task: task, shipping_company: shipping_company)

        expect(result).to be_success
        expect(result.data.tracking_number).to eq("TRACK123")
      end

      it 'creates shipping label record' do
        expect {
          described_class.call(task: task, shipping_company: shipping_company)
        }.to change(ShippingLabel, :count).by(1)
      end
    end

    context 'when API times out' do
      before do
        stub_request(:post, "#{shipping_company.api_url}/labels")
          .to_timeout
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
          .to_return(
            status: 422,
            body: { error: "Invalid address" }.to_json,
            headers: { 'Content-Type' => 'application/json' }
          )
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

## Testing Service Composition

```ruby
# spec/services/tasks_manager/process_delivery_spec.rb
require 'rails_helper'

RSpec.describe TasksManager::ProcessDelivery do
  let(:task) { create(:task, :assigned, :cod) }
  let(:carrier) { task.carrier }
  let(:params) { { otp: task.otp, photos: [fixture_file("photo.jpg")] } }

  describe '.call' do
    it 'completes the entire delivery flow' do
      result = described_class.call(task: task, carrier: carrier, params: params)

      expect(result).to be_success
      expect(task.reload.status).to eq('completed')
    end

    it 'processes COD payment' do
      expect {
        described_class.call(task: task, carrier: carrier, params: params)
      }.to change { carrier.cod_balance }.by(task.cod_amount)
    end

    it 'generates invoice' do
      expect {
        described_class.call(task: task, carrier: carrier, params: params)
      }.to change(Invoice, :count).by(1)
    end

    context 'when OTP is invalid' do
      let(:params) { { otp: 'wrong', photos: [] } }

      it 'returns failure and does not change task' do
        result = described_class.call(task: task, carrier: carrier, params: params)

        expect(result).to be_failure
        expect(task.reload.status).to eq('assigned')
      end
    end
  end
end
```

---

## Shared Examples for Services

```ruby
# spec/support/shared_examples/service_examples.rb
RSpec.shared_examples 'a service with result' do
  it 'returns ServiceResult' do
    expect(result).to be_a(ServiceResult)
  end
end

RSpec.shared_examples 'a successful service' do
  it_behaves_like 'a service with result'

  it 'returns success' do
    expect(result).to be_success
  end
end

RSpec.shared_examples 'a failed service' do |expected_error|
  it_behaves_like 'a service with result'

  it 'returns failure' do
    expect(result).to be_failure
  end

  if expected_error
    it "returns error: #{expected_error}" do
      expect(result.error).to eq(expected_error)
    end
  end
end

# Usage
RSpec.describe TasksManager::CreateTask do
  let(:result) { described_class.call(**params) }

  context 'with valid params' do
    let(:params) { valid_params }
    it_behaves_like 'a successful service'
  end

  context 'with invalid params' do
    let(:params) { invalid_params }
    it_behaves_like 'a failed service', "Recipient required"
  end
end
```

---

## Testing Jobs Enqueued by Services

```ruby
RSpec.describe TasksManager::CreateTask do
  include ActiveJob::TestHelper

  it 'enqueues notification job' do
    expect {
      described_class.call(account: account, merchant: merchant, params: valid_params)
    }.to have_enqueued_job(TaskNotificationJob)
  end

  it 'enqueues job with correct arguments' do
    task = described_class.call(account: account, merchant: merchant, params: valid_params)

    expect(TaskNotificationJob).to have_been_enqueued.with(task.id)
  end

  it 'processes job inline' do
    perform_enqueued_jobs do
      task = described_class.call(account: account, merchant: merchant, params: valid_params)
      expect(task.recipient.notifications.count).to eq(1)
    end
  end
end
```
