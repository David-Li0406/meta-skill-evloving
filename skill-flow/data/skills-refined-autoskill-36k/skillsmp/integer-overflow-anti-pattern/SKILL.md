---
name: "integer-overflow-anti-pattern"
description: "Security anti-pattern for integer overflow vulnerabilities (CWE-190). Use when generating or reviewing code that performs arithmetic on user-controlled values, handles sizes/quantities, or calculates prices/amounts. Detects overflow in validated inputs."
---

# Integer Overflow Anti-Pattern

**Severity:** High

## Summary

Integer overflow occurs when arithmetic operations exceed the maximum value for a data type, causing values to wrap around to small or negative numbers instead of erroring. Individually valid user-controlled inputs combined in calculations create exploitable conditions. Attackers bypass security checks, trigger buffer overflows, and manipulate financial transactions through overflow exploitation.

## The Anti-Pattern

Never perform arithmetic operations on user-controlled inputs without checking for overflow. Individual input validation is insufficient.

### BAD Code Example

```c
// VULNERABLE: Individual values are checked, but their multiplication can overflow.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

void process_purchase(uint32_t quantity, uint32_t price_per_item) {
    // Both inputs are validated and seem reasonable on their own.
    if (quantity > 1000) {
        printf("Error: Quantity too high.\n");
        return;
    }
    if (price_per_item > 100000) {
        printf("Error: Price per item too high.\n");
        return;
    }

    // Attacker sets `quantity = 50000` and `price_per_item = 100000`.
    // Both might pass initial checks if those checks are weak.
    // The expected total is 5,000,000,000.
    // The maximum value for a 32-bit unsigned integer is 4,294,967,295.
    uint32_t total_cost = quantity * price_per_item; // OVERFLOW!

    // The `total_cost` wraps around to a small number (705,032,704 in this case).
    // The attacker is charged a fraction of the real price.
    printf("Charging customer: %u\n", total_cost);
    charge_customer(total_cost);
}
```

### GOOD Code Example

```c
// SECURE: Check for potential overflow before performing the multiplication.
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

void process_purchase_safe(uint32_t quantity, uint32_t price_per_item) {
    if (quantity > 1000) {
        printf("Error: Quantity too high.\n");
        return;
    }
    if (price_per_item > 100000) {
        printf("Error: Price per item too high.\n");
        return;
    }

    // Pre-condition check: before multiplying, verify if the result would exceed the maximum value.
    if (price_per_item > 0 && quantity > UINT32_MAX / price_per_item) {
        printf("Error: Potential overflow detected. Transaction cancelled.\n");
        return;
    }

    // The multiplication is now safe to perform.
    uint32_t total_cost = quantity * price_per_item;

    printf("Charging customer: %u\n", total_cost);
    charge_customer(total_cost);
}
```

### Language-Specific Examples

**Python:**
```python
# VULNERABLE: Python 3 has arbitrary precision integers, but C extensions don't
import ctypes

def allocate_buffer(width, height, bytes_per_pixel):
    # Individually valid: width=1000000, height=1000000, bytes_per_pixel=4
    # Product: 4,000,000,000,000 - may overflow in C extension
    size = width * height * bytes_per_pixel

    # When passed to C extension expecting int32:
    buffer = ctypes.create_string_buffer(size)  # Overflow in C layer!
    return buffer
```

```python
# SECURE: Check for overflow before calculation
import sys

def allocate_buffer_safe(width, height, bytes_per_pixel):
    MAX_INT32 = 2**31 - 1

    # Check multiplication won't overflow
    if height > 0 and width > MAX_INT32 // (height * bytes_per_pixel):
        raise ValueError("Buffer size would overflow")

    size = width * height * bytes_per_pixel

    if size > MAX_INT32:
        raise ValueError(f"Buffer size {size} exceeds maximum")

    buffer = ctypes.create_string_buffer(size)
    return buffer
```

**JavaScript:**
```javascript
// VULNERABLE: JavaScript numbers are 64-bit floats but lose precision
function calculateTotal(quantity, pricePerUnit) {
    // Numbers > 2^53 lose precision
    // quantity=10000000000000, pricePerUnit=100
    const total = quantity * pricePerUnit; // Precision loss!
    return total;
}
```

