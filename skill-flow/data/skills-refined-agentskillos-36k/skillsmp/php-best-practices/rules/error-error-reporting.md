---
title: Configure Appropriate Error Reporting Levels
impact: HIGH
impactDescription: Catches bugs in development, hides details in production
tags: errors, reporting, debugging, production
---

## Configure Appropriate Error Reporting Levels

Development needs verbose errors for debugging. Production needs silent logging to prevent information disclosure. Configure error reporting appropriately.

**Incorrect (same config everywhere):**

```php
<?php
// Errors visible in production - security risk
error_reporting(E_ALL);
ini_set('display_errors', '1');

// Or errors hidden in development - bugs go unnoticed
error_reporting(0);
ini_set('display_errors', '0');

// Suppressing errors with @ operator
$data = @file_get_contents($file); // Hides problems
```

**Correct (environment-appropriate configuration):**

```php
<?php
// Development - show everything
if (getenv('APP_ENV') === 'development') {
    error_reporting(E_ALL);
    ini_set('display_errors', '1');
    ini_set('display_startup_errors', '1');
}

// Production - log but don't display
if (getenv('APP_ENV') === 'production') {
    error_reporting(E_ALL);
    ini_set('display_errors', '0');
    ini_set('display_startup_errors', '0');
    ini_set('log_errors', '1');
    ini_set('error_log', '/var/log/php/error.log');
}

// Custom error handler
set_error_handler(function (
    int $severity,
    string $message,
    string $file,
    int $line
): bool {
    // Convert errors to exceptions
    throw new ErrorException($message, 0, $severity, $file, $line);
});

// Custom exception handler
set_exception_handler(function (Throwable $e): void {
    // Log the full exception
    error_log($e->getMessage() . "\n" . $e->getTraceAsString());

    // Show generic error to user in production
    if (getenv('APP_ENV') === 'production') {
        http_response_code(500);
        echo 'An error occurred. Please try again later.';
    } else {
        // Show details in development
        echo "<pre>" . htmlspecialchars($e) . "</pre>";
    }
});

// Instead of @ operator, handle explicitly
$data = file_get_contents($file);
if ($data === false) {
    throw new FileReadException("Could not read file: {$file}");
}
```

Use a logging library (Monolog) for production error tracking.

Reference: [PHP Error Reporting](https://www.php.net/manual/en/function.error-reporting.php)
