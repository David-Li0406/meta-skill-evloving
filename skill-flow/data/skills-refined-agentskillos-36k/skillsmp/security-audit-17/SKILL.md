---
name: security-audit
description: Security vulnerability scanning and audit. Use when user needs security check, dependency updates, vulnerability scan, or says "check security", "audit code", "security vulnerabilities", "update gems", "CVE check".
---

# Security Audit

보안 취약점 스캔, 의존성 검사, 환경 변수 관리 등 애플리케이션 보안 감사를 수행합니다.

## Quick Start

```
Task Progress (copy and check off):
- [ ] 1. Run security scan
- [ ] 2. Review vulnerabilities
- [ ] 3. Update dependencies
- [ ] 4. Fix security issues
- [ ] 5. Re-scan to verify
```

## Security Tools

### 1. Brakeman (Static Analysis)

Rails 보안 취약점을 자동으로 감지합니다.

**Installation**:
```ruby
# Gemfile
group :development do
  gem 'brakeman', require: false
end
```

**Usage**:
```bash
# Run security scan
bundle exec brakeman

# Output to file
bundle exec brakeman -o brakeman_report.html

# Quiet mode (only show warnings)
bundle exec brakeman -q

# Check specific files
bundle exec brakeman app/controllers/
```

**Common Vulnerabilities Detected**:
- SQL Injection
- Cross-Site Scripting (XSS)
- Cross-Site Request Forgery (CSRF)
- Mass Assignment
- Command Injection
- Unsafe Redirects

### 2. Bundler Audit (Dependency Vulnerabilities)

Gem 의존성의 알려진 취약점을 검사합니다.

**Installation**:
```ruby
# Gemfile
group :development do
  gem 'bundler-audit', require: false
end
```

**Usage**:
```bash
# Update vulnerability database
bundle exec bundler-audit update

# Check for vulnerabilities
bundle exec bundler-audit check

# Auto-update vulnerable gems (use with caution)
bundle exec bundler-audit check --update
```

**Fix Vulnerabilities**:
```bash
# Update specific gem
bundle update gem_name

# Update all gems (risky)
bundle update
```

### 3. Rails Security Checklist

**Authentication & Authorization**:
```ruby
# ✅ Use has_secure_password
class User < ApplicationRecord
  has_secure_password
  validates :password, length: { minimum: 8 }
end

# ✅ Use before_action for authorization
class PostsController < ApplicationController
  before_action :require_login
  before_action :authorize_user, only: [:edit, :update, :destroy]

  private

  def authorize_user
    @post = Post.find(params[:id])
    redirect_to root_path unless @post.user == current_user
  end
end
```

**SQL Injection Prevention**:
```ruby
# ❌ Vulnerable to SQL injection
User.where("email = '#{params[:email]}'")

# ✅ Use parameterized queries
User.where("email = ?", params[:email])
User.where(email: params[:email])
```

**XSS Prevention**:
```erb
<%# ❌ Vulnerable to XSS %>
<%= raw @post.content %>
<%= @post.content.html_safe %>

<%# ✅ Safe (auto-escaped) %>
<%= @post.content %>

<%# ✅ If HTML is needed, sanitize %>
<%= sanitize @post.content, tags: %w[p br strong em] %>
```

**CSRF Protection**:
```ruby
# ApplicationController (enabled by default)
class ApplicationController < ActionController::Base
  protect_from_forgery with: :exception
end

# For API controllers, use null_session
class Api::V1::BaseController < ApplicationController
  protect_from_forgery with: :null_session
end
```

**Mass Assignment Protection**:
```ruby
# ✅ Use strong parameters
class UsersController < ApplicationController
  def create
    @user = User.new(user_params)
    # ...
  end

  private

  def user_params
    params.require(:user).permit(:email, :name, :password)
    # Never permit :admin, :role without authorization check
  end
end
```

### 4. Environment Variables Security

**Never commit secrets**:
```ruby
# ❌ Never do this
class ApiClient
  API_KEY = "sk_live_123456789"  # Hard-coded secret!
end

# ✅ Use environment variables
class ApiClient
  API_KEY = ENV['API_KEY']
end
```

