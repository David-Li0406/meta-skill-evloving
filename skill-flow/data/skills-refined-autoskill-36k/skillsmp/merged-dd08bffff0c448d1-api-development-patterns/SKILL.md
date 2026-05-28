---
name: api-development-patterns
description: Comprehensive guide to building production-ready REST APIs in Rails with serialization, authentication, versioning, rate limiting, and testing.
---

# API Development Patterns

Complete patterns and best practices for building production-grade REST APIs in Rails 7.x/8.x.

## RESTful API Conventions

### Resource-Oriented Design

**Core Principles:**
- Resources are nouns (not verbs): `/users`, `/posts`, not `/get_user`
- Use HTTP methods for actions: GET (read), POST (create), PATCH/PUT (update), DELETE (destroy)
- Nest resources for relationships, but limit nesting to 1-2 levels
- Use plural resource names: `/users` not `/user`

**Standard Resource Routes:**

```ruby
# config/routes.rb
Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :posts do
        resources :comments, only: [:index, :create] # Nested but limited
        member do
          post :publish
          post :archive
        end
        collection do
          get :trending
        end
      end

      # Flat route for comments by ID (better than deep nesting)
      resources :comments, only: [:show, :update, :destroy]
    end
  end
end
```

### HTTP Methods & Status Codes

**Standard API Actions:**

| Method | Action | Success Status | Body |
|--------|--------|----------------|------|
| GET | Index/List | 200 OK | Resource array + pagination |
| GET | Show | 200 OK | Single resource |
| POST | Create | 201 Created | Created resource |
| PATCH/PUT | Update | 200 OK | Updated resource |
| DELETE | Destroy | 204 No Content | Empty |

**Error Status Codes:**

| Code | Meaning | When to Use |
|------|---------|-------------|
| 400 | Bad Request | Invalid JSON, malformed request |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Maintenance mode, overloaded |

**Controller Example:**

```ruby
# app/controllers/api/v1/posts_controller.rb
module Api
  module V1
    class PostsController < Api::BaseController
      before_action :authenticate_api_user!
      before_action :set_post, only: [:show, :update, :destroy]

      def index
        @posts = Post.published
                     .page(params[:page])
                     .per(params[:per_page] || 25)

        render json: PostBlueprint.render(@posts, root: :posts), status: :ok
      end

      def show
        render json: PostBlueprint.render(@post), status: :ok
      end

      def create
        @post = Current.user.posts.build(post_params)

        if @post.save
          render json: PostBlueprint.render(@post), status: :created, location: api_v1_post_url(@post)
        else
          render json: { errors: @post.errors }, status: :unprocessable_entity
        end
      end

      def update
        if @post.update(post_params)
          render json: PostBlueprint.render(@post), status: :ok
        else
          render json: { errors: @post.errors }, status: :unprocessable_entity
        end
      end

      def destroy
        @post.destroy
        head :no_content
      end

      private

      def set_post
        @post = Post.find(params[:id])
      rescue ActiveRecord::RecordNotFound
        render json: { error: "Post not found" }, status: :not_found
      end

      def post_params
        params.require(:post).permit(:title, :body, :published_at, tag_ids: [])
      end
    end
  end
end
```

---

## Serialization Patterns

### Blueprinter (Recommended)

**Installation:**

```ruby
# Gemfile
gem 'blueprinter'
gem 'oj' # Fast JSON parser
```

**Basic Blueprint:**

```ruby
# app/blueprints/post_blueprint.rb
class PostBlueprint < Blueprinter::Base
  identifier :id

  fields :title, :body, :published_at, :created_at

  field :slug do |post|
    post.title.parameterize
  end

  association :author, blueprint: UserBlueprint, view: :compact

  association :comments, blueprint: CommentBlueprint do |post, options|
    post.comments.limit(options[:comment_limit] || 10)
  end

  view :compact do
    fields :id, :title, :slug
  end

  view :extended do
    include_view :default
    fields :view_count, :like_count
    association :tags, blueprint: TagBlueprint
  end
end
```

**Using Views:**

```ruby
# Compact view for lists
PostBlueprint.render(@posts, view: :compact, root: :posts)

# Extended view for show
PostBlueprint.render(@post, view: :extended)

# Pass options to associations
PostBlueprint.render(@post, comment_limit: 5)
```

### JSONAPI::Serializer (Alternative)

**For JSON:API Specification Compliance:**

