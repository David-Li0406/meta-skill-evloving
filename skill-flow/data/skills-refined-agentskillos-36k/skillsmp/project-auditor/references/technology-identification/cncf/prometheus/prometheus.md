# Prometheus

**Category**: cncf
**Description**: Monitoring system and time series database
**Homepage**: https://prometheus.io

---

## TIER 1: Quick Detection (SBOM-based)

### Package Detection

#### NPM
*Prometheus client packages*

- `prom-client` - Prometheus client for Node.js
- `express-prometheus-middleware` - Express middleware

#### PYPI
*Prometheus Python packages*

- `prometheus-client` - Official Python client
- `prometheus-flask-exporter` - Flask exporter
- `prometheus-fastapi-instrumentator` - FastAPI instrumentator
- `django-prometheus` - Django integration

#### GO
*Prometheus Go packages*

- `github.com/prometheus/client_golang` - Official Go client
- `github.com/prometheus/common` - Common utilities
- `github.com/prometheus/prometheus` - Prometheus server

#### MAVEN
*Prometheus Java packages*

- `io.prometheus:simpleclient` - Java client
- `io.prometheus:simpleclient_hotspot` - JVM metrics
- `io.prometheus:simpleclient_httpserver` - HTTP server
- `io.micrometer:micrometer-registry-prometheus` - Micrometer registry

#### RUBYGEMS
*Prometheus Ruby packages*

- `prometheus-client` - Ruby client
- `prometheus-client-mmap` - Multi-process client
- `yabeda-prometheus` - Yabeda adapter

#### NUGET
*Prometheus .NET packages*

- `prometheus-net` - .NET client
- `prometheus-net.AspNetCore` - ASP.NET Core integration

#### CARGO
*Prometheus Rust packages*

- `prometheus` - Rust client
- `prometheus-static-metric` - Static metrics

---

## TIER 2: Deep Detection (File-based)

### Configuration Files
*Known configuration files that indicate Prometheus usage*

- `prometheus.yml` - Prometheus configuration
- `prometheus.yaml` - Alternative config
- `alertmanager.yml` - Alertmanager config
- `rules/*.yml` - Alerting rules
- `recording_rules.yml` - Recording rules

### Import Patterns

#### JavaScript/TypeScript
Extensions: `.js`, `.ts`

**Pattern**: `from\s+['"]prom-client['"]`
- prom-client import
- Example: `import { Counter, Histogram } from 'prom-client';`

#### Python
Extensions: `.py`

**Pattern**: `^from\s+prometheus_client\s+import`
- prometheus_client import
- Example: `from prometheus_client import Counter, Gauge, start_http_server`

#### Go
Extensions: `.go`

**Pattern**: `"github\.com/prometheus/client_golang/prometheus"`
- Prometheus Go client import
- Example: `import "github.com/prometheus/client_golang/prometheus"`

#### Java
Extensions: `.java`

**Pattern**: `import\s+io\.prometheus\.`
- Prometheus Java import
- Example: `import io.prometheus.client.Counter;`

### Code Patterns

**Pattern**: `Counter\(|Gauge\(|Histogram\(|Summary\(`
- Prometheus metric types
- Example: `Counter('http_requests_total', 'Total HTTP requests')`

**Pattern**: `/metrics|prometheus\.io/scrape`
- Prometheus metrics endpoint
- Example: `http://localhost:9090/metrics`

**Pattern**: `:9090|:9091|:9093`
- Prometheus default ports
- Example: `prometheus:9090`

**Pattern**: `scrape_configs:|global:|alerting:`
- Prometheus config sections
- Example: `scrape_configs:`

**Pattern**: `PROMETHEUS_|prometheus\.yml`
- Prometheus environment and config
- Example: `PROMETHEUS_CONFIG_FILE`

---

## Environment Variables

- `PROMETHEUS_CONFIG_FILE` - Config file path
- `PROMETHEUS_STORAGE_PATH` - Data storage path
- `PROMETHEUS_PORT` - Prometheus port
- `PROMETHEUS_MULTIPROC_DIR` - Multi-process directory

## Detection Notes

- Default port is 9090
- /metrics endpoint exposes metrics
- PromQL is the query language
- Alertmanager handles alerting
- Often paired with Grafana

---

## Secrets Detection

### Credentials

#### Prometheus Basic Auth
**Pattern**: `basic_auth:.*?password:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Prometheus basic auth password in config
**Multiline**: true

#### Prometheus Bearer Token
**Pattern**: `bearer_token:\s*['"]?([^\s'"]+)['"]?`
**Severity**: critical
**Description**: Prometheus bearer token for scrape target

---

## TIER 3: Configuration Extraction

### Scrape Interval Extraction

**Pattern**: `scrape_interval:\s*['"]?([0-9]+[smh])['"]?`
- Prometheus scrape interval
- Extracts: `scrape_interval`
- Example: `scrape_interval: 15s`

### Job Name Extraction

**Pattern**: `job_name:\s*['"]?([a-zA-Z0-9_-]+)['"]?`
- Prometheus job name
- Extracts: `job_name`
- Example: `job_name: 'kubernetes-pods'`
