# Horizon Advanced

## Job Tags

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Bus\Queueable;

class ProcessOrder implements ShouldQueue
{
    use Queueable;

    public function __construct(
        public Order $order
    ) {}

    /**
     * Get the tags for Horizon dashboard filtering.
     *
     * @return array<string>
     */
    public function tags(): array
    {
        return [
            'order:' . $this->order->id,
            'user:' . $this->order->user_id,
        ];
    }
}
```

## Job Batches

```php
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;

$batch = Bus::batch([
    new ProcessOrder($order1),
    new ProcessOrder($order2),
    new ProcessOrder($order3),
])
->then(function (Batch $batch) {
    // All jobs completed successfully
})
->catch(function (Batch $batch, Throwable $e) {
    // First job failure
})
->finally(function (Batch $batch) {
    // Batch completed (success or failure)
})
->name('Process Weekend Orders')
->dispatch();

// Check batch status
$batch = Bus::findBatch($batchId);
$batch->progress();       // 0-100
$batch->finished();       // boolean
$batch->cancelled();      // boolean
```

## Rate Limiting

```php
<?php

namespace App\Jobs;

use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\Middleware\RateLimited;

class CallExternalApi implements ShouldQueue
{
    /**
     * Get the middleware for the job.
     *
     * @return array<object>
     */
    public function middleware(): array
    {
        return [new RateLimited('external-api')];
    }
}

// In AppServiceProvider
RateLimiter::for('external-api', function (object $job) {
    return Limit::perMinute(60);
});
```

## Supervisor Configuration

```ini
# /etc/supervisor/conf.d/horizon.conf
[program:horizon]
process_name=%(program_name)s
command=php /var/www/app/artisan horizon
autostart=true
autorestart=true
user=www-data
redirect_stderr=true
stdout_logfile=/var/www/app/storage/logs/horizon.log
stopwaitsecs=3600

# Reload supervisor
supervisorctl reread
supervisorctl update
supervisorctl start horizon
```

## Metrics and Monitoring

```php
// Dashboard access control
// app/Providers/HorizonServiceProvider.php
protected function gate(): void
{
    Gate::define('viewHorizon', function (User $user) {
        return $user->isAdmin();
    });
}
```

## Failed Jobs

```bash
# List failed jobs
php artisan queue:failed

# Retry failed job
php artisan queue:retry <id>

# Retry all failed
php artisan queue:retry all

# Delete failed job
php artisan queue:forget <id>

# Delete all failed
php artisan queue:flush
```
