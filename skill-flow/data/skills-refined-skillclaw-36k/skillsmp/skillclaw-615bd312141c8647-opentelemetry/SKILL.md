---
name: opentelemetry
description: Use this skill for implementing OpenTelemetry observability patterns, including distributed tracing, metrics collection, and structured logging in your applications.
---

# OpenTelemetry Observability Patterns

## Quick Start

1. **Set Up Dependencies**: Add OpenTelemetry dependencies to your project.
   ```kotlin
   // build.gradle.kts
   dependencies {
       implementation(platform("io.opentelemetry.instrumentation:opentelemetry-instrumentation-bom:2.15.0"))
       implementation("io.opentelemetry.instrumentation:opentelemetry-spring-boot-starter")
       implementation("io.micrometer:micrometer-tracing-bridge-otel")
       implementation("io.opentelemetry:opentelemetry-exporter-zipkin")
       implementation("io.sentry:sentry-spring-boot-starter-jakarta:8.26.0")
       implementation("io.sentry:sentry-logback:8.26.0")
   }
   ```

2. **Configure Application**: Set up your application configuration for OpenTelemetry.
   ```yaml
   # application.yaml
   spring:
     application:
       name: your-project
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
       name: your-project
     resource:
       attributes:
         deployment.environment: ${ENVIRONMENT:dev}
         service.version: ${APP_VERSION:unknown}
   sentry:
     dsn: ${SENTRY_DSN:}
     environment: ${ENVIRONMENT:dev}
     traces-sample-rate: 1.0
   ```

3. **Create Custom Spans**: Implement a service to create and manage spans.
   ```kotlin
   import io.opentelemetry.api.trace.Tracer
   import io.opentelemetry.context.Context
   import org.springframework.stereotype.Component

   @Component
   class TracingService(private val tracer: Tracer) {
       fun <T> withSpan(spanName: String, attributes: Map<String, String> = emptyMap(), block: () -> T): T {
           val span = tracer.spanBuilder(spanName).setParent(Context.current()).startSpan()
           attributes.forEach { (key, value) -> span.setAttribute(key, value) }
           return try {
               span.makeCurrent().use { block() }
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

## Observability Guidelines

- **Core Principles**: Ensure maintainable code with built-in observability, enforce modular design, and promote test-driven development.
- **Tracing**: Start and propagate tracing spans across service boundaries. Use middleware for automatic instrumentation.
- **Metrics**: Monitor key metrics such as request latency, throughput, and error rates.
- **Structured Logging**: Include unique request IDs and trace context in logs. Use structured formats for machine parseability.

## Best Practices

- **Naming Conventions**: Name spans after business operations, not transport methods. Follow OpenTelemetry naming standards for metrics and attributes.
- **Error Handling**: Record errors in spans and set appropriate statuses.
- **Context Propagation**: Use W3C Trace Context for propagating context across service boundaries.

## Additional Resources

- For more detailed guidelines, refer to the OpenTelemetry documentation and best practices for instrumentation and troubleshooting.