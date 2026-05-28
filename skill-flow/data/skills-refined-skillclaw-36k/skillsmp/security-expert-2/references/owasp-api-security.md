# OWASP API Security Top 10 Reference

## Table of Contents
1. [API1 - Broken Object Level Authorization](#api1-bola)
2. [API2 - Broken Authentication](#api2-broken-auth)
3. [API3 - Broken Object Property Level Authorization](#api3-bopla)
4. [API4 - Unrestricted Resource Consumption](#api4-resource)
5. [API5 - Broken Function Level Authorization](#api5-bfla)
6. [API6 - Unrestricted Access to Sensitive Business Flows](#api6-business-flows)
7. [API7 - Server Side Request Forgery](#api7-ssrf)
8. [API8 - Security Misconfiguration](#api8-misconfig)
9. [API9 - Improper Inventory Management](#api9-inventory)
10. [API10 - Unsafe Consumption of APIs](#api10-unsafe-consumption)

## API1 - Broken Object Level Authorization (BOLA) {#api1-bola}

### Vulnerability
Attacker changes object ID to access other users' data.

```
GET /api/users/123/documents  → Own documents
GET /api/users/456/documents  → Other user's documents (BOLA!)
```

### Prevention
```java
@GetMapping("/documents/{documentId}")
public Document getDocument(@PathVariable String documentId, Authentication auth) {
    Document doc = documentService.findById(documentId);
    
    // ALWAYS verify ownership/access
    if (!doc.getOwnerId().equals(auth.getName()) && 
        !hasPermission(auth, doc, "read")) {
        throw new AccessDeniedException("Not authorized");
    }
    
    return doc;
}

// Better: Use method security
@PreAuthorize("@documentSecurity.canRead(#documentId, authentication)")
@GetMapping("/documents/{documentId}")
public Document getDocument(@PathVariable String documentId) {
    return documentService.findById(documentId);
}
```

### Testing
```bash
# Get legitimate document
curl -H "Authorization: Bearer $TOKEN_USER_A" /api/documents/doc-123

# Try another user's document
curl -H "Authorization: Bearer $TOKEN_USER_A" /api/documents/doc-456
# Should return 403, not the document
```

## API2 - Broken Authentication {#api2-broken-auth}

### Vulnerabilities
- Weak passwords allowed
- No brute-force protection
- Credential stuffing
- JWT issues (weak secret, alg confusion)

### Prevention
```java
// Rate limiting for auth endpoints
@Bean
public RateLimiter authRateLimiter() {
    return RateLimiter.of("auth", RateLimiterConfig.custom()
        .limitForPeriod(5)
        .limitRefreshPeriod(Duration.ofMinutes(1))
        .timeoutDuration(Duration.ZERO)
        .build());
}

// Account lockout
@Service
public class LoginAttemptService {
    private final LoadingCache<String, Integer> attempts = CacheBuilder.newBuilder()
        .expireAfterWrite(15, TimeUnit.MINUTES)
        .build(CacheLoader.from(() -> 0));
    
    public void loginFailed(String username) {
        int current = attempts.getUnchecked(username);
        attempts.put(username, current + 1);
    }
    
    public boolean isBlocked(String username) {
        return attempts.getUnchecked(username) >= 5;
    }
}

// Password policy
@Bean
public PasswordEncoder passwordEncoder() {
    return new BCryptPasswordEncoder(12);  // Cost factor 12
}
```

## API3 - Broken Object Property Level Authorization (BOPLA) {#api3-bopla}

### Vulnerabilities
- Mass assignment: User modifies fields they shouldn't
- Excessive data exposure: API returns more than needed

### Prevention - Mass Assignment
```java
// BAD: Binding directly to entity
@PutMapping("/users/{id}")
public User updateUser(@PathVariable Long id, @RequestBody User user) {
    return userRepository.save(user);  // User could set isAdmin=true!
}

// GOOD: Use DTOs
public record UserUpdateRequest(
    String name,
    String email
    // No role, no isAdmin
) {}

@PutMapping("/users/{id}")
public UserResponse updateUser(@PathVariable Long id, 
                                @RequestBody UserUpdateRequest request,
                                Authentication auth) {
    User user = userRepository.findById(id).orElseThrow();
    
    // Verify ownership
    if (!user.getId().equals(auth.getName())) {
        throw new AccessDeniedException("Not authorized");
    }
    
    // Only update allowed fields
    user.setName(request.name());
    user.setEmail(request.email());
    
    return UserResponse.from(userRepository.save(user));
}
```

### Prevention - Data Exposure
```java
// BAD: Return entity with all fields
@GetMapping("/users/{id}")
public User getUser(@PathVariable Long id) {
    return userRepository.findById(id).orElseThrow();
    // Exposes: password hash, internal IDs, etc.
}

// GOOD: Return only needed fields
public record UserPublicResponse(
    String id,
    String name,
    String avatarUrl
) {
    public static UserPublicResponse from(User user) {
        return new UserPublicResponse(user.getId(), user.getName(), user.getAvatarUrl());
    }
}
```

## API4 - Unrestricted Resource Consumption {#api4-resource}

### Vulnerabilities
- No rate limiting
- Unlimited pagination
- Uncontrolled file uploads
- Expensive operations without limits

### Prevention
```java
// Rate limiting
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.addFilterBefore(rateLimitFilter, UsernamePasswordAuthenticationFilter.class);
    return http.build();
}

// Pagination limits
@GetMapping("/documents")
public Page<Document> listDocuments(
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "20") int size) {
    
    // Enforce maximum page size
    int safeSize = Math.min(size, 100);
    return documentRepository.findAll(PageRequest.of(page, safeSize));
}

// File upload limits
spring:
  servlet:
    multipart:
      max-file-size: 10MB
      max-request-size: 10MB

// Timeout for expensive operations
@Transactional(timeout = 30)  // 30 second timeout
public Report generateReport(ReportRequest request) { }
```

## API5 - Broken Function Level Authorization (BFLA) {#api5-bfla}

### Vulnerability
User accesses admin functions by guessing URLs.

```
POST /api/users         → Create user (user function)
DELETE /api/users/123   → Delete user (admin function - BFLA!)
```

### Prevention
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.authorizeHttpRequests(auth -> auth
            // Public endpoints
            .requestMatchers(HttpMethod.GET, "/api/public/**").permitAll()
            
            // User endpoints
            .requestMatchers("/api/users/me/**").authenticated()
            
            // Admin endpoints - explicit authorization
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .requestMatchers(HttpMethod.DELETE, "/api/**").hasRole("ADMIN")
            
            // Default deny
            .anyRequest().denyAll()
        );
        return http.build();
    }
}

// Method-level security as backup
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/users/{id}")
public void deleteUser(@PathVariable Long id) { }
```

## API6 - Unrestricted Access to Sensitive Business Flows {#api6-business-flows}

### Vulnerabilities
- Automated ticket scalping
- Mass account creation
- Referral fraud
- Scraping

### Prevention
```java
// CAPTCHA for sensitive flows
@PostMapping("/purchase")
public Order createOrder(@RequestBody OrderRequest request,
                         @RequestHeader("X-Captcha-Token") String captchaToken) {
    if (!captchaService.verify(captchaToken)) {
        throw new BadRequestException("Invalid captcha");
    }
    return orderService.create(request);
}

// Business logic rate limits
@Service
public class OrderService {
    public Order create(OrderRequest request, User user) {
        // Limit orders per user per time period
        int recentOrders = orderRepository.countByUserIdAndCreatedAtAfter(
            user.getId(), 
            Instant.now().minus(1, ChronoUnit.HOURS)
        );
        
        if (recentOrders >= 3) {
            throw new RateLimitException("Too many orders");
        }
        
        return createOrder(request, user);
    }
}

// Device fingerprinting
@PostMapping("/register")
public void register(@RequestBody RegistrationRequest request,
                     @RequestHeader("X-Device-Fingerprint") String fingerprint) {
    if (deviceService.isSuspicious(fingerprint)) {
        throw new BadRequestException("Registration blocked");
    }
}
```

## API7 - Server Side Request Forgery (SSRF) {#api7-ssrf}

### Vulnerability
API makes requests to user-controlled URLs.

```json
POST /api/import
{"url": "http://internal-admin-service/delete-all"}
```

### Prevention
```java
@Service
public class UrlFetcher {
    
    private static final Set<String> ALLOWED_HOSTS = Set.of(
        "api.trusted-partner.com",
        "cdn.example.com"
    );
    
    public byte[] fetch(String urlString) {
        URL url;
        try {
            url = new URL(urlString);
        } catch (MalformedURLException e) {
            throw new BadRequestException("Invalid URL");
        }
        
        // Block internal addresses
        String host = url.getHost();
        InetAddress address = InetAddress.getByName(host);
        if (address.isLoopbackAddress() || 
            address.isSiteLocalAddress() ||
            address.isLinkLocalAddress()) {
            throw new BadRequestException("Internal URLs not allowed");
        }
        
        // Allowlist approach (preferred)
        if (!ALLOWED_HOSTS.contains(host)) {
            throw new BadRequestException("Host not in allowlist");
        }
        
        // Only allow HTTPS
        if (!"https".equals(url.getProtocol())) {
            throw new BadRequestException("Only HTTPS allowed");
        }
        
        return httpClient.fetch(url);
    }
}
```

## API8 - Security Misconfiguration {#api8-misconfig}

### Common Issues
- Verbose error messages
- Default credentials
- Unnecessary features enabled
- Missing security headers
- Permissive CORS

### Prevention Checklist
```yaml
# application.yml
server:
  error:
    include-message: never
    include-stacktrace: never
    include-binding-errors: never

spring:
  jackson:
    default-property-inclusion: non_null
    serialization:
      fail-on-empty-beans: false
```

```java
// Security headers
http.headers(headers -> headers
    .contentSecurityPolicy(csp -> csp.policyDirectives(
        "default-src 'self'; frame-ancestors 'none'"))
    .frameOptions(frame -> frame.deny())
    .contentTypeOptions(Customizer.withDefaults()));

// Strict CORS
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("https://app.example.com"));  // NOT *
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
    config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
    config.setAllowCredentials(true);
    // ...
}

// Disable unused endpoints
management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
```

## API9 - Improper Inventory Management {#api9-inventory}

### Issues
- Old API versions still running
- Unpatched dependencies
- Shadow/zombie APIs
- Missing documentation

### Prevention
```java
// API versioning
@RestController
@RequestMapping("/api/v2/users")
public class UserControllerV2 { }

// Deprecation headers
@GetMapping("/api/v1/users")
@Deprecated
public ResponseEntity<List<User>> listUsersV1() {
    return ResponseEntity.ok()
        .header("Deprecation", "true")
        .header("Sunset", "Sat, 1 Jan 2025 00:00:00 GMT")
        .header("Link", "</api/v2/users>; rel=\"successor-version\"")
        .body(userService.findAll());
}

// OpenAPI documentation
@OpenAPIDefinition(
    info = @Info(title = "User API", version = "2.0"),
    servers = @Server(url = "https://api.example.com")
)
public class OpenApiConfig { }
```

## API10 - Unsafe Consumption of APIs {#api10-unsafe-consumption}

### Vulnerability
Trusting data from third-party APIs without validation.

### Prevention
```java
@Service
public class ThirdPartyIntegration {
    
    public ProcessedData fetchAndProcess(String externalId) {
        // Fetch from third party
        ExternalResponse response = externalClient.fetch(externalId);
        
        // NEVER trust external data
        // Validate all fields
        if (response.getId() == null || response.getId().length() > 100) {
            throw new ValidationException("Invalid external ID");
        }
        
        // Sanitize for storage/display
        String safeName = Jsoup.clean(response.getName(), Safelist.none());
        
        // Validate URLs before following
        if (response.getCallbackUrl() != null) {
            validateUrl(response.getCallbackUrl());
        }
        
        return new ProcessedData(response.getId(), safeName);
    }
    
    private void validateUrl(String url) {
        // Same SSRF protections as API7
        // ...
    }
}
```
