<!--
Copyright (c) 2025 Crash Override Inc. - https://crashoverride.com

SPDX-License-Identifier: GPL-3.0
-->

# Monitoring and Observability Capability

Comprehensive guide to implementing monitoring and observability practices based on DORA research.

## Core Definitions

### Monitoring

**Definition**: Tooling or technical solution that allows teams to watch and understand the state of their systems using predefined metrics or logs.

**Purpose**:
- Track known system states
- Measure performance metrics
- Alert on threshold violations
- Trend analysis over time

### Observability

**Definition**: Tooling or technical solution that allows teams to actively debug their system by exploring unanticipated patterns and properties.

**Purpose**:
- Investigate unknown problems
- Explore system behavior interactively
- Understand emergent properties
- Debug production issues in real-time

### Key Distinction

- **Monitoring**: Tells you **what** is wrong (predefined metrics)
- **Observability**: Helps you understand **why** it's wrong (exploratory analysis)

## Essential Capabilities

Teams should implement:

1. **System Health Reporting**
   - Overall system status
   - Component health checks
   - Dependency status
   - Resource utilization

2. **Customer Experience Monitoring**
   - User-facing metrics
   - Real user monitoring (RUM)
   - Synthetic transaction monitoring
   - User journey tracking

3. **Business Metrics Tracking**
   - Key performance indicators (KPIs)
   - Transaction volumes
   - Conversion rates
   - Revenue metrics

4. **Production Debugging**
   - Distributed tracing
   - Log aggregation and search
   - Metric exploration
   - Real-time query capabilities

5. **Unknown Unknowns Identification**
   - Pattern detection
   - Anomaly detection
   - Correlation analysis
   - Root cause analysis

6. **Infrastructure Tracing**
   - Service-to-service calls
   - Request flows across boundaries
   - Dependency mapping
   - Performance bottleneck identification

## Implementation Approaches

### Blackbox (Synthetic) Monitoring

**Definition**: Sends input to systems like customers would, measuring responses without knowledge of internal implementation.

**Characteristics**:
- Sampling-based method
- External perspective
- User simulation
- End-to-end validation

**Components**:

1. **Scheduling System**
   - Probe frequency control
   - Geographic distribution
   - Load balancing
   - Time-based scheduling

2. **Validation Engine**
   - Response code verification
   - Content validation (regex, DOM parsing)
   - Performance threshold checking
   - Availability confirmation

3. **Failure Storage**
   - Snapshot capture on failure
   - Historical failure data
   - Diagnostic information
   - Trend analysis

**Example Synthetic Tests**:
```bash
# HTTP endpoint check
curl -f -s -o /dev/null https://api.example.com/health || alert "API down"

# Login flow test
selenium-test user-login-flow.js

# Transaction completion test
synthetic-test checkout-flow --timeout 30s
```

**Use Cases**:
- API availability monitoring
- User flow validation
- Performance regression detection
- Geographic availability testing

### Whitebox Monitoring

**Definition**: Collects signals from workloads themselves, providing internal system state visibility.

**Core Components**:

#### 1. Metrics

**Definition**: Numeric measurements of system behavior.

**Types**:

**Counters**:
```python
# Monotonically increasing values
http_requests_total
errors_total
bytes_processed_total
```

**Distributions** (Histograms/Summaries):
```python
# Value distributions over time
http_request_duration_seconds
database_query_duration_milliseconds
response_size_bytes
```

**Gauges**:
```python
# Point-in-time measurements
cpu_usage_percent
memory_available_bytes
active_connections
queue_depth
```

**Best Practices**:
- Use counters for accumulating values
- Use gauges for current state
- Use histograms for latency measurements
- Include labels for dimensions (service, environment, region)

#### 2. Logs

**Definition**: Append-only records of work states with timestamps and metadata.

**Structure**:
```json
{
  "timestamp": "2024-11-21T10:30:45.123Z",
  "level": "ERROR",
  "service": "api-gateway",
  "message": "Database connection failed",
  "error": "ETIMEDOUT",
  "query": "SELECT * FROM users WHERE id = ?",
  "duration_ms": 5000,
  "trace_id": "abc123",
  "span_id": "def456"
}
```

