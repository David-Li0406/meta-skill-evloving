# Service-Repository Pattern

## When to Use Repository

Use Repository layer when:

- Complex queries reused across multiple services
- Need to abstract database operations for testing
- Multiple data sources (API + Database)

Skip Repository when:

- Simple CRUD with Eloquent is sufficient
- Query only used in one place

## Service Layer

```php
<?php


namespace App\Services;

use App\Events\OrderCreated;
use App\Events\OrderCancelled;
use App\Models\Order;
use App\Repositories\OrderRepository;
use Illuminate\Support\Facades\DB;

final class OrderService
{
    public function __construct(
        private readonly OrderRepository $orderRepository,
        private readonly InventoryService $inventoryService,
    ) {}

    public function create(array $data): Order
    {
        return DB::transaction(function () use ($data): Order {
            // Business logic
            $this->inventoryService->reserve($data['items']);
            
            // Create via repository
            $order = $this->orderRepository->create([
                'user_id' => auth()->id(),
                'status' => OrderStatus::Pending,
                'total' => $this->calculateTotal($data['items']),
            ]);

            $order->items()->createMany($data['items']);

            // Side effects via events
            event(new OrderCreated($order));

            return $order->load('items');
        });
    }

    public function cancel(Order $order): Order
    {
        return DB::transaction(function () use ($order): Order {
            $order->update(['status' => OrderStatus::Cancelled]);
            
            $this->inventoryService->release($order->items);
            
            event(new OrderCancelled($order));

            return $order->fresh();
        });
    }

    private function calculateTotal(array $items): float
    {
        return collect($items)->sum(fn ($item) => $item['price'] * $item['quantity']);
    }
}
```

## Repository Layer

```php
<?php


namespace App\Repositories;

use App\Models\Order;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Pagination\LengthAwarePaginator;

final class OrderRepository
{
    public function create(array $data): Order
    {
        return Order::query()->create($data);
    }

    public function findById(int $id): ?Order
    {
        return Order::query()->find($id);
    }

    public function findByIdOrFail(int $id): Order
    {
        return Order::query()->findOrFail($id);
    }

    public function getForUser(int $userId, int $perPage = 15): LengthAwarePaginator
    {
        return Order::query()
            ->where('user_id', $userId)
            ->with(['items'])
            ->latest()
            ->paginate($perPage);
    }

    public function getPendingOlderThan(int $hours): Collection
    {
        return Order::query()
            ->where('status', OrderStatus::Pending)
            ->where('created_at', '<', now()->subHours($hours))
            ->get();
    }
}
```

## Binding in Service Provider

```php
// AppServiceProvider boot()
$this->app->bind(OrderRepository::class, function ($app) {
    return new OrderRepository();
});

// Or auto-resolution works for concrete classes
```

## Testing Services

```php
it('creates order with inventory reservation', function () {
    $inventoryService = Mockery::mock(InventoryService::class);
    $inventoryService->shouldReceive('reserve')->once();
    
    $service = new OrderService(
        new OrderRepository(),
        $inventoryService,
    );

    $order = $service->create([
        'items' => [
            ['product_id' => 1, 'quantity' => 2, 'price' => 10.00],
        ],
    ]);

    expect($order)->status->toBe(OrderStatus::Pending);
});
```
