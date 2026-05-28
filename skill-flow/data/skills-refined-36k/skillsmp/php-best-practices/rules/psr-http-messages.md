---
title: Use PSR-7 for HTTP Message Handling
impact: MEDIUM
impactDescription: Framework-agnostic HTTP abstractions
tags: psr, http, messages, middleware
---

## Use PSR-7 for HTTP Message Handling

Direct use of superglobals ($_GET, $_POST) couples code to PHP's environment. PSR-7 provides immutable HTTP message interfaces that work with any framework.

**Incorrect (superglobal dependency):**

```php
<?php
// Tightly coupled to superglobals
function handleRequest() {
    $method = $_SERVER['REQUEST_METHOD'];
    $path = $_SERVER['REQUEST_URI'];
    $body = file_get_contents('php://input');
    $contentType = $_SERVER['HTTP_CONTENT_TYPE'] ?? '';

    // Hard to test without mocking globals
    if ($method === 'POST' && $path === '/users') {
        $data = json_decode($body, true);
        // ...
    }

    // Setting response directly
    header('Content-Type: application/json');
    echo json_encode(['success' => true]);
}
```

**Correct (PSR-7 HTTP messages):**

```php
<?php
declare(strict_types=1);

use Psr\Http\Message\RequestInterface;
use Psr\Http\Message\ResponseInterface;
use Psr\Http\Message\ServerRequestInterface;
use Psr\Http\Server\RequestHandlerInterface;
use Nyholm\Psr7\Response;

final class CreateUserHandler implements RequestHandlerInterface
{
    public function __construct(
        private UserService $userService
    ) {
    }

    public function handle(ServerRequestInterface $request): ResponseInterface
    {
        // Access request data through interface
        $body = $request->getParsedBody();
        $contentType = $request->getHeaderLine('Content-Type');

        // Query parameters
        $params = $request->getQueryParams();

        // Uploaded files
        $files = $request->getUploadedFiles();

        // Request attributes (set by middleware)
        $userId = $request->getAttribute('user_id');

        try {
            $user = $this->userService->create($body);

            return new Response(
                status: 201,
                headers: ['Content-Type' => 'application/json'],
                body: json_encode(['id' => $user->id])
            );
        } catch (ValidationException $e) {
            return new Response(
                status: 400,
                headers: ['Content-Type' => 'application/json'],
                body: json_encode(['error' => $e->getMessage()])
            );
        }
    }
}

// Easy to test
final class CreateUserHandlerTest extends TestCase
{
    public function testCreateUser(): void
    {
        $request = (new ServerRequest('POST', '/users'))
            ->withParsedBody(['name' => 'Alice', 'email' => 'alice@example.com']);

        $handler = new CreateUserHandler($this->userService);
        $response = $handler->handle($request);

        $this->assertEquals(201, $response->getStatusCode());
    }
}
```

Use Nyholm/psr7 or Guzzle for PSR-7 implementations.

Reference: [PSR-7](https://www.php-fig.org/psr/psr-7/)
