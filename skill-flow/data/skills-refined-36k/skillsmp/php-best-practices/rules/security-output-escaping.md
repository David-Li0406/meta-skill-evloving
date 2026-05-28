---
title: Escape Output Based on Context
impact: CRITICAL
impactDescription: Prevents XSS attacks in HTML, JavaScript, and other contexts
tags: security, xss, escaping, output
---

## Escape Output Based on Context

Different output contexts (HTML, JavaScript, URLs, CSS) require different escaping strategies. Using the wrong escape function leaves XSS vulnerabilities.

**Incorrect (no escaping or wrong context):**

```php
<?php
// No escaping - XSS vulnerability
echo "<p>Welcome, " . $userName . "</p>";

// Wrong context - htmlspecialchars doesn't work in JS
echo "<script>var name = '" . htmlspecialchars($name) . "';</script>";

// Incomplete escaping
echo '<a href="' . $url . '">Link</a>';
```

**Correct (context-appropriate escaping):**

```php
<?php
// HTML context
echo "<p>Welcome, " . htmlspecialchars($userName, ENT_QUOTES, 'UTF-8') . "</p>";

// HTML attribute context
echo '<input value="' . htmlspecialchars($value, ENT_QUOTES, 'UTF-8') . '">';

// JavaScript context - use JSON encoding
echo '<script>var data = ' . json_encode($data, JSON_HEX_TAG | JSON_HEX_AMP) . ';</script>';

// URL context
echo '<a href="/user/' . rawurlencode($userId) . '">Profile</a>';

// URL with query parameters
$url = '/search?' . http_build_query(['q' => $searchTerm]);
echo '<a href="' . htmlspecialchars($url, ENT_QUOTES, 'UTF-8') . '">Search</a>';

// CSS context (avoid user input in CSS when possible)
$safeColor = preg_match('/^#[0-9A-Fa-f]{6}$/', $color) ? $color : '#000000';
echo '<div style="color: ' . $safeColor . ';">';

// Helper function for HTML
function e(string $string): string {
    return htmlspecialchars($string, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}
echo "<p>" . e($userInput) . "</p>";
```

Always escape at the point of output, not at input time.

Reference: [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
