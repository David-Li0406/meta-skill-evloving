# Integration Patterns Reference

## Table of Contents
1. [Spring Boot Backend](#spring-boot-backend)
2. [NextAuth.js Frontend](#nextauthjs-frontend)
3. [Token Handling Patterns](#token-handling-patterns)
4. [Custom Keycloak Providers](#custom-keycloak-providers)

## Spring Boot Backend

### OAuth2 Resource Server Configuration

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http.oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtAuthConverter())))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/public/**").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated());
        return http.build();
    }
    
    @Bean
    public JwtAuthenticationConverter jwtAuthConverter() {
        // Note: Keycloak stores roles in a nested structure (realm_access.roles)
        // The standard JwtGrantedAuthoritiesConverter cannot handle nested claims,
        // so we use a custom converter below.
        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(keycloakRoleConverter());
        return converter;
    }

    // Extract roles from Keycloak's nested structure (realm_access.roles)
    private Converter<Jwt, Collection<GrantedAuthority>> keycloakRoleConverter() {
        return jwt -> {
            Map<String, Object> realmAccess = jwt.getClaim("realm_access");
            if (realmAccess == null) return Collections.emptyList();
            
            @SuppressWarnings("unchecked")
            List<String> roles = (List<String>) realmAccess.get("roles");
            if (roles == null) return Collections.emptyList();
            
            return roles.stream()
                .map(role -> new SimpleGrantedAuthority("ROLE_" + role.toUpperCase()))
                .collect(Collectors.toList());
        };
    }
}
```

### Application Properties
```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: ${KEYCLOAK_AUTH_SERVER_URL}/realms/${KEYCLOAK_REALM}
          jwk-set-uri: ${KEYCLOAK_AUTH_SERVER_URL}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/certs

keycloak:
  auth-server-url: ${KEYCLOAK_AUTH_SERVER_URL:http://localhost:8080}
  realm: ${KEYCLOAK_REALM:toolbox}
  resource: ${KEYCLOAK_CLIENT_ID:toolbox-webui}
  credentials:
    secret: ${KEYCLOAK_CLIENT_SECRET}
```

### ABAC Annotation and Aspect

**Annotation:**
```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface AbacPolicy {
    String resource();
    String action();
}
```

**Aspect:**
```java
@Aspect
@Component
@RequiredArgsConstructor
public class AbacAspect {
    
    private final AbacService abacService;
    
    @Around("@annotation(abacPolicy)")
    public Object enforcePolicy(ProceedingJoinPoint joinPoint, 
                                AbacPolicy abacPolicy) throws Throwable {
        var authentication = SecurityContextHolder.getContext().getAuthentication();
        
        if (authentication == null) {
            throw new AccessDeniedException("No authentication found");
        }
        
        var result = abacService.evaluatePolicy(
            authentication,
            abacPolicy.resource(),
            abacPolicy.action()
        );
        
        return switch (result) {
            case AbacService.PolicyResult.Success s -> joinPoint.proceed();
            case AbacService.PolicyResult.Forbidden f -> 
                throw new AccessDeniedException("Access denied: " + f.message());
            case AbacService.PolicyResult.Error e -> 
                throw new AccessDeniedException("Policy error: " + e.message());
        };
    }
}
```

**Service (UMA Token Exchange):**
```java
@Service
@Slf4j
public class AbacService {
    
    private final String authServerUrl;
    private final String realm;
    private final String clientId;
    private final String clientSecret;
    private final RestTemplate restTemplate;
    
    public sealed interface PolicyResult {
        record Success() implements PolicyResult {}
        record Forbidden(String message) implements PolicyResult {}
        record Error(String message) implements PolicyResult {}
    }
    
    @Retryable(
        retryFor = {HttpServerErrorException.class, ResourceAccessException.class},
        maxAttempts = 3,
        backoff = @Backoff(delay = 750, multiplier = 2)
    )
    @Cacheable(
        value = "policyCache",
        keyGenerator = "policyEvaluationKeyGenerator",
        unless = "#result instanceof T(...PolicyResult$Error)"
    )
    public PolicyResult evaluatePolicy(Authentication authentication, 
                                       String resource, String action) {
        if (!(authentication instanceof JwtAuthenticationToken jwtAuth)) {
            return new PolicyResult.Error("Invalid authentication type");
        }
        
        try {
            String userToken = jwtAuth.getToken().getTokenValue();
            String tokenEndpoint = String.format(
                "%s/realms/%s/protocol/openid-connect/token",
                authServerUrl, realm
            );
            
            MultiValueMap<String, String> form = new LinkedMultiValueMap<>();
            form.add("grant_type", "urn:ietf:params:oauth:grant-type:uma-ticket");
            form.add("audience", clientId);
            form.add("permission", resource + "#" + action);
            form.add("client_id", clientId);
            form.add("client_secret", clientSecret);
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);
            headers.setBearerAuth(userToken);
            
            var response = restTemplate.exchange(
                tokenEndpoint,
                HttpMethod.POST,
                new HttpEntity<>(form, headers),
                Map.class
            );
            
            if (response.getStatusCode().is2xxSuccessful() 
                && response.getBody() != null
                && response.getBody().containsKey("access_token")) {
                return new PolicyResult.Success();
            }
            return new PolicyResult.Forbidden("No permission granted");
            
        } catch (HttpClientErrorException.Forbidden e) {
            return new PolicyResult.Forbidden("Access denied by policy");
        } catch (HttpClientErrorException.BadRequest e) {
            return new PolicyResult.Error("Invalid permission request");
        } catch (Exception e) {
            return new PolicyResult.Error("Policy evaluation failed: " + e.getMessage());
        }
    }
}
```

### Controller Usage
```java
@RestController
@RequestMapping("/api/mail")
@RequiredArgsConstructor
public class MailController {
    
    private final MailService mailService;
    
    @AbacPolicy(resource = "mailtemplate", action = "view")
    @GetMapping("/templates")
    public List<MailTemplate> getMailTemplates() {
        return mailService.getAllTemplates();
    }
    
    @AbacPolicy(resource = "mailtemplate", action = "edit")
    @PostMapping("/templates")
    public MailTemplate createTemplate(@RequestBody MailTemplateRequest request) {
        return mailService.createTemplate(request);
    }
}
```

## NextAuth.js Frontend

### Keycloak Provider Configuration

**auth.ts:**
```typescript
import NextAuth from "next-auth";
import KeycloakProvider from "next-auth/providers/keycloak";

export const {
  handlers: { GET, POST },
  auth,
  signIn,
  signOut,
} = NextAuth({
  providers: [
    KeycloakProvider({
      clientId: process.env.AUTH_KEYCLOAK_ID!,
      clientSecret: process.env.AUTH_KEYCLOAK_SECRET!,
      issuer: process.env.AUTH_KEYCLOAK_ISSUER!,
    }),
  ],
  callbacks: {
    jwt: async ({ token, account }) => {
      if (account) {
        token.accessToken = account.access_token;
        token.refreshToken = account.refresh_token;
        token.expiresAt = account.expires_at;
        token.idToken = account.id_token;
      }
      
      // Check if token needs refresh
      if (token.expiresAt && Date.now() < token.expiresAt * 1000 - 30000) {
        return token;
      }
      
      // Refresh the token
      return await refreshAccessToken(token);
    },
    session: async ({ session, token }) => {
      session.accessToken = token.accessToken as string;
      session.error = token.error as string | undefined;
      return session;
    },
  },
});

async function refreshAccessToken(token: any) {
  try {
    const response = await fetch(
      `${process.env.AUTH_KEYCLOAK_ISSUER}/protocol/openid-connect/token`,
      {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          client_id: process.env.AUTH_KEYCLOAK_ID!,
          client_secret: process.env.AUTH_KEYCLOAK_SECRET!,
          grant_type: "refresh_token",
          refresh_token: token.refreshToken,
        }),
      }
    );

    const refreshedTokens = await response.json();

    if (!response.ok) throw refreshedTokens;

    return {
      ...token,
      accessToken: refreshedTokens.access_token,
      refreshToken: refreshedTokens.refresh_token ?? token.refreshToken,
      expiresAt: Math.floor(Date.now() / 1000) + refreshedTokens.expires_in,
    };
  } catch (error) {
    return { ...token, error: "RefreshAccessTokenError" };
  }
}
```

### Authenticated API Calls

**fetchWithAuth utility:**
```typescript
export async function fetchWithAuth(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const session = await auth();
  
  if (!session?.accessToken) {
    throw new Error("No access token available");
  }
  
  if (session.error === "RefreshAccessTokenError") {
    // Redirect to sign-in
    throw new Error("Session expired");
  }
  
  const headers = new Headers(options.headers);
  headers.set("Authorization", `Bearer ${session.accessToken}`);
  
  return fetch(url, { ...options, headers });
}
```

**Server Action:**
```typescript
"use server";

import { fetchWithAuth } from "@/lib/auth-utils";

export async function getMailTemplates() {
  const response = await fetchWithAuth(
    `${process.env.API_BASE_URL}/api/mail/templates`
  );
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return response.json();
}
```

### Environment Variables
```env
AUTH_KEYCLOAK_ID=toolbox-webui
AUTH_KEYCLOAK_SECRET=your-client-secret
AUTH_KEYCLOAK_ISSUER=https://keycloak.example.com/realms/toolbox

# Optional configuration
TOKEN_CLEANUP_INTERVAL=3600000
MAX_STORED_TOKENS=1000
TOKEN_EXPIRY_BUFFER=30000
SESSION_DURATION=10800
```

## Token Handling Patterns

### JWT Structure from Keycloak
```json
{
  "sub": "user-uuid",
  "preferred_username": "john.doe",
  "email": "john@example.com",
  
  "realm_access": {
    "roles": ["admin", "2ndline", "offline_access"]
  },
  
  "resource_access": {
    "toolbox-webui": {
      "roles": ["report-viewer"]
    }
  },
  
  "custom_claim": "value",
  "flexii_username": "john.doe.flexii",
  "oister_username": "j.doe.oister",
  
  "iss": "https://keycloak.example.com/realms/toolbox",
  "aud": "toolbox-webui",
  "exp": 1635724800,
  "iat": 1635721200
}
```

### Token Validation (Backend)
```java
// Spring Security auto-validates:
// 1. Signature (using JWKS from issuer-uri)
// 2. Expiration (exp claim)
// 3. Issuer (iss claim matches issuer-uri)

// Custom validation can be added:
@Bean
public JwtDecoder jwtDecoder() {
    NimbusJwtDecoder decoder = JwtDecoders.fromIssuerLocation(issuerUri);
    
    OAuth2TokenValidator<Jwt> withIssuer = JwtValidators.createDefaultWithIssuer(issuerUri);
    OAuth2TokenValidator<Jwt> audienceValidator = new AudienceValidator(expectedAudience);
    OAuth2TokenValidator<Jwt> validator = new DelegatingOAuth2TokenValidator<>(
        withIssuer, audienceValidator
    );
    
    decoder.setJwtValidator(validator);
    return decoder;
}
```

## Custom Keycloak Providers

### Protocol Mapper SPI

**AbstractUsernameMapper:**
```java
public abstract class AbstractUsernameMapper 
    extends AbstractOIDCProtocolMapper
    implements OIDCAccessTokenMapper, OIDCIDTokenMapper, UserInfoTokenMapper {
    
    protected abstract String getClaimName();
    protected abstract String lookupUsername(String email);
    
    @Override
    protected void setClaim(IDToken token, ProtocolMapperModel model,
                           UserSessionModel userSession, KeycloakSession session,
                           ClientSessionContext context) {
        UserModel user = userSession.getUser();
        String email = user.getEmail();
        
        if (email != null && !email.isEmpty()) {
            String username = lookupUsername(email);
            if (username != null) {
                token.getOtherClaims().put(getClaimName(), username);
            }
        }
    }
}
```

**Implementation:**
```java
public class FlexiiUsernameMapper extends AbstractUsernameMapper {
    
    public static final String PROVIDER_ID = "flexii-username-mapper";
    
    @Override
    protected String getClaimName() {
        return "flexii_username";
    }
    
    @Override
    protected String lookupUsername(String email) {
        // Database lookup with caching
        return FlexiiDatabaseService.getInstance().findUsernameByEmail(email);
    }
    
    @Override
    public String getId() {
        return PROVIDER_ID;
    }
    
    @Override
    public String getDisplayType() {
        return "Flexii Username Mapper";
    }
}
```

**SPI Registration (META-INF/services/org.keycloak.protocol.ProtocolMapper):**
```
com.example.keycloak.providers.FlexiiUsernameMapper
com.example.keycloak.providers.OisterUsernameMapper
```

### Adding Mappers via Admin API
```java
// Using the Mappers utility class
Mappers mappers = new Mappers(keycloakClient);

// Add custom protocol mapper to client
mappers.configureProtocolMapper(
    "toolbox",
    "toolbox-webui",
    "flexii-username-mapper",  // Custom provider ID
    "Flexii Username",
    "flexii_username"
);

// The mapper will add flexii_username claim to tokens
// when users have valid emails in the Flexii database
```
