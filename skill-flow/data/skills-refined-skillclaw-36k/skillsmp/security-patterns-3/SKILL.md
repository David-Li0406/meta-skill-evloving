---
name: security-patterns
description: Elixir-specific security patterns, OWASP mitigations, and compliance best practices
---

# Security Patterns Skill

Use this skill when implementing security features, handling user data, or ensuring compliance in Elixir applications.

## When to Use

- Implementing authentication and authorization
- Handling user input and validation
- Working with sensitive data (passwords, tokens)
- Designing secure APIs
- Ensuring GDPR/SOC2/HIPAA compliance
- Implementing OWASP Top 10 mitigations
- Managing secrets and encryption
- Preventing common security vulnerabilities

## OWASP Top 10 Mitigations

### A01: Broken Access Control

**Problem**: Users can access resources they shouldn't.

**Elixir Solution**: Role-Based Access Control (RBAC) with Ash policies
```elixir
defmodule Accounts.Policies.User do
  use Ash.Policy

  policy :read do
    authorize_if user.id == resource.user_id
  end

  policy :update do
    authorize_if user.id == resource.user_id and user.role in [:admin, :manager]
  end
end
```

### A02: Cryptographic Failures

**Problem**: Using weak or deprecated cryptography.

**Elixir Solution**: Use proven crypto libraries
```elixir
# ✅ Good: Argon2 for password hashing
def hash_password(password) do
  Argon2.hash_pwd(password)
end

def verify_password(password, hash) do
  Argon2.verify_pwd(password, hash)
end

# ❌ Bad: SHA1 or MD5
def hash_password_legacy(password) do
  :crypto.hash(:sha256, password)
end
```

### A03: Injection

**Problem**: SQL injection via string interpolation.

**Elixir Solution**: Parameterized queries with Ecto
```elixir
# ✅ Good: Parameterized
def get_user(id) do
  from(u in User, where: u.id == ^id)
  |> Repo.one()
end

# ❌ Bad: String interpolation
def get_user_unsafe(id) do
  Repo.query!("SELECT * FROM users WHERE id = #{id}")
end
```

### A04: Insecure Design

**Problem**: Security through obscurity or unvalidated redirects.

**Elixir Solution**: Proper session management and secure redirects
```elixir
# ✅ Good: Constant-time comparison
def verify_token(token, stored_token) do
  Plug.Crypto.secure_compare(token, stored_token)
end

# ❌ Bad: Timing-sensitive comparison
def verify_token_unsafe(token, stored_token) do
  token == stored_token
end
```

### A07: Identification and Authentication Failures

**Problem**: Weak session management.

**Elixir Solution**: Secure JWT with proper signing and verification
```elixir
defmodule Auth.Token do
  use Joken

  def generate_token(user_id, expiration \\ 3600) do
    signer()
    |> add_claim("sub", user_id)
    |> add_claim("exp", current_time() + expiration)
    |> sign()
  end

  def verify_token(token) do
    verifier()
    |> verify(token)
  end
end
```

### A08: Software and Data Integrity Failures

**Problem**: Using unsigned packages or no checksums.

**Elixir Solution**: Pin dependencies and verify checksums
```elixir
# mix.exs
defp deps do
  [
    {:bcrypt_elixir, "~> 3.0"},
    {:jason, "~> 1.4"},
    {:ash, "~> 3.0", override: true}  # Pin to specific version
  ]
end
```

### A09: Security Logging and Monitoring

**Problem**: Logging sensitive data or poor error handling.

**Elixir Solution**: Structured logging with redaction
```elixir
# ✅ Good: Redact sensitive data
def log_user_action(user_id, action) do
  Logger.info("User action", user_id: anonymize(user_id), action: action)
end

defp anonymize(user_id) do
  "usr_#{Base.encode16(:crypto.hash(:md5, user_id))}"
end

# ❌ Bad: Log sensitive data
def log_user_action_unsafe(user_id, action) do
  IO.inspect("User #{user_id} performed #{action}")
end
```

## Elixir-Specific Security

### Atom Exhaustion Protection

**Problem**: Creating atoms from user input can exhaust atom table.

