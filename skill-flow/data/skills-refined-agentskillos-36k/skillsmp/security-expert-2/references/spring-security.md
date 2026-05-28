# Spring Security Reference

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Filter Chain](#filter-chain)
3. [OAuth2 Resource Server](#oauth2-resource-server)
4. [Method Security](#method-security)
5. [Common Configurations](#common-configurations)
6. [Testing Security](#testing-security)

## Architecture Overview

### Security Filter Chain
```
Request → DelegatingFilterProxy → FilterChainProxy → SecurityFilterChain → Controller
                                        ↓
                              [SecurityContextHolder]
                                        ↓
                               Authentication object
```

### Key Components
- **SecurityContextHolder**: Thread-local storage for Authentication
- **Authentication**: Principal + credentials + authorities
- **AuthenticationManager**: Validates credentials
- **AuthorizationManager**: Checks permissions

## Filter Chain

### Default Filter Order (Spring Security 6.x)
```
1. DisableEncodeUrlFilter
2. WebAsyncManagerIntegrationFilter
3. SecurityContextHolderFilter
4. HeaderWriterFilter
5. CorsFilter
6. CsrfFilter
7. LogoutFilter
8. OAuth2AuthorizationRequestRedirectFilter
9. OAuth2LoginAuthenticationFilter
10. BearerTokenAuthenticationFilter      ← JWT validation
11. RequestCacheAwareFilter
12. SecurityContextHolderAwareRequestFilter
13. AnonymousAuthenticationFilter
14. ExceptionTranslationFilter
15. AuthorizationFilter                   ← Access decisions
```

### Custom Filter Example
```java
@Component
public class ApiKeyAuthFilter extends OncePerRequestFilter {
    @Override
    protected void doFilterInternal(HttpServletRequest request, 
                                    HttpServletResponse response, 
                                    FilterChain chain) throws ServletException, IOException {
        String apiKey = request.getHeader("X-API-Key");
        if (apiKey != null && validateApiKey(apiKey)) {
            Authentication auth = new ApiKeyAuthentication(apiKey, getAuthorities(apiKey));
            SecurityContextHolder.getContext().setAuthentication(auth);
        }
        chain.doFilter(request, response);
    }
}

// Register in filter chain
http.addFilterBefore(apiKeyFilter, BearerTokenAuthenticationFilter.class);
```

## OAuth2 Resource Server

### JWT Configuration
```java
@Configuration
@EnableWebSecurity
public class ResourceServerConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())  // Stateless API
            .sessionManagement(session -> 
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .oauth2ResourceServer(oauth2 -> oauth2
                .jwt(jwt -> jwt
                    .decoder(jwtDecoder())
                    .jwtAuthenticationConverter(jwtAuthConverter())))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/actuator/health").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .requestMatchers("/api/**").authenticated()
                .anyRequest().denyAll());
        
        return http.build();
    }
    
    @Bean
    public JwtDecoder jwtDecoder() {
        NimbusJwtDecoder decoder = NimbusJwtDecoder
            .withJwkSetUri("https://auth.example.com/.well-known/jwks.json")
            .build();
        
        OAuth2TokenValidator<Jwt> validator = new DelegatingOAuth2TokenValidator<>(
            JwtValidators.createDefaultWithIssuer("https://auth.example.com"),
            new JwtClaimValidator<List<String>>("aud", 
                aud -> aud != null && aud.contains("my-api")),
            new JwtTimestampValidator(Duration.ofSeconds(60))  // Clock skew
        );
        
        decoder.setJwtValidator(validator);
        return decoder;
    }
    
    @Bean
    public JwtAuthenticationConverter jwtAuthConverter() {
        JwtGrantedAuthoritiesConverter authorities = new JwtGrantedAuthoritiesConverter();
        authorities.setAuthoritiesClaimName("roles");
        authorities.setAuthorityPrefix("ROLE_");
        
        JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
        converter.setJwtGrantedAuthoritiesConverter(authorities);
        converter.setPrincipalClaimName("sub");
        return converter;
    }
}
```

### Opaque Token (Token Introspection)
```java
http.oauth2ResourceServer(oauth2 -> oauth2
    .opaqueToken(opaque -> opaque
        .introspectionUri("https://auth.example.com/introspect")
        .introspectionClientCredentials("client-id", "client-secret")));
```

## Method Security

### Enable Method Security
```java
@Configuration
@EnableMethodSecurity(prePostEnabled = true, securedEnabled = true)
public class MethodSecurityConfig { }
```

### Annotations
```java
@Service
public class DocumentService {
    
    // Role-based
    @PreAuthorize("hasRole('ADMIN')")
    public void deleteAll() { }
    
    // Multiple roles
    @PreAuthorize("hasAnyRole('ADMIN', 'MANAGER')")
    public List<Document> listAll() { }
    
    // Custom expression with parameter
    @PreAuthorize("#document.ownerId == authentication.name or hasRole('ADMIN')")
    public void update(Document document) { }
    
    // Post-filter results
    @PostFilter("filterObject.ownerId == authentication.name or hasRole('ADMIN')")
    public List<Document> findAll() { }
    
    // Return value check
    @PostAuthorize("returnObject.ownerId == authentication.name")
    public Document findById(String id) { }
    
    // Permission evaluator
    @PreAuthorize("hasPermission(#id, 'Document', 'READ')")
    public Document read(String id) { }
}
```

### Custom Permission Evaluator
```java
@Component
public class CustomPermissionEvaluator implements PermissionEvaluator {
    
    @Override
    public boolean hasPermission(Authentication auth, Object target, Object permission) {
        if (target instanceof Document doc) {
            return checkDocumentPermission(auth, doc, permission.toString());
        }
        return false;
    }
    
    @Override
    public boolean hasPermission(Authentication auth, Serializable targetId, 
                                 String targetType, Object permission) {
        // Load object and check
        return checkPermissionById(auth, targetId, targetType, permission.toString());
    }
}

@Configuration
@EnableMethodSecurity
public class MethodSecurityConfig {
    @Bean
    public MethodSecurityExpressionHandler methodSecurityExpressionHandler(
            CustomPermissionEvaluator evaluator) {
        DefaultMethodSecurityExpressionHandler handler = 
            new DefaultMethodSecurityExpressionHandler();
        handler.setPermissionEvaluator(evaluator);
        return handler;
    }
}
```

## Common Configurations

### CORS Configuration
```java
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("https://app.example.com"));
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
    config.setAllowedHeaders(List.of("Authorization", "Content-Type"));
    config.setExposedHeaders(List.of("X-Request-Id"));
    config.setAllowCredentials(true);
    config.setMaxAge(3600L);
    
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/api/**", config);
    return source;
}

// In security config
http.cors(cors -> cors.configurationSource(corsConfigurationSource()));
```

### Security Headers
```java
http.headers(headers -> headers
    .contentSecurityPolicy(csp -> 
        csp.policyDirectives("default-src 'self'; script-src 'self'"))
    .frameOptions(frame -> frame.deny())
    .xssProtection(xss -> xss.disable())  // Modern browsers don't need
    .contentTypeOptions(Customizer.withDefaults())
    .referrerPolicy(referrer -> 
        referrer.policy(ReferrerPolicyHeaderWriter.ReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN))
    .permissionsPolicy(permissions -> 
        permissions.policy("geolocation=(), microphone=(), camera=()")));
```

### Error Handling
```java
http.exceptionHandling(exceptions -> exceptions
    .authenticationEntryPoint((request, response, authException) -> {
        response.setStatus(HttpStatus.UNAUTHORIZED.value());
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.getWriter().write("""
            {"error": "unauthorized", "message": "Authentication required"}
            """);
    })
    .accessDeniedHandler((request, response, accessDeniedException) -> {
        response.setStatus(HttpStatus.FORBIDDEN.value());
        response.setContentType(MediaType.APPLICATION_JSON_VALUE);
        response.getWriter().write("""
            {"error": "forbidden", "message": "Insufficient permissions"}
            """);
    }));
```

## Testing Security

### Test Configuration
```java
@SpringBootTest
@AutoConfigureMockMvc
class SecurityTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void unauthenticatedRequest_returns401() throws Exception {
        mockMvc.perform(get("/api/protected"))
            .andExpect(status().isUnauthorized());
    }
    
    @Test
    @WithMockUser(roles = "USER")
    void authenticatedUser_canAccessProtected() throws Exception {
        mockMvc.perform(get("/api/protected"))
            .andExpect(status().isOk());
    }
    
    @Test
    @WithMockUser(roles = "USER")
    void regularUser_cannotAccessAdmin() throws Exception {
        mockMvc.perform(get("/api/admin"))
            .andExpect(status().isForbidden());
    }
    
    @Test
    void withJwt_canAccess() throws Exception {
        mockMvc.perform(get("/api/protected")
            .with(jwt()
                .jwt(jwt -> jwt
                    .subject("user-123")
                    .claim("roles", List.of("USER"))
                    .claim("aud", List.of("my-api")))))
            .andExpect(status().isOk());
    }
}
```

### Custom Security Test Annotation
```java
@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@WithSecurityContext(factory = WithMockAdminSecurityContextFactory.class)
public @interface WithMockAdmin {
    String username() default "admin";
}

public class WithMockAdminSecurityContextFactory 
        implements WithSecurityContextFactory<WithMockAdmin> {
    
    @Override
    public SecurityContext createSecurityContext(WithMockAdmin annotation) {
        SecurityContext context = SecurityContextHolder.createEmptyContext();
        
        JwtAuthenticationToken auth = new JwtAuthenticationToken(
            Jwt.withTokenValue("mock-token")
                .header("alg", "RS256")
                .subject(annotation.username())
                .claim("roles", List.of("ADMIN"))
                .build(),
            List.of(new SimpleGrantedAuthority("ROLE_ADMIN"))
        );
        
        context.setAuthentication(auth);
        return context;
    }
}
```
