---
name: api-endpoint
description: Generate JSON API endpoints with authentication and versioning. Use when user needs API, mobile backend, external integration, or says "create API", "add endpoint", "JSON response", "API for mobile", "REST API".
---

# API Endpoint Generator

Generate RESTful JSON API endpoints with authentication, versioning, and documentation.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Design API endpoint structure
- [ ] 2. Create API controller
- [ ] 3. Add routes with versioning
- [ ] 4. Implement authentication
- [ ] 5. Add serialization
- [ ] 6. Handle errors
- [ ] 7. Test with curl/Postman
- [ ] 8. Document endpoints
```

## API Structure

```
app/controllers/api/
├── v1/
│   ├── base_controller.rb
│   ├── posts_controller.rb
│   ├── users_controller.rb
│   └── sessions_controller.rb
└── v2/
    └── ...
```

## Base Controller

```ruby
# app/controllers/api/v1/base_controller.rb
module Api
  module V1
    class BaseController < ApplicationController
      skip_before_action :verify_authenticity_token
      before_action :authenticate_api_user

      rescue_from ActiveRecord::RecordNotFound, with: :not_found
      rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity

      private

      def authenticate_api_user
        token = request.headers["Authorization"]&.split(" ")&.last
        @current_api_user = User.find_by(api_token: token)

        unless @current_api_user
          render json: { error: "Unauthorized" }, status: :unauthorized
        end
      end

      def current_api_user
        @current_api_user
      end

      def not_found
        render json: { error: "Resource not found" }, status: :not_found
      end

      def unprocessable_entity(exception)
        render json: { errors: exception.record.errors.full_messages }, status: :unprocessable_entity
      end
    end
  end
end
```

## Resource Controller

```ruby
# app/controllers/api/v1/posts_controller.rb
module Api
  module V1
    class PostsController < BaseController
      before_action :set_post, only: [:show, :update, :destroy]

      # GET /api/v1/posts
      def index
        @posts = Post.includes(:user).order(created_at: :desc).limit(50)

        render json: {
          data: @posts.map { |post| post_json(post) },
          meta: {
            total: @posts.count,
            page: 1,
            per_page: 50
          }
        }
      end

      # GET /api/v1/posts/:id
      def show
        render json: { data: post_json(@post) }
      end

      # POST /api/v1/posts
      def create
        @post = current_api_user.posts.build(post_params)

        if @post.save
          render json: { data: post_json(@post) }, status: :created
        else
          render json: { errors: @post.errors.full_messages }, status: :unprocessable_entity
        end
      end

      # PATCH /api/v1/posts/:id
      def update
        if @post.user != current_api_user
          return render json: { error: "Forbidden" }, status: :forbidden
        end

        if @post.update(post_params)
          render json: { data: post_json(@post) }
        else
          render json: { errors: @post.errors.full_messages }, status: :unprocessable_entity
        end
      end

      # DELETE /api/v1/posts/:id
      def destroy
        if @post.user != current_api_user
          return render json: { error: "Forbidden" }, status: :forbidden
        end

        @post.destroy
        head :no_content
      end

      private

      def set_post
        @post = Post.find(params[:id])
      end

      def post_params
        params.require(:post).permit(:title, :content, :status)
      end

      def post_json(post)
        {
          id: post.id,
          title: post.title,
          content: post.content,
          status: post.status,
          likes_count: post.likes_count,
          comments_count: post.comments_count,
          created_at: post.created_at.iso8601,
          updated_at: post.updated_at.iso8601,
          user: {
            id: post.user.id,
            name: post.user.name,
            avatar_url: post.user.avatar_url
          }
        }
      end
    end
  end
end
```

## Routes

```ruby
# config/routes.rb
namespace :api do
  namespace :v1 do
    resources :posts, only: [:index, :show, :create, :update, :destroy]
    resources :users, only: [:show, :create, :update]

    post "sessions", to: "sessions#create"
    delete "sessions", to: "sessions#destroy"
  end
end
```

## Authentication

### Token-Based

**Generate Token**:
```ruby
# app/models/user.rb
class User < ApplicationRecord
  has_secure_token :api_token

  def regenerate_api_token
    regenerate_api_token
  end
end
```

**Migration**:
```ruby
add_column :users, :api_token, :string
add_index :users, :api_token, unique: true
```

**Login Endpoint**:
```ruby
# app/controllers/api/v1/sessions_controller.rb
module Api
  module V1
    class SessionsController < BaseController
      skip_before_action :authenticate_api_user, only: [:create]

      def create
        user = User.find_by(email: params[:email])

        if user&.authenticate(params[:password])
          render json: {
            data: {
              token: user.api_token,
              user: user_json(user)
            }
          }, status: :created
        else
          render json: { error: "Invalid credentials" }, status: :unauthorized
        end
      end

      def destroy
        current_api_user.regenerate_api_token
        head :no_content
      end

      private

      def user_json(user)
        {
          id: user.id,
          email: user.email,
          name: user.name
        }
      end
    end
  end
