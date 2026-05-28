---
title: One Class, One Responsibility
impact: HIGH
impactDescription: Improves testability and maintainability
tags: architecture, solid, srp, clean-code
---

## One Class, One Responsibility

Fat controllers and models are hard to test and maintain. Extract responsibilities into focused classes.

**Incorrect (fat controller):**

```php
<?php

class OrderController extends Controller
{
    public function store(Request $request)
    {
        // ❌ Validation in controller
        $validated = $request->validate([...]);

        // ❌ Business logic in controller
        $order = new Order($validated);
        $order->total = $this->calculateTotal($validated['items']);
        $order->tax = $order->total * 0.1;
        $order->save();

        // ❌ Side effects in controller
        foreach ($validated['items'] as $item) {
            Product::find($item['id'])->decrement('stock', $item['qty']);
        }

        // ❌ Notifications in controller
        Mail::to($request->user())->send(new OrderConfirmation($order));

        // ❌ External API calls in controller
        $this->paymentGateway->charge($order->total);

        return redirect('/orders/' . $order->id);
    }
}
```

**Correct (separated responsibilities):**

```php
<?php

// Controller - HTTP handling only
class OrderController extends Controller
{
    public function __construct(
        private CreateOrderAction $createOrder
    ) {}

    public function store(StoreOrderRequest $request)
    {
        $order = $this->createOrder->execute(
            $request->user(),
            $request->validated()
        );

        return redirect()->route('orders.show', $order);
    }
}

// Form Request - Validation
class StoreOrderRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'items' => ['required', 'array', 'min:1'],
            'items.*.id' => ['required', 'exists:products,id'],
            'items.*.qty' => ['required', 'integer', 'min:1'],
        ];
    }
}

// Action - Business logic
class CreateOrderAction
{
    public function __construct(
        private OrderCalculator $calculator,
        private InventoryService $inventory,
        private PaymentService $payment
    ) {}

    public function execute(User $user, array $data): Order
    {
        return DB::transaction(function () use ($user, $data) {
            $order = Order::create([
                'user_id' => $user->id,
                'total' => $this->calculator->total($data['items']),
                'tax' => $this->calculator->tax($data['items']),
            ]);

            $this->inventory->decrementStock($data['items']);
            $this->payment->charge($user, $order->total);

            OrderCreated::dispatch($order); // Event handles notifications

            return $order;
        });
    }
}
```

**Benefits:**

- Controllers are thin and testable
- Business logic is reusable
- Each class has one reason to change
- Easy to mock dependencies in tests

Reference: [Single Responsibility Principle](https://laravel.com/docs/controllers)
