#!/usr/bin/env ruby
# Logging Setup Script
# Usage: ruby setup_logging.rb

require 'fileutils'

class LoggingSetup
  def self.run
    new.run
  end

  def run
    puts "🔧 Setting up logging system..."

    create_directories
    create_business_logger
    create_request_logger_concern
    create_lograge_initializer
    create_sentry_initializer
    update_application_controller
    update_application_job
    update_production_config
    add_gemfile_dependencies

    puts "\n✅ Logging setup complete!"
    puts "\n📋 Next steps:"
    puts "  1. Run: bundle install"
    puts "  2. (Optional) Add SENTRY_DSN to .env"
    puts "  3. Restart server"
    puts "  4. Check logs: tail -f log/development.log"
  end

  private

  def create_directories
    puts "\n[1/9] Creating directories..."
    FileUtils.mkdir_p('app/services/loggers')
    puts "  ✓ Created app/services/loggers/"
  end

  def create_business_logger
    puts "\n[2/9] Creating Business Logger..."

    content = <<~RUBY
      # Business event logger for tracking important domain events
      module Loggers
        class BusinessLogger
          def self.log_event(event_type, details = {})
            Rails.logger.info({
              event: event_type,
              timestamp: Time.current.iso8601,
              environment: Rails.env,
              **details
            }.to_json)
          end

          def self.log_user_action(user, action, resource = nil)
            log_event('user_action', {
              user_id: user.id,
              user_email: user.email,
              action: action,
              resource_type: resource&.class&.name,
              resource_id: resource&.id
            })
          end

          def self.log_error(error, context = {})
            log_event('error', {
              error_class: error.class.name,
              error_message: error.message,
              backtrace: error.backtrace&.first(5),
              **context
            })
          end

          def self.log_performance(operation, duration_ms, details = {})
            level = duration_ms > 1000 ? :warn : :info

            Rails.logger.public_send(level, {
              event: 'performance',
              operation: operation,
              duration_ms: duration_ms.round(2),
              **details
            }.to_json)
          end
        end
      end
    RUBY

    File.write('app/services/loggers/business_logger.rb', content)
    puts "  ✓ Created app/services/loggers/business_logger.rb"
  end

  def create_request_logger_concern
    puts "\n[3/9] Creating Request Logger Concern..."

    FileUtils.mkdir_p('app/controllers/concerns')

    content = <<~RUBY
      # Request performance logger for all controller actions
      module RequestLogger
        extend ActiveSupport::Concern

        included do
          around_action :log_request_performance
        end

        private

        def log_request_performance
          start_time = Time.current

          yield

          duration = Time.current - start_time
          duration_ms = (duration * 1000).round(2)

          log_data = {
            type: 'request_performance',
            controller: controller_name,
            action: action_name,
            method: request.method,
            path: request.fullpath,
            status: response.status,
            duration_ms: duration_ms,
            user_id: try(:current_user)&.id,
            ip: request.remote_ip
          }

          if duration > 1.0
            Rails.logger.warn(log_data.merge(warning: 'slow_request').to_json)
          else
            Rails.logger.info(log_data.to_json)
          end
        end
      end
    RUBY

    File.write('app/controllers/concerns/request_logger.rb', content)
    puts "  ✓ Created app/controllers/concerns/request_logger.rb"
  end

  def create_lograge_initializer
    puts "\n[4/9] Creating Lograge Initializer..."

    content = <<~RUBY
      # Lograge configuration for structured logging
      Rails.application.configure do
        # Enable Lograge
        config.lograge.enabled = true

        # Use JSON formatter
        config.lograge.formatter = Lograge::Formatters::Json.new

        # Custom options to add to every log entry
        config.lograge.custom_options = lambda do |event|
          {
            user_id: event.payload[:user_id],
            ip: event.payload[:ip],
            host: event.payload[:host],
            params: event.payload[:params]&.except('controller', 'action', 'format')
          }
        end

        # Ignore health check endpoints
        config.lograge.ignore_actions = ['HealthController#check', 'Rails::HealthController#show']

        # Add custom data to payload
        config.lograge.custom_payload do |controller|
          {
            host: controller.request.host,
            user_id: controller.try(:current_user)&.id,
            ip: controller.request.remote_ip
          }
        end
      end
    RUBY

    File.write('config/initializers/lograge.rb', content)
    puts "  ✓ Created config/initializers/lograge.rb"
  end

  def create_sentry_initializer
    puts "\n[5/9] Creating Sentry Initializer (optional)..."

    content = <<~RUBY
      # Sentry error tracking configuration
      # Add SENTRY_DSN to your environment variables to enable

      if ENV['SENTRY_DSN'].present?
        Sentry.init do |config|
          config.dsn = ENV['SENTRY_DSN']
          config.breadcrumbs_logger = [:active_support_logger, :http_logger]

          # Environment
          config.environment = Rails.env
          config.enabled_environments = %w[production staging]

          # Sampling (send 10% of transactions)
          config.traces_sample_rate = 0.1

          # Filter sensitive data
          config.send_default_pii = false

          # Exclude common exceptions
          config.excluded_exceptions += [
            'ActiveRecord::RecordNotFound',
            'ActionController::RoutingError'
          ]
        end
      end
    RUBY

    File.write('config/initializers/sentry.rb', content)
    puts "  ✓ Created config/initializers/sentry.rb"
  end

  def update_application_controller
    puts "\n[6/9] Updating ApplicationController..."

    file_path = 'app/controllers/application_controller.rb'

    if File.exist?(file_path)
      content = File.read(file_path)

      unless content.include?('include RequestLogger')
        # Add include after the class definition
        updated_content = content.sub(
          /class ApplicationController < ActionController::Base\n/,
          "class ApplicationController < ActionController::Base\n  include RequestLogger\n"
        )

        File.write(file_path, updated_content)
        puts "  ✓ Added RequestLogger to ApplicationController"
      else
        puts "  ℹ RequestLogger already included"
      end
    else
      puts "  ⚠ ApplicationController not found"
    end
  end

  def update_application_job
    puts "\n[7/9] Updating ApplicationJob..."

    file_path = 'app/jobs/application_job.rb'

    if File.exist?(file_path)
      content = File.read(file_path)

      unless content.include?('around_perform :log_job_performance')
        job_logging = <<~RUBY

  around_perform :log_job_performance

  private

  def log_job_performance
    start_time = Time.current

    Rails.logger.info({
      type: 'job_started',
      job: self.class.name,
      job_id: job_id,
      queue: queue_name
    }.to_json)

    yield

    duration_ms = ((Time.current - start_time) * 1000).round(2)
    Rails.logger.info({
      type: 'job_completed',
      job: self.class.name,
      job_id: job_id,
      duration_ms: duration_ms,
      status: 'success'
    }.to_json)
  rescue => e
    Rails.logger.error({
      type: 'job_failed',
      job: self.class.name,
      job_id: job_id,
      error: e.class.name,
      message: e.message
    }.to_json)

    raise
  end
        RUBY

        # Add before the last 'end'
        updated_content = content.sub(/end\s*\z/, "#{job_logging}end")
        File.write(file_path, updated_content)
        puts "  ✓ Added job performance logging to ApplicationJob"
      else
        puts "  ℹ Job logging already added"
      end
    else
      puts "  ⚠ ApplicationJob not found"
    end
  end

  def update_production_config
    puts "\n[8/9] Updating production config..."

    file_path = 'config/environments/production.rb'

    if File.exist?(file_path)
      content = File.read(file_path)

      # Add log rotation if not present
      unless content.include?('ActiveSupport::Logger.new')
        log_config = <<~RUBY

  # Log to file with rotation (10 files, 10MB each)
  config.logger = ActiveSupport::Logger.new(
    Rails.root.join('log', "\#{Rails.env}.log"),
    10,           # Keep 10 log files
    10.megabytes  # Each file max 10MB
  )
        RUBY

        updated_content = content.sub(/end\s*\z/, "#{log_config}end")
        File.write(file_path, updated_content)
        puts "  ✓ Added log rotation to production.rb"
      else
        puts "  ℹ Log rotation already configured"
      end
    else
      puts "  ⚠ production.rb not found"
    end
  end

  def add_gemfile_dependencies
    puts "\n[9/9] Checking Gemfile dependencies..."

    gemfile_path = 'Gemfile'

    if File.exist?(gemfile_path)
      content = File.read(gemfile_path)

      gems_to_add = []
      gems_to_add << "gem 'lograge'" unless content.include?("gem 'lograge'")
      gems_to_add << "\n# Error tracking (optional)" unless content.include?("gem 'sentry-ruby'")
      gems_to_add << "gem 'sentry-ruby'" unless content.include?("gem 'sentry-ruby'")
      gems_to_add << "gem 'sentry-rails'" unless content.include?("gem 'sentry-rails'")

      if gems_to_add.any?
        File.open(gemfile_path, 'a') do |f|
          f.puts "\n# Logging & Monitoring"
          gems_to_add.each { |gem| f.puts gem }
        end
        puts "  ✓ Added gems to Gemfile"
        puts "    - lograge" unless content.include?("'lograge'")
        puts "    - sentry-ruby (optional)" unless content.include?("'sentry-ruby'")
        puts "    - sentry-rails (optional)" unless content.include?("'sentry-rails'")
      else
        puts "  ℹ All gems already present"
      end
    else
      puts "  ⚠ Gemfile not found"
    end
  end
end

# Run setup
LoggingSetup.run if __FILE__ == $0
