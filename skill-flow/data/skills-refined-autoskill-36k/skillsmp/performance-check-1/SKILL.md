---
name: performance-check
description: Performance monitoring and optimization. Use when user needs N+1 detection, slow query analysis, memory profiling, or says "performance issue", "slow queries", "N+1 problem", "optimize performance", "memory leak".
---

# Performance Check

N+1 쿼리 감지, 느린 쿼리 분석, 메모리 프로파일링 등 성능 최적화 작업을 수행합니다.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Identify performance issue
- [ ] 2. Profile the problem
- [ ] 3. Analyze results
- [ ] 4. Apply optimization
- [ ] 5. Measure improvement
```

## Performance Tools

### 1. Bullet (N+1 Query Detection)

N+1 쿼리를 자동으로 감지하고 경고합니다.

**Installation**:
```ruby
# Gemfile
group :development do
  gem 'bullet'
end
```

**Configuration**:
```ruby
# config/environments/development.rb
config.after_initialize do
  Bullet.enable = true
  Bullet.alert = true                 # JavaScript alert
  Bullet.bullet_logger = true         # Log to bullet.log
  Bullet.console = true               # Browser console
  Bullet.rails_logger = true          # Rails log
  Bullet.add_footer = true            # Bottom of page

  # Alert on N+1 queries
  Bullet.n_plus_one_query_enable = true

  # Alert on unused eager loading
  Bullet.unused_eager_loading_enable = true

  # Alert on missing counter cache
  Bullet.counter_cache_enable = true
end
```

**Example N+1 Problem**:
```ruby
# ❌ N+1 Query (1 query for posts + N queries for users)
@posts = Post.all
@posts.each do |post|
  puts post.user.name  # N queries!
end

# ✅ Fixed with includes
@posts = Post.includes(:user).all
@posts.each do |post|
  puts post.user.name  # 2 queries total
end
```

### 2. Rack Mini Profiler

페이지 로딩 시간과 쿼리를 실시간으로 프로파일링합니다.

**Installation**:
```ruby
# Gemfile
group :development do
  gem 'rack-mini-profiler'
  gem 'memory_profiler'      # Memory profiling
  gem 'stackprof'            # CPU profiling (MRI Ruby)
end
```

**Usage**:
- 자동으로 페이지 상단에 타이밍 정보 표시
- `?pp=help` URL 파라미터로 모든 옵션 확인
- `?pp=profile-memory` 메모리 프로파일링
- `?pp=profile-gc` GC 프로파일링

**Configuration**:
```ruby
# config/initializers/rack_profiler.rb
if Rails.env.development?
  require 'rack-mini-profiler'

  Rack::MiniProfiler.config.position = 'bottom-right'
  Rack::MiniProfiler.config.start_hidden = false
end
```

### 3. Query Analysis

**Slow Query Detection**:
```ruby
# config/initializers/query_logging.rb (development only)
if Rails.env.development?
  ActiveSupport::Notifications.subscribe('sql.active_record') do |name, start, finish, id, payload|
    duration = (finish - start) * 1000  # ms

    if duration > 100  # Queries slower than 100ms
      Rails.logger.warn "SLOW QUERY (#{duration.round(2)}ms): #{payload[:sql]}"
    end
  end
end
```

**Common Slow Query Patterns**:

**Problem 1: Missing Index**
```ruby
# Slow without index
Post.where(status: 'published').count

# Add index
add_index :posts, :status
```

**Problem 2: N+1 Queries**
```ruby
# N+1
posts = Post.all
posts.map { |p| p.user.name }

# Fixed
posts = Post.includes(:user).all
posts.map { |p| p.user.name }
```

**Problem 3: Loading Too Much Data**
```ruby
# Loads all columns
Post.all.map(&:title)

# Only load needed columns
Post.select(:id, :title).all
```

**Problem 4: Inefficient Counting**
```ruby
# Loads all records
if user.posts.any?

# Use exists? (stops at first match)
if user.posts.exists?

# Use counter cache for frequent counts
class User < ApplicationRecord
  has_many :posts
end

# Migration
add_column :users, :posts_count, :integer, default: 0, null: false
```

### 4. Memory Profiling

**Using memory_profiler**:
```ruby
require 'memory_profiler'

report = MemoryProfiler.report do
  # Code to profile
  Post.includes(:user, :comments).limit(100).to_a
end

