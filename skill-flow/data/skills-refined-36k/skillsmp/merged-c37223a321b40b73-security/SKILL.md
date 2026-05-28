---
name: security
description: Use this skill for implementing authentication, authorization, JWT, CORS, and security best practices in applications.
---

# Security

## Context

This skill covers security implementations at multiple layers, including authentication, authorization, and transport security.

| Layer | Implementation |
|-------|----------------|
| Authentication | NextAuth.js (Frontend), JWT (API) |
| Authorization | Role-based guards |
| Transport | HTTPS |
| Headers | Helmet.js |

---

## Authentication Flow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Client  │───▶│ Auth     │───▶│   API    │───▶│   DB     │
│          │    │  (JWT)   │    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │               │               │
     │  1. Login     │               │
     │──────────────▶│               │
     │               │  2. Verify    │
     │               │──────────────▶│
     │               │               │  3. Check user
     │               │               │──────────────▶│
     │               │◀──────────────│◀──────────────│
     │  4. JWT Token │               │
     │◀──────────────│               │
```

---

## Authentication Configuration

### NextAuth.js Example

```typescript
import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';

export const authOptions = {
  providers: [
    CredentialsProvider({
      credentials: {
        email: { label: 'Email', type: 'email' },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        const res = await fetch(`${API_URL}/auth/login`, {
          method: 'POST',
          body: JSON.stringify(credentials),
          headers: { 'Content-Type': 'application/json' },
        });
        const user = await res.json();
        if (res.ok && user) return user;
        return null;
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) token.accessToken = user.accessToken;
      return token;
    },
    async session({ session, token }) {
      session.accessToken = token.accessToken;
      return session;
    },
  },
  pages: {
    signIn: '/login',
    error: '/login',
  },
  secret: process.env.NEXTAUTH_SECRET,
};
```

### Spring Security Example

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        return http
            .csrf(csrf -> csrf.disable())
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
}
```

---

## JWT Token Strategy

### API Implementation

```typescript
@Injectable()
export class AuthService {
  constructor(private jwtService: JwtService) {}

  async login(user: User) {
    const payload = { sub: user.id, email: user.email, role: user.role };
    return {
      accessToken: this.jwtService.sign(payload, { expiresIn: '1h' }),
      refreshToken: this.jwtService.sign(payload, { expiresIn: '7d' }),
    };
  }
}
```

### JWT Authentication Filter (Spring)

```java
@Component
@RequiredArgsConstructor
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    // Implementation details...
}
```

---

## CORS Configuration

### Example Configuration

```typescript
app.enableCors({
  origin: process.env.CORS_ORIGINS?.split(',') || ['https://example.com'],
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
});
```

### Spring Example

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

---

## Best Practices

| ✅ DO | ❌ DON'T |
|-------|----------|
| Validate all inputs | Trust client data |
| Use HTTPS everywhere | Expose HTTP endpoints |
| Rotate secrets regularly | Use same secret forever |
| Log auth failures | Log passwords/tokens |
| Hash passwords (bcrypt) | Store plain text |
| Use short-lived tokens | Use long-lived tokens |