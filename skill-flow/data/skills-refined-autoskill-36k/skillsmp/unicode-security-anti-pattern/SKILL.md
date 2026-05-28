---
name: "unicode-security-anti-pattern"
description: "Security anti-pattern for Unicode-related vulnerabilities (CWE-176). Use when generating or reviewing code that handles usernames, displays text, validates input, or compares strings. Detects confusable characters, normalization issues, and bidirectional text attacks."
---

# Unicode Security Anti-Pattern

**Severity:** Medium

## Summary

Applications fail to handle Unicode character representation variants, enabling username spoofing, phishing, and validation bypasses through:

1. **Confusable Characters (Homoglyphs):** Identical-looking characters from different scripts (Latin 'a' vs. Cyrillic 'а').
2. **Normalization Issues:** Multiple byte sequences for the same character (precomposed vs. base + combining accent).
3. **Zero-Width Characters:** Non-printing characters hiding malicious content or altering string lengths.
4. **Bidirectional Text Overrides:** Control characters reordering display (obfuscating `exe.pdf` as `fdp.exe`).

## The Anti-Pattern

The anti-pattern is processing Unicode strings without normalization, confusable detection, or control character stripping.

### BAD Code Example

```python
# VULNERABLE: Comparing strings without normalization or confusable detection.
def authenticate_user(provided_username, password):
    # This example assumes `fetch_user_from_db` expects the exact string from the DB.
    stored_user = fetch_user_from_db(provided_username)

    if stored_user and stored_user.password == hash_password(password):
        # The 'admin' account exists.
        # An attacker registers an account with username "аdmin" (Cyrillic 'a').
        # The database stores "аdmin".
        # When an attacker tries to log in as "аdmin", `provided_username` is "аdmin".
        # `fetch_user_from_db` finds the attacker's "аdmin" user.
        # But if the application internally processes "аdmin" to "admin"
        # in some other place for a check like `if username == "admin"`,
        # then "аdmin" might bypass this check.
        # Or, more directly, if `fetch_user_from_db` is case/normalization insensitive:
        # Attacker registers "Admin" (Latin A).
        # Legitimate user is "admin" (Latin a).
        # Both may resolve to the same internal user, or one user can spoof another.
        return True
    return False

# Another example: Allowing confusable characters for domain names.
# Attacker registers "pаypal.com" (with Cyrillic 'a')
# This looks identical to "paypal.com" (with Latin 'a'), enabling phishing.
```

### GOOD Code Example

```python
# SECURE: Normalize, filter, and compare Unicode strings consistently.
import unicodedata
import re

def normalize_and_sanitize_username(username):
    # 1. Normalize to canonical form (NFC) for consistent comparison.
    #    NFC replaces combining characters with precomposed equivalents.
    normalized = unicodedata.normalize('NFC', username)

    # 2. Strip zero-width and bidirectional control characters.
    #    Prevents display manipulation and hidden content.
    sanitized = re.sub(r'[\u200B-\u200F\u202A-\u202E\u2066-\u2069]', '', normalized)

    # 3. Apply confusable detection (recommended for critical identifiers).
    #    Convert to "skeleton" form or use confusables database.
    #    (Implementation depends on specific libraries/algorithms).

    # 4. Enforce allowlist of permitted characters.
    #    For usernames, restrict to ASCII alphanumeric and limited symbols.
    if not re.fullmatch(r'^[a-zA-Z0-9_.-]+$', sanitized):
        raise ValueError("Username contains disallowed characters.")

    return sanitized

def authenticate_user_secure(provided_username, password):
    # All usernames should be normalized and sanitized consistently before storage and comparison.
    sanitized_username = normalize_and_sanitize_username(provided_username)
    stored_user = fetch_user_from_db(sanitized_username)

    if stored_user and stored_user.password == hash_password(password):
        return True
    return False

# When displaying usernames or domain names, consider using Punycode for internationalized domain names (IDNs)
# to make spoofing more obvious to users.
```

## Detection

- **Review string comparisons:** Look for any comparisons of user-controlled strings, especially for authentication, authorization, or access control decisions.
- **Check input processing:** See how input strings are handled from reception to storage and display. Are normalization steps applied consistently?
- **Test with confusable characters:** Try registering usernames or domains that use homoglyphs (e.g., Cyrillic 'a' instead of Latin 'a') for common reserved names (admin, root) or well-known brands (paypal, apple).
- **Test with zero-width characters:** Insert zero-width characters (e.g., `\u200B`) into inputs to see if they bypass length checks or string comparisons.

## Prevention

- [ ] **Normalize all Unicode input:** Convert all strings to NFC (Normalization Form C) before validation, storage, or comparison.
- [ ] **Strip dangerous control characters:** Remove zero-width spaces (`\u200B`), bidirectional overrides (`\u202E`), and non-printing characters.
- [ ] **Implement confusable detection:** For critical identifiers (usernames, domains), check for homoglyphs using skeleton forms or confusables databases.
- [ ] **Restrict character sets:** For sensitive identifiers, limit to well-defined character sets (ASCII alphanumeric preferred).
- [ ] **Apply consistently:** Use identical Unicode processing (normalization, stripping, filtering) throughout application (input, storage, comparison, display).

## Related Security Patterns & Anti-Patterns

- [Encoding Bypass Anti-Pattern](../encoding-bypass/): Unicode issues are a specific type of encoding manipulation that can bypass security filters.
- [Missing Input Validation Anti-Pattern](../missing-input-validation/): Failure to handle Unicode correctly is a form of improper input validation.
- [Cross-Site Scripting (XSS) Anti-Pattern](../xss/): Malicious Unicode characters can sometimes be used to bypass XSS filters.

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM05:2025 - Improper Output Handling](https://genai.owasp.org/llmrisk/llm05-improper-output-handling/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [CWE-176: Improper Handling of Unicode](https://cwe.mitre.org/data/definitions/176.html)
- [CAPEC-71: Using Unicode Encoding to Bypass Validation](https://capec.mitre.org/data/definitions/71.html)
- [Unicode Security Considerations](https://unicode.org/reports/tr36/)
- [Unicode Confusables](https://util.unicode.org/UnicodeJsps/confusables.jsp)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
