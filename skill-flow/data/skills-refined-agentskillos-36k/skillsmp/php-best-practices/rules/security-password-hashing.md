---
title: Use password_hash() with PASSWORD_DEFAULT
impact: CRITICAL
impactDescription: Ensures secure password storage with automatic algorithm updates
tags: security, passwords, hashing, bcrypt
---

## Use password_hash() with PASSWORD_DEFAULT

Never store plain text passwords or use weak hashing algorithms. password_hash() with PASSWORD_DEFAULT automatically uses the strongest available algorithm.

**Incorrect (insecure password storage):**

```php
<?php
// Plain text - catastrophic
$password = $_POST['password'];
$query = "INSERT INTO users (password) VALUES ('$password')";

// MD5/SHA1 - easily cracked
$hash = md5($password);
$hash = sha1($password);

// Single iteration - too fast
$hash = hash('sha256', $password);

// Hardcoded algorithm that becomes outdated
$hash = password_hash($password, PASSWORD_BCRYPT);
```

**Correct (secure password handling):**

```php
<?php
// Hash password with automatic algorithm selection
$password = $_POST['password'];
$hash = password_hash($password, PASSWORD_DEFAULT);
// Stores hash like: $2y$10$... (bcrypt) or $argon2id$... (future)

// Store only the hash in database
$stmt = $pdo->prepare("INSERT INTO users (password_hash) VALUES (?)");
$stmt->execute([$hash]);

// Verify password
function verifyPassword(string $password, string $hash): bool {
    return password_verify($password, $hash);
}

// Check if rehash is needed (algorithm upgraded)
function checkAndRehash(string $password, string $hash, PDO $pdo, int $userId): string {
    if (password_needs_rehash($hash, PASSWORD_DEFAULT)) {
        $newHash = password_hash($password, PASSWORD_DEFAULT);
        $stmt = $pdo->prepare("UPDATE users SET password_hash = ? WHERE id = ?");
        $stmt->execute([$newHash, $userId]);
        return $newHash;
    }
    return $hash;
}

// Complete login flow
function login(string $email, string $password, PDO $pdo): ?array {
    $stmt = $pdo->prepare("SELECT id, password_hash FROM users WHERE email = ?");
    $stmt->execute([$email]);
    $user = $stmt->fetch();

    if (!$user || !password_verify($password, $user['password_hash'])) {
        return null; // Don't reveal which was wrong
    }

    checkAndRehash($password, $user['password_hash'], $pdo, $user['id']);
    return $user;
}
```

PASSWORD_DEFAULT ensures your app automatically uses better algorithms as PHP adds them.

Reference: [PHP Password Hashing](https://www.php.net/manual/en/function.password-hash.php)
