---
name: RSpec Rails
description: This skill should be used when the user asks about "request specs", "system specs", "model specs", "controller specs", "mailer specs", "feature specs", "Capybara", "rspec-rails", or needs guidance on testing Rails applications with RSpec.
version: 1.0.0
---

# RSpec Rails

rspec-rails integrates RSpec with Rails, providing specialized spec types for each Rails component.

## Spec Types

| Spec Type | Location | Purpose |
|-----------|----------|---------|
| Model | `spec/models/` | ActiveRecord models, validations, associations |
| Request | `spec/requests/` | HTTP requests, full controller + routing |
| System | `spec/system/` | Browser-based end-to-end tests |
| Mailer | `spec/mailers/` | Email content and delivery |
| Job | `spec/jobs/` | Background job behavior |
| View | `spec/views/` | View rendering (less common) |
| Helper | `spec/helpers/` | View helper methods |
| Routing | `spec/routing/` | Route resolution |
| Controller | `spec/controllers/` | **Deprecated** - use request specs |

## Model Specs

Test ActiveRecord models, validations, associations, and scopes:

```ruby
# spec/models/user_spec.rb
RSpec.describe User, type: :model do
  describe "validations" do
    it { is_expected.to validate_presence_of(:email) }
    it { is_expected.to validate_uniqueness_of(:email).case_insensitive }
    it { is_expected.to validate_length_of(:password).is_at_least(8) }
  end

  describe "associations" do
    it { is_expected.to have_many(:posts).dependent(:destroy) }
    it { is_expected.to belong_to(:organization).optional }
    it { is_expected.to have_one(:profile) }
  end

  describe "#full_name" do
    it "returns first and last name" do
      user = build(:user, first_name: "John", last_name: "Doe")
      expect(user.full_name).to eq("John Doe")
    end
  end

  describe ".active" do
    it "returns only active users" do
      active = create(:user, active: true)
      inactive = create(:user, active: false)

      expect(User.active).to include(active)
      expect(User.active).not_to include(inactive)
    end
  end
end
```

### Shoulda Matchers

Add to Gemfile for one-liner validations:

```ruby
# Gemfile
group :test do
  gem "shoulda-matchers"
end

# spec/rails_helper.rb
Shoulda::Matchers.configure do |config|
  config.integrate do |with|
    with.test_framework :rspec
    with.library :rails
  end
end
```

## Request Specs

Test HTTP endpoints (preferred over controller specs):

```ruby
# spec/requests/users_spec.rb
RSpec.describe "Users", type: :request do
  describe "GET /users" do
    it "returns a list of users" do
      create_list(:user, 3)

      get users_path

      expect(response).to have_http_status(:ok)
      expect(response.parsed_body.size).to eq(3)
    end
  end

  describe "POST /users" do
    context "with valid params" do
      it "creates a user" do
        user_params = { user: { email: "new@example.com", password: "password123" } }

        expect {
          post users_path, params: user_params
        }.to change(User, :count).by(1)

        expect(response).to redirect_to(user_path(User.last))
      end
    end

    context "with invalid params" do
      it "returns unprocessable entity" do
        post users_path, params: { user: { email: "" } }

        expect(response).to have_http_status(:unprocessable_entity)
      end
    end
  end

  describe "with authentication" do
    let(:user) { create(:user) }

    it "allows access to authenticated users" do
      sign_in user  # Devise helper

      get dashboard_path

      expect(response).to have_http_status(:ok)
    end

    it "redirects unauthenticated users" do
      get dashboard_path

      expect(response).to redirect_to(login_path)
    end
  end
end
```

### JSON API Testing

```ruby
RSpec.describe "API::Users", type: :request do
  describe "GET /api/users/:id" do
    it "returns user as JSON" do
      user = create(:user)

      get api_user_path(user), headers: { "Accept" => "application/json" }

      expect(response).to have_http_status(:ok)
      expect(response.content_type).to include("application/json")

      json = response.parsed_body
      expect(json["email"]).to eq(user.email)
    end
  end

  describe "POST /api/users" do
    it "creates user with JSON params" do
      headers = {
        "Content-Type" => "application/json",
        "Accept" => "application/json"
      }

      post api_users_path,
        params: { email: "test@example.com" }.to_json,
        headers: headers

      expect(response).to have_http_status(:created)
    end
  end
end
```

## System Specs

Browser-based tests using Capybara:

