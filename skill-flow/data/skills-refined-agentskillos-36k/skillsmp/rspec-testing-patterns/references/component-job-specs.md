# ViewComponent & Job Specs Reference

## ViewComponent Specs

```ruby
# spec/components/metrics/kpi_card_component_spec.rb
require 'rails_helper'

RSpec.describe Metrics::KpiCardComponent, type: :component do
  let(:title) { "Total Orders" }
  let(:value) { 1234 }

  subject(:component) do
    described_class.new(title: title, value: value)
  end

  describe "#render" do
    before { render_inline(component) }

    it "renders the title" do
      expect(page).to have_css("h3", text: title)
    end

    it "renders the value" do
      expect(page).to have_text("1,234")
    end
  end

  describe "#formatted_value" do
    it "formats large numbers with delimiter" do
      component = described_class.new(title: "Test", value: 1234567)
      expect(component.formatted_value).to eq("1,234,567")
    end
  end

  context "with trend" do
    let(:component) do
      described_class.new(title: title, value: value, trend: :up)
    end

    before { render_inline(component) }

    it "shows trend indicator" do
      expect(page).to have_css(".text-green-500")
    end
  end

  context "with content block" do
    before do
      render_inline(component) do
        "Additional content"
      end
    end

    it "renders the block content" do
      expect(page).to have_text("Additional content")
    end
  end
end
```

---

## Testing Component Slots

```ruby
RSpec.describe Cards::CardComponent, type: :component do
  it 'renders header slot' do
    render_inline(described_class.new) do |c|
      c.with_header { "Card Title" }
      c.with_body { "Card content" }
    end

    expect(page).to have_css('.card-header', text: 'Card Title')
    expect(page).to have_css('.card-body', text: 'Card content')
  end
end
```

---

## Component Previews Testing

```ruby
# spec/components/previews/button_component_preview.rb
class ButtonComponentPreview < ViewComponent::Preview
  def default
    render(ButtonComponent.new(label: "Click me"))
  end

  def primary
    render(ButtonComponent.new(label: "Primary", variant: :primary))
  end

  def with_icon
    render(ButtonComponent.new(label: "Save", icon: "check"))
  end
end
```

---

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

    context "when task doesn't exist" do
      it "handles gracefully" do
        expect { described_class.perform_now(0) }.not_to raise_error
      end
    end
  end

  describe "enqueuing" do
    it "enqueues in correct queue" do
      expect {
        described_class.perform_later(task.id)
      }.to have_enqueued_job.on_queue("notifications")
    end

    it "enqueues with correct arguments" do
      expect {
        described_class.perform_later(task.id)
      }.to have_enqueued_job.with(task.id)
    end
  end
end
```

---

## Testing Job Retry Behavior

```ruby
describe 'retry behavior' do
  it 'retries on network error' do
    allow(SmsService).to receive(:send).and_raise(Faraday::ConnectionFailed)

    expect {
      described_class.perform_now(task.id)
    }.to raise_error(Faraday::ConnectionFailed)

    # Job should be configured for retry
    expect(described_class.sidekiq_options['retry']).to eq(5)
  end
end
```

---

## Testing Scheduled Jobs

```ruby
describe 'scheduled execution' do
  it 'schedules for later' do
    expect {
      described_class.set(wait: 1.hour).perform_later(task.id)
    }.to have_enqueued_job.at(1.hour.from_now)
  end
end
```

---

## Performing Jobs Inline

```ruby
describe 'full integration' do
  it 'sends notification and updates task' do
    perform_enqueued_jobs do
      TasksManager::CreateTask.call(params)
    end

    expect(task.recipient.notifications.count).to eq(1)
  end
end
```
