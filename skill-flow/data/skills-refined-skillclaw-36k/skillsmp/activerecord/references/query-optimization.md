# Query Optimization in Rails

## Detecting N+1 Queries

### Using Bullet Gem

```ruby
# Gemfile
group :development do
  gem 'bullet'
end

# config/environments/development.rb
config.after_initialize do
  Bullet.enable = true
  Bullet.alert = true
  Bullet.bullet_logger = true
  Bullet.console = true
  Bullet.rails_logger = true
  Bullet.add_footer = true
end
```

### Manual Detection

```ruby
# In rails console
ActiveRecord::Base.logger = Logger.new(STDOUT)

# Look for repeated queries
Article.all.each { |a| a.author.name }
# You'll see: SELECT * FROM users WHERE id = ? (repeated)
```

## Indexing Strategies

### When to Add Indexes

1. **Foreign keys** - Always index
2. **Columns in WHERE clauses** - Frequently queried
3. **Columns in ORDER BY** - Sorting columns
4. **Unique constraints** - For uniqueness validation

### Types of Indexes

```ruby
class AddIndexes < ActiveRecord::Migration[7.1]
  def change
    # Single column index
    add_index :articles, :user_id

    # Composite index (order matters!)
    add_index :articles, [:user_id, :created_at]

    # Unique index
    add_index :users, :email, unique: true

    # Partial index (PostgreSQL)
    add_index :articles, :published_at, where: "status = 'published'"

    # Index for text search (PostgreSQL)
    add_index :articles, :title, using: :gin, opclass: :gin_trgm_ops
  end
end
```

### Composite Index Order

```ruby
# Index on [:user_id, :created_at] helps:
Article.where(user_id: 1)
Article.where(user_id: 1, created_at: date)
Article.where(user_id: 1).order(:created_at)

# Does NOT help:
Article.where(created_at: date)  # Wrong order
Article.order(:created_at)       # Missing user_id
```

## Query Optimization Techniques

### Using Joins vs Includes

```ruby
# includes - Use when you need the associated data
articles = Article.includes(:author)
articles.each { |a| puts a.author.name }  # No N+1

# joins - Use when filtering by association
Article.joins(:author).where(users: { role: "admin" })

# joins doesn't load association data
articles = Article.joins(:author).where(users: { role: "admin" })
articles.each { |a| puts a.author.name }  # N+1 problem!

# Solution: joins + includes
Article.joins(:author)
       .includes(:author)
       .where(users: { role: "admin" })
```

### Selecting Specific Columns

```ruby
# Load everything (slow)
User.all

# Select only needed columns (faster)
User.select(:id, :email, :name)

# For single values
User.pluck(:email)  # Returns array: ["a@b.com", "c@d.com"]

# For key-value pairs
User.pluck(:id, :email).to_h  # {1 => "a@b.com", 2 => "c@d.com"}
```

### Counting Efficiently

```ruby
# BAD: Loads all records
User.all.count
User.where(active: true).to_a.size

# GOOD: SQL COUNT
User.count
User.where(active: true).count

# For associations with counter_cache
class Comment < ApplicationRecord
  belongs_to :article, counter_cache: true
end

# Migration
add_column :articles, :comments_count, :integer, default: 0

# Now article.comments.count is instant (no query)
```

### Exists vs Any

```ruby
# BAD: Loads records to check existence
User.where(role: "admin").any?

# GOOD: SQL EXISTS (stops at first match)
User.where(role: "admin").exists?
```

### Finding in Batches

```ruby
# BAD: Loads millions of records
Article.all.each { |a| process(a) }

# GOOD: Load in batches
Article.find_each(batch_size: 1000) { |a| process(a) }

# With custom ordering (needs unique column)
Article.find_each(batch_size: 1000, order: :desc) { |a| process(a) }

# For updates
Article.in_batches(of: 1000).update_all(processed: true)

# With enumerable methods
Article.find_each.map(&:title)  # Memory efficient
```

## Database-Specific Optimizations

### PostgreSQL

```ruby
# Use array columns
class User < ApplicationRecord
  # tags: text[]
  scope :tagged_with, ->(tag) { where("? = ANY(tags)", tag) }
end

# Full-text search
class Article < ApplicationRecord
  include PgSearch::Model
  pg_search_scope :search_content,
    against: [:title, :body],
    using: { tsearch: { prefix: true } }
end

# JSONB columns
class Event < ApplicationRecord
  # metadata: jsonb
  scope :with_source, ->(src) { where("metadata->>'source' = ?", src) }
end
```

### MySQL

```ruby
# Use FORCE INDEX hint when needed
Article.from("articles FORCE INDEX (index_articles_on_created_at)")
       .order(:created_at)
```

## Query Analysis

### Using EXPLAIN

```ruby
# Rails explain
Article.where(status: "published").explain

# PostgreSQL detailed
Article.where(status: "published").explain(analyze: true, verbose: true)

# Looking for:
# - Seq Scan (bad for large tables)
# - Index Scan (good)
# - Bitmap Index Scan (good for multiple conditions)
```

### Query Logging in Development

```ruby
# config/environments/development.rb
config.active_record.verbose_query_logs = true

# Shows file:line where query originated
# Article Load (0.5ms)  SELECT * FROM articles
#   ↳ app/controllers/articles_controller.rb:15:in `index'
```

## Caching Strategies

### Query Caching

```ruby
# Within a request, identical queries are cached
2.times { Article.find(1) }  # Only 1 query

# Manual query cache
ActiveRecord::Base.cache do
  Article.find(1)
  Article.find(1)  # Uses cache
end
```

### Low-Level Caching

```ruby
# Cache expensive queries
def expensive_stats
  Rails.cache.fetch("articles/stats", expires_in: 1.hour) do
    {
      total: Article.count,
      published: Article.published.count,
      by_category: Article.group(:category_id).count
    }
  end
end

# Cache with dependencies
Rails.cache.fetch(["articles/recent", Article.maximum(:updated_at)]) do
  Article.recent.limit(10).to_a
end
```

### Counter Caches

```ruby
# Instead of querying count each time
class Comment < ApplicationRecord
  belongs_to :article, counter_cache: true
end

# Migration
add_column :articles, :comments_count, :integer, default: 0, null: false

# Reset existing counts
Article.find_each do |article|
  Article.reset_counters(article.id, :comments)
end
```

## Common Anti-Patterns

### Anti-Pattern: Loading Then Filtering

```ruby
# BAD
articles = Article.all.select { |a| a.published? }

# GOOD
articles = Article.where(published: true)
```

### Anti-Pattern: N+1 in Views

```erb
<!-- BAD -->
<% @articles.each do |article| %>
  <%= article.author.name %>
  <%= article.comments.count %>
<% end %>

<!-- Controller should eager load -->
@articles = Article.includes(:author).with_count(:comments)
```

### Anti-Pattern: Over-Eager Loading

```ruby
# BAD: Loading associations you don't use
Article.includes(:author, :comments, :tags, :category)

# GOOD: Only load what you need
Article.includes(:author)  # If only showing author
```