**Use Rails credentials** (Rails 5.2+):
```bash
# Edit credentials
EDITOR=nano rails credentials:edit

# Access in code
Rails.application.credentials.api_key
Rails.application.credentials.dig(:aws, :access_key_id)
```

**Check for exposed secrets**:
```bash
# .gitignore should include:
/.env
/config/master.key
/config/credentials/*.key
```

### 5. Session Security

**Secure session configuration**:
```ruby
# config/initializers/session_store.rb
Rails.application.config.session_store :cookie_store,
  key: '_app_session',
  secure: Rails.env.production?,  # HTTPS only in production
  httponly: true,                 # Not accessible via JavaScript
  same_site: :lax                 # CSRF protection
```

**Session timeout**:
```ruby
# app/controllers/application_controller.rb
before_action :check_session_timeout

private

def check_session_timeout
  if session[:last_seen_at] && session[:last_seen_at] < 30.minutes.ago
    reset_session
    redirect_to login_path, alert: "Session expired"
  end
  session[:last_seen_at] = Time.current
end
```

### 6. File Upload Security

**Validate file types**:
```ruby
class User < ApplicationRecord
  has_one_attached :avatar

  validate :acceptable_avatar

  private

  def acceptable_avatar
    return unless avatar.attached?

    unless avatar.content_type.in?(%w[image/jpeg image/png image/gif])
      errors.add(:avatar, "must be a JPEG, PNG, or GIF")
    end

    if avatar.byte_size > 5.megabytes
      errors.add(:avatar, "is too large (max 5MB)")
    end
  end
end
```

**Secure file storage**:
```ruby
# config/storage.yml
production:
  service: S3
  access_key_id: <%= Rails.application.credentials.dig(:aws, :access_key_id) %>
  secret_access_key: <%= Rails.application.credentials.dig(:aws, :secret_access_key) %>
  region: us-east-1
  bucket: your-bucket-name
  public: false  # Important: Files not publicly accessible
```

### 7. Rate Limiting

**Using Rack Attack** (recommended):
```ruby
# Gemfile
gem 'rack-attack'

# config/initializers/rack_attack.rb
Rack::Attack.throttle("requests by ip", limit: 300, period: 5.minutes) do |req|
  req.ip
end

Rack::Attack.throttle("logins/ip", limit: 5, period: 20.seconds) do |req|
  req.ip if req.path == '/login' && req.post?
end

# Block bad actors
Rack::Attack.blocklist("block bad IPs") do |req|
  # Check against your blocklist
  Redis.current.sismember("blocked_ips", req.ip)
end
```

### 8. Database Security

**Use database-level constraints**:
```ruby
# Migration
def change
  add_index :users, :email, unique: true  # Prevent duplicates
  add_foreign_key :posts, :users         # Referential integrity

  # NOT NULL constraints
  change_column_null :users, :email, false
end
```

**Encrypted attributes** (for sensitive data):
```ruby
# Gemfile
gem 'attr_encrypted'

# Model
class User < ApplicationRecord
  attr_encrypted :ssn,
    key: Rails.application.credentials.encryption_key,
    algorithm: 'aes-256-gcm'
end
```

### 9. Headers Security

**Security headers** (use gem):
```ruby
# Gemfile
gem 'secure_headers'

# config/initializers/secure_headers.rb
SecureHeaders::Configuration.default do |config|
  config.x_frame_options = "DENY"
  config.x_content_type_options = "nosniff"
  config.x_xss_protection = "1; mode=block"
  config.referrer_policy = "strict-origin-when-cross-origin"

  config.csp = {
    default_src: %w['self'],
    script_src: %w['self' 'unsafe-inline'],
    style_src: %w['self' 'unsafe-inline'],
    img_src: %w['self' data: https:],
    font_src: %w['self' data:]
  }
end
```

### 10. Logging & Monitoring

**Never log sensitive data**:
```ruby
# config/initializers/filter_parameter_logging.rb
Rails.application.config.filter_parameters += [
  :password,
  :password_confirmation,
  :credit_card,
  :ssn,
  :api_key,
  :token
]
```

