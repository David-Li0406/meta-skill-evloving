---
name: query-object
description: Generate query objects for complex database queries. Use when queries are complex, reusable, need filtering/sorting, or says "complex query", "search", "filter posts", "advanced search", "query builder", "scope is too complex".
---

# Query Object Generator

Extract complex database queries into reusable query objects for better organization and performance.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Identify complex query to extract
- [ ] 2. Create query class
- [ ] 3. Move query logic
- [ ] 4. Add chainable methods
- [ ] 5. Use in controller
- [ ] 6. Test query performance
```

## When to Use Query Objects

✅ **Good candidates**:
- Complex WHERE conditions
- Multiple JOINs
- Reusable search/filter logic
- Queries with many optional filters
- Performance-critical queries
- Queries spanning multiple models

❌ **Don't use for**:
- Simple `Model.where(status: :active)`
- One-time queries
- Basic associations

## Query Structure

```
app/queries/
├── application_query.rb      # Base class
├── posts_query.rb
├── users_query.rb
├── job_posts_query.rb
└── search/
    ├── post_search_query.rb
    └── user_search_query.rb
```

## Base Query Class

```ruby
# app/queries/application_query.rb
class ApplicationQuery
  def initialize(relation = nil)
    @relation = relation
  end

  def call
    @relation
  end

  alias_method :resolve, :call

  private

  attr_reader :relation
end
```

## Basic Query Template

```ruby
# app/queries/example_query.rb
class ExampleQuery < ApplicationQuery
  def initialize(relation = Model.all)
    super(relation)
  end

  def call
    @relation
      .where(conditions)
      .joins(associations)
      .order(ordering)
  end

  private

  def conditions
    # WHERE conditions
  end

  def associations
    # JOIN logic
  end

  def ordering
    { created_at: :desc }
  end
end
```

**Usage**:
```ruby
# In controller
@results = ExampleQuery.new.call

# Or with relation
@results = ExampleQuery.new(Model.active).call
```

## Common Patterns

### 1. Posts Search Query

```ruby
# app/queries/posts_query.rb
class PostsQuery < ApplicationQuery
  def initialize(relation = Post.includes(:user))
    super(relation)
    @filters = {}
  end

  def call
    apply_filters
    @relation
  end

  # Chainable filter methods
  def search(term)
    return self if term.blank?

    @filters[:search] = term
    self
  end

  def by_status(status)
    return self if status.blank?

    @filters[:status] = status
    self
  end

  def by_user(user_id)
    return self if user_id.blank?

    @filters[:user_id] = user_id
    self
  end

  def published_only
    @filters[:published] = true
    self
  end

  def recent
    @filters[:recent] = true
    self
  end

  def popular(min_likes = 10)
    @filters[:popular] = min_likes
    self
  end

  private

  def apply_filters
    apply_search_filter
    apply_status_filter
    apply_user_filter
    apply_published_filter
    apply_recent_filter
    apply_popular_filter
  end

  def apply_search_filter
    return unless @filters[:search]

    term = @filters[:search]
    @relation = @relation.where(
      "title LIKE ? OR content LIKE ?",
      "%#{term}%",
      "%#{term}%"
    )
  end

  def apply_status_filter
    return unless @filters[:status]

    @relation = @relation.where(status: @filters[:status])
  end

  def apply_user_filter
    return unless @filters[:user_id]

    @relation = @relation.where(user_id: @filters[:user_id])
  end

  def apply_published_filter
    return unless @filters[:published]

    @relation = @relation.where(status: :published)
  end

  def apply_recent_filter
    return unless @filters[:recent]

    @relation = @relation.where("created_at > ?", 7.days.ago)
                         .order(created_at: :desc)
  end

  def apply_popular_filter
    return unless @filters[:popular]

    @relation = @relation.where("likes_count >= ?", @filters[:popular])
                         .order(likes_count: :desc)
  end
end
```

**Controller Usage**:
```ruby
class PostsController < ApplicationController
  def index
    @posts = PostsQuery.new
                       .search(params[:q])
                       .by_status(params[:status])
                       .published_only
                       .recent
                       .call
                       .page(params[:page])
  end