**Elixir Solution**: Use binaries or limit atom creation
```elixir
# ✅ Good: Use binaries
def handle_user_type(type) when is_binary(type) do
  # type is already a binary
  :ok
end

def handle_user_type(type) do
  # Convert to atom ONLY for known values
  case type do
    "admin" -> :admin
    "user" -> :user
    _ -> :unknown
  end
end

# ❌ Bad: Direct atom creation
def handle_user_type_unsafe(type) do
  String.to_atom(type)
end
```

### Timing Attack Prevention

**Problem**: Variable-time operations can leak information.

**Elixir Solution**: Constant-time operations
```elixir
# ✅ Good: Constant-time comparison
def compare_hashes(hash1, hash2) do
  Plug.Crypto.secure_compare(hash1, hash2)
end

# ❌ Bad: Linear-time comparison
def compare_hashes_unsafe(hash1, hash2) do
  :crypto.hash(:sha256, hash1) == :crypto.hash(:sha256, hash2)
end
```

### Boolean Coercion Prevention

**Problem**: Truthy/falsy values causing security issues.

**Elixir Solution**: Explicit boolean checks
```elixir
# ✅ Good: Explicit checks
def has_permission?(user, permission) do
  permission in user.permissions
end

# ❌ Bad: Relies on truthiness
def has_permission_unsafe(user, permission) do
  user.permissions[permission]
end
```

## Cookie Security

### Secure Cookie Attributes

```elixir
# ✅ Good: Secure cookie configuration
def secure_session(conn) do
  conn
  |> put_resp_cookie("session_id", session_id,
    max_age: 3600,
    secure: true,              # HTTPS only
    http_only: true,          # Not accessible via JavaScript
    same_site: "Strict",     # CSRF protection
    path: "/",
    encrypt: true
  )
end
```

## Input Validation

### Ash Changesets for Security

```elixir
defmodule Accounts.User do
  use Ash.Resource

  attributes do
    attribute :email, :string,
      allow_nil?: false,
      constraints: [
        max_length: 255,
        match: ~r/^[\w-\.]+@[\w-\.]+$/,
        format: [with: ~r/@/]
      ]

    attribute :password, :string,
      allow_nil?: false,
      constraints: [
        min_length: 12,
        max_length: 128,
        format: [with: ~r/^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/]
      ]
  end
end
```

## CSRF Protection

### Phoenix Plug Configuration

```elixir
defmodule MyAppWeb.Plugs.CSRFProtection do
  import Plug.Conn
  alias Phoenix.Controller

  def init(opts), do: opts

  def call(conn, opts) do
    # Check CSRF token for state-changing requests
    if conn.method in ["POST", "PUT", "PATCH", "DELETE"] do
      check_csrf_token(conn, opts)
    else
      conn
    end
  end

  defp check_csrf_token(conn, opts) do
    token = get_csrf_token(conn)

    case verify_csrf_token(token, conn) do
      :ok -> conn
      :error ->
        conn
        |> put_status(403)
        |> halt()
    end
  end
end
```

## Secrets Management

### Environment Variables

```elixir
# config/runtime.exs
import Config

config :my_app, :secrets,
  database_url: System.get_env("DATABASE_URL"),
  secret_key_base: System.get_env("SECRET_KEY_BASE")

# NEVER hardcode secrets
# ❌ config/config.exs
# config :my_app, :secrets,
#   secret_key: "hardcoded_secret_key_here"  # DANGEROUS!
```

### Encryption at Rest

```elixir
# ✅ Good: Database encryption
def encrypt_sensitive_data(data) do
  :crypto.block_encrypt(
    :aes_gcm,
    Application.get_env(:my_app, :encryption_key),
    data,
    true  # Base64 encoding
  )
end

# ❌ Bad: Storing plaintext
def store_sensitive_data(data) do
  Repo.insert(%Sensitive{data: data})  # NO ENCRYPTION!
end
```

## Compliance Frameworks

### GDPR Compliance Checklist

- [ ] Data minimization: collect only necessary data
- [ ] Right to erasure: user data deletion on request
- [ ] Data portability: export user data in standard format
- [ ] Explicit consent: opt-in for data processing
- [ ] Data breach notification: 72-hour rule
- [ ] Privacy by design: privacy impact assessment
- [ ] Data protection officer: DPO assigned
- [ ] Data retention policy: defined time limits
- [ ] Consent management: granular permissions

