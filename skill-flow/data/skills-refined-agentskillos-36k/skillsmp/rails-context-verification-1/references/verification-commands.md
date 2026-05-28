# Context Verification Commands

Complete search commands for verifying Rails codebase context.

## Authentication Verification

### Find current_* Helpers

```bash
# Search all authentication helpers
rg "def current_" app/controllers/ app/helpers/

# Common patterns you'll find:
# - current_user (Devise for :users)
# - current_admin (Devise for :admins)
# - current_administrator (Devise for :administrators)
# - current_account (custom multi-tenancy helper)
# - current_organization (custom helper)
```

### Find signed_in? Helpers

```bash
# Check existing usage in views
rg "signed_in\?" app/views/namespace/ --type erb

# Example output:
# app/views/admins/dashboard/_header.html.erb:
#   <% if administrator_signed_in? %>
```

### Find Devise Configuration

```bash
# Check routes.rb for devise_for
rg "devise_for" config/routes.rb

# Example output:
# devise_for :users, path: 'clients'
# devise_for :administrators, path: 'admins'

# This tells you:
# User model → current_user, user_signed_in?
# Administrator model → current_administrator, administrator_signed_in?
```

## Controller Verification

### Find Base Controller Methods

```bash
# Check what's available in base controller
rg "def\s" app/controllers/namespace/base_controller.rb

# Check before_actions
rg "before_action" app/controllers/namespace/base_controller.rb
```

### Find Controller Inheritance

```bash
# Understand controller hierarchy
rg "class.*Controller.*<" app/controllers/namespace/
```

### Find Authorization Methods

```bash
# Search for authorization patterns
rg "authorize\|policy\|can\?\|require_" app/controllers/namespace/
```

## Route Verification

### Find Route Helpers

```bash
# Check existing route helper patterns
rg "_path\|_url" app/views/namespace/ --type erb | head -20

# Run rails routes for specific namespace
rails routes | grep namespace
```

### Common Route Patterns

```bash
# Admin routes typically:
admins_dashboard_path       # Note: admins_ (plural)
destroy_admins_session_path
new_admins_administrator_path

# Client routes typically:
clients_dashboard_path
destroy_clients_session_path
```

## View Helper Verification

```bash
# Search for custom view helpers
rg "def helper_name" app/helpers/

# Check all helpers in namespace
rg "def\s" app/helpers/namespace_helper.rb
```

## Instance Variable Verification

```bash
# Check if variable is set in controller
rg "@variable_name\s*=" app/controllers/namespace/controller_file.rb

# Check all instance variables in controller
rg "@\w+\s*=" app/controllers/namespace/controller_file.rb
```

## Model Method Verification

```bash
# Check model has method
rg "def method_name" app/models/model_name.rb

# Check associations
rg "has_many\|has_one\|belongs_to" app/models/model_name.rb

# Check scopes
rg "scope :" app/models/model_name.rb
```

## Test Infrastructure Verification

```bash
# Check factory exists
rg "factory :model_name" spec/factories/

# Check test helper methods
rg "def helper_name" spec/support/

# Check shared examples
rg "shared_examples" spec/support/
```

## Namespace-Specific Commands

### Admin Namespace

```bash
# Authentication
rg "def current_" app/controllers/admins/ app/controllers/application_controller.rb
rg "administrator_signed_in\?" app/views/admins/

# Routes
rails routes | grep admins

# Base controller
rg "before_action" app/controllers/admins/base_controller.rb
```

### Client Namespace

```bash
# Authentication
rg "def current_" app/controllers/clients/ app/controllers/application_controller.rb
rg "user_signed_in\?" app/views/clients/

# Routes
rails routes | grep clients

# Base controller
rg "before_action" app/controllers/clients/base_controller.rb
```

### API Namespace

```bash
# Authentication (usually token-based)
rg "def current_\|authenticate_with_http_token" app/controllers/api/

# Routes
rails routes | grep api

# Base controller
rg "before_action" app/controllers/api/base_controller.rb
```
