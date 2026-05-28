---
name: creating-dtos
description: Create Laravel Data Transfer Objects (DTOs) for safely passing data between layers. Use when creating DTOs, transferring data, passing validated data to Actions, or when user mentions DTOs, data objects, value objects, or data transfer.
---

# Create Laravel DTOs

Create Data Transfer Objects (DTOs) that provide type-safe containers for passing validated data between application layers. DTOs ensure data integrity from Form Requests through Actions, with immutable properties and factory methods for construction.

## File Structure

DTOs are organized by domain context:

```
app/DTOs/{Domain}/{Name}Data.php
```

**Examples:**

- `app/DTOs/Auth/RegisterData.php`
- `app/DTOs/User/UpdateUserData.php`
- `app/DTOs/Order/CreateOrderData.php`

## Core Conventions

### 1. DTO Class Structure

DTOs must follow these patterns:

```php
<?php

declare(strict_types=1);

namespace App\DTOs\{Domain};

final readonly class {Name}Data
{
    public function __construct(
        public string $propertyOne,
        public int $propertyTwo,
        public ?array $propertyThree = null,
    ) {}
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `final readonly` class modifier
- All properties must be public and readonly
- Use constructor property promotion
- Full type hints on all properties (including nullable)
- Optional properties have default values

### 2. Naming Conventions

- **Class name:** `{Context}Data` (e.g., `RegisterData`, `UpdateUserData`)
- **Namespace:** `App\DTOs\{Domain}`
- **Properties:** Use camelCase, match domain terminology

### 3. Property Types

Use PHP's type system fully:

```php
final readonly class UpdateUserData
{
    public function __construct(
        public string $name,              // Required string
        public ?string $email = null,     // Optional string
        public array $roles = [],         // Required array with default
        public bool $active = true,       // Required bool with default
    ) {}
}
```

## Examples

### Example 1: Simple DTO

```php
<?php

declare(strict_types=1);

namespace App\DTOs\Auth;

final readonly class RegisterData
{
    public function __construct(
        public string $name,
        public string $email,
        public string $language,
        public string $password,
    ) {}
}
```

### Example 2: DTO with Optional Properties

```php
<?php

declare(strict_types=1);

namespace App\DTOs\User;

final readonly class UpdateUserData
{
    public function __construct(
        public int $userId,
        public string $name,
        public ?string $email = null,
        public ?string $language = null,
    ) {}
}
```

### Example 3: DTO with Complex Types

```php
<?php

declare(strict_types=1);

namespace App\DTOs\User;

use Illuminate\Http\UploadedFile;

final readonly class UpdateUserAvatarData
{
    public function __construct(
        public int $userId,
        public UploadedFile $avatar,
    ) {}
}
```

## Integration with Form Requests

Form Requests convert validated data to DTOs:

```php
final class RegisterRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', 'unique:users'],
            'password' => ['required', 'confirmed', Password::defaults()],
        ];
    }

    public function toDTO(): RegisterData
    {
        return new RegisterData(
            name: $this->validated('name'),
            email: $this->validated('email'),
            language: $this->validated('language') ?? config('app.locale'),
            password: $this->validated('password'),
        );
    }
}
```

## Integration with Actions

Actions receive DTOs, not Requests:

```php
final readonly class RegisterUserAction
{
    public function handle(RegisterData $data): User
    {
        return User::query()->create([
            'name' => $data->name,
            'email' => $data->email,
            'language' => $data->language,
            'password' => Hash::make($data->password),
        ]);
    }
}
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't use mutable properties
final class UpdateUserData
{
    public string $name; // ❌ Must be readonly
}

// Don't omit type hints
final readonly class RegisterData
{
    public function __construct(
        public $name, // ❌ Must have type hint
    ) {}
}

// Don't add methods (keep it a pure data container)
final readonly class RegisterData
{
    public function __construct(public string $name) {}

    public function isValid(): bool {} // ❌ No methods
}

// Don't use arrays for structured data
public function __construct(
    public array $user, // ❌ Use specific DTOs
) {}
```

### ✅ Do This Instead

```php
// Use readonly properties
final readonly class UpdateUserData
{
    public function __construct(
        public string $name,
    ) {}
}

// Always type hint
public function __construct(
    public string $name,
    public ?string $email = null,
) {}

// Keep DTOs pure (no methods)
final readonly class RegisterData
{
    public function __construct(
        public string $name,
        public string $email,
    ) {}
}

// Use nested DTOs for structure
public function __construct(
    public UserData $user,
    public AddressData $address,
) {}
```

## Quality Standards

- All DTOs must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Refactored with Rector
- No behavioral logic in DTOs (pure data)