### SOC2 Compliance Checklist

- [ ] Access control: least privilege principle
- [ ] Audit logging: all security-relevant actions logged
- [ ] Network security: TLS/HTTPS everywhere
- [ ] Change management: controlled changes
- [ ] System monitoring: real-time alerts
- [ ] Incident response: procedures defined
- [ ] Penetration testing: regular security tests
- [ ] Vulnerability management: tracking and remediation

## Security Tools

### Sobelow (Static Analysis)

```bash
# Install
mix deps.get sobelow

# Run
mix sobelow --verbose

# Common findings
# - High: XSS vulnerability
# - High: SQL injection
# - Medium: CSRF protection missing
```

### Dependency Scanning

```bash
# Mix Hex Audit
mix hex.outdated
mix hex.audit --format json

# Continuous scanning in CI/CD
# - Automated security checks on every PR
# - Automated dependency updates
```

### Secrets Detection

```bash
# Git Secrets scanning
git secrets --scan

# Detects:
# - API keys
# - Database passwords
# - Private keys
# - Access tokens
```

## Anti-Patterns

### Security Through Obscurity

```elixir
# ❌ Anti-pattern: Hiding security issues
# defmodule SecretAPI do
#   # Secret algorithm (NO!)
#   def encrypt(data) do
#     :crypto.hash(:md5, data)
#   end
# end

# ✅ Pattern: Use proven, audited libraries
defmodule SecretAPI do
  def encrypt(data) do
    Argon2.hash_pwd(data)
  end
end
```

### Frontend Authorization Checks

```elixir
# ❌ Anti-pattern: Authorization checks in UI
# # Phoenix LiveView
# def mount(%{assigns: %{current_user: user}}) do
#   if user.role != :admin do
#     push_redirect("/forbidden")
#   end
# end

# ✅ Pattern: Backend-only authorization
defmodule Accounts.Policies.Admin do
  policy :admin_only do
    authorize_if user.role == :admin
  end
end
```

## Best Practices Summary

### Authentication & Authorization

1. **Use Ash policies** for authorization, never in controllers
2. **Implement JWT** with proper signing and expiration
3. **Store session data** in server, not client
4. **Use CSRF tokens** for state-changing requests
5. **Enable rate limiting** on authentication endpoints

### Data Protection

1. **Never log sensitive data** (passwords, tokens, PII)
2. **Encrypt at rest** using strong encryption (AES-256-GCM)
3. **Use TLS everywhere** (HTTPS for all endpoints)
4. **Validate input** at application boundaries
5. **Use parameterized queries** (Ecto) to prevent injection

### Secrets Management

1. **Use environment variables** for all secrets
2. **Never commit secrets** to version control
3. **Rotate secrets** regularly
4. **Use secret scanning** in CI/CD pipelines
5. **Implement secret injection** for development

### OWASP Protection

1. **Implement RBAC** with Ash policies
2. **Prevent injection** via parameterized queries
3. **Use strong cryptography** (Argon2, bcrypt)
4. **Implement CSRF** protection everywhere
5. **Validate and sanitize** all user input
6. **Use secure headers** (CSP, HSTS, X-Frame-Options)

### Compliance

1. **Document data processing** activities
2. **Implement data export/deletion** on request
3. **Maintain audit logs** for compliance evidence
4. **Conduct regular security assessments**
5. **Document incident response** procedures

## Tools to Use

- **Sobelow**: Security static analysis for Elixir
- **Hex.audit**: Dependency vulnerability scanning
- **Git-secrets**: Secrets detection in repositories
- **Plug.Crypto**: Constant-time crypto operations
- **Ash.Policy**: Authorization policies
- **Joken**: JWT token management
- **Phoenix.LiveSecurity**: LiveView security patterns

## Resources

- OWASP Top 10: https://owasp.org/www-project-top-ten
- Elixir Secure Coding Training: https://github.com/erlef/elixir-secure-coding
- CWE Top 25: https://cwe.mitre.org/top25/
- Elixir Security Guidelines: https://hexdocs.pm/phoenix/plug_security
