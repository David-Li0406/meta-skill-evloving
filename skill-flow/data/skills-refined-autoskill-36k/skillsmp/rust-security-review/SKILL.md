---
name: rust-security-review
description: |
  Use this skill when adding authentication, handling user input, working with secrets, creating API endpoints, or implementing payment/sensitive features in Rust. 
  Provides a comprehensive security checklist and patterns using idiomatic crates.
---

# Rust Security Review

This skill ensures all Rust code follows security best practices, leveraging the language's type safety while identifying potential logic-level vulnerabilities.

## When to Activate

- Implementing authentication or authorization (JWT, session cookies)
- Handling user input via `serde` or public API endpoints
- Working with secrets, credentials, or `.env` files
- Interacting with databases using `sqlx`.
- Implementing payment features or handling sensitive PII
- Integrating third-party crates or APIs

---

## Security Checklist

### 1. Secrets Management

#### ❌ NEVER Do This
```rust
// Hardcoded secret - will be compiled into the binary
const API_KEY: &str = "sk-proj-xxxxx"; 
```

#### ✅ ALWAYS Do This
Use `dotenvy` for loading and `envy` for type-safe deserialization. Use the `secrecy` crate to prevent accidental logging.

```rust
use serde::Deserialize;
use secrecy::{Secret, ExposeSecret};

#[derive(Deserialize)]
struct Config {
    database_url: Secret<String>,
    api_key: Secret<String>,
}

fn main() {
    dotenvy::dotenv().ok();
    let config = envy::from_env::<Config>().expect("Missing env vars");
    
    // Access safely: config.api_key.expose_secret()
}
```

#### Verification Steps
- [ ] No hardcoded keys in source code or `Cargo.toml`.
- [ ] `.env` added to `.gitignore`.
- [ ] Sensitive strings wrapped in `secrecy::Secret`.
- [ ] CI/CD secrets injected via environment, not files.

### 2. Input Validation

#### Validate at the Serialization Boundary
Use the `validator` crate alongside `serde` to enforce business logic on input.

```rust
use serde::Deserialize;
use validator::Validate;

#[derive(Deserialize, Validate)]
struct SignupRequest {
    #[validate(email)]
    email: String,
    #[validate(length(min = 8))]
    password: String,
    #[validate(range(min = 18, max = 120))]
    age: u16,
}

// In an Axum handler
async fn register(axum::Json(payload): axum::Json<SignupRequest>) -> impl IntoResponse {
    if let Err(e) = payload.validate() {
        return (StatusCode::BAD_REQUEST, format!("Validation error: {}", e));
    }
    // Proceed...
}
```

#### Verification Steps
- [ ] All public structs implement `Validate`.
- [ ] String length limits enforced (prevent memory exhaustion/ReDoS).
- [ ] Numeric bounds checked (prevent overflow/logic errors).
- [ ] Whitelist validation for enums and fixed strings.

### 3. SQL Injection Prevention

#### ❌ NEVER Construct SQL with String Formatting
```rust
// DANGEROUS: SQL Injection vulnerability
let query = format!("SELECT * FROM users WHERE email = '{}'", user_email);
```

#### ✅ ALWAYS Use Parameterized Queries
`sqlx` provides compile-time checked queries that are inherently safe.

```rust
// Safe: Parameters are bound via the database protocol
let user = sqlx::query!(
    "SELECT id, name FROM users WHERE email = $1",
    user_email
)
.fetch_optional(&pool)
.await?;
```

#### Verification Steps
- [ ] No `format!` or `concat!` used to build SQL strings.
- [ ] `sqlx::query!` or `sqlx::query_as!` macros used for compile-time safety.
- [ ] Database user has minimal required permissions.

### 4. Authentication & Authorization

#### Cookie Security
```rust
use axum_extra::extract::cookie::{Cookie, SameSite};

// Set secure, httpOnly cookies
let cookie = Cookie::build(("session", token))
    .path("/")
    .http_only(true)
    .secure(true)
    .same_site(SameSite::Strict)
    .finish();
```

