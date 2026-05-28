---
name: security-checker
description: Performs security audit on code changes checking for OWASP Top 10 vulnerabilities
---

# Security Checker Skill

Bu skill, kod değişikliklerinde güvenlik kontrolü yapar.

## Ne Zaman Kullan

- Yeni endpoint eklendiğinde
- Kullanıcı input'u işlendiğinde
- Veritabanı sorgusu yazıldığında
- Authentication/authorization kodunda

## OWASP Top 10 Kontrolleri

### A01: Broken Access Control

```csharp
// ❌ YANLIŞ: Authorization yok
[HttpGet("{id}")]
public async Task<IActionResult> GetOrder(Guid id) { }

// ✅ DOĞRU: Authorization var
[HttpGet("{id}")]
[Authorize]
public async Task<IActionResult> GetOrder(Guid id)
{
    var order = await _repository.GetByIdAsync(id, ct);

    // Resource ownership check
    if (order.UserId != _currentUser.Id)
        throw new ForbiddenException();
}
```

### A02: Cryptographic Failures

```csharp
// ❌ YANLIŞ: Plain text password
user.Password = request.Password;

// ✅ DOĞRU: Hashed password
user.PasswordHash = _passwordHasher.HashPassword(user, request.Password);

// ❌ YANLIŞ: Hardcoded secret
var key = "my-secret-key-123";

// ✅ DOĞRU: Configuration'dan
var key = _configuration["Jwt:Secret"];
```

### A03: Injection

```csharp
// ❌ YANLIŞ: SQL Injection
var sql = $"SELECT * FROM products WHERE name = '{name}'";
await _context.Database.ExecuteSqlRawAsync(sql);

// ✅ DOĞRU: Parameterized query
await _context.Products.Where(p => p.Name == name).ToListAsync();

// ✅ DOĞRU: Parameterized raw SQL
await _context.Database.ExecuteSqlAsync(
    $"SELECT * FROM products WHERE name = {name}");
```

### A04: Insecure Design

```csharp
// ❌ YANLIŞ: Rate limiting yok
[HttpPost("login")]
public async Task<IActionResult> Login(LoginRequest request) { }

// ✅ DOĞRU: Rate limiting var
[HttpPost("login")]
[EnableRateLimiting("auth")]
public async Task<IActionResult> Login(LoginRequest request) { }
```

### A05: Security Misconfiguration

```csharp
// ❌ YANLIŞ: Detaylı error production'da
if (env.IsDevelopment())
    app.UseDeveloperExceptionPage();
else
    app.UseDeveloperExceptionPage(); // YANLIŞ!

// ✅ DOĞRU
if (env.IsDevelopment())
    app.UseDeveloperExceptionPage();
else
    app.UseExceptionHandler("/error");
```

### A07: Auth Failures

```csharp
// ❌ YANLIŞ: Weak password policy
RuleFor(x => x.Password)
    .MinimumLength(4);

// ✅ DOĞRU: Strong password policy
RuleFor(x => x.Password)
    .MinimumLength(12)
    .Matches("[A-Z]").WithMessage("Uppercase required")
    .Matches("[a-z]").WithMessage("Lowercase required")
    .Matches("[0-9]").WithMessage("Digit required")
    .Matches("[^a-zA-Z0-9]").WithMessage("Special char required");
```

### A09: Logging Failures

```csharp
// ❌ YANLIŞ: Sensitive data logging
_logger.LogInformation("User {Email} logged in with password {Password}",
    email, password);

// ✅ DOĞRU: Masked logging
_logger.LogInformation("User {Email} logged in", LogMasking.MaskEmail(email));
```

## Quick Scan Patterns

```bash
# Hardcoded secrets
grep -rn "password\s*=" --include="*.cs" .
grep -rn "secret\s*=" --include="*.cs" .
grep -rn "apikey\s*=" --include="*.cs" .

# SQL injection risk
grep -rn "ExecuteSqlRaw\|FromSqlRaw" --include="*.cs" .
grep -rn "string\.Format.*SELECT" --include="*.cs" .

# Missing authorization
grep -rn "\[Http" --include="*.cs" . | grep -v "\[Authorize"

# Sensitive logging
grep -rn "LogInformation.*password\|LogDebug.*token" --include="*.cs" .
```

## Severity Levels

- **CRITICAL**: Immediate fix required (SQL injection, auth bypass)
- **HIGH**: Fix before merge (missing auth, weak crypto)
- **MEDIUM**: Plan to fix (verbose errors, missing rate limit)
- **LOW**: Consider fixing (info disclosure, missing headers)
