# Configuration - @Configuration and @Bean Wiring

Configuration classes wire together application services, adapters, and Spring beans.
They bridge the **application layer** (framework-agnostic) with **Spring's DI container**.

## Purpose

Application layer services should NOT have Spring annotations. Instead, we wire them as beans
using `@Configuration` classes in the infrastructure layer.

```markdown
Application Layer                    Infrastructure Layer
┌─────────────────────┐              ┌─────────────────────────────┐
│ WaitlistJoiner      │◄─────────────│ @Configuration              │
│ (no Spring annot.)  │  @Bean       │ WaitlistConfiguration       │
│                     │              │                             │
│ UserCreator         │◄─────────────│ fun waitlistJoiner() = ...  │
│ (no Spring annot.)  │  @Bean       │ fun userCreator() = ...     │
└─────────────────────┘              └─────────────────────────────┘
```

## Basic Configuration

```kotlin
// infrastructure/configuration/UserConfiguration.kt
@Configuration
class UserConfiguration {

    @Bean
    fun userCreator(
        userRepository: UserRepository,    // Injected from Spring context
        emailService: EmailService,        // Injected from Spring context
    ): UserCreator = UserCreator(userRepository, emailService)

    @Bean
    fun userFinder(
        userRepository: UserRepository,
    ): UserFinder = UserFinder(userRepository)
}
```

## Type-Safe Configuration Properties

**ALWAYS** use `@ConfigurationProperties` for type-safe configuration:

```kotlin
// infrastructure/configuration/WaitlistSecurityProperties.kt
@ConfigurationProperties(prefix = "waitlist.security")
data class WaitlistSecurityProperties(
    val ipHmacSecret: String,
    val maxEntriesPerIp: Int = 5,
    val rateLimitPerMinute: Int = 10,
)
```

```yaml
# application.yml
waitlist:
    security:
        ip-hmac-secret: ${WAITLIST_IP_HMAC_SECRET}
        max-entries-per-ip: 5
        rate-limit-per-minute: 10
```

Enable scanning in main application:

```kotlin
@SpringBootApplication
@ConfigurationPropertiesScan
class Application

fun main(args: Array<String>) {
    runApplication<Application>(*args)
}
```

## Conditional Beans

Use `@ConditionalOnProperty` for feature flags:

```kotlin
@Configuration
class FeatureConfiguration {

    @Bean
    @ConditionalOnProperty(
        name = ["features.email-notifications.enabled"],
        havingValue = "true",
        matchIfMissing = false,
    )
    fun emailNotificationService(
        emailClient: EmailClient,
    ): NotificationService = EmailNotificationService(emailClient)

    @Bean
    @ConditionalOnProperty(
        name = ["features.email-notifications.enabled"],
        havingValue = "false",
        matchIfMissing = true,
    )
    fun noOpNotificationService(): NotificationService = NoOpNotificationService()
}
```

## Profile-Specific Configuration

```kotlin
@Configuration
@Profile("dev")
class DevConfiguration {
    @Bean
    fun emailService(): EmailService = MockEmailService()
}

@Configuration
@Profile("prod")
class ProdConfiguration {
    @Bean
    fun emailService(smtpClient: SmtpClient): EmailService = SmtpEmailService(smtpClient)
}
```

## Security Configuration

WebFlux security with OAuth2 and CSRF protection for SPAs:

```kotlin
@Configuration
@EnableWebFluxSecurity
@EnableReactiveMethodSecurity
class SecurityConfiguration(
    val securityProperties: ApplicationSecurityProperties,
) {

    @Bean
    fun filterChain(http: ServerHttpSecurity): SecurityWebFilterChain {
        return http
            .csrf { csrf ->
                // CSRF enabled with cookie-based tokens for SPA compatibility
                csrf.csrfTokenRepository(
                    CookieServerCsrfTokenRepository.withHttpOnlyFalse().apply {
                        // Match Axios default header name
                        setHeaderName("X-XSRF-TOKEN")
                    }
                )
                .csrfTokenRequestHandler(SpaCsrfTokenRequestHandler())
            }
            .cors { cors ->
                cors.configurationSource(corsConfigurationSource())
            }
            .authorizeExchange { exchanges ->
                exchanges
                    .pathMatchers(HttpMethod.OPTIONS, "/**").permitAll()
                    .pathMatchers("/api/public/**", "/api/health-check").permitAll()
                    .pathMatchers("/api/admin/**").hasAuthority(Role.ADMIN.key())
                    .pathMatchers("/api/**").authenticated()
                    .pathMatchers("/actuator/health", "/actuator/info").permitAll()
                    .pathMatchers("/actuator/**").authenticated()
            }
            .oauth2Login(withDefaults())
            .oauth2ResourceServer { oauth2 ->
                oauth2.jwt { jwt ->
                    jwt.jwtAuthenticationConverter(authenticationConverter())
                }
            }
            .build()
    }
}
```

