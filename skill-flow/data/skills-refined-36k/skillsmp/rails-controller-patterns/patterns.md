# Controller Patterns for Rails

Detailed patterns for Rails controllers.

## Response Handling

### Multiple Formats

```ruby
def show
  @post = Post.find(params[:id])

  respond_to do |format|
    format.html
    format.json { render json: @post }
    format.turbo_stream
  end
end

def create
  @post = current_user.posts.build(post_params)

  respond_to do |format|
    if @post.save
      format.html { redirect_to @post, notice: 'Created!' }
      format.json { render json: @post, status: :created }
      format.turbo_stream
    else
      format.html { render :new, status: :unprocessable_entity }
      format.json { render json: @post.errors, status: :unprocessable_entity }
      format.turbo_stream { render :form_errors, status: :unprocessable_entity }
    end
  end
end
```

### JSON API

```ruby
class Api::V1::PostsController < Api::V1::BaseController
  def index
    @posts = Post.includes(:user).page(params[:page])
    render json: @posts, each_serializer: PostSerializer
  end

  def show
    @post = Post.find(params[:id])
    render json: @post, serializer: PostSerializer
  end

  def create
    @post = current_user.posts.build(post_params)

    if @post.save
      render json: @post, status: :created
    else
      render json: { errors: @post.errors }, status: :unprocessable_entity
    end
  end
end
```

## Before Actions

### Common Patterns

```ruby
class PostsController < ApplicationController
  before_action :authenticate_user!
  before_action :set_post, only: [:show, :edit, :update, :destroy]
  before_action :authorize_post!, only: [:edit, :update, :destroy]

  private

  def set_post
    @post = Post.find(params[:id])
  end

  def authorize_post!
    redirect_to posts_path, alert: 'Not authorized' unless @post.user == current_user
  end
end
```

### Skipping Filters

```ruby
class SessionsController < ApplicationController
  skip_before_action :authenticate_user!, only: [:new, :create]
end
```

## Error Handling

### Rescue From

```ruby
class ApplicationController < ActionController::Base
  rescue_from ActiveRecord::RecordNotFound, with: :not_found
  rescue_from Pundit::NotAuthorizedError, with: :forbidden

  private

  def not_found
    respond_to do |format|
      format.html { render 'errors/not_found', status: :not_found }
      format.json { render json: { error: 'Not found' }, status: :not_found }
    end
  end

  def forbidden
    respond_to do |format|
      format.html { redirect_to root_path, alert: 'Access denied' }
      format.json { render json: { error: 'Forbidden' }, status: :forbidden }
    end
  end
end
```

### Manual Error Handling

```ruby
def create
  @post = current_user.posts.build(post_params)

  if @post.save
    redirect_to @post
  else
    flash.now[:alert] = 'Could not create post'
    render :new, status: :unprocessable_entity
  end
rescue ExternalServiceError => e
  flash[:alert] = 'Service temporarily unavailable'
  redirect_to posts_path
end
```

## Routing

### RESTful Resources

```ruby
# config/routes.rb
Rails.application.routes.draw do
  resources :posts do
    resources :comments, shallow: true
    member do
      post :publish
      delete :archive
    end
    collection do
      get :search
      get :drafts
    end
  end
end
```

### Resource-Based Controllers (Preferred Pattern)

Instead of custom member actions, create dedicated resource controllers. This pattern treats state changes as resources themselves, providing cleaner RESTful design.

**Context Awareness**: Always applicable - improves on traditional custom actions.

```ruby
# Bad - custom actions
resources :cards do
  post :close
  post :reopen
  post :pin
  post :unpin
end

# Good - resource controllers
resources :cards do
  scope module: :cards do
    resource :closure      # create = close, destroy = reopen
    resource :pin          # create = pin, destroy = unpin
    resource :watch        # create = watch, destroy = unwatch
    resource :goldness     # create = gild, destroy = ungild
    resource :triage       # create = move to triage
  end
end
```

**Example Controller Implementation**:

```ruby
class Cards::ClosuresController < ApplicationController
  include CardScoped

  def create
    @card.close
    respond_to do |format|
      format.turbo_stream { render_card_replacement }
      format.json { head :no_content }
    end
  end

  def destroy
    @card.reopen
    respond_to do |format|
      format.turbo_stream { render_card_replacement }
      format.json { head :no_content }
    end
  end
end
```

**Benefits**:
- RESTful HTTP verbs (POST to create state, DELETE to remove state)
- Clear, focused controllers
- Easier to test and maintain
- Natural fit with Turbo Streams

### Nested Resources

```ruby
resources :users do
  resources :posts, only: [:index, :new, :create]
end

# Generates:
# GET    /users/:user_id/posts
# GET    /users/:user_id/posts/new
# POST   /users/:user_id/posts
```

