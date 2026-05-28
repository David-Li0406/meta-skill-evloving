---
name: "oauth-security-anti-pattern"
description: "Security anti-pattern for OAuth implementation vulnerabilities (CWE-352, CWE-287). Use when generating or reviewing OAuth/OIDC authentication flows, state parameter handling, or token exchange. Detects missing CSRF protection and insecure redirect handling."
---

# OAuth Security Anti-Pattern

**Severity:** High

## Summary

OAuth 2.0/OIDC flows are complex and easily misconfigured. The critical mistake: failing to implement and validate the `state` parameter. This parameter defends against CSRF attacks during OAuth flows. Missing or predictable `state` allows attackers to trick victims into logging into the attacker's account, enabling account takeover.

## The Anti-Pattern

The anti-pattern is initiating OAuth flows without `state` parameters, or using predictable values not validated on callback.

### BAD Code Example

```python
# VULNERABLE: The OAuth flow is initiated without a `state` parameter.
from flask import request, redirect

OAUTH_PROVIDER_URL = "https://provider.com/auth"
CLIENT_ID = "my-client-id"
CALLBACK_URL = "https://myapp.com/callback"

@app.route("/login/provider")
def oauth_login():
    # Redirects user to OAuth provider.
    # FLAW: No `state` parameter to prevent CSRF.
    auth_url = (f"{OAUTH_PROVIDER_URL}?client_id={CLIENT_ID}"
                f"&redirect_uri={CALLBACK_URL}&response_type=code")
    return redirect(auth_url)

@app.route("/callback")
def oauth_callback():
    # User redirected back from provider.
    # No way to verify callback corresponds to user-initiated flow.
    auth_code = request.args.get("code")
    # Exchanges code for tokens, logs user in.
    # Attacker can link victim's session to attacker's account.
    access_token = exchange_code_for_token(auth_code)
    log_user_in(access_token)
    return "Logged in successfully!"
```

**Attack:**
1. Attacker initiates OAuth flow with own account
2. Provider redirects to `https://myapp.com/callback?code=ATTACKER_CODE`
3. Attacker intercepts and pauses request
4. Attacker tricks victim into visiting malicious callback URL
5. `myapp.com` associates victim's session with attacker's account

### GOOD Code Example

```python
# SECURE: A unique, unpredictable `state` is generated, stored in the session, and validated on callback.
from flask import request, redirect, session
import secrets

@app.route("/login/provider/secure")
def oauth_login_secure():
    # 1. Generate cryptographically random `state`.
    state = secrets.token_urlsafe(32)
    # 2. Store in user's session.
    session['oauth_state'] = state

    auth_url = (f"{OAUTH_PROVIDER_URL}?client_id={CLIENT_ID}"
                f"&redirect_uri={CALLBACK_URL}&response_type=code"
                f"&state={state}") # 3. Send state to provider.
    return redirect(auth_url)

@app.route("/callback/secure")
def oauth_callback_secure():
    # 4. Provider returns `state` in callback.
    received_state = request.args.get("state")
    auth_code = request.args.get("code")

    # 5. CRITICAL: Validate returned state matches session state.
    stored_state = session.pop('oauth_state', None)
    if stored_state is None or not secrets.compare_digest(stored_state, received_state):
        return "Invalid state parameter. CSRF attack detected.", 403

    # State valid, safe to proceed.
    access_token = exchange_code_for_token(auth_code)
    log_user_in(access_token)
    return "Logged in successfully!"
```

## Detection

- **Trace the OAuth flow:** Start at the point where your application redirects to the OAuth provider.
  - Is a `state` parameter being generated?
  - Is it cryptographically random and unpredictable?
- **Examine the callback endpoint:**
  - Does it retrieve the `state` from the incoming request?
  - Does it compare it to a value stored in the user's session *before* the redirect?
  - Is the comparison done in constant time (`hmac.compare_digest`) to prevent timing attacks?
  - Is the state value single-use (i.e., deleted from the session after being checked)?

## Prevention

- [ ] **Always use `state` parameter:** Required in all OAuth/OIDC authorization requests.
- [ ] **Generate cryptographically random `state`:** Minimum 32 characters. Never use predictable values (user ID, timestamp).
- [ ] **Bind to session:** Store `state` in session cookie before redirect.
- [ ] **Strictly validate on callback:** Compare request `state` with session value. Reject mismatches.
- [ ] **Make single-use:** Remove from session after validation to prevent replay attacks.
- [ ] **Use PKCE for public clients:** SPAs and mobile apps require PKCE (Proof Key for Code Exchange) in addition to `state`.

## Related Security Patterns & Anti-Patterns

- [Session Fixation Anti-Pattern](../session-fixation/): A successful OAuth CSRF attack is a form of session fixation.
- [Insufficient Randomness Anti-Pattern](../insufficient-randomness/): The `state` parameter must be generated with a cryptographically secure random number generator.
- [Missing Authentication Anti-Pattern](../missing-authentication/): OAuth is a form of authentication, and its flows must be implemented correctly to be secure.

## References

- [OWASP Top 10 A07:2025 - Authentication Failures](https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/)
- [OWASP GenAI LLM06:2025 - Excessive Agency](https://genai.owasp.org/llmrisk/llm06-excessive-agency/)
- [OWASP API Security API2:2023 - Broken Authentication](https://owasp.org/API-Security/editions/2023/en/0xa2-broken-authentication/)
- [OWASP OAuth Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/OAuth_Cheat_Sheet.html)
- [CWE-352: Cross-Site Request Forgery](https://cwe.mitre.org/data/definitions/352.html)
- [CAPEC-103: Clickjacking](https://capec.mitre.org/data/definitions/103.html)
- [PortSwigger: Oauth](https://portswigger.net/web-security/oauth)
- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- Source: [sec-context](https://github.com/Arcanum-Sec/sec-context)
