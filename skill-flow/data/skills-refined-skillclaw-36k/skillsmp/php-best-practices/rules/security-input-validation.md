---
title: Validate All Input with filter_var()
impact: CRITICAL
impactDescription: Prevents injection attacks and data corruption
tags: security, validation, filter, input
---

## Validate All Input with filter_var()

User input is untrusted by default. Always validate and sanitize input before use to prevent injection attacks and data integrity issues.

**Incorrect (trusting user input):**

```php
<?php
// Direct use of user input
$email = $_POST['email'];
$userId = $_GET['id'];

// SQL injection vulnerability
$query = "SELECT * FROM users WHERE id = $userId";

// XSS vulnerability
echo "Welcome, " . $_POST['name'];
```

**Correct (validated input):**

```php
<?php
// Validate email
$email = filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL);
if ($email === false) {
    throw new ValidationException('Invalid email address');
}

// Validate integer
$userId = filter_var($_GET['id'] ?? '', FILTER_VALIDATE_INT);
if ($userId === false) {
    throw new ValidationException('Invalid user ID');
}

// Sanitize string input
$name = filter_var($_POST['name'] ?? '', FILTER_SANITIZE_SPECIAL_CHARS);

// Validate URL
$url = filter_var($_POST['website'] ?? '', FILTER_VALIDATE_URL);

// Validate with options
$age = filter_var($_POST['age'] ?? '', FILTER_VALIDATE_INT, [
    'options' => ['min_range' => 0, 'max_range' => 150]
]);

// Custom validation with filter callback
$username = filter_var($_POST['username'] ?? '', FILTER_CALLBACK, [
    'options' => function($value) {
        return preg_match('/^[a-zA-Z0-9_]{3,20}$/', $value) ? $value : false;
    }
]);
```

Never trust input from $_GET, $_POST, $_REQUEST, $_COOKIE, or any external source.

Reference: [PHP filter_var](https://www.php.net/manual/en/function.filter-var.php)
