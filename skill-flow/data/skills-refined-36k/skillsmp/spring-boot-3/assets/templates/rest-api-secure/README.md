# Secure REST API Template

Extends the Basic REST API template with JWT authentication, role-based access control, and security best practices.

## Additional Dependencies

```xml
<!-- Spring Security -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>

<!-- JWT -->
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-api</artifactId>
    <version>0.11.5</version>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-impl</artifactId>
    <version>0.11.5</version>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>io.jsonwebtoken</groupId>
    <artifactId>jjwt-jackson</artifactId>
    <version>0.11.5</version>
    <scope>runtime</scope>
</dependency>
```

## Additional Project Structure

```
config/
├── SecurityConfig.java          # Main security config
└── JwtTokenProvider.java        # JWT utilities

security/
├── JwtAuthenticationFilter.java # JWT validation filter
└── JwtAuthenticationEntryPoint.java # 401 error handler

service/
└── CustomUserDetailsService.java # User loading

request/
└── LoginRequest.java            # Login DTO
```

## Configuration

### application.yml additions

```yaml
app:
  jwt:
    secret: ${JWT_SECRET:your-very-long-secret-key-for-jwt-token-generation-must-be-at-least-256-bits}
    expiration: 86400  # 24 hours
```

### SecurityConfig.java

See [examples/security-config/README.md](../../../examples/security-config/README.md) for complete implementation.

## User Entity with Role

```java
@Entity
@Table(name = "users")
public class User {
    // ... other fields

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Role role;

    // Use this instead of enum if using many-to-many:
    // @ManyToMany
    // @JoinTable(name = "user_roles")
    // private Set<Role> roles;
}

public enum Role {
    USER,
    ADMIN,
    MODERATOR
}
```

## Authentication Endpoints

### POST /api/auth/login

Request:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0...",
  "type": "Bearer"
}
```

### POST /api/auth/register

Request:
```json
{
  "email": "newuser@example.com",
  "password": "Password123!",
  "firstName": "John",
  "lastName": "Doe"
}
```

## Protected Endpoints

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    // All endpoints protected by default

    @GetMapping("/me")
    public ResponseEntity<UserDTO> getCurrentUser(Principal principal) {
        // Get current user from JWT
    }

    @PreAuthorize("hasRole('ADMIN')")
    @GetMapping("/all")
    public ResponseEntity<List<UserDTO>> getAllUsers() {
        // Only admins can access
    }
}
```

## Using JWT Token

Include in request headers:

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     http://localhost:8080/api/users/me
```

## Security Features

- ✅ BCrypt password hashing
- ✅ JWT stateless authentication
- ✅ Role-based access control (RBAC)
- ✅ Method-level security with @PreAuthorize
- ✅ Custom 401 error handling
- ✅ Protected admin endpoints
- ✅ Public auth endpoints
- ✅ Input validation

## Testing

```java
@SpringBootTest
@AutoConfigureMockMvc
class SecurityTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    @WithMockUser(roles = "ADMIN")
    void adminEndpoint_WithAdminRole_ShouldSucceed() throws Exception {
        mockMvc.perform(get("/api/admin/users"))
            .andExpect(status().isOk());
    }

    @Test
    void protectedEndpoint_WithoutAuth_ShouldReturn401() throws Exception {
        mockMvc.perform(get("/api/users/me"))
            .andExpect(status().isUnauthorized());
    }
}
```

## Security Best Practices Implemented

1. Never store passwords in plain text
2. Use HTTPS in production
3. Validate all input
4. Use parameterized queries (JPA handles this)
5. Implement proper HTTP status codes
6. Log security events
7. Never expose stack traces
8. Use strong JWT secrets
9. Implement rate limiting
10. Keep dependencies updated

## Environment Variables

```bash
# Production
export JWT_SECRET=your-very-long-secret-key
export DB_PASSWORD=strong-password
export SPRING_PROFILES_ACTIVE=prod
```

## Additional Security Considerations

1. Add refresh token mechanism
2. Implement account lockout after failed attempts
3. Add CORS configuration for frontend
4. Implement rate limiting
5. Add 2FA for sensitive operations
6. Use HTTPS only
7. Implement security headers
8. Regular security audits

## Migration from Basic Template

1. Add security dependencies
2. Create security package
3. Implement SecurityConfig
4. Add JWT filter and provider
5. Create UserDetailsService
6. Add role field to User entity
7. Protect endpoints
8. Add auth endpoints
9. Update tests

## See Also

- [Basic REST API Template](../rest-api-basic/) - Base template
- [Security Example](../../../examples/security-config/README.md) - Detailed implementation
