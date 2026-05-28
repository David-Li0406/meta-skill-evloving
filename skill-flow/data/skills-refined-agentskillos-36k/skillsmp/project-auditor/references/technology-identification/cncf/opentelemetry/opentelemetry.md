# OpenTelemetry

**Category**: cncf
**Description**: Observability framework for cloud-native software
**Homepage**: https://opentelemetry.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*OpenTelemetry Node.js packages*

- `@opentelemetry/api` - API package
- `@opentelemetry/sdk-node` - Node.js SDK
- `@opentelemetry/sdk-trace-base` - Tracing SDK
- `@opentelemetry/sdk-metrics` - Metrics SDK
- `@opentelemetry/exporter-trace-otlp-http` - OTLP HTTP exporter
- `@opentelemetry/exporter-trace-otlp-grpc` - OTLP gRPC exporter
- `@opentelemetry/auto-instrumentations-node` - Auto instrumentation

#### PYPI
*OpenTelemetry Python packages*

- `opentelemetry-api` - API package
- `opentelemetry-sdk` - SDK package
- `opentelemetry-exporter-otlp` - OTLP exporter
- `opentelemetry-instrumentation` - Instrumentation base
- `opentelemetry-distro` - Distribution package

#### GO
*OpenTelemetry Go packages*

- `go.opentelemetry.io/otel` - Go API
- `go.opentelemetry.io/otel/sdk` - Go SDK
- `go.opentelemetry.io/otel/exporters/otlp` - OTLP exporter
- `go.opentelemetry.io/contrib` - Contrib packages

#### MAVEN
*OpenTelemetry Java packages*

- `io.opentelemetry:opentelemetry-api` - Java API
- `io.opentelemetry:opentelemetry-sdk` - Java SDK
- `io.opentelemetry:opentelemetry-exporter-otlp` - OTLP exporter
- `io.opentelemetry.javaagent:opentelemetry-javaagent` - Java agent

#### NUGET
*OpenTelemetry .NET packages*

- `OpenTelemetry` - .NET SDK
- `OpenTelemetry.Api` - .NET API
- `OpenTelemetry.Exporter.OpenTelemetryProtocol` - OTLP exporter
- `OpenTelemetry.Instrumentation.AspNetCore` - ASP.NET Core

#### CARGO
*OpenTelemetry Rust packages*

- `opentelemetry` - Rust API
- `opentelemetry-otlp` - OTLP exporter

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate OpenTelemetry usage*

- `otel-collector-config.yaml` - Collector configuration
- `otel-config.yaml` - OTel config

### Code Patterns

**Pattern**: `opentelemetry|otel|OTEL_`
- OpenTelemetry references
- Example: `OTEL_SERVICE_NAME=my-service`

**Pattern**: `TracerProvider|MeterProvider|LoggerProvider`
- OTel providers
- Example: `TracerProvider.builder()`

**Pattern**: `getTracer|getMeter|getLogger`
- OTel instrumentation API
- Example: `tracer = trace.get_tracer(__name__)`

**Pattern**: `@WithSpan|StartSpan|StartActiveSpan`
- Span creation patterns
- Example: `@WithSpan("operation-name")`

**Pattern**: `OTLP|otlp://|:4317|:4318`
- OTLP protocol and ports
- Example: `otlp://localhost:4317`

**Pattern**: `otelcol|otel-collector`
- OpenTelemetry Collector
- Example: `otelcol --config=config.yaml`

**Pattern**: `receivers:|exporters:|processors:|service:`
- Collector config sections
- Example: `receivers:\n  otlp:`

**Pattern**: `W3C.*traceparent|traceparent:`
- W3C trace context
- Example: `traceparent: 00-0af7651916cd43dd8448eb211c80319c-b7ad6b7169203331-01`

---

## Environment Variables

- `OTEL_SERVICE_NAME` - Service name
- `OTEL_EXPORTER_OTLP_ENDPOINT` - OTLP endpoint
- `OTEL_EXPORTER_OTLP_HEADERS` - OTLP headers
- `OTEL_TRACES_EXPORTER` - Traces exporter
- `OTEL_METRICS_EXPORTER` - Metrics exporter
- `OTEL_LOGS_EXPORTER` - Logs exporter
- `OTEL_RESOURCE_ATTRIBUTES` - Resource attributes
- `OTEL_PROPAGATORS` - Context propagators

## Detection Notes

- Three signals: traces, metrics, logs
- OTLP is the standard protocol
- Collector for receiving, processing, exporting
- Auto-instrumentation available
- Replaces OpenTracing and OpenCensus

---

## Secrets Detection

### Credentials

#### OTLP Headers
**Pattern**: `OTEL_EXPORTER_OTLP_HEADERS\s*[=:]\s*['"]?([^\s'"]+)['"]?`
**Severity**: high
**Description**: OTLP authentication headers (may contain API keys)

#### Collector Auth
**Pattern**: `headers:\s*\n\s*authorization:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Collector authorization header
**Multiline**: true

---

## TIER 3: Configuration Extraction

### Service Name Extraction

**Pattern**: `OTEL_SERVICE_NAME\s*[=:]\s*['"]?([^\s'"]+)['"]?`
- OpenTelemetry service name
- Extracts: `service_name`
- Example: `OTEL_SERVICE_NAME=my-service`

### OTLP Endpoint Extraction

**Pattern**: `OTEL_EXPORTER_OTLP_ENDPOINT\s*[=:]\s*['"]?(https?://[^\s'"]+)['"]?`
- OTLP exporter endpoint
- Extracts: `otlp_endpoint`
- Example: `OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317`

### Sampling Rate Extraction

**Pattern**: `OTEL_TRACES_SAMPLER_ARG\s*[=:]\s*['"]?([0-9.]+)['"]?`
- Trace sampling rate
- Extracts: `sampling_rate`
- Example: `OTEL_TRACES_SAMPLER_ARG=0.1`
