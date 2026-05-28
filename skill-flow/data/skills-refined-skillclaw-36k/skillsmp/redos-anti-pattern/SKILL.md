---
name: "redos-anti-pattern"
description: "Security anti-pattern for Regular Expression Denial of Service (CWE-1333). Use when generating or reviewing code that uses regex for input validation, parsing, or pattern matching. Detects catastrophic backtracking patterns with nested quantifiers."
---

# ReDoS (Regular Expression Denial of Service) Anti-Pattern

**Severity:** High

## Summary

Poorly written regex patterns take extremely long to evaluate malicious input, causing applications to hang and consume 100% CPU from a single request. Caused by catastrophic backtracking in patterns with nested quantifiers (`(a+)+`) or overlapping alternations.

## The Anti-Pattern

The anti-pattern is regex with exponential-time complexity for input validation. Small input length increases cause exponential computation time growth.

### BAD Code Example

```javascript
// VULNERABLE: Nested quantifiers cause catastrophic backtracking.

// Validates string of 'a's followed by 'b'.
// `(a+)+` is the "evil" pattern creating catastrophic backtracking.
const VULNERABLE_REGEX = /^(a+)+b$/;

function validateString(input) {
    console.time('Regex Execution');
    const result = VULNERABLE_REGEX.test(input);
    console.timeEnd('Regex Execution');
    return result;
}

// Normal: validateString("aaab"); // -> true, < 1ms

// Attack: string that almost matches
const malicious_input = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaab"; // 30 'a's + 'b'

// `(a+)+` matches 'a's in exponential ways.
// "aaa" → (a)(a)(a), (aa)(a), (a)(aa), (aaa)
// Engine tries all combinations.
// 30 'a's → over 1 billion backtracking steps, freezing process.
validateString(malicious_input); // Hangs for very long time.
```

### GOOD Code Example

```javascript
// SECURE: Linear-time regex or add controls.

// Option 1 (Best): Remove nested quantifier.
// Functionally identical, linear-time complexity.
const SAFE_REGEX = /^a+b$/;

function validateStringSafe(input) {
    console.time('Regex Execution');
    // Fails almost instantly for malicious input.
    const result = SAFE_REGEX.test(input);
    console.timeEnd('Regex Execution');
    return result;
}

// Option 2: Input length limit (defense-in-depth).
const MAX_LENGTH = 50;
function validateStringWithLimit(input) {
    if (input.length > MAX_LENGTH) {
        throw new Error("Input exceeds maximum length.");
    }
    // Prefer safe regex, but this provides fallback.
    return VULNERABLE_REGEX.test(input);
}

// Option 3: Use ReDoS-safe engine (Google RE2)
// Guarantees linear-time, avoids catastrophic backtracking.
```

## Detection

- **Scan for "evil" regex patterns:** The most common red flags are nested quantifiers. Look for patterns like:
  - `(a+)+`
  - `(a*)*`
  - `(a|a)+`
  - `(a?)*`
- **Look for alternations with overlapping patterns:** `(a|b)*` is safe, but `(a|ab)*` is not, because `ab` can be matched in two different ways.
- **Use static analysis tools:** There are many linters and security scanners that are specifically designed to detect vulnerable regular expressions in your code (e.g., `safe-regex` for Node.js).
- **Test with "almost matching" strings:** To test a regex, create a long string that matches the repeating part of the pattern but fails at the very end. If the execution time increases dramatically with the length of the string, it is likely vulnerable.

## Prevention

- [ ] **Avoid nested quantifiers:** Most important rule. Rewrite `(a+)+` as `a+`.
- [ ] **Avoid overlapping alternations:** Use `(a|b)` not `(a|ab)` within repeated groups.
- [ ] **Limit input length:** Validate input length before complex regex. Caps execution time (crude but effective defense).
- [ ] **Use timeouts:** Regex match timeouts prevent indefinite freezing (doesn't fix underlying vulnerability).
- [ ] **Use ReDoS-safe engines:** Google RE2 guarantees linear-time, immune to catastrophic backtracking.

## Related Security Patterns & Anti-Patterns

- [Missing Input Validation Anti-Pattern](../missing-input-validation/): Failing to limit input length is a form of missing validation that makes ReDoS attacks possible.
- [Denial of Service (DoS):](../#) ReDoS is a specific type of application-layer DoS attack.

## References

- [OWASP Top 10 A06:2025 - Insecure Design](https://owasp.org/Top10/2025/A06_2025-Insecure_Design/)
- [OWASP GenAI LLM10:2025 - Unbounded Consumption](https://genai.owasp.org/llmrisk/llm10-unbounded-consumption/)
- [OWASP API Security API4:2023 - Unrestricted Resource Consumption](https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/)
- [OWASP ReDoS](https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS)
- [CWE-1333: Inefficient Regular Expression](https://cwe.mitre.org/data/definitions/1333.html)
- [CAPEC-492: Regular Expression Exponential Blowup](https://capec.mitre.org/data/definitions/492.html)
- [safe-regex npm package](https://www.npmjs.com/package/safe-regex)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
