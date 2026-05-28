# Unit Test Examples

Complete examples demonstrating unit test patterns.

## Contents

- [Testing Model Business Logic](#testing-model-business-logic)
- [Testing Helper Functions](#testing-helper-functions)
- [Testing Actions with Dependencies](#testing-actions-with-dependencies)
- [Testing Services](#testing-services)
- [Supplementing Feature Tests](#supplementing-feature-tests)

---

## Testing Model Business Logic

```php
<?php

declare(strict_types=1);

use App\Models\User;

test('it can determine if user is admin', function (): void {
    $admin = User::factory()->create(['role' => 'admin']);
    $user = User::factory()->create(['role' => 'user']);

    expect($admin->isAdmin())->toBeTrue()
        ->and($user->isAdmin())->toBeFalse();
});

test('it can get user full name', function (): void {
    $user = User::factory()->create([
        'first_name' => 'John',
        'last_name' => 'Doe',
    ]);

    expect($user->fullName())->toBe('John Doe');
});

test('it can check if user has verified email', function (): void {
    $verified = User::factory()->create(['email_verified_at' => now()]);
    $unverified = User::factory()->create(['email_verified_at' => null]);

    expect($verified->hasVerifiedEmail())->toBeTrue()
        ->and($unverified->hasVerifiedEmail())->toBeFalse();
});
```

---

## Testing Helper Functions

```php
<?php

declare(strict_types=1);

test('it can format currency', function (): void {
    expect(formatCurrency(1000))->toBe('$10.00')
        ->and(formatCurrency(1050))->toBe('$10.50')
        ->and(formatCurrency(0))->toBe('$0.00');
});

test('it can truncate string', function (): void {
    expect(truncate('Hello World', 5))->toBe('Hello...')
        ->and(truncate('Hello', 10))->toBe('Hello')
        ->and(truncate('', 5))->toBe('');
});

test('it can generate slug from string', function (): void {
    expect(slugify('Hello World'))->toBe('hello-world')
        ->and(slugify('Test & Demo'))->toBe('test-and-demo')
        ->and(slugify('  Spaces  '))->toBe('spaces');
});
```

---

## Testing Actions with Dependencies

```php
<?php

declare(strict_types=1);

use App\Actions\Order\ProcessOrderAction;
use App\DTOs\Order\ProcessOrderData;
use App\Models\Order;
use App\Services\PaymentGateway;
use Illuminate\Support\Facades\Event;

test('it can process order with successful payment', function (): void {
    Event::fake();

    $paymentGateway = mock(PaymentGateway::class);
    $paymentGateway->shouldReceive('charge')
        ->once()
        ->with(1000, 'tok_visa')
        ->andReturn(['id' => 'ch_123', 'status' => 'succeeded']);

    $order = Order::factory()->create(['total' => 1000]);

    $action = new ProcessOrderAction($paymentGateway);

    $result = $action->handle(ProcessOrderData::from([
        'orderId' => $order->id,
        'paymentToken' => 'tok_visa',
    ]));

    expect($result)
        ->toBeInstanceOf(Order::class)
        ->status->toBe('paid')
        ->payment_id->toBe('ch_123');

    Event::assertDispatched(OrderProcessed::class);
});

test('it throws exception when payment fails', function (): void {
    $paymentGateway = mock(PaymentGateway::class);
    $paymentGateway->shouldReceive('charge')
        ->once()
        ->andThrow(new PaymentException('Card declined'));

    $order = Order::factory()->create();

    $action = new ProcessOrderAction($paymentGateway);

    $action->handle(ProcessOrderData::from([
        'orderId' => $order->id,
        'paymentToken' => 'tok_visa',
    ]));
})->throws(PaymentException::class, 'Card declined');
```

---

## Testing Services

```php
<?php

declare(strict_types=1);

use App\Support\Localisation\Localisation;

test('it can get the ISO 15897 locale', function (): void {
    $localisation = createLocalisation();

    expect($localisation->getIso15897Locale('en-GB'))->toBe('en_GB')
        ->and($localisation->getIso15897Locale('en_GB'))->toBe('en_GB')
        ->and($localisation->getIso15897Locale('en'))->toBe('en');
});

test('it can check if a locale is supported', function (): void {
    $localisation = createLocalisation();

    expect($localisation->isSupportedLocale('en_GB'))->toBeTrue()
        ->and($localisation->isSupportedLocale('fr_FR'))->toBeTrue()
        ->and($localisation->isSupportedLocale('invalid'))->toBeFalse();
});

test('it throws an exception when setting an unsupported locale', function (): void {
    $localisation = createLocalisation();

    $localisation->setLocale('invalid');
})->throws(InvalidArgumentException::class);

function createLocalisation(): Localisation
{
    return new Localisation(
        defaultLocale: 'en_GB',
        supportedLocales: [
            'en_GB' => ['name' => 'English', 'nativeName' => 'English', 'regional' => 'en_GB'],
            'fr_FR' => ['name' => 'French', 'nativeName' => 'Francais', 'regional' => 'fr_FR'],
        ],
        request: new Request
    );
}
```

---

## Supplementing Feature Tests

Feature tests are primary, unit tests are supplementary for complex areas:

```php
// Feature test (PRIMARY) - Tests full HTTP flow
// This should ALWAYS be written first
test('new users can register with locale', function (): void {
    $this->post(route('register'), [
        'name' => 'Test',
        'email' => 'test@example.com',
        'language' => 'fr',
        'password' => 'password',
        'password_confirmation' => 'password',
    ])->assertRedirect(route('dashboard.index'));

    expect(User::query()->sole()->language)->toBe('fr_FR');
});

// Unit test (SUPPLEMENTARY) - Tests Action in isolation
// Only add this if the locale handling logic is particularly complex
test('it can register user with correct locale normalization', function (): void {
    $localisation = createLocalisation();
    $action = new RegisterUserAction($localisation);

    // Test complex edge cases harder to test via HTTP
    $user = $action->handle(RegisterData::from([
        'name' => 'Test',
        'email' => 'test@example.com',
        'language' => 'fr',
        'password' => 'password',
    ]));

    expect($user->language)->toBe('fr_FR');
});
```

**Guideline:** If you're only writing the feature test, that's often sufficient. Only add unit tests when the complexity justifies additional focused coverage.
