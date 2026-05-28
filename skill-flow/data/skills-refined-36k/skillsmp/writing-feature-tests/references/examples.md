# Feature Test Examples

Complete examples demonstrating feature test patterns.

## Contents

- [Registration Test](#registration-test)
- [Update Profile Test](#update-profile-test)
- [API Resource Test](#api-resource-test)
- [Action Integration Test](#action-integration-test)

---

## Registration Test

```php
<?php

declare(strict_types=1);

use App\Models\User;
use Illuminate\Support\Facades\Hash;

test('new users can register', function (): void {
    $this->post(route('register'), getRegistrationData())
        ->assertValid()
        ->assertRedirect(route('dashboard.index'));

    $this->assertAuthenticated();

    $user = User::query()->sole();

    expect($user)
        ->name->toBe('Test User')
        ->email->toBe('test@example.com')
        ->language->toBe(config('app.locale'))
        ->email_verified_at->toBeNull()
        ->and(Hash::check('password', $user->password))->toBeTrue();
});

test('registration requires valid email', function (): void {
    $this->post(route('register'), getRegistrationData(['email' => 'invalid']))
        ->assertInvalid(['email']);

    $this->assertGuest();
    $this->assertDatabaseCount('users', 0);
});

function getRegistrationData(array $overrides = []): array
{
    return array_merge([
        'name' => 'Test User',
        'email' => 'test@example.com',
        'language' => 'en',
        'password' => 'password',
        'password_confirmation' => 'password',
    ], $overrides);
}
```

---

## Update Profile Test

```php
<?php

declare(strict_types=1);

use App\Models\User;

test('authenticated users can update their profile', function (): void {
    $user = User::factory()->create([
        'name' => 'Old Name',
        'email' => 'old@example.com',
    ]);

    $this->actingAs($user)
        ->patch(route('profile.update'), getProfileData())
        ->assertValid()
        ->assertRedirect(route('profile.edit'))
        ->assertSessionHas('status', 'profile-updated');

    expect($user->fresh())
        ->name->toBe('New Name')
        ->email->toBe('new@example.com');
});

test('users cannot update profile with duplicate email', function (): void {
    $existingUser = User::factory()->create(['email' => 'existing@example.com']);
    $user = User::factory()->create();

    $this->actingAs($user)
        ->patch(route('profile.update'), getProfileData([
            'email' => 'existing@example.com',
        ]))
        ->assertInvalid(['email']);

    expect($user->fresh()->email)->not->toBe('existing@example.com');
});

function getProfileData(array $overrides = []): array
{
    return array_merge([
        'name' => 'New Name',
        'email' => 'new@example.com',
    ], $overrides);
}
```

---

## API Resource Test

```php
<?php

declare(strict_types=1);

use App\Models\Order;
use App\Models\User;

test('authenticated users can list their orders', function (): void {
    $user = User::factory()->create();
    $orders = Order::factory()->count(3)->for($user)->create();

    $this->actingAs($user)
        ->get(route('api.orders.index'))
        ->assertOk()
        ->assertJsonCount(3, 'data')
        ->assertJsonStructure([
            'data' => [
                '*' => ['id', 'total', 'status', 'created_at'],
            ],
        ]);
});

test('users can only see their own orders', function (): void {
    $user = User::factory()->create();
    $otherUser = User::factory()->create();

    Order::factory()->for($otherUser)->create();
    Order::factory()->for($user)->create();

    $this->actingAs($user)
        ->get(route('api.orders.index'))
        ->assertOk()
        ->assertJsonCount(1, 'data');
});
```

---

## Action Integration Test

```php
test('order is processed successfully', function (): void {
    $user = User::factory()->create();
    $product = Product::factory()->create(['price' => 1000]);

    $this->actingAs($user)
        ->post(route('orders.store'), [
            'product_id' => $product->id,
            'quantity' => 2,
        ])
        ->assertValid()
        ->assertRedirect(route('orders.index'));

    // Verify Action results
    $order = Order::query()->sole();

    expect($order)
        ->user_id->toBe($user->id)
        ->total->toBe(2000)
        ->status->toBe('pending');
});
```
