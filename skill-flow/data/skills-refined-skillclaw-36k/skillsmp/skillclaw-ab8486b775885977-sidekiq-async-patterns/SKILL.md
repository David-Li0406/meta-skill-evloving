---
name: sidekiq-async-patterns
description: Use this skill when you need to implement background job processing with Sidekiq in Ruby on Rails, including creating jobs, configuring queues, and handling errors.
---

# Sidekiq & Async Patterns Skill

This skill provides comprehensive guidance for implementing background jobs with Sidekiq in Rails applications.

## When to Use This Skill

- Creating new background jobs
- Configuring Sidekiq queues
- Implementing retry strategies
- Designing idempotent operations
- Setting up scheduled jobs
- Handling job failures
- Optimizing async processing

## External Documentation

**Official Wiki**: [Sidekiq Wiki](https://github.com/sidekiq/sidekiq/wiki)

```bash
# Always check the official wiki for latest patterns
# Key wiki pages:
# - Best Practices: https://github.com/sidekiq/sidekiq/wiki/Best-Practices
# - Error Handling: https://github.com/sidekiq/sidekiq/wiki/Error-Handling
# - Scheduled Jobs: https://github.com/sidekiq/sidekiq/wiki/Scheduled-Jobs
```

## Pre-Work Inspection

```bash
# Check existing jobs
ls app/jobs/ app/sidekiq/ app/workers/ 2>/dev/null

# Check job naming conventions
head -30 $(find app/jobs -name '*.rb' | head -1) 2>/dev/null

# Check Sidekiq configuration
cat config/sidekiq.yml 2>/dev/null
cat config/initializers/sidekiq.rb 2>/dev/null

# Check queue configuration
grep -r 'queue_as\|sidekiq_options' app/jobs/ --include='*.rb' | head -10

# Check scheduled jobs
cat config/schedule.yml 2>/dev/null
cat config/recurring.yml 2>/dev/null
```

## Core Principles

### 1. Idempotency (CRITICAL)

**Jobs MUST be idempotent** - running the same job multiple times produces the same result.

```ruby
# WRONG - Not idempotent (sends duplicate emails)
class SendWelcomeEmailJob < ApplicationJob
  def perform(user_id)
    user = User.find(user_id)
    UserMailer.welcome(user).deliver_now
  end
end

# CORRECT - Idempotent (checks before sending)
class SendWelcomeEmailJob < ApplicationJob
  def perform(user_id)
    user = User.find(user_id)
    return if user.welcome_email_sent_at.present?
    
    UserMailer.welcome(user).deliver_now
    user.update!(welcome_email_sent_at: Time.current)
  end
end
```

### 2. Small Payloads

**Pass IDs, not objects** - objects serialize and can become stale.

```ruby
# WRONG - Object serialization
NotificationJob.perform_later(@user)  # Serialization can lead to stale data
```