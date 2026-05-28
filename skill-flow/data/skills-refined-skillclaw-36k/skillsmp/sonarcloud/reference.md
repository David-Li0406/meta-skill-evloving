# SonarCloud API Reference

Complete parameter and response documentation for all endpoints.

## Issues (`/api/issues/search`)

### Parameters

| Parameter | Description | Values |
| --------- | ----------- | ------ |
| `organization` | Org key | Required |
| `componentKeys` | Project key(s) | Comma-separated |
| `types` | Issue types | `BUG`, `VULNERABILITY`, `CODE_SMELL`, `SECURITY_HOTSPOT` |
| `severities` | Severity | `BLOCKER`, `CRITICAL`, `MAJOR`, `MINOR`, `INFO` |
| `statuses` | Status | `OPEN`, `CONFIRMED`, `REOPENED`, `RESOLVED`, `CLOSED` |
| `resolutions` | Resolution | `FALSE-POSITIVE`, `WONTFIX`, `FIXED`, `REMOVED` |
| `resolved` | Filter | `true`, `false` |
| `branch` | Branch name | String |
| `pullRequest` | PR number | String |
| `createdAfter` | Date filter | `YYYY-MM-DD` |
| `createdBefore` | Date filter | `YYYY-MM-DD` |
| `languages` | Languages | `java`, `typescript`, `python`, etc. |
| `rules` | Rule keys | Comma-separated |
| `tags` | Issue tags | Comma-separated |
| `assignees` | Assigned users | Comma-separated |
| `authors` | Code authors | Comma-separated |
| `scopes` | Scope | `MAIN`, `TEST` |
| `inNewCodePeriod` | New code only | `true`, `false` |
| `facets` | Aggregations | `severities`, `types`, `rules`, `tags` |
| `p` | Page number | Integer (1-based) |
| `ps` | Page size | Integer (max 500) |
| `s` | Sort field | `CREATION_DATE`, `UPDATE_DATE`, `SEVERITY` |
| `asc` | Sort order | `true`, `false` |

### Response

```json
{
  "total": 150,
  "paging": { "pageIndex": 1, "pageSize": 100, "total": 150 },
  "issues": [{
    "key": "AYx...",
    "rule": "typescript:S1234",
    "severity": "MAJOR",
    "component": "my-project:src/file.ts",
    "line": 42,
    "message": "Remove this unused variable.",
    "type": "CODE_SMELL",
    "status": "OPEN",
    "effort": "5min",
    "tags": ["unused"],
    "creationDate": "2024-01-15T10:30:00+0000"
  }],
  "facets": [{ "property": "severities", "values": [{ "val": "MAJOR", "count": 50 }] }]
}
```

---

## Metrics (`/api/measures/component`)

### Parameters

| Parameter | Description |
| --------- | ----------- |
| `component` | Project key (required) |
| `metricKeys` | Metrics (comma-separated) |
| `branch` | Branch name |
| `pullRequest` | PR number |
| `additionalFields` | `metrics`, `periods` |

### All Metric Keys

| Category | Keys |
| -------- | ---- |
| Size | `ncloc`, `lines`, `statements`, `functions`, `classes`, `files` |
| Complexity | `complexity`, `cognitive_complexity` |
| Coverage | `coverage`, `line_coverage`, `branch_coverage`, `tests`, `test_success_density`, `uncovered_lines`, `uncovered_conditions` |
| Duplication | `duplicated_lines`, `duplicated_lines_density`, `duplicated_blocks`, `duplicated_files` |
| Issues | `bugs`, `vulnerabilities`, `code_smells`, `security_hotspots` |
| Ratings | `sqale_rating`, `reliability_rating`, `security_rating`, `security_review_rating` (1=A to 5=E) |
| Debt | `sqale_index` (minutes), `sqale_debt_ratio` (%) |
| Quality Gate | `alert_status`, `quality_gate_details` |
| New Code | `new_bugs`, `new_vulnerabilities`, `new_code_smells`, `new_coverage`, `new_duplicated_lines_density` |

### Response

```json
{
  "component": {
    "key": "my-project",
    "name": "My Project",
    "measures": [
      { "metric": "bugs", "value": "12" },
      { "metric": "coverage", "value": "78.5" },
      { "metric": "sqale_rating", "value": "2.0" }
    ]
  }
}
```

