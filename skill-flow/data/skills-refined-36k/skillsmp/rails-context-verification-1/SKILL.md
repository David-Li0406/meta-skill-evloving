---
name: Rails Context Verification
description: "Systematic verification of codebase context before code generation to prevent assumption bugs. Use when: (1) Working in unfamiliar namespace, (2) Using authentication helpers, (3) Copying patterns across namespaces, (4) Before any code generation. Trigger keywords: context, assumptions, helpers, authentication, current_user, verify, validate context"
version: 1.2.0
category: implementation
---

# Rails Context Verification

Prevent "assumption bugs" by verifying codebase context before generating code.

## Context Verification Decision Tree

```
What are you generating?
│
├─ View with authentication
│   └─ Verify: rg "def current_" app/controllers/
│
├─ Controller with auth check
│   └─ Verify: rg "devise_for" config/routes.rb
│
├─ Route helpers (link_to, redirect_to)
│   └─ Verify: rails routes | grep namespace
│
├─ Instance variables in view
│   └─ Verify: rg "@variable\s*=" controller_file
│
├─ Custom helper method
│   └─ Verify: rg "def helper_name" app/helpers/
│
└─ Copying pattern from other namespace
    └─ STOP! Search target namespace for actual patterns
```

---

## NEVER Do This

**NEVER** assume authentication helper names:
```ruby
# WRONG - Assuming current_admin exists
<%= current_admin.email %>

# RIGHT - Verify first: rg "def current_" app/controllers/
# Found: current_administrator
<%= current_administrator.email %>
```

**NEVER** assume Devise scope matches model name:
```ruby
# WRONG - Model is Administrator, assuming admin scope
before_action :authenticate_admin!

# RIGHT - Check routes.rb: devise_for :administrators
before_action :authenticate_administrator!
```

**NEVER** assume route prefixes:
```erb
<%# WRONG - Assuming singular prefix %>
<%= link_to "Dashboard", admin_dashboard_path %>

<%# RIGHT - Verify: rails routes | grep admin → shows admins_ (plural) %>
<%= link_to "Dashboard", admins_dashboard_path %>
```

**NEVER** copy patterns across namespaces without verification:
```ruby
# WRONG - Copying client pattern to admin
# Client uses: before_action :set_account
# Admin controller:
before_action :set_account  # FAILS - admins don't have accounts!

# RIGHT - Verify what admin actually has
# rg "before_action" app/controllers/admins/base_controller.rb
before_action :authenticate_administrator!
```

**NEVER** use instance variables without verifying they're set:
```erb
<%# WRONG - Using @current_account without verification %>
<%= @current_account.name %>  # NIL ERROR if not set!

<%# RIGHT - Check controller first %>
<%# rg "@current_account\s*=" controller_file %>
<%# Not found? Don't use it. %>
```

---

## Core Verification Protocol

### Before ANY Code Generation

1. **Identify Namespace:** Admin? Client? API? Public?
2. **Search for Patterns:** Don't invent - discover
3. **Use Verified Names:** Only what search confirms exists
4. **Document Context:** Record verified helpers for team

### Quick Verification Commands

| What | Command |
|------|---------|
| Authentication helper | `rg "def current_" app/controllers/` |
| Signed-in? helper | `rg "signed_in\?" app/views/namespace/` |
| Devise scope | `rg "devise_for" config/routes.rb` |
| Route helpers | `rails routes \| grep namespace` |
| View helpers | `rg "def helper_name" app/helpers/` |
| Instance variables | `rg "@variable\s*=" controller_file` |
| Before actions | `rg "before_action" base_controller.rb` |
| Model methods | `rg "def method_name" app/models/` |
| Factories | `rg "factory :name" spec/factories/` |

---

## Verification Checklist

### For Views
- [ ] Authentication helper verified (`current_*`)
- [ ] Signed-in helper verified (`*_signed_in?`)
- [ ] Instance variables set in controller
- [ ] View helpers exist
- [ ] Route helpers correct

### For Controllers
- [ ] Authentication method verified (`authenticate_*!`)
- [ ] Authorization pattern discovered
- [ ] Before actions exist in base controller
- [ ] Service objects exist before calling

### For Tests
- [ ] Factory exists for model
- [ ] Shared examples exist if used
- [ ] Test helpers verified

---

## Namespace-Specific Patterns

| Namespace | Authentication | Route Prefix | Base Controller |
|-----------|---------------|--------------|-----------------|
| Admin | `current_administrator`, `administrator_signed_in?` | `admins_` | `Admins::BaseController` |
| Client | `current_user`, `user_signed_in?` | `clients_` | `Clients::BaseController` |
| API | Token-based | `api_v1_` | `Api::BaseController` |
| Public | None or optional | Default | `ApplicationController` |

**Warning:** These are examples. Your codebase may differ. Always verify!

---

## Context Documentation Format

When delegating to specialists, include verified context:

```markdown
**Verified Context:**
- Namespace: admin
- Auth helper: `current_administrator` (verified: app/controllers/application_controller.rb:42)
- Route prefix: `admins_` (verified: rails routes)
- Authorization: `require_super_admin` (verified: base_controller.rb:8)

CRITICAL: Use ONLY these verified helpers. Do not assume others exist.
```

---

## Remember

1. **Never assume** - always verify helper names, routes, methods
2. **Search first** - discover patterns before applying them
3. **Namespace matters** - admin ≠ client ≠ api (different patterns)
4. **Devise scope matters** - :users ≠ :admins ≠ :administrators
5. **2 minutes to verify** saves hours of debugging

---

## References

Detailed examples and commands in `references/`:
- `verification-commands.md` - Complete search command reference
- `pattern-discovery-examples.md` - Real-world verification workflows
- `workflow-integration.md` - Implementation workflow integration, beads tracking
