---
title: Implement CSRF Protection for Forms
impact: CRITICAL
impactDescription: Prevents cross-site request forgery attacks
tags: security, csrf, forms, tokens
---

## Implement CSRF Protection for Forms

Without CSRF tokens, attackers can trick users into submitting malicious forms. Every state-changing form needs CSRF protection.

**Incorrect (no CSRF protection):**

```php
<?php
// Form without CSRF token
?>
<form method="POST" action="/transfer">
    <input name="amount" value="1000">
    <input name="to_account" value="12345">
    <button type="submit">Transfer</button>
</form>

<?php
// Processing without validation
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    transferMoney($_POST['amount'], $_POST['to_account']);
}
```

**Correct (CSRF protection implemented):**

```php
<?php
// Token generation and validation
class CsrfProtection {
    public static function generateToken(): string {
        if (empty($_SESSION['csrf_token'])) {
            $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
        }
        return $_SESSION['csrf_token'];
    }

    public static function validateToken(?string $token): bool {
        if (empty($_SESSION['csrf_token']) || empty($token)) {
            return false;
        }
        return hash_equals($_SESSION['csrf_token'], $token);
    }

    public static function getTokenField(): string {
        $token = htmlspecialchars(self::generateToken(), ENT_QUOTES, 'UTF-8');
        return '<input type="hidden" name="csrf_token" value="' . $token . '">';
    }
}

// Form with CSRF token
session_start();
?>
<form method="POST" action="/transfer">
    <?= CsrfProtection::getTokenField() ?>
    <input name="amount" value="1000">
    <input name="to_account" value="12345">
    <button type="submit">Transfer</button>
</form>

<?php
// Validate token before processing
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!CsrfProtection::validateToken($_POST['csrf_token'] ?? null)) {
        http_response_code(403);
        die('Invalid CSRF token');
    }

    // Safe to process
    transferMoney($_POST['amount'], $_POST['to_account']);
}
```

Also consider SameSite cookies and double-submit cookie patterns for APIs.

Reference: [OWASP CSRF Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