### Namespaced Routes

```ruby
namespace :admin do
  resources :users
  resources :posts
end

namespace :api do
  namespace :v1 do
    resources :posts, only: [:index, :show, :create]
  end
end
```

### Custom Routes

```ruby
# Singular resource (no :id)
resource :profile, only: [:show, :edit, :update]

# Non-resourceful routes
get 'about', to: 'pages#about'
post 'login', to: 'sessions#create'

# Root route
root 'home#index'
```

## Strong Parameters Patterns

### Modern Strong Params (Rails 7.1+)

**Context Awareness**: Check Rails version before using `params.expect`
- Rails >= 7.1: Use `params.expect` (cleaner, more secure)
- Rails < 7.1: Use `params.require().permit()` (traditional)

**Check Rails version**:
```bash
# In Gemfile.lock, look for:
rails (7.1.x)
```

**Rails 7.1+ - Preferred**:

```ruby
def post_params
  params.expect(post: [:title, :content, :published])
end

def webhook_params
  params
    .expect(webhook: [:name, :url, subscribed_actions: []])
    .merge(board_id: @board.id)
end
```

**Rails < 7.1 - Fallback**:

```ruby
def post_params
  params.require(:post).permit(:title, :content, :published)
end

def webhook_params
  params
    .require(:webhook)
    .permit(:name, :url, subscribed_actions: [])
    .merge(board_id: @board.id)
end
```

### Nested Attributes

```ruby
def user_params
  params.expect(user: [
    :name,
    :email,
    profile_attributes: [:bio, :website, :id, :_destroy],
    addresses_attributes: [:street, :city, :id, :_destroy]
  ])
end
```

### Dynamic/Hash Attributes

```ruby
def product_params
  params.expect(product: [
    :name,
    :price,
    metadata: {}  # Allow any hash
  ])
end
```

### Array Parameters

```ruby
def post_params
  params.expect(post: [
    :title,
    tag_ids: [],           # Array of IDs
    categories: []         # Array of values
  ])
end
```

## Concerns

### Layered Controller Concerns (Recommended Pattern)

Create concerns that combine before_actions with reusable helper methods. This pattern provides cleaner, more maintainable controllers with shared scoping logic.

**Context Awareness**: Always applicable - improves code reuse and consistency.

```ruby
# app/controllers/concerns/card_scoped.rb
module CardScoped
  extend ActiveSupport::Concern

  included do
    before_action :set_card, :set_board
  end

  private
    def set_card
      @card = Current.user.accessible_cards.find_by!(number: params[:card_id])
    end

    def set_board
      @board = @card.board
    end

    def render_card_replacement
      render turbo_stream: turbo_stream.replace(
        [@card, :card_container],
        partial: "cards/container",
        method: :morph,
        locals: { card: @card.reload }
      )
    end
end

# Usage in multiple controllers
class Cards::ClosuresController < ApplicationController
  include CardScoped
end

class Cards::PinsController < ApplicationController
  include CardScoped
end
```

**Benefits**:
- Combines related before_actions and helper methods
- Reduces duplication across resource controllers
- Clear dependencies and setup
- Easy to test in isolation

### Shared Behavior

```ruby
# app/controllers/concerns/searchable.rb
module Searchable
  extend ActiveSupport::Concern

  included do
    helper_method :search_results
  end

  def search
    @results = search_results
    render :search_results
  end

  private

  def search_results
    model_class.search(params[:q]).page(params[:page])
  end

  def model_class
    controller_name.classify.constantize
  end
end

# Usage
class PostsController < ApplicationController
  include Searchable
end
```

## Authorization Patterns

### Model-Based Authorization (Alternative to Pundit/CanCanCan)

**Context Awareness**: IMPORTANT - Check project dependencies first!

**Detection**: Check `Gemfile` for authorization gems:
```ruby
# If you find these, DO NOT use model-based auth:
gem 'pundit'
gem 'cancancan'
```

**When to Use**:
- New projects without existing authorization
- Simple authorization needs
- User explicitly asks to simplify/remove Pundit

**When NOT to Use**:
- Pundit or CanCanCan already installed
- Complex permission requirements
- Unless migrating away from these gems

**Pattern** (use only if no auth gem present):

```ruby
# In controller
class BoardsController < ApplicationController
  before_action :set_board
  before_action :ensure_permission_to_admin_board, only: [:edit, :update, :destroy]

  private
    def ensure_permission_to_admin_board
      head :forbidden unless Current.user.can_administer_board?(@board)
    end

    def ensure_creatorship
      head :forbidden if Current.user != @comment.creator
    end
end

# In User model
class User < ApplicationRecord
  def can_administer_board?(board)
    admin? || board.creator == self
  end

  def can_change?(other_user)
    admin? || self == other_user
  end
end
```

