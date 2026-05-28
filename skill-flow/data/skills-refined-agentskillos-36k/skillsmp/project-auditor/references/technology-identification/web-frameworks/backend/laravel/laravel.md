# Laravel

**Category**: web-frameworks/backend
**Description**: The PHP Framework for Web Artisans - Elegant syntax and developer experience

## Package Detection

### COMPOSER
- `laravel/framework`
- `laravel/laravel`

### Related Packages
- `laravel/tinker`
- `laravel/sanctum`
- `laravel/passport`
- `laravel/horizon`
- `laravel/telescope`
- `spatie/laravel-permission`

## Import Detection

### Php
File extensions: .php

**Pattern**: `use Illuminate\\`
- Laravel framework imports
- Example: `use Illuminate\Support\Facades\Route;`

**Pattern**: `namespace App\\`
- Laravel application namespace
- Example: `namespace App\Http\Controllers;`

**Pattern**: `use App\\Models\\`
- Laravel Eloquent models
- Example: `use App\Models\User;`

### Common Imports
- `Illuminate\Support\Facades\Route`
- `Illuminate\Support\Facades\DB`
- `Illuminate\Http\Request`
- `App\Models`

## Environment Variables

*Laravel environment variables*

- `APP_NAME`
- `APP_ENV`
- `APP_KEY`
- `APP_DEBUG`
- `APP_URL`
- `DB_CONNECTION`
- `DB_HOST`
- `DB_DATABASE`

## Configuration Files

- `artisan`
- `composer.json`
- `config/app.php`
- `routes/web.php`
- `routes/api.php`

## Detection Notes

- Laravel is PHP-based
- Uses Composer for dependency management
- Artisan CLI for code generation

## Detection Confidence

- **Package Detection**: 95% (HIGH)
- **Import Detection**: 90% (HIGH)
- **Environment Variable Detection**: 75% (MEDIUM)
- **API Endpoint Detection**: 80% (MEDIUM)
