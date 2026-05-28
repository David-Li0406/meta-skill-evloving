---
name: "encoding-bypass-anti-pattern"
description: "Security anti-pattern for encoding bypass vulnerabilities (CWE-838). Use when generating or reviewing code that handles URL encoding, Unicode normalization, or character set conversions before security validation. Detects validation before normalization and double-encoding issues."
---

# Encoding Bypass Anti-Pattern

**Severity:** High

## Summary

Encoding bypass evades security checks via alternate encodings. Occurs when validation happens before decoding/normalization. Encoded payload appears safe but becomes malicious after processing. Bypasses WAFs, input filters, enables XSS and SQL injection.

## The Anti-Pattern

Flawed order of operations: **Validate then Decode/Normalize**. Security checks run on encoded data, application later uses decoded version, re-introducing the vulnerability.

### BAD Code Example

```python
# VULNERABLE: Validation happens before Unicode normalization.
import unicodedata

def is_safe_username(username):
    # This check is flawed because it doesn't account for Unicode variants.
    if '<' in username or '>' in username:
        return False
    return True

def create_user_profile(username):
    if not is_safe_username(username):
        raise ValueError("Invalid characters in username.")

    # The application later normalizes the username for display or storage.
    # The full-width less-than sign '＜' (U+FF1C) was not caught by the check.
    # It gets normalized into the standard '<' (U+003C), enabling XSS.
    normalized_username = unicodedata.normalize('NFKC', username)

    # This will render the malicious script tag.
    return f"<div>Welcome, {normalized_username}</div>"

# Attacker's input: '＜script＞alert(1)＜/script＞'
# is_safe_username returns True.
# The normalized output becomes '<div>Welcome, <script>alert(1)</script></div>'
```

### GOOD Code Example

```python
# SECURE: Normalize then validate.
import unicodedata

def is_safe_username(username):
    # This check is now effective because it runs on the canonical form of the input.
    if '<' in username or '>' in username:
        return False
    return True

def create_user_profile(username):
    # First, normalize the input to its canonical form.
    normalized_username = unicodedata.normalize('NFKC', username)

    # Then, perform the security validation on the normalized data.
    if not is_safe_username(normalized_username):
        raise ValueError("Invalid characters in username.")

    # Now it's safe to use the normalized username.
    return f"<div>Welcome, {normalized_username}</div>"
```

### JavaScript/Node.js Examples

**BAD:**
```javascript
// VULNERABLE: Validation before URL decoding in path traversal
const express = require('express');
const fs = require('fs');
const path = require('path');

app.get('/file/:filename', (req, res) => {
    const filename = req.params.filename;

    // Check for path traversal - but filename is still encoded
    if (filename.includes('..')) {
        return res.status(400).send('Invalid filename');
    }

    // Express automatically decodes URL parameters
    // Attack: filename = "..%2F..%2Fetc%2Fpasswd"
    // After decoding: "../../etc/passwd" - bypasses the check
    const filePath = path.join('/uploads', filename);
    res.sendFile(filePath);
});

// Attack payload: GET /file/..%252F..%252Fetc%252Fpasswd
// Double encoding: %252F becomes %2F, then becomes /
```

**GOOD:**
```javascript
// SECURE: Decode then validate
const express = require('express');
const fs = require('fs');
const path = require('path');

app.get('/file/:filename', (req, res) => {
    // Express already decoded once, but check for double encoding
    let filename = decodeURIComponent(req.params.filename);

    // Normalize to canonical form
    filename = path.normalize(filename);

    // Now validate the normalized path
    if (filename.includes('..') || path.isAbsolute(filename)) {
        return res.status(400).send('Invalid filename');
    }

    // Safe to use
    const filePath = path.join('/uploads', filename);
    res.sendFile(filePath);
});
```

### Java Examples

**BAD:**
```java
// VULNERABLE: SQL injection via URL decoding bypass
import java.net.URLDecoder;
import java.sql.*;

public void searchUser(String encodedQuery) {
    // Validate before decoding
    if (encodedQuery.contains("'") || encodedQuery.contains("--")) {
        throw new SecurityException("Invalid characters");
    }

    // Decode after validation
    String query = URLDecoder.decode(encodedQuery, "UTF-8");

    // Attack: encodedQuery = "admin%27%20OR%20%271%27%3D%271"
    // After decode: "admin' OR '1'='1" - bypasses the check
    String sql = "SELECT * FROM users WHERE name = '" + query + "'";
    Statement stmt = connection.createStatement();
    ResultSet rs = stmt.executeQuery(sql);
}
```

**GOOD:**
```java
// SECURE: Decode then validate (but use parameterized queries)
import java.net.URLDecoder;
import java.sql.*;
import java.util.regex.Pattern;

public void searchUser(String encodedQuery) {
    // Decode to canonical form first
    String query = URLDecoder.decode(encodedQuery, "UTF-8");

    // Validate the decoded form
    if (!Pattern.matches("^[a-zA-Z0-9_]+$", query)) {
        throw new SecurityException("Invalid characters");
    }

    // Use parameterized query (best practice)
    String sql = "SELECT * FROM users WHERE name = ?";
    PreparedStatement stmt = connection.prepareStatement(sql);
    stmt.setString(1, query);
    ResultSet rs = stmt.executeQuery();
}
```