---

## Quality Gate (`/api/qualitygates/project_status`)

### Parameters

| Parameter | Description |
| --------- | ----------- |
| `projectKey` | Project key (required) |
| `branch` | Branch name |
| `pullRequest` | PR number |

### Response

```json
{
  "projectStatus": {
    "status": "ERROR",
    "conditions": [{
      "status": "ERROR",
      "metricKey": "new_coverage",
      "comparator": "LT",
      "errorThreshold": "80",
      "actualValue": "65.3"
    }],
    "ignoredConditions": false
  }
}
```

---

## Security Hotspots (`/api/hotspots/search`)

### Parameters

| Parameter | Description | Values |
| --------- | ----------- | ------ |
| `projectKey` | Project key | Required |
| `branch` | Branch name | String |
| `pullRequest` | PR number | String |
| `status` | Status | `TO_REVIEW`, `REVIEWED` |
| `resolution` | Resolution | `FIXED`, `SAFE`, `ACKNOWLEDGED` |
| `inNewCodePeriod` | New code | `true`, `false` |
| `p` / `ps` | Pagination | Integer |

### Response

```json
{
  "paging": { "total": 5 },
  "hotspots": [{
    "key": "...",
    "component": "my-project:src/auth.ts",
    "securityCategory": "sql-injection",
    "vulnerabilityProbability": "HIGH",
    "status": "TO_REVIEW",
    "message": "Make sure this SQL query is safe.",
    "line": 42
  }]
}
```

---

## Projects (`/api/projects/search`)

### Parameters

| Parameter | Description |
| --------- | ----------- |
| `organization` | Org key |
| `q` | Search query |
| `qualifiers` | `TRK` (project), `APP` |
| `p` / `ps` | Pagination |

---

## Analysis History (`/api/project_analyses/search`)

### Parameters

| Parameter | Description |
| --------- | ----------- |
| `project` | Project key |
| `branch` | Branch name |
| `from` / `to` | Date range |
| `p` / `ps` | Pagination |

### Response

```json
{
  "analyses": [{
    "key": "AYx...",
    "date": "2024-01-15T10:30:00+0000",
    "projectVersion": "1.2.0",
    "revision": "abc123def",
    "events": [{ "category": "VERSION", "name": "1.2.0" }]
  }]
}
```

---

## Metrics History (`/api/measures/search_history`)

### Parameters

| Parameter | Description |
| --------- | ----------- |
| `component` | Project key |
| `metrics` | Metric keys |
| `from` / `to` | Date range (`YYYY-MM-DD`) |
| `branch` | Branch name |
| `p` / `ps` | Pagination |

---

## Component Tree (`/api/components/tree`)

### Parameters

| Parameter | Description |
| --------- | ----------- |
| `component` | Project key |
| `branch` | Branch name |
| `qualifiers` | `FIL` (file), `DIR`, `UTS` (test) |
| `metricKeys` | Metrics per component |
| `strategy` | `children`, `leaves`, `all` |
| `q` | Search query |
| `s` / `asc` | Sort field / ascending |
| `metricSort` | Metric to sort by |

---

## Duplications (`/api/duplications/show`)

Get detailed duplicate code blocks for a specific file.

### Parameters

| Parameter | Description |
| --------- | ----------- |
| `key` | File key (required) - format: `project-key:path/to/file.ts` |
| `branch` | Branch name |
| `pullRequest` | PR number |

### Response

```json
{
  "duplications": [
    {
      "blocks": [
        {
          "from": 1,
          "size": 20,
          "_ref": "1"
        },
        {
          "from": 50,
          "size": 20,
          "_ref": "2"
        }
      ]
    }
  ],
  "files": {
    "1": {
      "key": "my-project:src/utils/helpers.ts",
      "name": "helpers.ts",
      "projectName": "My Project"
    },
    "2": {
      "key": "my-project:src/utils/common.ts",
      "name": "common.ts",
      "projectName": "My Project"
    }
  }
}
```

### Workflow: Find All Duplicates

```bash
# 1. Get files with most duplication
curl -H "Authorization: Bearer $TOKEN" \
  "https://sonarcloud.io/api/components/tree?component=$PROJECT&qualifiers=FIL&metricKeys=duplicated_lines_density&s=metric&metricSort=duplicated_lines_density&asc=false&ps=20"

# 2. For each file, get duplicate blocks
curl -H "Authorization: Bearer $TOKEN" \
  "https://sonarcloud.io/api/duplications/show?key=my-project:src/file.ts"
```

