---
name: minitest
description: This skill should be used when the user asks about "Minitest", "Rails testing", "test/", "fixtures", "ActiveSupport::TestCase", "ActionDispatch::IntegrationTest", "system tests", "functional tests", "assert", "assert_equal", "assert_difference", "test_helper", "rails test", or needs guidance on testing Rails applications with the default Minitest framework.
version: 1.0.0
---

# Minitest for Rails

Comprehensive guide to testing Rails applications with Minitest, the default Rails testing framework.

## Test Case Classes

Rails provides specialized test case base classes:

| Base Class | Purpose | Location |
|------------|---------|----------|
| `ActiveSupport::TestCase` | Model and unit tests | `test/models/` |
| `ActionDispatch::IntegrationTest` | Multi-controller workflow tests | `test/integration/` |
| `ActionDispatch::SystemTestCase` | Browser-based end-to-end tests | `test/system/` |
| `ActionController::TestCase` | Functional controller tests | `test/controllers/` |
| `ActionView::TestCase` | View and helper tests | `test/helpers/` |
| `ActionMailer::TestCase` | Mailer tests | `test/mailers/` |
| `ActiveJob::TestCase` | Background job tests | `test/jobs/` |

## Configuration

```ruby
# test/test_helper.rb
ENV["RAILS_ENV"] ||= "test"
require_relative "../config/environment"
require "rails/test_help"

class ActiveSupport::TestCase
  # Run tests in parallel
  parallelize(workers: :number_of_processors)

  # Load fixtures
  fixtures :all

  # Add helper methods here
end


```

## Directory Structure

```
test/
├── controllers/          # Functional controller tests
├── fixtures/
│   ├── files/           # Upload test files
│   ├── users.yml
│   └── articles.yml
├── helpers/             # View helper tests
├── integration/         # Multi-controller tests
├── jobs/                # ActiveJob tests
├── mailers/             # Email tests
├── models/              # Model unit tests
├── system/              # Browser tests (Capybara)
├── application_system_test_case.rb
└── test_helper.rb
```

## Model Tests

```ruby
# test/models/article_test.rb
require "test_helper"

class ArticleTest < ActiveSupport::TestCase
  # Setup runs before each test
  setup do
    @article = articles(:published)
  end

  # Associations
  test "belongs to user" do
    assert_respond_to @article, :user
    assert_instance_of User, @article.user
  end

  test "has many comments" do
    assert_respond_to @article, :comments
  end

  # Validations
  test "is invalid without title" do
    article = Article.new(body: "Content", user: @user)
    assert_not article.valid?
    assert_includes article.errors[:title], "can't be blank"
  end

  test "is invalid with title over 255 characters" do
    article = Article.new(title: "a" * 256, body: "Content", user: @user)
    assert_not article.valid?
  end

  test "is valid with all attributes" do
    article = Article.new(title: "Test", body: "Content", user: @user)
    assert article.valid?
  end

  # Scopes
  test ".published returns only published articles" do
    assert_includes Article.published, articles(:published)
    assert_not_includes Article.published, articles(:draft)
  end

  test ".recent orders by created_at descending" do
    recent = Article.recent.first
    assert_equal articles(:published), recent
  end

  # Instance methods
  test "#publish! changes status to published" do
    article = articles(:draft)
    article.publish!

    assert_equal "published", article.status
    assert_not_nil article.published_at
  end

  test "#published? returns true for published articles" do
    assert articles(:published).published?
    assert_not articles(:draft).published?
  end
end
```

## Controller Tests (Functional)