end
```

### 2. Advanced Search Query

```ruby
# app/queries/search/post_search_query.rb
module Search
  class PostSearchQuery < ApplicationQuery
    def initialize(params = {})
      super(Post.includes(:user))
      @params = params
    end

    def call
      @relation = filter_by_keyword
      @relation = filter_by_category
      @relation = filter_by_date_range
      @relation = filter_by_likes
      @relation = sort_results

      @relation
    end

    private

    def filter_by_keyword
      keyword = @params[:keyword]
      return @relation if keyword.blank?

      @relation.where(
        "LOWER(title) LIKE :term OR LOWER(content) LIKE :term",
        term: "%#{keyword.downcase}%"
      )
    end

    def filter_by_category
      category = @params[:category]
      return @relation if category.blank?

      @relation.where(category: category)
    end

    def filter_by_date_range
      start_date = @params[:start_date]
      end_date = @params[:end_date]

      return @relation if start_date.blank? || end_date.blank?

      @relation.where(created_at: start_date..end_date)
    end

    def filter_by_likes
      min_likes = @params[:min_likes]&.to_i || 0

      @relation.where("likes_count >= ?", min_likes)
    end

    def sort_results
      sort_by = @params[:sort_by] || "recent"

      case sort_by
      when "popular"
        @relation.order(likes_count: :desc, created_at: :desc)
      when "commented"
        @relation.order(comments_count: :desc, created_at: :desc)
      else # recent
        @relation.order(created_at: :desc)
      end
    end
  end
end
```

### 3. Job Posts Filter Query

```ruby
# app/queries/job_posts_query.rb
class JobPostsQuery < ApplicationQuery
  VALID_CATEGORIES = %w[development design planning marketing].freeze
  VALID_TYPES = %w[short_term long_term].freeze
  VALID_STATUSES = %w[open closed].freeze

  def initialize(relation = JobPost.includes(:user))
    super(relation)
  end

  def by_category(category)
    return self unless VALID_CATEGORIES.include?(category)

    @relation = @relation.where(category: category)
    self
  end

  def by_project_type(type)
    return self unless VALID_TYPES.include?(type)

    @relation = @relation.where(project_type: type)
    self
  end

  def by_status(status)
    return self unless VALID_STATUSES.include?(status)

    @relation = @relation.where(status: status)
    self
  end

  def open_only
    @relation = @relation.where(status: :open)
    self
  end

  def with_budget
    @relation = @relation.where.not(budget: nil)
    self
  end

  def budget_range(min, max)
    return self if min.blank? || max.blank?

    @relation = @relation.where(
      "CAST(REPLACE(REPLACE(budget, '만원', ''), ',', '') AS INTEGER) BETWEEN ? AND ?",
      min,
      max
    )
    self
  end

  def recent(days = 7)
    @relation = @relation.where("created_at > ?", days.days.ago)
    self
  end

  def popular(min_views = 100)
    @relation = @relation.where("views_count >= ?", min_views)
    self
  end

  def call
    @relation.order(created_at: :desc)
  end
end
```

### 4. User Analytics Query

```ruby
# app/queries/user_analytics_query.rb
class UserAnalyticsQuery < ApplicationQuery
  def initialize(relation = User.all)
    super(relation)
  end

  def active_users(days = 30)
    @relation = @relation.where("last_sign_in_at > ?", days.days.ago)
    self
  end

  def with_posts
    @relation = @relation.where("posts_count > 0")
    self
  end

  def top_contributors(limit = 10)
    @relation = @relation.order(posts_count: :desc).limit(limit)
    self
  end

  def by_role(role_title)
    return self if role_title.blank?

    @relation = @relation.where(role_title: role_title)
    self
  end

  def joined_between(start_date, end_date)
    @relation = @relation.where(created_at: start_date..end_date)
    self
  end

  def call
    @relation
  end
end
```

## Hash-Based Parameters

```ruby
# app/queries/flexible_query.rb
class FlexibleQuery < ApplicationQuery
  def initialize(relation = Model.all, filters = {})
    super(relation)
    @filters = filters
  end

  def call
    @relation = apply_filters(@relation, @filters)
    @relation
  end

  private

  def apply_filters(relation, filters)
    filters.each do |key, value|
      next if value.blank?

      relation = case key.to_sym
                 when :status
                   relation.where(status: value)
                 when :user_id
                   relation.where(user_id: value)
                 when :search
                   relation.where("title LIKE ?", "%#{value}%")
                 when :min_date
                   relation.where("created_at >= ?", value)
                 when :max_date
                   relation.where("created_at <= ?", value)
                 else
                   relation
                 end
    end

    relation
  end
