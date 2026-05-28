---
name: "xpath-injection-anti-pattern"
description: "Security anti-pattern for XPath injection vulnerabilities (CWE-643). Use when generating or reviewing code that queries XML documents, constructs XPath expressions, or handles user input in XML operations. Detects unescaped quotes and special characters in XPath queries."
---

# XPath Injection Anti-Pattern

**Severity:** High

## Summary

XPath Injection occurs when applications insecurely embed user input into XPath queries without proper escaping or parameterization. XPath is used to navigate and query XML documents. Similar to SQL Injection, attackers can inject special characters into the input, manipulating the XPath query's logic. This can lead to authentication bypass, unauthorized access to sensitive XML data, or information disclosure about the XML document structure.

## The Anti-Pattern

The anti-pattern is constructing XPath queries by concatenating user-controlled input directly into the XPath string without proper escaping or parameterization.

### BAD Code Example

```python
# VULNERABLE: User input is directly concatenated into an XPath query.
from lxml import etree

# Sample XML document
xml_doc = etree.fromstring('''
<users>
    <user>
        <name>admin</name>
        <password>adminpass</password>
        <role>administrator</role>
    </user>
    <user>
        <name>guest</name>
        <password>guestpass</password>
        <role>user</role>
    </user>
</users>
''')

def authenticate_user(username, password):
    # The XPath query is constructed using string concatenation.
    # Attacker can inject single quotes or boolean logic.
    xpath_query = f"//user[name='{username}' and password='{password}']"

    # Attacker's input:
    # username = "admin' or '1'='1"
    # password = "anything"

    # Resulting XPath query:
    # "//user[name='admin' or '1'='1' and password='anything']"
    # This query will bypass authentication and return the 'admin' user,
    # as '1'='1' is always true.

    found_users = xml_doc.xpath(xpath_query)
    return len(found_users) > 0

# Test the vulnerable function
# print(authenticate_user("admin' or '1'='1", "blah")) # Returns True!
```

### GOOD Code Example

```python
# SECURE: Use a parameterization mechanism or escape user input for XPath.
from lxml import etree

xml_doc = etree.fromstring('''
<users>
    <user>
        <name>admin</name>
        <password>adminpass</password>
        <role>administrator</role>
    </user>
    <user>
        <name>guest</name>
        <password>guestpass</password>
        <role>user</role>
    </user>
</users>
''')

# lxml (and other libraries) support XPath parameterization.
# This separates the query structure from the user-provided data.
def authenticate_user_secure(username, password):
    # Pass parameters separately using a variable binding mechanism.
    # The library will handle proper escaping.
    xpath_query = "//user[name=$username and password=$password]"

    # Define the variables for the XPath expression.
    variables = {'username': username, 'password': password}

    found_users = xml_doc.xpath(xpath_query, **variables)
    return len(found_users) > 0

# Test the secure function
# print(authenticate_user_secure("admin' or '1'='1", "blah")) # Returns False (correctly)
```

## Detection

- **Review XPath query construction:** Look for any code that constructs XPath queries using string concatenation, interpolation (e.g., f-strings), or formatting methods with user-supplied input.
- **Identify XPath evaluation functions:** Search for calls to functions like `xpath()`, `evaluate()`, `selectNodes()`, or similar methods in your XML processing library.
- **Check for escaping:** Verify that any user input inserted into an XPath query is properly escaped. The rules for escaping in XPath can be complex, especially for strings containing both single and double quotes.
- **Test with injection payloads:** Input XPath metacharacters (e.g., `'`, `"`, `and`, `or`, `comment()`) to see if they alter the query's behavior or cause unexpected results.

## Prevention

- [ ] **Use parameterized XPath queries:** This is the most effective defense. Many XML libraries provide mechanisms to pass variables to XPath expressions separately from the query string, which handles escaping automatically.
- [ ] **Escape user input:** If parameterization is not available, all user-supplied input used in XPath queries must be properly escaped. Be careful with strings that contain both single and double quotes, as these require special handling (e.g., using `concat()` in XPath):

```python
def escape_xpath_string(s):
    # Handle strings with both quotes using concat()
    if "'" in s and '"' in s:
        return "concat('" + s.replace("'", "',\"'\",'") + "')"
    elif "'" in s:
        return '"' + s + '"'
    else:
        return "'" + s + "'"
```

- [ ] **Validate input:** Use a strict allowlist to validate user input before it's used in any XPath query. For example, if a username is expected, ensure it only contains alphanumeric characters.
- [ ] **Avoid building dynamic XPath expressions:** Whenever possible, use static XPath expressions and rely on parameters or DOM traversal for dynamic selection.

## Related Security Patterns & Anti-Patterns

- [SQL Injection Anti-Pattern](../sql-injection/): A direct analog, where the target is a relational database.
- [LDAP Injection Anti-Pattern](../ldap-injection/): A direct analog, where the target is an LDAP directory service.
- [Missing Input Validation Anti-Pattern](../missing-input-validation/): The fundamental vulnerability that allows XPath injection to occur.

## References

- [OWASP Top 10 A05:2025 - Injection](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [OWASP GenAI LLM01:2025 - Prompt Injection](https://genai.owasp.org/llmrisk/llm01-prompt-injection/)
- [OWASP API Security API8:2023 - Security Misconfiguration](https://owasp.org/API-Security/editions/2023/en/0xa8-security-misconfiguration/)
- [OWASP XPath Injection](https://owasp.org/www-community/attacks/XPATH_Injection)
- [CWE-643: Improper Neutralization of Data within XPath Expressions ('XPath Injection')](https://cwe.mitre.org/data/definitions/643.html)
- [CAPEC-83: XPath Injection](https://capec.mitre.org/data/definitions/83.html)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
