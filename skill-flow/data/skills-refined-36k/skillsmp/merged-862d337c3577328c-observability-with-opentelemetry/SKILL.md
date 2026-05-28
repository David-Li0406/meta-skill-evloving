---
name: observability-with-opentelemetry
description: Use this skill for implementing observability in distributed systems with OpenTelemetry, including tracing, metrics, and structured logging.
---

# OpenTelemetry Observability Patterns

## Core Observability Principles

- Guide the development of idiomatic, maintainable, and high-performance code with built-in observability.
- Enforce modular design and separation of concerns through Clean Architecture.
- Promote test-driven development and robust observability from the start.

## OpenTelemetry Integration

- Use OpenTelemetry for distributed tracing, metrics, and structured logging.
- Start and propagate tracing spans across all service boundaries.
- Use `otel.Tracer` for creating spans and `otel.Meter` for collecting metrics.
- Export data to OpenTelemetry Collector, Jaeger, or Prometheus.
- Configure appropriate sampling rates for production environments.

## Spring Boot Configuration

```kotlin
// build.gradle.kts
dependencies {
    implementation(platform("io.opentelemetry.instrumentation:opentelemetry-instrumentation-bom:2.15.0"))
    implementation("io.opentelemetry.instrumentation:opentelemetry-spring-boot-starter")
    implementation("io.micrometer:micrometer-tracing-bridge-otel")
    implementation("io.opentelemetry:opentelemetry-exporter-zipkin")

    // Sentry integration
    implementation("io.sentry:sentry-spring-boot-starter-jakarta:8.26.0")
    implementation("io.sentry:sentry-logback:8.26.0")
}
```

```yaml
# application.yaml
spring:
  application:
    name: <your-project-name>

management:
  tracing:
    sampling:
      probability: 1.0  # 100% in dev, lower in prod
  otlp:
    tracing:
      endpoint: http://localhost:4318/v1/traces

otel:
  exporter:
    otlp:
      endpoint: http://otel-collector:4317
  service:
    name: <your-project-name>
  resource:
    attributes:
      deployment.environment: ${ENVIRONMENT:dev}
      service.version: ${APP_VERSION:unknown}

sentry:
  dsn: ${SENTRY_DSN:}
  environment: ${ENVIRONMENT:dev}
  traces-sample-rate: 1.0
```

## Custom Span Creation

```kotlin
import io.opentelemetry.api.trace.Span
import io.opentelemetry.api.trace.Tracer
import io.opentelemetry.context.Context
import org.springframework.stereotype.Component

@Component
class TracingService(
    private val tracer: Tracer
) {

    fun <T> withSpan(
        spanName: String,
        attributes: Map<String, String> = emptyMap(),
        block: () -> T
    ): T {
        val span = tracer.spanBuilder(spanName)
            .setParent(Context.current())
            .startSpan()

        attributes.forEach { (key, value) ->
            span.setAttribute(key, value)
        }

        return try {
            span.makeCurrent().use {
                block()
            }
        } catch (e: Exception) {
            span.recordException(e)
            span.setStatus(io.opentelemetry.api.trace.StatusCode.ERROR, e.message ?: "Error")
            throw e
        } finally {
            span.end()
        }
    }
}
```

## Annotation-Based Tracing

```kotlin
import io.micrometer.tracing.annotation.NewSpan
import io.micrometer.tracing.annotation.SpanTag

@Service
class MessageService {

    @NewSpan("bot.sendMessage")
    suspend fun sendMessage(
        @SpanTag("telegram.chat_id") chatId: Long,
        @SpanTag("message.type") type: String
    ): Message {
        // Automatically traced
        return bot.sendMessage(ChatId(chatId), text)
    }

    @NewSpan("bot.handleCallback")
    suspend fun handleCallback(
        @SpanTag("callback.data") data: String,
        @SpanTag("telegram.user_id") userId: Long
    ) {
        // Process callback query
    }
}
```

## Baggage Propagation

```kotlin
import io.opentelemetry.api.baggage.Baggage

// Set baggage (propagates across services)
fun setUserContext(userId: String, tenantId: String) {
    Baggage.current()
        .toBuilder()
        .put("user.id", userId)
        .put("tenant.id", tenantId)
        .build()
        .makeCurrent()
}

// Read baggage
fun getCurrentUserId(): String? {
    return Baggage.current().getEntryValue("user.id")
}
```

## Metrics Collection

Monitor these key metrics across all services:

- **Request latency**: Track p50, p90, p95, and p99 percentiles.
- **Throughput**: Measure requests per second by endpoint.
- **Error rate**: Track 4xx and 5xx responses separately.
- **Resource usage**: Monitor CPU, memory, disk, and network utilization.
- **Custom business metrics**: Track domain-specific KPIs.

```kotlin
import io.micrometer.core.instrument.MeterRegistry
import io.micrometer.core.instrument.Timer

@Component
class BotMetricsService(
    private val registry: MeterRegistry
) {

    private val commandCounter = registry.counter(
        "<your-project-name>.bot.commands",
        "command", "unknown"
    )

    private val messageProcessingTimer = Timer.builder("<your-project-name>.bot.message.duration")
        .description("Time to process a message")
        .register(registry)

    fun recordCommand(command: String) {
        registry.counter("<your-project-name>.bot.commands", "command", command).increment()
    }

    fun recordCallback(action: String) {
        registry.counter("<your-project-name>.bot.callbacks", "action", action).increment()
    }

    fun <T> timeMessageProcessing(block: () -> T): T {
        return messageProcessingTimer.recordCallable(block)!!
    }
}
```

## Sentry Integration

```kotlin
import io.sentry.Sentry
import io.sentry.SentryLevel

class BotErrorHandler {

    fun handleBotException(e: Exception, chatId: Long?, command: String?) {
        Sentry.withScope { scope ->
            scope.setTag("error.type", e.javaClass.simpleName)
            scope.setTag("bot.command", command ?: "unknown")
            scope.setLevel(SentryLevel.ERROR)
            scope.setContexts("telegram", mapOf(
                "chat_id" to (chatId?.toString() ?: "unknown"),
                "command" to (command ?: "none")
            ))
            Sentry.captureException(e)
        }
    }
}
```

## OpenTelemetry Collector Config

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 1s
    send_batch_size: 1024

exporters:
  zipkin:
    endpoint: http://zipkin:9411/api/v2/spans
  prometheus:
    endpoint: 0.0.0.0:8889
  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [zipkin, logging]
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus]
```

## Alerting and Dashboards

- Create dashboards for service health and business metrics.
- Set up alerts based on SLOs and error budgets.
- Use anomaly detection for proactive issue identification.
- Document runbooks for common alert scenarios.
- Review and tune alerts regularly to reduce noise.

## Instrumentation Best Practices

- Instrument at service boundaries (entry/exit points).
- Add custom spans for database operations and external calls.
- Include relevant attributes (user ID, request type, etc.).
- Avoid over-instrumentation that creates noise.
- Use semantic conventions for consistent attribute naming.

## Production Considerations

- Configure appropriate sampling rates to balance visibility and cost.
- Use head-based sampling for consistent trace capture.
- Implement tail-based sampling for capturing errors.
- Set retention policies based on debugging needs.
- Monitor observability infrastructure health.