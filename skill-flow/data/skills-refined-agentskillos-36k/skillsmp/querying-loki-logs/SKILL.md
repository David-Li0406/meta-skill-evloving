---
name: querying-loki-logs
description: Use when querying Loki logs for debugging, investigating errors, tracing requests, or analyzing log patterns across testbeds
version: 1.0.0
trigger: log analysis, loki, logql, debugging logs, log query, tail logs, log volume
---

# Querying Loki Logs

Query Grafana Loki logs for debugging and analysis. Uses **Grafana's datasource proxy API** (not direct Loki access) since testbed Loki instances are only exposed through Grafana.

## When to Use

- Investigating errors, exceptions, or unexpected behavior
- Tracing request flows across services
- Analyzing log patterns and volumes
- Tailing logs during active debugging
- Answering "what happened between time X and Y?"

## Prerequisites

Access to Grafana instances with Loki datasource configured. Testbeds use Grafana proxy API.

```bash
# Test connectivity (replace with actual testbed values)
curl -s -u "admin:password" "https://grafana-host/api/datasources/proxy/uid/nvo/loki/api/v1/labels"
```

## Architecture

Testbed Loki instances are **not directly accessible**. Instead:

1. Grafana exposes Loki via its **datasource proxy** endpoint
2. API path: `https://<grafana_url>/api/datasources/proxy/uid/<datasource_uid>/loki/api/v1/<endpoint>`
3. Authentication: Basic auth to Grafana (not Loki)

**LogCLI cannot be used** - it requires direct Loki access. Use `curl` instead.

## Querying via Grafana Proxy

### Base URL Pattern

```
https://<grafana_url>/api/datasources/proxy/uid/<datasource_uid>/loki/api/v1/<endpoint>
```

### Available Endpoints

| Endpoint | Purpose | Method |
|----------|---------|--------|
| `/labels` | List all label names | GET |
| `/label/<name>/values` | List values for label | GET |
| `/query_range` | Query logs with time range | GET |
| `/query` | Instant query (metrics) | GET |
| `/series` | Find matching series | GET |
| `/tail` | Stream logs (WebSocket) | WS |

### Query Examples

```bash
# Set testbed variables (from loki-testbeds.yaml)
GRAFANA_URL="https://ws3r1-log.ep1test.com"
DATASOURCE_UID="nvo"
AUTH="admin:Extreme@123"
BASE="${GRAFANA_URL}/api/datasources/proxy/uid/${DATASOURCE_UID}/loki/api/v1"

# List all labels
curl -s -u "$AUTH" "$BASE/labels" | jq -r '.data[]'

# List values for a label
curl -s -u "$AUTH" "$BASE/label/app/values" | jq -r '.data[]'

# Query logs (last 5 minutes)
START=$(date -d '5 minutes ago' +%s)000000000
END=$(date +%s)000000000
curl -s -u "$AUTH" "$BASE/query_range" \
  --data-urlencode 'query={app="nvo-network"}' \
  --data-urlencode 'limit=100' \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END" | jq '.data.result[].values[][1]'

# Query with line filter
curl -s -u "$AUTH" "$BASE/query_range" \
  --data-urlencode 'query={app="nvo-network"} |= `error`' \
  --data-urlencode 'limit=50' \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END" | jq '.data.result[].values[][1]'

# Instant query (count errors)
curl -s -u "$AUTH" "$BASE/query" \
  --data-urlencode 'query=count_over_time({app="nvo-network"} |= `error` [5m])' | jq '.data.result'
```

### Time Formats

Loki expects nanosecond Unix timestamps:

```bash
# Current time in nanoseconds
date +%s000000000

# 1 hour ago
date -d '1 hour ago' +%s000000000

# Specific time
date -d '2024-01-15T10:00:00Z' +%s000000000
```

## Testbed Configuration

### Config File Location

Resolution order (first found wins):
1. **`$LOKI_TESTBEDS_CONFIG`** - Environment variable pointing to config file
2. **`./loki-testbeds.yaml`** - Relative to this skill's directory