> **Note:** CSRF is enabled by default. Only disable for purely stateless APIs that use
> JWT in Authorization headers (not cookies) and have no web UI endpoints.

## R2DBC Configuration

```kotlin
@Configuration
@EnableR2dbcAuditing
class R2dbcConfiguration {

    @Bean
    fun auditorAware(): ReactiveAuditorAware<String> {
        return ReactiveAuditorAware {
            ReactiveSecurityContextHolder.getContext()
                .map { it.authentication?.name ?: "system" }
                .defaultIfEmpty("system")
        }
    }
}
```

Connection pool in `application.yml`:

```yaml
spring:
    r2dbc:
        url: r2dbc:postgresql://${DB_HOST:localhost}:${DB_PORT:5432}/${DB_NAME:cvix}
        username: ${DB_USER:cvix}
        password: ${DB_PASSWORD}
        pool:
            initial-size: 5
            max-size: 20
            max-idle-time: 30m
            validation-query: SELECT 1
```

## WebClient Configuration

```kotlin
@Configuration
class WebClientConfiguration {

    @Bean
    fun webClient(): WebClient = WebClient.builder()
        .codecs { codecs ->
            codecs.defaultCodecs().maxInMemorySize(16 * 1024 * 1024)  // 16MB
        }
        .build()

    @Bean
    fun externalApiClient(
        @Value("\${external.api.base-url}") baseUrl: String,
        @Value("\${external.api.timeout:30s}") timeout: Duration,
    ): WebClient = WebClient.builder()
        .baseUrl(baseUrl)
        .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
        .clientConnector(
            ReactorClientHttpConnector(
                HttpClient.create()
                    .responseTimeout(timeout)
                    .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, timeout.toMillis().toInt())
            )
        )
        .build()
}
```

## Domain Port to Adapter Wiring

Wire domain port interfaces to infrastructure adapters:

```kotlin
@Configuration
class WaitlistConfiguration {

    // WaitlistSecurityConfig is a domain port (interface in domain layer)
    // WaitlistSecurityProperties is the infrastructure adapter (implements the port)
    @Bean
    fun waitlistSecurityConfig(
        properties: WaitlistSecurityProperties,
    ): WaitlistSecurityConfig = object : WaitlistSecurityConfig {
        override val ipHmacSecret: String = properties.ipHmacSecret
        override val maxEntriesPerIp: Int = properties.maxEntriesPerIp
    }

    // WaitlistMetrics is a domain port
    // WaitlistMetricsAdapter is the infrastructure adapter (uses Micrometer)
    @Bean
    fun waitlistMetrics(
        meterRegistry: MeterRegistry,
    ): WaitlistMetrics = WaitlistMetricsAdapter(meterRegistry)
}
```

## Bean Lifecycle

```kotlin
@Configuration
class LifecycleConfiguration {

    @Bean(initMethod = "init", destroyMethod = "close")
    fun connectionPool(): ConnectionPool {
        return ConnectionPool()
    }

    // Or use @PostConstruct / @PreDestroy in the class
}
```

## Anti-Patterns

```kotlin
// ❌ WRONG: Spring annotations on application services
@Service  // org.springframework.stereotype.Service
class UserCreator(
    @Autowired private val repository: UserRepository,  // Field injection!
)

// ✅ CORRECT: Wire via configuration
// application/UserCreator.kt - NO Spring annotations
class UserCreator(
    private val repository: UserRepository,
)

// infrastructure/configuration/UserConfiguration.kt
@Configuration
class UserConfiguration {
    @Bean
    fun userCreator(repository: UserRepository) = UserCreator(repository)
}

// ❌ WRONG: Hardcoded values
@Bean
fun apiClient() = WebClient.builder()
    .baseUrl("https://api.example.com")  // Hardcoded!
    .build()

// ✅ CORRECT: Externalize configuration
@Bean
fun apiClient(
    @Value("\${api.base-url}") baseUrl: String,
) = WebClient.builder()
    .baseUrl(baseUrl)
    .build()

// ❌ WRONG: Using @Value for complex configuration
@Service
class MyService(
    @Value("\${feature.timeout}") timeout: Long,
    @Value("\${feature.retries}") retries: Int,
    @Value("\${feature.enabled}") enabled: Boolean,
)

// ✅ CORRECT: Use @ConfigurationProperties
@ConfigurationProperties(prefix = "feature")
data class FeatureProperties(
    val timeout: Duration,
    val retries: Int,
    val enabled: Boolean,
)
```

## Related References

- [cqrs-handlers.md](./cqrs-handlers.md) - Application services wired as beans
- [repositories.md](./repositories.md) - R2DBC configuration
