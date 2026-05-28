---
name: security-patterns
description: PHP security best practices and patterns for preventing common vulnerabilities
---

# PHP Security Patterns

Language-level security patterns for PHP, applicable to any PHP project.

## Input Validation

### Type Validation

```php
// Always validate and sanitize input
public function processUserId(mixed $input): int
{
    if (!is_numeric($input)) {
        throw new \InvalidArgumentException('User ID must be numeric');
    }

    $id = (int)$input;

    if ($id <= 0) {
        throw new \InvalidArgumentException('User ID must be positive');
    }

    return $id;
}
```

### Email Validation

```php
public function validateEmail(string $email): bool
{
    // Use built-in filter
    $filtered = filter_var($email, FILTER_VALIDATE_EMAIL);

    if ($filtered === false) {
        throw new \InvalidArgumentException('Invalid email format');
    }

    return true;
}
```

### URL Validation

```php
public function validateUrl(string $url): bool
{
    $filtered = filter_var($url, FILTER_VALIDATE_URL);

    if ($filtered === false) {
        throw new \InvalidArgumentException('Invalid URL format');
    }

    // Additional checks
    $parsed = parse_url($url);

    // Only allow http/https
    if (!in_array($parsed['scheme'] ?? '', ['http', 'https'])) {
        throw new \InvalidArgumentException('URL must use http or https');
    }

    return true;
}
```

## SQL Injection Prevention

### Use ORM Query Builder (Recommended)

```php
// ✅ CORRECT: Use ORM (CakePHP example)
public function findUserByEmail(string $email): ?User
{
    return $this->Users->find()
        ->where(['email' => $email])  // Automatically parameterized
        ->first();
}

// ✅ CORRECT: ORM with conditions array
public function findActiveUsers(int $companyId): array
{
    return $this->Users->find()
        ->where([
            'company_id' => $companyId,
            'status' => 1,
            'del_flg' => 0,
        ])
        ->toArray();
}

// ❌ WRONG: Raw SQL with string concatenation
public function findUserUnsafe(string $email): ?User
{
    $query = "SELECT * FROM users WHERE email = '" . $email . "'";  // VULNERABLE!
    return $this->getConnection()->query($query)->fetch();
}
```

### Use Query Expressions for Complex Conditions

```php
// ✅ CORRECT: Use Query expressions for complex logic
public function findUsersWithComplexCondition(string $searchTerm): array
{
    return $this->Users->find()
        ->where(function ($exp, $q) use ($searchTerm) {
            return $exp->or([
                'email LIKE' => '%' . $searchTerm . '%',
                'name LIKE' => '%' . $searchTerm . '%',
            ]);
        })
        ->toArray();
}
```

### Only Use Raw SQL When Absolutely Necessary

```php
// If raw SQL is unavoidable, ALWAYS use parameter binding
public function executeRawQuery(int $userId): array
{
    $conn = $this->getConnection();

    // ✅ CORRECT: Named parameters
    $stmt = $conn->execute(
        'SELECT * FROM users WHERE id = :id',
        ['id' => $userId],
        ['id' => 'integer']
    );

    return $stmt->fetchAll();
}

// ❌ WRONG: Never concatenate user input
public function unsafeRawQuery(string $email): array
{
    $sql = "SELECT * FROM users WHERE email = '$email'";  // VULNERABLE!
    return $this->getConnection()->execute($sql)->fetchAll();
}
```

## XSS (Cross-Site Scripting) Prevention

### Output Escaping

```php
// ✅ CORRECT: Escape output
echo htmlspecialchars($userInput, ENT_QUOTES, 'UTF-8');

// For HTML attributes
echo '<input value="' . htmlspecialchars($value, ENT_QUOTES, 'UTF-8') . '">';

// For JavaScript
echo '<script>var name = "' . json_encode($name, JSON_HEX_TAG | JSON_HEX_AMP) . '";</script>';

// For URLs
echo '<a href="' . urlencode($url) . '">Link</a>';
```

### Content Security Policy

```php
// Set CSP headers
header("Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'");
```

## CSRF (Cross-Site Request Forgery) Prevention

### Token Generation

```php
class CsrfToken
{
    public static function generate(): string
    {
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }

        $token = bin2hex(random_bytes(32));
        $_SESSION['csrf_token'] = $token;

        return $token;
    }

    public static function validate(string $token): bool
    {
        if (session_status() === PHP_SESSION_NONE) {
            session_start();
        }

        return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
    }
}
```

### Form Implementation

```php
// In form
<form method="POST">
    <input type="hidden" name="csrf_token" value="<?= CsrfToken::generate() ?>">
    <!-- Other fields -->
</form>

// In handler
if (!CsrfToken::validate($_POST['csrf_token'] ?? '')) {
    throw new SecurityException('Invalid CSRF token');
}
```

## Password Security

### Hashing

```php
// ✅ CORRECT: Use password_hash()
public function hashPassword(string $password): string
{
    return password_hash($password, PASSWORD_ARGON2ID, [
        'memory_cost' => 65536,
        'time_cost' => 4,
        'threads' => 3,
    ]);
}

// ❌ WRONG: Never use md5, sha1, or plain text
public function insecureHash(string $password): string
{
    return md5($password);  // VULNERABLE!
}
```

### Verification

```php
public function verifyPassword(string $password, string $hash): bool
{
    return password_verify($password, $hash);
}

public function needsRehash(string $hash): bool
{
    return password_needs_rehash($hash, PASSWORD_ARGON2ID, [
        'memory_cost' => 65536,
        'time_cost' => 4,
        'threads' => 3,
    ]);
}
```