```ruby
# test/controllers/articles_controller_test.rb
require "test_helper"

class ArticlesControllerTest < ActionDispatch::IntegrationTest
  setup do
    @article = articles(:published)
    @user = users(:one)
  end

  test "should get index" do
    get articles_url
    assert_response :success
  end

  test "should get show" do
    get article_url(@article)
    assert_response :success
  end

  test "should get new" do
    get new_article_url
    assert_response :success
  end

  test "should create article" do
    assert_difference("Article.count") do
      post articles_url, params: {
        article: { title: "New Article", body: "Content" }
      }
    end

    assert_redirected_to article_url(Article.last)
  end

  test "should not create article with invalid params" do
    assert_no_difference("Article.count") do
      post articles_url, params: { article: { title: "" } }
    end

    assert_response :unprocessable_entity
  end

  test "should update article" do
    patch article_url(@article), params: {
      article: { title: "Updated Title" }
    }

    assert_redirected_to article_url(@article)
    @article.reload
    assert_equal "Updated Title", @article.title
  end

  test "should destroy article" do
    assert_difference("Article.count", -1) do
      delete article_url(@article)
    end

    assert_redirected_to articles_url
  end
end
```

## Integration Tests

```ruby
# test/integration/user_flows_test.rb
require "test_helper"

class UserFlowsTest < ActionDispatch::IntegrationTest
  test "user can create article" do
    get new_article_url
    assert_response :success

    post articles_url, params: {
      article: { title: "My First Article", body: "Content" }
    }
    follow_redirect!
    assert_select "h1", "My First Article"
  end

  test "browsing articles as guest" do
    get articles_url
    assert_response :success
    assert_select "article", minimum: 1

    get article_url(articles(:published))
    assert_response :success
    assert_select "h1", articles(:published).title
  end
end
```

## System Tests

```ruby
# test/application_system_test_case.rb
require "test_helper"

class ApplicationSystemTestCase < ActionDispatch::SystemTestCase
  driven_by :selenium, using: :headless_chrome, screen_size: [1400, 1400]
end
```

```ruby
# test/system/articles_test.rb
require "application_system_test_case"

class ArticlesTest < ApplicationSystemTestCase
  setup do
    @article = articles(:published)
  end

  test "visiting the index" do
    visit articles_url
    assert_selector "h1", text: "Articles"
  end

  test "creating an article" do
    visit new_article_url

    fill_in "Title", with: "System Test Article"
    fill_in "Body", with: "This is test content."
    click_on "Create Article"

    assert_text "Article was successfully created"
    assert_text "System Test Article"
  end

  test "updating an article" do
    visit article_url(@article)
    click_on "Edit"

    fill_in "Title", with: "Updated Title"
    click_on "Update Article"

    assert_text "Article was successfully updated"
    assert_text "Updated Title"
  end

  test "destroying an article" do
    visit article_url(@article)
    click_on "Delete", match: :first

    assert_text "Article was successfully destroyed"
  end

  test "adding comment with Turbo" do
    visit article_url(@article)

    fill_in "comment_body", with: "Great article!"
    click_on "Add Comment"

    within "#comments" do
      assert_text "Great article!"
    end
  end
end
```

## Fixtures

```yaml
# test/fixtures/users.yml
one:
  email: user1@example.com
  name: Test User

admin:
  email: admin@example.com
  name: Admin User
  role: admin

# test/fixtures/articles.yml
published:
  title: Published Article
  body: This is published content.
  status: published
  user: one
  published_at: <%= 1.day.ago %>
  created_at: <%= 2.days.ago %>

draft:
  title: Draft Article
  body: This is draft content.
  status: draft
  user: one
  created_at: <%= 1.day.ago %>

# With associations
# test/fixtures/comments.yml
one:
  body: Great article!
  article: published
  user: one
```

## Assertions Reference

### Basic Assertions

```ruby
assert value                        # truthy
assert_not value                    # falsy (Rails)
refute value                        # falsy (Minitest)

assert_equal expected, actual       # ==
assert_not_equal unexpected, actual
assert_same expected, actual        # same object
assert_nil value
assert_not_nil value

assert_empty collection
assert_not_empty collection
assert_includes collection, item
assert_not_includes collection, item

assert_instance_of Class, object
assert_kind_of Class, object
assert_respond_to object, :method

assert_match /regex/, string
assert_no_match /regex/, string

assert_raises(ErrorClass) { action }
assert_nothing_raised { action }
```

### Rails-Specific Assertions