### Config File Format

```yaml
testbeds:
  ws3r1:
    grafana_url: https://ws3r1-log.ep1test.com
    datasource_uid: nvo
    username: admin
    password: ${LOKI_PASSWORD:-password}
  
  g2r1:
    grafana_url: https://g2r1-log.ep1test.com
    datasource_uid: nvo
    username: readonly
    password: ${LOKI_PASSWORD:-password}
```

### Environment Variable Expansion

Values wrapped in `${VAR_NAME}` are expanded from environment variables at query time. Supports default values: `${VAR:-default}`.

### Resolving Testbed to API Endpoint

**User MUST specify a testbed explicitly.** When user says "query ws3r1 for errors":

1. Locate config file (`$LOKI_TESTBEDS_CONFIG` → `./loki-testbeds.yaml`)
2. Read and parse YAML
3. Look up testbed by name (error if not found)
4. Expand any `${ENV_VAR}` references
5. Build curl command:

```bash
# Testbed: ws3r1
GRAFANA_URL="https://ws3r1-log.ep1test.com"
DATASOURCE_UID="nvo"
AUTH="admin:Extreme@123"
BASE="${GRAFANA_URL}/api/datasources/proxy/uid/${DATASOURCE_UID}/loki/api/v1"

curl -s -u "$AUTH" "$BASE/query_range" \
  --data-urlencode 'query={app="nvo-network"} |= `error`' \
  --data-urlencode 'limit=100' \
  --data-urlencode "start=$(date -d '1 hour ago' +%s)000000000" \
  --data-urlencode "end=$(date +%s)000000000"
```

### If Testbed Not Specified

Ask user: "Which testbed should I query? Available: ws2r1, ws3r1, ws4r1, g2r1, st2r1, nvo2"

(List comes from config file keys)

## Loki API Reference (via Grafana Proxy)

All commands use this pattern:
```bash
curl -s -u "$AUTH" "$BASE/<endpoint>" [params]
```

Where `$AUTH` and `$BASE` are set from testbed config (see above).

### Labels - Discover Available Labels

```bash
# List all label names
curl -s -u "$AUTH" "$BASE/labels" | jq -r '.data[]'

# List values for a specific label
curl -s -u "$AUTH" "$BASE/label/namespace/values" | jq -r '.data[]'
curl -s -u "$AUTH" "$BASE/label/app/values" | jq -r '.data[]'
curl -s -u "$AUTH" "$BASE/label/pod/values" | jq -r '.data[]'
```

**Use first** to understand what's available before building queries.

### Query Range - Fetch Log Lines

```bash
# Basic query (last hour)
START=$(date -d '1 hour ago' +%s)000000000
END=$(date +%s)000000000

curl -s -u "$AUTH" "$BASE/query_range" \
  --data-urlencode 'query={app="api-gateway"}' \
  --data-urlencode 'limit=100' \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END" | jq '.data.result[].values[][1]'

# With line filter
curl -s -u "$AUTH" "$BASE/query_range" \
  --data-urlencode 'query={app="api-gateway"} |= `error`' \
  --data-urlencode 'limit=100' \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END" | jq '.data.result[].values[][1]'

# Include timestamps
curl -s -u "$AUTH" "$BASE/query_range" \
  --data-urlencode 'query={app="api-gateway"}' \
  --data-urlencode 'limit=50' \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END" | jq -r '.data.result[].values[] | "\(.[0] | tonumber / 1000000000 | strftime("%Y-%m-%d %H:%M:%S")) \(.[1])"'

# Direction (forward = oldest first, backward = newest first)
curl -s -u "$AUTH" "$BASE/query_range" \
  --data-urlencode 'query={app="api-gateway"}' \
  --data-urlencode 'limit=50' \
  --data-urlencode 'direction=forward' \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END"
```

### Query - Instant Metric Queries

