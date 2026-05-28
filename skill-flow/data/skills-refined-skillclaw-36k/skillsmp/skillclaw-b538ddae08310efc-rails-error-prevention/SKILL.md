---
name: rails-error-prevention
description: Use this skill before writing any Rails code to prevent common errors related to ViewComponents, ActiveRecord queries, and method exposure issues.
---

# Rails Error Prevention Skill

This skill provides preventative checklists and error patterns for common Rails mistakes. **Review relevant sections BEFORE writing code.**

## When to Use This Skill

- Before creating ViewComponents
- Before writing ActiveRecord queries with GROUP BY or joins
- Before writing view code that calls component methods
- Before creating controller actions
- When debugging undefined method errors
- When debugging template not found errors
- When debugging ActiveRecord grouping errors

## Critical Rule: Method Exposure Verification

**This is the #1 cause of runtime errors in Rails applications.**

```
WRONG ASSUMPTION: Service has method → View can call it through component
CORRECT RULE:     Service has method + Component exposes it = View can call it
```

### Verification Process

```bash
# Step 1: List all methods view will call on component
grep -oE '@[a-z_]+\.[a-z_]+' app/views/{path}/*.erb | sort -u

# Step 2: List all public methods in component
grep -E '^\s+def [a-z_]+' app/components/{component}_component.rb

# Step 3: Compare - any view call without component method = BUG
# Missing methods MUST be added to component BEFORE writing view code
```

### Patterns to Fix Missing Methods

```ruby
# Pattern 1: Delegation
class Metrics::DashboardComponent < ViewComponent::Base
  delegate :calculate_lifetime_tasks,
           :calculate_lifetime_success_rate,
           to: :@service
  
  def initialize(service:)
    @service = service
  end
end

# Pattern 2: Wrapper methods (preferred for transformation)
class Metrics::DashboardComponent < ViewComponent::Base
  def initialize(service:)
    @service = service
  end
  
  def lifetime_tasks
    @service.calculate_lifetime_tasks
  end
  
  def lifetime_success_rate
    @service.calculate_lifetime_success_rate
  end
end

# Pattern 3: Expose service directly (use sparingly)
class Metrics::DashboardComponent < ViewComponent::Base
  attr_reader :service
  
  def initialize(service:)
    @service = service
  end
end
```