```ruby
# Count changes
assert_difference "Article.count", 1 do
  post articles_url, params: { article: valid_params }
end

assert_no_difference "Article.count" do
  post articles_url, params: { article: invalid_params }
end

# Multiple counts
assert_difference ["Article.count", "Tag.count"], 1 do
  post articles_url, params: params_with_tag
end

# HTTP responses
assert_response :success         # 200
assert_response :redirect        # 3xx
assert_response :not_found       # 404
assert_response :unprocessable_entity  # 422
assert_response 201              # Specific code

# Redirects
assert_redirected_to article_url(@article)
assert_redirected_to root_url

# Query count (prevent N+1)
assert_queries_count(2) do
  Article.includes(:user).each { |a| a.user.name }
end

# Enqueued jobs
assert_enqueued_jobs 1 do
  ArticleMailer.published(@article).deliver_later
end

assert_enqueued_with(job: NotifyJob, args: [@article]) do
  @article.publish!
end

# Enqueued emails
assert_enqueued_emails 1 do
  UserMailer.welcome(@user).deliver_later
end

# DOM assertions (system tests)
assert_selector "h1", text: "Title"
assert_text "Expected content"
assert_no_text "Should not appear"
assert_select "article", count: 3
```

## Mailer Tests

```ruby
# test/mailers/user_mailer_test.rb
require "test_helper"

class UserMailerTest < ActionMailer::TestCase
  test "welcome email" do
    user = users(:one)
    email = UserMailer.welcome(user)

    assert_emails 1 do
      email.deliver_now
    end

    assert_equal ["welcome@example.com"], email.from
    assert_equal [user.email], email.to
    assert_equal "Welcome to Our App", email.subject
    assert_match "Hello #{user.name}", email.body.encoded
  end

  test "welcome email is enqueued" do
    user = users(:one)

    assert_enqueued_emails 1 do
      UserMailer.welcome(user).deliver_later
    end
  end
end
```

## Job Tests

```ruby
# test/jobs/article_notification_job_test.rb
require "test_helper"

class ArticleNotificationJobTest < ActiveJob::TestCase
  test "sends notification to subscribers" do
    article = articles(:published)

    assert_enqueued_emails article.subscribers.count do
      ArticleNotificationJob.perform_now(article)
    end
  end

  test "job is enqueued on publish" do
    article = articles(:draft)

    assert_enqueued_with(job: ArticleNotificationJob, args: [article]) do
      article.publish!
    end
  end

  test "performs enqueued jobs" do
    article = articles(:draft)
    article.publish!

    perform_enqueued_jobs

    # Verify side effects
    assert_emails article.subscribers.count
  end
end
```

## Helper Tests

```ruby
# test/helpers/articles_helper_test.rb
require "test_helper"

class ArticlesHelperTest < ActionView::TestCase
  test "format_status returns badge HTML" do
    result = format_status("published")
    assert_dom_equal '<span class="badge badge-success">Published</span>', result
  end

  test "reading_time calculates minutes" do
    article = articles(:published)
    article.body = "word " * 500  # 500 words

    assert_equal "2 min read", reading_time(article)
  end
end
```

## Parallel Testing

```ruby
# test/test_helper.rb
class ActiveSupport::TestCase
  # Run tests in parallel with specified workers
  parallelize(workers: :number_of_processors)

  # Or with specific count
  parallelize(workers: 4)

  # Setup for parallel testing
  parallelize_setup do |worker|
    # Setup for each worker
  end

  parallelize_teardown do |worker|
    # Cleanup for each worker
  end
end
```

## Running Tests

```bash
# All tests
rails test

# Specific directory
rails test test/models

# Single file
rails test test/models/article_test.rb

# Single test by line number
rails test test/models/article_test.rb:25

# Single test by name
rails test test/models/article_test.rb -n test_is_invalid_without_title

# System tests only
rails test:system

# All including system
rails test:all

# Parallel execution
rails test:parallel:all

# With verbose output
rails test -v

# Stop on first failure
rails test -f

# Specific seed (for reproducibility)
rails test --seed 12345
```

## Additional Resources

### Reference Files

- **`references/minitest-patterns.md`** - Advanced patterns, custom assertions, test organization
