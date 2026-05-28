# Security Headers Reference

## Table of Contents
1. [Essential Headers](#essential-headers)
2. [Content Security Policy](#csp)
3. [CORS Configuration](#cors)
4. [Cookie Security](#cookies)
5. [Spring Security Configuration](#spring-config)

## Essential Headers

### Header Summary
| Header | Purpose | Recommended Value |
|--------|---------|-------------------|
| `Strict-Transport-Security` | Force HTTPS | `max-age=31536000; includeSubDomains` |
| `X-Content-Type-Options` | Prevent MIME sniffing | `nosniff` |
| `X-Frame-Options` | Prevent clickjacking | `DENY` |
| `Content-Security-Policy` | Control resource loading | See CSP section |
| `Referrer-Policy` | Control referrer info | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | Control browser features | `geolocation=(), camera=()` |
| `Cache-Control` | Prevent sensitive data caching | `no-store` for sensitive responses |

### HSTS (HTTP Strict Transport Security)
```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```
- `max-age`: Seconds browser should remember HTTPS-only
- `includeSubDomains`: Apply to all subdomains
- `preload`: Submit to browser preload lists

### X-Content-Type-Options
```
X-Content-Type-Options: nosniff
```
Prevents browsers from MIME-sniffing away from declared Content-Type.

### X-Frame-Options
```
X-Frame-Options: DENY
```
Options: `DENY`, `SAMEORIGIN`, `ALLOW-FROM uri` (deprecated)

## Content Security Policy (CSP) {#csp}

### Basic API CSP
```
Content-Security-Policy: default-src 'none'; frame-ancestors 'none'
```

### Web Application CSP
```
Content-Security-Policy: 
    default-src 'self';
    script-src 'self' 'nonce-{random}';
    style-src 'self' 'unsafe-inline';
    img-src 'self' data: https://cdn.example.com;
    font-src 'self' https://fonts.googleapis.com;
    connect-src 'self' https://api.example.com;
    frame-ancestors 'none';
    form-action 'self';
    base-uri 'self';
    upgrade-insecure-requests;
```

### CSP Directives Reference
| Directive | Controls |
|-----------|----------|
| `default-src` | Fallback for other directives |
| `script-src` | JavaScript sources |
| `style-src` | CSS sources |
| `img-src` | Image sources |
| `font-src` | Font sources |
| `connect-src` | XHR, WebSocket, fetch |
| `frame-src` | iframe sources |
| `frame-ancestors` | Who can embed this page |
| `form-action` | Form submission targets |
| `base-uri` | Restrict `<base>` element |

### CSP Source Values
| Value | Meaning |
|-------|---------|
| `'self'` | Same origin |
| `'none'` | Block all |
| `'unsafe-inline'` | Allow inline scripts/styles (avoid) |
| `'unsafe-eval'` | Allow eval() (avoid) |
| `'nonce-{value}'` | Allow specific inline with nonce |
| `'strict-dynamic'` | Trust scripts loaded by trusted scripts |
| `https:` | Any HTTPS source |
| `data:` | data: URIs |

### Nonce-Based CSP
```java
@Component
public class CspNonceFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, 
                                    HttpServletResponse response,
                                    FilterChain chain) {
        String nonce = generateSecureNonce();
        request.setAttribute("cspNonce", nonce);
        
        response.setHeader("Content-Security-Policy", 
            String.format("script-src 'self' 'nonce-%s'", nonce));
        
        chain.doFilter(request, response);
    }
    
    private String generateSecureNonce() {
        byte[] bytes = new byte[16];
        new SecureRandom().nextBytes(bytes);
        return Base64.getEncoder().encodeToString(bytes);
    }
}

// In template
<script nonce="${cspNonce}">
    // This script will execute
</script>
```

### Report-Only Mode (Testing)
```
Content-Security-Policy-Report-Only: default-src 'self'; report-uri /csp-report
```

## CORS Configuration {#cors}

### CORS Headers
| Header | Purpose |
|--------|---------|
| `Access-Control-Allow-Origin` | Allowed origins |
| `Access-Control-Allow-Methods` | Allowed HTTP methods |
| `Access-Control-Allow-Headers` | Allowed request headers |
| `Access-Control-Expose-Headers` | Headers readable by client |
| `Access-Control-Allow-Credentials` | Allow cookies/auth |
| `Access-Control-Max-Age` | Preflight cache duration |

### Secure CORS Configuration
```java
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    
    // NEVER use "*" with credentials
    config.setAllowedOrigins(List.of(
        "https://app.example.com",
        "https://admin.example.com"
    ));
    
    // Or use pattern matching
    config.setAllowedOriginPatterns(List.of(
        "https://*.example.com"
    ));
    
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
    config.setAllowedHeaders(List.of("Authorization", "Content-Type", "X-Request-ID"));
    config.setExposedHeaders(List.of("X-Request-ID", "X-RateLimit-Remaining"));
    config.setAllowCredentials(true);
    config.setMaxAge(3600L);  // 1 hour preflight cache
    
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/api/**", config);
    return source;
}
```

### CORS Security Pitfalls

❌ **Dangerous: Reflect Origin**
```java
// NEVER do this
String origin = request.getHeader("Origin");
response.setHeader("Access-Control-Allow-Origin", origin);
```

❌ **Dangerous: Wildcard with Credentials**
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
// Browsers block this, but configuration is wrong
```

✅ **Safe: Explicit Allowlist**
```java
private static final Set<String> ALLOWED_ORIGINS = Set.of(
    "https://app.example.com",
    "https://admin.example.com"
);

String origin = request.getHeader("Origin");
if (ALLOWED_ORIGINS.contains(origin)) {
    response.setHeader("Access-Control-Allow-Origin", origin);
}
```

## Cookie Security {#cookies}

### Secure Cookie Attributes
| Attribute | Purpose |
|-----------|---------|
| `Secure` | HTTPS only |
| `HttpOnly` | No JavaScript access |
| `SameSite` | CSRF protection |
| `Path` | Scope to path |
| `Domain` | Scope to domain |
| `Max-Age` | Expiration |

### SameSite Values
| Value | Behavior |
|-------|----------|
| `Strict` | Never sent cross-site |
| `Lax` | Sent on top-level navigation GET |
| `None` | Sent cross-site (requires Secure) |

### Spring Cookie Configuration
```java
// Session cookie
server:
  servlet:
    session:
      cookie:
        secure: true
        http-only: true
        same-site: strict
        name: __Host-SESSION

// Custom cookie
ResponseCookie cookie = ResponseCookie.from("token", value)
    .secure(true)
    .httpOnly(true)
    .sameSite("Strict")
    .path("/api")
    .maxAge(Duration.ofHours(1))
    .build();

response.addHeader(HttpHeaders.SET_COOKIE, cookie.toString());
```

### Cookie Prefixes
| Prefix | Requirements |
|--------|--------------|
| `__Secure-` | Must have Secure flag |
| `__Host-` | Secure + no Domain + Path=/ |

```
Set-Cookie: __Host-token=abc; Secure; Path=/; HttpOnly; SameSite=Strict
```

## Spring Security Configuration {#spring-config}

### Complete Headers Configuration
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .headers(headers -> headers
                // HSTS
                .httpStrictTransportSecurity(hsts -> hsts
                    .maxAgeInSeconds(31536000)
                    .includeSubDomains(true)
                    .preload(true))
                
                // Prevent clickjacking
                .frameOptions(frame -> frame.deny())
                
                // Prevent MIME sniffing
                .contentTypeOptions(Customizer.withDefaults())
                
                // CSP
                .contentSecurityPolicy(csp -> csp
                    .policyDirectives("default-src 'self'; frame-ancestors 'none'"))
                
                // Referrer policy
                .referrerPolicy(referrer -> referrer
                    .policy(ReferrerPolicyHeaderWriter.ReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN))
                
                // Permissions policy
                .permissionsPolicy(permissions -> permissions
                    .policy("geolocation=(), microphone=(), camera=()"))
                
                // Cache control for sensitive data
                .cacheControl(Customizer.withDefaults()))
            
            // CORS
            .cors(cors -> cors.configurationSource(corsConfigurationSource()));
        
        return http.build();
    }
}
```

### Per-Response Headers
```java
@GetMapping("/sensitive-data")
public ResponseEntity<SensitiveData> getSensitiveData() {
    return ResponseEntity.ok()
        .cacheControl(CacheControl.noStore())
        .header("X-Content-Type-Options", "nosniff")
        .body(data);
}
```

### Testing Headers
```java
@Test
void securityHeaders_arePresent() throws Exception {
    mockMvc.perform(get("/api/test"))
        .andExpect(header().string("Strict-Transport-Security", 
            containsString("max-age=")))
        .andExpect(header().string("X-Content-Type-Options", "nosniff"))
        .andExpect(header().string("X-Frame-Options", "DENY"))
        .andExpect(header().exists("Content-Security-Policy"));
}
```
