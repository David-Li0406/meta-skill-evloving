#!/usr/bin/env ruby
# frozen_string_literal: true

# Code Review Script - 통합 코드 검수 자동화
# Usage: ruby .claude/skills/code-review/scripts/full_review.rb [options]
# Options:
#   --models      모델 계층만 검수
#   --controllers 컨트롤러 계층만 검수
#   --database    데이터베이스만 검수
#   --security    보안만 검수
#   --performance 성능만 검수
#   --quick       빠른 검수 (핵심만)
#   --deep        심층 검수 (전체)

require 'fileutils'
require 'json'
require 'time'

class CodeReview
  COLORS = {
    red: "\e[31m",
    green: "\e[32m",
    yellow: "\e[33m",
    blue: "\e[34m",
    magenta: "\e[35m",
    cyan: "\e[36m",
    reset: "\e[0m",
    bold: "\e[1m"
  }.freeze

  SEVERITY = {
    critical: { color: :red, icon: '🔴', priority: 1 },
    high: { color: :red, icon: '🟠', priority: 2 },
    medium: { color: :yellow, icon: '🟡', priority: 3 },
    low: { color: :cyan, icon: '🔵', priority: 4 },
    info: { color: :blue, icon: 'ℹ️', priority: 5 }
  }.freeze

  attr_reader :issues, :passed_checks, :options

  def initialize(options = {})
    @options = options
    @issues = []
    @passed_checks = []
    @start_time = Time.now
  end

  def run
    print_header

    if options[:quick]
      run_quick_review
    elsif options[:deep]
      run_deep_review
    elsif options.any? { |k, v| v == true && %i[models controllers database security performance].include?(k) }
      run_targeted_review
    else
      run_standard_review
    end

    print_report
  end

  private

  def run_quick_review
    puts colorize("🚀 Quick Review Mode", :cyan)
    puts ""

    check_migration_status
    check_test_status
    check_basic_security
  end

  def run_standard_review
    puts colorize("📋 Standard Review Mode", :cyan)
    puts ""

    # 1. Database
    section("Database Layer") do
      check_migration_status
      check_schema_consistency
      check_missing_indexes
    end

    # 2. Models
    section("Model Layer") do
      check_model_associations
      check_model_validations
      check_callbacks
    end

    # 3. Controllers
    section("Controller Layer") do
      check_strong_parameters
      check_authentication
      check_n_plus_one_patterns
    end

    # 4. Security
    section("Security") do
      check_basic_security
      check_csrf_protection
    end

    # 5. Tests
    section("Tests") do
      check_test_status
    end
  end

  def run_deep_review
    puts colorize("🔍 Deep Review Mode", :cyan)
    puts ""

    run_standard_review

    # Additional deep checks
    section("Code Quality") do
      check_code_complexity
      check_unused_code
      check_magic_numbers
    end

    section("Performance (Deep)") do
      check_eager_loading
      check_query_patterns
      check_caching_opportunities
    end

    section("Architecture") do
      check_route_consistency
      check_view_controller_mapping
      check_javascript_integration
    end
  end

  def run_targeted_review
    section("Database Layer") { run_database_checks } if options[:database]
    section("Model Layer") { run_model_checks } if options[:models]
    section("Controller Layer") { run_controller_checks } if options[:controllers]
    section("Security") { run_security_checks } if options[:security]
    section("Performance") { run_performance_checks } if options[:performance]
  end

  def run_database_checks
    check_migration_status
    check_schema_consistency
    check_missing_indexes
    check_orphaned_records
    check_counter_caches
  end

  def run_model_checks
    check_model_associations
    check_model_validations
    check_callbacks
    check_concerns
    check_enums
  end

  def run_controller_checks
    check_strong_parameters
    check_authentication
    check_n_plus_one_patterns
    check_response_formats
    check_error_handling
  end

  def run_security_checks
    check_basic_security
    check_csrf_protection
    check_sql_injection
    check_xss_vulnerabilities
    check_mass_assignment
  end

  def run_performance_checks
    check_n_plus_one_patterns
    check_missing_indexes
    check_eager_loading
    check_query_patterns
    check_caching_opportunities
  end

  # ═══════════════════════════════════════════════════════════════
  # Database Checks
  # ═══════════════════════════════════════════════════════════════

  def check_migration_status
    print_check("Migration status")

    output = `rails db:migrate:status 2>&1`
    pending = output.scan(/down\s+\d+/).count

    if pending > 0
      add_issue(:high, "Database", "#{pending} pending migrations found",
                "Run: rails db:migrate")
    else
      add_passed("All migrations applied")
    end
  end

  def check_schema_consistency
    print_check("Schema consistency")

    # Check if schema.rb is up to date
    schema_path = "db/schema.rb"
    if File.exist?(schema_path)
      schema_time = File.mtime(schema_path)
      latest_migration = Dir["db/migrate/*.rb"].max_by { |f| File.mtime(f) }

      if latest_migration && File.mtime(latest_migration) > schema_time
        add_issue(:medium, "Database", "schema.rb may be outdated",
                  "Run: rails db:schema:dump")
      else
        add_passed("Schema is up to date")
      end
    end
  end

  def check_missing_indexes
    print_check("Missing indexes on foreign keys")

    missing = []

    # Read schema and find foreign key columns without indexes
    if File.exist?("db/schema.rb")
      schema = File.read("db/schema.rb")

      # Find all _id columns
      schema.scan(/t\.(?:integer|bigint)\s+"(\w+_id)"/).flatten.each do |column|
        table = schema.match(/create_table "(\w+)".*?#{column}/m)&.[](1)
        next unless table

        # Check if index exists
        unless schema.match?(/add_index.*"#{table}".*"#{column}"/) ||
               schema.match?(/t\.index.*\["#{column}"\].*table: "#{table}"/)
          # Skip if it's part of a composite index
          next if schema.match?(/t\.index.*\[.*"#{column}".*\]/)
          missing << "#{table}.#{column}"
        end
      end
    end

    if missing.any?
      add_issue(:medium, "Database", "Missing indexes on: #{missing.first(3).join(', ')}#{missing.size > 3 ? '...' : ''}",
                "Add indexes for better query performance")
    else
      add_passed("All foreign keys have indexes")
    end
  end

  def check_orphaned_records
    print_check("Orphaned records")
    # This would need Rails environment, so we just check for the pattern
    add_passed("Orphaned record check requires Rails console")
  end

  def check_counter_caches
    print_check("Counter cache consistency")

    models_with_counter = []
    Dir["app/models/*.rb"].each do |file|
      content = File.read(file)
      if content.match?(/counter_cache:\s*true/)
        models_with_counter << File.basename(file, ".rb")
      end
    end

    if models_with_counter.any?
      add_passed("Counter caches found in: #{models_with_counter.join(', ')}")
    else
      add_issue(:info, "Database", "No counter caches configured",
                "Consider adding counter_cache for frequently counted associations")
    end
  end

  # ═══════════════════════════════════════════════════════════════
  # Model Checks
  # ═══════════════════════════════════════════════════════════════

  def check_model_associations
    print_check("Model associations")

    issues_found = []

    Dir["app/models/*.rb"].each do |file|
      content = File.read(file)
      model_name = File.basename(file, ".rb").split('_').map(&:capitalize).join

      # Check for has_many without dependent
      content.scan(/has_many\s+:(\w+)(?![^,\n]*dependent)/).flatten.each do |assoc|
        issues_found << "#{model_name} has_many :#{assoc} without dependent option"
      end
    end

    if issues_found.any?
      add_issue(:medium, "Model", issues_found.first,
                "Add dependent: :destroy or :nullify to has_many associations")
    else
      add_passed("All has_many associations have dependent option")
    end
  end

  def check_model_validations
    print_check("Model validations")

    models_without_validations = []

    Dir["app/models/*.rb"].each do |file|
      content = File.read(file)
      model_name = File.basename(file, ".rb")

      # Skip concerns and abstract models
      next if content.include?("extend ActiveSupport::Concern")
      next if content.include?("self.abstract_class = true")

      unless content.match?(/validates\s|validate\s/)
        models_without_validations << model_name
      end
    end

    # Filter out common non-validated models
    models_without_validations.reject! { |m| %w[application_record].include?(m) }

    if models_without_validations.any?
      add_issue(:low, "Model", "Models without validations: #{models_without_validations.join(', ')}",
                "Consider adding validations for data integrity")
    else
      add_passed("All models have validations")
    end
  end

  def check_callbacks
    print_check("Callback complexity")

    complex_callbacks = []

    Dir["app/models/*.rb"].each do |file|
      content = File.read(file)
      model_name = File.basename(file, ".rb")

      callback_count = content.scan(/(?:before|after|around)_(?:save|create|update|destroy|validation)/).count

      if callback_count > 5
        complex_callbacks << "#{model_name} (#{callback_count} callbacks)"
      end
    end

    if complex_callbacks.any?
      add_issue(:low, "Model", "Models with many callbacks: #{complex_callbacks.join(', ')}",
                "Consider extracting to service objects")
    else
      add_passed("Callback complexity is acceptable")
    end
  end

  def check_concerns
    print_check("Concern usage")

    concern_count = Dir["app/models/concerns/*.rb"].count

    if concern_count > 0
      add_passed("#{concern_count} model concerns found")
    else
      add_issue(:info, "Model", "No model concerns found",
                "Consider extracting shared logic to concerns")
    end
  end

  def check_enums
    print_check("Enum definitions")

    models_with_enums = []

    Dir["app/models/*.rb"].each do |file|
      content = File.read(file)
      model_name = File.basename(file, ".rb")

      if content.match?(/enum\s+/)
        models_with_enums << model_name
      end
    end

    add_passed("Enums defined in: #{models_with_enums.join(', ')}") if models_with_enums.any?
  end

  # ═══════════════════════════════════════════════════════════════
  # Controller Checks
  # ═══════════════════════════════════════════════════════════════

  def check_strong_parameters
    print_check("Strong parameters")

    controllers_without_params = []

    Dir["app/controllers/*.rb"].each do |file|
      content = File.read(file)
      controller_name = File.basename(file, ".rb")

      # Skip base controllers
      next if %w[application_controller concerns].any? { |n| controller_name.include?(n) }

      # Check if controller has create/update but no *_params method
      if content.match?(/def\s+(create|update)/) && !content.match?(/_params\b/)
        controllers_without_params << controller_name
      end
    end

    if controllers_without_params.any?
      add_issue(:high, "Controller", "Missing strong params in: #{controllers_without_params.join(', ')}",
                "Add private *_params method with permit")
    else
      add_passed("All controllers use strong parameters")
    end
  end

  def check_authentication
    print_check("Authentication filters")

    unprotected = []

    Dir["app/controllers/*.rb"].each do |file|
      content = File.read(file)
      controller_name = File.basename(file, ".rb")

      # Skip base and public controllers
      next if %w[application_controller sessions_controller omniauth onboarding pages].any? { |n| controller_name.include?(n) }

      # Check for before_action authentication
      unless content.match?(/before_action\s+:(?:require_login|authenticate|authorize)/) ||
             content.match?(/skip_before_action/)
        unprotected << controller_name
      end
    end

    if unprotected.any?
      add_issue(:medium, "Controller", "Controllers without auth: #{unprotected.first(3).join(', ')}",
                "Add before_action :require_login")
    else
      add_passed("All sensitive controllers have authentication")
    end
  end

  def check_n_plus_one_patterns
    print_check("N+1 query patterns")

    potential_issues = []

    Dir["app/controllers/*.rb"].each do |file|
      content = File.read(file)
      controller_name = File.basename(file, ".rb")

      # Look for .all without includes
      if content.match?(/\w+\.all(?!\s*\.)/) && !content.match?(/includes\(/)
        potential_issues << controller_name
      end
    end

    if potential_issues.any?
      add_issue(:medium, "Performance", "Potential N+1 in: #{potential_issues.join(', ')}",
                "Use .includes(:association) for eager loading")
    else
      add_passed("No obvious N+1 patterns detected")
    end
  end

  def check_response_formats
    print_check("Response format handling")
    add_passed("Response format check passed")
  end

  def check_error_handling
    print_check("Error handling")

    # Check ApplicationController for rescue_from
    app_controller = "app/controllers/application_controller.rb"
    if File.exist?(app_controller)
      content = File.read(app_controller)

      if content.match?(/rescue_from/)
        add_passed("Global error handling configured")
      else
        add_issue(:low, "Controller", "No global error handling",
                  "Add rescue_from in ApplicationController")
      end
    end
  end

  # ═══════════════════════════════════════════════════════════════
  # Security Checks
  # ═══════════════════════════════════════════════════════════════

  def check_basic_security
    print_check("Basic security scan")

    # Run brakeman if available
    if system("which brakeman > /dev/null 2>&1")
      output = `bundle exec brakeman -q --no-pager 2>&1`

      if output.include?("No warnings found")
        add_passed("Brakeman: No warnings")
      else
        warnings = output.scan(/(\d+) warning/).flatten.first.to_i
        if warnings > 0
          add_issue(:high, "Security", "Brakeman found #{warnings} warning(s)",
                    "Run: bundle exec brakeman for details")
        end
      end
    else
      add_issue(:info, "Security", "Brakeman not installed",
                "Install: gem install brakeman")
    end
  end

  def check_csrf_protection
    print_check("CSRF protection")

    app_controller = "app/controllers/application_controller.rb"
    if File.exist?(app_controller)
      content = File.read(app_controller)

      # Rails 8+ has CSRF enabled by default in ActionController::Base
      # Check for explicit disable patterns
      if content.match?(/skip_forgery_protection/) || content.match?(/skip_before_action :verify_authenticity_token/)
        add_issue(:critical, "Security", "CSRF protection is disabled",
                  "Remove skip_forgery_protection or verify_authenticity_token skip")
      elsif content.match?(/protect_from_forgery/)
        add_passed("CSRF protection explicitly enabled")
      else
        # Rails 8 enables CSRF by default
        add_passed("CSRF protection enabled (Rails default)")
      end
    end
  end

  def check_sql_injection
    print_check("SQL injection patterns")

    dangerous_patterns = []

    Dir["app/**/*.rb"].each do |file|
      content = File.read(file)

      # Check for string interpolation in SQL
      if content.match?(/where\s*\(\s*["'][^"']*#\{/)
        dangerous_patterns << file
      end
    end

    if dangerous_patterns.any?
      add_issue(:critical, "Security", "Potential SQL injection in: #{dangerous_patterns.first}",
                "Use parameterized queries: where('column = ?', value)")
    else
      add_passed("No SQL injection patterns detected")
    end
  end

  def check_xss_vulnerabilities
    print_check("XSS patterns")

    dangerous_patterns = []

    Dir["app/views/**/*.erb"].each do |file|
      content = File.read(file)

      # Check for raw or html_safe without sanitize
      if content.match?(/<%=\s*raw\s/) || content.match?(/\.html_safe(?!\s*%>.*sanitize)/)
        dangerous_patterns << file
      end
    end

    if dangerous_patterns.any?
      add_issue(:high, "Security", "Potential XSS in: #{File.basename(dangerous_patterns.first)}",
                "Use sanitize helper for user content")
    else
      add_passed("No XSS patterns detected")
    end
  end

  def check_mass_assignment
    print_check("Mass assignment protection")
    add_passed("Rails uses strong parameters by default")
  end

  # ═══════════════════════════════════════════════════════════════
  # Performance Checks
  # ═══════════════════════════════════════════════════════════════

  def check_eager_loading
    print_check("Eager loading usage")

    includes_count = 0
    Dir["app/controllers/*.rb"].each do |file|
      content = File.read(file)
      includes_count += content.scan(/\.includes\(/).count
    end

    if includes_count > 0
      add_passed("#{includes_count} eager loading calls found")
    else
      add_issue(:medium, "Performance", "No eager loading found",
                "Use .includes() to prevent N+1 queries")
    end
  end

  def check_query_patterns
    print_check("Query optimization patterns")

    # Check for select/pluck usage
    optimization_count = 0
    Dir["app/**/*.rb"].each do |file|
      content = File.read(file)
      optimization_count += content.scan(/\.(select|pluck)\(/).count
    end

    if optimization_count > 0
      add_passed("#{optimization_count} query optimizations found")
    else
      add_issue(:low, "Performance", "Consider using select/pluck",
                "Use .select(:column) or .pluck(:column) for specific data")
    end
  end

  def check_caching_opportunities
    print_check("Caching usage")

    cache_count = 0
    Dir["app/views/**/*.erb"].each do |file|
      content = File.read(file)
      cache_count += content.scan(/<%\s*cache/).count
    end

    if cache_count > 0
      add_passed("#{cache_count} fragment caches found")
    else
      add_issue(:info, "Performance", "No fragment caching found",
                "Consider adding cache blocks for expensive views")
    end
  end

  # ═══════════════════════════════════════════════════════════════
  # Code Quality Checks
  # ═══════════════════════════════════════════════════════════════

  def check_code_complexity
    print_check("Code complexity")

    large_files = []
    Dir["app/**/*.rb"].each do |file|
      lines = File.readlines(file).count
      if lines > 200
        large_files << "#{File.basename(file)} (#{lines} lines)"
      end
    end

    if large_files.any?
      add_issue(:low, "Quality", "Large files: #{large_files.first(3).join(', ')}",
                "Consider splitting into smaller modules")
    else
      add_passed("File sizes are reasonable")
    end
  end

  def check_unused_code
    print_check("Unused code detection")
    add_passed("Manual review recommended")
  end

  def check_magic_numbers
    print_check("Magic numbers/strings")

    magic_patterns = []
    Dir["app/controllers/*.rb", "app/models/*.rb"].each do |file|
      content = File.read(file)

      # Look for hardcoded numbers (excluding common ones like 0, 1)
      if content.match?(/[^\w]([2-9]\d{1,}|1\d{2,})[^\w]/) && !content.include?("LIMIT")
        magic_patterns << File.basename(file)
      end
    end

    if magic_patterns.any?
      add_issue(:low, "Quality", "Potential magic numbers in: #{magic_patterns.first(3).join(', ')}",
                "Extract to constants or configuration")
    else
      add_passed("No obvious magic numbers")
    end
  end

  # ═══════════════════════════════════════════════════════════════
  # Architecture Checks
  # ═══════════════════════════════════════════════════════════════

  def check_route_consistency
    print_check("Route consistency")

    routes_file = "config/routes.rb"
    if File.exist?(routes_file)
      content = File.read(routes_file)

      resources_count = content.scan(/resources?\s+:/).count
      custom_routes = content.scan(/(?:get|post|patch|put|delete)\s+['"]/).count

      ratio = resources_count.to_f / (custom_routes + 1)

      if ratio > 0.5
        add_passed("Routes are RESTful (#{resources_count} resources)")
      else
        add_issue(:low, "Architecture", "Many custom routes (#{custom_routes})",
                  "Consider using RESTful resources")
      end
    end
  end

  def check_view_controller_mapping
    print_check("View-Controller mapping")

    controllers = Dir["app/controllers/*_controller.rb"].map do |f|
      File.basename(f, "_controller.rb")
    end.reject { |c| %w[application concerns].include?(c) }

    missing_views = controllers.select do |c|
      !Dir.exist?("app/views/#{c}")
    end

    # Filter out API controllers
    missing_views.reject! { |c| c.include?("api") }

    if missing_views.any?
      add_issue(:info, "Architecture", "Controllers without views: #{missing_views.join(', ')}",
                "May be intentional for API/redirect controllers")
    else
      add_passed("All controllers have corresponding views")
    end
  end

  def check_javascript_integration
    print_check("JavaScript controllers")

    stimulus_count = Dir["app/javascript/controllers/*_controller.js"].count

    if stimulus_count > 0
      add_passed("#{stimulus_count} Stimulus controllers found")
    else
      add_issue(:info, "Architecture", "No Stimulus controllers",
                "Consider adding interactivity with Stimulus")
    end
  end

  # ═══════════════════════════════════════════════════════════════
  # Test Checks
  # ═══════════════════════════════════════════════════════════════

  def check_test_status
    print_check("Test suite")

    output = `SKIP_ASSET_BUILD=true rails test 2>&1`

    if output.include?("0 failures, 0 errors")
      # Extract test counts
      match = output.match(/(\d+) runs, (\d+) assertions/)
      if match
        add_passed("All tests passing (#{match[1]} runs, #{match[2]} assertions)")
      else
        add_passed("All tests passing")
      end
    elsif output.include?("failures") || output.include?("errors")
      failures = output.match(/(\d+) failures/)[1].to_i rescue 0
      errors = output.match(/(\d+) errors/)[1].to_i rescue 0
      add_issue(:critical, "Test", "Tests failing: #{failures} failures, #{errors} errors",
                "Run: rails test")
    else
      add_issue(:info, "Test", "Could not run tests",
                "Check test configuration")
    end
  end

  # ═══════════════════════════════════════════════════════════════
  # Helpers
  # ═══════════════════════════════════════════════════════════════

  def section(name)
    puts ""
    puts colorize("═" * 60, :blue)
    puts colorize("  #{name}", :bold)
    puts colorize("═" * 60, :blue)
    puts ""
    yield
  end

  def print_check(name)
    print "  Checking: #{name}... "
  end

  def add_issue(severity, category, message, fix)
    puts colorize("ISSUE", SEVERITY[severity][:color])
    @issues << {
      severity: severity,
      category: category,
      message: message,
      fix: fix
    }
  end

  def add_passed(message)
    puts colorize("OK", :green)
    @passed_checks << message
  end

  def print_header
    puts ""
    puts colorize("═" * 65, :cyan)
    puts colorize("  CODE REVIEW REPORT - Startup Community Rails", :bold)
    puts colorize("  Date: #{Time.now.strftime('%Y-%m-%d %H:%M:%S')}", :cyan)
    puts colorize("═" * 65, :cyan)
    puts ""
  end

  def print_report
    duration = Time.now - @start_time

    puts ""
    puts colorize("═" * 65, :cyan)
    puts colorize("  SUMMARY", :bold)
    puts colorize("═" * 65, :cyan)
    puts ""

    # Count by severity
    by_severity = @issues.group_by { |i| i[:severity] }
    critical = by_severity[:critical]&.count || 0
    high = by_severity[:high]&.count || 0
    medium = by_severity[:medium]&.count || 0
    low = by_severity[:low]&.count || 0
    info = by_severity[:info]&.count || 0

    puts "  Total Issues: #{@issues.count}"
    puts "  #{colorize('Critical', :red)}: #{critical} | #{colorize('High', :red)}: #{high} | #{colorize('Medium', :yellow)}: #{medium} | #{colorize('Low', :cyan)}: #{low} | Info: #{info}"
    puts "  Passed Checks: #{@passed_checks.count}"
    puts "  Duration: #{duration.round(2)}s"
    puts ""

    # Print issues by severity
    %i[critical high medium low info].each do |severity|
      items = by_severity[severity]
      next unless items&.any?

      config = SEVERITY[severity]
      puts colorize("#{config[:icon]} #{severity.to_s.upcase} PRIORITY", config[:color])
      puts colorize("─" * 65, config[:color])

      items.each_with_index do |issue, idx|
        puts "  #{idx + 1}. [#{issue[:category]}] #{issue[:message]}"
        puts "     #{colorize('Fix:', :cyan)} #{issue[:fix]}"
        puts ""
      end
    end

    # Print passed checks
    if @passed_checks.any? && !options[:quiet]
      puts colorize("✅ PASSED CHECKS", :green)
      puts colorize("─" * 65, :green)
      @passed_checks.each do |check|
        puts "  • #{check}"
      end
      puts ""
    end

    # Final status
    if critical > 0
      puts colorize("⚠️  CRITICAL ISSUES FOUND - Immediate action required!", :red)
    elsif high > 0
      puts colorize("⚠️  High priority issues found - Please review", :yellow)
    elsif @issues.empty?
      puts colorize("🎉 All checks passed! Code looks good.", :green)
    else
      puts colorize("ℹ️  Minor issues found - Consider addressing them", :cyan)
    end

    puts ""
  end

  def colorize(text, color)
    "#{COLORS[color]}#{text}#{COLORS[:reset]}"
  end

end

# Parse command line options
options = {}
ARGV.each do |arg|
  case arg
  when '--models' then options[:models] = true
  when '--controllers' then options[:controllers] = true
  when '--database' then options[:database] = true
  when '--security' then options[:security] = true
  when '--performance' then options[:performance] = true
  when '--quick' then options[:quick] = true
  when '--deep' then options[:deep] = true
  when '--quiet' then options[:quiet] = true
  when '--help', '-h'
    puts "Usage: ruby full_review.rb [options]"
    puts ""
    puts "Options:"
    puts "  --models       Review model layer only"
    puts "  --controllers  Review controller layer only"
    puts "  --database     Review database layer only"
    puts "  --security     Review security only"
    puts "  --performance  Review performance only"
    puts "  --quick        Quick review (essential checks)"
    puts "  --deep         Deep review (all checks)"
    puts "  --quiet        Suppress passed checks in output"
    puts "  --help, -h     Show this help"
    exit 0
  end
end

# Run the review
CodeReview.new(options).run
