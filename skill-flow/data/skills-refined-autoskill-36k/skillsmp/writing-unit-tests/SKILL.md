---
name: writing-unit-tests
description: Write unit tests for isolated business logic, Actions, DTOs, Services, and domain code using Pest v4. SUPPLEMENTARY to feature tests - use for complex, concentrated areas of the codebase that benefit from focused isolated testing. Feature tests should be your primary approach.
---

# Write Unit Tests

Unit tests are supplementary to feature tests for testing isolated business logic. Use them selectively for complex, concentrated areas like Action classes, Service classes, or helper functions that benefit from focused, isolated testing with mocked dependencies.

## Testing Hierarchy

1. **Feature Tests (PRIMARY)** - Default for all business logic and HTTP endpoints
2. **Unit Tests (SUPPLEMENTARY)** - For complex, concentrated areas (you're here)
3. **Browser Tests (MINIMAL)** - Only for core areas and JS interactions

## File Structure

```
tests/Unit/{Domain}/{ClassName}Test.php
```

**Examples:**

- `tests/Unit/Support/Localisation/LocalisationTest.php`
- `tests/Unit/Helpers/HelpersTest.php`
- `tests/Unit/Models/UserTest.php`

## Core Conventions

### Test Structure

```php
<?php

declare(strict_types=1);

use App\Actions\Domain\MyAction;
use App\DTOs\Domain\MyData;

test('it can perform expected behavior', function (): void {
    $action = createAction();
    $data = MyData::from(['field' => 'value']);

    $result = $action->handle($data);

    expect($result)
        ->toBeInstanceOf(ExpectedClass::class)
        ->property->toBe('expected value');
});

// Helper functions at bottom of file
function createAction(): MyAction
{
    return new MyAction(
        dependency: mock(DependencyClass::class)
    );
}
```

**Key Requirements:**

- Always include `declare(strict_types=1);`
- Use `test('it can...', function (): void {})` syntax
- Descriptive test names starting with "it can" or "it throws"
- Follow Arrange-Act-Assert (AAA) pattern
- Helper functions at bottom of file
- Avoid database when possible (use mocks/fakes)

### Expect Assertions

```php
// Value assertions
expect($value)->toBe('expected')
expect($value)->toBeTrue()
expect($value)->toBeNull()

// Type assertions
expect($value)->toBeInstanceOf(User::class)

// Collection assertions
expect($collection)->toHaveCount(3)

// Chaining assertions
expect($user)
    ->name->toBe('John Doe')
    ->email->toBe('john@example.com');
```

### Exception Testing

```php
test('it throws exception for invalid input', function (): void {
    $action = createAction();
    $action->handle(invalidData());
})->throws(InvalidArgumentException::class);
```

### Mocking Dependencies

```php
test('it calls dependency method', function (): void {
    $mock = mock(EmailService::class);
    $mock->shouldReceive('send')
        ->once()
        ->andReturn(true);

    $action = new SendEmailAction($mock);
    $result = $action->handle($data);

    expect($result)->toBeTrue();
});
```

### Helper Functions

```php
function createAction(
    ?DependencyOne $depOne = null,
): MyAction {
    return new MyAction(
        dependencyOne: $depOne ?? new DependencyOne,
    );
}

function createValidData(array $overrides = []): MyData
{
    return MyData::from(array_merge([
        'field1' => 'value1',
    ], $overrides));
}
```

## Anti-Patterns

### Don't Do This

```php
// Don't skip return type
test('it can do something', function () {});

// Don't test multiple behaviors in one test
test('it can do everything', function (): void {
    expect($service->methodOne())->toBeTrue();
    expect($service->methodTwo())->toBe('value');
});

// Don't use database when unnecessary
test('it can calculate total', function (): void {
    $order = Order::factory()->create(['subtotal' => 100]);
    expect($order->calculateTotal())->toBe(110);
});
```

### Do This Instead

```php
// Always type hint return type
test('it can do something', function (): void {});

// One behavior per test
test('it can validate email format', function (): void {
    expect($validator->isValidEmail('test@example.com'))->toBeTrue();
});

// Avoid database when possible
test('it can calculate total', function (): void {
    $calculator = new OrderCalculator;
    expect($calculator->calculateTotal(100, 0.1))->toBe(110);
});
```

## Running Tests

```bash
php artisan test --testsuite=Unit
php artisan test tests/Unit/Support/Localisation/LocalisationTest.php
php artisan test --filter="it can get the ISO 15897 locale"
```

## Quality Standards

- All unit tests must pass PHPStan level 8
- 100% type coverage required
- Tests must be independent and run in any order
- Prefer mocks/fakes over real dependencies
- Every public method should have unit tests
- Test edge cases, not just happy paths

## References

- [references/examples.md](references/examples.md) - Complete working examples
