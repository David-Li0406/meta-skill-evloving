# JWT Authentication Flow

## JWT Service

```java
@Service
@RequiredArgsConstructor
public class JwtService {

    @Value("${jwt.secret}")
    private String secretKey;

    @Value("${jwt.access-token-expiration}")
    private Duration accessTokenExpiration;

    @Value("${jwt.refresh-token-expiration}")
    private Duration refreshTokenExpiration;

    public String generateAccessToken(UserDetails userDetails) {
        return generateToken(userDetails, accessTokenExpiration, Map.of());
    }

    public String generateRefreshToken(UserDetails userDetails) {
        return generateToken(userDetails, refreshTokenExpiration, Map.of("type", "refresh"));
    }

    private String generateToken(
            UserDetails userDetails,
            Duration expiration,
            Map<String, Object> extraClaims) {

        Instant now = Instant.now();
        return Jwts.builder()
            .claims(extraClaims)
            .subject(userDetails.getUsername())
            .issuedAt(Date.from(now))
            .expiration(Date.from(now.plus(expiration)))
            .signWith(getSigningKey())
            .compact();
    }

    public String extractUsername(String token) {
        return extractClaim(token, Claims::getSubject);
    }

    public <T> T extractClaim(String token, Function<Claims, T> claimsResolver) {
        Claims claims = extractAllClaims(token);
        return claimsResolver.apply(claims);
    }

    private Claims extractAllClaims(String token) {
        return Jwts.parser()
            .verifyWith(getSigningKey())
            .build()
            .parseSignedClaims(token)
            .getPayload();
    }

    public boolean isTokenValid(String token, UserDetails userDetails) {
        String username = extractUsername(token);
        return username.equals(userDetails.getUsername()) && !isTokenExpired(token);
    }

    private boolean isTokenExpired(String token) {
        return extractClaim(token, Claims::getExpiration).before(new Date());
    }

    private SecretKey getSigningKey() {
        byte[] keyBytes = Decoders.BASE64.decode(secretKey);
        return Keys.hmacShaKeyFor(keyBytes);
    }
}
```

## Authentication Controller

```java
@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {

    private final AuthenticationManager authManager;
    private final JwtService jwtService;
    private final UserDetailsService userDetailsService;
    private final RefreshTokenService refreshTokenService;

    @PostMapping("/login")
    public AuthResponse login(@Valid @RequestBody LoginRequest request) {
        authManager.authenticate(
            new UsernamePasswordAuthenticationToken(
                request.email(),
                request.password()
            )
        );

        UserDetails userDetails = userDetailsService.loadUserByUsername(request.email());
        String accessToken = jwtService.generateAccessToken(userDetails);
        String refreshToken = jwtService.generateRefreshToken(userDetails);

        refreshTokenService.save(request.email(), refreshToken);

        return new AuthResponse(accessToken, refreshToken);
    }

    @PostMapping("/refresh")
    public AuthResponse refresh(@Valid @RequestBody RefreshRequest request) {
        String refreshToken = request.refreshToken();

        if (!refreshTokenService.isValid(refreshToken)) {
            throw new InvalidTokenException("Invalid refresh token");
        }

        String username = jwtService.extractUsername(refreshToken);
        UserDetails userDetails = userDetailsService.loadUserByUsername(username);

        String newAccessToken = jwtService.generateAccessToken(userDetails);
        String newRefreshToken = jwtService.generateRefreshToken(userDetails);

        refreshTokenService.revoke(refreshToken);
        refreshTokenService.save(username, newRefreshToken);

        return new AuthResponse(newAccessToken, newRefreshToken);
    }

    @PostMapping("/logout")
    public void logout(@RequestHeader("Authorization") String authHeader) {
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            String token = authHeader.substring(7);
            String username = jwtService.extractUsername(token);
            refreshTokenService.revokeAllForUser(username);
        }
    }
}

public record LoginRequest(
    @NotBlank @Email String email,
    @NotBlank String password
) {}

public record RefreshRequest(
    @NotBlank String refreshToken
) {}

public record AuthResponse(
    String accessToken,
    String refreshToken
) {}
```

## Refresh Token Storage

```java
@Service
@RequiredArgsConstructor
public class RefreshTokenService {

    private final RefreshTokenRepository repository;
    private final JwtService jwtService;

    public void save(String username, String token) {
        RefreshToken refreshToken = new RefreshToken();
        refreshToken.setUsername(username);
        refreshToken.setToken(token);
        refreshToken.setExpiresAt(
            jwtService.extractClaim(token, Claims::getExpiration).toInstant()
        );
        repository.save(refreshToken);
    }

    public boolean isValid(String token) {
        return repository.findByToken(token)
            .map(rt -> rt.getExpiresAt().isAfter(Instant.now()))
            .orElse(false);
    }

    public void revoke(String token) {
        repository.deleteByToken(token);
    }

    public void revokeAllForUser(String username) {
        repository.deleteAllByUsername(username);
    }
}

@Entity
@Table(name = "refresh_tokens")
public class RefreshToken {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String username;

    @Column(nullable = false, unique = true)
    private String token;

    @Column(nullable = false)
    private Instant expiresAt;

    // getters, setters
}
```

## Configuration

```yaml
jwt:
  secret: ${JWT_SECRET}  # Base64 encoded, min 256 bits
  access-token-expiration: 15m
  refresh-token-expiration: 7d
```