## Detection

**Python:**
- Validation before `unicodedata.normalize()`
- Input checks before `urllib.parse.unquote()`
- Regex patterns before string normalization
- HTML entity validation before `html.unescape()`

**JavaScript/Node.js:**
- Validation before `decodeURIComponent()`
- Path checks before `path.normalize()`
- Express middleware order (validate before decode)
- Input checks before `Buffer.from(input, 'base64')`

**Java:**
- Validation before `URLDecoder.decode()`
- Security checks before `Normalizer.normalize()`
- Input validation before `StringEscapeUtils.unescapeHtml()`
- Path validation before `Paths.get().normalize()`

**PHP:**
- Validation before `urldecode()`
- Input checks before `html_entity_decode()`
- Path validation before `realpath()`

**Search Patterns:**
- Grep: `normalize\(|decode\(|unescape\(|URLDecoder|decodeURIComponent`
- Look for validation logic (if statements, regex) before these functions
- Check for double decoding: multiple decode calls in sequence
- Review web framework routing (automatic decoding may occur)

**Common Encoding Bypass Techniques:**
- **URL encoding:** `%3c` for `<`, `%2e%2e%2f` for `../`
- **Double URL encoding:** `%253c` for `<` (decoded twice)
- **Unicode variants:** `＜` (U+FF1C) for `<`
- **HTML entities:** `&#60;` or `&lt;` for `<`
- **Unicode escapes:** `\u003c` for `<`
- **Mixed encoding:** `%u003c` or `%c0%bc` for `<`
- **Path traversal:** `..%2f`, `..%5c`, `%2e%2e/`

## Prevention

- [ ] **Normalize/decode before validation:** Always bring data to its simplest, canonical form before performing any security checks on it.
- [ ] **Use parameterized queries (for SQL)** and other safe APIs that handle encoding internally. This is the best defense against injection attacks.
- [ ] **Enforce strict character encoding** for all input (e.g., reject any data that is not valid UTF-8).
- [ ] **Be aware of implicit decoding** performed by your web framework or libraries and ensure your validation logic runs after it.
- [ ] **Canonicalize paths** and URLs before validating them to prevent path traversal attacks.

## Testing for Encoding Bypass

**Manual Testing:**
1. Test URL encoding: `%3cscript%3e`, `..%2f..%2f`
2. Test double encoding: `%253cscript%253e`, `..%252f..%252f`
3. Test Unicode variants: `＜script＞`, `．．／`
4. Test HTML entities: `&#60;script&#62;`, `&lt;script&gt;`
5. Test mixed encoding: `%u003cscript%u003e`
6. Verify filters catch all encoding variants

**Automated Testing:**
- **Static Analysis:** Semgrep, CodeQL to detect validation-before-decode patterns
- **DAST:** Burp Suite Intruder with encoding payloads, OWASP ZAP fuzzer
- **Payload Lists:** SecLists encoding bypass payloads
- **Custom Scripts:** Automated encoding variant generation

**Example Test:**
```python
# Test that validation occurs after normalization
def test_encoding_bypass_prevention():
    # Unicode variant of '<script>'
    malicious_input = "＜script＞alert(1)＜/script＞"

    try:
        create_user_profile(malicious_input)
        assert False, "Should reject encoded malicious input"
    except ValueError:
        pass  # Expected

    # Double URL encoding
    encoded_input = "%253cscript%253e"
    try:
        search_user(encoded_input)
        assert False, "Should reject double-encoded input"
    except SecurityException:
        pass  # Expected
```

**Burp Suite Test:**
```
# Intruder payload positions
GET /file/§..%2f..%2fetc%2fpasswd§

# Payload list (encoding variants)
..%2f..%2f
..%252f..%252f
．．／．．／
%2e%2e%2f%2e%2e%2f
```

## Remediation Steps

1. **Identify decoding operations** - Use detection patterns to find decode/normalize functions
2. **Trace data flow** - Follow user input from entry to security validation
3. **Check validation order** - Verify decode/normalize happens before validation
4. **Reverse order if needed** - Move normalization before security checks
5. **Add missing normalization** - Insert decode/normalize if absent
6. **Test with encoding variants** - Use payload list from Testing section
7. **Verify canonicalization** - Ensure all paths/URLs are normalized
8. **Review framework behavior** - Check for automatic decoding in web framework

## Related Security Patterns & Anti-Patterns

- [SQL Injection Anti-Pattern](../sql-injection/): A common goal of encoding bypass attacks.
- [Cross-Site Scripting (XSS) Anti-Pattern](../xss/): Often enabled by bypassing filters with encoded payloads.
- [Path Traversal Anti-Pattern](../path-traversal/): Can be achieved by using encoded representations of `../`.
- [Unicode Security Anti-Pattern](../unicode-security/): A collection of issues related to handling Unicode securely.

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM05:2025 - Improper Output Handling](https://genai.owasp.org/llmrisk/llm05-improper-output-handling/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP Testing for HTTP Incoming Requests](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE-838: Inappropriate Encoding for Output Context](https://cwe.mitre.org/data/definitions/838.html)
- [CAPEC-267: Leverage Alternate Encoding](https://capec.mitre.org/data/definitions/267.html)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