```bash
# Count errors in last 5 minutes
curl -s -u "$AUTH" "$BASE/query" \
  --data-urlencode 'query=count_over_time({app="api-gateway"} |= `error` [5m])' | jq '.data.result'

# Rate of requests per second
curl -s -u "$AUTH" "$BASE/query" \
  --data-urlencode 'query=rate({app="api-gateway"} [1m])' | jq '.data.result'

# Top 5 pods by log volume
curl -s -u "$AUTH" "$BASE/query" \
  --data-urlencode 'query=topk(5, count_over_time({namespace="nvo"}[1h]) by (pod))' | jq '.data.result'
```

**Use for aggregations** - returns computed values, not log lines.

### Series - Find Active Streams

```bash
# List all streams matching selector
curl -s -u "$AUTH" "$BASE/series" \
  --data-urlencode 'match[]={namespace="nvo"}' \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END" | jq '.data'

# Count unique label combinations
curl -s -u "$AUTH" "$BASE/series" \
  --data-urlencode 'match[]={app="api-gateway"}' \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END" | jq '.data | length'
```

**Use to understand cardinality** before expensive queries.

### Common Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `query` | LogQL query string | `{app="x"} \|= "error"` |
| `start` | Start time (nanoseconds) | `$(date -d '1h ago' +%s)000000000` |
| `end` | End time (nanoseconds) | `$(date +%s)000000000` |
| `limit` | Max results | `100` |
| `direction` | Sort order | `forward` (oldest first), `backward` (newest first) |

## LogQL Query Patterns

### Stream Selectors (Label Matchers)

```logql
# Exact match
{app="api-gateway"}

# Not equal
{app!="debug-service"}

# Regex match
{app=~"api-.*"}

# Regex not match
{app!~"test-.*"}

# Multiple labels (AND)
{namespace="prod", app="api-gateway", level="error"}

# Filter by filename (exclude rotated/gzipped logs)
{job="my-service", filename=~".*server.log"}
```

### Line Filters

```logql
# Contains (case-sensitive) - use backticks for special chars
{app="api-gateway"} |= `error`

# Not contains
{app="api-gateway"} != `healthcheck`

# Regex match
{app="api-gateway"} |~ `(?i)error|exception|fatal`

# Regex not match
{app="api-gateway"} !~ `DEBUG|TRACE`

# Multi-value match
{job="device-connector"} |~ `(CONNECTED|DELETED).*`

# Chained filters (AND - most selective first for performance)
{app="api-gateway"} |= `error` != `healthcheck` |~ `user_id=\d+`
```

**Quoting styles:**
- Double quotes: `"error"` - standard, requires escaping
- Backticks: `` `error` `` - no escaping needed, preferred for regex/special chars

### Parsers

#### `| json` - Parse JSON logs

```logql
{app="api-gateway"} | json
{app="api-gateway"} | json | level="error"
{app="api-gateway"} | json | status >= 500
```

#### `| logfmt` - Parse key=value logs

```logql
{app="api-gateway"} | logfmt
{app="api-gateway"} | logfmt | level="error" | duration > 1s
```

#### `| regexp` - Extract with named capture groups

```logql
# Extract fields from unstructured logs
{job="my-service"} | regexp `user_id=(?P<user_id>[0-9]+).*status=(?P<status>[A-Z]+)`

# Filter on extracted fields
{job="my-service"} | regexp `duration=(?P<dur>\d+)ms` | dur > 1000
```

#### `| pattern` - Template-based extraction

```logql
# Parse: 192.168.1.1 - - [15/Jan/2024:10:00:00] "GET /api/users" 200
{app="nginx"} | pattern `<ip> - - [<_>] "<method> <path>" <status>`
{app="nginx"} | pattern `<ip> - - [<_>] "<method> <path>" <status>` | status >= 400
```

### Filtering Extracted Labels

After parsing, filter on extracted fields:

```logql
# String comparison
| level="error"
| event=~`(CONNECTED|DISCONNECTED)`

# Numeric comparison  
| status >= 400
| duration > 1m

# Filter out empty fields (important after regex extraction)
| owner_id != ""
| device_make != ""
```

