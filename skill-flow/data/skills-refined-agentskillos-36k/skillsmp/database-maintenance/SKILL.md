---
name: database-maintenance
description: Database maintenance and health checks. Use when user needs migration safety, data integrity, index optimization, or says "check database", "optimize DB", "migration rollback", "data consistency", "database health".
---

# Database Maintenance

데이터베이스 마이그레이션, 데이터 정합성, 인덱스 최적화 등 데이터베이스 유지보수 작업을 수행합니다.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Identify maintenance need
- [ ] 2. Run appropriate check/fix script
- [ ] 3. Review results
- [ ] 4. Apply fixes if needed
- [ ] 5. Verify database health
```

## Use Cases

✅ **When to use**:
- Before deploying migrations
- After major data changes
- Regular health checks
- Performance degradation
- Data inconsistency reports
- Index optimization needed

## Maintenance Tasks

### 1. Migration Safety Check

**Check pending migrations**:
```bash
rails db:migrate:status
```

**Dry-run migration** (check SQL without executing):
```ruby
# Add to migration file
def change
  reversible do |dir|
    dir.up do
      # Log what will happen
      Rails.logger.info "Will add index on users.email"
    end
  end

  add_index :users, :email, if_not_exists: true
end
```

**Safe migration patterns**:
```ruby
# ✅ Good: Add column with default
def change
  add_column :posts, :view_count, :integer, default: 0, null: false
end

# ✅ Good: Add index concurrently (PostgreSQL)
disable_ddl_transaction!
def change
  add_index :posts, :user_id, algorithm: :concurrently
end

# ❌ Bad: Remove column without safety period
def change
  remove_column :users, :legacy_field  # Dangerous!
end

# ✅ Good: Remove column with deprecation period
# Step 1: Ignore column (deploy)
class User < ApplicationRecord
  self.ignored_columns = [:legacy_field]
end

# Step 2: Remove column after all servers updated
def change
  remove_column :users, :legacy_field
end
```

### 2. Data Integrity Checks

**Foreign key validation**:
```ruby
# Check for orphaned records
Post.where.missing(:user).count
Comment.where.missing(:post).count

# Fix orphaned records
Post.where.missing(:user).delete_all
```

**Counter cache validation**:
```ruby
# Check counter cache accuracy
User.find_each do |user|
  actual_count = user.posts.count
  cached_count = user.posts_count

  if actual_count != cached_count
    puts "User #{user.id}: cached=#{cached_count}, actual=#{actual_count}"
    user.update_column(:posts_count, actual_count)
  end
end
```

**Uniqueness validation**:
```ruby
# Find duplicate emails
User.group(:email).having('COUNT(*) > 1').count

# Fix duplicates (keep oldest)
User.select(:email)
    .group(:email)
    .having('COUNT(*) > 1')
    .pluck(:email)
    .each do |email|
  users = User.where(email: email).order(:created_at)
  users[1..-1].each(&:destroy)
end
```

### 3. Index Optimization

**Find missing indexes**:
```ruby
# Check for foreign keys without indexes
ActiveRecord::Base.connection.tables.each do |table|
  columns = ActiveRecord::Base.connection.columns(table)

  columns.select { |c| c.name.end_with?('_id') }.each do |column|
    indexes = ActiveRecord::Base.connection.indexes(table)

    unless indexes.any? { |i| i.columns.include?(column.name) }
      puts "Missing index: #{table}.#{column.name}"
    end
  end
end
```

**Find unused indexes** (PostgreSQL):
```sql
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan as index_scans
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY schemaname, tablename;
```

**Add composite indexes**:
```ruby
# For queries like: Post.where(user_id: x, status: :published)
add_index :posts, [:user_id, :status]

# For queries with ORDER BY
add_index :posts, [:user_id, :created_at]
```

### 4. Database Health Check

**Connection pool status**:
```ruby
# Check active connections
pool = ActiveRecord::Base.connection_pool
puts "Size: #{pool.size}, Active: #{pool.connections.size}, Available: #{pool.available}"
```

**Table sizes** (PostgreSQL):
```sql
SELECT
  table_name,
  pg_size_pretty(pg_total_relation_size(quote_ident(table_name))) as size
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY pg_total_relation_size(quote_ident(table_name)) DESC;
```

**Slow queries log**:
```ruby
# config/environments/production.rb
config.active_record.logger = ActiveSupport::Logger.new('log/db_queries.log')
config.log_level = :debug

