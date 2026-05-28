---
name: observability
description: Telemetry, metrics, tracing, and observability for Elixir/BEAM applications
---

# Observability Skill

Use this skill when:
- Setting up application observability
- Implementing Telemetry events
- Creating metrics dashboards
- Setting up distributed tracing
- Error tracking and alerting
- Performance monitoring
- Health checks

## Telemetry Setup

### Basic Configuration

```elixir
# config/config.exs
import Config

config :my_app, :telemetry,
  attach_handler_id: MyAppWeb.Telemetry
```

### Telemetry Handler

```elixir
# lib/my_app_web/telemetry.ex
defmodule MyAppWeb.Telemetry do
  use Telemetry.Handler

  @impl true
  def handle_event([:web, :request, :stop], measurements, metadata, _config, _handler_meta) do
    # Handle web request metrics
    :ok
  end

  @impl true
  def handle_event([:my_app, :database, :query, :stop], measurements, metadata, _config, _handler_meta) do
    # Handle database query metrics
    :ok
  end

  @impl true
  def handle_event([:my_app, :user, :created, :stop], measurements, metadata, _config, _handler_meta) do
    # Handle user creation events
    :ok
  end
end
```

## Metrics Collection

### Application Metrics

```elixir
defmodule MyApp.Telemetry do
  def increment_counter(event_name, count \\ 1) do
    :telemetry.execute([:my_app, event_name], count: count)
  end

  def histogram(event_name, value) do
    :telemetry.execute([:my_app, event_name, value: value)
  end

  def timing(event_name, start_time) do
    duration = System.monotonic_time(:millisecond) - start_time
    :telemetry.execute([:my_app, event_name, duration: duration)
  end

  def distribution(event_name, value) do
    :telemetry.execute([:my_app, event_name, value: value)
  end
end
```

## PromEx Integration

### Basic Setup

```elixir
# mix.exs
def deps do
  [
    {:prom_ex, "~> 1.0"},
    {:prometheus, "~> 4.0"},
    {:prometheus_plugs, "~> 4.0"}
  ]
end

# lib/my_app/prom_ex.ex
defmodule MyApp.PromEx do
  use PromEx

  @impl true
  def init do
    {:ok, 
      prom_ex: %{
        dashboard_assigns: [
          # Dashboard metrics
        ],
        metrics: [
          # Metric definitions
        ],
        graphs: [
          # Graph definitions
        ]
      }
    }
  end
end
```

### Metrics Definition

```elixir
# Application metrics
defmodule MyApp.ApplicationMetrics do
  use PromEx.Metric

  # Counter metrics
  defmetrics do
    [
      counter("my_app.web.requests.total"),
      counter("my_app.web.requests.2xx"),
      counter("my_app.web.requests.5xx"),
      counter("my_app.web.requests.errors")
    ]
  end

  # Histogram metrics
  defhistograms do
    [
      histogram("my_app.web.request.duration", 
        unit: {:native, :millisecond},
        buckets: [5, 10, 25, 50, 100, 250, 500, 1000, 5000]
      )
    ]

  # Summary metrics
  defsummaries do
    [
      summary("my_app.web.requests", 
        unit: :native,
        tags: [:controller, :action]
      )
    ]
  end

  def labels do
    [
      label("my_app.web.requests.total", [controller: :action])
    ]
  end
end
```

## Distributed Tracing

### OpenTelemetry

```elixir
# mix.exs
def deps do
  [
    {:opentelemetry, "~> 1.0"},
    {:opentelemetry_exporter_prometheus, "~> 1.0"},
    {:opentelemetry_resource_applications, "~> 0.3"}
  ]
end

# config/runtime.exs
import Config

config :my_app, :opentelemetry,
  resource: [
    MyApp.Repo,
    MyApp.PubSub
  ]

config :opentelemetry,
  traces_exporter: {
    Prometheus,
    [ MyApp.Traces.Exporter]
  }

config :opentelemetry,
  span_processor: MyApp.Traces.Processor
```

### Trace Processor

```elixir
# lib/my_app/traces/processor.ex
defmodule MyApp.Traces.Processor do
  use OpenTelemetry.SpanProcessor

  @impl true
  def handle_span(ctx, span, parent_context, span_context) do
    # Enrich span with application context
    {:ok, ctx}
  end
end
```

