# Controller Patterns

## Controller Concerns

```ruby
# app/controllers/concerns/authenticatable.rb
module Authenticatable
  extend ActiveSupport::Concern

  included do
    before_action :authenticate_user!
    helper_method :current_user, :user_signed_in?
  end

  private

  def current_user
    @current_user ||= User.find_by(id: session[:user_id])
  end

  def user_signed_in?
    current_user.present?
  end

  def authenticate_user!
    redirect_to login_path, alert: "Please sign in" unless user_signed_in?
  end
end

# app/controllers/concerns/paginatable.rb
module Paginatable
  extend ActiveSupport::Concern

  def paginate(scope)
    scope.page(params[:page]).per(params[:per_page] || 25)
  end
end
```

## Service Object Integration

```ruby
# app/controllers/articles_controller.rb
class ArticlesController < ApplicationController
  def create
    result = Articles::CreateService.call(
      params: article_params,
      user: current_user
    )

    if result.success?
      redirect_to result.article, notice: "Created!"
    else
      @article = result.article
      flash.now[:alert] = result.error
      render :new, status: :unprocessable_entity
    end
  end

  def publish
    result = Articles::PublishService.call(article: @article, user: current_user)

    if result.success?
      redirect_to @article, notice: "Published!"
    else
      redirect_to @article, alert: result.error
    end
  end
end

# app/services/articles/create_service.rb
module Articles
  class CreateService
    def self.call(...)
      new(...).call
    end

    def initialize(params:, user:)
      @params = params
      @user = user
    end

    def call
      article = @user.articles.build(@params)

      if article.save
        notify_subscribers(article)
        Result.new(success: true, article: article)
      else
        Result.new(success: false, article: article, error: "Failed to save")
      end
    end

    private

    def notify_subscribers(article)
      ArticleNotificationJob.perform_later(article)
    end

    Result = Struct.new(:success, :article, :error, keyword_init: true) do
      alias_method :success?, :success
    end
  end
end
```

## Query Object Integration

```ruby
# app/controllers/articles_controller.rb
class ArticlesController < ApplicationController
  def index
    @articles = ArticleQuery.new(
      scope: Article.all,
      params: filter_params
    ).call

    @articles = paginate(@articles)
  end

  private

  def filter_params
    params.permit(:status, :category_id, :author_id, :q, :sort)
  end
end

# app/queries/article_query.rb
class ArticleQuery
  def initialize(scope:, params:)
    @scope = scope
    @params = params
  end

  def call
    scope = @scope
    scope = filter_by_status(scope)
    scope = filter_by_category(scope)
    scope = filter_by_author(scope)
    scope = search(scope)
    scope = sort(scope)
    scope
  end

  private

  def filter_by_status(scope)
    return scope if @params[:status].blank?
    scope.where(status: @params[:status])
  end

  def filter_by_category(scope)
    return scope if @params[:category_id].blank?
    scope.where(category_id: @params[:category_id])
  end

  def filter_by_author(scope)
    return scope if @params[:author_id].blank?
    scope.where(author_id: @params[:author_id])
  end

  def search(scope)
    return scope if @params[:q].blank?
    scope.where("title ILIKE ?", "%#{@params[:q]}%")
  end

  def sort(scope)
    case @params[:sort]
    when "oldest" then scope.order(created_at: :asc)
    when "title" then scope.order(title: :asc)
    else scope.order(created_at: :desc)
    end
  end
end
```

## Responders

```ruby
# Using responders gem
class ArticlesController < ApplicationController
  respond_to :html, :json

  def index
    @articles = Article.all
    respond_with @articles
  end

  def create
    @article = Article.create(article_params)
    respond_with @article, location: -> { articles_path }
  end
end
```

## Rate Limiting

```ruby
# app/controllers/api/base_controller.rb
class Api::BaseController < ActionController::API
  include RateLimiting

  rate_limit to: 100, within: 1.hour, by: -> { request.remote_ip }
end

# app/controllers/concerns/rate_limiting.rb
module RateLimiting
  extend ActiveSupport::Concern

  class_methods do
    def rate_limit(to:, within:, by:)
      before_action -> { check_rate_limit(to, within, by) }
    end
  end

  private

  def check_rate_limit(limit, period, key_proc)
    key = "rate_limit:#{controller_name}:#{instance_exec(&key_proc)}"
    count = Rails.cache.increment(key, 1, expires_in: period)

    if count > limit
      response.headers["Retry-After"] = period.to_i.to_s
      render json: { error: "Rate limit exceeded" }, status: :too_many_requests
    end
  end
end
```

## Caching

```ruby
class ArticlesController < ApplicationController
  # Page caching (for static pages)
  caches_page :about

  # Action caching with expiry
  caches_action :index, expires_in: 1.hour

  # Fragment caching in controller
  def show
    @article = Article.find(params[:id])
    fresh_when @article
  end

  # Conditional GET
  def show
    @article = Article.find(params[:id])

    if stale?(etag: @article, last_modified: @article.updated_at)
      respond_to do |format|
        format.html
        format.json { render json: @article }
      end
    end
  end
end
```

## Versioned API Controllers

```ruby
# app/controllers/api/v1/base_controller.rb
module Api
  module V1
    class BaseController < ActionController::API
      include Api::Authentication
      include Api::ErrorHandling

      before_action :set_default_format

      private

      def set_default_format
        request.format = :json
      end
    end
  end
end

# app/controllers/api/v2/base_controller.rb
module Api
  module V2
    class BaseController < Api::V1::BaseController
      # V2-specific behavior
    end
  end
end
```
