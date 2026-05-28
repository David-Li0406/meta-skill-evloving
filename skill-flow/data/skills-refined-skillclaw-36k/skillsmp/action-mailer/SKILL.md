---
name: action-mailer
description: This skill should be used when the user asks about "email", "mailers", "Action Mailer", "deliver_now", "deliver_later", "email templates", "attachments", "mail previews", "SMTP", "email configuration", "interceptors", or needs guidance on sending emails in Rails applications.
version: 1.0.0
---

# Action Mailer

Comprehensive guide to sending emails in Rails applications.

## Creating Mailers

```bash
rails generate mailer User welcome reset_password
```

```ruby
# app/mailers/application_mailer.rb
class ApplicationMailer < ActionMailer::Base
  default from: "noreply@example.com"
  layout "mailer"
end

# app/mailers/user_mailer.rb
class UserMailer < ApplicationMailer
  def welcome(user)
    @user = user
    @login_url = login_url

    mail(
      to: @user.email,
      subject: "Welcome to Our App!"
    )
  end

  def reset_password(user)
    @user = user
    @reset_url = edit_password_url(token: @user.reset_token)

    mail(to: @user.email, subject: "Reset Your Password")
  end
end
```

## Mail Options

```ruby
mail(
  to: "user@example.com",           # Single recipient
  to: ["a@ex.com", "b@ex.com"],     # Multiple recipients
  from: "sender@example.com",
  cc: "manager@example.com",
  bcc: "archive@example.com",
  reply_to: "support@example.com",
  subject: "Email Subject",
  content_type: "text/html",        # Default is multipart
  importance: "high",
  delivery_method_options: { ... }
)
```

### Default Values

```ruby
class ApplicationMailer < ActionMailer::Base
  default from: "noreply@example.com",
          reply_to: "support@example.com"
end

class UserMailer < ApplicationMailer
  default from: "users@example.com"  # Override for this mailer
end
```

### Using Params

```ruby
# Passing params
UserMailer.with(user: @user, account: @account).welcome.deliver_later

# Accessing params
class UserMailer < ApplicationMailer
  def welcome
    @user = params[:user]
    @account = params[:account]
    mail(to: @user.email)
  end
end
```

## Email Templates

### Directory Structure

```
app/views/user_mailer/
├── welcome.html.erb      # HTML version
├── welcome.text.erb      # Plain text version
└── reset_password.html.erb
```

### HTML Template

```erb
<%# app/views/user_mailer/welcome.html.erb %>
<h1>Welcome, <%= @user.name %>!</h1>

<p>Thanks for signing up. Get started by visiting your dashboard:</p>

<p><%= link_to "Go to Dashboard", dashboard_url %></p>

<p>
  Best regards,<br>
  The Team
</p>
```

### Plain Text Template

```erb
<%# app/views/user_mailer/welcome.text.erb %>
Welcome, <%= @user.name %>!

Thanks for signing up. Get started by visiting your dashboard:
<%= dashboard_url %>

Best regards,
The Team
```

### Layouts

```erb
<%# app/views/layouts/mailer.html.erb %>
<!DOCTYPE html>
<html>
  <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type" />
    <style>
      body { font-family: Arial, sans-serif; }
      .header { background: #3498db; color: white; padding: 20px; }
      .content { padding: 20px; }
      .footer { color: #666; font-size: 12px; padding: 20px; }
    </style>
  </head>
  <body>
    <div class="header">
      <%= image_tag attachments['logo.png'].url if attachments['logo.png'] %>
    </div>
    <div class="content">
      <%= yield %>
    </div>
    <div class="footer">
      <p>&copy; <%= Date.current.year %> Our Company</p>
      <p><%= link_to "Unsubscribe", unsubscribe_url %></p>
    </div>
  </body>
</html>
```

## Attachments

### File Attachments

```ruby
class ReportMailer < ApplicationMailer
  def monthly_report(user, report)
    @user = user

    # From file
    attachments["report.pdf"] = File.read(report.path)

    # With options
    attachments["data.csv"] = {
      mime_type: "text/csv",
      content: generate_csv(report)
    }

    mail(to: @user.email, subject: "Monthly Report")
  end
end
```

### Inline Attachments

```ruby
def welcome(user)
  @user = user
  attachments.inline["logo.png"] = File.read("app/assets/images/logo.png")
  mail(to: @user.email)
end
```

