# Code Quality Guide for Rails

This guide defines code quality standards and refactoring strategies to prevent bloated classes and methods.

## Table of Contents

- [Core Principles](#core-principles)
- [Method Size Guidelines](#method-size-guidelines)
- [Class Size Guidelines](#class-size-guidelines)
- [Refactoring Patterns](#refactoring-patterns)
- [Service Objects](#service-objects)
- [Query Objects](#query-objects)
- [Form Objects](#form-objects)
- [Decorators/Presenters](#decoratorspresenters)

## Core Principles

### Single Responsibility Principle (SRP)

Each class and method should have one clear responsibility.

**Signs of violation:**
- Methods doing multiple unrelated things
- Classes with many public methods
- Names with "and" or "or" (e.g., `create_and_notify_user`)

### Keep It Simple

Prefer simple, readable code over clever solutions.

**Guidelines:**
- Favor explicit over implicit
- Avoid deep nesting (max 2-3 levels)
- Use early returns to reduce nesting

## Method Size Guidelines

### Maximum Lines per Method

**Target: 5-10 lines**
**Hard limit: 15 lines**

If a method exceeds 15 lines, it likely does too much and should be refactored.

### Signs a Method Needs Refactoring

```ruby
# ❌ BAD - Too long, does too much
def create
  @article = Article.new(article_params)
  @article.user = current_user

  if @article.save
    # Send notification
    ArticleMailer.published_email(@article).deliver_later

    # Update user stats
    current_user.increment!(:articles_count)

    # Create activity log
    ActivityLog.create(
      user: current_user,
      action: 'created_article',
      resource: @article
    )

    # Notify followers
    current_user.followers.each do |follower|
      NotificationMailer.new_article(follower, @article).deliver_later
    end

    redirect_to @article, notice: 'Article created successfully.'
  else
    render :new, status: :unprocessable_entity
  end
end
```

```ruby
# ✅ GOOD - Extracted into smaller methods
def create
  @article = Article.new(article_params)
  @article.user = current_user

  if @article.save
    handle_successful_creation
    redirect_to @article, notice: 'Article created successfully.'
  else
    render :new, status: :unprocessable_entity
  end
end

private

def handle_successful_creation
  send_notifications
  update_user_stats
  log_activity
end

def send_notifications
  ArticleMailer.published_email(@article).deliver_later
  notify_followers
end

def notify_followers
  current_user.followers.each do |follower|
    NotificationMailer.new_article(follower, @article).deliver_later
  end
end

def update_user_stats
  current_user.increment!(:articles_count)
end

def log_activity
  ActivityLog.create(
    user: current_user,
    action: 'created_article',
    resource: @article
  )
end
```

**Even Better - Use Service Object:**

```ruby
# ✅ BEST - Service object handles complexity
def create
  @article = Article.new(article_params)
  @article.user = current_user

  if ArticleCreator.new(@article).create
    redirect_to @article, notice: 'Article created successfully.'
  else
    render :new, status: :unprocessable_entity
  end
end
```

## Class Size Guidelines

### Controller Actions

**Maximum: 7 RESTful actions**

If a controller needs more actions, consider:
- Extracting to a new controller
- Using nested resources
- Creating a custom action in a separate concern

### Model Methods

**Target: 10-15 public methods**
**Hard limit: 20 public methods**

If a model exceeds 20 public methods, extract logic to:
- Service objects for business logic
- Query objects for complex queries
- Decorators for presentation logic

### Signs a Class Needs Refactoring

```ruby
# ❌ BAD - Bloated model with too many responsibilities
class User < ApplicationRecord
  # Authentication logic
  def authenticate(password)
    # ...
  end

  # Statistics methods
  def total_articles
    # ...
  end

  def average_article_rating
    # ...
  end

  # Notification methods
  def send_welcome_email
    # ...
  end

  def notify_followers_of_new_article(article)
    # ...
  end

  # Search methods
  def self.search_by_name(query)
    # ...
  end

  def self.active_users
    # ...
  end

  # ... 20+ more methods
end
```

```ruby
# ✅ GOOD - Separated concerns
class User < ApplicationRecord
  # Only core user logic here
  validates :email, presence: true, uniqueness: true

  has_many :articles

  # Delegate complex queries to query object
  def self.search(query)
    UserQuery.new.search(query)
  end

  # Delegate statistics to service
  def statistics
    UserStatistics.new(self)
  end

  # Delegate notifications to service
  def notifications
    UserNotificationService.new(self)
  end
end

# app/services/user_statistics.rb
class UserStatistics
  def initialize(user)
    @user = user
  end

  def total_articles
    @user.articles.count
  end

  def average_article_rating
    @user.articles.average(:rating)
  end
end

# app/services/user_notification_service.rb
class UserNotificationService
  def initialize(user)
    @user = user
  end

  def send_welcome_email
    UserMailer.welcome_email(@user).deliver_later
  end

  def notify_followers_of_new_article(article)
    @user.followers.each do |follower|
      NotificationMailer.new_article(follower, article).deliver_later
    end
  end
end

# app/queries/user_query.rb
class UserQuery
  def search(query)
    User.where('name LIKE ? OR email LIKE ?', "%#{query}%", "%#{query}%")
  end

  def active
    User.where(active: true)
  end
end
```

## Refactoring Patterns

### Extract Method

When a method does multiple things, extract each responsibility.

```ruby
# Before
def process_order
  total = order_items.sum(&:price)
  tax = total * 0.1
  shipping = calculate_shipping(total)
  grand_total = total + tax + shipping

  charge_credit_card(grand_total)
  send_confirmation_email
  update_inventory
end

# After
def process_order
  grand_total = calculate_grand_total
  charge_payment(grand_total)
  post_process_order
end

private

def calculate_grand_total
  total = order_items.sum(&:price)
  tax = calculate_tax(total)
  shipping = calculate_shipping(total)
  total + tax + shipping
end

def calculate_tax(total)
  total * 0.1
end

def charge_payment(amount)
  charge_credit_card(amount)
end

def post_process_order
  send_confirmation_email
  update_inventory
end
```

### Early Returns

Use early returns to reduce nesting and improve readability.

```ruby
# ❌ BAD - Deep nesting
def publish_article
  if article.draft?
    if article.valid?
      if current_user.can_publish?
        article.update(status: 'published')
        notify_subscribers
        true
      else
        false
      end
    else
      false
    end
  else
    false
  end
end

# ✅ GOOD - Early returns
def publish_article
  return false unless article.draft?
  return false unless article.valid?
  return false unless current_user.can_publish?

  article.update(status: 'published')
  notify_subscribers
  true
end
```

## Service Objects

Use service objects for complex business logic that doesn't belong in models or controllers.

### When to Use Service Objects

- Multi-step processes
- Operations involving multiple models
- External API interactions
- Complex calculations or data transformations

### Service Object Pattern

```ruby
# app/services/article_publisher.rb
class ArticlePublisher
  def initialize(article, user)
    @article = article
    @user = user
  end

  def publish
    return false unless publishable?

    ActiveRecord::Base.transaction do
      update_article
      create_activity_log
      send_notifications
    end

    true
  rescue => e
    Rails.logger.error("Failed to publish article: #{e.message}")
    false
  end

  private

  def publishable?
    @article.draft? && @article.valid? && @user.can_publish?
  end

  def update_article
    @article.update!(
      status: 'published',
      published_at: Time.current,
      published_by: @user
    )
  end

  def create_activity_log
    ActivityLog.create!(
      user: @user,
      action: 'published_article',
      resource: @article
    )
  end

  def send_notifications
    NotificationService.new(@article).notify_subscribers
  end
end

# Usage in controller:
def publish
  if ArticlePublisher.new(@article, current_user).publish
    redirect_to @article, notice: 'Article published successfully.'
  else
    redirect_to @article, alert: 'Failed to publish article.'
  end
end
```

## Query Objects

Use query objects to encapsulate complex queries and keep models clean.

```ruby
# app/queries/article_query.rb
class ArticleQuery
  def initialize(relation = Article.all)
    @relation = relation
  end

  def published
    @relation.where(status: 'published')
  end

  def by_author(user)
    @relation.where(user: user)
  end

  def recent(days = 7)
    @relation.where('created_at >= ?', days.days.ago)
  end

  def popular(min_views = 100)
    @relation.where('views_count >= ?', min_views)
  end

  def search(query)
    @relation.where('title LIKE ? OR body LIKE ?', "%#{query}%", "%#{query}%")
  end
end

# Usage in controller:
def index
  query = ArticleQuery.new
  @articles = query.published.recent.popular
  @articles = query.by_author(User.find(params[:author_id])) if params[:author_id]
  @articles = query.search(params[:q]) if params[:q]
end
```

## Form Objects

Use form objects for complex forms that don't map to a single model.

```ruby
# app/forms/user_registration_form.rb
class UserRegistrationForm
  include ActiveModel::Model

  attr_accessor :email, :password, :password_confirmation,
                :first_name, :last_name, :company_name

  validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }
  validates :password, presence: true, length: { minimum: 8 }
  validates :password_confirmation, presence: true
  validate :passwords_match
  validates :first_name, :last_name, :company_name, presence: true

  def save
    return false unless valid?

    ActiveRecord::Base.transaction do
      create_user
      create_company
      assign_user_to_company
      send_welcome_email
    end

    true
  rescue => e
    errors.add(:base, e.message)
    false
  end

  private

  def passwords_match
    if password != password_confirmation
      errors.add(:password_confirmation, "doesn't match password")
    end
  end

  def create_user
    @user = User.create!(
      email: email,
      password: password,
      first_name: first_name,
      last_name: last_name
    )
  end

  def create_company
    @company = Company.create!(name: company_name)
  end

  def assign_user_to_company
    @user.update!(company: @company)
  end

  def send_welcome_email
    UserMailer.welcome_email(@user).deliver_later
  end
end

# Usage in controller:
def create
  @form = UserRegistrationForm.new(registration_params)

  if @form.save
    redirect_to root_path, notice: 'Registration successful.'
  else
    render :new, status: :unprocessable_entity
  end
end
```

## Decorators/Presenters

Use decorators to handle presentation logic and keep views clean.

```ruby
# app/decorators/article_decorator.rb
class ArticleDecorator
  def initialize(article)
    @article = article
  end

  def formatted_published_date
    return 'Draft' unless @article.published_at

    if @article.published_at > 1.week.ago
      "#{time_ago_in_words(@article.published_at)} ago"
    else
      @article.published_at.strftime('%B %d, %Y')
    end
  end

  def status_badge_class
    case @article.status
    when 'published' then 'badge-success'
    when 'draft' then 'badge-secondary'
    when 'archived' then 'badge-warning'
    else 'badge-light'
    end
  end

  def excerpt(length = 200)
    return '' if @article.body.blank?

    if @article.body.length > length
      "#{@article.body[0...length]}..."
    else
      @article.body
    end
  end

  def reading_time
    words = @article.body.split.size
    minutes = (words / 200.0).ceil
    "#{minutes} min read"
  end

  # Delegate missing methods to the article
  def method_missing(method, *args, &block)
    @article.send(method, *args, &block)
  end

  def respond_to_missing?(method, include_private = false)
    @article.respond_to?(method, include_private) || super
  end
end

# Usage in controller:
def show
  @article = ArticleDecorator.new(Article.find(params[:id]))
end

# Usage in view:
<%= @article.formatted_published_date %>
<span class="<%= @article.status_badge_class %>"><%= @article.status %></span>
<%= @article.reading_time %>
```

## Summary

### Red Flags to Watch For

- ❌ Methods longer than 15 lines
- ❌ Controllers with more than 7 actions
- ❌ Models with more than 20 public methods
- ❌ Deep nesting (3+ levels)
- ❌ Multiple responsibilities in one class/method
- ❌ Callback chains performing complex logic

### Refactoring Checklist

- ✅ Extract long methods into smaller, focused methods
- ✅ Use service objects for complex business logic
- ✅ Use query objects for complex database queries
- ✅ Use form objects for multi-model forms
- ✅ Use decorators for presentation logic
- ✅ Apply early returns to reduce nesting
- ✅ Keep controllers thin (only handle request/response)
- ✅ Keep models focused on data and associations
