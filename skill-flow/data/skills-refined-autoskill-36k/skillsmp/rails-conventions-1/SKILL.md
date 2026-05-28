---
name: rails-conventions
description: This skill should be used when the user asks about "Rails conventions", "Rails best practices", "Rails file structure", "MVC patterns", "naming conventions", "Rails Way", "convention over configuration", "where to put code", "Rails architecture", or needs guidance on organizing Rails application code following established conventions.
version: 1.1.0
---

# Rails Conventions

Comprehensive guide to Ruby on Rails conventions, the Rails Way philosophy, and best practices for organizing Rails 7+ applications.

## Core Philosophy

Rails follows "Convention over Configuration" - sensible defaults reduce decision fatigue and boilerplate. Learn the conventions to write less code and collaborate effectively.

### The Rails Way Principles

1. **DRY (Don't Repeat Yourself)** - Extract duplication into helpers, concerns, or services
2. **Convention over Configuration** - Follow naming patterns, get automatic wiring
3. **Fat Models, Skinny Controllers** - Business logic in models, controllers handle HTTP
4. **RESTful Design** - Resources map to standard CRUD actions

## File Structure (Rails 7+)

```
app/
├── controllers/          # Handle HTTP requests
│   ├── concerns/         # Shared controller modules
│   └── application_controller.rb
├── models/               # Business logic and data
│   ├── concerns/         # Shared model modules
│   └── application_record.rb
├── views/                # Templates
│   ├── layouts/          # Page wrappers
│   └── shared/           # Partials used across views
├── helpers/              # View helper methods
├── mailers/              # Email logic
├── jobs/                 # Background jobs (ActiveJob)
├── channels/             # ActionCable WebSocket channels
└── javascript/           # Hotwire/Stimulus (import maps)
    └── controllers/      # Stimulus controllers

config/
├── routes.rb             # URL routing
├── database.yml          # Database configuration
├── credentials.yml.enc   # Encrypted secrets
└── initializers/         # Startup configuration

db/
├── migrate/              # Database migrations
├── schema.rb             # Current schema (auto-generated)
└── seeds.rb              # Seed data

lib/
├── tasks/                # Custom Rake tasks
└── [custom modules]      # Non-Rails-specific code

test/                     # Tests (Minitest)
```

## Naming Conventions

### Models

| Convention | Example | Notes |
|------------|---------|-------|
| Class name | `User`, `BlogPost` | Singular, CamelCase |
| File name | `user.rb`, `blog_post.rb` | Singular, snake_case |
| Table name | `users`, `blog_posts` | Plural, snake_case |
| Foreign key | `user_id`, `blog_post_id` | Singular + `_id` |

### Controllers

| Convention | Example | Notes |
|------------|---------|-------|
| Class name | `UsersController` | Plural + Controller |
| File name | `users_controller.rb` | Plural, snake_case |
| Actions | `index`, `show`, `new`, `create`, `edit`, `update`, `destroy` | RESTful |

### Views

| Convention | Example |
|------------|---------|
| Directory | `app/views/users/` |
| Template | `index.html.erb`, `show.html.erb` |
| Partial | `_user.html.erb`, `_form.html.erb` |
| Layout | `application.html.erb` |

## RESTful Routes

Standard resource routes map to controller actions:

```ruby
# config/routes.rb
resources :articles do
  resources :comments, only: [:create, :destroy]
end
```

| HTTP Verb | Path | Controller#Action | Purpose |
|-----------|------|-------------------|---------|
| GET | /articles | articles#index | List all |
| GET | /articles/new | articles#new | New form |
| POST | /articles | articles#create | Create |
| GET | /articles/:id | articles#show | Show one |
| GET | /articles/:id/edit | articles#edit | Edit form |
| PATCH/PUT | /articles/:id | articles#update | Update |
| DELETE | /articles/:id | articles#destroy | Delete |

### Custom Routes

Add member and collection routes when needed:

```ruby
resources :articles do
  member do
    post :publish      # POST /articles/:id/publish
  end
  collection do
    get :drafts        # GET /articles/drafts
  end
end
```

## Controller Conventions

### Standard Controller Pattern

```ruby
class ArticlesController < ApplicationController
  before_action :set_article, only: [:show, :edit, :update, :destroy]

  def index
    @articles = Article.all
  end

  def show; end

  def new
    @article = Article.new
  end

  def create
    @article = Article.new(article_params)
    if @article.save
      redirect_to @article, notice: "Article created."
    else
      render :new, status: :unprocessable_entity
    end
  end

  def edit; end

  def update
    if @article.update(article_params)
      redirect_to @article, notice: "Article updated."
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def destroy
    @article.destroy
    redirect_to articles_url, notice: "Article deleted."
  end

  private

  def set_article
    @article = Article.find(params[:id])
  end

  def article_params
    params.require(:article).permit(:title, :body, :published)
  end
end
```

### Strong Parameters

Always whitelist permitted parameters:

```ruby
def article_params
  params.require(:article).permit(:title, :body, :published, tag_ids: [])
end
```

## Model Conventions

### Standard Model Structure

```ruby
class Article < ApplicationRecord
  # Constants first
  STATUSES = %w[draft published archived].freeze

  # Associations
  belongs_to :author, class_name: "User"
  has_many :comments, dependent: :destroy
  has_many :taggings, dependent: :destroy
  has_many :tags, through: :taggings

  # Validations
  validates :title, presence: true, length: { maximum: 255 }
  validates :body, presence: true
  validates :status, inclusion: { in: STATUSES }

  # Callbacks (use sparingly)
  before_validation :normalize_title
  after_create :notify_subscribers

  # Scopes
  scope :published, -> { where(status: "published") }
  scope :recent, -> { order(created_at: :desc) }
  scope :by_author, ->(author) { where(author: author) }

  # Class methods
  def self.search(query)
    where("title ILIKE ?", "%#{query}%")
  end

  # Instance methods
  def publish!
    update!(status: "published", published_at: Time.current)
  end

  private

  def normalize_title
    self.title = title&.strip&.titleize
  end

  def notify_subscribers
    ArticleNotificationJob.perform_later(self)
  end
end
```

## Concerns

Extract shared behavior into concerns:

```ruby
# app/models/concerns/publishable.rb
module Publishable
  extend ActiveSupport::Concern

  included do
    scope :published, -> { where.not(published_at: nil) }
    scope :draft, -> { where(published_at: nil) }
  end

  def published?
    published_at.present?
  end

  def publish!
    update!(published_at: Time.current)
  end
end

# app/models/article.rb
class Article < ApplicationRecord
  include Publishable
end
```

## Service Objects

For complex business logic, use service objects in `app/services/`:

```ruby
# app/services/article_publisher.rb
class ArticlePublisher
  def initialize(article, user:)
    @article = article
    @user = user
  end

  def call
    return failure("Not authorized") unless @user.can_publish?(@article)
    return failure("Already published") if @article.published?

    ActiveRecord::Base.transaction do
      @article.publish!
      notify_subscribers
      track_analytics
    end

    success(@article)
  rescue StandardError => e
    failure(e.message)
  end

  private

  def notify_subscribers
    # notification logic
  end

  def track_analytics
    # analytics logic
  end

  def success(result)
    OpenStruct.new(success?: true, result: result)
  end

  def failure(error)
    OpenStruct.new(success?: false, error: error)
  end
end
```

## Where to Put Code

| Code Type | Location | Example |
|-----------|----------|---------|
| Business logic | Models or Services | Validation, calculations |
| HTTP handling | Controllers | Params, redirects, rendering |
| View formatting | Helpers or View Components | Date formatting, HTML helpers |
| Background work | Jobs | Email sending, API calls |
| Database queries | Models (scopes) | Complex queries |
| External APIs | `lib/` or Services | API wrappers |
| Shared behavior | Concerns | Reusable modules |

## Best Practices

1. **Keep controllers thin** - Move logic to models or services
2. **Use scopes** - Named queries are reusable and testable
3. **Validate early** - Database constraints + model validations
4. **Use concerns wisely** - For truly shared behavior, not just to shrink files
5. **Prefer composition** - Service objects over massive models
6. **Follow REST** - Custom actions are a smell; consider new resources

## Additional Resources

### Reference Files

- **`references/advanced-patterns.md`** - Service objects, query objects, form objects
- **`references/code-organization.md`** - When models get too big
