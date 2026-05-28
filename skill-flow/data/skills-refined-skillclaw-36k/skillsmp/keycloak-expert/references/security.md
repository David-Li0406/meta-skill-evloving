# Security Reference

## Table of Contents
1. [PKCE Configuration](#pkce-configuration)
2. [Security Hardening](#security-hardening)
3. [Token Revocation](#token-revocation)
4. [Monitoring and Observability](#monitoring-and-observability)

## PKCE Configuration

PKCE (Proof Key for Code Exchange) prevents authorization code interception attacks. **Recommended for ALL clients** per OAuth 2.0 Security BCP, including confidential clients.

### When to Use PKCE

| Client Type | PKCE Required? | Reason |
|-------------|---------------|--------|
| Public (SPA, mobile) | **Mandatory** | No client secret to protect code |
| Confidential (backend) | **Recommended** | Defense in depth against code interception |
| Machine-to-machine | Not applicable | Uses client credentials flow |

### Enabling PKCE via Fluent Builder

```java
FluentClientBuilder.forRealm("toolbox")
    .with(keycloakClient)
    .createClient("mobile-app")
        .publicClient()           // No client secret
        .enableStandardFlow()
        .enablePKCE()             // Require PKCE
        .withPkceMethod("S256")   // SHA-256 (recommended)
        .addRedirectUri("myapp://callback")
        .and()
    .apply();
```

### PKCE in Client Configuration (Admin Console)

1. Navigate to: Clients > [client] > Settings
2. Under "Capability config":
   - Set "Proof Key for Code Exchange Code Challenge Method" to `S256`
3. Save

### Enforcing PKCE via Client Policies

Create realm-wide policy to enforce PKCE on all clients:

```java
// In realm configuration
.configureClientPolicy("enforce-pkce")
    .withCondition("any-client")
    .withExecutor("pkce-enforcer")
        .requirePkce(true)
        .allowedMethods("S256")  // Disallow plain
        .and()
    .and()
```

### PKCE Flow (How It Works)

```
1. Client generates:
   - code_verifier: Random 43-128 character string
   - code_challenge: BASE64URL(SHA256(code_verifier))

2. Authorization request includes:
   - code_challenge
   - code_challenge_method=S256

3. Token request includes:
   - code_verifier (original value)

4. Keycloak verifies:
   - SHA256(code_verifier) == code_challenge
```

### Spring Security OAuth2 Client with PKCE

```java
@Configuration
public class OAuth2ClientConfig {

    @Bean
    public ClientRegistrationRepository clientRegistrationRepository() {
        return new InMemoryClientRegistrationRepository(keycloakRegistration());
    }

    private ClientRegistration keycloakRegistration() {
        return ClientRegistration.withRegistrationId("keycloak")
            .clientId("my-client")
            .clientSecret("secret")  // Even with secret, use PKCE
            .authorizationGrantType(AuthorizationGrantType.AUTHORIZATION_CODE)
            .redirectUri("{baseUrl}/login/oauth2/code/{registrationId}")
            .scope("openid", "profile")
            .authorizationUri("https://keycloak.example.com/realms/toolbox/protocol/openid-connect/auth")
            .tokenUri("https://keycloak.example.com/realms/toolbox/protocol/openid-connect/token")
            .jwkSetUri("https://keycloak.example.com/realms/toolbox/protocol/openid-connect/certs")
            .clientAuthenticationMethod(ClientAuthenticationMethod.CLIENT_SECRET_POST)
            .build();
    }

    @Bean
    public OAuth2AuthorizedClientManager authorizedClientManager(
            ClientRegistrationRepository clientRegistrationRepository,
            OAuth2AuthorizedClientRepository authorizedClientRepository) {

        OAuth2AuthorizedClientProvider authorizedClientProvider =
            OAuth2AuthorizedClientProviderBuilder.builder()
                .authorizationCode()
                .refreshToken()
                .build();

        DefaultOAuth2AuthorizedClientManager authorizedClientManager =
            new DefaultOAuth2AuthorizedClientManager(
                clientRegistrationRepository, authorizedClientRepository);
        authorizedClientManager.setAuthorizedClientProvider(authorizedClientProvider);

        return authorizedClientManager;
    }
}

// application.yml - Spring enables PKCE by default for authorization_code flow
spring:
  security:
    oauth2:
      client:
        registration:
          keycloak:
            client-id: my-client
            client-secret: secret
            authorization-grant-type: authorization_code
            scope: openid,profile
        provider:
          keycloak:
            issuer-uri: https://keycloak.example.com/realms/toolbox
```

### NextAuth.js with PKCE

NextAuth.js enables PKCE automatically for the Keycloak provider. For custom configuration:

```typescript
import NextAuth from "next-auth";
import KeycloakProvider from "next-auth/providers/keycloak";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    KeycloakProvider({
      clientId: process.env.AUTH_KEYCLOAK_ID!,
      clientSecret: process.env.AUTH_KEYCLOAK_SECRET!,
      issuer: process.env.AUTH_KEYCLOAK_ISSUER!,
      authorization: {
        params: {
          // PKCE is enabled by default, but can be explicit
          code_challenge_method: "S256",
        },
      },
    }),
  ],
});
```

## Security Hardening

### Admin Console Isolation

**Critical**: Separate admin access from user authentication.

```yaml
# Keycloak CR - separate hostnames
apiVersion: k8s.keycloak.org/v2alpha1
kind: Keycloak
spec:
  hostname:
    hostname: https://auth.example.com        # User-facing
    admin: https://admin-auth.example.com     # Admin-only, restricted
    strict: true
```

**Network Policy** - restrict admin access:
```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: keycloak-admin-restrict
spec:
  podSelector:
    matchLabels:
      app: keycloak
  ingress:
    # Admin hostname only from internal network
    - from:
        - ipBlock:
            cidr: 10.0.0.0/8
      ports:
        - port: 8443
          protocol: TCP
```

### Rate Limiting and Load Shedding

```bash
# Environment variables for production
KC_HTTP_MAX_QUEUED_REQUESTS=100    # Reject requests when queue full
KC_HTTP_POOL_MAX_THREADS=50        # Limit concurrent requests
KC_SPI_BRUTE_FORCE_PROTECTION_DEFAULT_MAX_LOGIN_FAILURES=5
KC_SPI_BRUTE_FORCE_PROTECTION_DEFAULT_WAIT_INCREMENT_SECONDS=60
KC_SPI_BRUTE_FORCE_PROTECTION_DEFAULT_MAX_WAIT_SECONDS=900
```

### Brute Force Protection

```java
FluentRealmBuilder.create()
    .with(keycloakClient)
    .createRealm("toolbox")
    .bruteForceProtected(true)
    .permanentLockout(false)
    .maxFailureWaitSeconds(900)
    .minimumQuickLoginWaitSeconds(60)
    .waitIncrementSeconds(60)
    .quickLoginCheckMilliSeconds(1000)
    .maxDeltaTimeSeconds(43200)  // 12 hours
    .failureFactor(30)
    .and().apply();
```

### TLS Configuration

**Always use TLS** in production:

```yaml
# Keycloak CR
spec:
  http:
    httpEnabled: false           # Disable HTTP entirely in prod
    httpsPort: 8443
    tlsSecret: keycloak-tls
```

For internal health checks without TLS:
```yaml
spec:
  http:
    httpEnabled: true            # Only for health probes
    httpPort: 8080
  # Health probes use http://localhost:8080/health
  # External traffic uses HTTPS only
```

### Security Headers

Configure via reverse proxy (ingress/route):

```yaml
# Ingress annotations
metadata:
  annotations:
    nginx.ingress.kubernetes.io/configuration-snippet: |
      add_header X-Frame-Options "SAMEORIGIN" always;
      add_header X-Content-Type-Options "nosniff" always;
      add_header X-XSS-Protection "1; mode=block" always;
      add_header Referrer-Policy "strict-origin-when-cross-origin" always;
      add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
```

### Credential Rotation

**Client Secret Rotation**:
```java
// Generate new secret
String newSecret = keycloakClient.realm("toolbox")
    .clients().get(clientId)
    .generateNewSecret()
    .getValue();

// Update applications with new secret
// Old secret remains valid until explicitly revoked
```

**Admin Password Rotation**:
```bash
# Via kcadm CLI
/opt/keycloak/bin/kcadm.sh set-password \
    --server https://keycloak.example.com \
    --realm master \
    --user admin \
    --new-password "new-secure-password"
```

### Audit Logging

Enable event logging for security audits:

```java
FluentRealmBuilder.create()
    .with(keycloakClient)
    .createRealm("toolbox")
    .eventsEnabled(true)
    .eventsListeners("jboss-logging")
    .enabledEventTypes(
        "LOGIN", "LOGIN_ERROR",
        "LOGOUT", "LOGOUT_ERROR",
        "CODE_TO_TOKEN", "CODE_TO_TOKEN_ERROR",
        "CLIENT_LOGIN", "CLIENT_LOGIN_ERROR",
        "REFRESH_TOKEN", "REFRESH_TOKEN_ERROR",
        "PERMISSION_TOKEN"  // ABAC events
    )
    .eventsExpiration(604800)  // 7 days
    .adminEventsEnabled(true)
    .adminEventsDetailsEnabled(true)
    .and().apply();
```

## Token Revocation

### Logout Flows

**Frontend-Initiated Logout** (RP-Initiated):
```typescript
// NextAuth.js - redirect to Keycloak logout
import { signOut } from "next-auth/react";

async function handleLogout() {
  const idToken = session?.idToken;
  const logoutUrl = `${process.env.AUTH_KEYCLOAK_ISSUER}/protocol/openid-connect/logout?` +
    `id_token_hint=${idToken}&` +
    `post_logout_redirect_uri=${encodeURIComponent(window.location.origin)}`;

  // Sign out of NextAuth, then redirect to Keycloak
  await signOut({ redirect: false });
  window.location.href = logoutUrl;
}
```

**Backend Token Revocation**:
```java
public void revokeToken(String refreshToken) {
    String revokeEndpoint = String.format(
        "%s/realms/%s/protocol/openid-connect/revoke",
        authServerUrl, realm
    );

    MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
    form.add("client_id", clientId);
    form.add("client_secret", clientSecret);
    form.add("token", refreshToken);
    form.add("token_type_hint", "refresh_token");

    restTemplate.postForEntity(revokeEndpoint,
        new HttpEntity<>(form, headers), Void.class);
}
```

### Backchannel Logout

Keycloak notifies all clients when user logs out:

**Enable on Client**:
```java
FluentClientBuilder.forRealm("toolbox")
    .with(keycloakClient)
    .createClient("my-app")
        .confidentialClient()
        .enableBackchannelLogout(true)
        .backchannelLogoutUrl("https://myapp.example.com/logout/backchannel")
        .backchannelLogoutSessionRequired(true)
        .and()
    .apply();
```

**Spring Boot Backchannel Logout Handler**:
```java
@RestController
public class BackchannelLogoutController {

    private final JwtDecoder jwtDecoder;
    private final SessionRegistry sessionRegistry;

    @PostMapping("/logout/backchannel")
    public ResponseEntity<Void> handleBackchannelLogout(
            @RequestParam("logout_token") String logoutToken) {

        Jwt jwt = jwtDecoder.decode(logoutToken);

        // Validate logout token
        if (!"logout+jwt".equals(jwt.getClaim("events"))) {
            return ResponseEntity.badRequest().build();
        }

        String sid = jwt.getClaim("sid");  // Session ID
        String sub = jwt.getSubject();      // User ID

        // Invalidate local sessions
        sessionRegistry.getAllPrincipals().stream()
            .filter(p -> p.toString().equals(sub))
            .flatMap(p -> sessionRegistry.getAllSessions(p, false).stream())
            .forEach(SessionInformation::expireNow);

        return ResponseEntity.ok().build();
    }
}
```

### Session Management

**Max Session Configuration**:
```java
FluentRealmBuilder.create()
    .with(keycloakClient)
    .createRealm("toolbox")
    .ssoSessionIdleTimeout(1800)      // 30 min idle
    .ssoSessionMaxLifespan(36000)     // 10 hours max
    .offlineSessionIdleTimeout(2592000)  // 30 days
    .offlineSessionMaxLifespan(5184000)  // 60 days
    .and().apply();
```

**Force Session Termination**:
```java
// Terminate all sessions for a user
keycloakClient.realm("toolbox")
    .users().get(userId)
    .logout();

// Terminate specific session
keycloakClient.realm("toolbox")
    .users().get(userId)
    .revokeConsent(clientId);
```

## Monitoring and Observability

### Prometheus Metrics

Enable in Keycloak:
```bash
KC_METRICS_ENABLED=true
```

**Dockerfile** (for custom image):
```dockerfile
FROM quay.io/keycloak/keycloak:26.3.1 AS builder

ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true
ENV KC_DB=mysql

RUN /opt/keycloak/bin/kc.sh build
```

### Key Metrics to Monitor

| Metric | Alert Threshold | Description |
|--------|-----------------|-------------|
| `keycloak_logins{outcome="error"}` | >10/min | Failed login attempts |
| `keycloak_request_duration_seconds` | p99 > 2s | Token endpoint latency |
| `keycloak_sessions` | >80% capacity | Active session count |
| `keycloak_request_errors_total` | >1% | Error rate |
| `jvm_memory_used_bytes` | >80% heap | Memory pressure |

### Prometheus ServiceMonitor

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: keycloak
  labels:
    app: keycloak
spec:
  selector:
    matchLabels:
      app: keycloak
  endpoints:
    - port: http
      path: /metrics
      interval: 30s
      scheme: http
```

### Grafana Dashboard Queries

**Login Success Rate**:
```promql
sum(rate(keycloak_logins{outcome="success"}[5m])) /
sum(rate(keycloak_logins[5m])) * 100
```

**Token Endpoint Latency**:
```promql
histogram_quantile(0.99,
  sum(rate(keycloak_request_duration_seconds_bucket{uri="/protocol/openid-connect/token"}[5m])) by (le)
)
```

**Active Sessions**:
```promql
sum(keycloak_sessions{type="online"})
```

### Alerting Rules

```yaml
groups:
  - name: keycloak
    rules:
      - alert: KeycloakHighLoginFailures
        expr: sum(rate(keycloak_logins{outcome="error"}[5m])) > 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High rate of login failures

      - alert: KeycloakHighLatency
        expr: histogram_quantile(0.99, sum(rate(keycloak_request_duration_seconds_bucket[5m])) by (le)) > 2
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: Token endpoint latency above 2s

      - alert: KeycloakDown
        expr: up{job="keycloak"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: Keycloak instance is down
```

### Logging Configuration

```bash
# Production logging
KC_LOG_LEVEL=INFO
KC_LOG_CONSOLE_OUTPUT=json  # Structured logging

# Debug specific components (temporary)
KC_LOG_LEVEL=INFO,org.keycloak.services.managers:DEBUG,org.keycloak.protocol.oidc:DEBUG
```

**Log Events to Monitor**:
- `LOGIN_ERROR` - Failed authentications
- `CODE_TO_TOKEN_ERROR` - Token exchange failures
- `REFRESH_TOKEN_ERROR` - Token refresh failures
- `CLIENT_LOGIN_ERROR` - Service account failures
- `PERMISSION_TOKEN_ERROR` - ABAC policy denials