# Find slow queries (> 100ms)
# Requires logging setup from logging-setup skill
```

### 5. Migration Rollback

**Rollback last migration**:
```bash
rails db:rollback
```

**Rollback multiple steps**:
```bash
rails db:rollback STEP=3
```

**Rollback to specific version**:
```bash
rails db:migrate:down VERSION=20231219000000
```

**Safe rollback pattern**:
```ruby
class AddEmailToUsers < ActiveRecord::Migration[8.0]
  def up
    add_column :users, :email, :string
    add_index :users, :email, unique: true
  end

  def down
    remove_index :users, :email
    remove_column :users, :email
  end
end
```

### 6. Data Migration

**Backfill data safely**:
```ruby
# Use background job for large datasets
class BackfillUserEmailsJob < ApplicationJob
  def perform(batch_size: 1000)
    User.where(email: nil).find_in_batches(batch_size: batch_size) do |users|
      users.each do |user|
        user.update(email: generate_email(user))
      end

      # Sleep to avoid overloading DB
      sleep 0.1
    end
  end
end
```

**Data migration in migration file**:
```ruby
class MigrateOldDataToNewFormat < ActiveRecord::Migration[8.0]
  def up
    # Add new column
    add_column :posts, :metadata, :jsonb, default: {}

    # Migrate data in batches
    Post.find_each do |post|
      post.update_column(:metadata, {
        old_field: post.old_field,
        legacy_data: post.legacy_data
      })
    end
  end

  def down
    remove_column :posts, :metadata
  end
end
```

## Automation Scripts

### Database Health Check Script

```bash
# Run via: ruby .claude/skills/database-maintenance/scripts/health_check.rb
```

The script checks:
- Pending migrations
- Orphaned records
- Counter cache accuracy
- Missing indexes on foreign keys
- Connection pool status

### Index Optimization Script

```bash
# Run via: ruby .claude/skills/database-maintenance/scripts/optimize_indexes.rb
```

The script:
- Identifies missing indexes
- Suggests composite indexes
- Finds unused indexes

## Best Practices

### Migration Safety

1. **Always test migrations locally first**
2. **Use reversible migrations** (up/down methods)
3. **Add indexes with if_not_exists: true**
4. **Use disable_ddl_transaction! for large tables** (PostgreSQL)
5. **Never remove columns in same deploy** (deprecation period)

### Data Integrity

1. **Run integrity checks before major releases**
2. **Set up foreign key constraints** where appropriate
3. **Use database-level validations** (unique indexes)
4. **Regular counter cache resets**

### Performance

1. **Monitor query performance** (logging-setup skill)
2. **Add indexes for frequently queried columns**
3. **Use composite indexes for multi-column queries**
4. **Remove unused indexes** (they slow down writes)

### Backup & Recovery

1. **Always backup before major migrations**
2. **Test rollback procedures**
3. **Keep migration files in version control**
4. **Document destructive migrations**

## Common Issues & Solutions

### Issue: Migration fails in production
```bash
# 1. Check migration status
rails db:migrate:status

# 2. Rollback if partially applied
rails db:rollback

# 3. Fix migration file
# 4. Re-run migration
rails db:migrate
```

### Issue: Counter caches out of sync
```bash
# Reset all counter caches
rails runner "Post.find_each { |p| Post.reset_counters(p.id, :comments) }"
```

### Issue: Orphaned records causing errors
```ruby
# Find and clean orphaned records
Comment.includes(:post).where(posts: { id: nil }).delete_all
```

### Issue: Slow queries
```ruby
# 1. Enable query logging (logging-setup skill)
# 2. Identify slow queries
# 3. Add appropriate indexes
# 4. Optimize query with includes/joins
```

## PostgreSQL-Specific Tips

**Analyze tables after major changes**:
```sql
ANALYZE table_name;
```

**Vacuum to reclaim space**:
```sql
VACUUM ANALYZE;
```

**Reindex for performance**:
```sql
REINDEX INDEX index_name;
```

## SQLite-Specific Tips

**Integrity check**:
```bash
rails dbconsole
> PRAGMA integrity_check;
```

**Optimize database**:
```bash
rails dbconsole
> VACUUM;
> PRAGMA optimize;
```

## Monitoring & Alerts

Integrate with logging-setup skill for:
- Migration duration tracking
- Query performance monitoring
- Data integrity alerts

## Checklist

- [ ] Migrations tested locally
- [ ] Migrations are reversible
- [ ] Foreign keys have indexes
- [ ] Counter caches are accurate
- [ ] No orphaned records
- [ ] Backup taken before major changes
- [ ] Rollback procedure documented
- [ ] Performance impact assessed
