# Advanced Slash Command Examples

This file contains advanced command patterns and examples for creating sophisticated slash commands.

## 1. Workflow Automation Commands

### Deploy Command with Environment Detection

````markdown
---
description: Deploy application with environment-specific configuration
argument-hint: [environment] [--dry-run] [--skip-tests]
allowed-tools: Bash(git:*), Bash(npm:*), Bash(docker:*)
---

# Application Deployment

Deploying to: $1
Options: $2

## Pre-deployment Checks

1. Verify current git status: !`git status`
2. Ensure working directory is clean
3. Run tests if not skipped: !`npm test`
4. Check environment configuration

## Environment-specific Deployment

### Staging ($1 = "staging" or default)

```bash
docker-compose -f docker-compose.staging.yml build
docker-compose -f docker-compose.staging.yml push
kubectl apply -f k8s/staging/
```
````

### Production ($1 = "production")

```bash
# Additional checks for production
npm run security-audit
npm run performance-test

# Deploy with zero downtime
kubectl rollout status deployment/app
```

## Post-deployment Verification

1. Health checks: !`curl -f https://$1.example.com/health`
2. Rollback on failure if needed
3. Notify team of deployment status

## Rollback Procedure

If deployment fails:

```bash
kubectl rollout undo deployment/app
kubectl rollout status deployment/app
```

````

### CI/CD Pipeline Trigger
```markdown
---
description: Trigger CI/CD pipeline for specific branch or PR
argument-hint: [branch-or-pr] [--skip-build] [--force]
allowed-tools: Bash(git:*), WebFetch
---

# CI/CD Pipeline Trigger

Target: $1
Options: $2

## Pipeline Configuration

1. Determine target type:
   - If $1 starts with "#": PR number
   - If $1 matches "*/": Branch name
   - Otherwise: Treat as branch name

2. Fetch current pipeline status
3. Queue new pipeline job

## Pipeline Steps

### Build Phase (skip with --skip-build)
- Compile TypeScript: !`npm run build`
- Run linting: !`npm run lint`
- Execute tests: !`npm run test:coverage`

### Deployment Phase
- Build Docker image
- Push to registry
- Deploy to environment

## Notifications

- Slack notifications on start/complete
- Email on failure
- GitHub status updates
````

## 2. Data Processing Commands

### Database Migration Command

````markdown
---
description: Run database migrations with rollback capability
argument-hint: [migration-name] [--dry-run] [--force]
allowed-tools: Bash, Read, Write
---

# Database Migration

Migration: $1
Options: $2

## Migration Process

1. Check migration status: !`npm run migration:status`
2. Backup current database
3. Run migration in transaction
4. Verify data integrity

## Migration Templates

### Create Table Migration

```sql
-- Migration: $1
BEGIN;

CREATE TABLE table_name (
  id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_table_name_created_at ON table_name(created_at);

COMMIT;
```
````

### Add Column Migration

```sql
-- Migration: $1
BEGIN;

ALTER TABLE table_name
ADD COLUMN new_column VARCHAR(255);

-- Update existing records if needed
UPDATE table_name
SET new_column = 'default_value'
WHERE new_column IS NULL;

COMMIT;
```

## Rollback Plan

Always include down migration:

```sql
-- Rollback for $1
BEGIN;

DROP TABLE IF EXISTS table_name;
-- or
ALTER TABLE table_name DROP COLUMN new_column;

COMMIT;
```

````

## 3. Code Generation Commands

### Component Generator with Variations
```markdown
---
description: Generate React components with multiple template options
argument-hint: [component-name] [template] [--with-tests] [--with-stories]
allowed-tools: Read, Write, Glob, Bash
---

# Component Generator

Component: $1
Template: $2
Options: $3

## Template Options

- `basic`: Simple functional component
- `with-props`: Component with TypeScript props
- `with-hooks`: Component with useState/useEffect
- `with-form`: Form component with validation
- `with-table`: Data table component

## Generation Process

1. Create component directory
2. Generate component file based on template
3. Create index.ts export
4. Add test file if requested
5. Add Storybook stories if requested
6. Update component registry

## Example: Basic Template
```tsx
import React from 'react';

export interface $1Props {
  children?: React.ReactNode;
  className?: string;
}

export const $1: React.FC<$1Props> = ({
  children,
  className = ''
}) => {
  return (
    <div className={className}>
      {children}
    </div>
  );
};

export default $1;
````

````

### API Client Generator
```markdown
---
description: Generate TypeScript API client from OpenAPI spec
argument-hint: [spec-url] [--output-dir] [--include-mocks]
allowed-tools: WebFetch, Write, Bash
---

# API Client Generator

OpenAPI Spec: $1
Output: $2
Options: $3

## Generation Steps

1. Fetch OpenAPI specification
2. Parse endpoints and schemas
3. Generate TypeScript interfaces
4. Create API client methods
5. Add mock data if requested

## Client Structure

````

src/api/
├── client.ts # Main API client
├── types.ts # Generated types
├── endpoints/ # Endpoint methods
│ ├── auth.ts
│ ├── users.ts
│ └── posts.ts
└── mocks/ # Mock data (optional)

````

## Generated Client Example

```typescript
export class ApiClient {
  private baseUrl: string;
  private apiKey?: string;

  constructor(baseUrl: string, apiKey?: string) {
    this.baseUrl = baseUrl;
    this.apiKey = apiKey;
  }

  // Auto-generated method
  async getUser(id: string): Promise<User> {
    const response = await fetch(`${this.baseUrl}/users/${id}`, {
      headers: {
        Authorization: this.apiKey ? `Bearer ${this.apiKey}` : undefined,
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch user: ${response.statusText}`);
    }

    return response.json();
  }
}
````