```ruby
# Gemfile
gem 'jsonapi-serializer'

# app/serializers/post_serializer.rb
class PostSerializer
  include JSONAPI::Serializer

  attributes :title, :body, :published_at

  belongs_to :author, serializer: UserSerializer
  has_many :comments, serializer: CommentSerializer

  attribute :slug do |post|
    post.title.parameterize
  end

  link :self do |post|
    Rails.application.routes.url_helpers.api_v1_post_url(post)
  end
end

# Usage
PostSerializer.new(@posts, include: [:author, :comments]).serializable_hash
```

### Alba (Lightweight Alternative)

```ruby
# Gemfile
gem 'alba'

# app/serializers/post_serializer.rb
class PostSerializer
  include Alba::Resource

  attributes :id, :title, :body, :published_at

  one :author, resource: UserSerializer
  many :comments, resource: CommentSerializer

  attribute :slug do |post|
    post.title.parameterize
  end
end

# Usage
PostSerializer.new(@posts).serialize
```

---

## Authentication

### JWT (JSON Web Tokens)

**Installation:**

```ruby
# Gemfile
gem 'jwt'
gem 'bcrypt' # For password hashing
```

**JWT Service:**

```ruby
# app/services/json_web_token_service.rb
class JsonWebTokenService
  SECRET_KEY = Rails.application.credentials.secret_key_base
  ALGORITHM = 'HS256'

  def self.encode(payload, expiration = 24.hours.from_now)
    payload[:exp] = expiration.to_i
    JWT.encode(payload, SECRET_KEY, ALGORITHM)
  end

  def self.decode(token)
    decoded = JWT.decode(token, SECRET_KEY, true, algorithm: ALGORITHM)[0]
    HashWithIndifferentAccess.new(decoded)
  rescue JWT::DecodeError, JWT::ExpiredSignature => e
    nil
  end
end
```

**Authentication Controller:**

```ruby
# app/controllers/api/v1/authentication_controller.rb
module Api
  module V1
    class AuthenticationController < Api::BaseController
      skip_before_action :authenticate_api_user!, only: [:create]

      def create
        user = User.find_by(email: params[:email])

        if user&.authenticate(params[:password])
          token = JsonWebTokenService.encode(user_id: user.id)
          render json: {
            token: token,
            user: UserBlueprint.render_as_hash(user)
          }, status: :ok
        else
          render json: { error: 'Invalid credentials' }, status: :unauthorized
        end
      end

      def destroy
        # Implement token revocation (requires Redis/database storage)
        head :no_content
      end
    end
  end
end
```

**Base Controller with JWT Authentication:**

```ruby
# app/controllers/api/base_controller.rb
module Api
  class BaseController < ActionController::API
    before_action :authenticate_api_user!

    rescue_from ActiveRecord::RecordNotFound, with: :not_found
    rescue_from ActionController::ParameterMissing, with: :bad_request

    private

    def authenticate_api_user!
      token = request.headers['Authorization']&.split(' ')&.last
      return render_unauthorized unless token

      decoded_token = JsonWebTokenService.decode(token)
      return render_unauthorized unless decoded_token

      @current_user = User.find_by(id: decoded_token[:user_id])
      return render_unauthorized unless @current_user

      # Store in Current for easy access
      Current.user = @current_user
    rescue
      render_unauthorized
    end

    def current_user
      @current_user
    end

    def render_unauthorized
      render json: { error: 'Unauthorized' }, status: :unauthorized
    end

    def not_found
      render json: { error: 'Resource not found' }, status: :not_found
    end

    def bad_request
      render json: { error: 'Bad request' }, status: :bad_request
    end
  end
end
```

### API Keys (Alternative)

**For Service-to-Service Authentication:**

```ruby
# Migration
create_table :api_keys do |t|
  t.references :user, null: false, foreign_key: true
  t.string :key, null: false, index: { unique: true }
  t.string :name # e.g., "Production Server", "Mobile App"
  t.datetime :last_used_at
  t.datetime :expires_at
  t.timestamps
end

# app/models/api_key.rb
class ApiKey < ApplicationRecord
  belongs_to :user

  before_create :generate_key

  scope :active, -> { where('expires_at IS NULL OR expires_at > ?', Time.current) }

  def self.authenticate(key)
    active.find_by(key: key)&.tap do |api_key|
      api_key.update_column(:last_used_at, Time.current)
    end
  end

  private

  def generate_key
    self.key = SecureRandom.base58(32)
  end
end

# Authentication in controller
def authenticate_api_key!
  key = request.headers['X-API-Key'] || params[:api_key]
  return render_unauthorized unless key

  @api_key = ApiKey.authenticate(key)
  return render_unauthorized unless @api_key

  @current_user = @api_key.user
  Current.user = @current_user
end
```