end
```

**Usage**:
```ruby
filters = {
  status: params[:status],
  user_id: params[:user_id],
  search: params[:q],
  min_date: params[:from]
}

@results = FlexibleQuery.new(Post.all, filters).call
```

## Performance Optimization

### Eager Loading
```ruby
class OptimizedPostsQuery < ApplicationQuery
  def initialize
    super(Post.includes(:user, :comments, :likes))
  end

  def call
    @relation.order(created_at: :desc)
  end
end
```

### Select Specific Columns
```ruby
class LightweightPostsQuery < ApplicationQuery
  def call
    @relation.select(:id, :title, :created_at, :user_id, :likes_count)
  end
end
```

### Use Counter Cache
```ruby
class PopularPostsQuery < ApplicationQuery
  def call
    # Uses counter_cache, no COUNT query
    @relation.where("likes_count > 10")
             .order(likes_count: :desc)
  end
end
```

### Batch Processing
```ruby
class BatchQuery < ApplicationQuery
  def find_each_batch(batch_size = 1000)
    @relation.find_each(batch_size: batch_size) do |record|
      yield record
    end
  end
end
```

## Testing

```ruby
# test/queries/posts_query_test.rb
require "test_helper"

class PostsQueryTest < ActiveSupport::TestCase
  test "filters by search term" do
    post1 = create(:post, title: "Ruby on Rails")
    post2 = create(:post, title: "Python Django")
    post3 = create(:post, title: "Rails Tutorial")

    results = PostsQuery.new.search("Rails").call

    assert_includes results, post1
    assert_includes results, post3
    assert_not_includes results, post2
  end

  test "filters by status" do
    draft = create(:post, status: :draft)
    published = create(:post, status: :published)

    results = PostsQuery.new.by_status(:published).call

    assert_includes results, published
    assert_not_includes results, draft
  end

  test "chains multiple filters" do
    user = create(:user)
    post1 = create(:post, user: user, status: :published, likes_count: 20)
    post2 = create(:post, user: user, status: :draft)
    post3 = create(:post, status: :published, likes_count: 5)

    results = PostsQuery.new
                        .by_user(user.id)
                        .published_only
                        .popular(10)
                        .call

    assert_includes results, post1
    assert_not_includes results, post2
    assert_not_includes results, post3
  end

  test "returns correct SQL query" do
    query = PostsQuery.new.search("test").by_status(:published)

    sql = query.call.to_sql

    assert_match /title LIKE/, sql
    assert_match /status/, sql
  end
end
```

## Best Practices

1. **Chainable Methods**: Return `self` for method chaining
2. **Default Includes**: Eager load associations by default
3. **Validation**: Validate filter parameters
4. **Performance**: Use indexes, counter caches, select columns
5. **Immutability**: Don't modify input relation
6. **Explicitness**: Clear method names (by_status, not filter)
7. **Testing**: Test each filter and combinations

## Integration Examples

### Controller with Pagination
```ruby
class PostsController < ApplicationController
  def index
    @posts = PostsQuery.new
                       .search(params[:q])
                       .by_status(params[:status])
                       .recent
                       .call
                       .page(params[:page])
                       .per(20)
  end
end
```

### Background Job
```ruby
class AnalyticsJob < ApplicationJob
  def perform
    users = UserAnalyticsQuery.new
                              .active_users(30)
                              .with_posts
                              .call

    users.find_each do |user|
      calculate_stats(user)
    end
  end
end
```

### API Endpoint
```ruby
module Api
  module V1
    class PostsController < BaseController
      def index
        @posts = PostsQuery.new
                           .by_status(params[:status])
                           .recent
                           .call
                           .limit(50)

        render json: { data: @posts.map { |p| post_json(p) } }
      end
    end
  end
end
```

## Checklist

- [ ] Query class created in app/queries/
- [ ] Inherits from ApplicationQuery
- [ ] Chainable filter methods
- [ ] Eager loading configured
- [ ] Returns relation (not array)
- [ ] Tested with various filters
- [ ] Performance optimized
- [ ] Used in controller/service
