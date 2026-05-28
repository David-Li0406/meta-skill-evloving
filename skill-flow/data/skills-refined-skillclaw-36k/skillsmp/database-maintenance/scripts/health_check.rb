#!/usr/bin/env ruby
# Database Health Check Script
# Usage: ruby health_check.rb

require_relative '../../../config/environment'

class DatabaseHealthCheck
  def self.run
    new.run
  end

  def run
    puts "🔍 Database Health Check"
    puts "=" * 50

    check_pending_migrations
    check_orphaned_records
    check_counter_caches
    check_missing_indexes
    check_connection_pool
    check_table_sizes

    puts "\n✅ Health check complete!"
  end

  private

  def check_pending_migrations
    puts "\n[1/6] Checking pending migrations..."

    pending = ActiveRecord::Base.connection.migration_context.needs_migration?

    if pending
      puts "  ⚠️  Warning: Pending migrations detected"
      puts "  Run: rails db:migrate"
    else
      puts "  ✓ No pending migrations"
    end
  end

  def check_orphaned_records
    puts "\n[2/6] Checking for orphaned records..."

    orphaned = []

    # Check posts without users
    if defined?(Post)
      count = Post.where.missing(:user).count
      orphaned << "Posts without user: #{count}" if count > 0
    end

    # Check comments without posts
    if defined?(Comment)
      count = Comment.where.missing(:post).count
      orphaned << "Comments without post: #{count}" if count > 0
    end

    # Check job_posts without users
    if defined?(JobPost)
      count = JobPost.where.missing(:user).count
      orphaned << "JobPosts without user: #{count}" if count > 0
    end

    if orphaned.any?
      puts "  ⚠️  Orphaned records found:"
      orphaned.each { |msg| puts "     - #{msg}" }
    else
      puts "  ✓ No orphaned records"
    end
  end

  def check_counter_caches
    puts "\n[3/6] Checking counter caches..."

    issues = []

    # Check User posts_count
    if defined?(User) && User.column_names.include?('posts_count')
      User.find_each do |user|
        actual = user.posts.count
        cached = user.posts_count || 0

        if actual != cached
          issues << "User ##{user.id}: posts_count=#{cached}, actual=#{actual}"
        end
      end
    end

    # Check Post comments_count
    if defined?(Post) && Post.column_names.include?('comments_count')
      Post.find_each do |post|
        actual = post.comments.count
        cached = post.comments_count || 0

        if actual != cached
          issues << "Post ##{post.id}: comments_count=#{cached}, actual=#{actual}"
        end
      end
    end

    if issues.any?
      puts "  ⚠️  Counter cache mismatches:"
      issues.first(5).each { |msg| puts "     - #{msg}" }
      puts "     ... and #{issues.size - 5} more" if issues.size > 5
      puts "  Fix with: rails runner 'User.find_each { |u| User.reset_counters(u.id, :posts) }'"
    else
      puts "  ✓ Counter caches are accurate"
    end
  end

  def check_missing_indexes
    puts "\n[4/6] Checking for missing indexes..."

    missing = []

    ActiveRecord::Base.connection.tables.each do |table|
      next if table == 'schema_migrations' || table == 'ar_internal_metadata'

      columns = ActiveRecord::Base.connection.columns(table)
      indexes = ActiveRecord::Base.connection.indexes(table)

      # Check foreign key columns
      columns.select { |c| c.name.end_with?('_id') }.each do |column|
        has_index = indexes.any? do |idx|
          idx.columns.include?(column.name) ||
          idx.columns.first == column.name
        end

        missing << "#{table}.#{column.name}" unless has_index
      end
    end

    if missing.any?
      puts "  ⚠️  Missing indexes on foreign keys:"
      missing.first(10).each { |col| puts "     - #{col}" }
      puts "     ... and #{missing.size - 10} more" if missing.size > 10
    else
      puts "  ✓ All foreign keys have indexes"
    end
  end

  def check_connection_pool
    puts "\n[5/6] Checking connection pool..."

    pool = ActiveRecord::Base.connection_pool

    size = pool.size
    active = pool.connections.size
    available = size - active

    puts "  Pool size: #{size}"
    puts "  Active connections: #{active}"
    puts "  Available connections: #{available}"

    if available < 2
      puts "  ⚠️  Low available connections!"
    else
      puts "  ✓ Connection pool healthy"
    end
  end

  def check_table_sizes
    puts "\n[6/6] Checking table sizes..."

    if sqlite?
      check_sqlite_sizes
    elsif postgresql?
      check_postgresql_sizes
    else
      puts "  ℹ️  Table size check not supported for this database"
    end
  end

  def sqlite?
    ActiveRecord::Base.connection.adapter_name.downcase == 'sqlite'
  end

  def postgresql?
    ActiveRecord::Base.connection.adapter_name.downcase.include?('postgres')
  end

  def check_sqlite_sizes
    # SQLite doesn't have easy table size queries
    db_file = ActiveRecord::Base.connection_db_config.database
    if File.exist?(db_file)
      size_mb = File.size(db_file) / 1024.0 / 1024.0
      puts "  Database size: #{size_mb.round(2)} MB"
    end
  end

  def check_postgresql_sizes
    sql = <<~SQL
      SELECT
        table_name,
        pg_size_pretty(pg_total_relation_size(quote_ident(table_name))) as size
      FROM information_schema.tables
      WHERE table_schema = 'public'
      ORDER BY pg_total_relation_size(quote_ident(table_name)) DESC
      LIMIT 10;
    SQL

    results = ActiveRecord::Base.connection.execute(sql)

    puts "  Top 10 largest tables:"
    results.each do |row|
      puts "     - #{row['table_name']}: #{row['size']}"
    end
  end
end

# Run health check if executed directly
DatabaseHealthCheck.run if __FILE__ == $PROGRAM_NAME
