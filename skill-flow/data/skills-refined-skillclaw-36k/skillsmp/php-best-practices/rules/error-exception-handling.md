---
title: Use Try-Catch for Expected Exceptions
impact: HIGH
impactDescription: Enables graceful error recovery and better user experience
tags: errors, exceptions, try-catch, handling
---

## Use Try-Catch for Expected Exceptions

Unhandled exceptions crash applications and expose error details to users. Catch exceptions where you can meaningfully handle them.

**Incorrect (unhandled exceptions):**

```php
<?php
// No error handling - exposes internals on failure
$data = json_decode(file_get_contents($url), true);
$user = $repository->find($id);
echo $user['name'];

// Catching but not handling
try {
    $result = riskyOperation();
} catch (Exception $e) {
    // Swallowed silently - debugging nightmare
}

// Catching too broadly
try {
    $user = findUser($id);
    $order = createOrder($user);
} catch (Exception $e) {
    echo "Error"; // Which operation failed?
}
```

**Correct (proper exception handling):**

```php
<?php
// Handle specific exceptions appropriately
try {
    $user = $userRepository->findOrFail($id);
} catch (NotFoundException $e) {
    return response()->notFound('User not found');
} catch (DatabaseException $e) {
    $logger->error('Database error', ['exception' => $e]);
    return response()->serverError('Service temporarily unavailable');
}

// Re-throw with context
try {
    $data = $this->fetchExternalData($url);
} catch (HttpException $e) {
    throw new DataFetchException(
        "Failed to fetch data from {$url}",
        previous: $e
    );
}

// Finally for cleanup
$connection = null;
try {
    $connection = $this->connect();
    return $connection->query($sql);
} catch (ConnectionException $e) {
    $this->logger->error('Connection failed', ['exception' => $e]);
    throw $e;
} finally {
    $connection?->close();
}

// Log and recover with default
try {
    $config = $this->loadConfig($path);
} catch (ConfigException $e) {
    $this->logger->warning('Config load failed, using defaults', [
        'path' => $path,
        'error' => $e->getMessage()
    ]);
    $config = $this->getDefaultConfig();
}
```

Only catch exceptions you can meaningfully handle. Let others bubble up.

Reference: [PHP Exceptions](https://www.php.net/manual/en/language.exceptions.php)
