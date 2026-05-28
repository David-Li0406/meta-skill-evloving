---
name: creating-form-requests
description: Create Laravel Form Request classes for validation with toDTO() conversion methods. Use when creating form requests, validating input, handling validation rules, or when user mentions form requests, validation, request validation, or input validation.
---

# Create Laravel Form Requests

Create Form Request classes that handle validation and convert input to type-safe DTOs. Form Requests centralize validation rules, authorization checks, and data transformation, keeping controllers thin and validation reusable.

## File Structure

Form Requests are organized by domain/feature:

```
app/Http/Requests/{Domain}/{Name}Request.php
```

**Examples:**

- `app/Http/Requests/Auth/RegisterRequest.php`
- `app/Http/Requests/Account/UpdateAccountRequest.php`
- `app/Http/Requests/Account/UpdateAccountAvatarRequest.php`

## Core Conventions

### 1. Form Request Structure

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests\{Domain};

use App\DTOs\{Domain}\{Name}Data;
use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;
use Illuminate\Foundation\Http\FormRequest;

final class {Name}Request extends FormRequest
{
    /**
     * @return array<string, list<ValidatorAwareRule|ValidationRule|string|null>>
     */
    public function rules(): array
    {
        return [
            'field' => ['required', 'string', 'max:255'],
        ];
    }

    public function toDTO(): {Name}Data
    {
        return new {Name}Data(
            field: $this->validated('field'),
        );
    }
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `final class` modifier
- Extend `FormRequest` base class
- Type hint `rules()` return with full PHPDoc array shape
- Always include `toDTO()` method returning a DTO
- Use `validated()` method to get validated values

### 2. Validation Rules

```php
public function rules(): array
{
    return [
        'name' => ['required', 'string', 'max:255'],
        'email' => ['required', 'email', 'unique:users'],
        'password' => ['required', 'confirmed', Password::defaults()],
        'language' => ['sometimes', 'nullable', 'string'],
    ];
}
```

- Array syntax for rules (not pipe syntax)
- Use Laravel's rule objects for complex validation
- Use `sometimes` for optional fields
- Use `nullable` to allow null values

### 3. toDTO() Method

```php
public function toDTO(): RegisterData
{
    return new RegisterData(
        name: $this->validated('name'),
        email: $this->validated('email'),
        language: $this->validated('language') ?? config('app.locale'),
        password: $this->validated('password'),
    );
}
```

- Use `validated()` method for type safety
- Provide defaults for optional values
- Use named arguments for clarity

## Examples

### Example 1: Simple Form Request

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests\Auth;

use App\DTOs\Auth\RegisterData;
use App\Support\Localisation\Facades\Localisation;
use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

final class RegisterRequest extends FormRequest
{
    /**
     * @return array<string, list<ValidatorAwareRule|ValidationRule|string|null>>
     */
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'string', 'lowercase', 'email', 'max:255', 'unique:users'],
            'language' => ['sometimes', 'nullable', 'string'],
            'password' => ['required', 'confirmed', Password::defaults()],
        ];
    }

    public function toDTO(): RegisterData
    {
        return new RegisterData(
            name: $this->validated('name'),
            email: $this->validated('email'),
            language: $this->validated('language') ?? Localisation::getDefaultLocale(),
            password: $this->validated('password'),
        );
    }
}
```

### Example 2: Form Request with Authorization

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests\Account;

use App\DTOs\User\UpdateUserData;
use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

final class UpdateAccountRequest extends FormRequest
{
    /**
     * @return array<string, list<ValidatorAwareRule|ValidationRule|string|null>>
     */
    public function rules(): array
    {
        return [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'email', 'max:255', Rule::unique('users')->ignore($this->user())],
        ];
    }

    public function authorize(): bool
    {
        return $this->user() !== null;
    }

    public function toDTO(): UpdateUserData
    {
        return new UpdateUserData(
            userId: $this->user()->id,
            name: $this->validated('name'),
            email: $this->validated('email'),
        );
    }
}
```

### Example 3: Form Request with File Upload

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests\Account;

use App\DTOs\User\UpdateUserAvatarData;
use Illuminate\Contracts\Validation\ValidationRule;
use Illuminate\Contracts\Validation\ValidatorAwareRule;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\File;

final class UpdateAccountAvatarRequest extends FormRequest
{
    /**
     * @return array<string, list<ValidatorAwareRule|ValidationRule|string|null>>
     */
    public function rules(): array
    {
        return [
            'avatar' => ['required', File::image()->max(2048)],
        ];
    }

    public function toDTO(): UpdateUserAvatarData
    {
        return new UpdateUserAvatarData(
            userId: $this->user()->id,
            avatar: $this->validated('avatar'),
        );
    }
}
```

## Anti-Patterns

### ❌ Don't Do This

```php
// Don't omit type hints on rules()
public function rules()
{
    return ['name' => 'required'];
}

// Don't skip toDTO() method
final class RegisterRequest extends FormRequest
{
    public function rules(): array
    {
        return ['name' => ['required']];
    }
    // ❌ Missing toDTO()
}

// Don't access unvalidated input
public function toDTO(): RegisterData
{
    return new RegisterData(
        name: $this->input('name'), // ❌ Use validated()
    );
}

// Don't return arrays instead of DTOs
public function toArray(): array // ❌ Use toDTO() returning DTO
{
    return $this->validated();
}
```

### ✅ Do This Instead

```php
// Type hint rules() with PHPDoc
/**
 * @return array<string, list<ValidatorAwareRule|ValidationRule|string|null>>
 */
public function rules(): array

// Always include toDTO()
public function toDTO(): RegisterData
{
    return new RegisterData(
        name: $this->validated('name'),
    );
}

// Use validated() method
public function toDTO(): RegisterData
{
    return new RegisterData(
        name: $this->validated('name'),
    );
}
```

## Integration with Controllers

Controllers receive Form Requests and convert to DTOs:

```php
public function store(
    RegisterRequest $request,
    RegisterUserAction $action
): RedirectResponse {
    $user = $action->handle($request->toDTO());

    return redirect('dashboard');
}
```

## Quality Standards

- All Form Requests must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Refactored with Rector
- Covered by feature tests (see `writing-feature-tests` skill)