end
```

**Client Usage**:
```bash
# Login
curl -X POST http://localhost:3000/api/v1/sessions \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Use token
curl http://localhost:3000/api/v1/posts \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Response Format

### Success (200/201)
```json
{
  "data": {
    "id": 1,
    "title": "Post Title",
    "content": "Content here"
  }
}
```

### List (200)
```json
{
  "data": [
    { "id": 1, "title": "Post 1" },
    { "id": 2, "title": "Post 2" }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "per_page": 50
  }
}
```

### Error (4xx/5xx)
```json
{
  "error": "Resource not found"
}
```

### Validation Error (422)
```json
{
  "errors": [
    "Title can't be blank",
    "Content is too short"
  ]
}
```

## Pagination

```ruby
def index
  page = params[:page]&.to_i || 1
  per_page = params[:per_page]&.to_i || 20
  per_page = 100 if per_page > 100 # Max limit

  @posts = Post.order(created_at: :desc)
                .limit(per_page)
                .offset((page - 1) * per_page)

  render json: {
    data: @posts.map { |post| post_json(post) },
    meta: {
      total: Post.count,
      page: page,
      per_page: per_page,
      total_pages: (Post.count.to_f / per_page).ceil
    }
  }
end
```

## Serialization (Optional)

**Using Jbuilder**:
```ruby
# app/views/api/v1/posts/index.json.jbuilder
json.data @posts do |post|
  json.id post.id
  json.title post.title
  json.content post.content
  json.user do
    json.id post.user.id
    json.name post.user.name
  end
end

json.meta do
  json.total @posts.count
end
```

**Controller**:
```ruby
def index
  @posts = Post.includes(:user).limit(50)
  # Renders app/views/api/v1/posts/index.json.jbuilder
end
```

## CORS (for JavaScript clients)

**Gemfile**:
```ruby
gem 'rack-cors'
```

**config/initializers/cors.rb**:
```ruby
Rails.application.config.middleware.insert_before 0, Rack::Cors do
  allow do
    origins 'localhost:3001', 'example.com' # Your frontend domains

    resource '/api/*',
      headers: :any,
      methods: [:get, :post, :put, :patch, :delete, :options, :head],
      credentials: true
  end
end
```

## Testing

**RSpec** (optional):
```ruby
# spec/requests/api/v1/posts_spec.rb
RSpec.describe "Api::V1::Posts", type: :request do
  let(:user) { create(:user) }
  let(:headers) { { "Authorization" => "Bearer #{user.api_token}" } }

  describe "GET /api/v1/posts" do
    it "returns posts" do
      create_list(:post, 3)

      get "/api/v1/posts", headers: headers

      expect(response).to have_http_status(:success)
      expect(JSON.parse(response.body)["data"].count).to eq(3)
    end
  end

  describe "POST /api/v1/posts" do
    it "creates a post" do
      post_params = { title: "New Post", content: "Content here" }

      post "/api/v1/posts", params: { post: post_params }, headers: headers

      expect(response).to have_http_status(:created)
      expect(JSON.parse(response.body)["data"]["title"]).to eq("New Post")
    end
  end
end
```

## Documentation

**README section**:
```markdown
## API Documentation

### Authentication

All API requests require authentication via Bearer token.

```bash
Authorization: Bearer YOUR_TOKEN_HERE
```

### Endpoints

**GET /api/v1/posts**
- Returns list of posts
- Params: `page`, `per_page`

**POST /api/v1/posts**
- Create new post
- Body: `{ "post": { "title": "...", "content": "..." } }`

**GET /api/v1/posts/:id**
- Returns single post

**PATCH /api/v1/posts/:id**
- Update post (owner only)

**DELETE /api/v1/posts/:id**
- Delete post (owner only)
```

## Best Practices

1. **Versioning**: Always use `/api/v1/` namespace
2. **Authentication**: Token in `Authorization` header
3. **Consistent Format**: `{ data: {}, meta: {} }`
4. **Error Handling**: Proper HTTP status codes
5. **N+1 Prevention**: Use `includes()` in queries
6. **Rate Limiting**: Consider adding (e.g., rack-attack gem)
7. **HTTPS Only**: In production

## Checklist

- [ ] API controller created in `app/controllers/api/v1/`
- [ ] Inherits from BaseController
- [ ] Routes added with `namespace :api, :v1`
- [ ] Authentication implemented
- [ ] JSON responses with `data` and `meta`
- [ ] Error handling for 404, 422, 401, 403
- [ ] CORS configured if needed
- [ ] Tested with curl or Postman
- [ ] API documented