**Monitor failed login attempts**:
```ruby
# app/controllers/sessions_controller.rb
def create
  user = User.find_by(email: params[:email])

  if user&.authenticate(params[:password])
    session[:user_id] = user.id
    redirect_to root_path
  else
    # Log failed attempt
    Rails.logger.warn "Failed login attempt for #{params[:email]} from #{request.remote_ip}"
    flash.now[:alert] = "Invalid credentials"
    render :new
  end
end
```

## Automation Script

### Security Audit Runner

```bash
# Run via: ruby .claude/skills/security-audit/scripts/security_audit.rb
```

The script runs:
1. Brakeman security scan
2. Bundler-audit dependency check
3. Environment variables check
4. Credentials security check
5. Security headers verification

## Common Vulnerabilities & Fixes

### 1. Weak Passwords

**Problem**: Short or simple passwords

**Fix**:
```ruby
class User < ApplicationRecord
  has_secure_password

  validates :password,
    length: { minimum: 12 },
    format: {
      with: /\A(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/,
      message: "must include uppercase, lowercase, and number"
    },
    if: :password_digest_changed?
end
```

### 2. Insecure Direct Object Reference (IDOR)

**Problem**: Users can access other users' data

**Fix**:
```ruby
# ❌ Vulnerable
def show
  @post = Post.find(params[:id])  # Any post!
end

# ✅ Scope to current user
def show
  @post = current_user.posts.find(params[:id])
end
```

### 3. Missing Authorization

**Problem**: No permission checks

**Fix**:
```ruby
# Use Pundit or CanCanCan
class PostPolicy < ApplicationPolicy
  def update?
    user == record.user || user.admin?
  end
end

# In controller
authorize @post
```

### 4. Timing Attack on Authentication

**Problem**: Different response times leak information

**Fix**:
```ruby
# Use secure_compare for password/token comparison
def valid_token?(provided_token)
  ActiveSupport::SecurityUtils.secure_compare(
    provided_token,
    expected_token
  )
end
```

## Security Best Practices

1. **Keep Rails and gems updated**
   ```bash
   bundle update --conservative rails
   ```

2. **Run security audits regularly**
   ```bash
   bundle exec brakeman
   bundle exec bundler-audit check
   ```

3. **Use HTTPS in production** (force SSL)
   ```ruby
   # config/environments/production.rb
   config.force_ssl = true
   ```

4. **Implement proper authentication**
   - Use Devise or has_secure_password
   - Multi-factor authentication for sensitive operations
   - Password strength requirements

5. **Authorization on every action**
   - Never trust user input
   - Always scope queries to current user
   - Use authorization gems (Pundit, CanCanCan)

6. **Secure file uploads**
   - Validate file types and sizes
   - Scan for malware (ClamAV)
   - Store in secure location (S3 private buckets)

7. **API Security**
   - Use authentication tokens
   - Rate limiting
   - CORS configuration
   - API versioning

8. **Regular backups**
   - Automated database backups
   - Encrypted backup storage
   - Tested restore procedures

## CI/CD Integration

Add security checks to your CI pipeline:

```yaml
# .github/workflows/security.yml
name: Security Audit

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: ruby/setup-ruby@v1
        with:
          bundler-cache: true
      - name: Run Brakeman
        run: bundle exec brakeman --no-pager
      - name: Run Bundler Audit
        run: |
          bundle exec bundler-audit update
          bundle exec bundler-audit check
```

## Checklist

- [ ] Brakeman scan passed
- [ ] No vulnerable dependencies (bundler-audit)
- [ ] Secrets not in version control
- [ ] Strong parameters used everywhere
- [ ] SQL injection protected (parameterized queries)
- [ ] XSS protected (proper escaping)
- [ ] CSRF protection enabled
- [ ] Proper authorization on all actions
- [ ] File uploads validated
- [ ] Rate limiting configured
- [ ] Security headers set
- [ ] HTTPS enforced in production
- [ ] Sensitive data filtered from logs
- [ ] Regular security audits scheduled