```ruby
# spec/system/user_registration_spec.rb
RSpec.describe "User Registration", type: :system do
  before do
    driven_by(:rack_test)  # Fast, no JS
    # driven_by(:selenium_chrome_headless)  # With JS
  end

  it "allows new user to register" do
    visit new_user_registration_path

    fill_in "Email", with: "newuser@example.com"
    fill_in "Password", with: "password123"
    fill_in "Password confirmation", with: "password123"
    click_button "Sign up"

    expect(page).to have_content("Welcome!")
    expect(page).to have_current_path(dashboard_path)
  end

  it "shows validation errors" do
    visit new_user_registration_path

    fill_in "Email", with: ""
    click_button "Sign up"

    expect(page).to have_content("Email can't be blank")
  end
end
```

### JavaScript Testing

```ruby
RSpec.describe "Dynamic Form", type: :system, js: true do
  before do
    driven_by(:selenium_chrome_headless)
  end

  it "adds items dynamically" do
    visit new_order_path

    click_button "Add Item"

    within "#items" do
      expect(page).to have_selector(".item", count: 1)
    end
  end

  it "filters results without page reload" do
    create(:product, name: "Widget")
    create(:product, name: "Gadget")

    visit products_path

    fill_in "Search", with: "Wid"

    expect(page).to have_content("Widget")
    expect(page).not_to have_content("Gadget")
  end
end
```

### Capybara Matchers

```ruby
# Content
expect(page).to have_content("Welcome")
expect(page).to have_text("Hello", exact: true)
expect(page).not_to have_content("Error")

# Elements
expect(page).to have_selector("div.alert")
expect(page).to have_css(".user-list li", count: 3)
expect(page).to have_xpath("//table/tr")

# Forms
expect(page).to have_field("Email")
expect(page).to have_button("Submit")
expect(page).to have_checked_field("Remember me")

# Links
expect(page).to have_link("Home", href: root_path)

# Current URL
expect(page).to have_current_path(dashboard_path)
```

## Mailer Specs

```ruby
# spec/mailers/user_mailer_spec.rb
RSpec.describe UserMailer, type: :mailer do
  describe "#welcome" do
    let(:user) { create(:user, email: "test@example.com") }
    let(:mail) { described_class.welcome(user) }

    it "renders the headers" do
      expect(mail.subject).to eq("Welcome to Our App!")
      expect(mail.to).to eq(["test@example.com"])
      expect(mail.from).to eq(["noreply@example.com"])
    end

    it "renders the body" do
      expect(mail.body.encoded).to include("Hello")
      expect(mail.body.encoded).to include(user.first_name)
    end

    it "includes unsubscribe link" do
      expect(mail.body.encoded).to include(unsubscribe_url)
    end
  end
end
```

### Testing Email Delivery

```ruby
RSpec.describe UserRegistration do
  it "sends welcome email" do
    expect {
      described_class.call(user_params)
    }.to change { ActionMailer::Base.deliveries.count }.by(1)
  end

  it "enqueues welcome email" do
    expect {
      described_class.call(user_params)
    }.to have_enqueued_mail(UserMailer, :welcome)
  end
end
```

## Job Specs

```ruby
# spec/jobs/send_newsletter_job_spec.rb
RSpec.describe SendNewsletterJob, type: :job do
  describe "#perform" do
    it "sends newsletter to all subscribers" do
      subscribers = create_list(:user, 3, subscribed: true)
      newsletter = create(:newsletter)

      expect {
        described_class.perform_now(newsletter.id)
      }.to change { ActionMailer::Base.deliveries.count }.by(3)
    end
  end

  describe "enqueuing" do
    it "enqueues job" do
      expect {
        described_class.perform_later(1)
      }.to have_enqueued_job(described_class).with(1)
    end

    it "enqueues to correct queue" do
      expect {
        described_class.perform_later(1)
      }.to have_enqueued_job.on_queue("mailers")
    end
  end
end
```

## Rails Helper

```ruby
# spec/rails_helper.rb
require "spec_helper"
ENV["RAILS_ENV"] ||= "test"
require_relative "../config/environment"
abort("Production!") if Rails.env.production?
require "rspec/rails"

Dir[Rails.root.join("spec/support/**/*.rb")].each { |f| require f }

RSpec.configure do |config|
  config.fixture_paths = [Rails.root.join("spec/fixtures")]
  config.use_transactional_fixtures = true
  config.infer_spec_type_from_file_location!
  config.filter_rails_from_backtrace!
end
```

## Additional Resources

### Reference Files

- **`references/system-spec-patterns.md`** - Advanced Capybara patterns
- **`references/request-spec-patterns.md`** - API testing patterns

### Example Files

- **`examples/full_request_spec.rb`** - Complete request spec example
- **`examples/system_spec_with_js.rb`** - JavaScript testing example
