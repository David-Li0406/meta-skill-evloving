---
name: managing-localisation
description: Create and manage Laravel translation files using PHP arrays for internationalization. Use when creating translation files, adding translations, managing i18n, or when user mentions translation files, localization, i18n, or language files.
---

# Manage Laravel Localisation Files

Create and manage Laravel translation files using PHP arrays for internationalization. Translation files are organized by locale and category, accessed via the `__()` helper or `@lang` Blade directive throughout the application.

## File Structure

Translation files are stored in the lang directory:

```
lang/{locale}/{file}.php
```

**Examples:**

- `lang/en_GB/common.php`
- `lang/en_GB/validation.php`
- `lang/en_GB/auth.php`
- `lang/es_ES/common.php`

## Core Conventions

### 1. Translation File Structure

```php
<?php

declare(strict_types=1);

return [
    'key' => 'Translation string',
    'key_with_params' => 'Hello :name',
    'nested' => [
        'key' => 'Nested translation',
    ],
];
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Return array directly (no variables)
- Use snake_case for keys
- Support parameter placeholders with `:param`
- Use nested arrays for organization
- Keep translations in same file structure across locales

### 2. Parameter Placeholders

```php
return [
    'welcome' => 'Welcome :name!',
    'items_count' => 'You have :count items',
    'user_greeting' => 'Hello :name, you have :count messages',
];
```

### 3. Pluralization

```php
return [
    'apples' => '{0} No apples|{1} One apple|[2,*] :count apples',
    'messages' => '{0} No messages|{1} One message|[2,*] :count messages',
];
```

## Examples

### Example 1: Common Translations

```php
<?php

declare(strict_types=1);

return [
    'copyright_notice' => 'Copyright © :year Moon Pixels Ltd. All rights reserved.',
    'welcome' => 'Welcome to :app',
    'loading' => 'Loading...',
    'save' => 'Save',
    'cancel' => 'Cancel',
    'delete' => 'Delete',
    'edit' => 'Edit',
    'create' => 'Create',
    'update' => 'Update',
    'confirm' => 'Are you sure?',
];
```

### Example 2: Validation Translations

```php
<?php

declare(strict_types=1);

return [
    'required' => 'The :attribute field is required.',
    'email' => 'The :attribute must be a valid email address.',
    'max' => [
        'string' => 'The :attribute must not be greater than :max characters.',
        'numeric' => 'The :attribute must not be greater than :max.',
    ],
    'min' => [
        'string' => 'The :attribute must be at least :min characters.',
        'numeric' => 'The :attribute must be at least :min.',
    ],
    'unique' => 'The :attribute has already been taken.',
    'confirmed' => 'The :attribute confirmation does not match.',

    'attributes' => [
        'email' => 'email address',
        'password' => 'password',
        'name' => 'name',
    ],
];
```

### Example 3: Authentication Translations

```php
<?php

declare(strict_types=1);

return [
    'failed' => 'These credentials do not match our records.',
    'password' => 'The provided password is incorrect.',
    'throttle' => 'Too many login attempts. Please try again in :seconds seconds.',

    'login' => [
        'title' => 'Log in to your account',
        'email' => 'Email address',
        'password' => 'Password',
        'remember' => 'Remember me',
        'forgot' => 'Forgot your password?',
        'submit' => 'Log in',
    ],

    'register' => [
        'title' => 'Create an account',
        'name' => 'Full name',
        'email' => 'Email address',
        'password' => 'Password',
        'password_confirmation' => 'Confirm password',
        'submit' => 'Register',
    ],
];
```

### Example 4: Pagination Translations

```php
<?php

declare(strict_types=1);

return [
    'previous' => '&laquo; Previous',
    'next' => 'Next &raquo;',
    'showing' => 'Showing :from to :to of :total results',
    'per_page' => 'Per page',
];
```

### Example 5: Model-Specific Translations

```php
<?php

declare(strict_types=1);

