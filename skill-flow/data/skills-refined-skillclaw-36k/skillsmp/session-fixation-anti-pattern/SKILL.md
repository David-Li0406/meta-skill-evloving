---
name: "session-fixation-anti-pattern"
description: "Security anti-pattern for session fixation vulnerabilities (CWE-384). Use when generating or reviewing code that handles user sessions, login flows, or authentication state changes. Detects failure to regenerate session IDs after authentication."
---

# Session Fixation Anti-Pattern

**Severity:** High

## Summary

Attackers fix a user's session ID before login. The attacker obtains a valid session ID, tricks the victim into using it, and when authentication fails to regenerate the session ID, hijacks the victim's authenticated session.

## The Anti-Pattern

The anti-pattern is reusing the same session ID before and after authentication.

### BAD Code Example

```python
# VULNERABLE: Session ID not regenerated after login.
from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Insecure in production

@app.route('/')
def index():
    if 'username' in session:
        return f'Hello {session["username"]}! <a href="/logout">Logout</a>'
    return 'Welcome, please <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            # FLAW: Session ID not regenerated.
            # Existing session (potentially attacker-fixed) now authenticated.
            session['username'] = username
            return redirect(url_for('index'))
        return 'Invalid credentials'
    return '''
        <form method="post">
            <p><input type=text name=username></p>
            <p><input type=password name=password></p>
            <p><input type=submit value=Login></p>
        </form>
    '''

# Attack:
# 1. Attacker gets session_id=ABCD
# 2. Tricks victim into using session_id=ABCD (XSS, referrer, etc.)
# 3. Victim logs in, server reuses session_id=ABCD
# 4. Attacker hijacks authenticated session with session_id=ABCD
```

### GOOD Code Example

```python
# SECURE: Regenerate session ID after login and privilege changes.
from flask import Flask, session, redirect, url_for, request

app = Flask(__name__)
app.secret_key = 'your_secret_key' # Use strong, securely managed key

@app.route('/')
def index_secure():
    if 'username' in session:
        return f'Hello {session["username"]}! <a href="/logout">Logout</a>'
    return 'Welcome, please <a href="/login_secure">Login Securely</a>'

@app.route('/login_secure', methods=['GET', 'POST'])
def login_secure():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            # Regenerate session ID after authentication.
            # Creates new session, invalidating pre-login session ID.
            session.regenerate()
            session['username'] = username
            return redirect(url_for('index_secure'))
        return 'Invalid credentials'
    return '''
        <form method="post">
            <p><input type=text name=username></p>
            <p><input type=password name=password></p>
            <p><input type=submit value=Login></p>
        </form>
    '''

@app.route('/logout')
def logout():
    session.clear() # Invalidate session data.
    session.regenerate() # Regenerate to prevent reuse.
    return redirect(url_for('index_secure'))
```

## Detection

- **Review login flows:** Trace the code paths involved in user authentication. Verify that after a successful login, the application explicitly invalidates the old session and generates a completely new session ID.
- **Check session management libraries:** Understand how your web framework or session management library handles session ID generation and regeneration. Ensure it's used correctly.
- **Test with a fixed session ID:** Manually attempt to set a session ID (e.g., using browser developer tools or a proxy like Burp Suite) before logging in. After logging in, check if the session ID remains the same.

## Prevention

- [ ] **Regenerate session ID after authentication:** Always create new session after successful login, invalidating pre-login session ID.
- [ ] **Regenerate on privilege changes:** New session ID when users gain elevated permissions (e.g., admin promotion).
- [ ] **Invalidate old sessions server-side:** Ensure old session IDs cannot be reused after regeneration.
- [ ] **Set secure cookie flags:**
  - `HttpOnly`: Prevents client-side script access
  - `Secure`: HTTPS-only transmission
  - `SameSite`: CSRF protection
- [ ] **Implement session timeouts:** Use both absolute and idle timeouts to limit attack window.

## Related Security Patterns & Anti-Patterns

- [Missing Authentication Anti-Pattern](../missing-authentication/): The foundation of secure user management, without which session fixation is more easily exploited.
- [JWT Misuse Anti-Pattern](../jwt-misuse/): When using JWTs, token revocation and expiration become crucial for managing session state securely.
- [Insufficient Randomness Anti-Pattern](../insufficient-randomness/): Session IDs must be generated using a cryptographically secure random number generator to prevent prediction.

## References

- [OWASP Top 10 A07:2025 - Authentication Failures](https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/)
- [OWASP GenAI LLM06:2025 - Excessive Agency](https://genai.owasp.org/llmrisk/llm06-excessive-agency/)
- [OWASP API Security API2:2023 - Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [CWE-384: Session Fixation](https://cwe.mitre.org/data/definitions/384.html)
- [CAPEC-61: Session Fixation](https://capec.mitre.org/data/definitions/61.html)
- [PortSwigger: Authentication](https://portswigger.net/web-security/authentication)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