### Exporter

```elixir
# lib/my_app/traces/exporter.ex
defmodule MyApp.Traces.Exporter do
  use OpenTelemetry.SpanExporter

  @impl true
  def handle_span(ctx, span, parent_context) do
    # Send to Prometheus
    OpenTelemetry.SpanExporter.Prometheus.handle_span(ctx, span, parent_context)
  end
end
```

## Error Tracking

### Sentry Integration

```elixir
# mix.exs
def deps do
  [
    {:sentry, "~> 8.0"}
  ]
end

# lib/my_app/sentry.ex
defmodule MyApp.Sentry do
  use Sentry

  def init do
    {:ok, 
      dsn: System.get_env("SENTRY_DSN"),
      environment_name: config_env(),
      integrations: [
        {:opentelemetry, MyApp.Traces.Exporter}
      ]
    }
  end

  @impl true
  def handle_exception(event, source, stacktrace, request, extra) do
    Sentry.capture_exception(event, source, stacktrace, request, extra)
  end

  @impl true
  def handle_message(event, source, stacktrace, request, extra) do
    Sentry.capture_message(event, source, stacktrace, request, extra)
  end
end
```

## Health Checks

### Health Endpoint

```elixir
# lib/my_app_web/health_check.ex
defmodule MyAppWeb.HealthCheck do
  use Plug.Router

  plug Plug.Logger

  get "/health", to: MyAppWeb.HealthCheckController, :index
end

defmodule MyAppWeb.HealthCheckController do
  use MyAppWeb, :controller

  def index(conn, _params) do
    health_status = health_check()
    
    json(conn, %{
      status: health_status,
      version: Application.spec_version(),
      env: config_env(),
      timestamp: System.monotonic_time(:second)
    })
  end

  defp health_check do
    checks = [
      check_database(),
      check_redis(),
      check_pubsub()
    ]

    all_healthy? = Enum.all?(fn {status, _} -> status == :ok end, checks)
    
    if all_healthy? do
      :ok
    else
      :degraded
    end
  end

  defp check_database do
    case MyApp.Repo.query("SELECT 1", []) do
      {:ok, _} -> :ok
      _ -> :error
    end
  end

  defp check_redis do
    case MyApp.Redis.command("PING") do
      {:ok, _} -> :ok
      _ -> :error
    end
  end

  defp check_pubsub do
    if Phoenix.PubSub.Server.Subscription.check("my_topic") do
      :ok
    else
      :error
    end
  end
end
```

## Performance Monitoring

### Benchmarking

```elixir
# test/my_app/performance/bench.exs
defmodule MyApp.Performance.Bench do
  use Benchee

  bench "database_query", do: MyApp.Users.list()
  bench "cache_lookup", do: MyApp.Cache.get("user_1")
end
```

### Load Testing

```bash
# Using k6 or locust for load testing

# k6_script.js
import http from "k6";

export let options = {
  vus: 100,
  duration: "30s",
  thresholds: {
    http_req_duration: ["p(95)<500"],  # 95th percentile < 500ms
    http_req_failed: ["rate<0.05"]  # Error rate < 5%
  }
};

export default function() {
  const res = http.get("http://localhost:4000/api/users", options);
  check(res, {
    "http_req_duration": (res.timings.duration < options.thresholds.http_req_duration[0]),
    "http_req_failed": (res.status !== 200)
  });
}

export default function(data) {
  http.post("http://localhost:4000/api/users", JSON.stringify(data), options);
}
```

## Best Practices

### 1. Structured Logging

```elixir
# Use LoggerJSON for structured logs
defmodule MyApp.Logger do
  use LoggerJSON

  @impl true
  def init do
    {:ok, 
      level: :info,
      json_encoder: Jason
    }
  end

  def log_user_action(user_id, action, metadata) do
    info("User action",
      user_id: user_id,
      action: action,
      metadata: metadata,
      extra: %{timestamp: System.monotonic_time(:second)}
    )
  end
end
```

### 2. Metrics Best Practices