---

## Authorization

### Pundit for APIs

```ruby
# Gemfile
gem 'pundit'

# app/controllers/api/base_controller.rb
module Api
  class BaseController < ActionController::API
    include Pundit::Authorization

    rescue_from Pundit::NotAuthorizedError, with: :forbidden

    private

    def forbidden
      render json: { error: 'Forbidden' }, status: :forbidden
    end
  end
end

# app/policies/post_policy.rb
class PostPolicy < ApplicationPolicy
  def index?
    true
  end

  def show?
    record.published? || record.author == user
  end

  def create?
    user.present?
  end

  def update?
    record.author == user
  end

  def destroy?
    record.author == user || user.admin?
  end
end

# In controller
def show
  @post = Post.find(params[:id])
  authorize @post
  render json: PostBlueprint.render(@post)
end
```

---

## Versioning Strategies

### URL Versioning (Recommended)

**Routes:**

```ruby
# config/routes.rb
Rails.application.routes.draw do
  namespace :api do
    namespace :v1 do
      resources :posts
    end

    namespace :v2 do
      resources :posts
    end
  end
end
```

**Pros:** Simple, clear, cache-friendly  
**Cons:** URLs change between versions

### Header Versioning

```ruby
# config/routes.rb
namespace :api, defaults: { format: :json } do
  scope module: :v1, constraints: ApiVersion.new('v1', default: true) do
    resources :posts
  end

  scope module: :v2, constraints: ApiVersion.new('v2') do
    resources :posts
  end
end

# lib/api_version.rb
class ApiVersion
  def initialize(version, default = false)
    @version = version
    @default = default
  end

  def matches?(request)
    @default || check_headers(request.headers)
  end

  private

  def check_headers(headers)
    accept = headers['Accept']
    accept&.include?("application/vnd.myapp.#{@version}+json")
  end
end
```

**Usage:**
```
Accept: application/vnd.myapp.v2+json
```

---

## Pagination

### Kaminari

```ruby
# Gemfile
gem 'kaminari'

# Controller
def index
  @posts = Post.published
               .page(params[:page])
               .per(params[:per_page] || 25)

  render json: {
    posts: PostBlueprint.render_as_hash(@posts, view: :compact),
    meta: pagination_meta(@posts)
  }
end

private

def pagination_meta(collection)
  {
    current_page: collection.current_page,
    next_page: collection.next_page,
    prev_page: collection.prev_page,
    total_pages: collection.total_pages,
    total_count: collection.total_count,
    per_page: collection.limit_value
  }
end
```

### pagy (Faster Alternative)

```ruby
# Gemfile
gem 'pagy'

# app/controllers/api/base_controller.rb
include Pagy::Backend

def index
  @pagy, @posts = pagy(Post.published, items: params[:per_page] || 25)

  render json: {
    posts: PostBlueprint.render_as_hash(@posts),
    meta: pagy_metadata(@pagy)
  }
end

private

def pagy_metadata(pagy_object)
  {
    current_page: pagy_object.page,
    next_page: pagy_object.next,
    prev_page: pagy_object.prev,
    total_pages: pagy_object.pages,
    total_count: pagy_object.count,
    per_page: pagy_object.items
  }
end
```

---

## Rate Limiting

### Rack::Attack

```ruby
# Gemfile
gem 'rack-attack'

# config/initializers/rack_attack.rb
class Rack::Attack
  # Throttle all requests by IP
  throttle('req/ip', limit: 300, period: 5.minutes) do |req|
    req.ip if req.path.start_with?('/api/')
  end

  # Throttle API requests by authentication token
  throttle('api/token', limit: 1000, period: 1.hour) do |req|
    req.env['HTTP_AUTHORIZATION']&.split(' ')&.last if req.path.start_with?('/api/')
  end

  # Throttle login attempts
  throttle('logins/email', limit: 5, period: 20.minutes) do |req|
    if req.path == '/api/v1/login' && req.post?
      req.params['email'].to_s.downcase.gsub(/\s+/, "")
    end
  end

  # Block specific IPs
  blocklist('block bad IPs') do |req|
    # Read from Redis or database
    Redis.current.sismember('blocked_ips', req.ip)
  end

  # Custom response for throttled requests
  self.throttled_responder = lambda do |env|
    retry_after = env['rack.attack.match_data'][:period]
    [
      429,
      {
        'Content-Type' => 'application/json',
        'Retry-After' => retry_after.to_s
      },
      [{ error: 'Rate limit exceeded', retry_after: retry_after }.to_json]
    ]
  end