report.pretty_print
```

**Check Memory Usage**:
```ruby
# In development console
def memory_usage
  `ps -o rss= -p #{Process.pid}`.to_i / 1024  # MB
end

before = memory_usage
# Run code
after = memory_usage
puts "Memory used: #{after - before}MB"
```

### 5. Caching Strategies

**Fragment Caching**:
```erb
<%# Cache expensive view rendering %>
<% cache @post do %>
  <%= render @post %>
<% end %>

<%# Cache collection %>
<% cache @posts do %>
  <%= render @posts %>
<% end %>
```

**Query Caching** (automatic in development):
```ruby
# First query hits database
Post.where(status: 'published').to_a

# Second identical query uses cache (within same request)
Post.where(status: 'published').to_a
```

**Russian Doll Caching**:
```erb
<%# Outer cache depends on post and comments %>
<% cache [@post, @post.comments.maximum(:updated_at)] do %>
  <%= render @post %>

  <% @post.comments.each do |comment| %>
    <%# Inner cache for each comment %>
    <% cache comment do %>
      <%= render comment %>
    <% end %>
  <% end %>
<% end %>
```

**Counter Cache** (avoid COUNT queries):
```ruby
# Migration
class AddCommentsCountToPosts < ActiveRecord::Migration[8.0]
  def change
    add_column :posts, :comments_count, :integer, default: 0, null: false

    # Backfill existing data
    Post.find_each do |post|
      Post.reset_counters(post.id, :comments)
    end
  end
end

# Model
class Comment < ApplicationRecord
  belongs_to :post, counter_cache: true
end

# Usage
post.comments_count  # No query!
```

### 6. Database Optimization

**Use select to load only needed columns**:
```ruby
# ❌ Loads all columns (inefficient)
Post.all.map(&:title)

# ✅ Only loads id and title
Post.select(:id, :title).all
```

**Use pluck for simple arrays**:
```ruby
# ❌ Instantiates full ActiveRecord objects
Post.all.map(&:id)

# ✅ Direct SQL query, returns array
Post.pluck(:id)

# Multiple columns
Post.pluck(:id, :title)
```

**Batch processing for large datasets**:
```ruby
# ❌ Loads all records into memory
User.all.each do |user|
  user.send_email
end

# ✅ Processes in batches of 1000
User.find_each(batch_size: 1000) do |user|
  user.send_email
end

# Or with find_in_batches
User.find_in_batches(batch_size: 1000) do |users|
  UserMailer.batch_send(users).deliver_later
end
```

**Eager loading with includes/joins**:
```ruby
# ❌ N+1 queries
posts = Post.all
posts.each { |p| puts "#{p.user.name}: #{p.title}" }

# ✅ includes (LEFT OUTER JOIN, loads associations)
posts = Post.includes(:user).all

# ✅ joins (INNER JOIN, doesn't load associations)
posts = Post.joins(:user).where(users: { active: true })

# ✅ preload (separate queries, good for multiple associations)
posts = Post.preload(:user, :comments).all

# ✅ eager_load (LEFT OUTER JOIN, forces eager loading)
posts = Post.eager_load(:user).all
```

### 7. View Optimization

**Avoid logic in views**:
```erb
<%# ❌ Bad: Complex logic in view %>
<% if @post.published? && @post.user.premium? && @post.comments.count > 10 %>
  Popular post!
<% end %>

<%# ✅ Good: Move to helper or presenter %>
<% if popular_post?(@post) %>
  Popular post!
<% end %>
```

**Minimize database queries in loops**:
```erb
<%# ❌ N+1 in view %>
<% @posts.each do |post| %>
  <%= post.user.name %>  <%# N queries! %>
<% end %>

<%# ✅ Eager load in controller %>
<%# PostsController: @posts = Post.includes(:user) %>
<% @posts.each do |post| %>
  <%= post.user.name %>
<% end %>
```

### 8. Background Jobs

**Move slow operations to background**:
```ruby
# ❌ Slow synchronous operation
class UsersController < ApplicationController
  def create
    @user = User.create(user_params)
    UserMailer.welcome_email(@user).deliver_now  # Slow!
    redirect_to root_path
  end
end

# ✅ Fast async operation
class UsersController < ApplicationController
  def create
    @user = User.create(user_params)
    UserMailer.welcome_email(@user).deliver_later  # Fast!
    redirect_to root_path
  end