## Session Security

### Secure Session Configuration

```php
// Configure secure sessions
ini_set('session.cookie_httponly', '1');
ini_set('session.cookie_secure', '1');  // HTTPS only
ini_set('session.cookie_samesite', 'Strict');
ini_set('session.use_strict_mode', '1');

// Regenerate session ID on login
session_start();
if ($loginSuccessful) {
    session_regenerate_id(true);
}
```

### Session Fixation Prevention

```php
public function login(string $username, string $password): bool
{
    if ($this->authenticate($username, $password)) {
        // Regenerate session ID to prevent fixation
        session_regenerate_id(true);

        $_SESSION['user_id'] = $userId;
        $_SESSION['last_activity'] = time();

        return true;
    }

    return false;
}
```

### Session Timeout

```php
public function checkSessionTimeout(): bool
{
    $timeout = 1800; // 30 minutes

    if (isset($_SESSION['last_activity'])) {
        if (time() - $_SESSION['last_activity'] > $timeout) {
            session_destroy();
            return false;
        }
    }

    $_SESSION['last_activity'] = time();
    return true;
}
```

## File Upload Security

### Validation

```php
public function validateUpload(array $file): bool
{
    // Check for upload errors
    if ($file['error'] !== UPLOAD_ERR_OK) {
        throw new \RuntimeException('Upload failed');
    }

    // Validate MIME type
    $allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    $finfo = finfo_open(FILEINFO_MIME_TYPE);
    $mimeType = finfo_file($finfo, $file['tmp_name']);
    finfo_close($finfo);

    if (!in_array($mimeType, $allowedTypes)) {
        throw new \InvalidArgumentException('Invalid file type');
    }

    // Validate file size (max 5MB)
    if ($file['size'] > 5 * 1024 * 1024) {
        throw new \InvalidArgumentException('File too large');
    }

    return true;
}

public function saveUpload(array $file): string
{
    $this->validateUpload($file);

    // Generate safe filename
    $extension = pathinfo($file['name'], PATHINFO_EXTENSION);
    $filename = bin2hex(random_bytes(16)) . '.' . $extension;

    // Save outside web root
    $uploadDir = '/var/uploads/';
    $destination = $uploadDir . $filename;

    if (!move_uploaded_file($file['tmp_name'], $destination)) {
        throw new \RuntimeException('Failed to save file');
    }

    return $filename;
}
```

## Directory Traversal Prevention

### Path Sanitization

```php
public function getSecurePath(string $userPath): string
{
    // Define safe base directory
    $baseDir = realpath('/var/www/uploads/');

    // Resolve user path
    $requestedPath = realpath($baseDir . '/' . $userPath);

    // Ensure path is within base directory
    if ($requestedPath === false || strpos($requestedPath, $baseDir) !== 0) {
        throw new \InvalidArgumentException('Invalid path');
    }

    return $requestedPath;
}
```

## Command Injection Prevention

### Avoid shell execution

```php
// ✅ CORRECT: Use native PHP functions
$files = scandir($directory);

// ✅ CORRECT: If shell needed, use escapeshellarg()
$filename = escapeshellarg($userFilename);
exec("ls -la " . $filename, $output);

// ❌ WRONG: Direct shell execution with user input
exec("ls -la " . $userFilename);  // VULNERABLE!
```

## XML External Entity (XXE) Prevention

### Disable external entities

```php
// ✅ CORRECT: Disable external entity loading
libxml_disable_entity_loader(true);

$dom = new DOMDocument();
$dom->loadXML($xmlString, LIBXML_NOENT | LIBXML_DTDLOAD);

// Or use SimpleXML
$xml = simplexml_load_string($xmlString, 'SimpleXMLElement', LIBXML_NOENT);
```

## Cryptographic Random Numbers

### Use secure random

```php
// ✅ CORRECT: Use random_bytes() or random_int()
$token = bin2hex(random_bytes(32));
$randomNumber = random_int(1, 100);

// ❌ WRONG: Never use rand() or mt_rand() for security
$insecureToken = mt_rand();  // VULNERABLE!
```

## HTTP Headers

### Security Headers

```php
// X-Frame-Options
header('X-Frame-Options: SAMEORIGIN');

// X-Content-Type-Options
header('X-Content-Type-Options: nosniff');

// X-XSS-Protection
header('X-XSS-Protection: 1; mode=block');

// Strict-Transport-Security (HTTPS only)
header('Strict-Transport-Security: max-age=31536000; includeSubDomains');

// Referrer-Policy
header('Referrer-Policy: strict-origin-when-cross-origin');
```

## Error Handling

### Don't expose sensitive information

```php
// ✅ CORRECT: Log detailed errors, show generic message
try {
    $this->processPayment($amount);
} catch (\Exception $e) {
    // Log full error for debugging
    error_log('Payment error: ' . $e->getMessage());

    // Show generic message to user
    throw new \RuntimeException('Payment processing failed');
}

// ❌ WRONG: Expose stack traces in production
ini_set('display_errors', '1');  // VULNERABLE in production!
```

## Framework-Agnostic

These security patterns apply to:
- CakePHP projects
- Laravel projects
- Symfony projects
- Any PHP application

Framework-specific security features (Authentication, Authorization, CSRF middleware, etc.) should be defined in framework-level skills (e.g., `php-cakephp/security-patterns`).
