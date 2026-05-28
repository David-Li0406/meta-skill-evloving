# Controller Patterns

## RESTful Controller Structure

```ruby
class PostsController < ApplicationController
  before_action :authenticate_user!
  before_action :set_post, only: [:show, :edit, :update, :destroy]
  before_action :authorize_post, only: [:edit, :update, :destroy]

  # GET /posts
  def index
    @posts = Post.published.page(params[:page])
  end

  # GET /posts/:id
  def show
    # @post set by before_action
  end

  # GET /posts/new
  def new
    @post = Post.new
  end

  # POST /posts
  def create
    @post = CreatePostService.call(current_user, post_params)

    if @post.persisted?
      redirect_to @post, notice: "Post created successfully"
    else
      render :new, status: :unprocessable_entity
    end
  end

  # PATCH /posts/:id
  def update
    if UpdatePostService.call(@post, post_params)
      redirect_to @post, notice: "Post updated successfully"
    else
      render :edit, status: :unprocessable_entity
    end
  end

  # DELETE /posts/:id
  def destroy
    @post.destroy!
    redirect_to posts_url, notice: "Post deleted successfully"
  end

  private

  def set_post
    @post = Post.find(params[:id])
  end

  def authorize_post
    authorize @post # Pundit
  end

  def post_params
    params.require(:post).permit(:title, :body, :published)
  end
end
```

---

## API Controller Pattern

```ruby
# app/controllers/api/base_controller.rb
module Api
  class BaseController < ActionController::API
    include ActionController::HttpAuthentication::Token::ControllerMethods

    before_action :authenticate_api_user!

    rescue_from ActiveRecord::RecordNotFound, with: :not_found
    rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity
    rescue_from Pundit::NotAuthorizedError, with: :forbidden

    private

    def authenticate_api_user!
      authenticate_or_request_with_http_token do |token, options|
        @current_user = User.find_by(api_token: token)
      end
    end

    def not_found(exception)
      render json: { error: exception.message }, status: :not_found
    end

    def unprocessable_entity(exception)
      render json: { errors: exception.record.errors }, status: :unprocessable_entity
    end

    def forbidden
      render json: { error: "Forbidden" }, status: :forbidden
    end
  end
end

# app/controllers/api/v1/posts_controller.rb
module Api
  module V1
    class PostsController < Api::BaseController
      def index
        posts = Post.published.page(params[:page])
        render json: PostBlueprint.render(posts, root: :posts)
      end

      def create
        post = CreatePostService.call(current_user, post_params)

        if post.persisted?
          render json: PostBlueprint.render(post), status: :created
        else
          render json: { errors: post.errors }, status: :unprocessable_entity
        end
      end
    end
  end
end
```

---

## Hotwire Controller Pattern

```ruby
class PostsController < ApplicationController
  def create
    @post = CreatePostService.call(current_user, post_params)

    respond_to do |format|
      if @post.persisted?
        format.turbo_stream
        format.html { redirect_to @post }
      else
        format.turbo_stream { render :form_errors, status: :unprocessable_entity }
        format.html { render :new, status: :unprocessable_entity }
      end
    end
  end
end

# app/views/posts/create.turbo_stream.erb
<%= turbo_stream.prepend "posts", @post %>
<%= turbo_stream.update "new_post_form", "" %>
```

---

## Nested Resource Controller

```ruby
class CommentsController < ApplicationController
  before_action :set_post
  before_action :set_comment, only: [:show, :edit, :update, :destroy]

  # GET /posts/:post_id/comments
  def index
    @comments = @post.comments.page(params[:page])
  end

  # POST /posts/:post_id/comments
  def create
    @comment = @post.comments.build(comment_params)
    @comment.user = current_user

    if @comment.save
      redirect_to [@post, @comment]
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def set_post
    @post = Post.find(params[:post_id])
  end

  def set_comment
    @comment = @post.comments.find(params[:id])
  end
end
```

---

## Controller Concerns

```ruby
# app/controllers/concerns/paginatable.rb
module Paginatable
  extend ActiveSupport::Concern

  included do
    before_action :set_pagination_params
  end

  private

  def set_pagination_params
    @page = params[:page] || 1
    @per_page = params[:per_page] || 25
  end

  def paginate(collection)
    collection.page(@page).per(@per_page)
  end
end

# Usage
class PostsController < ApplicationController
  include Paginatable

  def index
    @posts = paginate(Post.published)
  end
end
```

---

## Error Handling Concern

```ruby
# app/controllers/concerns/error_handling.rb
module ErrorHandling
  extend ActiveSupport::Concern

  included do
    rescue_from ActiveRecord::RecordNotFound, with: :not_found
    rescue_from ActiveRecord::RecordInvalid, with: :unprocessable_entity
    rescue_from Pundit::NotAuthorizedError, with: :unauthorized
  end

  private

  def not_found
    respond_to do |format|
      format.html { render 'errors/404', status: :not_found }
      format.json { render json: { error: 'Not found' }, status: :not_found }
    end
  end

  def unprocessable_entity(exception)
    respond_to do |format|
      format.html { render 'errors/422', status: :unprocessable_entity }
      format.json { render json: { errors: exception.record.errors }, status: :unprocessable_entity }
    end
  end

  def unauthorized
    respond_to do |format|
      format.html { redirect_to root_path, alert: 'Not authorized' }
      format.json { render json: { error: 'Not authorized' }, status: :forbidden }
    end
  end
end
```