**Benefits** (when applicable):
- Simpler than full authorization frameworks
- Authorization logic lives with domain models
- Easy to understand and test
- No DSL to learn

**Migration Path**: Only suggest removing Pundit/CanCanCan if user explicitly asks to simplify authorization.

## Pagination Pattern

```ruby
class PostsController < ApplicationController
  def index
    @posts = Post.published
                 .includes(:user, :category)
                 .order(created_at: :desc)
                 .page(params[:page])
                 .per(25)
  end
end
```

## Streaming Responses

```ruby
class ReportsController < ApplicationController
  def export
    respond_to do |format|
      format.csv do
        headers['Content-Disposition'] = 'attachment; filename="report.csv"'
        headers['Content-Type'] = 'text/csv'

        self.response_body = Enumerator.new do |yielder|
          yielder << CSV.generate_line(['ID', 'Name', 'Email'])
          User.find_each do |user|
            yielder << CSV.generate_line([user.id, user.name, user.email])
          end
        end
      end
    end
  end
end
```

## Flash Messages

```ruby
def create
  @post = current_user.posts.build(post_params)

  if @post.save
    redirect_to @post, notice: 'Post created successfully.'
  else
    flash.now[:alert] = 'Could not create post.'
    render :new, status: :unprocessable_entity
  end
end

def destroy
  @post.destroy
  redirect_to posts_path, notice: 'Post deleted.', status: :see_other
end
```

## Status Codes

| Status | Code | Use When |
|--------|------|----------|
| `:ok` | 200 | Successful GET/PUT/PATCH |
| `:created` | 201 | Successful POST |
| `:no_content` | 204 | Successful DELETE (no body) |
| `:see_other` | 303 | Redirect after DELETE |
| `:bad_request` | 400 | Invalid request format |
| `:unauthorized` | 401 | Authentication required |
| `:forbidden` | 403 | Permission denied |
| `:not_found` | 404 | Resource not found |
| `:unprocessable_entity` | 422 | Validation errors |
| `:internal_server_error` | 500 | Server error |

## API Controller Base

```ruby
class Api::V1::BaseController < ActionController::API
  include ActionController::HttpAuthentication::Token::ControllerMethods

  before_action :authenticate_token!

  rescue_from ActiveRecord::RecordNotFound, with: :not_found
  rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity

  private

  def authenticate_token!
    authenticate_or_request_with_http_token do |token, _options|
      @current_user = User.find_by(api_token: token)
    end
  end

  def current_user
    @current_user
  end

  def not_found
    render json: { error: 'Not found' }, status: :not_found
  end

  def unprocessable_entity(exception)
    render json: { errors: exception.record.errors }, status: :unprocessable_entity
  end
end
```

## Context Awareness Reference

Use this table to determine which patterns to apply based on project context:

| Pattern | Detection Method | Conflicts/Blockers | Applicability |
|---------|------------------|-------------------|---------------|
| **Resource Controllers** | Check `config/routes.rb` for custom actions | None - additive pattern | **Always Applicable** - Improves on traditional custom actions |
| **Layered Concerns** | Check `app/controllers/concerns/` | None - additive pattern | **Always Applicable** - Reduces duplication |
| **Model-Based Auth** | Check `Gemfile` for `pundit`, `cancancan` | Pundit/CanCanCan installed | **Conditional** - Only if no auth gem OR explicit migration request |
| **params.expect** | Check `Gemfile.lock` for Rails version (>= 7.1) | Rails < 7.1 | **Rails 7.1+** - Use modern syntax; fallback to .require().permit() for older |

### Detection Steps

**1. Check Rails Version**:
```bash
grep "rails (" Gemfile.lock
# Look for: rails (7.1.x) or higher
```

**2. Check Authorization Gems**:
```bash
grep -E "gem ['\"]pundit|cancancan" Gemfile
# If found: Use existing gem, don't suggest model-based auth
# If not found: Model-based auth is an option
```

**3. Check Routing Style**:
```ruby
# In config/routes.rb, look for:
resources :posts do
  post :publish   # Custom action - candidate for resource controller
  post :archive   # Custom action - candidate for resource controller
end
```

## Best Practices

### Do
- Keep controllers thin
- Use before_actions for repetitive setup
- Return appropriate status codes
- Use strong parameters
- Delegate business logic to models/services
- Check project context before suggesting patterns (see Context Awareness Reference)
- Prefer resource controllers over custom actions
- Use layered concerns for shared setup logic

### Don't
- Put business logic in controllers
- Use instance variables excessively
- Skip validation status codes
- Nest resources more than one level deep
- Create non-RESTful actions without good reason
- Suggest model-based auth when Pundit/CanCanCan is installed
- Use `params.expect` in Rails < 7.1