**Structured Logging**:
```python
# Good: Structured
logger.info("user_login",
           user_id=user.id,
           ip=request.ip,
           duration_ms=duration)

# Bad: Unstructured
logger.info(f"User {user.id} logged in from {request.ip} in {duration}ms")
```

**Log Levels**:
- **TRACE**: Detailed execution flow
- **DEBUG**: Debugging information
- **INFO**: Informational messages
- **WARN**: Warning conditions
- **ERROR**: Error conditions
- **FATAL**: Fatal errors

#### 3. Traces

**Definition**: Spans showing request paths through distributed systems.

**Structure**:
```
Trace ID: abc123
├─ Span: api-gateway (100ms)
│  ├─ Span: auth-service (20ms)
│  └─ Span: user-service (60ms)
│     ├─ Span: database-query (40ms)
│     └─ Span: cache-lookup (5ms)
```

**OpenTelemetry Example**:
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("process_request") as span:
    span.set_attribute("user.id", user_id)
    span.set_attribute("request.method", "POST")

    # Process request
    result = process_user_request(user_id)

    span.set_attribute("response.status", 200)
    span.add_event("request_processed")
```

**Key Concepts**:
- **Trace**: Complete request journey
- **Span**: Single operation within trace
- **Context Propagation**: Passing trace ID across services
- **Sampling**: Selective trace collection (e.g., 1% of requests)

## Instrumentation Strategy

### Code Instrumentation

**Definition**: Adding code to expose internal system state.

**Examples**:

**Connection Pool Monitoring**:
```python
pool_size = Gauge('db_connection_pool_size', 'Database connection pool size')
pool_available = Gauge('db_connection_pool_available', 'Available connections')

def get_connection():
    pool_size.set(pool.total_connections)
    pool_available.set(pool.available_connections)
    return pool.acquire()
```

**Service Invocation Tracking**:
```python
service_calls = Counter('external_service_calls_total',
                       'External service calls',
                       ['service', 'method', 'status'])

@instrument_call
def call_external_service(service, method):
    try:
        response = http.request(service, method)
        service_calls.labels(service, method, response.status).inc()
        return response
    except Exception as e:
        service_calls.labels(service, method, 'error').inc()
        raise
```

**Queue Depth Monitoring**:
```python
queue_depth = Gauge('message_queue_depth', 'Message queue depth', ['queue'])

def monitor_queues():
    for queue in queues:
        depth = get_queue_depth(queue.name)
        queue_depth.labels(queue.name).set(depth)
```

### Auto-Instrumentation

**Libraries and Frameworks**:
- OpenTelemetry auto-instrumentation
- APM agent instrumentation (Datadog, New Relic)
- Language-specific libraries

**Example (Python)**:
```bash
pip install opentelemetry-instrumentation-flask
opentelemetry-instrument flask run
```

## Critical Implementation Patterns

### Cardinality & Dimensionality Management

#### Cardinality

**Definition**: Measure of distinct values in a dimension.

**Examples**:
- **Low cardinality**: HTTP status codes (5 values: 1xx, 2xx, 3xx, 4xx, 5xx)
- **Medium cardinality**: Service names (10-100 services)
- **High cardinality**: User IDs (millions of users)

**Impact**:
```
Metric: http_requests_total{user_id, endpoint, method}

Low cardinality:
- 10 endpoints × 5 methods = 50 time series

High cardinality:
- 1M users × 10 endpoints × 5 methods = 50M time series
```

**Best Practices**:
- Avoid user IDs, session IDs in metric labels
- Use aggregation for high-cardinality data
- Store high-cardinality data in logs/traces
- Use sampling for expensive operations

#### Dimensionality

**Definition**: Recording multiple data points with timestamps and metadata.

**Structure**:
```python
metric_name{
  environment="production",
  service="api-gateway",
  cluster="us-east-1",
  version="v2.3.1"
} value timestamp
```

**Impact**:
- More dimensions = more storage
- More compute for queries
- Better filtering and aggregation

**Balance**:
```python
# Good: Reasonable dimensions
http_requests{service, environment, status_code}

# Bad: Excessive dimensions
http_requests{service, environment, status_code, user_id, session_id, ip_address}
```

### Alert Strategy: Symptom vs Cause

#### Cause-Based Alerting (Anti-Pattern)

**Definition**: Alert on internal conditions that might cause problems.

**Example**:
```yaml
# Bad: Cause-based alerts
alerts:
  - name: DiskUsageHigh
    condition: disk_usage > 80%
  - name: MemoryHigh
    condition: memory_usage > 90%
  - name: CPUHigh
    condition: cpu_usage > 85%
