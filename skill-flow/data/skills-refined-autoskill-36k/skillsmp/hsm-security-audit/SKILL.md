---
name: HSM Security Audit
description: Comprehensive security verification - audit dependencies, check for vulnerabilities, verify constant-time ops
version: 1.0.0
tags: [hsm, security, audit]
---

# HSM Security Audit

Comprehensive security verification for HSM modules.

## Usage

```
/hsm-security [module-number]
```

## What You Do

1. **Dependency Audit:**
   ```bash
   cargo audit
   ```
   Check for CVEs in dependencies.

2. **Clippy Security Lints:**
   ```bash
   cargo clippy --all -- -D warnings
   ```
   Check for security anti-patterns, unsafe usage, potential panics.

3. **Constant-Time Operations:**
   Search for crypto operations and verify they use constant-time:
   - ✅ Uses `subtle::ConstantTimeEq`
   - ❌ Uses `==` for signature/password comparison

4. **Memory Zeroization:**
   Check sensitive types have `#[derive(Zeroize, ZeroizeOnDrop)]`
   - Private keys
   - Passwords/tokens
   - Temporary crypto buffers

5. **Secret Redaction:**
   Verify secrets never in Debug impl or logs:
   ```rust
   // ✅ Good
   impl fmt::Debug for Config {
       fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
           f.debug_struct("Config")
               .field("master_key", &"<redacted>")
               .finish()
       }
   }
   ```

6. **Input Validation:**
   Check all external inputs validated (size limits, range checks, sanitization).

7. **Generate Report:**
   Show findings with severity (Critical, High, Medium, Low) and recommendations.
