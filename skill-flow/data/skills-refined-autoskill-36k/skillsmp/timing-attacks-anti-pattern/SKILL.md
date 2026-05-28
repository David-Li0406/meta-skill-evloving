---
name: "timing-attacks-anti-pattern"
description: "Security anti-pattern for timing side-channel vulnerabilities (CWE-208). Use when generating or reviewing code that compares secrets, tokens, passwords, or cryptographic values. Detects early-exit comparisons that leak information through timing differences."
---

# Timing Attacks Anti-Pattern

**Severity:** Medium

## Summary

Attackers measure operation timing to extract secrets. Early-exit comparisons leak information: comparing `ABCDEF` to `ABCDEG` takes longer than `ABCDEF` to `XBCDEF` (more matching characters before mismatch). These timing differences enable character-by-character secret recovery.

## The Anti-Pattern

The anti-pattern is comparison functions returning early upon finding differences in sensitive values (passwords, tokens, hashes).

### BAD Code Example

```python
# VULNERABLE: String comparison leaking timing information.

def insecure_compare(s1, s2):
    # Exits on first mismatch (early exit).
    # First character mismatch returns quickly.
    # Last character mismatch takes longer.
    if len(s1) != len(s2):
        return False
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            return False # Early exit leaks timing.
    return True

SECRET_TOKEN = "abcdef123456"

@app.route("/check_token")
def check_token():
    provided_token = request.args.get("token")
    if insecure_compare(provided_token, SECRET_TOKEN):
        return "Token valid!"
    return "Token invalid!"

# Attack: Measure response times to discover secret character-by-character.
# token=X -> fast (first char wrong)
# token=a -> slower (first char matches)
# token=ab -> even slower (two chars match)
```

### GOOD Code Example

```python
# SECURE: Constant-time comparison prevents timing leaks.
import hmac
import secrets

def secure_compare(s1_bytes, s2_bytes):
    # `hmac.compare_digest` performs constant-time comparison.
    # Execution time depends only on length, not values.
    # Always compares all bytes.
    return hmac.compare_digest(s1_bytes, s2_bytes)

SECRET_TOKEN = secrets.token_bytes(16) # Secure 128-bit token.

@app.route("/check_token_secure")
def check_token_secure():
    provided_token_hex = request.args.get("token")
    try:
        provided_token_bytes = bytes.fromhex(provided_token_hex)
    except ValueError:
        return "Token invalid!", 400

    # Length check handled safely by compare_digest.
    if len(provided_token_bytes) != len(SECRET_TOKEN):
        return "Token invalid!", 400

    if secure_compare(provided_token_bytes, SECRET_TOKEN):
        return "Token valid!"
    return "Token invalid!"
```

## Detection

- **Review code for secret comparisons:** Look for any place in the code where sensitive values (passwords, API keys, session tokens, cryptographic hashes, HMAC signatures) are compared.
- **Identify standard equality operators:** Search for `==` or `===` being used for comparing secrets. These operators are typically not constant-time.
- **Look for custom comparison loops:** If a custom loop iterates through characters and returns `False` on the first mismatch, it's vulnerable.

## Prevention

- [ ] **Use constant-time comparison for secrets:** Never use standard equality operators for sensitive values.
- [ ] **Know constant-time functions:**
  - **Python:** `hmac.compare_digest()` or `secrets.compare_digest()`
  - **Node.js:** `crypto.timingSafeEqual()`
  - **Go:** `subtle.ConstantTimeCompare()`
  - **Java:** `MessageDigest.isEqual()` (byte arrays)
  - **PHP:** `hash_equals()`
- [ ] **Use password library verification:** Libraries like bcrypt/argon2 provide timing-safe verification (`bcrypt.checkpw()`, `argon2.verify()`).
- [ ] **Verify equal lengths:** Constant-time functions handle length mismatches safely, but pre-checking improves clarity.

## Related Security Patterns & Anti-Patterns

- [Weak Password Hashing Anti-Pattern](../weak-password-hashing/): Proper password hashing (e.g., bcrypt) includes protection against timing attacks during verification.
- [JWT Misuse Anti-Pattern](../jwt-misuse/): Signature verification of JWTs should use constant-time comparisons.
- [Padding Oracle Anti-Pattern](../padding-oracle/): Another type of cryptographic timing issue where information about padding validity is leaked through timing.

## References

- [OWASP Top 10 A04:2025 - Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/)
- [OWASP GenAI LLM10:2025 - Unbounded Consumption](https://genai.owasp.org/llmrisk/llm10-unbounded-consumption/)
- [OWASP API Security API2:2023 - Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)
- [OWASP Testing for Timing Attacks](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE-208: Observable Timing Discrepancy](https://cwe.mitre.org/data/definitions/208.html)
- [CAPEC-462: Cross-Domain Search Timing](https://capec.mitre.org/data/definitions/462.html)
- [BlueKrypt - Cryptographic Key Length Recommendation](https://www.keylength.com/)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
