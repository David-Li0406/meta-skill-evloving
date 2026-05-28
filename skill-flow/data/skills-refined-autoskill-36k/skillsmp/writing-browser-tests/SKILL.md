---
name: writing-browser-tests
description: Write browser tests for end-to-end user workflows and JavaScript interactions using Pest v4 with Playwright. Use MINIMALLY - only for core areas, happy paths, and functionality that CANNOT be tested with feature tests. Browser tests replace QA smoke testing, not feature tests.
---

# Write Browser Tests

Browser tests should be used minimally as automated QA smoke tests. They are slow, complex, and must never duplicate feature test coverage. Use them only for core critical workflows and functionality that requires a real browser (JavaScript interactions, WebSocket updates, drag-and-drop).

## Testing Hierarchy

1. **Feature Tests (PRIMARY)** - Default for all business logic and HTTP endpoints
2. **Unit Tests (SUPPLEMENTARY)** - For complex, concentrated areas
3. **Browser Tests (MINIMAL)** - Only for core areas and JS interactions (you're here)

## File Structure

```
tests/Browser/{FeatureName}Test.php
```

**Examples:** `LoginTest.php`, `RegistrationTest.php`, `CheckoutTest.php`

## Core Conventions

### Test Structure

```php
<?php

declare(strict_types=1);

use App\Models\User;

test('users can complete the workflow', function (): void {
    $user = User::factory()->create();

    visit(route('feature.index'))
        ->fill('field', 'value')
        ->press('Submit')
        ->assertSee('Success message')
        ->assertRoute('dashboard.index');
});
```

### Browser Testing Helpers

**Navigation:**

```php
visit(route('login'))
click('Dashboard')
back()
```

**Form Interactions:**

```php
fill('email', 'test@example.com')
select('country', 'US')
check('terms')
uncheck('newsletter')
press('Submit')
```

**Assertions:**

```php
assertSee('Welcome')
assertDontSee('Error')
assertRoute('dashboard.index')
assertPresent('#element-id')
assertMissing('.error-message')
assertChecked('terms')
```

**Waiting:**

```php
waitForText('Loading complete')
waitFor('.modal')
waitForRoute('dashboard.index')
```

### Authentication Helper

```php
function loginAs(User $user): void
{
    visit(route('login'))
        ->fill('email', $user->email)
        ->fill('password', 'password')
        ->press('Log in')
        ->assertRoute('dashboard.index');
}
```

## Anti-Patterns

### Don't Do This

```php
// Don't test validation with browser tests (use feature tests)
test('form validation works', function (): void {
    visit(route('register'))
        ->press('Submit')
        ->assertSee('The email field is required');
});

// Don't test simple form submissions (use feature tests)
test('users can update profile', function (): void {
    loginAs($user);
    visit(route('profile.edit'))
        ->fill('name', 'New Name')
        ->press('Save')
        ->assertSee('Profile updated');
});
```

### Do This Instead

```php
// Feature test - Fast and comprehensive
test('registration requires email', function (): void {
    $this->post(route('register'), [])
        ->assertInvalid(['email']);
});

// Browser test - Only for what feature tests can't test
test('profile image preview updates when file selected', function (): void {
    $user = User::factory()->create();
    loginAs($user);

    visit(route('profile.edit'))
        ->attach('avatar', storage_path('testing/avatar.jpg'))
        ->waitFor('.image-preview') // JavaScript-driven preview
        ->assertPresent('.image-preview img');
});
```

## The Golden Rule

**Before writing a browser test, ask: "Can I test this with a feature test?"**

If yes, write a feature test instead. Browser tests are for:

- Core workflow smoke tests (happy paths only)
- Functionality that literally cannot be tested without a real browser

## Running Tests

```bash
# Run all browser tests
php artisan test --testsuite=Browser

# Run in headed mode (see browser)
HEADED=1 php artisan test --testsuite=Browser
```

## Debugging

```php
screenshot('debug-screen.png')
pause(5000)
dump(script('return document.body.innerHTML'))
```

## Quality Standards

- All browser tests must pass PHPStan level 8
- Tests must be independent and idempotent
- **MINIMAL BROWSER TESTS** - Far fewer than feature tests
- **NO DUPLICATION** - Never test what feature tests already cover
- Keep tests focused on ONE happy path workflow

## References

- [references/examples.md](references/examples.md) - Complete working examples and patterns
