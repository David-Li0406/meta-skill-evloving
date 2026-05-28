---
name: action-controller
description: This skill should be used when the user asks about "controllers", "actions", "params", "strong parameters", "filters", "before_action", "after_action", "callbacks", "respond_to", "render", "redirect_to", "flash messages", "sessions", "cookies", "request handling", "routing constraints", or needs guidance on building Rails controllers.
version: 1.0.0
---

# Action Controller

Comprehensive guide to Rails controllers, request handling, filters, and responses.

## Controller Basics

### Naming Conventions

| Convention | Example |
|------------|---------|
| Class name | `ArticlesController` (plural + Controller) |
| File name | `articles_controller.rb` |
| Views directory | `app/views/articles/` |
| Route resource | `resources :articles` |

### Standard RESTful Actions

```ruby
class ArticlesController < ApplicationController
  before_action :set_article, only: [:show, :edit, :update, :destroy]
  before_action :authenticate_user!, except: [:index, :show]

  # GET /articles
  def index
    @articles = Article.published.recent.page(params[:page])
  end

  # GET /articles/:id
  def show
  end

  # GET /articles/new
  def new
    @article = current_user.articles.build
  end

  # POST /articles
  def create
    @article = current_user.articles.build(article_params)

    if @article.save
      redirect_to @article, notice: "Article created successfully."
    else
      render :new, status: :unprocessable_entity
    end
  end

  # GET /articles/:id/edit
  def edit
  end

  # PATCH/PUT /articles/:id
  def update
    if @article.update(article_params)
      redirect_to @article, notice: "Article updated successfully."
    else
      render :edit, status: :unprocessable_entity
    end
  end

  # DELETE /articles/:id
  def destroy
    @article.destroy
    redirect_to articles_url, notice: "Article deleted."
  end

  private

  def set_article
    @article = Article.find(params[:id])
  end

  def article_params
    params.require(:article).permit(:title, :body, :status, tag_ids: [])
  end
end
```

## Strong Parameters

### Basic Usage

```ruby
def article_params
  params.require(:article).permit(:title, :body, :published)
end
```

### Nested Attributes

```ruby
def article_params
  params.require(:article).permit(
    :title,
    :body,
    tag_ids: [],
    comments_attributes: [:id, :body, :_destroy],
    metadata: {}  # Permit hash with any keys
  )
end
```

### Conditional Permitting

```ruby
def article_params
  permitted = [:title, :body]
  permitted << :featured if current_user.admin?
  params.require(:article).permit(permitted)
end
```

### Using expect (Rails 8+)

```ruby
def article_params
  params.expect(article: [:title, :body, :status])
end
```

## Filters (Callbacks)

### Types

```ruby
class ApplicationController < ActionController::Base
  before_action :authenticate_user!
  after_action :log_activity
  around_action :wrap_in_transaction
end
```

### Filter Options

```ruby
class ArticlesController < ApplicationController
  before_action :set_article, only: [:show, :edit, :update, :destroy]
  before_action :authenticate_user!, except: [:index, :show]
  before_action :require_admin, if: :admin_action?
  before_action :check_feature_flag, unless: -> { Rails.env.development? }
  skip_before_action :authenticate_user!, only: [:index]
end
```

### Filter Methods

```ruby
class ApplicationController < ActionController::Base
  before_action :set_locale

  private

  def set_locale
    I18n.locale = params[:locale] || I18n.default_locale
  end

  def authenticate_user!
    redirect_to login_path, alert: "Please sign in" unless current_user
  end

  def require_admin
    head :forbidden unless current_user&.admin?
  end
end
```

## Rendering

### Render Options

```ruby
# Render view for current action
render

# Render specific template
render :edit
render "articles/edit"
render template: "articles/edit"

# Render with status
render :new, status: :unprocessable_entity

# Render partial
render partial: "form"
render partial: "article", locals: { article: @article }
render partial: "article", collection: @articles

# Render inline
render inline: "<%= @article.title %>"
render plain: "OK"
render html: "<strong>Bold</strong>".html_safe
render json: @article
render xml: @article

# Render nothing
head :ok
head :no_content
head :not_found
```

### Render Formats

```ruby
def show
  respond_to do |format|
    format.html
    format.json { render json: @article }
    format.pdf { render pdf: generate_pdf(@article) }
  end
end
```

### Turbo Stream Responses

```ruby
def create
  @comment = @article.comments.build(comment_params)

  if @comment.save
    respond_to do |format|
      format.turbo_stream
      format.html { redirect_to @article }
    end
  else
    render :new, status: :unprocessable_entity
  end
end
```

## Redirects

```ruby
# To URL
redirect_to articles_url
redirect_to article_path(@article)

# To record (resourceful)
redirect_to @article  # Same as article_path(@article)

# With flash message
redirect_to @article, notice: "Saved!"
redirect_to @article, alert: "Warning!"
redirect_to @article, flash: { info: "Custom message" }

# Status codes
redirect_to @article, status: :see_other  # 303
redirect_to @article, status: :moved_permanently  # 301

# Back to referrer
redirect_back(fallback_location: root_path)
redirect_back_or_to root_path  # Rails 7+
```

