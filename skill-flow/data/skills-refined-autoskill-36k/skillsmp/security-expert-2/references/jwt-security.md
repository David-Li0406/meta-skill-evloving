# JWT Security Reference

## Table of Contents
1. [JWT Structure](#jwt-structure)
2. [Common Vulnerabilities](#common-vulnerabilities)
3. [Secure Implementation](#secure-implementation)
4. [Token Storage](#token-storage)
5. [Refresh Token Patterns](#refresh-token-patterns)

## JWT Structure

```
header.payload.signature
```

### Header
```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "key-identifier"
}
```

### Payload (Claims)
```json
{
  "iss": "https://auth.example.com",
  "sub": "user-123",
  "aud": ["api.example.com"],
  "exp": 1700000000,
  "iat": 1699999000,
  "nbf": 1699999000,
  "jti": "unique-token-id",
  "scope": "read write",
  "roles": ["user", "admin"]
}
```

### Required Claim Validations
| Claim | Validation | Risk if Missing |
|-------|------------|-----------------|
| `exp` | Token not expired | Token replay indefinitely |
| `iss` | Matches expected issuer | Accept tokens from attackers |
| `aud` | Contains your service | Cross-service token abuse |
| `nbf` | Current time >= nbf | Premature token use |

## Common Vulnerabilities

### 1. Algorithm Confusion Attack
**Attack**: Change `alg` header from RS256 to HS256, sign with public key
**Prevention**: Explicitly specify allowed algorithms, never trust header
```java
// Spring Boot - explicit algorithm
@Bean
public JwtDecoder jwtDecoder() {
    NimbusJwtDecoder decoder = NimbusJwtDecoder
        .withPublicKey(rsaPublicKey)
        .build();
    decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
        new JwtTimestampValidator(),
        new JwtIssuerValidator("https://auth.example.com")
    ));
    return decoder;
}
```

### 2. None Algorithm Attack
**Attack**: Set `alg` to "none", remove signature
**Prevention**: Reject tokens with alg=none, use allowlist of algorithms

### 3. Key Confusion (JWKS)
**Attack**: Inject malicious key into JWKS endpoint
**Prevention**: Pin expected key IDs, validate JWKS URL, use HTTPS only

### 4. Weak Secret Keys
**Attack**: Brute force HS256 with weak secrets
**Prevention**: Minimum 256-bit entropy for HS256, prefer RS256/ES256

### 5. Missing Signature Validation
**Attack**: Modify payload, keep original signature
**Prevention**: Always verify signature before trusting claims

### 6. Token Sidejacking
**Attack**: Steal token via XSS, MITM, or logs
**Prevention**: 
- Bind token to TLS session (token binding)
- Use short expiry + refresh rotation
- Store in httpOnly cookies (not localStorage)

## Secure Implementation

### Token Generation
```java
public String generateToken(User user) {
    Instant now = Instant.now();
    JwtClaimsSet claims = JwtClaimsSet.builder()
        .issuer("https://auth.example.com")
        .subject(user.getId())
        .audience(List.of("api.example.com"))
        .issuedAt(now)
        .expiresAt(now.plus(15, ChronoUnit.MINUTES))
        .notBefore(now)
        .claim("jti", UUID.randomUUID().toString())
        .claim("roles", user.getRoles())
        .build();
    
    return jwtEncoder.encode(JwtEncoderParameters.from(claims)).getTokenValue();
}
```

### Token Validation Checklist
```java
public void validateToken(Jwt jwt) {
    // 1. Signature verified by JwtDecoder
    
    // 2. Check expiration
    if (jwt.getExpiresAt().isBefore(Instant.now())) {
        throw new JwtValidationException("Token expired");
    }
    
    // 3. Check issuer
    if (!"https://auth.example.com".equals(jwt.getIssuer().toString())) {
        throw new JwtValidationException("Invalid issuer");
    }
    
    // 4. Check audience
    if (!jwt.getAudience().contains("api.example.com")) {
        throw new JwtValidationException("Invalid audience");
    }
    
    // 5. Check not-before
    if (jwt.getNotBefore() != null && jwt.getNotBefore().isAfter(Instant.now())) {
        throw new JwtValidationException("Token not yet valid");
    }
    
    // 6. Optional: Check token not revoked
    if (tokenBlacklist.contains(jwt.getId())) {
        throw new JwtValidationException("Token revoked");
    }
}
```

## Token Storage

### Browser Storage Comparison
| Storage | XSS Risk | CSRF Risk | Recommendation |
|---------|----------|-----------|----------------|
| localStorage | HIGH | None | ❌ Avoid |
| sessionStorage | HIGH | None | ❌ Avoid |
| httpOnly Cookie | Protected | Requires mitigation | ✅ Preferred |
| Memory (JS variable) | Moderate | None | ⚠️ Lost on refresh |

### Secure Cookie Configuration
```java
ResponseCookie cookie = ResponseCookie.from("access_token", token)
    .httpOnly(true)          // Prevent JS access
    .secure(true)            // HTTPS only
    .sameSite("Strict")      // CSRF protection
    .path("/api")            // Limit scope
    .maxAge(Duration.ofMinutes(15))
    .build();
```

## Refresh Token Patterns

### Rotation Pattern (Recommended)
1. Access token: 15 min expiry, stateless
2. Refresh token: 7 days expiry, stored server-side
3. On refresh: Invalidate old refresh token, issue new pair
4. Detect reuse: If old refresh token used, revoke family

```java
public TokenPair refreshTokens(String refreshToken) {
    RefreshTokenEntity stored = refreshTokenRepo.findByToken(refreshToken)
        .orElseThrow(() -> new InvalidTokenException("Unknown refresh token"));
    
    // Detect token reuse (replay attack)
    if (stored.isUsed()) {
        refreshTokenRepo.revokeFamily(stored.getFamilyId());
        throw new SecurityException("Refresh token reuse detected");
    }
    
    // Mark as used
    stored.setUsed(true);
    refreshTokenRepo.save(stored);
    
    // Issue new token pair
    String newAccessToken = generateAccessToken(stored.getUser());
    String newRefreshToken = generateRefreshToken(stored.getUser(), stored.getFamilyId());
    
    return new TokenPair(newAccessToken, newRefreshToken);
}
```

### Token Binding
Bind tokens to client fingerprint to prevent theft:
```java
String fingerprint = generateSecureRandom();
String fingerprintHash = sha256(fingerprint);

// Include hash in JWT
claims.claim("fpt", fingerprintHash);

// Send fingerprint in separate httpOnly cookie
ResponseCookie fpCookie = ResponseCookie.from("__Secure-Fgp", fingerprint)
    .httpOnly(true)
    .secure(true)
    .sameSite("Strict")
    .build();

// On validation, verify fingerprint matches
String providedFingerprint = request.getCookie("__Secure-Fgp");
if (!sha256(providedFingerprint).equals(jwt.getClaim("fpt"))) {
    throw new SecurityException("Token binding mismatch");
}
```
