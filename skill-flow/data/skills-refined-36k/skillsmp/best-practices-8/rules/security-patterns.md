---
title: Security Patterns
impact: MEDIUM
impactDescription: Reactive authentication, context propagation
tags: security, JWT, CORS, ReactiveSecurityContext, authentication
---

# Security Patterns

Spring Security with WebFlux requires reactive security context handling.

## Rule 1: Use ReactiveSecurityContextHolder

```kotlin
// ❌ INCORRECT - blocking SecurityContextHolder
suspend fun getCurrentUser(): User {
    val auth = SecurityContextHolder.getContext().authentication  // May be empty!
    return auth.principal as User
}

// ✅ CORRECT - ReactiveSecurityContextHolder with coroutines
suspend fun getCurrentUser(): User {
    return ReactiveSecurityContextHolder.getContext()
        .awaitSingleOrNull()
        ?.authentication
        ?.principal as? User
        ?: throw UnauthorizedException()
}
```

## Rule 2: Use @PreAuthorize with Suspend

```kotlin
// ✅ CORRECT - enable reactive method security
@Configuration
@EnableReactiveMethodSecurity
class SecurityConfig

// ✅ CORRECT - @PreAuthorize on suspend functions
@Service
class AdminService {

    @PreAuthorize("hasRole('ADMIN')")
    suspend fun deleteUser(userId: Long) {
        userRepository.deleteById(userId)
    }

    @PreAuthorize("hasRole('ADMIN') or #userId == principal.id")
    suspend fun updateUser(userId: Long, update: UserUpdate): User {
        return userRepository.update(userId, update)
    }
}
```

## Rule 3: Configure JWT for WebFlux

```kotlin
// ✅ CORRECT - JWT configuration for WebFlux
@Configuration
@EnableWebFluxSecurity
class SecurityConfig {

    @Bean
    fun securityWebFilterChain(http: ServerHttpSecurity): SecurityWebFilterChain {
        return http
            .csrf { it.disable() }
            .httpBasic { it.disable() }
            .authorizeExchange { auth ->
                auth.pathMatchers("/api/auth/**").permitAll()
                auth.pathMatchers("/api/admin/**").hasRole("ADMIN")
                auth.anyExchange().authenticated()
            }
            .oauth2ResourceServer { oauth2 ->
                oauth2.jwt { jwt ->
                    jwt.jwtAuthenticationConverter(jwtAuthConverter())
                }
            }
            .build()
    }
}
```

## Rule 4: Configure CORS Correctly

```kotlin
// ✅ CORRECT - CORS configuration for WebFlux
@Bean
fun corsConfigurationSource(): CorsConfigurationSource {
    val configuration = CorsConfiguration().apply {
        allowedOrigins = listOf("https://myapp.com")
        allowedMethods = listOf("GET", "POST", "PUT", "DELETE")
        allowedHeaders = listOf(HttpHeaders.AUTHORIZATION, HttpHeaders.CONTENT_TYPE)
        allowCredentials = true
        maxAge = 3600
    }

    return UrlBasedCorsConfigurationSource().apply {
        registerCorsConfiguration("/api/**", configuration)
    }
}
```

## Detection Checklist

- [ ] `SecurityContextHolder.getContext()` in suspend functions
- [ ] Missing `@EnableReactiveMethodSecurity`
- [ ] `allow_origins = ["*"]` in production
- [ ] Credentials in source code instead of environment variables
