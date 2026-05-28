# Test Helpers & Mocking Reference

## Authentication Helpers

```ruby
# spec/support/helpers/auth_helpers.rb
module AuthHelpers
  def auth_headers(user)
    token = user.generate_jwt_token
    { 'Authorization' => "Bearer #{token}" }
  end

  def sign_in(user)
    login_as(user, scope: :user)
  end
end

RSpec.configure do |config|
  config.include AuthHelpers, type: :request
  config.include AuthHelpers, type: :system
end
```

---

## JSON Response Helper

```ruby
# spec/support/helpers/json_helpers.rb
module JsonHelpers
  def json_response
    JSON.parse(response.body)
  end

  def json_data
    json_response['data']
  end

  def json_errors
    json_response['errors']
  end
end

RSpec.configure do |config|
  config.include JsonHelpers, type: :request
end
```

---

## Mocking External Services

### WebMock

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

  def stub_shipping_api_failure
    stub_request(:post, "https://shipping.example.com/api/labels")
      .to_return(status: 500, body: { error: "Server error" }.to_json)
  end

  def stub_shipping_api_timeout
    stub_request(:post, "https://shipping.example.com/api/labels")
      .to_timeout
  end
end

RSpec.configure do |config|
  config.include WebmockHelpers
end

# Usage in spec
describe "creating shipping label" do
  before { stub_shipping_api_success }

  it "creates label successfully" do
    # test...
  end
end
```

### VCR Cassettes

```ruby
# spec/support/vcr.rb
VCR.configure do |config|
  config.cassette_library_dir = 'spec/cassettes'
  config.hook_into :webmock
  config.filter_sensitive_data('<API_KEY>') { ENV['SHIPPING_API_KEY'] }
end

# Usage
describe 'shipping integration', :vcr do
  it 'creates real shipping label' do
    result = ShippingService.create_label(task)
    expect(result.tracking_number).to be_present
  end
end
```

---

## Instance Doubles

```ruby
# Strict verification of expected methods
let(:service) { instance_double(NotificationService) }

before do
  allow(service).to receive(:send_sms).and_return(true)
  allow(NotificationService).to receive(:new).and_return(service)
end

it 'calls notification service' do
  expect(service).to receive(:send_sms).with(phone: '+1234567890', message: anything)
  described_class.call(params)
end
```

---

## Spy Pattern

```ruby
let(:mailer) { spy(UserMailer) }

it 'sends welcome email' do
  described_class.call(user)

  expect(UserMailer).to have_received(:welcome_email).with(user)
end
```

---

## Time Helpers

```ruby
# Freeze time
it 'sets created_at to current time' do
  freeze_time do
    task = create(:task)
    expect(task.created_at).to eq(Time.current)
  end
end

# Travel to specific time
it 'handles past date' do
  travel_to(1.week.ago) do
    task = create(:task)
    expect(task.created_at).to eq(1.week.ago)
  end
end

# Travel forward
it 'expires after 24 hours' do
  token = create(:token)

  travel 25.hours

  expect(token.expired?).to be true
end
```

---

## Database Cleaner

```ruby
# spec/support/database_cleaner.rb
RSpec.configure do |config|
  config.before(:suite) do
    DatabaseCleaner.strategy = :transaction
    DatabaseCleaner.clean_with(:truncation)
  end

  config.around(:each) do |example|
    DatabaseCleaner.cleaning do
      example.run
    end
  end

  # For JS tests, use truncation
  config.before(:each, js: true) do
    DatabaseCleaner.strategy = :truncation
  end
end
```
