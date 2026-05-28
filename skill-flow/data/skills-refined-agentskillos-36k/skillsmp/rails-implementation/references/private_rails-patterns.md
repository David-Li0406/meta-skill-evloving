# Rails Implementation Patterns

This reference provides common implementation patterns for Rails development.

## Table of Contents

- [Model Annotations](#model-annotations)
- [CRUD Operations](#crud-operations)
- [Authentication & Authorization](#authentication--authorization)
- [API Endpoints](#api-endpoints)
- [Background Jobs](#background-jobs)
- [File Uploads](#file-uploads)
- [Search & Filtering](#search--filtering)
- [Associations](#associations)

## Model Annotations

### Using Annotate Gem

The `annotate` gem automatically adds schema information to Rails models as comments. When present in the project, always add meaningful column descriptions after creating or modifying models.

**Check if annotate is available:**
```bash
bundle list | grep annotate
# or
cat Gemfile | grep annotate
```

**Running annotate:**
```bash
# Annotate all models
bundle exec annotate

# Annotate specific model
bundle exec annotate --models
```

### Adding Column Descriptions

After running migrations that add/modify columns, add descriptions to the generated annotations:

**Before (auto-generated):**
```ruby
# == Schema Information
#
# Table name: articles
#
#  id         :bigint           not null, primary key
#  title      :string
#  body       :text
#  status     :string
#  user_id    :bigint           not null
#  created_at :datetime         not null
#  updated_at :datetime         not null
#

class Article < ApplicationRecord
  validates :title, presence: true
  belongs_to :user
end
```

**After (with descriptions):**
```ruby
# == Schema Information
#
# Table name: articles
#
#  id         :bigint           not null, primary key
#  title      :string           記事のタイトル
#  body       :text             記事の本文
#  status     :string           公開状態 (draft/published/archived)
#  user_id    :bigint           not null  記事の投稿者ID
#  created_at :datetime         not null
#  updated_at :datetime         not null
#

class Article < ApplicationRecord
  validates :title, presence: true
  belongs_to :user
end
```

### When to Add Descriptions

**Always add descriptions for:**
- ✅ Business logic columns (status, flags, computed values)
- ✅ Columns with specific formats or constraints
- ✅ Foreign keys with non-obvious relationships
- ✅ Enum columns (include possible values)
- ✅ Columns with units or specific meanings

**Skip descriptions for:**
- ❌ Obvious columns (created_at, updated_at, id)
- ❌ Self-explanatory boolean flags (published, active)
- ❌ Standard Rails columns

**Workflow:**
1. Create migration and run `rails db:migrate`
2. Run `bundle exec annotate` to update model annotations
3. Add meaningful descriptions to new/modified columns
4. Commit both migration and annotated model

## CRUD Operations

### Basic Resource

**Model:**
```ruby
# app/models/article.rb
class Article < ApplicationRecord
  validates :title, presence: true, length: { minimum: 3 }
  validates :body, presence: true

  belongs_to :user
end
```

**Controller:**
```ruby
# app/controllers/articles_controller.rb
class ArticlesController < ApplicationController
  before_action :set_article, only: [:show, :edit, :update, :destroy]

  def index
    @articles = Article.all
  end

  def show
  end

  def new
    @article = Article.new
  end

  def create
    @article = Article.new(article_params)

    if @article.save
      redirect_to @article, notice: 'Article was successfully created.'
    else
      render :new, status: :unprocessable_entity
    end
  end

  def update
    if @article.update(article_params)
      redirect_to @article, notice: 'Article was successfully updated.'
    else
      render :edit, status: :unprocessable_entity
    end
  end

  def destroy
    @article.destroy
    redirect_to articles_url, notice: 'Article was successfully destroyed.'
  end

  private

  def set_article
    @article = Article.find(params[:id])
  end

  def article_params
    params.require(:article).permit(:title, :body)
  end
end
```

## Authentication & Authorization

### Using Devise

```ruby
# app/models/user.rb
class User < ApplicationRecord
  devise :database_authenticatable, :registerable,
         :recoverable, :rememberable, :validatable
end
```

### Custom Authentication

```ruby
# app/controllers/sessions_controller.rb
class SessionsController < ApplicationController
  def create
    user = User.find_by(email: params[:email])

    if user&.authenticate(params[:password])
      session[:user_id] = user.id
      redirect_to root_path, notice: 'Logged in successfully.'
    else
      flash.now[:alert] = 'Invalid email or password.'
      render :new, status: :unprocessable_entity
    end
  end

  def destroy
    session[:user_id] = nil
    redirect_to root_path, notice: 'Logged out successfully.'
  end
end
```

### Authorization with Current User

```ruby
# app/controllers/application_controller.rb
class ApplicationController < ActionController::Base
  before_action :require_login

  private

  def current_user
    @current_user ||= User.find_by(id: session[:user_id])
  end
  helper_method :current_user

  def require_login
    unless current_user
      redirect_to login_path, alert: 'You must be logged in to access this page.'
    end
  end

  def authorize_user!(resource)
    unless resource.user == current_user
      redirect_to root_path, alert: 'You are not authorized to perform this action.'
    end
  end
end
```

## API Endpoints

### JSON API

```ruby
# app/controllers/api/v1/articles_controller.rb
module Api
  module V1
    class ArticlesController < ApplicationController
      skip_before_action :verify_authenticity_token
      before_action :set_article, only: [:show, :update, :destroy]

      def index
        @articles = Article.all
        render json: @articles
      end

      def show
        render json: @article
      end

      def create
        @article = Article.new(article_params)

        if @article.save
          render json: @article, status: :created
        else
          render json: { errors: @article.errors.full_messages }, status: :unprocessable_entity
        end
      end

      def update
        if @article.update(article_params)
          render json: @article
        else
          render json: { errors: @article.errors.full_messages }, status: :unprocessable_entity
        end
      end

      def destroy
        @article.destroy
        head :no_content
      end

      private

      def set_article
        @article = Article.find(params[:id])
      end

      def article_params
        params.require(:article).permit(:title, :body)
      end
    end
  end
end
```

### API Serializer Pattern

```ruby
# app/serializers/article_serializer.rb
class ArticleSerializer
  def initialize(article)
    @article = article
  end

  def as_json
    {
      id: @article.id,
      title: @article.title,
      body: @article.body,
      author: {
        id: @article.user.id,
        name: @article.user.name
      },
      created_at: @article.created_at,
      updated_at: @article.updated_at
    }
  end
end

# Usage in controller:
# render json: ArticleSerializer.new(@article).as_json
```

## Background Jobs

### Active Job

```ruby
# app/jobs/send_welcome_email_job.rb
class SendWelcomeEmailJob < ApplicationJob
  queue_as :default

  def perform(user)
    UserMailer.welcome_email(user).deliver_now
  end
end

# Usage:
# SendWelcomeEmailJob.perform_later(user)
```

## File Uploads

### Active Storage

```ruby
# app/models/user.rb
class User < ApplicationRecord
  has_one_attached :avatar
  has_many_attached :documents
end

# app/controllers/users_controller.rb
def update
  if @user.update(user_params)
    redirect_to @user, notice: 'Profile updated.'
  else
    render :edit
  end
end

private

def user_params
  params.require(:user).permit(:name, :email, :avatar, documents: [])
end
```

## Search & Filtering

### Simple Search

```ruby
# app/models/article.rb
class Article < ApplicationRecord
  scope :search, ->(query) {
    where('title LIKE ? OR body LIKE ?', "%#{query}%", "%#{query}%")
  }

  scope :published, -> { where(published: true) }
  scope :by_author, ->(user_id) { where(user_id: user_id) }
end

# app/controllers/articles_controller.rb
def index
  @articles = Article.all
  @articles = @articles.search(params[:query]) if params[:query].present?
  @articles = @articles.by_author(params[:author_id]) if params[:author_id].present?
  @articles = @articles.published if params[:published] == 'true'
end
```

## Associations

### Common Patterns

```ruby
# Has Many Through
class User < ApplicationRecord
  has_many :memberships
  has_many :teams, through: :memberships
end

class Membership < ApplicationRecord
  belongs_to :user
  belongs_to :team
end

class Team < ApplicationRecord
  has_many :memberships
  has_many :users, through: :memberships
end

# Polymorphic Association
class Comment < ApplicationRecord
  belongs_to :commentable, polymorphic: true
end

class Article < ApplicationRecord
  has_many :comments, as: :commentable
end

class Photo < ApplicationRecord
  has_many :comments, as: :commentable
end

# Self-Referential Association
class User < ApplicationRecord
  has_many :friendships
  has_many :friends, through: :friendships
end

class Friendship < ApplicationRecord
  belongs_to :user
  belongs_to :friend, class_name: 'User'
end
```