#### Password Hashing
```rust
use argon2::{
    password_hash::{rand_core::OsRng, PasswordHasher, SaltString},
    Argon2
};

// Use Argon2id for hashing
let salt = SaltString::generate(&mut OsRng);
let password_hash = Argon2::default()
    .hash_password(password.as_bytes(), &salt)?
    .to_string();
```

#### Verification Steps
- [ ] Passwords hashed with `Argon2id` or `scrypt`.
- [ ] Cookies are `HttpOnly`, `Secure`, and `SameSite=Strict/Lax`.
- [ ] Authorization checks performed at the handler level.
- [ ] JWTs (if used) have short expiration and validated signatures.

### 5. XSS Prevention

#### Sanitize User-Provided HTML
Use `ammonia` to clean any HTML intended for rendering.

```rust
let unsafe_html = "<img src=x onerror=alert(1)><b>Hello</b>";
let clean_html = ammonia::clean(unsafe_html);
// Result: "<b>Hello</b>"
```

#### Verification Steps
- [ ] User-provided strings sanitized before being rendered as HTML.
- [ ] Content Security Policy (CSP) headers implemented.
- [ ] Templates (Tera/Askama) set to auto-escape by default.

### 6. Rate Limiting

#### API Throttling
Use `tower-governor` (for Axum) or `governor` to prevent brute force.

```rust
let governor_conf = Box::new(
    GovernorConfigBuilder::default()
        .per_second(2)
        .burst_size(5)
        .finish()
        .unwrap(),
);

let app = Router::new()
    .route("/api/login", post(login))
    .layer(GovernorLayer { config: &governor_conf });
```

#### Verification Steps
- [ ] Rate limiting applied to all auth/sensitive endpoints.
- [ ] Stricter limits on heavy database queries.

### 7. Blockchain (Solana/Anchor)

#### Arithmetic Safety
```rust
// ❌ WRONG: Potential overflow
let total = a + b;

// ✅ CORRECT: Checked math
let total = a.checked_add(b).ok_or(error!(ErrorCode::Overflow))?;
```

#### Signer and Ownership Checks
```rust
// Anchor enforces this via attributes
#[derive(Accounts)]
pub struct UpdateConfig<'info> {
    #[account(mut, has_one = admin)]
    pub config: Account<'info, GlobalConfig>,
    pub admin: Signer<'info>, // Must sign the transaction
}
```

#### Verification Steps
- [ ] All arithmetic uses `checked_`, `saturating_`, or `safe_` methods.
- [ ] Signer checks verified for all authority accounts.
- [ ] Account ownership and discriminators verified.

### 8. Logging and Errors

#### ❌ NEVER Log PII or Secrets
```rust
// DANGEROUS: Logs the password
error!("Failed login for {} with password {}", email, password);
```

#### ✅ ALWAYS Redact Sensitive Info
```rust
error!("Failed login attempt for email: {}", email);
// Detailed error only in internal tracing spans
```

#### Verification Steps
- [ ] No PII (emails, names, tokens) in standard logs.
- [ ] Generic error messages returned to the user (no stack traces).
- [ ] Internal errors logged with enough context for debugging.

### 9. Dependency Security



#### Audit Crates
```bash
# Check for vulnerabilities in dependencies
cargo audit

# Deny crates with specific licenses or known issues
cargo deny check
```

#### Verification Steps
- [ ] `Cargo.lock` is committed to Git.
- [ ] `cargo audit` runs in CI/CD.
- [ ] Minimal use of `unsafe` code; all `unsafe` blocks reviewed.

---

## Pre-Deployment Checklist

- [ ] **Environment**: No `.env` files in production; use platform secrets.
- [ ] **Audit**: `cargo audit` passed with zero vulnerabilities.
- [ ] **Overflows**: Compiled with overflow checks (enabled by default in dev, use `checked_` math for prod).
- [ ] **Headers**: HSTS, CSP, and X-Frame-Options configured.
- [ ] **Database**: RLS (if using Postgres) or minimal user roles set.
- [ ] **Errors**: User-facing errors are generic; logs are sanitized.

---

**Remember**: In Rust, memory safety is guaranteed, but logic safety is your responsibility. Always assume user input is malicious and that environment variables are missing.
