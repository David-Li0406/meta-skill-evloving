---
title: Never Use eval() or Dynamic Code Execution
impact: CRITICAL
impactDescription: Prevents remote code execution vulnerabilities
tags: security, eval, injection, rce
---

## Never Use eval() or Dynamic Code Execution

eval(), create_function(), and preg_replace with /e modifier execute arbitrary code, enabling attackers to completely compromise the server.

**Incorrect (code execution vulnerabilities):**

```php
<?php
// eval() with user input - RCE vulnerability
$formula = $_GET['formula'];
eval('$result = ' . $formula . ';'); // Attacker: "1; system('rm -rf /');"

// create_function() - deprecated and dangerous
$callback = create_function('$x', 'return $x * ' . $_GET['multiplier']);

// preg_replace /e modifier - removed in PHP 7
$result = preg_replace('/(.*)/e', 'strtoupper("$1")', $input);

// Variable variables with user input
$varName = $_GET['var'];
$$varName = 'value'; // Can overwrite any variable

// Dynamic function call with user input
$func = $_GET['action'];
$func(); // Can call any function
```

**Correct (safe alternatives):**

```php
<?php
// Math expressions - use a safe parser
use MathParser\StdMathParser;
$parser = new StdMathParser();
$result = $parser->parse($_GET['formula'])->evaluate();

// Or whitelist allowed operations
function safeMath(string $expr): float {
    if (!preg_match('/^[\d\s\+\-\*\/\(\)\.]+$/', $expr)) {
        throw new InvalidArgumentException('Invalid expression');
    }
    // Still be careful - consider using a proper math library
}

// Use closures instead of create_function
$multiplier = (int)$_GET['multiplier'];
$callback = fn($x) => $x * $multiplier;

// preg_replace_callback instead of /e
$result = preg_replace_callback(
    '/(.*?)/',
    fn($matches) => strtoupper($matches[1]),
    $input
);

// Whitelist allowed function calls
$allowedActions = ['view', 'edit', 'delete'];
$action = $_GET['action'];
if (in_array($action, $allowedActions, true)) {
    $handlers[$action]();
}

// Use match/switch for dynamic behavior
match($action) {
    'view' => handleView(),
    'edit' => handleEdit(),
    default => throw new InvalidArgumentException('Unknown action')
};
```

If you think you need eval(), you almost certainly don't. Use data-driven approaches.

Reference: [PHP eval()](https://www.php.net/manual/en/function.eval.php)