## Flash Messages

```ruby
class ArticlesController < ApplicationController
  def create
    @article = Article.new(article_params)

    if @article.save
      flash[:notice] = "Article created!"
      redirect_to @article
    else
      flash.now[:alert] = "Please fix the errors."
      render :new
    end
  end

  def update
    if @article.update(article_params)
      redirect_to @article, notice: "Updated!"  # Shorthand
    else
      flash.now[:alert] = "Failed to update."
      render :edit, status: :unprocessable_entity
    end
  end
end
```

### Flash Types

```ruby
# Standard
flash[:notice]  # Success messages
flash[:alert]   # Warning/error messages

# Custom types (add to application_controller.rb)
add_flash_types :info, :warning, :error
```

## Sessions and Cookies

### Sessions

```ruby
# Store
session[:user_id] = user.id
session[:cart] = { items: [], total: 0 }

# Read
current_user_id = session[:user_id]

# Delete
session.delete(:user_id)

# Clear all
reset_session
```

### Cookies

```ruby
# Simple cookie
cookies[:remember_token] = user.remember_token

# With options
cookies[:user_preferences] = {
  value: preferences.to_json,
  expires: 1.year.from_now,
  httponly: true,
  secure: Rails.env.production?
}

# Signed cookie (tamper-proof)
cookies.signed[:user_id] = current_user.id
user_id = cookies.signed[:user_id]

# Encrypted cookie
cookies.encrypted[:secret_data] = sensitive_info
data = cookies.encrypted[:secret_data]

# Permanent cookie (20 years)
cookies.permanent[:preferences] = value

# Delete
cookies.delete(:remember_token)
```

## Request and Response

### Accessing Request Data

```ruby
# Parameters
params[:id]
params[:article][:title]
params.permit(:title, :body)

# Request info
request.method        # "GET", "POST", etc.
request.path          # "/articles/1"
request.fullpath      # "/articles/1?page=2"
request.url           # Full URL
request.host          # "example.com"
request.ip            # Client IP
request.remote_ip     # Client IP (proxy-aware)
request.user_agent    # Browser info
request.referer       # Previous URL

# Headers
request.headers["Authorization"]
request.headers["X-Custom-Header"]

# Format
request.format        # :html, :json, etc.
request.xhr?          # AJAX request?
request.get?          # HTTP method checks
request.post?
```

### Setting Response

```ruby
# Headers
response.headers["X-Custom-Header"] = "value"
response.headers["Cache-Control"] = "no-cache"

# Status
response.status = 201

# Content type
response.content_type = "application/json"
```

## Error Handling

### Rescue From

```ruby
class ApplicationController < ActionController::Base
  rescue_from ActiveRecord::RecordNotFound, with: :not_found
  rescue_from ActionController::ParameterMissing, with: :bad_request
  rescue_from Pundit::NotAuthorizedError, with: :forbidden

  private

  def not_found
    respond_to do |format|
      format.html { render "errors/404", status: :not_found }
      format.json { render json: { error: "Not found" }, status: :not_found }
    end
  end

  def bad_request(exception)
    render json: { error: exception.message }, status: :bad_request
  end

  def forbidden
    redirect_to root_path, alert: "Access denied."
  end
end
```

## API Controllers

```ruby
class Api::V1::ArticlesController < ActionController::API
  before_action :authenticate_api_user!

  def index
    @articles = Article.published.page(params[:page])
    render json: @articles, each_serializer: ArticleSerializer
  end

  def show
    @article = Article.find(params[:id])
    render json: @article, serializer: ArticleSerializer
  end

  def create
    @article = current_user.articles.build(article_params)

    if @article.save
      render json: @article, status: :created
    else
      render json: { errors: @article.errors }, status: :unprocessable_entity
    end
  end

  private

  def authenticate_api_user!
    token = request.headers["Authorization"]&.split(" ")&.last
    @current_user = User.find_by(api_token: token)
    head :unauthorized unless @current_user
  end

  def article_params
    params.require(:article).permit(:title, :body)
  end
end
```

## Streaming and Downloads

```ruby
# Send file
send_file Rails.root.join("files", "report.pdf"),
          type: "application/pdf",
          disposition: "attachment"

# Send data
send_data generate_csv(@records),
          type: "text/csv",
          filename: "export.csv"

# Streaming response
def export
  response.headers["Content-Type"] = "text/csv"
  response.headers["Content-Disposition"] = 'attachment; filename="data.csv"'

  response.stream.write "id,name\n"
  Article.find_each do |article|
    response.stream.write "#{article.id},#{article.name}\n"
  end
ensure
  response.stream.close
end
```

## Additional Resources

### Reference Files

- **`references/controller-patterns.md`** - Advanced patterns, concerns, service integration
