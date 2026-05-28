# Observability SRE

## Patterns


---
  #### **Name**
SLO-Based Alerting
  #### **Description**
Define SLOs first, derive alerts from SLO budget burn
  #### **When**
Setting up alerting strategy for any service
  #### **Example**
    # Step 1: Define SLIs (Service Level Indicators)
    # What can you measure that indicates service health?
    
    # Availability SLI: Percentage of successful requests
    - record: sli:availability:ratio
      expr: |
        sum(rate(http_requests_total{status!~"5.."}[5m]))
        /
        sum(rate(http_requests_total[5m]))
    
    # Latency SLI: Percentage of requests under threshold
    - record: sli:latency:ratio
      expr: |
        sum(rate(http_request_duration_seconds_bucket{le="0.5"}[5m]))
        /
        sum(rate(http_request_duration_seconds_count[5m]))
    
    # Step 2: Define SLOs (Service Level Objectives)
    # 99.9% availability = 43.8 minutes downtime per month
    # 99.5% latency = 0.5% of requests can be slow
    
    slo:
      availability:
        target: 0.999
        window: 30d
      latency:
        target: 0.995
        window: 30d
    
    # Step 3: Calculate Error Budget
    - record: slo:availability:error_budget_remaining
      expr: |
        1 - (
          (1 - sli:availability:ratio)
          /
          (1 - 0.999)  # target
        )
    
    # Step 4: Alert on Budget Burn Rate
    # Burn rate 1 = consuming budget exactly at allowed rate
    # Burn rate 10 = 10x faster, will exhaust budget in 3 days
    
    groups:
      - name: slo-alerts
        rules:
          - alert: HighErrorBudgetBurn
            expr: |
              slo:availability:error_budget_remaining < 0.9
              and
              rate(http_requests_total{status=~"5.."}[1h])
                / rate(http_requests_total[1h]) > 0.001
            for: 5m
            labels:
              severity: warning
            annotations:
              summary: "Error budget burn rate high"
              description: "Consuming error budget at {{ $value | humanizePercentage }} remaining"
    
          - alert: ErrorBudgetExhausted
            expr: slo:availability:error_budget_remaining < 0
            for: 1m
            labels:
              severity: critical
            annotations:
              summary: "Error budget exhausted"
              description: "SLO violated, error budget is {{ $value | humanizePercentage }}"
    

---
  #### **Name**
Distributed Tracing Setup
  #### **Description**
End-to-end request tracing with context propagation
  #### **When**
Debugging latency or failures across services
  #### **Example**
    # OpenTelemetry instrumentation for Python
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
    from opentelemetry.instrumentation.asyncpg import AsyncPGInstrumentor
    
    def setup_tracing(service_name: str):
        """Configure OpenTelemetry tracing."""
    
        # Create tracer provider
        provider = TracerProvider(
            resource=Resource.create({
                "service.name": service_name,
                "service.version": os.getenv("VERSION", "unknown"),
                "deployment.environment": os.getenv("ENV", "development"),
            })
        )
    
        # Export to Jaeger/Tempo
        exporter = OTLPSpanExporter(
            endpoint=os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317"),
            insecure=True
        )
        provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(provider)
    
        # Auto-instrument frameworks
        FastAPIInstrumentor.instrument()
        HTTPXClientInstrumentor.instrument()
        AsyncPGInstrumentor.instrument()
    
    # Custom span for business logic
    tracer = trace.get_tracer(__name__)
    
    async def retrieve_memories(query: str, agent_id: str):
        with tracer.start_as_current_span("retrieve_memories") as span:
            span.set_attribute("agent.id", agent_id)
            span.set_attribute("query.length", len(query))
    
            # Child span for embedding
            with tracer.start_as_current_span("generate_embedding"):
                embedding = await embed(query)
                span.set_attribute("embedding.dimensions", len(embedding))
    
            # Child span for vector search
            with tracer.start_as_current_span("vector_search"):
                results = await vector_store.search(embedding, limit=10)
                span.set_attribute("results.count", len(results))
    
            return results
    

---
  #### **Name**
Structured Logging
  #### **Description**
JSON logging with correlation IDs and context
  #### **When**
