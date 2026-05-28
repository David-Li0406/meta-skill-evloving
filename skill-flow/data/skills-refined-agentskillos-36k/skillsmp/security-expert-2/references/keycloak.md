# Keycloak Reference

## Table of Contents
1. [Core Concepts](#core-concepts)
2. [Client Types](#client-types)
3. [Authentication Flows](#authentication-flows)
4. [Protocol Mappers](#protocol-mappers)
5. [Realm Configuration](#realm-configuration)
6. [Integration Patterns](#integration-patterns)

## Core Concepts

### Realm
- Isolated tenant with own users, roles, clients
- Master realm for admin, separate realms per environment/tenant
- Never use master realm for applications

### Client
- Application registered with Keycloak
- Has client ID, optional client secret
- Defines allowed redirect URIs, grant types

### User
- Identity with credentials
- Has attributes, roles, groups
- Can federate from LDAP, social providers

### Roles
- **Realm roles**: Global across all clients
- **Client roles**: Scoped to specific client
- **Composite roles**: Combine multiple roles

## Client Types

### Confidential Client
- Has client secret
- For server-side applications
- Can use client_credentials grant
```yaml
# application.yml
spring:
  security:
    oauth2:
      client:
        registration:
          keycloak:
            client-id: my-backend
            client-secret: ${KEYCLOAK_SECRET}
            authorization-grant-type: authorization_code
```

### Public Client
- No client secret (cannot keep secrets)
- For SPAs, mobile apps
- Must use PKCE
```javascript
// PKCE flow for SPA
const codeVerifier = generateCodeVerifier();
const codeChallenge = await sha256(codeVerifier);

const authUrl = `${keycloakUrl}/auth?` + new URLSearchParams({
  client_id: 'my-spa',
  response_type: 'code',
  redirect_uri: 'https://app.example.com/callback',
  code_challenge: codeChallenge,
  code_challenge_method: 'S256',
  scope: 'openid profile'
});
```

### Bearer-Only Client
- Cannot initiate login
- Only validates tokens
- For APIs/resource servers
```yaml
# Keycloak client config
{
  "clientId": "my-api",
  "bearerOnly": true,
  "publicClient": false
}
```

## Authentication Flows

### Authorization Code Flow (Recommended)
1. Redirect user to `/auth` endpoint
2. User authenticates, Keycloak redirects with `code`
3. Backend exchanges code for tokens
4. Backend validates and uses tokens

### Authorization Code + PKCE (SPAs/Mobile)
Same as above, but with code_challenge to prevent interception:
```
code_challenge = BASE64URL(SHA256(code_verifier))
```

### Client Credentials (Service-to-Service)
```bash
curl -X POST "${KEYCLOAK_URL}/token" \
  -d "grant_type=client_credentials" \
  -d "client_id=my-service" \
  -d "client_secret=${SECRET}"
```

### Direct Grant (Resource Owner Password) - Avoid
- Sends username/password to client
- Only for legacy migration, trusted first-party apps
- Cannot support MFA, social login

## Protocol Mappers

### Adding Roles to Token
```json
{
  "name": "realm-roles",
  "protocol": "openid-connect",
  "protocolMapper": "oidc-usermodel-realm-role-mapper",
  "config": {
    "claim.name": "roles",
    "jsonType.label": "String",
    "multivalued": "true",
    "id.token.claim": "true",
    "access.token.claim": "true"
  }
}
```

### Adding Custom Attributes
```json
{
  "name": "department",
  "protocol": "openid-connect",
  "protocolMapper": "oidc-usermodel-attribute-mapper",
  "config": {
    "claim.name": "department",
    "user.attribute": "department",
    "id.token.claim": "true",
    "access.token.claim": "true"
  }
}
```

### Audience Mapper (Critical for APIs)
```json
{
  "name": "api-audience",
  "protocol": "openid-connect",
  "protocolMapper": "oidc-audience-mapper",
  "config": {
    "included.client.audience": "my-api",
    "id.token.claim": "false",
    "access.token.claim": "true"
  }
}
```

## Realm Configuration

### Security Settings
```json
{
  "sslRequired": "all",
  "bruteForceProtected": true,
  "permanentLockout": false,
  "maxFailureWaitSeconds": 900,
  "minimumQuickLoginWaitSeconds": 60,
  "waitIncrementSeconds": 60,
  "quickLoginCheckMilliSeconds": 1000,
  "maxDeltaTimeSeconds": 43200,
  "failureFactor": 5
}
```

### Token Lifespans
```json
{
  "accessTokenLifespan": 300,
  "accessTokenLifespanForImplicitFlow": 300,
  "ssoSessionIdleTimeout": 1800,
  "ssoSessionMaxLifespan": 36000,
  "offlineSessionIdleTimeout": 2592000,
  "accessCodeLifespan": 60,
  "accessCodeLifespanUserAction": 300
}
```

### Password Policy
```
length(12) and digits(1) and upperCase(1) and lowerCase(1) and specialChars(1) and notUsername and passwordHistory(5)
```

## Integration Patterns

### Spring Boot Resource Server
```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://keycloak.example.com/realms/myrealm
          jwk-set-uri: https://keycloak.example.com/realms/myrealm/protocol/openid-connect/certs
```

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.oauth2ResourceServer(oauth2 -> oauth2
            .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthConverter())));
        return http.build();
    }
    
    @Bean
    public JwtAuthenticationConverter jwtAuthConverter() {
        JwtGrantedAuthoritiesConverter grantedAuthorities = new JwtGrantedAuthoritiesConverter();
        grantedAuthorities.setAuthoritiesClaimName("roles");
        grantedAuthorities.setAuthorityPrefix("ROLE_");
        
        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(grantedAuthorities);
        return converter;
    }
}
```

### Custom Role Extraction from Nested Claims
```java
// For Keycloak's nested realm_access.roles structure
public class KeycloakRoleConverter implements Converter<Jwt, Collection<GrantedAuthority>> {
    @Override
    public Collection<GrantedAuthority> convert(Jwt jwt) {
        Map<String, Object> realmAccess = jwt.getClaim("realm_access");
        if (realmAccess == null) return Collections.emptyList();
        
        @SuppressWarnings("unchecked")
        List<String> roles = (List<String>) realmAccess.get("roles");
        if (roles == null) return Collections.emptyList();
        
        return roles.stream()
            .map(role -> new SimpleGrantedAuthority("ROLE_" + role.toUpperCase()))
            .collect(Collectors.toList());
    }
}
```

### Multi-Tenant Configuration
```java
@Component
public class TenantJwtIssuerValidator implements OAuth2TokenValidator<Jwt> {
    private final Set<String> allowedIssuers = Set.of(
        "https://keycloak.example.com/realms/tenant1",
        "https://keycloak.example.com/realms/tenant2"
    );
    
    @Override
    public OAuth2TokenValidatorResult validate(Jwt jwt) {
        if (allowedIssuers.contains(jwt.getIssuer().toString())) {
            return OAuth2TokenValidatorResult.success();
        }
        return OAuth2TokenValidatorResult.failure(
            new OAuth2Error("invalid_issuer", "Unknown tenant", null));
    }
}
```
