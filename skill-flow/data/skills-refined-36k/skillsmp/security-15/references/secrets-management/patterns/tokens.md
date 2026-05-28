# Authentication Tokens

**Category**: devops/secrets/tokens
**Description**: Detection patterns for authentication tokens and session credentials
**CWE**: CWE-798, CWE-312, CWE-522

---

## JWT (JSON Web Tokens)

### JWT Token
**Pattern**: `eyJ[A-Za-z0-9_-]*\.eyJ[A-Za-z0-9_-]*\.[A-Za-z0-9_-]*`
**Type**: regex
**Severity**: high
**Languages**: [all]
- JWTs have three base64url-encoded parts separated by dots
- Header and payload both start with `eyJ`
- CWE-312: Cleartext Storage of Sensitive Information

### JWT Secret Key
**Pattern**: `JWT_SECRET|jwt[_-]?secret`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- JWT signing secrets are more dangerous than individual tokens
- Context: Environment variables, config files

---

## OAuth Tokens

### Google OAuth Access Token
**Pattern**: `ya29\.[A-Za-z0-9_-]+`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Google OAuth 2.0 access tokens start with `ya29.`

### Google OAuth Refresh Token
**Pattern**: `1//[A-Za-z0-9_-]+`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- Google refresh tokens are long-lived and more sensitive

### OAuth Client Secret
**Pattern**: `client_secret['":\s]+['"]?[A-Za-z0-9_-]{24,}['"]?`
**Type**: regex
**Severity**: critical
**Languages**: [all]
- OAuth client secrets enable impersonation

---

## Session Tokens

### Express/Connect Session
**Pattern**: `s:[A-Za-z0-9+/=]+\.[A-Za-z0-9+/=]+`
**Type**: regex
**Severity**: high
**Languages**: [javascript, typescript]
- Connect.sid cookie format

### PHP Session ID
**Pattern**: `PHPSESSID=[a-z0-9]{26,32}`
**Type**: regex
**Severity**: high
**Languages**: [php]
- PHP session identifiers

### Django Session ID
**Pattern**: `sessionid=[a-z0-9]{32}`
**Type**: regex
**Severity**: high
**Languages**: [python]
- Django session identifiers

### ASP.NET Session ID
**Pattern**: `ASP\.NET_SessionId=[a-z0-9]{24}`
**Type**: regex
**Severity**: high
**Languages**: [csharp]
- ASP.NET session identifiers

---

## API Bearer Tokens

### Bearer Token
**Pattern**: `[Bb]earer\s+[A-Za-z0-9_\-.~+/]+=*`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Authorization header bearer tokens

### Basic Auth Encoded
**Pattern**: `[Bb]asic\s+[A-Za-z0-9+/]+=*`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Can be decoded to reveal username:password
- CWE-522: Insufficiently Protected Credentials

---

## Service-Specific Tokens

### Auth0 Token
**Pattern**: `[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Context: AUTH0_CLIENT_SECRET, auth0.com domains

### Firebase Token
**Pattern**: `[0-9]+:[A-Za-z0-9_-]+:[A-Za-z0-9_-]+`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Firebase config and FCM tokens

### Supabase Service Role Key
**Pattern**: `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Supabase service role key bypasses Row Level Security
- Context: SUPABASE_SERVICE_ROLE_KEY

### Supabase Anon Key
**Pattern**: `eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Supabase anonymous key
- Context: SUPABASE_ANON_KEY

### Okta API Token
**Pattern**: `00[A-Za-z0-9_-]{40}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Okta API tokens start with `00`
- Context: OKTA_API_TOKEN

### Clerk Live Secret Key
**Pattern**: `sk_live_[A-Za-z0-9]{40,}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Clerk production secret keys

### Clerk Test Secret Key
**Pattern**: `sk_test_[A-Za-z0-9]{40,}`
**Type**: regex
**Severity**: low
**Languages**: [all]
- Clerk test environment keys

---

## CSRF Tokens

### CSRF Token
**Pattern**: `csrf[_-]?token['":\s]+['"]?[A-Za-z0-9_-]{32,}['"]?`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- CSRF tokens are session-specific but shouldn't be logged

---

## Password Reset Tokens

### Password Reset Token
**Pattern**: `reset[_-]?token['":\s]+['"]?[A-Za-z0-9_-]{32,}['"]?`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Password reset tokens allow account takeover if exposed

---

## Verification Tokens

### Email Verification Token
**Pattern**: `verify[_-]?token['":\s]+['"]?[A-Za-z0-9_-]{32,}['"]?`
**Type**: regex
**Severity**: medium
**Languages**: [all]
- Email verification tokens

### Magic Link Token
**Pattern**: `/auth/magic/[A-Za-z0-9_-]{32,}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Magic link authentication URLs

### Login Link Token
**Pattern**: `/login/[A-Za-z0-9_-]{64,}`
**Type**: regex
**Severity**: high
**Languages**: [all]
- Passwordless login URLs

---

## Detection Notes

### Token Characteristics
- Usually high entropy (random-looking)
- Often base64 or base64url encoded
- May have recognizable prefixes
- Time-limited but dangerous during validity

### Context Matters
- Tokens in code vs configuration
- Client-side vs server-side exposure
- Public vs authenticated endpoints

### False Positives
- Example tokens in documentation
- Mock tokens in test files
- Expired tokens in logs (still flag)
- Non-secret base64 data

### Severity Adjustments
- **Refresh tokens > Access tokens**: Longer validity
- **Admin tokens > User tokens**: Higher privilege
- **Production > Development**: Real data access

---

## References

- [CWE-798: Use of Hard-coded Credentials](https://cwe.mitre.org/data/definitions/798.html)
- [CWE-312: Cleartext Storage of Sensitive Information](https://cwe.mitre.org/data/definitions/312.html)
- [CWE-522: Insufficiently Protected Credentials](https://cwe.mitre.org/data/definitions/522.html)
