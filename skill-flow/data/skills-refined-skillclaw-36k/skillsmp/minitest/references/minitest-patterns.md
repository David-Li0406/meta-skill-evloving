# Advanced Minitest Patterns

## Custom Assertions

```ruby
# test/support/custom_assertions.rb
module CustomAssertions
  def assert_valid(record, msg = nil)
    msg = message(msg) { "Expected #{record.class} to be valid, but got errors: #{record.errors.full_messages.join(', ')}" }
    assert record.valid?, msg
  end

  def assert_invalid(record, attribute, msg = nil)
    record.valid?
    msg = message(msg) { "Expected #{record.class} to be invalid on #{attribute}" }
    assert record.errors[attribute].any?, msg
  end

  def assert_json_response
    assert_equal "application/json; charset=utf-8", response.content_type
  end

  def assert_paginated_response(expected_count)
    json = JSON.parse(response.body)
    assert_equal expected_count, json["data"].length
    assert json.key?("meta"), "Expected pagination meta"
  end
end

# Include in test_helper.rb
class ActiveSupport::TestCase
  include CustomAssertions
end
```

## Test Helpers

```ruby
# test/support/authentication_helper.rb
module AuthenticationHelper
  def sign_in(user)
    post user_session_url, params: {
      user: { email: user.email, password: "password" }
    }
  end

  def sign_out
    delete destroy_user_session_url
  end

  def auth_headers(user)
    { "Authorization" => "Bearer #{user.generate_jwt}" }
  end
end

class ActionDispatch::IntegrationTest
  include AuthenticationHelper
end
```

```ruby
# test/support/json_helper.rb
module JsonHelper
  def json_response
    JSON.parse(response.body, symbolize_names: true)
  end

  def json_body
    JSON.parse(response.body)
  end
end

class ActionDispatch::IntegrationTest
  include JsonHelper
end
```

## Fixture Best Practices

### Dynamic Fixtures with ERB

```yaml
# test/fixtures/users.yml
<% 5.times do |n| %>
user_<%= n %>:
  email: user<%= n %>@example.com
  name: User <%= n %>
  created_at: <%= n.days.ago %>
<% end %>

admin:
  email: admin@example.com
  name: Admin User
  role: admin
```

### Fixture Associations

```yaml
# test/fixtures/articles.yml
published:
  title: Published Article
  user: one  # References users(:one)
  status: published

# test/fixtures/comments.yml
first_comment:
  body: Great article!
  article: published  # References articles(:published)
  user: one
```

### Fixture Files

```yaml
# test/fixtures/attachments.yml
avatar:
  name: avatar.png
  content_type: image/png
  file: <%= ActiveStorage::Blob.fixture(filename: "avatar.png", content_type: "image/png") %>
```

## Test Organization

### Shared Setup

```ruby
# test/test_helper.rb
class ActiveSupport::TestCase
  # Common setup for all tests
  setup do
    Rails.cache.clear
  end
end

# Test-specific setup
class ArticleTest < ActiveSupport::TestCase
  setup do
    @article = articles(:published)
    @user = users(:one)
  end

  teardown do
    # Cleanup after each test
  end
end
```

### Shared Test Modules

```ruby
# test/support/publishable_tests.rb
module PublishableTests
  extend ActiveSupport::Concern

  included do
    test "can be published" do
      record = create_publishable_record(status: "draft")
      record.publish!
      assert_equal "published", record.status
    end

    test "sets published_at on publish" do
      record = create_publishable_record(status: "draft")
      freeze_time do
        record.publish!
        assert_equal Time.current, record.published_at
      end
    end
  end
end

# Usage
class ArticleTest < ActiveSupport::TestCase
  include PublishableTests

  private

  def create_publishable_record(**attrs)
    Article.create!(title: "Test", body: "Content", user: users(:one), **attrs)
  end
end
```

## System Test Patterns

### Page Objects

```ruby
# test/support/pages/login_page.rb
class LoginPage
  include Capybara::DSL

  def visit_page
    visit new_user_session_path
    self
  end

  def login(email:, password:)
    fill_in "Email", with: email
    fill_in "Password", with: password
    click_button "Sign in"
    self
  end

  def has_error?(message)
    has_content?(message)
  end
end

# Usage
class LoginSystemTest < ApplicationSystemTestCase
  test "successful login" do
    user = users(:one)

    LoginPage.new
      .visit_page
      .login(email: user.email, password: "password")

    assert_current_path root_path
  end
end
```

### Waiting for Turbo

```ruby
# test/support/turbo_helper.rb
module TurboHelper
  def wait_for_turbo
    assert_no_selector ".turbo-progress-bar"
  end

  def within_turbo_frame(id)
    within("turbo-frame##{id}") do
      yield
    end
  end
end

class ApplicationSystemTestCase < ActionDispatch::SystemTestCase
  include TurboHelper
end
```

## Performance Testing

```ruby
# test/models/article_test.rb
class ArticlePerformanceTest < ActiveSupport::TestCase
  test "index query uses eager loading" do
    create_articles(10)

    assert_queries_count(2) do
      Article.includes(:user, :tags).each do |article|
        article.user.name
        article.tags.map(&:name)
      end
    end
  end

  test "bulk insert is efficient" do
    assert_queries_count(1) do
      Article.insert_all([
        { title: "A", body: "Content", user_id: users(:one).id },
        { title: "B", body: "Content", user_id: users(:one).id }
      ])
    end
  end

  private

  def create_articles(count)
    count.times { |i| Article.create!(title: "Article #{i}", body: "Content", user: users(:one)) }
  end
end
```

## Testing Background Jobs

```ruby
# test/jobs/notification_job_test.rb
class NotificationJobTest < ActiveJob::TestCase
  test "sends email to all subscribers" do
    article = articles(:published)
    subscribers = [users(:one), users(:admin)]
    article.subscribers = subscribers

    perform_enqueued_jobs do
      NotificationJob.perform_later(article)
    end

    assert_emails subscribers.count
  end

  test "handles missing article gracefully" do
    assert_nothing_raised do
      NotificationJob.perform_now(999999)
    end
  end

  test "retries on temporary failure" do
    article = articles(:published)

    ExternalService.stub(:notify, ->(*) { raise Timeout::Error }) do
      assert_enqueued_with(job: NotificationJob) do
        NotificationJob.perform_later(article)
      end
    end
  end
end
```

## CI Configuration

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        ports: ['5432:5432']
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with:
          bundler-cache: true
      - run: bin/rails db:prepare
      - run: bin/rails test
      - run: bin/rails test:system
```

## Debugging Tests

```ruby
# Pause execution
binding.irb

# Save screenshot in system tests
take_screenshot

# Print page HTML
puts page.html

# Show current path
puts current_path

# Debug SQL queries
ActiveRecord::Base.logger = Logger.new(STDOUT)
```

## Test Data Strategies

Prefer fixtures for baseline data and use setup blocks to customize records
needed for a specific test.