```

**Problems**:
- Too many alerts
- False positives
- Alert fatigue
- May not indicate actual user impact

#### Symptom-Based Alerting (Best Practice)

**Definition**: Alert on user-facing impact.

**Example**:
```yaml
# Good: Symptom-based alerts
alerts:
  - name: HighErrorRate
    condition: error_rate > 1%
    impact: Users seeing errors

  - name: SlowResponses
    condition: p95_latency > 1000ms
    impact: Slow user experience

  - name: ServiceDown
    condition: availability < 99.9%
    impact: Service unavailable
```

**Benefits**:
- Actionable alerts
- Clear user impact
- Lower alert volume
- Reduced fatigue

**Implementation**:
```python
# Symptom-based metrics
success_rate = (successful_requests / total_requests) * 100
error_rate = (failed_requests / total_requests) * 100
availability = (uptime / total_time) * 100

# Alert on symptoms
if success_rate < 99.0:
    alert("User-facing error rate exceeded threshold")

if p95_latency > SLO_LATENCY:
    alert("User experience degraded - slow responses")
```

### Configuration Management

**Best Practices**:

1. **Version Control**:
```bash
monitoring/
├── alerts/
│   ├── api-gateway.yaml
│   ├── database.yaml
│   └── frontend.yaml
├── dashboards/
│   ├── overview.json
│   └── service-specific.json
└── scrape-configs/
    └── prometheus.yaml
```

2. **Code Review**:
- Pull request workflow
- Peer review of alert changes
- Test alerts in staging
- Gradual rollout

3. **CI/CD Integration**:
```yaml
# .github/workflows/monitoring.yml
name: Deploy Monitoring Config

on:
  push:
    paths:
      - 'monitoring/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Validate configs
        run: promtool check config monitoring/prometheus.yaml
      - name: Deploy to production
        run: kubectl apply -f monitoring/
```

4. **Documentation**:
```yaml
# alerts/api-gateway.yaml
- alert: HighErrorRate
  expr: rate(http_errors_total[5m]) > 0.01
  for: 5m
  annotations:
    summary: "High error rate on {{ $labels.service }}"
    description: "Error rate is {{ $value }}% (threshold: 1%)"
    runbook: "https://wiki.example.com/runbooks/high-error-rate"
    impact: "Users experiencing errors on API calls"
    action: "Check logs, review recent deployments, check dependencies"
