---
title: Inject Dependencies Instead of Creating Inside
impact: MEDIUM
impactDescription: Enables testing, flexibility, and loose coupling
tags: oop, dependency-injection, testing, solid
---

## Inject Dependencies Instead of Creating Inside

Creating dependencies inside classes creates tight coupling, making testing impossible and changes expensive. Inject dependencies through constructors.

**Incorrect (hard-coded dependencies):**

```php
<?php
class OrderService {
    private $repository;
    private $mailer;
    private $logger;

    public function __construct() {
        // Hard-coded dependencies - untestable
        $this->repository = new MySqlOrderRepository();
        $this->mailer = new SmtpMailer('smtp.example.com');
        $this->logger = new FileLogger('/var/log/orders.log');
    }

    public function createOrder(array $data): Order {
        // Can't test without real database and email server
        $order = new Order($data);
        $this->repository->save($order);
        $this->mailer->send($order->userEmail, 'Order confirmed');
        $this->logger->info('Order created: ' . $order->id);
        return $order;
    }
}

// Singleton - global state nightmare
class Database {
    private static $instance;

    public static function getInstance(): Database {
        if (self::$instance === null) {
            self::$instance = new Database();
        }
        return self::$instance;
    }
}
```

**Correct (dependency injection):**

```php
<?php
declare(strict_types=1);

// Dependencies injected through constructor
final class OrderService {
    public function __construct(
        private OrderRepositoryInterface $repository,
        private MailerInterface $mailer,
        private LoggerInterface $logger
    ) {}

    public function createOrder(array $data): Order {
        $order = new Order($data);
        $this->repository->save($order);
        $this->mailer->send($order->userEmail, 'Order confirmed');
        $this->logger->info('Order created', ['order_id' => $order->id]);
        return $order;
    }
}

// Easy to test with mocks
final class OrderServiceTest extends TestCase {
    public function testCreateOrder(): void {
        $repository = $this->createMock(OrderRepositoryInterface::class);
        $repository->expects($this->once())->method('save');

        $mailer = $this->createMock(MailerInterface::class);
        $mailer->expects($this->once())->method('send');

        $logger = new NullLogger();

        $service = new OrderService($repository, $mailer, $logger);
        $order = $service->createOrder(['product_id' => 1]);

        $this->assertInstanceOf(Order::class, $order);
    }
}

// Container configuration
$container->set(OrderService::class, function($c) {
    return new OrderService(
        $c->get(OrderRepositoryInterface::class),
        $c->get(MailerInterface::class),
        $c->get(LoggerInterface::class)
    );
});
```

Use a DI container (PHP-DI, Symfony DI, Laravel's container) to manage object graphs.

Reference: [PHP-DI](https://php-di.org/)