Setting up logging for any service
  #### **Example**
    import structlog
    import logging
    from contextvars import ContextVar
    
    # Context variables for request tracking
    request_id_ctx: ContextVar[str] = ContextVar("request_id", default="")
    agent_id_ctx: ContextVar[str] = ContextVar("agent_id", default="")
    
    def configure_logging():
        """Configure structured JSON logging."""
    
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.add_log_level,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.JSONRenderer()
            ],
            wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True
        )
    
    logger = structlog.get_logger()
    
    # Middleware to set context
    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        request_id_ctx.set(request_id)
    
        # Bind context for all logs in this request
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            path=request.url.path,
            method=request.method
        )
    
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
    
        logger.info(
            "request_completed",
            status_code=response.status_code,
            duration_ms=duration * 1000
        )
    
        response.headers["X-Request-ID"] = request_id
        return response
    
    # Usage in code
    async def process_memory(memory_id: str):
        logger.info("processing_memory", memory_id=memory_id)
        try:
            result = await do_work()
            logger.info("memory_processed", memory_id=memory_id)
            return result
        except Exception as e:
            logger.error("memory_processing_failed",
                        memory_id=memory_id,
                        error=str(e),
                        exc_info=True)
            raise
    

---
  #### **Name**
The Four Golden Signals Dashboard
  #### **Description**
Essential metrics every service should have
  #### **When**
Creating monitoring for any service
  #### **Example**
    # Prometheus metrics for the four golden signals
    
    from prometheus_client import Counter, Histogram, Gauge
    
    # 1. Latency - How long requests take
    REQUEST_LATENCY = Histogram(
        'http_request_duration_seconds',
        'Request latency in seconds',
        ['method', 'endpoint', 'status'],
        buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
    )
    
    # 2. Traffic - How much demand
    REQUEST_COUNT = Counter(
        'http_requests_total',
        'Total HTTP requests',
        ['method', 'endpoint', 'status']
    )
    
    # 3. Errors - Rate of failures
    ERROR_COUNT = Counter(
        'http_errors_total',
        'Total HTTP errors',
        ['method', 'endpoint', 'error_type']
    )
    
    # 4. Saturation - How full the service is
    IN_FLIGHT_REQUESTS = Gauge(
        'http_requests_in_flight',
        'Currently processing requests'
    )
    
    CONNECTION_POOL_USAGE = Gauge(
        'db_connection_pool_usage_ratio',
        'Database connection pool utilization',
        ['pool_name']
    )
    
    # Middleware to record metrics
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        IN_FLIGHT_REQUESTS.inc()
        start = time.perf_counter()
    
        try:
            response = await call_next(request)
            status = response.status_code
        except Exception as e:
            status = 500
            ERROR_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                error_type=type(e).__name__
            ).inc()
            raise
        finally:
            duration = time.perf_counter() - start
            IN_FLIGHT_REQUESTS.dec()
    
            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=request.url.path,
                status=status
            ).observe(duration)
    
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=status
            ).inc()
    
        return response
    

## Anti-Patterns


---
  #### **Name**
Alert on Causes Not Symptoms
  #### **Description**
Alerting on CPU/memory instead of user impact
  #### **Why**
High CPU might be fine if latency is normal. Users don't care about your CPU.
  #### **Instead**
Alert on latency, error rate, SLO violations

---
  #### **Name**
Alert Fatigue
  #### **Description**
Too many alerts, team ignores them
  #### **Why**
If every alert isn't actionable, the real ones get missed.
  #### **Instead**
Every alert needs runbook, expected action, ownership

---
  #### **Name**
Logs Without Context
  #### **Description**
Logs that say "Error occurred" without request ID
  #### **Why**
Can't correlate across services, can't find the request.
  #### **Instead**
Include request_id, trace_id, user_id in every log

---
  #### **Name**
Metrics Without Labels
  #### **Description**
Total request count without endpoint/status breakdown
  #### **Why**
When errors spike, which endpoint? Which error? Need labels.
  #### **Instead**
Label by endpoint, status, method - but not unbounded (no user_id)

---
  #### **Name**
Dashboard Overload
  #### **Description**
50 graphs nobody looks at
  #### **Why**
Information overload, nobody knows where to look during incident.
  #### **Instead**
One SLO dashboard, drill-down dashboards for investigation