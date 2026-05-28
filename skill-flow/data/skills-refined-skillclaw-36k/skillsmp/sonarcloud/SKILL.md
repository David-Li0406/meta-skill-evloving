---
name: sonarcloud
description: Pull issues, metrics, quality gates, and analysis data from SonarCloud. Use when checking code quality, security vulnerabilities, test coverage, technical debt, or CI/CD quality gates.
category: Code Quality
tags: [sonarcloud, code-quality, issues, metrics, security]
---

# SonarCloud Integration

**Base**: `https://sonarcloud.io/api` | **Auth**: `Bearer $SONARCLOUD_TOKEN`

## Quick Start

```bash
# Set credentials (generate token at sonarcloud.io/account/security)
export SONARCLOUD_TOKEN="your_token"
export SONARCLOUD_ORG="your-org"
export SONARCLOUD_PROJECT="your-project"

# Common queries
curl -H "Authorization: Bearer $TOKEN" \
  "https://sonarcloud.io/api/issues/search?organization=$ORG&componentKeys=$PROJECT&resolved=false"
curl -H "Authorization: Bearer $TOKEN" \
  "https://sonarcloud.io/api/measures/component?component=$PROJECT&metricKeys=bugs,coverage"
curl -H "Authorization: Bearer $TOKEN" \
  "https://sonarcloud.io/api/qualitygates/project_status?projectKey=$PROJECT"
```

## Endpoints

| Endpoint                        | Purpose                  | Key Params                               |
| ------------------------------- | ------------------------ | ---------------------------------------- |
| `/api/issues/search`            | Bugs, vulnerabilities    | `types`, `severities`, `branch`, `pullRequest` |
| `/api/measures/component`       | Coverage, complexity     | `metricKeys`, `branch`, `pullRequest`    |
| `/api/qualitygates/project_status` | Pass/fail status      | `projectKey`, `branch`, `pullRequest`    |
| `/api/hotspots/search`          | Security hotspots        | `projectKey`, `status`                   |
| `/api/projects/search`          | List projects            | `organization`, `q`                      |
| `/api/project_analyses/search`  | Analysis history         | `project`, `from`, `to`                  |
| `/api/measures/search_history`  | Metrics over time        | `component`, `metrics`, `from`           |
| `/api/components/tree`          | Files with metrics       | `qualifiers=FIL`, `metricKeys`           |
| `/api/duplications/show`        | Duplicate code blocks    | `key` (file key), `branch`               |
| `/api/sources/raw`              | Raw source code          | `key` (file key), `branch`               |
| `/api/sources/scm`              | SCM blame info           | `key`, `from`, `to`                      |
| `/api/ce/activity`              | Background tasks         | `component`, `status`, `type`            |
| `/api/qualityprofiles/search`   | Quality profiles         | `language`, `project`                    |
| `/api/languages/list`           | Supported languages      | -                                        |
| `/api/project_branches/list`    | Project branches         | `project`                                |
| `/api/project_badges/measure`   | SVG badge                | `project`, `metric`, `branch`            |
| `/api/rules/search`             | Coding rules             | `languages`, `severities`, `types`       |

## Common Filters

**Issues**: `types=BUG,VULNERABILITY,CODE_SMELL` | `severities=BLOCKER,CRITICAL,MAJOR` | `resolved=false` | `inNewCodePeriod=true`

**Metrics**: `bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density,sqale_rating,reliability_rating,security_rating`

**New Code**: `new_bugs,new_vulnerabilities,new_coverage,new_duplicated_lines_density`

## Workflows

### Health Check

```bash
curl ... "/api/qualitygates/project_status?projectKey=$PROJECT"
curl ... "/api/measures/component?component=$PROJECT&metricKeys=bugs,vulnerabilities,coverage,sqale_rating"
curl ... "/api/issues/search?organization=$ORG&componentKeys=$PROJECT&resolved=false&facets=severities,types&ps=1"
```

### PR Analysis

```bash
curl ... "/api/qualitygates/project_status?projectKey=$PROJECT&pullRequest=123"
curl ... "/api/issues/search?organization=$ORG&componentKeys=$PROJECT&pullRequest=123&resolved=false"
curl ... "/api/measures/component?component=$PROJECT&pullRequest=123&metricKeys=new_bugs,new_coverage"
```

### Security Audit

```bash
curl ... "/api/issues/search?organization=$ORG&componentKeys=$PROJECT&types=VULNERABILITY&resolved=false"
curl ... "/api/hotspots/search?projectKey=$PROJECT&status=TO_REVIEW"
```

### Duplication Analysis

```bash
# Get duplication metrics
curl ... "/api/measures/component?component=$PROJECT&metricKeys=duplicated_lines,duplicated_lines_density,duplicated_blocks,duplicated_files"

# Get files with most duplication
curl ... "/api/components/tree?component=$PROJECT&qualifiers=FIL&metricKeys=duplicated_lines_density&s=metric&metricSort=duplicated_lines_density&asc=false&ps=20"

# Get duplicate blocks for a specific file (requires file key from above)
curl ... "/api/duplications/show?key=my-project:src/utils/helpers.ts"
```

## Response Processing

```bash
# Count by severity
curl ... | jq '.issues | group_by(.severity) | map({severity: .[0].severity, count: length})'

# Failed quality gate conditions
curl ... | jq '.projectStatus.conditions | map(select(.status == "ERROR"))'

# Metrics as key-value
curl ... | jq '.component.measures | map({(.metric): .value}) | add'
```

## TypeScript Client

See [sonarcloud.ts](../../../next-app/src/lib/integrations/sonarcloud.ts):

```typescript
import { createSonarCloudClient } from '@/lib/integrations/sonarcloud';
const client = createSonarCloudClient('my-org');
await client.getProjectHealth('my-project');
await client.getQualityGateStatus('my-project', { pullRequest: '123' });
```

## Detailed Reference

For complete API parameters and response schemas, see [reference.md](reference.md).
