# Browser Test Examples

Complete working examples for browser tests.

## Contents

- [Simple Login Test](#simple-login-test)
- [Registration Flow](#registration-flow)
- [Interactive UI Testing](#interactive-ui-testing)
- [Multi-Step Workflow](#multi-step-workflow)
- [Proper Test Distribution](#proper-test-distribution)

---

## Simple Login Test

```php
<?php

declare(strict_types=1);

use App\Models\User;

test('users can login', function (): void {
    $user = User::factory()->create();

    visit(route('login'))
        ->fill('email', $user->email)
        ->fill('password', 'password')
        ->press('Log in')
        ->assertSee('Welcome')
        ->assertRoute('dashboard.index');
});

test('users with invalid credentials cannot login', function (): void {
    visit(route('login'))
        ->fill('email', 'test@example.com')
        ->fill('password', 'wrong-password')
        ->press('Log in')
        ->assertSee('These credentials do not match our records.');
});
```

---

## Registration Flow

```php
<?php

declare(strict_types=1);

use App\Models\User;

test('new users can register', function (): void {
    visit(route('register'))
        ->fill('name', 'Test User')
        ->fill('email', 'test@example.com')
        ->fill('password', 'password')
        ->fill('password_confirmation', 'password')
        ->select('language', 'en')
        ->check('terms')
        ->press('Register')
        ->assertRoute('dashboard.index')
        ->assertSee('Welcome, Test User');

    $user = User::query()->where('email', 'test@example.com')->sole();

    expect($user)
        ->name->toBe('Test User')
        ->email->toBe('test@example.com')
        ->language->toBe('en');
});

test('registration validates required fields', function (): void {
    visit(route('register'))
        ->press('Register')
        ->assertSee('The name field is required')
        ->assertSee('The email field is required')
        ->assertSee('The password field is required');
});
```

---

## Interactive UI Testing

```php
<?php

declare(strict_types=1);

use App\Models\User;

test('users can update profile with image upload', function (): void {
    $user = User::factory()->create();

    loginAs($user);

    visit(route('profile.edit'))
        ->fill('name', 'Updated Name')
        ->attach('avatar', storage_path('testing/avatar.jpg'))
        ->press('Save')
        ->waitForText('Profile updated')
        ->assertSee('Updated Name');

    expect($user->fresh())
        ->name->toBe('Updated Name')
        ->avatar_path->not->toBeNull();
});

test('users can toggle notification settings', function (): void {
    $user = User::factory()->create([
        'email_notifications' => true,
    ]);

    loginAs($user);

    visit(route('settings.notifications'))
        ->assertChecked('email_notifications')
        ->uncheck('email_notifications')
        ->press('Save')
        ->waitForText('Settings saved')
        ->assertNotChecked('email_notifications');

    expect($user->fresh()->email_notifications)->toBeFalse();
});

test('modal opens and closes correctly', function (): void {
    $user = User::factory()->create();

    loginAs($user);

    visit(route('dashboard.index'))
        ->assertMissing('.modal')
        ->press('Open Modal')
        ->waitFor('.modal')
        ->assertSee('Modal Content')
        ->press('Close')
        ->waitForMissing('.modal')
        ->assertMissing('.modal');
});

function loginAs(User $user): void
{
    visit(route('login'))
        ->fill('email', $user->email)
        ->fill('password', 'password')
        ->press('Log in')
        ->assertRoute('dashboard.index');
}
```

---

## Multi-Step Workflow

```php
test('users can complete checkout process', function (): void {
    $user = User::factory()->create();
    $product = Product::factory()->create(['price' => 1000]);

    loginAs($user);

    // Step 1: Add to cart
    visit(route('products.show', $product))
        ->press('Add to Cart')
        ->assertSee('Added to cart');

    // Step 2: View cart
    click('Cart')
        ->assertRoute('cart.index')
        ->assertSee($product->name)
        ->assertSee('$10.00');

    // Step 3: Proceed to checkout
    press('Checkout')
        ->assertRoute('checkout.index');

    // Step 4: Fill shipping info
    fill('address', '123 Main St')
        ->fill('city', 'New York')
        ->select('country', 'US')
        ->press('Continue');

    // Step 5: Fill payment info
    fill('card_number', '4242424242424242')
        ->fill('expiry', '12/25')
        ->fill('cvc', '123')
        ->press('Place Order');

    // Step 6: Verify success
    waitForText('Order confirmed')
        ->assertRoute('orders.show')
        ->assertSee('Order #');
});
```

---

## Proper Test Distribution

Feature tests are primary. Browser tests are supplementary smoke tests.

```php
// Feature tests (PRIMARY) - Test all the logic
test('order total is calculated correctly', function (): void {
    $user = User::factory()->create();
    $product = Product::factory()->create(['price' => 1000]);

    $this->actingAs($user)
        ->post(route('orders.store'), [
            'product_id' => $product->id,
            'quantity' => 2,
        ])
        ->assertRedirect();

    expect(Order::query()->sole()->total)->toBe(2000);
});

test('order requires valid payment method', function (): void {
    // ... feature test for validation
});

test('order updates inventory', function (): void {
    // ... feature test for inventory logic
});

// Browser test (MINIMAL) - Just the happy path smoke test
// This assumes all logic is already tested via feature tests
test('users can complete checkout happy path', function (): void {
    $user = User::factory()->create();
    $product = Product::factory()->create(['price' => 1000]);

    loginAs($user);

    // Only testing critical path works end-to-end in a real browser
    visit(route('products.show', $product))
        ->press('Add to Cart')
        ->click('Checkout')
        ->fill('address', '123 Main St')
        ->press('Place Order')
        ->waitForText('Order confirmed')
        ->assertSee('Order #');
});
```

**Guideline:**

- Feature tests: Test ALL the logic comprehensively
- Browser tests: Test ONE happy path to verify it works in a real browser

You should have many feature tests and very few browser tests.
