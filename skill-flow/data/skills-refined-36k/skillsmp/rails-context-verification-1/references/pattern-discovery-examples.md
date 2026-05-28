# Pattern Discovery Examples

Real-world verification workflows.

## Example 1: Adding User Dropdown to Admin Header

**Task:** Add admin user dropdown with logout link

### Wrong Approach (Assumption)

```erb
<%# Assume current_admin and destroy_admin_session_path %>
<% if admin_signed_in? %>
  <%= current_admin.email %>
  <%= link_to "Logout", destroy_admin_session_path %>
<% end %>
```

### Correct Approach (Verification)

```bash
# Step 1: Verify authentication helper
$ rg "def current_" app/controllers/
# Found: def current_administrator

# Step 2: Verify signed_in? helper
$ rg "signed_in\?" app/views/admins/
# Found: administrator_signed_in?

# Step 3: Verify logout route
$ rails routes | grep destroy.*session | grep admin
# Found: destroy_admins_session_path

# Step 4: Use verified helpers
```

```erb
<% if administrator_signed_in? %>
  <%= current_administrator.email %>
  <%= link_to "Logout", destroy_admins_session_path, method: :delete %>
<% end %>
```

---

## Example 2: Adding Authorization Check

**Task:** Restrict action to super admins

### Wrong Approach (Assumption)

```ruby
# Assume authorize method exists
before_action :authorize_admin!
```

### Correct Approach (Verification)

```bash
# Step 1: Check existing authorization patterns
$ rg "before_action.*authorize\|admin\|permission" app/controllers/admins/
# Found: before_action :require_super_admin

# Step 2: Verify method exists
$ rg "def require_super_admin" app/controllers/
# Found in: app/controllers/admins/base_controller.rb

# Step 3: Use verified pattern
```

```ruby
before_action :require_super_admin
```

---

## Example 3: Adding Account-Scoped Query

**Task:** Show records for current account

### Wrong Approach (Assumption)

```ruby
# Assume current_account exists
@records = current_account.records
```

### Correct Approach (Verification)

```bash
# Step 1: Check if multi-tenancy is used
$ rg "current_account" app/controllers/clients/

# Step 2: Check how it's set
$ rg "def current_account\|@current_account\s*=" app/controllers/

# Step 3: If found, verify it's available in this controller
# Step 4: If not found, check what scoping is used
```

```ruby
# If current_account exists:
@records = current_account.records

# If not, check for other patterns:
@records = current_user.records  # Or:
@records = Record.all  # If no scoping
```

---

## Common Bug: Undefined Authentication Helper

**Assumption:**
```erb
<%# Agent assumes current_admin exists %>
<%= current_admin.email %>
```

**Prevention:**
```bash
# Verify first
$ rg "def current_" app/controllers/

# Find actual helper name, then use it
<%= current_administrator.email %>
```

---

## Common Bug: Wrong Devise Scope Name

**Assumption:**
```ruby
# Agent assumes admin_signed_in? exists
before_action :authenticate_admin!
```

**Prevention:**
```bash
# Check routes.rb for devise_for declaration
$ rg "devise_for" config/routes.rb

# Output: devise_for :administrators
# Correct helper: authenticate_administrator!
```

---

## Common Bug: Namespace Route Mismatch

**Assumption:**
```erb
<%# Agent assumes admin_users_path exists %>
<%= link_to "Users", admin_users_path %>
```

**Prevention:**
```bash
# Check existing route helper patterns
$ rg "_path" app/views/admins/ --type erb | head -5

# Output: admins_users_path (note the 's' in admins)
# Correct: admins_users_path
```

---

## Common Bug: Cross-Namespace Pattern Copying

**Assumption:**
```ruby
# Agent copies client pattern to admin without verification
# In app/controllers/clients/dashboard_controller.rb:
before_action :set_account

# In app/controllers/admins/dashboard_controller.rb:
before_action :set_account  # BREAKS - admin doesn't have accounts!
```

**Prevention:**
```bash
# Check what before_actions exist in target namespace
$ rg "before_action" app/controllers/admins/base_controller.rb

# Output shows actual available callbacks
# Use only verified callbacks, don't copy blindly
```