````

## 4. Monitoring and Debugging Commands

### Log Analyzer
```markdown
---
description: Analyze application logs for errors and patterns
argument-hint: [log-file] [--error-only] [--since]
allowed-tools: Read, Bash
---

# Log Analyzer

Analyzing: $1
Options: $2

## Log Analysis Process

1. Load log file: $1
2. Parse log entries
3. Filter based on options
4. Generate summary report

## Analysis Patterns

### Error Extraction
- Identify ERROR and FATAL messages
- Extract stack traces
- Group by error type
- Count occurrences

### Performance Analysis
- Extract slow query logs
- Identify request duration outliers
- Analyze memory usage patterns
- Detect performance bottlenecks

### Security Analysis
- Detect failed login attempts
- Identify suspicious IP addresses
- Check for authentication failures
- Monitor authorization issues

## Report Generation

Generate HTML report with:
- Error summary with counts
- Timeline of events
- Top error patterns
- Recommendations
````

### Health Check Command

```markdown
---
description: Perform comprehensive system health check
argument-hint: [--deep] [--service-specific]
allowed-tools: Bash, WebFetch, Read
---

# System Health Check

Options: $1

## Health Checks

### Basic Health (default)

- Application status: !`curl -f http://localhost:3000/health`
- Database connectivity
- Redis connection
- External API endpoints

### Deep Health (--deep)

- Resource usage (CPU, memory, disk)
- Database performance metrics
- Response time distribution
- Error rate analysis

### Service-Specific (--service-specific)

- Custom service health endpoints
- Business metric validation
- SLA compliance check

## Health Check Results

Generate report with:

- Overall system status (UP/DOWN)
- Individual service statuses
- Response times
- Error rates
- Resource utilization
- Recommendations

## Alerting

- Critical alerts for DOWN services
- Warnings for degraded performance
- Notifications for threshold breaches
```

## 5. Testing Commands

### E2E Test Runner

```markdown
---
description: Run end-to-end tests with specific scenarios
argument-hint: [test-suite] [--headless] [--record]
allowed-tools: Bash, Write, Read
---

# E2E Test Runner

Test Suite: $1
Options: $2

## Test Execution

1. Start test environment
2. Run database migrations
3. Seed test data
4. Execute test scenarios
5. Generate reports

## Test Scenarios

### User Journey Tests

- Registration flow
- Login/logout
- Main user workflows
- Error scenarios

### API Integration Tests

- CRUD operations
- Authentication flows
- Rate limiting
- Error handling

### Performance Tests

- Load testing
- Stress testing
- Concurrent users
- Response times

## Report Generation

- Test results summary
- Screenshots on failure
- Performance metrics
- Coverage reports
```

## Best Practices for Complex Commands

1. **Modular Design**: Break complex commands into logical sections
2. **Error Handling**: Include rollback procedures and error recovery
3. **Logging**: Add comprehensive logging for debugging
4. **Validation**: Validate inputs before processing
5. **Progress Indicators**: Show progress for long-running operations
6. **Atomic Operations**: Ensure operations can be rolled back
7. **Security**: Validate permissions and sanitize inputs
8. **Documentation**: Include inline documentation for complex logic