---

## Rules (`/api/rules/search`)

### Parameters

| Parameter | Description |
| --------- | ----------- |
| `languages` | Filter by language |
| `severities` | Filter by severity |
| `types` | Filter by type |
| `tags` | Filter by tags |
| `q` | Search query |
| `p` / `ps` | Pagination |

---

## Sources (`/api/sources/*`)

### Raw Source Code (`/api/sources/raw`)

| Parameter | Description |
| --------- | ----------- |
| `key` | File key (required) - format: `project:path/to/file.ts` |
| `branch` | Branch name |

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://sonarcloud.io/api/sources/raw?key=my-project:src/utils/helpers.ts"
```

### SCM Blame (`/api/sources/scm`)

| Parameter | Description |
| --------- | ----------- |
| `key` | File key (required) |
| `from` | Start line |
| `to` | End line |

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://sonarcloud.io/api/sources/scm?key=my-project:src/utils/helpers.ts"
```

**Response**: Returns author, date, and revision for each line.

---

## Compute Engine (`/api/ce/activity`)

Get background task status (analysis jobs).

| Parameter | Description |
| --------- | ----------- |
| `component` | Project key |
| `status` | `SUCCESS`, `FAILED`, `CANCELED`, `PENDING`, `IN_PROGRESS` |
| `type` | Task type (e.g., `REPORT`) |
| `minSubmittedAt` | Filter by submission date |
| `maxExecutedAt` | Filter by execution date |
| `p` / `ps` | Pagination |

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://sonarcloud.io/api/ce/activity?component=my-project&status=FAILED"
```

---

## Quality Profiles (`/api/qualityprofiles/search`)

| Parameter | Description |
| --------- | ----------- |
| `language` | Filter by language |
| `project` | Project key |
| `qualityProfile` | Profile name |

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://sonarcloud.io/api/qualityprofiles/search?language=ts"
```

---

## Languages (`/api/languages/list`)

List all supported languages.

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://sonarcloud.io/api/languages/list"
```

**Response**: `{ "languages": [{ "key": "ts", "name": "TypeScript" }, ...] }`

---

## Branches (`/api/project_branches/list`)

| Parameter | Description |
| --------- | ----------- |
| `project` | Project key (required) |

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://sonarcloud.io/api/project_branches/list?project=my-project"
```

**Response**: `{ "branches": [{ "name": "main", "isMain": true, "type": "LONG", "status": { "qualityGateStatus": "OK" } }] }`

---

## Badges (`/api/project_badges/*`)

### Measure Badge (`/api/project_badges/measure`)

| Parameter | Description |
| --------- | ----------- |
| `project` | Project key |
| `metric` | `bugs`, `coverage`, `code_smells`, `vulnerabilities`, etc. |
| `branch` | Branch name |

Returns SVG badge image.

```bash
curl "https://sonarcloud.io/api/project_badges/measure?project=my-project&metric=coverage"
```

### Quality Gate Badge (`/api/project_badges/quality_gate`)

| Parameter | Description |
| --------- | ----------- |
| `project` | Project key |
| `branch` | Branch name |

```bash
curl "https://sonarcloud.io/api/project_badges/quality_gate?project=my-project"
```

---

## Pagination Example

```bash
PAGE=1
while true; do
  R=$(curl -s -H "Authorization: Bearer $TOKEN" \
    "https://sonarcloud.io/api/issues/search?organization=$ORG&componentKeys=$PROJECT&p=$PAGE&ps=500")
  echo $R | jq '.issues[]'
  [ $((PAGE * 500)) -ge $(echo $R | jq '.total') ] && break
  PAGE=$((PAGE + 1))
done
```

---

## Error Codes

| Code | Meaning | Fix |
| ---- | ------- | --- |
| 401 | Invalid token | Check `SONARCLOUD_TOKEN` |
| 403 | No permission | Verify project access |
| 404 | Not found | Check project/org key |
| 400 | Bad request | Check parameter values |

---

## References

- [SonarCloud Web API](https://sonarcloud.io/web_api)
- [SonarCloud Docs](https://docs.sonarsource.com/sonarcloud/)
