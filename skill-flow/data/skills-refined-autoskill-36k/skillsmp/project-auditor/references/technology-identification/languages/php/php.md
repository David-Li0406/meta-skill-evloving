# PHP

**Category**: languages
**Description**: PHP programming language - server-side scripting language widely used for web development
**Homepage**: https://www.php.net

## Package Detection

### COMPOSER
- `php`
- `composer/composer`
- `phpunit/phpunit`
- `phpstan/phpstan`

## Configuration Files

- `composer.json`
- `composer.lock`
- `php.ini`
- `phpunit.xml`
- `phpunit.xml.dist`
- `phpstan.neon`
- `phpcs.xml`
- `.php-version`
- `.php-cs-fixer.php`
- `.phpunit.result.cache`
- `artisan` (Laravel)

## File Extensions

- `.php`
- `.phtml`
- `.inc`
- `.phps`

## Import Detection

### PHP
**Pattern**: `<\?php`
- PHP opening tag
- Example: `<?php`

**Pattern**: `^namespace\s+[\w\\\\]+;`
- Namespace declaration
- Example: `namespace App\Services;`

**Pattern**: `^use\s+[\w\\\\]+;`
- Use statement
- Example: `use Illuminate\Http\Request;`

**Pattern**: `^class\s+\w+`
- Class declaration
- Example: `class UserController extends Controller {}`

**Pattern**: `^function\s+\w+\(`
- Function declaration
- Example: `function processOrder($order) {}`

**Pattern**: `require(_once)?\s+['"]`
- Require statement
- Example: `require_once 'vendor/autoload.php';`

## Environment Variables

- `PHP_VERSION`
- `COMPOSER_HOME`
- `COMPOSER_CACHE_DIR`
- `APP_ENV`
- `APP_DEBUG`
- `APP_KEY`

## Version Indicators

- PHP 8.3 (current)
- PHP 8.2 (stable)
- PHP 8.1 (active support)
- PHP 8.0 (security only)
- PHP 7.4 (end of life)

## Detection Notes

- Look for `.php` files in repository
- composer.json is the primary indicator
- Check for framework files (artisan for Laravel)
- vendor/ directory contains dependencies
- public/index.php often indicates web app

## Detection Confidence

- **File Extension Detection**: 95% (HIGH)
- **composer.json Detection**: 95% (HIGH)
- **Package Detection**: 90% (HIGH)