**Common pattern:** Always filter empty fields after optional regex captures.

### Formatting Output

```logql
# Reformat log line
{job="my-service"} | json | line_format "{{._time}} - {{.serialnumber}} {{.msg}}"

# Include timestamp and level
{job="my-service"} | json | line_format "{{.timestamp}} {{.level}} {{.message}}"
```

### Quick Reference

| Goal | Pattern |
|------|---------|
| Exclude rotated logs | `filename=~".*server.log"` |
| Case-insensitive match | `` \|~ `(?i)error` `` |
| Multi-value OR | `` \|~ `(A\|B\|C)` `` |
| Extract fields | `` \| regexp `(?P<name>pattern)` `` |
| Filter empty fields | `\| field != ""` |
| Duration comparison | `\| duration > 1m` |
| Reformat output | `` \| line_format "{{.field}}" `` |

## LogQL Metric Queries

Use `logcli instant-query` for aggregations that return computed values, not log lines.

### count_over_time - Count Matching Lines

```logql
# Count errors in last 5 minutes
count_over_time({app="api-gateway"} |= `error` [5m])

# Count by label
sum by (level) (count_over_time({app="api-gateway"} | json [1h]))

# Count events by type after regex extraction
sum by (event) (count_over_time(
  {job="my-service"} 
  | regexp `event=(?P<event>[A-Z_]+)` 
  [1m]
))
```

### rate - Events Per Second

```logql
# Requests per second
rate({app="api-gateway"} [1m])

# Error rate by service
sum by (app) (rate({namespace="prod"} |= `error` [5m]))
```

### sum by - Group Aggregations

```logql
# Count by partition
sum by (partition) (count_over_time(
  {job="my-service"} 
  | regexp `partition=(?P<partition>[0-9]+)` 
  [1h]
))

# Count by multiple dimensions
sum by (event, owner_id) (count_over_time(
  {job="my-service"} 
  | regexp `event=(?P<event>[A-Z_]+).*owner_id=(?P<owner_id>[0-9]+)` 
  [1h]
))
```

### topk / bottomk - Find Extremes

```logql
# Top 3 noisiest pods
topk(3, sum by (pod) (count_over_time({namespace="prod"} [1h])))

# Top 3 busiest (event, serial_number) combinations
topk(3, sum by (event, serial_number) (count_over_time(
  {job="my-service"} 
  | regexp `event=(?P<event>[A-Z_]+).*serial=(?P<serial_number>[A-Z0-9-]+)` 
  [1h]
)))

# Bottom 3 (least active)
bottomk(3, sum by (partition) (count_over_time(
  {job="my-service"} 
  | regexp `partition=(?P<partition>[0-9]+)` 
  [1h]
)))
```

### unwrap - Extract Numeric Values

Use `unwrap` to extract numeric fields for mathematical aggregations.

```logql
# Max queue length by filename
max by (filename) (max_over_time(
  {job="my-service"} 
  | regexp `queue length (?P<queue_length>[0-9]+)` 
  | unwrap queue_length 
  [1m]
))

# Sum of durations (using duration_seconds for time values)
sum_over_time(
  {job="my-service"} 
  | regexp `completed in (?P<duration>.*)\.` 
  | unwrap duration_seconds(duration) 
  [1m]
)

# Max running workers
max by (filename) (max_over_time(
  {job="my-service"} 
  | regexp `running=(?P<running>[0-9]+)` 
  | unwrap running 
  [1s]
))
```

**unwrap functions:**
- `unwrap field` - numeric field
- `unwrap duration_seconds(field)` - parse duration string (1m, 500ms, etc.)
- `unwrap bytes(field)` - parse byte string (1KB, 5MB, etc.)

### quantile_over_time - Percentiles

