---
title: Write Feature Tests for User Journeys
impact: MEDIUM
impactDescription: Ensures critical flows work end-to-end
tags: testing, feature-tests, phpunit, http
---

## Write Feature Tests for User Journeys

Unit tests verify isolated components. Feature tests verify that entire user flows work correctly through the HTTP layer.

**Incorrect (only unit tests):**

```php
<?php

// Only testing isolated methods
class OrderCalculatorTest extends TestCase
{
    public function test_calculates_total()
    {
        $calc = new OrderCalculator();
        $this->assertEquals(100, $calc->total([...]));
    }
}

// ❌ Doesn't test: routing, middleware, validation,
// database persistence, events, notifications...
```

**Correct (feature tests for flows):**

```php
<?php

class OrderCreationTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_create_order()
    {
        // Arrange
        $user = User::factory()->create();
        $product = Product::factory()->create(['stock' => 10]);

        // Act
        $response = $this->actingAs($user)
            ->postJson('/api/orders', [
                'items' => [
                    ['product_id' => $product->id, 'quantity' => 2],
                ],
            ]);

        // Assert HTTP response
        $response->assertCreated()
            ->assertJsonStructure([
                'data' => ['id', 'total', 'items'],
            ]);

        // Assert database state
        $this->assertDatabaseHas('orders', [
            'user_id' => $user->id,
        ]);

        // Assert side effects
        $this->assertEquals(8, $product->fresh()->stock);
    }

    public function test_guest_cannot_create_order()
    {
        $response = $this->postJson('/api/orders', [
            'items' => [...],
        ]);

        $response->assertUnauthorized();
    }

    public function test_validation_rejects_invalid_data()
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)
            ->postJson('/api/orders', [
                'items' => [], // Empty items
            ]);

        $response->assertUnprocessable()
            ->assertJsonValidationErrors(['items']);
    }
}
```

**Testing with events and jobs:**

```php
<?php

public function test_order_created_dispatches_event()
{
    Event::fake([OrderCreated::class]);

    $user = User::factory()->create();
    $this->actingAs($user)->postJson('/api/orders', [...]);

    Event::assertDispatched(OrderCreated::class, function ($event) use ($user) {
        return $event->order->user_id === $user->id;
    });
}

public function test_order_queues_notification_job()
{
    Queue::fake();

    $user = User::factory()->create();
    $this->actingAs($user)->postJson('/api/orders', [...]);

    Queue::assertPushed(SendOrderConfirmation::class);
}
```

Reference: [HTTP Tests](https://laravel.com/docs/http-tests)