```erb
<%# In template %>
<%= image_tag attachments['logo.png'].url %>
```

## Sending Emails

### Asynchronous (Recommended)

```ruby
# Queue for background delivery
UserMailer.welcome(@user).deliver_later

# With delay
UserMailer.welcome(@user).deliver_later(wait: 1.hour)
UserMailer.welcome(@user).deliver_later(wait_until: Date.tomorrow.noon)

# With options
UserMailer.welcome(@user).deliver_later(queue: :mailers, priority: 10)
```

### Synchronous

```ruby
# Send immediately (blocks)
UserMailer.welcome(@user).deliver_now

# Useful in background jobs
class WelcomeJob < ApplicationJob
  def perform(user)
    UserMailer.welcome(user).deliver_now
  end
end
```

## Email Previews

```ruby
# test/mailers/previews/user_mailer_preview.rb
class UserMailerPreview < ActionMailer::Preview
  def welcome
    user = User.first || User.new(name: "Test User", email: "test@example.com")
    UserMailer.welcome(user)
  end

  def reset_password
    user = User.first
    UserMailer.reset_password(user)
  end
end
```

Access at: `http://localhost:3000/rails/mailers/user_mailer/welcome`

## Configuration

### Development

```ruby
# config/environments/development.rb
config.action_mailer.delivery_method = :letter_opener  # View in browser
# or
config.action_mailer.delivery_method = :test  # Store in ActionMailer::Base.deliveries

config.action_mailer.default_url_options = { host: "localhost", port: 3000 }
config.action_mailer.raise_delivery_errors = true
config.action_mailer.perform_caching = false
```

### Production (SMTP)

```ruby
# config/environments/production.rb
config.action_mailer.delivery_method = :smtp
config.action_mailer.default_url_options = { host: "example.com" }

config.action_mailer.smtp_settings = {
  address: "smtp.example.com",
  port: 587,
  domain: "example.com",
  user_name: Rails.application.credentials.smtp[:user],
  password: Rails.application.credentials.smtp[:password],
  authentication: "plain",
  enable_starttls_auto: true
}
```

### Common Providers

```ruby
# SendGrid
config.action_mailer.smtp_settings = {
  address: "smtp.sendgrid.net",
  port: 587,
  authentication: :plain,
  user_name: "apikey",
  password: ENV["SENDGRID_API_KEY"],
  domain: "example.com",
  enable_starttls_auto: true
}

# Mailgun
config.action_mailer.smtp_settings = {
  address: "smtp.mailgun.org",
  port: 587,
  user_name: ENV["MAILGUN_SMTP_LOGIN"],
  password: ENV["MAILGUN_SMTP_PASSWORD"],
  authentication: :plain,
  enable_starttls_auto: true
}
```

## Interceptors and Observers

### Interceptor (Modify Before Sending)

```ruby
# app/mailers/sandbox_email_interceptor.rb
class SandboxEmailInterceptor
  def self.delivering_email(message)
    message.to = ["sandbox@example.com"]
    message.subject = "[SANDBOX] #{message.subject}"
  end
end

# config/initializers/mail_interceptors.rb
if Rails.env.staging?
  ActionMailer::Base.register_interceptor(SandboxEmailInterceptor)
end
```

### Observer (Log After Sending)

```ruby
# app/mailers/email_delivery_observer.rb
class EmailDeliveryObserver
  def self.delivered_email(message)
    EmailLog.create!(
      to: message.to.join(", "),
      subject: message.subject,
      sent_at: Time.current
    )
  end
end

# config/initializers/mail_observers.rb
ActionMailer::Base.register_observer(EmailDeliveryObserver)
```

## Testing

### Minitest

```ruby
require "test_helper"

class UserMailerTest < ActionMailer::TestCase
  test "welcome email" do
    user = users(:one)
    email = UserMailer.welcome(user)

    assert_emails 1 do
      email.deliver_now
    end

    assert_equal ["noreply@example.com"], email.from
    assert_equal [user.email], email.to
    assert_equal "Welcome to Our App!", email.subject
    assert_match user.name, email.body.encoded
  end

  test "welcome email is enqueued" do
    user = users(:one)

    assert_enqueued_emails 1 do
      UserMailer.welcome(user).deliver_later
    end
  end
end
```
