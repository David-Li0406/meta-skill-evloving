# PHPUnit Advanced Patterns

## Data Providers

```php
<?php

namespace Tests\Unit;

use App\Services\PriceCalculator;
use PHPUnit\Framework\Attributes\DataProvider;
use PHPUnit\Framework\TestCase;

class PriceCalculatorTest extends TestCase
{
    #[DataProvider('priceData')]
    public function test_calculates_discount(float $price, int $discount, float $expected): void
    {
        $calculator = new PriceCalculator();
        
        $this->assertEquals($expected, $calculator->applyDiscount($price, $discount));
    }

    public static function priceData(): array
    {
        return [
            'no discount' => [100.00, 0, 100.00],
            '10% discount' => [100.00, 10, 90.00],
            '50% discount' => [100.00, 50, 50.00],
            '100% discount' => [100.00, 100, 0.00],
        ];
    }
}
```

## Exception Testing

```php
public function test_throws_exception_for_invalid_input(): void
{
    $this->expectException(InvalidArgumentException::class);
    $this->expectExceptionMessage('Price cannot be negative');

    $calculator = new PriceCalculator();
    $calculator->calculate(-100);
}
```

## Setup and Teardown

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class OrderWorkflowTest extends TestCase
{
    use RefreshDatabase;

    private User $user;

    protected function setUp(): void
    {
        parent::setUp();
        
        $this->user = User::factory()->create();
    }

    protected function tearDown(): void
    {
        // Cleanup if needed
        parent::tearDown();
    }

    public function test_complete_order_workflow(): void
    {
        $this->actingAs($this->user);
        // ...
    }
}
```

## HTTP Testing Helpers

```php
// Authentication
$this->actingAs($user);
$this->actingAs($user, 'api');  // Specific guard

// Headers
$response = $this->withHeaders([
    'X-Custom-Header' => 'value',
])->postJson('/api/endpoint');

// Cookies
$response = $this->withCookie('token', 'value')->get('/path');

// Session
$response = $this->withSession(['key' => 'value'])->get('/path');
```

## File Upload Testing

```php
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;

public function test_avatar_upload(): void
{
    Storage::fake('public');

    $file = UploadedFile::fake()->image('avatar.jpg', 200, 200);

    $response = $this
        ->actingAs($this->user)
        ->postJson('/api/profile/avatar', [
            'avatar' => $file,
        ]);

    $response->assertOk();

    Storage::disk('public')->assertExists('avatars/' . $file->hashName());
}
```

## Queue Testing

```php
use Illuminate\Support\Facades\Queue;
use App\Jobs\ProcessOrder;

public function test_order_dispatches_processing_job(): void
{
    Queue::fake();

    $this->actingAs($user)->postJson('/api/orders', $data);

    Queue::assertPushed(ProcessOrder::class, function ($job) use ($order) {
        return $job->order->id === $order->id;
    });
}
```

## Event Testing

```php
use Illuminate\Support\Facades\Event;
use App\Events\OrderCreated;

public function test_order_creation_dispatches_event(): void
{
    Event::fake();

    $this->actingAs($user)->postJson('/api/orders', $data);

    Event::assertDispatched(OrderCreated::class);
}
```

## Mail Testing

```php
use Illuminate\Support\Facades\Mail;
use App\Mail\OrderConfirmation;

public function test_sends_order_confirmation_email(): void
{
    Mail::fake();

    $this->actingAs($user)->postJson('/api/orders', $data);

    Mail::assertSent(OrderConfirmation::class, function ($mail) use ($user) {
        return $mail->hasTo($user->email);
    });
}
```
