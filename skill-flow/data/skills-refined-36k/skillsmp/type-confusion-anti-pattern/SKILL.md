---
name: "type-confusion-anti-pattern"
description: "Security anti-pattern for type confusion vulnerabilities (CWE-843). Use when generating or reviewing code in dynamic languages that compares values, processes JSON/user input, or uses loose equality. Detects weak typing exploits and type coercion attacks."
---

# Type Confusion Anti-Pattern

**Severity:** High

## Summary

Programs misinterpret data types through loose comparisons, implicit coercion, or improper input handling. Attackers exploit type confusion in weakly-typed languages (JavaScript, PHP) and dynamic data structures (JSON) to bypass security checks, manipulate logic, or achieve code execution.

## The Anti-Pattern

The anti-pattern is using loose equality (`==`) or trusting incoming data types without explicit validation.

### BAD Code Example

```javascript
// VULNERABLE: Loose equality comparison in authentication.

function checkAdminAccess(userId) {
    // Expected: userId is string "123".
    // Attacker input: userId is number 0.
    // JavaScript: "0" == 0 evaluates to true (type coercion).
    if (userId == 0) { // Loose equality
        return true; // Grants admin access if userId is "0" or 0.
    }
    return false;
}

// Scenario 1: userId = "0" (string) gains admin access.
// Scenario 2: userId = 0 (number) bypasses the check.

// PHP example: "0e12345" == "0e56789" (both evaluate to 0).
// If password hash starts with "0e", attacker provides another
// hash starting with "0e" to bypass authentication.
```

### GOOD Code Example

```javascript
// SECURE: Strict equality and explicit type validation.

// Option 1: Strict equality (===) checks both value AND type.
function checkAdminAccessSecure(userId) {
    // "0" === 0 evaluates to false.
    if (userId === 0) {
        return true;
    }
    return false;
}

// Option 2: Explicitly validate input type.
function processProductId(productId) {
    // Ensure productId is string matching expected format.
    if (typeof productId !== 'string' || !/^\d+$/.test(productId)) {
        throw new Error("Invalid product ID format.");
    }
    // Safe to use productId with known type and format.
    return parseInt(productId, 10);
}
```

## Detection

- **Code Review:**
  - **Loose equality operators:** Search for `==` in JavaScript or PHP code (prefer `===`).
  - **Implicit type conversions:** Look for contexts where a variable of one type might be implicitly converted to another, especially when performing comparisons or operations.
  - **Dynamic language features:** Be cautious with how user-provided data is used in contexts where the language might automatically infer or coerce types.
- **Input Validation:** Check if all incoming user input (JSON body, query parameters, form data) is explicitly validated for its expected data type *before* being processed.
- **Dynamic Queries:** Review code that constructs queries for NoSQL databases (like MongoDB) or other systems using user input. Attackers can often inject operators (`$gt`, `$ne`) by changing the input's type from a string to an object.

## Prevention

- [ ] **Use strict equality:** In JavaScript/PHP, always use `===` instead of `==`.
- [ ] **Validate input types explicitly:** Check and enforce expected types before using user data. Safely convert integers and validate ranges.
- [ ] **Use schema validation:** For JSON APIs, use validation libraries (JSON Schema, Joi, Pydantic) that strictly enforce types and formats.
- [ ] **Protect NoSQL queries:** Avoid embedding user-controlled objects in queries. Sanitize or allowlist specific field-value pairs to prevent operator injection.
- [ ] **Understand language type juggling:** Know how your language handles type conversions and stay vigilant where this enables exploits.

## Related Security Patterns & Anti-Patterns

- [Missing Input Validation Anti-Pattern](../missing-input-validation/): Type validation is a fundamental part of comprehensive input validation.
- [Integer Overflow Anti-Pattern](../integer-overflow/): A specific type of numeric issue that can arise from unexpected type handling.
- [NoSQL Injection:](../#) Type confusion is a common vector for exploiting NoSQL databases.

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM05:2025 - Improper Output Handling](https://genai.owasp.org/llmrisk/llm05-improper-output-handling/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [CWE-843: Access of Resource Using Incompatible Type](https://cwe.mitre.org/data/definitions/843.html)
- [CAPEC-153: Input Data Manipulation](https://capec.mitre.org/data/definitions/153.html)
- [PHP Type Juggling (OWASP)](https://owasp.org/www-pdf-archive/PHPMagicTricks-TypeJuggling.pdf)
- [NoSQL Injection Testing (OWASP)](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.6-Testing_for_NoSQL_Injection)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
