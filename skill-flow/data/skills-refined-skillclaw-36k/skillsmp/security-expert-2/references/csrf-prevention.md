# CSRF Prevention Reference

## Table of Contents
1. [CSRF Attack Mechanics](#csrf-mechanics)
2. [When CSRF Protection Is Needed](#when-needed)
3. [Synchronizer Token Pattern](#synchronizer-token)
4. [Double Submit Cookie Pattern](#double-submit)
5. [SameSite Cookie Deep Dive](#samesite)
6. [Spring Security CSRF Config](#spring-csrf)
7. [SPA/API CSRF Protection](#spa-api)

## CSRF Attack Mechanics {#csrf-mechanics}

### What Is CSRF?
Cross-Site Request Forgery tricks authenticated users into making unintended requests.

### Attack Flow
```
1. User logs into bank.com (gets session cookie)
2. User visits evil.com
3. evil.com contains: <form action="https://bank.com/transfer" method="POST">
4. Form auto-submits with user's cookies
5. Bank processes transfer (user authenticated via cookie)
```

### Why Cookies Alone Aren't Enough
Browsers automatically attach cookies to requests, even from other origins:

```html
<!-- On evil.com -->
<form action="https://bank.com/api/transfer" method="POST">
  <input type="hidden" name="to" value="attacker" />
  <input type="hidden" name="amount" value="10000" />
</form>
<script>document.forms[0].submit();</script>
```

The user's bank.com session cookie is sent automatically.

### What CSRF Can Do
- State-changing actions (transfer money, change password)
- Actions the user is authorized to perform
- NOT data exfiltration (attacker can't read response)

## When CSRF Protection Is Needed {#when-needed}

### Protection Required
| Scenario | Need CSRF Protection? |
|----------|----------------------|
| Session cookies (stateful) | **Yes** |
| Form submissions | **Yes** |
| AJAX with cookies | **Yes** |
| Actions with side effects | **Yes** |

### Protection Optional/Not Needed
| Scenario | Need CSRF Protection? |
|----------|----------------------|
| Stateless JWT in header | No (not auto-attached) |
| Public read-only endpoints | No |
| CORS-protected API (no credentials) | No |
| Requests requiring custom headers | Partial protection |

### Decision Matrix
```
Is request state-changing?
  └─ No → No CSRF protection needed
  └─ Yes → Is auth via cookies?
            └─ No (JWT in header) → No CSRF protection needed
            └─ Yes → CSRF protection required
```

## Synchronizer Token Pattern {#synchronizer-token}

### How It Works
1. Server generates unique token per session
2. Token embedded in forms/stored for AJAX
3. Server validates token on state-changing requests
4. Attacker can't guess token (not in cookies)

### Server-Side Implementation (Spring)
```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf
                // Use cookie-based token repository for SPAs
                .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
                // Or session-based for traditional apps
                // .csrfTokenRepository(new HttpSessionCsrfTokenRepository())
            );
        return http.build();
    }
}
```

### Form Integration (Thymeleaf)
```html
<!-- Token automatically included -->
<form th:action="@{/transfer}" method="post">
    <input type="hidden" th:name="${_csrf.parameterName}" th:value="${_csrf.token}"/>
    <!-- or just let Thymeleaf handle it automatically -->
</form>
```

### Token Validation
Spring Security automatically:
1. Generates token on session creation
2. Validates token on POST/PUT/DELETE/PATCH
3. Rejects requests with invalid/missing tokens

## Double Submit Cookie Pattern {#double-submit}

### How It Works
1. Server sets CSRF token in cookie (readable by JS)
2. Client reads cookie, sends token in header/body
3. Server compares cookie value with header/body value
4. Attacker can't read cookie from different origin

### Why It Works
- Attacker can trigger requests with cookies (auto-attached)
- Attacker CANNOT read cookie values (same-origin policy)
- So attacker can't put correct token in header/body

### Implementation
```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.csrf(csrf -> csrf
        // Cookie readable by JavaScript
        .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
        // For SPAs: expect token in header
        .csrfTokenRequestHandler(new SpaCsrfTokenRequestHandler())
    );
    return http.build();
}

// Custom handler for SPA pattern
public class SpaCsrfTokenRequestHandler extends CsrfTokenRequestAttributeHandler {

    private final CsrfTokenRequestHandler delegate = new XorCsrfTokenRequestAttributeHandler();

    @Override
    public void handle(HttpServletRequest request, HttpServletResponse response,
                       Supplier<CsrfToken> csrfToken) {
        delegate.handle(request, response, csrfToken);
    }

    @Override
    public String resolveCsrfTokenValue(HttpServletRequest request, CsrfToken csrfToken) {
        // Check header first (SPA), then parameter (forms)
        String headerValue = request.getHeader(csrfToken.getHeaderName());
        return (headerValue != null) ? headerValue :
               delegate.resolveCsrfTokenValue(request, csrfToken);
    }
}
```

### Client-Side (React/Fetch)
```typescript
// Read CSRF token from cookie
function getCsrfToken(): string {
  const match = document.cookie.match(/XSRF-TOKEN=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : '';
}

// Include in requests
async function securePost(url: string, data: unknown) {
  const response = await fetch(url, {
    method: 'POST',
    credentials: 'include',  // Send cookies
    headers: {
      'Content-Type': 'application/json',
      'X-XSRF-TOKEN': getCsrfToken(),  // CSRF token in header
    },
    body: JSON.stringify(data),
  });
  return response.json();
}
```

## SameSite Cookie Deep Dive {#samesite}

### SameSite Values
| Value | Cross-Site Requests | Top-Level Navigation |
|-------|--------------------|--------------------|
| `Strict` | Never sent | Never sent |
| `Lax` | Never sent | Sent (GET only) |
| `None` | Always sent* | Always sent* |

*Requires `Secure` flag

### Lax (Default in Modern Browsers)
```java
// Cookie sent on:
// - Same-site requests (always)
// - Cross-site top-level navigation GET (clicking links)

// Cookie NOT sent on:
// - Cross-site POST/PUT/DELETE
// - Cross-site AJAX
// - Cross-site iframes
```

### Strict
```java
// Cookie only sent on same-site requests
// Never sent on cross-site requests, even navigation

// Good for: highly sensitive actions
// Bad for: usability (user coming from email link won't be logged in)
```

### Spring Configuration
```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.sessionManagement(session -> session
        .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
    );
    return http.build();
}

// application.yml
server:
  servlet:
    session:
      cookie:
        same-site: lax  # or strict
        secure: true
        http-only: true
```

### SameSite Limitations
- Not supported in older browsers
- `Lax` allows GET navigation (logout CSRF still possible)
- Cross-origin scenarios (subdomains, OAuth) require `None`

**Best Practice**: Use SameSite=Lax + synchronizer tokens

## Spring Security CSRF Config {#spring-csrf}

### Enable CSRF (Default)
```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    // CSRF enabled by default
    http.csrf(Customizer.withDefaults());
    return http.build();
}
```

### Disable for Stateless APIs
```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http
        .csrf(csrf -> csrf.disable())  // Only for stateless JWT APIs
        .sessionManagement(session -> session
            .sessionCreationPolicy(SessionCreationPolicy.STATELESS));
    return http.build();
}
```

### Selective CSRF
```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.csrf(csrf -> csrf
        // Ignore CSRF for specific paths
        .ignoringRequestMatchers("/api/webhooks/**")
        .ignoringRequestMatchers("/api/public/**")
    );
    return http.build();
}
```

### Custom Token Repository
```java
@Bean
public CsrfTokenRepository csrfTokenRepository() {
    // Cookie-based for SPAs
    CookieCsrfTokenRepository repository = CookieCsrfTokenRepository.withHttpOnlyFalse();
    repository.setCookieName("XSRF-TOKEN");
    repository.setHeaderName("X-XSRF-TOKEN");
    repository.setCookiePath("/");
    return repository;
}
```

### Testing with CSRF
```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    void createUser_shouldRequireCsrf() throws Exception {
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\":\"test\"}"))
            .andExpect(status().isForbidden());  // No CSRF token
    }

    @Test
    void createUser_withCsrf_shouldSucceed() throws Exception {
        mockMvc.perform(post("/api/users")
                .with(csrf())  // Add CSRF token
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\":\"test\"}"))
            .andExpect(status().isCreated());
    }
}
```

## SPA/API CSRF Protection {#spa-api}

### Custom Header Defense
Require custom header that can't be set cross-origin:

```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    http.csrf(csrf -> csrf.disable())  // Disable standard CSRF
        .addFilterBefore(new CustomHeaderFilter(), UsernamePasswordAuthenticationFilter.class);
    return http.build();
}

public class CustomHeaderFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {

        if (isStateChanging(request.getMethod())) {
            String customHeader = request.getHeader("X-Requested-With");
            if (!"XMLHttpRequest".equals(customHeader)) {
                response.sendError(HttpServletResponse.SC_FORBIDDEN, "Missing custom header");
                return;
            }
        }
        chain.doFilter(request, response);
    }

    private boolean isStateChanging(String method) {
        return "POST".equals(method) || "PUT".equals(method) ||
               "DELETE".equals(method) || "PATCH".equals(method);
    }
}
```

### Origin/Referer Validation
```java
@Component
public class OriginValidationFilter extends OncePerRequestFilter {

    private static final Set<String> ALLOWED_ORIGINS = Set.of(
        "https://app.example.com",
        "https://admin.example.com"
    );

    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                    HttpServletResponse response,
                                    FilterChain chain) throws ServletException, IOException {

        if (isStateChanging(request.getMethod())) {
            String origin = request.getHeader("Origin");
            String referer = request.getHeader("Referer");

            if (!isValidOrigin(origin, referer)) {
                response.sendError(HttpServletResponse.SC_FORBIDDEN, "Invalid origin");
                return;
            }
        }
        chain.doFilter(request, response);
    }

    private boolean isValidOrigin(String origin, String referer) {
        // Check Origin header first
        if (origin != null) {
            return ALLOWED_ORIGINS.contains(origin);
        }
        // Fall back to Referer
        if (referer != null) {
            try {
                URL url = new URL(referer);
                String refOrigin = url.getProtocol() + "://" + url.getHost();
                return ALLOWED_ORIGINS.contains(refOrigin);
            } catch (MalformedURLException e) {
                return false;
            }
        }
        // No origin info - block by default for state-changing
        return false;
    }
}
```

### React/Next.js Integration
```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL;

async function fetchWithCsrf(url: string, options: RequestInit = {}) {
  // Get CSRF token from cookie (set by backend)
  const csrfToken = getCookie('XSRF-TOKEN');

  const response = await fetch(`${API_BASE}${url}`, {
    ...options,
    credentials: 'include',
    headers: {
      ...options.headers,
      'Content-Type': 'application/json',
      'X-XSRF-TOKEN': csrfToken ?? '',
      'X-Requested-With': 'XMLHttpRequest',
    },
  });

  if (!response.ok) {
    throw new ApiError(response.status, await response.text());
  }

  return response.json();
}

export const api = {
  get: (url: string) => fetchWithCsrf(url, { method: 'GET' }),
  post: (url: string, data: unknown) =>
    fetchWithCsrf(url, { method: 'POST', body: JSON.stringify(data) }),
  put: (url: string, data: unknown) =>
    fetchWithCsrf(url, { method: 'PUT', body: JSON.stringify(data) }),
  delete: (url: string) => fetchWithCsrf(url, { method: 'DELETE' }),
};
```

## Common CSRF Mistakes

### Mistake 1: CSRF Disabled for Convenience
```java
// VULNERABLE: Disabled because "it's just an API"
http.csrf(csrf -> csrf.disable());

// But API uses session cookies for auth = CSRF vulnerable!
```

### Mistake 2: GET Requests with Side Effects
```java
// VULNERABLE: State change on GET (no CSRF protection)
@GetMapping("/api/logout")
public void logout(HttpSession session) {
    session.invalidate();
}

// SAFE: Use POST for state changes
@PostMapping("/api/logout")
public void logout(HttpSession session) {
    session.invalidate();
}
```

### Mistake 3: Token in Cookie Only
```java
// VULNERABLE: Token only in cookie, not validated in header/body
// Attacker can trigger request with cookie auto-attached

// SAFE: Double-submit - require token in both cookie AND header
```

### Mistake 4: Predictable Tokens
```java
// VULNERABLE: Token based on session ID
String token = DigestUtils.md5Hex(session.getId());

// SAFE: Cryptographically random token
String token = UUID.randomUUID().toString();
```

## Quick Reference

### When to Use CSRF Protection
- Session cookies for authentication
- Any state-changing operation
- Traditional form submissions
- AJAX with credentials: 'include'

### When CSRF Can Be Disabled
- Stateless JWT (token in Authorization header)
- Public read-only APIs
- Webhook endpoints (use HMAC signature instead)

### Recommended Approach
1. **SameSite=Lax cookies** (blocks most cross-site requests)
2. **Plus synchronizer token** (defense in depth)
3. **Plus origin validation** (additional layer)
4. **Plus custom header requirement** (for APIs)

### Testing Checklist
- [ ] POST without token returns 403
- [ ] POST with valid token succeeds
- [ ] Token is unique per session
- [ ] Token changes on login
- [ ] GET requests don't have side effects
