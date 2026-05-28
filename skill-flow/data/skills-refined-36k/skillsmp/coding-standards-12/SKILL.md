---
name: coding-standards
description: PHP coding standards (PSR-12, PHPDoc, type hints) for any PHP project
hooks:
  SessionStart:
    - type: command
      command: |
        if command -v yq &> /dev/null && [ -f ".claude/config.yaml" ]; then
          echo "=== PHP Coding Standards ==="
          yq -o=json '.coding_standards' .claude/config.yaml 2>/dev/null || true
        fi
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: |
            FILE="${TOOL_INPUT_FILE_PATH:-}"
            [ -z "$FILE" ] && exit 0
            EXT="${FILE##*.}"
            case "$EXT" in
              php) php -l "$FILE" 2>&1 | head -5 || true ;;
            esac
---

# PHP Coding Standards

Language-level coding standards for PHP, applicable to any PHP project regardless of framework.

## PSR-12 Compliance

### File Structure

```php
<?php
declare(strict_types=1);  // Required at file top

namespace App\Controller\User;  // PSR-4 autoloading

use Cake\Controller\Controller;  // Alphabetical imports
use Cake\Http\Response;

/**
 * User Controller
 *
 * Handles user management operations
 *
 * @property \App\Model\Table\UsersTable $Users
 */
class UserController extends Controller  // PascalCase for classes
{
    // Class body
}
```

### Method Documentation (PHPDoc)

```php
/**
 * Display user list
 *
 * Retrieves and displays paginated list of users for the current company.
 *
 * @return \Cake\Http\Response|null Renders user list view
 * @throws \Cake\Http\Exception\NotFoundException When user not found
 */
public function index(): ?Response
{
    // Method implementation
}
```

### Type Hints (PHP 8.2+)

**Required for all methods:**

```php
// Parameter type hints
public function findUser(int $id): ?User
{
    return $this->Users->get($id);
}

// Return type hints
public function getStatus(): string
{
    return 'active';
}

// Union types (PHP 8.0+)
public function process(string|int $value): bool
{
    return is_numeric($value);
}

// Nullable types
public function findOptional(int $id): ?User
{
    try {
        return $this->Users->get($id);
    } catch (RecordNotFoundException $e) {
        return null;
    }
}
```

### Naming Conventions

```php
// Classes: PascalCase
class UserManagementService {}

// Methods: camelCase
public function getUserById(int $id): ?User {}

// Constants: UPPER_SNAKE_CASE
const MAX_LOGIN_ATTEMPTS = 5;

// Properties: camelCase
private string $userName;

// Local variables: camelCase
$userData = $this->fetchData();
```

### Code Formatting

```php
// Indentation: 4 spaces (not tabs)
public function example(): void
{
    if ($condition) {
        // 4 space indent
        $this->doSomething();
    }
}

// Line length: <= 120 characters
public function methodWithLongName(
    string $firstParameter,
    int $secondParameter,
    bool $thirdParameter
): array {
    return [];
}

// Blank lines
class Example
{
    private string $property;  // Property declaration
                               // Blank line before methods
    public function method(): void
    {
        // Method body
    }
                               // Blank line between methods
    public function anotherMethod(): void
    {
        // Method body
    }
}
```

## PHPDoc Standards

### Required Elements

```php
/**
 * Short description (one line)
 *
 * Long description if needed.
 * Can span multiple lines.
 *
 * @param string $name User name
 * @param int $age User age
 * @return bool Success status
 * @throws \InvalidArgumentException When age is negative
 */
public function validateUser(string $name, int $age): bool
{
    if ($age < 0) {
        throw new \InvalidArgumentException('Age cannot be negative');
    }
    return true;
}
```

### Optional Elements

```php
/**
 * Process user data
 *
 * @param array $data User data
 * @return User Processed user entity
 * @see UserValidator::validate() Related validation
 * @deprecated 2.0.0 Use processUserEntity() instead
 * @todo Add email validation
 */
public function processUser(array $data): User
{
    // Implementation
}
```

### Property Documentation

```php
/**
 * @var \App\Model\Table\UsersTable Users table instance
 */
public $Users;

/**
 * @var array<string, mixed> Configuration options
 */
private array $config;
```

## Error Handling

### Exception Types

```php
// Use specific exception types
throw new \InvalidArgumentException('Invalid user ID');
throw new \RuntimeException('Database connection failed');
throw new \LogicException('Method called in wrong state');

// Document all thrown exceptions
/**
 * @throws \InvalidArgumentException When ID is invalid
 * @throws \RuntimeException When database fails
 */
public function getUser(int $id): User {}
```

### Try-Catch Blocks

```php
try {
    $user = $this->Users->get($id);
    $this->processUser($user);
} catch (RecordNotFoundException $e) {
    // Handle specific exception
    Log::error('User not found: ' . $id);
    throw new NotFoundException('User not found');
} catch (\Exception $e) {
    // Handle general exception
    Log::error('Unexpected error: ' . $e->getMessage());
    throw $e;
}
```

## Code Quality Standards

### Validation Rules

Check these in code review:
- [ ] All public methods have PHPDoc comments
- [ ] All parameters have type hints
- [ ] Return types are declared
- [ ] Exceptions are documented with @throws
- [ ] PSR-12 formatting applied (indentation, spacing, line length)
- [ ] No unused imports
- [ ] Properties have visibility modifiers
- [ ] No PHP short tags (`<?=`)

### Static Analysis

Use PHPStan for type checking:
```bash
vendor/bin/phpstan analyse src tests --level 7
```

### Code Style

Use PHP-CS-Fixer for automatic formatting:
```bash
vendor/bin/php-cs-fixer fix --config=.php-cs-fixer.dist.php
```

## Framework-Agnostic

These standards apply to:
- CakePHP projects
- Laravel projects
- Symfony projects
- Plain PHP projects
- Any PHP codebase

Framework-specific conventions should be defined in framework-level skills (e.g., `php-cakephp/framework-conventions`).