```

## Measurement Metrics

Track organizational monitoring effectiveness:

### Velocity Metrics

**Configuration Changes per Week**:
```
Metric: Number of merged PRs to monitoring configs
Goal: Demonstrate improvement velocity
Calculation: COUNT(merged_prs WHERE path LIKE 'monitoring/%') / weeks
```

**Alert Creation Rate**:
```
Metric: New alerts added per month
Goal: Track monitoring coverage growth
Calculation: COUNT(new_alerts) / month
```

### Quality Metrics

**False Positive Rate**:
```
Metric: Alerts that didn't require action
Goal: Measure alert actionability
Calculation: (non_actionable_alerts / total_alerts) × 100%
Target: < 5%
```

**False Negative Rate**:
```
Metric: Incidents not detected by alerts
Goal: Identify detection gaps
Calculation: (undetected_incidents / total_incidents) × 100%
Target: < 1%
```

**Alert Acknowledgement Time**:
```
Metric: Time from alert to acknowledgement
Goal: Response time SLA compliance
Calculation: AVG(ack_time - alert_time)
Target: < 5 minutes
```

### Operational Metrics

**Out-of-Hours Alerts Percentage**:
```
Metric: Alerts triggering outside business hours
Goal: Leading indicator of on-call load
Calculation: (after_hours_alerts / total_alerts) × 100%
Target: Decreasing trend
```

**Team Alerting Balance**:
```
Metric: Distribution of alerts across team members
Goal: Equitable alert distribution
Calculation: STDDEV(alerts_per_person)
Target: Low standard deviation
```

**MTTD (Mean Time to Detect)**:
```
Metric: Time from incident start to detection
Goal: Faster problem identification
Calculation: AVG(detected_at - incident_start)
Target: < 5 minutes
```

**MTTR (Mean Time to Recovery)**:
```
Metric: Time from detection to resolution
Goal: Faster incident resolution
Calculation: AVG(resolved_at - detected_at)
Target: < 1 hour (Elite), < 1 day (High)
```

## Common Pitfalls

### Organizational Anti-Patterns

**Single Monitoring Owner**:
- Creates bottleneck
- Single point of failure
- Slows down improvements
- **Solution**: Distributed ownership, team responsibility

**Operations-Only Changes**:
- Developers lack context
- Slower feedback loops
- Knowledge silos
- **Solution**: Developers manage their service monitoring

**Email Distribution Lists**:
- Diffusion of responsibility
- Delayed response
- Lost alerts
- **Solution**: Direct alerts to on-call engineers, chat channels

### Technical Anti-Patterns

**Perfect Dashboard Curation**:
- Becomes outdated quickly
- Doesn't match actual usage
- High maintenance burden
- **Solution**: Self-service dashboards, frequent iteration

**Mixed Dashboard Types**:
- Operational metrics mixed with business metrics
- Different audiences, different needs
- Confusing to users
- **Solution**: Separate dashboards for operations, business, executives

**Cause-Based Alerting**:
- Too many alerts
- High false positive rate
- Alert fatigue
- **Solution**: Symptom-based alerting, SLO-based alerts

## Tools & Frameworks

### Open Source

**Metrics**:
- Prometheus
- InfluxDB
- Graphite
- Victoria Metrics

**Logs**:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Loki (Grafana)
- Fluentd
- Vector

**Traces**:
- Jaeger
- Zipkin
- OpenTelemetry

**Dashboards**:
- Grafana
- Kibana
- Chronograf

### Commercial

**All-in-One**:
- Datadog
- New Relic
- Dynatrace
- AppDynamics

**Specialized**:
- Splunk (logs)
- SignalFx (metrics)
- Lightstep (traces)
- Honeycomb (observability)

### Standards

**OpenTelemetry**:
- Vendor-neutral instrumentation
- Unified API for metrics, logs, traces
- Language SDKs
- Collector architecture

**Log Libraries**:
- log4j (Java)
- structlog (Python)
- bunyan (Node.js)
- log4net/Nlog (.NET)

## Success Indicators

High-performing teams show:

1. **Distributed Expertise**:
   - All developers can create/modify monitoring
   - Monitoring knowledge spread across team
   - No single monitoring expert

2. **Data-Driven Decisions**:
   - Metrics inform architectural decisions
   - Performance regressions caught early
   - Capacity planning based on trends

3. **Low Alert Fatigue**:
   - High signal-to-noise ratio
   - Actionable alerts only
   - <5% false positive rate

4. **Rapid Response**:
   - Quick symptom-to-action pathways
   - Clear runbooks
   - Effective on-call rotations

5. **Continuous Evolution**:
   - Regular monitoring improvements
   - Configuration in version control
   - Automated deployment

## Implementation Checklist

### Foundation
- [ ] Centralized logging infrastructure
- [ ] Metrics collection system
- [ ] Distributed tracing capability
- [ ] Basic dashboards for each service

### Automation
- [ ] Auto-instrumentation for common frameworks
- [ ] Automated alert deployment
- [ ] Configuration in version control
- [ ] CI/CD for monitoring configs

### Alerting
- [ ] Symptom-based alerts defined
- [ ] SLO-based alerting
- [ ] Runbooks for all alerts
- [ ] On-call rotation established

### Observability
- [ ] Request tracing across services
- [ ] Log aggregation and search
- [ ] Metric exploration tools
- [ ] Anomaly detection

### Culture
- [ ] Developers own service monitoring
- [ ] Blameless postmortems
- [ ] Regular monitoring reviews
- [ ] Knowledge sharing sessions

## References

- DORA Monitoring and Observability Guide: https://dora.dev/capabilities/monitoring-and-observability/
- OpenTelemetry: https://opentelemetry.io/
- Google SRE Book - Monitoring: https://sre.google/sre-book/monitoring-distributed-systems/
- Prometheus Best Practices: https://prometheus.io/docs/practices/
