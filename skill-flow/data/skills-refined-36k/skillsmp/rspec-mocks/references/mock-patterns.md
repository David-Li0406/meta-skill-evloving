# Mock Patterns

## Dependency Injection

The cleanest approach to mocking - inject dependencies through constructor:

```ruby
class OrderProcessor
  def initialize(payment_gateway:, mailer:)
    @payment_gateway = payment_gateway
    @mailer = mailer
  end

  def process(order)
    result = @payment_gateway.charge(order.total)
    @mailer.send_confirmation(order) if result.success?
    result
  end
end

# Test
RSpec.describe OrderProcessor do
  let(:payment_gateway) { instance_double(PaymentGateway) }
  let(:mailer) { instance_double(OrderMailer) }
  let(:processor) { described_class.new(payment_gateway: payment_gateway, mailer: mailer) }

  describe "#process" do
    let(:order) { build_stubbed(:order, total: 100) }

    context "when payment succeeds" do
      before do
        allow(payment_gateway).to receive(:charge).and_return(OpenStruct.new(success?: true))
        allow(mailer).to receive(:send_confirmation)
      end

      it "charges the payment gateway" do
        processor.process(order)
        expect(payment_gateway).to have_received(:charge).with(100)
      end

      it "sends confirmation email" do
        processor.process(order)
        expect(mailer).to have_received(:send_confirmation).with(order)
      end
    end

    context "when payment fails" do
      before do
        allow(payment_gateway).to receive(:charge).and_return(OpenStruct.new(success?: false))
      end

      it "does not send email" do
        processor.process(order)
        expect(mailer).not_to have_received(:send_confirmation)
      end
    end
  end
end
```

## Service Object Pattern

```ruby
class CreateUser
  def initialize(user_repo: User, mailer: UserMailer)
    @user_repo = user_repo
    @mailer = mailer
  end

  def call(params)
    user = @user_repo.create!(params)
    @mailer.welcome(user).deliver_later
    user
  end
end

RSpec.describe CreateUser do
  let(:user_repo) { class_double(User) }
  let(:mailer) { class_double(UserMailer) }
  let(:service) { described_class.new(user_repo: user_repo, mailer: mailer) }

  describe "#call" do
    let(:user) { build_stubbed(:user) }
    let(:mail) { instance_double(ActionMailer::MessageDelivery) }

    before do
      allow(user_repo).to receive(:create!).and_return(user)
      allow(mailer).to receive(:welcome).and_return(mail)
      allow(mail).to receive(:deliver_later)
    end

    it "creates user and sends welcome email" do
      result = service.call(email: "test@example.com")

      expect(result).to eq(user)
      expect(mailer).to have_received(:welcome).with(user)
    end
  end
end
```

## HTTP Client Mocking

### WebMock Pattern

```ruby
require "webmock/rspec"

RSpec.describe GitHubClient do
  describe "#fetch_user" do
    it "returns user data" do
      stub_request(:get, "https://api.github.com/users/octocat")
        .to_return(
          status: 200,
          body: { login: "octocat", id: 1 }.to_json,
          headers: { "Content-Type" => "application/json" }
        )

      result = described_class.new.fetch_user("octocat")

      expect(result[:login]).to eq("octocat")
    end

    it "handles rate limiting" do
      stub_request(:get, "https://api.github.com/users/octocat")
        .to_return(status: 429)

      expect {
        described_class.new.fetch_user("octocat")
      }.to raise_error(GitHubClient::RateLimitError)
    end
  end
end
```

### VCR for Recording

```ruby
VCR.configure do |config|
  config.cassette_library_dir = "spec/cassettes"
  config.hook_into :webmock
end

RSpec.describe GitHubClient do
  it "fetches real user data", :vcr do
    # First run: records HTTP interaction
    # Subsequent runs: replays from cassette
    result = described_class.new.fetch_user("octocat")
    expect(result[:login]).to eq("octocat")
  end
end
```

## Mocking Time

### travel_to Helper

```ruby
RSpec.describe Subscription do
  describe "#expired?" do
    it "returns true when past expiration" do
      subscription = create(:subscription, expires_at: 1.day.from_now)

      travel_to(2.days.from_now) do
        expect(subscription).to be_expired
      end
    end
  end
end
```

### Timecop Pattern

```ruby
around(:each) do |example|
  Timecop.freeze(Time.zone.local(2024, 6, 15, 12, 0, 0))
  example.run
  Timecop.return
end
```

## Mocking External Services

### Stripe Example

```ruby
RSpec.describe PaymentProcessor do
  describe "#charge" do
    let(:stripe_charge) { instance_double(Stripe::Charge, id: "ch_123", status: "succeeded") }

    before do
      allow(Stripe::Charge).to receive(:create).and_return(stripe_charge)
    end

    it "creates a charge" do
      result = described_class.new.charge(amount: 1000, token: "tok_visa")

      expect(Stripe::Charge).to have_received(:create).with(
        amount: 1000,
        currency: "usd",
        source: "tok_visa"
      )
      expect(result.id).to eq("ch_123")
    end
  end
end
```

### AWS S3 Example

```ruby
RSpec.describe FileUploader do
  let(:s3_client) { instance_double(Aws::S3::Client) }

  before do
    allow(Aws::S3::Client).to receive(:new).and_return(s3_client)
    allow(s3_client).to receive(:put_object)
  end

  it "uploads file to S3" do
    described_class.new.upload("test.txt", "content")

    expect(s3_client).to have_received(:put_object).with(
      bucket: "my-bucket",
      key: "test.txt",
      body: "content"
    )
  end
end
```

## Command Query Separation

Mock queries (return values), expect commands (side effects):

```ruby
# Query - stub return value
allow(user_repo).to receive(:find).and_return(user)

# Command - expect it was called
expect(mailer).to have_received(:send_notification)
```

## Partial Mock Anti-Pattern

```ruby
# Avoid mocking the class under test
RSpec.describe Calculator do
  it "adds numbers" do
    calc = Calculator.new
    # Don't do this - testing mock, not real code
    allow(calc).to receive(:add).and_return(5)
    expect(calc.add(2, 3)).to eq(5)
  end
end

# Instead, test real behavior
it "adds numbers" do
  calc = Calculator.new
  expect(calc.add(2, 3)).to eq(5)
end
```

## Spy Pattern for Commands

```ruby
RSpec.describe NotificationService do
  let(:slack) { instance_spy(SlackClient) }
  let(:email) { instance_spy(EmailClient) }
  let(:service) { described_class.new(slack: slack, email: email) }

  describe "#notify_all" do
    it "sends to all channels" do
      service.notify_all("Important message")

      expect(slack).to have_received(:post).with("Important message")
      expect(email).to have_received(:send).with("Important message")
    end
  end
end
```