end
```

### 9. Asset Optimization

**Compress assets**:
```ruby
# config/environments/production.rb
config.assets.compress = true
config.assets.js_compressor = :uglifier
config.assets.css_compressor = :sass
```

**Use CDN for assets**:
```ruby
# config/environments/production.rb
config.asset_host = 'https://cdn.example.com'
```

**Image optimization**:
- Use appropriate formats (WebP, AVIF)
- Resize images before upload
- Use image processing gems (image_processing)

### 10. HTTP Optimization

**Use HTTP/2** (automatic with Puma on HTTPS)

**Enable Gzip compression**:
```ruby
# config.ru
use Rack::Deflater
```

**Cache-Control headers**:
```ruby
# config/environments/production.rb
config.public_file_server.headers = {
  'Cache-Control' => 'public, max-age=31536000'
}
```

## Automation Script

### Performance Check Runner

```bash
# Run via: ruby .claude/skills/performance-check/scripts/performance_check.rb
```

The script checks:
1. N+1 query detection setup
2. Missing indexes
3. Slow query patterns
4. Memory usage
5. Caching configuration

## Common Performance Issues

### Issue 1: N+1 Queries

**Symptoms**: Slow page loads, many SQL queries

**Detection**:
- Bullet gem alerts
- Rails log shows repeated similar queries

**Fix**:
```ruby
# Use includes, joins, or preload
Post.includes(:user, :comments)
```

### Issue 2: Missing Indexes

**Symptoms**: Slow queries on WHERE clauses

**Detection**:
```ruby
# Check query EXPLAIN
Post.where(status: 'published').explain
```

**Fix**:
```ruby
# Add index in migration
add_index :posts, :status
add_index :posts, [:user_id, :status]  # Composite
```

### Issue 3: Loading Too Much Data

**Symptoms**: High memory usage, slow queries

**Fix**:
```ruby
# Use select, pluck, or limit
Post.select(:id, :title).limit(50)
```

### Issue 4: No Caching

**Symptoms**: Repeated expensive computations

**Fix**:
```ruby
# Add fragment caching
<% cache @post do %>
  <%= expensive_calculation(@post) %>
<% end %>

# Add counter caches
belongs_to :post, counter_cache: true
```

### Issue 5: Synchronous Long Operations

**Symptoms**: Slow response times

**Fix**:
```ruby
# Move to background job
SendEmailJob.perform_later(user_id)
```

## Benchmarking

**Simple benchmark**:
```ruby
require 'benchmark'

time = Benchmark.measure do
  Post.includes(:user).limit(100).to_a
end

puts "Time: #{time.real}s"
```

**Compare implementations**:
```ruby
require 'benchmark/ips'

Benchmark.ips do |x|
  x.report("map") { Post.all.map(&:id) }
  x.report("pluck") { Post.pluck(:id) }

  x.compare!
end
```

## Monitoring in Production

**Application Performance Monitoring (APM)**:
- Skylight
- New Relic
- Scout APM
- AppSignal

**Custom metrics** (with logging-setup skill):
```ruby
duration = Benchmark.realtime do
  # Operation
end

Loggers::BusinessLogger.log_performance(
  'complex_report',
  duration * 1000,  # ms
  { user_id: current_user.id }
)
```

## Best Practices

1. **Profile before optimizing**
   - Measure current performance
   - Identify actual bottlenecks
   - Don't optimize prematurely

2. **Use appropriate caching**
   - Fragment caching for views
   - Query caching (automatic)
   - Counter caches for counts

3. **Optimize database queries**
   - Add indexes for WHERE clauses
   - Use eager loading (includes)
   - Select only needed columns

4. **Background jobs for slow operations**
   - Email sending
   - File processing
   - External API calls

5. **Monitor continuously**
   - Use APM tools
   - Set up performance alerts
   - Regular performance reviews

6. **Load test before release**
   - Test with production-like data
   - Identify bottlenecks early
   - Plan scaling strategy

## Checklist

- [ ] Bullet gem configured (development)
- [ ] No N+1 queries in critical paths
- [ ] Indexes on all foreign keys
- [ ] Indexes on frequently queried columns
- [ ] Counter caches for frequent counts
- [ ] Fragment caching on expensive views
- [ ] Background jobs for slow operations
- [ ] Asset compression enabled (production)
- [ ] CDN configured (production)
- [ ] APM tool integrated (production)
- [ ] Regular performance reviews scheduled