- **Name metrics clearly**: Use hierarchical naming like `my_app.web.requests.total`
- **Add labels/tags**: Use labels for filtering (controller, action, status_code)
- **Choose right metric type**: Counter, histogram, summary, or gauge
- **Set appropriate buckets**: Use exponential buckets for timing metrics
- **Document metrics**: Use `@moduledoc` to explain what metrics represent
- **Avoid high cardinality**: Don't create metrics with too many unique tag combinations

### 3. Tracing Best Practices

- **Create meaningful spans**: Use operation names that describe the action
- **Add attributes**: Include relevant metadata (user_id, request_id)
- **Keep spans short**: Avoid overly long spans that make traces hard to read
- **Use span links**: Connect parent-child spans for complex operations
- **Sample strategically**: Don't trace every request, use sampling

### 4. Error Handling Best Practices

- **Capture context**: Always include relevant metadata (user_id, request_id)
- **Fingerprint errors**: Add unique error fingerprints for deduplication
- **Set severity**: Use appropriate severity levels
- **Add breadcrumbs**: Include navigation breadcrumbs for web requests
- **Configure alerts**: Set up alerting for critical errors

### 5. Health Check Best Practices

- **Check critical dependencies**: Database, cache, external services
- **Return version info**: Include application version in health response
- **Include environment**: Always return the environment name
- **Use proper HTTP status**: 200 for healthy, 503 for degraded
- **Add metrics**: Include system metrics in health response

## Token Efficiency

Use observability for:
- **Debugging** (~50% faster than logs alone)
- **Performance insights** (~40% faster than manual profiling)
- **Capacity planning** (~30% token savings vs ad-hoc investigations)
- **Incident response** (~70% faster with distributed tracing)

## Tools to Use

- **PromEx**: Metrics and dashboards (Elixir-native)
- **Prometheus**: Metrics database and alerting
- **Grafana**: Visualization dashboards
- **Sentry**: Error tracking and alerting
- **OpenTelemetry**: Distributed tracing standard
- **k6**: Load testing
- **locust**: Alternative load testing tool
- **Benchee**: Benchmarking library

## Configuration Templates

### Prometheus Config

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "my_app"
    static_configs:
      - targets:
        - localhost:4000/metrics
```

### Grafana Dashboard Template

```elixir
# Application configuration
defmodule MyApp.Metrics.Dashboard do
  def dashboard_panels do
    [
      %{
        title: "Application Overview",
        panels: [
          %{
            title: "Request Rate",
            targets: ["my_app_web_requests_total"]
          },
          %{
            title: "Response Time",
            targets: ["my_app_web_request_duration"]
          },
          %{
            title: "Error Rate",
            targets: ["my_app_web_requests_errors_total"]
          }
        ]
      }
    ]
  end
end
```

## Examples

### Complete Observability Stack

```elixir
# Observability agent
defmodule MyApp.Observability do
  def start_link do
    {:ok, _}
  end

  def setup_telemetry do
    # Configure Telemetry events
    :telemetry.attach("my_app_web", :request, &MyAppWeb.Telemetry/1)
  end

  def setup_metrics do
    # Configure PromEx metrics
    MyApp.ApplicationMetrics.setup()
  end

  def setup_tracing do
    # Configure OpenTelemetry
    MyApp.Traces.setup()
  end

  def setup_sentry do
    # Configure Sentry error tracking
    MyApp.Sentry.setup()
  end

  def setup_health_checks do
    # Configure health check endpoints
    MyAppWeb.HealthCheck.routes()
  end
end
```

## Monitoring Checklist

- [ ] Telemetry events defined
- [ ] Telemetry handlers configured
- [ ] PromEx metrics collected
- [ ] Prometheus exporter configured
- [ ] Grafana dashboards created
- [ ] Sentry error tracking configured
- [ ] Distributed tracing configured
- [ ] Health check endpoints created
- [ ] Load testing configured
- [ ] Alerts configured
- [ ] Documentation created

## Notes

- PromEx provides Elixir-native observability with built-in dashboard
- OpenTelemetry is industry standard for distributed tracing
- Sentry integrates seamlessly with Elixir/Phoenix
- Prometheus is commonly used for metrics collection
- Grafana provides excellent visualization

## Related Skills

- **security-patterns**: For secure observability data
- **liveview-patterns**: For LiveView-specific metrics
- **otp-patterns**: For process metrics and supervision tree monitoring