```javascript
// SECURE: Use BigInt for large calculations
function calculateTotalSafe(quantity, pricePerUnit) {
    const MAX_SAFE = Number.MAX_SAFE_INTEGER; // 2^53 - 1

    // Check for overflow before calculating
    if (quantity > MAX_SAFE / pricePerUnit) {
        throw new Error('Calculation would overflow safe integer range');
    }

    const total = quantity * pricePerUnit;
    return total;
}

// Or use BigInt for arbitrary precision
function calculateTotalBigInt(quantity, pricePerUnit) {
    const total = BigInt(quantity) * BigInt(pricePerUnit);
    return total;
}
```

**Java:**
```java
// VULNERABLE: Multiplication without overflow check
public long calculateTotalPrice(int quantity, int pricePerItem) {
    // Both int32, but product may overflow before promotion to long
    long total = quantity * pricePerItem; // Overflow before cast!
    return total;
}
```

```java
// SECURE: Use Math.multiplyExact or manual checks
public long calculateTotalPriceSafe(int quantity, int pricePerItem) {
    try {
        // Math.multiplyExact throws ArithmeticException on overflow
        return Math.multiplyExact(quantity, pricePerItem);
    } catch (ArithmeticException e) {
        throw new IllegalArgumentException("Price calculation overflow", e);
    }
}

// Alternative: Cast to long before multiplication
public long calculateTotalPriceSafe2(int quantity, int pricePerItem) {
    long total = (long) quantity * pricePerItem;
    if (total > Integer.MAX_VALUE) {
        throw new IllegalArgumentException("Total exceeds maximum");
    }
    return total;
}
```

## Detection

- **Audit arithmetic operations on user inputs:** Search for multiplications and additions:
  - `rg '\*|[+]' --type c --type cpp -A 2 -B 2` (C/C++)
  - `rg 'quantity.*price|amount.*rate|size.*count' -i`
  - Focus on financial calculations, memory allocations, buffer sizes
- **Find missing overflow checks:** Identify operations without pre-checks:
  - `rg '(?<!if.*)\w+\s*[*+]\s*\w+' --type c`
  - Look for calculations not preceded by validation
- **Test boundary values:** Fuzz with extreme values:
  - INT32_MAX: 2,147,483,647
  - UINT32_MAX: 4,294,967,295
  - INT64_MAX: 9,223,372,036,854,775,807
- **Use SAST tools:** Automated overflow detection:
  - CodeQL: `cpp/uncontrolled-arithmetic`
  - Clang Static Analyzer: `-analyzer-checker=security.intoverflow`
  - Semgrep rules for integer overflow patterns

## Prevention

- [ ] **Check before you calculate:** Before performing an arithmetic operation, check if it will result in an overflow. For multiplication (`a * b`), the check is `if (a > MAX_INT / b)`. For addition (`a + b`), it's `if (a > MAX_INT - b)`.
- [ ] **Use a larger data type:** If you expect large numbers, use a 64-bit integer (`long long` in C, `long` in Java) instead of a 32-bit one.
- [ ] **Use arbitrary-precision libraries:** For financial calculations where precision is critical, use a library that handles numbers of arbitrary size (e.g., `BigDecimal` in Java, `decimal` in Python).
- [ ] **Use compiler-level protections:** Some modern compilers provide flags (like `-ftrapv` in GCC/Clang) that can detect and abort on signed integer overflows.

## Related Security Patterns & Anti-Patterns

- [Missing Input Validation Anti-Pattern](../missing-input-validation/): While input validation is necessary, it is not sufficient on its own to prevent integer overflows.
- [Type Confusion Anti-Pattern](../type-confusion/): Incorrect assumptions about data types can lead to a variety of numeric vulnerabilities, including overflows.

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM10:2025 - Unbounded Consumption](https://genai.owasp.org/llmrisk/llm10-unbounded-consumption/)
- [CWE-190: Integer Overflow](https://cwe.mitre.org/data/definitions/190.html)
- [CAPEC-190: Forced Integer Overflow](https://capec.mitre.org/data/definitions/190.html)
- [PortSwigger: Logic Flaws](https://portswigger.net/web-security/logic-flaws)
- [CERT Secure Coding - Integer Security](https://wiki.sei.cmu.edu/confluence/display/c/INT32-C.+Ensure+that+operations+on+signed+integers+do+not+result+in+overflow)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