```logql
# P95 response time
quantile_over_time(0.95,
  {app="api-gateway"} 
  | json 
  | unwrap response_time_ms 
  [5m]
)

# P50 (median) by endpoint
quantile_over_time(0.5,
  {app="api-gateway"} 
  | json 
  | unwrap duration 
  [1h]
) by (endpoint)
```

### Combining Patterns

```logql
# Rate graph for specific message type
sum by (job) (rate({job="my-service"} |= `RECONNECT` [1m]))

# Pause/Resume counts by state per 5 minutes
sum by (filename, state) (count_over_time(
  {job="my-service"} 
  | regexp `Consumer (?P<state>paused|resumed)` 
  [5m]
))
```

### Quick Reference

| Goal | Function |
|------|----------|
| Count lines | `count_over_time({...} [range])` |
| Lines per second | `rate({...} [range])` |
| Group by label | `sum by (label) (...)` |
| Top N | `topk(N, ...)` |
| Bottom N | `bottomk(N, ...)` |
| Max of numeric field | `max_over_time(... \| unwrap field [range])` |
| Sum of numeric field | `sum_over_time(... \| unwrap field [range])` |
| Percentile | `quantile_over_time(0.95, ... \| unwrap field [range])` |
| Parse duration | `unwrap duration_seconds(field)` |

## Debugging Workflow

Follow this sequence when investigating issues. Each step narrows focus before running expensive queries.

### Step 1: Set Up Testbed Variables

```bash
# User specifies testbed (required) - e.g., "query ws3r1 for errors"
# Agent reads config and sets variables:
GRAFANA_URL="https://ws3r1-log.ep1test.com"
DATASOURCE_UID="nvo"
AUTH="admin:Extreme@123"
BASE="${GRAFANA_URL}/api/datasources/proxy/uid/${DATASOURCE_UID}/loki/api/v1"

# Set time range (reusable)
START=$(date -d '1 hour ago' +%s)000000000
END=$(date +%s)000000000
```

If user doesn't specify: "Which testbed should I query? Available: ws2r1, ws3r1, ws4r1, g2r1, st2r1, nvo2"

### Step 2: Discover Labels

```bash
# What labels exist?
curl -s -u "$AUTH" "$BASE/labels" | jq -r '.data[]'

# What apps/jobs are available?
curl -s -u "$AUTH" "$BASE/label/job/values" | jq -r '.data[]'
curl -s -u "$AUTH" "$BASE/label/app/values" | jq -r '.data[]'
curl -s -u "$AUTH" "$BASE/label/namespace/values" | jq -r '.data[]'
```

**Goal:** Understand what's queryable before building selectors.

### Step 3: Check Volume (Find Noisy Sources)

```bash
# Count logs by app in last hour
curl -s -u "$AUTH" "$BASE/query" \
  --data-urlencode 'query=sum by (app) (count_over_time({namespace="nvo"}[1h]))' | \
  jq -r '.data.result[] | "\(.metric.app): \(.value[1])"' | sort -t: -k2 -rn
```

**Goal:** Identify high-volume services, avoid querying everything.

### Step 4: Query Logs

Start broad, then narrow:

```bash
# Broad: Recent errors
curl -s -u "$AUTH" "$BASE/query_range" \
  --data-urlencode 'query={job="nvo-network"} |= `error`' \
  --data-urlencode 'limit=100' \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END" | jq '.data.result[].values[][1]'

# Narrower: Specific error type
curl -s -u "$AUTH" "$BASE/query_range" \
  --data-urlencode 'query={job="nvo-network"} |= `connection refused`' \
  --data-urlencode 'limit=100' \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END" | jq '.data.result[].values[][1]'

# With timestamps
curl -s -u "$AUTH" "$BASE/query_range" \
  --data-urlencode 'query={job="nvo-network"} |= `error`' \
  --data-urlencode 'limit=50' \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END" | \
  jq -r '.data.result[].values[] | "\(.[0] | tonumber / 1000000000 | strftime("%Y-%m-%d %H:%M:%S")) \(.[1])"'
```

