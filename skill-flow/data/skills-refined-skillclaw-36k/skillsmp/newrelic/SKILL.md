---
name: newrelic
description: Monitor applications, investigate performance issues, and analyze observability data in New Relic. Use when the user needs APM metrics, error tracking, infrastructure monitoring, or incident analysis.
metadata:
  short-description: New Relic observability and monitoring
---

# New Relic

## Overview

This skill provides a structured workflow for querying New Relic observability data. It ensures consistent integration with the New Relic MCP server for application performance monitoring (APM), error tracking, infrastructure metrics, distributed tracing, log analysis, and incident management.

## Prerequisites
- New Relic MCP server must be connected and accessible via API key
- Confirm access to the relevant New Relic account and applications
- Ensure `NEW_RELIC_API_KEY` environment variable is set

## Required Workflow

**Follow these steps in order. Do not skip steps.**

### Step 0: Set up New Relic MCP (if not already configured)

If any MCP call fails because New Relic MCP is not connected, pause and set it up:

1. Add the New Relic MCP:
   - `codex mcp add newrelic --url https://mcp.newrelic.com/mcp/`
2. Enable remote MCP client:
   - Set `[features] rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
3. Configure API credentials:
   - Set environment variable: `NEW_RELIC_API_KEY`
   - The API key should have appropriate permissions (read access minimum, write for incident acknowledgement)
   - Optional: Set `NEW_RELIC_ACCOUNT_ID` as default account (can be overridden per tool call)

After successful configuration, the user will need to restart codex. You should finish your answer and tell them so when they try again they can continue with Step 1.

### Step 1
Clarify the user's goal and scope (e.g., performance investigation, error analysis, capacity planning, incident response). Confirm application names/IDs, time ranges, metric types, and alert priorities as needed.

### Step 2
Select the appropriate workflow (see Practical Workflows below) and identify the New Relic MCP tools you will need. Confirm required identifiers (application name, entity GUID, incident ID) before calling tools.

### Step 3
Execute New Relic MCP tool calls in logical batches:
- Query first (metrics, applications, incidents) to gather context
- Analyze patterns (errors, latency, throughput, resource usage)
- For complex investigations, explain the analysis approach before executing multiple queries
- Use NRQL for detailed analysis with proper time filters (`SINCE`, `UNTIL`)

### Step 4
Summarize findings, highlight anomalies or trends, propose next actions (further investigation, configuration changes, alert acknowledgement, incident escalation), and provide actionable recommendations.

## Available Tools

**Application Performance**: `list_apm_applications`, `get_app_performance`, `get_app_errors`, `get_application_slow_transactions_details`, `get_application_top_database_operations_details`

**NRQL Queries**: `run_nrql_query`, `query_logs`

**Incident Management**: `list_open_incidents`, `list_open_incidents_rest`, `acknowledge_incident`, `list_alert_policies`

**Entity Discovery**: `search_entities`, `get_entity_details`, `list_related_entities`

**Infrastructure**: `get_infrastructure_hosts`, `get_metric_data_for_host`, `list_metric_names_for_host`

**Synthetic Monitoring**: `list_synthetics_monitors`, `create_simple_browser_monitor`

**Dashboards** (if supported): `list_dashboards`, `get_dashboard`, `create_dashboard`

## Practical Workflows

### Performance Analysis
**Goal**: Identify slow endpoints, database bottlenecks, and optimize application performance.

**Steps**:
1. List APM applications → Identify target application
2. Get app performance metrics → Check response time, throughput, Apdex
3. Query slow transactions → Find top 10 slowest endpoints with NRQL
4. Analyze database operations → Identify slow queries
5. Check infrastructure → Verify CPU/memory aren't bottlenecks
6. Provide optimization recommendations

**Example NRQL**:
```sql
SELECT average(duration), max(duration), count(*) 
FROM Transaction 
WHERE appName = 'MyApp' 
SINCE 24 hours ago 
FACET name 
ORDER BY average(duration) DESC 
LIMIT 10
```

### Error Investigation
**Goal**: Diagnose application errors, find root causes, track error rates.

**Steps**:
1. Get app errors → Check error rate and count
2. Query detailed errors → Find error messages and stack traces
3. Group by error type → Identify most common errors
4. Correlate with transactions → Find affected endpoints
5. Check for recent deployments or changes
6. Provide root cause analysis

**Example NRQL**:
```sql
SELECT errorMessage, error.class, stackTrace, duration, transactionName
FROM TransactionError 
WHERE appName = 'MyApp' 
AND error IS true 
SINCE 30 minutes ago 
LIMIT 50
ORDER BY timestamp DESC
```

### Incident Triage
**Goal**: Monitor alerts, acknowledge incidents, reduce MTTR.

**Steps**:
1. List open incidents (filter by CRITICAL/WARNING)
2. Get incident details and affected entities
3. Acknowledge critical incidents with status update
4. Query related metrics to understand impact
5. Check for cascading failures or dependencies
6. Provide incident summary and next steps

**Example**:
```
1. list_open_incidents(priority="CRITICAL")
2. get_entity_details(guid="ENTITY_GUID")
3. acknowledge_incident(incident_id=12345, message="Investigating payment latency")
4. run_nrql_query("SELECT * FROM Transaction WHERE appName='PaymentService' AND error IS true SINCE 30 minutes ago")
```

### Log Analysis
**Goal**: Search application logs to debug issues and understand system behavior.

**Steps**:
1. Query logs with keywords or patterns
2. Filter by log level (ERROR, WARN, INFO)
3. Group by application or environment
4. Correlate with trace IDs or transaction IDs
5. Identify patterns and anomalies

**Example NRQL**:
```sql
SELECT timestamp, level, message, logger, threadName
FROM Log 
WHERE message LIKE '%timeout%' 
AND level = 'ERROR' 
SINCE 1 hour ago 
ORDER BY timestamp DESC 
LIMIT 100
```

### Capacity Planning
**Goal**: Analyze resource usage trends and forecast scaling needs.

**Steps**:
1. Get infrastructure hosts → Check CPU, memory, disk
2. Query throughput trends over time
3. Analyze peak vs. average load
4. Check database connection pool usage
5. Identify resource constraints
6. Provide scaling recommendations

**Example NRQL**:
```sql
SELECT average(cpuPercent), max(cpuPercent), average(memoryUsedPercent)
FROM SystemSample 
SINCE 7 days ago 
FACET hostname 
TIMESERIES 1 day
```

### Infrastructure Health Check
**Goal**: Monitor host-level metrics and identify resource constraints.

**Steps**:
1. List infrastructure hosts → Get all hosts
2. Check CPU usage → Identify high CPU hosts
3. Check memory usage → Identify memory pressure
4. Check disk usage → Identify storage issues
5. Correlate with application performance
6. Provide health summary

### Synthetic Monitoring
**Goal**: Proactively monitor availability and performance from external locations.

**Steps**:
1. List synthetic monitors → Check status
2. Identify failed monitors
3. Analyze failure patterns (geographic, time-based)
4. Check success rate trends
5. Create new monitors for critical endpoints

## Tips for Maximum Productivity

- **Always use time filters**: Add `SINCE` clause to NRQL queries to limit data volume (e.g., `SINCE 1 hour ago`, `SINCE 24 hours ago`)
- **Start broad, drill down**: Begin with high-level metrics (app performance, error rate), then query details
- **Use FACET for grouping**: Group results by endpoint, error type, host (e.g., `FACET name`, `FACET error.class`)
- **Leverage TIMESERIES**: Visualize trends over time (e.g., `TIMESERIES 5 minutes`, `TIMESERIES 1 day`)
- **Combine data sources**: Correlate `Transaction` with `TransactionError`, `SystemSample` with `Transaction`
- **Cache application IDs**: Reuse application names/GUIDs across multiple queries
- **Batch related queries**: Execute multiple NRQL queries in parallel when investigating complex issues
- **Use ORDER BY**: Rank results (slowest endpoints, most frequent errors) with `ORDER BY average(duration) DESC`

## Troubleshooting

- **Authentication Errors**: Verify `NEW_RELIC_API_KEY` has appropriate permissions; check account ID is correct; re-authenticate if needed
- **Query Timeouts**: Reduce time range (use shorter `SINCE` intervals); limit result sets with `LIMIT`; avoid complex aggregations without filters
- **Missing Data**: Confirm application instrumentation is active; check data retention policies; verify entity is reporting
- **Rate Limits**: Batch queries; use specific filters to reduce data volume; implement exponential backoff for retries
- **NRQL Syntax Errors**: Validate metric names with `list_metric_names_for_host`; check NRQL syntax at https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/get-started/introduction-nrql-new-relics-query-language/
- **Incident Acknowledgement Failures**: Verify incident ID is correct; check incident state (can't acknowledge already closed incidents); ensure API key has write permissions

## Best Practices

### Query Optimization
- Use `LIMIT` to prevent excessive result sets (100-1000 rows)
- Apply `WHERE` filters before `FACET` for better performance
- Use `TIMESERIES` with appropriate intervals (1 minute for real-time, 1 day for trends)
- Avoid `SELECT *` - specify needed attributes

### Security
- Use read-only API keys for monitoring agents
- Grant write permissions only for incident management
- Rotate API keys regularly
- Never commit API keys to version control

### Investigation Methodology
1. **Scope**: Identify affected applications and time range
2. **Metrics**: Gather high-level performance data
3. **Errors**: Check for error spikes or patterns
4. **Infrastructure**: Verify resources aren't constrained
5. **Logs**: Search for error messages and stack traces
6. **Correlate**: Connect metrics, errors, and logs
7. **Root Cause**: Provide evidence-based diagnosis
8. **Recommend**: Actionable next steps
