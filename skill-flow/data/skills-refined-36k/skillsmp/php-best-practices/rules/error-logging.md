---
title: Use PSR-3 Logger Instead of error_log
impact: HIGH
impactDescription: Structured logging with levels, context, and flexible handlers
tags: logging, psr-3, monolog, debugging
---

## Use PSR-3 Logger Instead of error_log

error_log() is primitive - no log levels, no context, no flexibility. PSR-3 loggers provide structured logging with multiple handlers and output formats.

**Incorrect (primitive logging):**

```php
<?php
// No structure or context
error_log("User login failed");
error_log("Error: " . $e->getMessage());

// String concatenation loses context
error_log("Order {$orderId} failed for user {$userId}: {$reason}");

// Can't easily filter by severity
error_log("[WARNING] Low inventory");
error_log("[ERROR] Payment failed");
```

**Correct (PSR-3 structured logging):**

```php
<?php
use Psr\Log\LoggerInterface;
use Monolog\Logger;
use Monolog\Handler\StreamHandler;
use Monolog\Handler\RotatingFileHandler;
use Monolog\Formatter\JsonFormatter;

// Configure logger
$logger = new Logger('app');

// Development: human-readable
$logger->pushHandler(new StreamHandler('php://stderr', Logger::DEBUG));

// Production: JSON for log aggregation
$productionHandler = new RotatingFileHandler('/var/log/app/app.log', 14, Logger::INFO);
$productionHandler->setFormatter(new JsonFormatter());
$logger->pushHandler($productionHandler);

// Structured logging with context
$logger->info('User logged in', [
    'user_id' => $user->id,
    'ip' => $_SERVER['REMOTE_ADDR'],
    'user_agent' => $_SERVER['HTTP_USER_AGENT']
]);

$logger->error('Payment failed', [
    'order_id' => $order->id,
    'user_id' => $user->id,
    'amount' => $order->total,
    'error' => $e->getMessage(),
    'exception' => $e
]);

$logger->warning('Rate limit approaching', [
    'user_id' => $user->id,
    'current' => $currentRate,
    'limit' => $rateLimit
]);

// Inject logger via dependency injection
class OrderService {
    public function __construct(
        private LoggerInterface $logger
    ) {}

    public function createOrder(array $data): Order {
        $this->logger->debug('Creating order', ['data' => $data]);

        try {
            $order = $this->processOrder($data);
            $this->logger->info('Order created', ['order_id' => $order->id]);
            return $order;
        } catch (Exception $e) {
            $this->logger->error('Order creation failed', [
                'exception' => $e,
                'data' => $data
            ]);
            throw $e;
        }
    }
}
```

Reference: [PSR-3 Logger Interface](https://www.php-fig.org/psr/psr-3/)
