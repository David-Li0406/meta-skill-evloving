# Honeycomb Resource Dependency Graph

Resources must be created in this order. Higher-level resources depend on lower ones.

## Dependency Hierarchy

```
Level 0 (Foundation):
├── Environment (via Management Key)
└── Dataset

Level 1 (Schema):
└── Columns (requires: Dataset)

Level 2 (Data):
└── Events (requires: Dataset, Columns auto-created if not explicit)

Level 3 (Query Layer):
├── Queries/QueryResults (requires: Dataset with data)
└── Recipients (environment-scoped, no dataset needed)

Level 4 (Monitoring):
├── Triggers (requires: Dataset, Query or inline query)
├── Boards (environment-scoped, can reference queries)
├── SLOs (requires: Dataset with numeric column for SLI)
└── Markers (requires: Dataset)

Level 5 (SLO Alerting):
└── Burn Alerts (requires: existing SLO)

Level 6 (Observability):
└── Service Map Dependencies (requires: Dataset with trace data)
```

## Resource Details

### Environment (Level 0)
- **Auth**: Management Key required
- **Dependencies**: None
- **Creation**: `POST /2/teams/{team}/environments`
- **Notes**: 
  - Team slug can be discovered via auth endpoint
  - Set `delete_protected=False` for test environments

### Dataset (Level 0)
- **Auth**: API Key
- **Dependencies**: None
- **Creation**: `POST /1/datasets`
- **Test naming**: `test-live-{timestamp}`

### Columns (Level 1)
- **Auth**: API Key
- **Dependencies**: Dataset must exist
- **Creation**: `POST /1/columns/{dataset}`
- **Notes**: Auto-created when events are sent, but explicit creation ensures types
- **Recommended test columns**:
  ```
  duration_ms  (float)
  status       (integer)
  service      (string)
  endpoint     (string)
  error        (boolean)
  trace_id     (string)
  user_id      (string)
  ```

### Events (Level 2)
- **Auth**: API Key (Ingest permission)
- **Dependencies**: Dataset exists (columns auto-created)
- **Creation**: `POST /1/events/{dataset}` or `/1/batch/{dataset}`
- **CRITICAL**: Wait 30+ seconds after sending for data to be queryable
- **Test data pattern**:
  ```python
  {"service": "api", "endpoint": "/users", "duration_ms": 45, "status": 200}
  {"service": "api", "endpoint": "/users", "duration_ms": 1200, "status": 500, "error": True}
  ```

### Recipients (Level 3)
- **Auth**: API Key
- **Dependencies**: None (environment-scoped)
- **Creation**: `POST /1/recipients`
- **Test data**: Email recipient with `test@example.com`

### Queries (Level 3)
- **Auth**: API Key
- **Dependencies**: Dataset with queryable data
- **Creation**: `POST /1/queries/{dataset}`
- **Notes**: Query Results API requires Enterprise plan

### Triggers (Level 4)
- **Auth**: API Key
- **Dependencies**: Dataset, query spec or query_id
- **Creation**: `POST /1/triggers/{dataset}`
- **Constraints**:
  - `time_range` <= 3600 seconds
  - `time_range` <= `frequency` * 4
  - Only one calculation allowed
- **Test both**: TriggerBuilder pattern AND manual TriggerCreate

### SLOs (Level 4)
- **Auth**: API Key
- **Dependencies**: Dataset with numeric column for SLI
- **Creation**: `POST /1/slos/{dataset}`
- **Notes**: The SLI column must have data to be valid

### Boards (Level 4)
- **Auth**: API Key
- **Dependencies**: None (environment-scoped), but queries useful
- **Creation**: `POST /1/boards`

### Markers (Level 4)
- **Auth**: API Key
- **Dependencies**: Dataset
- **Creation**: `POST /1/markers/{dataset}`

### Burn Alerts (Level 5)
- **Auth**: API Key
- **Dependencies**: Existing SLO (must create SLO first)
- **Creation**: `POST /1/burn_alerts/{dataset}`

### Service Map Dependencies (Level 6)
- **Auth**: API Key
- **Dependencies**: Dataset with tracing data (trace_id, parent_id, etc.)
- **Creation**: `POST /1/maps/dependencies/requests`
- **Notes**: Requires trace-enriched data, may not be testable without proper setup

## Cleanup Order

Delete in reverse dependency order:

```
1. Burn Alerts
2. SLOs, Triggers, Boards, Markers
3. Queries
4. Recipients
5. Columns (optional, deletes with dataset)
6. Dataset
7. API Key (via Management API)
8. Environment (via Management API, optional)
```

## Common Test Failures by Resource

| Resource | Common Error | Cause |
|----------|--------------|-------|
| Triggers | "time_range too large" | time_range > 3600s or > frequency*4 |
| Triggers | "multiple calculations" | TriggerBuilder allows only one |
| Queries | Empty results | Data not ingested yet (wait 30s) |
| SLOs | "column not found" | SLI column has no data |
| Burn Alerts | "SLO not found" | Create SLO first |
| Environments | 403 Forbidden | Need management key, not API key |
