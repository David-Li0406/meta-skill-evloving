#!/usr/bin/env ruby
# Security Audit Script
# Usage: ruby security_audit.rb

class SecurityAudit
  def self.run
    new.run
  end

  def run
    puts "🔒 Security Audit"
    puts "=" * 50

    check_brakeman
    check_bundler_audit
    check_secrets_exposure
    check_credentials_security
    check_security_headers

    puts "\n✅ Security audit complete!"
    puts "\n📋 Recommendations:"
    print_recommendations
  end

  private

  def check_brakeman
    puts "\n[1/5] Running Brakeman security scan..."

    if gem_available?('brakeman')
      system('bundle exec brakeman --no-pager -q')
    else
      puts "  ⚠️  Brakeman not installed"
      puts "  Add to Gemfile: gem 'brakeman', group: :development"
    end
  end

  def check_bundler_audit
    puts "\n[2/5] Checking gem vulnerabilities..."

    if gem_available?('bundler-audit')
      puts "  Updating vulnerability database..."
      system('bundle exec bundler-audit update > /dev/null 2>&1')

      puts "  Checking for vulnerabilities..."
      system('bundle exec bundler-audit check')
    else
      puts "  ⚠️  Bundler-audit not installed"
      puts "  Add to Gemfile: gem 'bundler-audit', group: :development"
    end
  end

  def check_secrets_exposure
    puts "\n[3/5] Checking for exposed secrets..."

    issues = []

    # Check .gitignore
    unless File.exist?('.gitignore')
      issues << ".gitignore file missing"
    else
      gitignore = File.read('.gitignore')

      required_ignores = [
        '/.env',
        '/config/master.key',
        '/config/credentials/*.key'
      ]

      required_ignores.each do |pattern|
        unless gitignore.include?(pattern)
          issues << "#{pattern} not in .gitignore"
        end
      end
    end

    # Check for committed secrets
    secret_patterns = [
      '.env',
      'config/master.key',
      'config/credentials/production.key'
    ]

    secret_patterns.each do |file|
      if File.exist?(file) && !ignored?(file)
        issues << "#{file} exists but may not be ignored by git"
      end
    end

    if issues.any?
      puts "  ⚠️  Potential secret exposure:"
      issues.each { |issue| puts "     - #{issue}" }
    else
      puts "  ✓ No obvious secret exposure"
    end
  end

  def check_credentials_security
    puts "\n[4/5] Checking Rails credentials..."

    if File.exist?('config/credentials.yml.enc')
      puts "  ✓ Encrypted credentials file exists"

      if File.exist?('config/master.key')
        puts "  ✓ Master key exists"

        if ignored?('config/master.key')
          puts "  ✓ Master key is gitignored"
        else
          puts "  ⚠️  WARNING: Master key may not be gitignored!"
        end
      else
        puts "  ⚠️  Master key not found (check RAILS_MASTER_KEY env)"
      end
    else
      puts "  ℹ️  No encrypted credentials (consider using them)"
    end
  end

  def check_security_headers
    puts "\n[5/5] Checking security configuration..."

    issues = []

    # Check production config
    if File.exist?('config/environments/production.rb')
      prod_config = File.read('config/environments/production.rb')

      unless prod_config.include?('force_ssl = true')
        issues << "force_ssl not enabled in production"
      end

      unless prod_config.include?('config.log_level')
        issues << "Log level not explicitly set"
      end
    else
      issues << "Production config not found"
    end

    # Check filter parameters
    if File.exist?('config/initializers/filter_parameter_logging.rb')
      filter_config = File.read('config/initializers/filter_parameter_logging.rb')

      required_filters = ['password', 'token', 'api_key']
      required_filters.each do |filter|
        unless filter_config.include?(filter)
          issues << "#{filter} not in filter_parameters"
        end
      end
    else
      issues << "filter_parameter_logging.rb not configured"
    end

    if issues.any?
      puts "  ⚠️  Configuration issues:"
      issues.each { |issue| puts "     - #{issue}" }
    else
      puts "  ✓ Security configuration looks good"
    end
  end

  def print_recommendations
    recommendations = [
      "Run security audits regularly (weekly)",
      "Keep gems updated: bundle update --conservative",
      "Use strong password requirements (12+ chars)",
      "Enable multi-factor authentication for sensitive operations",
      "Implement rate limiting (rack-attack gem)",
      "Set up security headers (secure_headers gem)",
      "Use HTTPS in production (force_ssl = true)",
      "Regular backup and restore testing",
      "Monitor failed login attempts",
      "Implement proper authorization (Pundit/CanCanCan)"
    ]

    recommendations.each_with_index do |rec, i|
      puts "  #{i + 1}. #{rec}"
    end
  end

  def gem_available?(gem_name)
    Gem::Specification.find_by_name(gem_name)
    true
  rescue Gem::LoadError
    false
  end

  def ignored?(file)
    return false unless File.exist?('.gitignore')

    gitignore = File.read('.gitignore')
    pattern = file.start_with?('/') ? file : "/#{file}"
    gitignore.include?(pattern) || gitignore.include?(file)
  end
end

# Run security audit if executed directly
SecurityAudit.run if __FILE__ == $PROGRAM_NAME
