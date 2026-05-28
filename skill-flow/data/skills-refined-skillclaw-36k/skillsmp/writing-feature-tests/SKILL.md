---
name: writing-feature-tests
description: Write feature tests for HTTP endpoints, controllers, and full request/response cycles using Pest v4. Use when ANY business logic is added to codebase. Feature tests are the PRIMARY testing approach - use for all Controllers, Actions, Form Requests, and application behavior. This is your default testing strategy.
---

# Write Feature Tests

Feature tests are your primary testing approach for all business logic. Write feature tests for ALL logic added to the app, testing the full HTTP request/response cycle. They are fast, comprehensive, and should always be your default starting point.

## Testing Hierarchy

1. **Feature Tests (PRIMARY)** - Default for all business logic and HTTP endpoints (you're here)
2. **Unit Tests (SUPPLEMENTARY)** - Sprinkle in for complex, concentrated areas
3. **Browser Tests (MINIMAL)** - Only for core areas and JS interactions

## File Structure

```
tests/Feature/Http/Controllers/{ControllerName}/{MethodName}Test.php
```

**Examples:**

- `tests/Feature/Http/Controllers/Auth/RegisteredUserController/StoreTest.php`
- `tests/Feature/Http/Controllers/User/ProfileController/UpdateTest.php`

## Core Conventions

### Test Structure

```php
<?php

declare(strict_types=1);

use App\Models\User;

test('descriptive test name in sentence case', function (): void {
    // Arrange
    $user = User::factory()->create();

    // Act
    $response = $this->actingAs($user)->post(route('endpoint'), getData());

    // Assert
    $response->assertValid()->assertRedirect();

    expect($user->fresh())
        ->property->toBe('expected value');
});

// Helper functions at bottom of file
function getData(array $overrides = []): array
{
    return array_merge([
        'field' => 'value',
    ], $overrides);
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `test('description', function (): void {})` syntax (Pest v4)
- Follow Arrange-Act-Assert (AAA) pattern
- Helper functions at bottom of file

### HTTP Methods

```php
$this->get(route('users.index'))
$this->post(route('users.store'), getData())
$this->put(route('users.update', $user), getData())
$this->delete(route('users.destroy', $user))
```

### Authentication

```php
$this->actingAs($user)->get(route('dashboard'))
$this->assertAuthenticated()
$this->assertGuest()
```

### Response Assertions

```php
->assertOk()
->assertCreated()
->assertRedirect(route('dashboard'))
->assertValid()
->assertInvalid(['email'])
->assertJson(['key' => 'value'])
```

### Database Assertions

```php
$this->assertDatabaseHas('users', ['email' => 'test@example.com'])
$this->assertDatabaseMissing('users', ['email' => 'deleted@example.com'])
$this->assertDatabaseCount('users', 5)
```

### Expect Assertions

```php
$user = User::query()->sole();

expect($user)
    ->name->toBe('Test User')
    ->email->toBe('test@example.com')
    ->and($user->posts)->toHaveCount(3);
```

## Anti-Patterns

### Don't Do This

```php
// Don't skip return type
test('users can register', function () {});

// Don't hardcode URLs
$this->get('/dashboard');

// Don't create test data inline
$this->post(route('register'), [
    'name' => 'Test User',
    'email' => 'test@example.com',
]);
```

### Do This Instead

```php
// Always type hint return type
test('users can register', function (): void {});

// Use named routes
$this->get(route('dashboard.index'));

// Use helper functions
function getData(array $overrides = []): array
{
    return array_merge([
        'name' => 'Test User',
        'email' => 'test@example.com',
    ], $overrides);
}
```

## Running Tests

```bash
php artisan test --testsuite=Feature
php artisan test tests/Feature/Http/Controllers/Auth/RegisteredUserController/StoreTest.php
php artisan test --coverage --min=90
php artisan test --filter="new users can register"
```

## Quality Standards

- All feature tests must pass PHPStan level 8
- 100% type coverage required
- 90% overall test coverage required
- Tests must be independent (no test order dependency)
- Use `LazilyRefreshDatabase` trait (configured in Pest.php)
- Every controller method must have at least one feature test
- Critical paths must have multiple test cases (happy path + edge cases)

## References

- [references/examples.md](references/examples.md) - Complete working examples