return [
    'user' => [
        'created' => 'User created successfully.',
        'updated' => 'User updated successfully.',
        'deleted' => 'User deleted successfully.',
        'not_found' => 'User not found.',
        'profile' => 'User Profile',
        'settings' => 'User Settings',
    ],

    'order' => [
        'created' => 'Order placed successfully.',
        'cancelled' => 'Order cancelled.',
        'completed' => 'Order completed.',
        'status' => [
            'pending' => 'Pending',
            'processing' => 'Processing',
            'completed' => 'Completed',
            'cancelled' => 'Cancelled',
        ],
    ],
];
```

## Using Translations

### In PHP

```php
// Simple translation
__('common.welcome');

// With parameters
__('common.copyright_notice', ['year' => date('Y')]);

// With pluralization
trans_choice('messages.apples', $count);

// Nested keys
__('auth.login.title');
```

### In Blade Templates

```blade
{{ __('common.welcome') }}
{{ __('common.copyright_notice', ['year' => date('Y')]) }}
@lang('auth.login.title')
```

### In JavaScript (with i18next)

```typescript
import { useTranslation } from 'react-i18next'

const { t } = useTranslation()

t('common.welcome')
t('common.copyright_notice', { year: new Date().getFullYear() })
```

## Adding New Locales

### 1. Create Directory Structure

```bash
lang/es_ES/
├── auth.php
├── common.php
├── pagination.php
├── passwords.php
└── validation.php
```

### 2. Copy and Translate

```php
<?php

declare(strict_types=1);

// lang/es_ES/common.php
return [
    'welcome' => 'Bienvenido a :app',
    'loading' => 'Cargando...',
    'save' => 'Guardar',
    'cancel' => 'Cancelar',
];
```

### 3. Update Config

```php
// config/localisation.php
return [
    'supported_locales' => [
        'en_GB' => ['name' => 'English', 'native_name' => 'English', 'regional' => 'en-GB'],
        'es_ES' => ['name' => 'Spanish', 'native_name' => 'Español', 'regional' => 'es-ES'],
    ],
];
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't skip declare(strict_types=1)
<?php // ❌ Missing declare(strict_types=1);

return [
    'key' => 'value',
];

// Don't use camelCase keys
return [
    'welcomeMessage' => 'Welcome', // ❌ Use snake_case
];

// Don't hardcode values
return [
    'copyright' => 'Copyright © 2024', // ❌ Use parameter
];

// Don't use variables
$year = date('Y'); // ❌ No variables

return [
    'copyright' => "Copyright © {$year}",
];

// Don't mix locales in one file
return [
    'en' => ['welcome' => 'Welcome'],
    'es' => ['welcome' => 'Bienvenido'], // ❌ Separate files
];
```

### ✅ Do This Instead

```php
// Include declare(strict_types=1)
<?php

declare(strict_types=1);

return [
    'key' => 'value',
];

// Use snake_case keys
return [
    'welcome_message' => 'Welcome',
];

// Use parameters
return [
    'copyright' => 'Copyright © :year',
];

// Return array directly
return [
    'copyright' => 'Copyright © :year',
];

// Separate files per locale
// lang/en_GB/common.php
return [
    'welcome' => 'Welcome',
];

// lang/es_ES/common.php
return [
    'welcome' => 'Bienvenido',
];
```

## Organizing Translations

### By Feature

```
lang/en_GB/
├── common.php         # Common UI elements
├── auth.php          # Authentication
├── validation.php    # Validation messages
├── pagination.php    # Pagination
├── passwords.php     # Password reset
└── errors.php        # Error messages
```

### Nested Organization

```php
return [
    'dashboard' => [
        'title' => 'Dashboard',
        'welcome' => 'Welcome back, :name',
        'stats' => [
            'users' => 'Total Users',
            'orders' => 'Total Orders',
        ],
    ],

    'profile' => [
        'title' => 'Profile',
        'update' => 'Update Profile',
    ],
];
```

## Quality Standards

- All translation files must pass PHPStan level 8
- Code formatted with Pint
- Consistent key naming (snake_case)
- All locales have same key structure
- Use parameters for dynamic values
- Group related translations together
- Keep file sizes manageable (split large files)
