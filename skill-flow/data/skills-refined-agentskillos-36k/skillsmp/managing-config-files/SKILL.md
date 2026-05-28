---
name: managing-config-files
description: Create and manage Laravel configuration files with proper structure and type safety. Use when creating config files, managing application settings, defining configuration, or when user mentions config files, configuration, settings, or app config.
---

# Manage Laravel Config Files

Create and manage Laravel configuration files with proper structure and type safety. Config files define application settings accessed via the `config()` helper, with environment-specific values loaded from `.env` files.

## File Structure

Config files are stored in the config directory:

```
config/{name}.php
```

**Examples:**

- `config/localisation.php`
- `config/horizon.php`
- `config/services.php`

## Core Conventions

### 1. Config File Structure

```php
<?php

declare(strict_types=1);

return [
    /*
    |--------------------------------------------------------------------------
    | Configuration Section Title
    |--------------------------------------------------------------------------
    |
    | Description of what this configuration section controls and any
    | important information developers should know.
    |
    */

    'key' => env('ENV_VAR', 'default-value'),

    'nested' => [
        'key' => 'value',
    ],
];
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Return array directly (no variables)
- Use `env()` helper for environment variables
- Provide sensible defaults
- Include documentation blocks
- Use snake_case for keys

### 2. Environment Variables

```php
return [
    'api_key' => env('SERVICE_API_KEY'),
    'api_secret' => env('SERVICE_API_SECRET'),
    'timeout' => env('SERVICE_TIMEOUT', 30),
    'enabled' => env('SERVICE_ENABLED', true),
];
```

### 3. Nested Configuration

```php
return [
    'supported_locales' => [
        'en_GB' => ['name' => 'English', 'native_name' => 'English', 'regional' => 'en-GB'],
        'es_ES' => ['name' => 'Spanish', 'native_name' => 'Español', 'regional' => 'es-ES'],
    ],
];
```

## Examples

### Example 1: Simple Config File

```php
<?php

declare(strict_types=1);

return [
    /*
    |--------------------------------------------------------------------------
    | Supported Locales
    |--------------------------------------------------------------------------
    |
    | Here you may specify the list of locales that your application supports.
    | The localisation service will only set the locale to one of the
    | locales in this list.
    |
    */
    'supported_locales' => [
        'en_GB' => ['name' => 'English', 'native_name' => 'English', 'regional' => 'en-GB'],
    ],
];
```

### Example 2: Service Configuration

```php
<?php

declare(strict_types=1);

return [
    /*
    |--------------------------------------------------------------------------
    | Third Party Services
    |--------------------------------------------------------------------------
    |
    | This file is for storing the credentials for third party services such
    | as Mailgun, Postmark, AWS and more. This file provides the de facto
    | location for this type of information, allowing packages to have
    | a conventional file to locate the various service credentials.
    |
    */

    'stripe' => [
        'key' => env('STRIPE_KEY'),
        'secret' => env('STRIPE_SECRET'),
        'webhook' => [
            'secret' => env('STRIPE_WEBHOOK_SECRET'),
            'tolerance' => env('STRIPE_WEBHOOK_TOLERANCE', 300),
        ],
    ],

    'mailgun' => [
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
        'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
    ],
];
```

### Example 3: Feature Flags

```php
<?php

declare(strict_types=1);

return [
    /*
    |--------------------------------------------------------------------------
    | Feature Flags
    |--------------------------------------------------------------------------
    |
    | This file contains all feature flags for the application. Feature flags
    | allow you to enable or disable features without deploying new code.
    |
    */

    'features' => [
        'two_factor_auth' => env('FEATURE_TWO_FACTOR_AUTH', true),
        'api_v2' => env('FEATURE_API_V2', false),
        'maintenance_mode' => env('FEATURE_MAINTENANCE_MODE', false),
    ],
];
```

### Example 4: Query Builder Config

```php
<?php

declare(strict_types=1);

return [
    /*
    |--------------------------------------------------------------------------
    | Query Builder Parameters
    |--------------------------------------------------------------------------
    |
    | Configure the query string parameters used by Spatie Query Builder
    | for filtering, sorting, and including relationships.
    |
    */

    'parameters' => [
        'include' => 'include',
        'filter' => 'filter',
        'sort' => 'sort',
        'fields' => 'fields',
        'append' => 'append',
    ],

    'disable_invalid_filter_query_exception' => false,
];
```

## Accessing Config Values

### In Code

```php
// Simple value
$locale = config('app.locale');

// Nested value
$stripeKey = config('services.stripe.key');

// With default
$timeout = config('services.stripe.timeout', 30);

// All config
$allLocales = config('localisation.supported_locales');
```

### With Dependency Injection

```php
use Illuminate\Container\Attributes\Config;

final readonly class MyService
{
    public function __construct(
        #[Config('app.locale')] private string $defaultLocale,
        #[Config('services.stripe.key')] private string $stripeKey,
    ) {}
}
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't skip declare(strict_types=1)
<?php // ❌ Missing declare(strict_types=1);

return [
    'key' => 'value',
];

// Don't use variables
$timeout = 30; // ❌ No variables

return [
    'timeout' => $timeout,
];

// Don't access $_ENV directly
return [
    'key' => $_ENV['API_KEY'], // ❌ Use env()
];

// Don't use camelCase keys
return [
    'apiKey' => env('API_KEY'), // ❌ Use snake_case
];

// Don't skip defaults for optional values
return [
    'timeout' => env('TIMEOUT'), // ❌ Provide default
];

// Don't put business logic in config
return [
    'enabled' => now()->hour >= 9, // ❌ No logic
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

// Return array directly
return [
    'timeout' => 30,
];

// Use env() helper
return [
    'key' => env('API_KEY'),
];

// Use snake_case keys
return [
    'api_key' => env('API_KEY'),
];

// Provide defaults
return [
    'timeout' => env('TIMEOUT', 30),
];

// Keep config static
return [
    'enabled' => env('FEATURE_ENABLED', true),
];
```

## Environment Variables

Create corresponding `.env` entries:

```bash
# .env
SERVICE_API_KEY=your-api-key
SERVICE_TIMEOUT=30
FEATURE_TWO_FACTOR_AUTH=true
```

Document in `.env.example`:

```bash
# .env.example
SERVICE_API_KEY=
SERVICE_TIMEOUT=30
FEATURE_TWO_FACTOR_AUTH=true
```

## Quality Standards

- All config files must pass PHPStan level 8
- Code formatted with Pint
- Include documentation blocks
- Provide sensible defaults
- Use `env()` for environment-specific values
- Keep config files simple (no business logic)
