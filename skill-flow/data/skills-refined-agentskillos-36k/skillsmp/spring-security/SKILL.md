---
name: Spring Security
description: Authentication, authorization, JWT, OAuth2, CSRF, CORS, and security filter chain.
metadata:
  labels: [java, spring-boot, security, authentication, authorization]
  triggers:
    files: ['**/*Security*.java', '**/*Config*.java', '**/*Auth*.java']
    keywords: [SecurityFilterChain, HttpSecurity, Authentication, Authorization, csrf, jwt, OAuth2, UserDetails, PasswordEncoder]
---

# Spring Security Standards

## Security Configuration (Spring Boot 3+)

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())  // Disable for stateless API
            .cors(cors -> cors.configurationSource(corsConfigurationSource()))
            .sessionManagement(session ->
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/api/auth/**").permitAll()
                .requestMatchers("/api/public/**").permitAll()
                .requestMatchers("/actuator/health").permitAll()
                .requestMatchers("/api/admin/**").hasRole("ADMIN")
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtAuthFilter, UsernamePasswordAuthenticationFilter.class)
            .exceptionHandling(ex -> ex
                .authenticationEntryPoint(authEntryPoint)
                .accessDeniedHandler(accessDeniedHandler)
            )
            .build();
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager(
            AuthenticationConfiguration config) throws Exception {
        return config.getAuthenticationManager();
    }
}
```

## JWT Authentication Filter

```java
@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {

    private final JwtService jwtService;
    private final UserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain) throws ServletException, IOException {

        String authHeader = request.getHeader("Authorization");

        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            filterChain.doFilter(request, response);
            return;
        }

        String jwt = authHeader.substring(7);
        String username = jwtService.extractUsername(jwt);

        if (username != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            UserDetails userDetails = userDetailsService.loadUserByUsername(username);

            if (jwtService.isTokenValid(jwt, userDetails)) {
                UsernamePasswordAuthenticationToken authToken =
                    new UsernamePasswordAuthenticationToken(
                        userDetails,
                        null,
                        userDetails.getAuthorities()
                    );
                authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                SecurityContextHolder.getContext().setAuthentication(authToken);
            }
        }

        filterChain.doFilter(request, response);
    }
}
```

## Method Security

```java
@Service
public class UserService {

    @PreAuthorize("hasRole('ADMIN')")
    public void deleteUser(Long id) { }

    @PreAuthorize("hasRole('ADMIN') or #id == authentication.principal.id")
    public User updateUser(Long id, UpdateRequest request) { }

    @PostAuthorize("returnObject.owner == authentication.name")
    public Resource getResource(Long id) { }

    @PreAuthorize("@securityService.canAccess(#id)")
    public void accessResource(Long id) { }
}

@Component("securityService")
public class SecurityService {
    public boolean canAccess(Long resourceId) {
        // Custom authorization logic
        return true;
    }
}
```

## CORS Configuration

```java
@Bean
public CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration config = new CorsConfiguration();
    config.setAllowedOrigins(List.of("http://localhost:3000", "https://example.com"));
    config.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE", "OPTIONS"));
    config.setAllowedHeaders(List.of("*"));
    config.setAllowCredentials(true);
    config.setMaxAge(3600L);

    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/api/**", config);
    return source;
}
```

## Best Practices

1. **Use BCrypt** for password hashing (strength 10-12)
2. **Stateless sessions** for REST APIs with JWT
3. **Method security** for fine-grained authorization
4. **Validate JWT** on every request
5. **Short token expiry** with refresh token pattern
6. **Never log sensitive data** (passwords, tokens)

## References

- [JWT Auth Flow](references/jwt-auth-flow.md) - Token service, refresh tokens
- [OAuth2 Resource Server](references/oauth2-resource-server.md) - JWT decoder, claims
- [Security Filter Chain](references/security-filter-chain.md) - Filter order, custom filters