**Tips:**
- Use `direction=forward` for chronological order (tracing a flow)
- Pipe to `jq` for parsing JSON output
- Use `jq -r` for raw string output

### Step 5: Quantify (Metrics)

Once you understand the issue, quantify it:

```bash
# How often is this happening?
curl -s -u "$AUTH" "$BASE/query" \
  --data-urlencode 'query=count_over_time({job="nvo-network"} |= `error` [1h])' | jq '.data.result'

# Which pods are affected?
curl -s -u "$AUTH" "$BASE/query" \
  --data-urlencode 'query=sum by (pod) (count_over_time({job="nvo-network"} |= `error` [1h]))' | \
  jq -r '.data.result[] | "\(.metric.pod): \(.value[1])"'

# Top offenders
curl -s -u "$AUTH" "$BASE/query" \
  --data-urlencode 'query=topk(5, sum by (pod) (count_over_time({job="nvo-network"} |= `error` [1h])))' | \
  jq -r '.data.result[] | "\(.metric.pod): \(.value[1])"'
```

### Workflow Summary

| Step | Action | Purpose |
|------|--------|---------|
| 1 | Set testbed variables | Get `$BASE`, `$AUTH` |
| 2 | Query `/labels` | Discover what's available |
| 3 | Query `count_over_time by (app)` | Find noisy sources |
| 4 | Query `/query_range` | Fetch log lines |
| 5 | Query `/query` with metrics | Quantify with aggregations |

## Common Mistakes

### Missing Testbed Variables

```
# Always set these first from testbed config:
GRAFANA_URL="https://ws3r1-log.ep1test.com"
DATASOURCE_UID="nvo"
AUTH="admin:Extreme@123"
BASE="${GRAFANA_URL}/api/datasources/proxy/uid/${DATASOURCE_UID}/loki/api/v1"
```

Agent must always resolve testbed to these variables.

### Missing Time Range

```
# Always set start/end times (nanoseconds)
START=$(date -d '1 hour ago' +%s)000000000
END=$(date +%s)000000000

curl -s -u "$AUTH" "$BASE/query_range" \
  --data-urlencode 'query={app="x"}' \
  --data-urlencode "start=$START" \
  --data-urlencode "end=$END"
```

### Querying Too Broad

```
{namespace="nvo"}                    # All logs in namespace
{namespace="nvo", job="api-gateway"} # Specific service
{namespace="nvo"} |= `error`         # With filter
```

Always add label matchers or line filters to narrow scope.

### Wrong Time Range

```
# When investigating last 10 minutes, don't query 24 hours
START=$(date -d '10 minutes ago' +%s)000000000  # Appropriate
```

Start small, expand if needed.

### Forgetting Empty Field Filter

```
| regexp `user=(?P<user>\d+)` | user="123"             # Fails if regex doesn't match
| regexp `user=(?P<user>\d+)` | user!="" | user="123"  # Filter empty first
```

After optional regex captures, always filter `| field != ""`.

### Using Quotes Instead of Backticks for Regex

```
|~ "(error|warn)"     # Requires escaping
|~ `(error|warn)`     # No escaping needed
```

Prefer backticks for patterns with special characters.

### Slow Filters Last

```
{app="x"} |~ `complex.*regex` |= `error`  # Regex runs on all lines
{app="x"} |= `error` |~ `complex.*regex`  # Regex runs on fewer lines
```

Put most selective (fastest) filters first.

### Not URL-Encoding Query

```bash
# WRONG - query not encoded
curl "$BASE/query_range?query={app=x}"

# RIGHT - use --data-urlencode
curl -s -u "$AUTH" "$BASE/query_range" \
  --data-urlencode 'query={app="x"} |= `error`'
```

Always use `--data-urlencode` for the query parameter.

## Domain-Specific Examples

For project-specific query patterns, see the `references/` directory:
- `references/nvo-examples.md` - NVO service queries (device onboarding, Kafka infra, etc.)

Add your own reference files as needed.
