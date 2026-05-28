#!/usr/bin/env ruby
# Performance Check Script
# Usage: ruby performance_check.rb

require_relative '../../../config/environment'

class PerformanceCheck
  def self.run
    new.run
  end

  def run
    puts "⚡ Performance Check"
    puts "=" * 50

    check_bullet_setup
    check_missing_indexes
    check_counter_caches
    check_caching_setup
    check_eager_loading_opportunities

    puts "\n✅ Performance check complete!"
    puts "\n📋 Optimization Recommendations:"
    print_recommendations
  end

  private

  def check_bullet_setup
    puts "\n[1/5] Checking N+1 query detection..."

    if gem_available?('bullet')
      puts "  ✓ Bullet gem installed"

      dev_config_path = 'config/environments/development.rb'
      if File.exist?(dev_config_path)
        config = File.read(dev_config_path)

        if config.include?('Bullet.enable')
          puts "  ✓ Bullet is configured"
        else
          puts "  ⚠️  Bullet not configured in development.rb"
          puts "  Add Bullet configuration for N+1 detection"
        end
      end
    else
      puts "  ⚠️  Bullet gem not installed"
      puts "  Add to Gemfile: gem 'bullet', group: :development"
    end
  end

  def check_missing_indexes
    puts "\n[2/5] Checking for missing indexes..."

    missing = []

    ActiveRecord::Base.connection.tables.each do |table|
      next if table == 'schema_migrations' || table == 'ar_internal_metadata'

      columns = ActiveRecord::Base.connection.columns(table)
      indexes = ActiveRecord::Base.connection.indexes(table)

      # Check foreign key columns
      foreign_keys = columns.select { |c| c.name.end_with?('_id') }

      foreign_keys.each do |column|
        has_index = indexes.any? do |idx|
          idx.columns.include?(column.name) ||
          idx.columns.first == column.name
        end

        unless has_index
          missing << {
            table: table,
            column: column.name,
            suggestion: "add_index :#{table}, :#{column.name}"
          }
        end
      end
    end

    if missing.any?
      puts "  ⚠️  Missing indexes (#{missing.size} found):"
      missing.first(5).each do |info|
        puts "     - #{info[:table]}.#{info[:column]}"
        puts "       Fix: #{info[:suggestion]}"
      end
      puts "     ... and #{missing.size - 5} more" if missing.size > 5
    else
      puts "  ✓ All foreign keys have indexes"
    end
  end

  def check_counter_caches
    puts "\n[3/5] Checking counter cache usage..."

    recommendations = []

    # Check User posts_count
    if defined?(User) && defined?(Post)
      if User.column_names.include?('posts_count')
        puts "  ✓ User has posts_count counter cache"
      else
        recommendations << "Add posts_count to users table"
      end
    end

    # Check Post comments_count
    if defined?(Post) && defined?(Comment)
      if Post.column_names.include?('comments_count')
        puts "  ✓ Post has comments_count counter cache"
      else
        recommendations << "Add comments_count to posts table"
      end
    end

    # Check Post likes_count
    if defined?(Post) && Post.column_names.include?('likes_count')
      puts "  ✓ Post has likes_count counter cache"
    end

    if recommendations.any?
      puts "  💡 Consider adding counter caches:"
      recommendations.each { |rec| puts "     - #{rec}" }
    end
  end

  def check_caching_setup
    puts "\n[4/5] Checking caching configuration..."

    issues = []

    # Check if caching is enabled
    unless Rails.configuration.action_controller.perform_caching
      issues << "Caching disabled in current environment"
    end

    # Check cache store
    cache_store = Rails.configuration.cache_store
    if cache_store.nil? || cache_store.first == :null_store
      issues << "No cache store configured (using null_store)"
    else
      puts "  ✓ Cache store: #{cache_store.first}"
    end

    # Check for fragment caching in views
    view_files = Dir.glob('app/views/**/*.html.erb')
    cached_views = view_files.select { |f| File.read(f).include?('<% cache') }

    if cached_views.any?
      puts "  ✓ #{cached_views.size} views use fragment caching"
    else
      puts "  💡 Consider adding fragment caching to expensive views"
    end

    if issues.any?
      puts "  ⚠️  Caching issues:"
      issues.each { |issue| puts "     - #{issue}" }
    end
  end

  def check_eager_loading_opportunities
    puts "\n[5/5] Analyzing potential N+1 queries..."

    # Check controller code for common N+1 patterns
    controller_files = Dir.glob('app/controllers/**/*_controller.rb')

    potential_issues = []

    controller_files.each do |file|
      content = File.read(file)
      next unless content.include?('.all') || content.include?('.where')

      filename = File.basename(file)

      # Check if associations are used without includes
      if content.match?(/\.all\b/) && !content.include?('includes')
        potential_issues << "#{filename}: Consider using includes() for associations"
      end
    end

    if potential_issues.any?
      puts "  💡 Potential N+1 opportunities:"
      potential_issues.first(5).each { |issue| puts "     - #{issue}" }
    else
      puts "  ✓ Controllers look optimized"
    end

    puts "\n  💡 To detect N+1 at runtime:"
    puts "     1. Install bullet gem"
    puts "     2. Navigate pages in development"
    puts "     3. Check browser console for alerts"
  end

  def print_recommendations
    recommendations = [
      {
        priority: "HIGH",
        items: [
          "Add indexes to all foreign keys",
          "Fix N+1 queries (use includes/preload)",
          "Add counter caches for frequent counts",
          "Move slow operations to background jobs"
        ]
      },
      {
        priority: "MEDIUM",
        items: [
          "Enable fragment caching on expensive views",
          "Use select() to load only needed columns",
          "Configure production cache store (Redis/Memcached)",
          "Set up Bullet gem for N+1 detection"
        ]
      },
      {
        priority: "LOW",
        items: [
          "Use pluck() instead of map() for simple arrays",
          "Add composite indexes for multi-column queries",
          "Enable query caching where appropriate",
          "Consider APM tool (Skylight, New Relic)"
        ]
      }
    ]

    recommendations.each do |group|
      puts "\n  #{group[:priority]} Priority:"
      group[:items].each_with_index do |item, i|
        puts "    #{i + 1}. #{item}"
      end
    end

    puts "\n  📊 Performance Monitoring:"
    puts "     - Development: Use Bullet + rack-mini-profiler"
    puts "     - Production: Use APM tool + custom metrics"
    puts "     - Regular: Run this script before each release"
  end

  def gem_available?(gem_name)
    Gem::Specification.find_by_name(gem_name)
    true
  rescue Gem::LoadError
    false
  end
end

# Run performance check if executed directly
PerformanceCheck.run if __FILE__ == $PROGRAM_NAME
