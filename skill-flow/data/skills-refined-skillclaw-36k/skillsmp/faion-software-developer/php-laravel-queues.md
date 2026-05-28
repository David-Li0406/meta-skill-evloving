---
id: php-laravel-queues
name: "Laravel Queues"
domain: PHP
skill: faion-software-developer
category: "backend"
---

## Laravel Queues

### Problem
Process background tasks asynchronously.

### Framework: Job Structure

```php
<?php
// app/Jobs/ProcessOrderJob.php

namespace App\Jobs;

use App\Models\Order;
use App\Services\OrderProcessor;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Queue\Middleware\WithoutOverlapping;
use Throwable;

class ProcessOrderJob implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $backoff = 60;
    public int $timeout = 120;

    public function __construct(
        public readonly Order $order
    ) {}

    public function middleware(): array
    {
        return [
            new WithoutOverlapping($this->order->id),
        ];
    }

    public function handle(OrderProcessor $processor): void
    {
        if ($this->order->isProcessed()) {
            return;
        }

        $processor->process($this->order);

        NotifyCustomerJob::dispatch($this->order)
            ->onQueue('notifications');
    }

    public function failed(Throwable $exception): void
    {
        $this->order->update(['status' => 'failed']);

        \Log::error('Order processing failed', [
            'order_id' => $this->order->id,
            'error' => $exception->getMessage(),
        ]);
    }

    public function retryUntil(): \DateTime
    {
        return now()->addHours(24);
    }
}

// Dispatch
ProcessOrderJob::dispatch($order)->onQueue('orders');
ProcessOrderJob::dispatch($order)->delay(now()->addMinutes(10));
```

### Job Batching

```php
<?php
// app/Jobs/ExportUsersJob.php

namespace App\Jobs;

use App\Models\User;
use Illuminate\Bus\Batchable;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Bus;

class ExportUsersJob implements ShouldQueue
{
    use Batchable, Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        public readonly array $userIds,
        public readonly string $filePath
    ) {}

    public function handle(): void
    {
        if ($this->batch()->cancelled()) {
            return;
        }

        $users = User::whereIn('id', $this->userIds)->get();

        // Process chunk...
    }
}

// Create batch
$batch = Bus::batch([
    new ExportUsersJob($chunk1, $path),
    new ExportUsersJob($chunk2, $path),
    new ExportUsersJob($chunk3, $path),
])
->then(function ($batch) {
    // All jobs completed successfully
})
->catch(function ($batch, $e) {
    // First batch job failure
})
->finally(function ($batch) {
    // Batch finished (success or failure)
})
->name('Export Users')
->dispatch();
```

### Agent

faion-backend-agent
