---
name: creating-actions
description: Create Laravel Action classes for business logic operations following domain-driven design. Use when creating Actions, implementing business logic, handling user operations, or when user mentions Action classes, domain operations, business rules, or service classes.
---

# Create Laravel Actions

Create Action classes that encapsulate business logic in single-purpose, testable units. Actions receive typed DTOs, perform domain operations, and return results, keeping controllers thin and business rules centralized and reusable.

## File Structure

```
app/Actions/{Domain}/{Name}Action.php
```

**Examples:**

- `app/Actions/Auth/RegisterUserAction.php`
- `app/Actions/User/UpdateUserPasswordAction.php`
- `app/Actions/Order/ProcessOrderAction.php`

## Core Conventions

### 1. Action Class Structure

```php
<?php

declare(strict_types=1);

namespace App\Actions\{Domain};

use App\DTOs\{Domain}\{Name}Data;
use App\Models\{Model};

final readonly class {Name}Action
{
    public function __construct(
        private DependencyOne $dependencyOne,
    ) {}

    public function handle({Name}Data $data): {ReturnType}
    {
        // Business logic here
        return $result;
    }
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `final` class modifier (always required)
- Add `readonly` modifier when all class properties are readonly
- Constructor injection for all dependencies
- Single `handle()` method as the entry point
- Accept DTOs for external data, primitives/models for internal logic
- Return domain objects, not HTTP responses

### 2. The `readonly` Keyword

```php
// Use readonly - all properties are readonly via constructor
final readonly class RegisterUserAction
{
    public function __construct(
        private Localisation $localisation,
    ) {}
}

// No readonly - no constructor properties
final class DeleteUserAction
{
    public function handle(User $user): bool
    {
        return (bool) $user->delete();
    }
}
```

### 3. Naming Conventions

- **Class name:** `{Verb}{Noun}Action` (e.g., `RegisterUserAction`)
- **Method name:** Always `handle()`
- **Namespace:** `App\Actions\{Domain}`

### 4. Dependency Injection

```php
public function __construct(
    private UserRepository $users,
    private EmailService $emailService,
) {}
```

- Inject services, repositories, or other dependencies
- Do NOT inject Request or other HTTP-specific classes
- Can inject other Actions for composition

## Input & Output Patterns

### Input: DTOs vs Primitives

**Use DTOs when:**

- Accepting data from external sources (HTTP requests, API calls)
- Data originates from Form Requests
- Multiple related fields need to be passed together

```php
public function handle(RegisterData $data): User
{
    return User::create([
        'name' => $data->name,
        'email' => $data->email,
        'password' => Hash::make($data->password),
    ]);
}
```

**Use Primitives/Models when:**

- Handling internal business logic (triggered by jobs, events, services)
- Simple single-field operations
- Data is already validated/trusted

```php
public function handle(User $user, string $password): bool
{
    $user->password = Hash::make($password);
    return $user->save();
}
```

**Decision criteria:**

- **3+ parameters?** -> Use DTO
- **From HTTP request?** -> Use DTO
- **Internal service call?** -> Primitives are fine

### Return Types

**Return Model** - When caller needs the updated instance:

```php
public function handle(RegisterData $data): User
{
    $user = User::create([...]);
    return $user;
}
```

**Return bool** - For success/failure operations:

```php
public function handle(User $user, string $password): bool
{
    return $user->save();
}
```

**Return void** - For fire-and-forget operations:

```php
public function handle(User $user): void
{
    $user->delete();
}
```

**Never return:** HTTP Response objects, Request objects, or framework-specific types.

## Anti-Patterns

### Don't Do This

```php
// Don't inject Request directly
public function __construct(private Request $request) {}

// Don't return Response objects
public function handle($data): JsonResponse
{
    return response()->json(['success' => true]);
}

// Don't use mutable class properties
final class UpdateUserAction
{
    private User $user; // No mutable state
}

// Don't skip type declarations
public function handle($data) // Must type hint
```

### Do This Instead

```php
// Accept DTOs from external sources
public function handle(UpdateUserData $data): User

// Accept primitives for internal logic
public function handle(User $user, string $password): bool

// Return domain objects
public function handle(RegisterData $data): User

// Use readonly when all properties are readonly
final readonly class UpdateUserAction
{
    public function __construct(
        private UserRepository $users
    ) {}
}
```

## Integration with Controllers

Controllers should be thin and delegate to Actions:

```php
public function store(
    RegisterRequest $request,
    RegisterUserAction $action
): RedirectResponse {
    $user = $action->handle($request->toDTO());

    auth('web')->login($user);

    return redirect('dashboard');
}
```

**Controller responsibilities:** Validate input, call Action, handle HTTP response
**Action responsibilities:** Execute business logic, interact with models/services, maintain data integrity

## Quality Standards

- All Actions must pass PHPStan level 8
- 100% type coverage required
- Code formatted with Pint
- Refactored with Rector
- Covered by feature tests (see `writing-feature-tests` skill)

## References

- [references/patterns.md](references/patterns.md) - Advanced patterns (composition, transactions, exceptions)
- [references/examples.md](references/examples.md) - Complete working examples
