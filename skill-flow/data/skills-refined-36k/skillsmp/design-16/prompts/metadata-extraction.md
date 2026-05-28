# Metadata Extraction Prompt (Few-Shot)

You are analyzing a software specification to extract metadata for PRP generation.

## Examples

### Example 1: User Authentication Spec
**Spec excerpt:**
```
# User Authentication System
Build email-based signup and login for the web application.
- Users can create accounts with email/password
- Password reset via email link
- Session management with JWT tokens
```

**Extracted metadata:**
```json
{
  "project_name": "User Authentication System",
  "project_type": "user-feature",
  "domain": "consumer",
  "complexity": 5,
  "patterns": ["auth-flow", "error-handling", "config-loading"],
  "thinking_level": "Think",
  "timeline_hint": null,
  "tech_stack": ["JWT", "email"],
  "has_external_deps": false
}
```

### Example 2: Payment Gateway Integration
**Spec excerpt:**
```
# Stripe Payment Integration
Integrate Stripe as the primary payment processor.
- Payment intent creation via Stripe API
- Webhook handling for payment events
- PCI compliance requirements
```

**Extracted metadata:**
```json
{
  "project_name": "Stripe Payment Integration",
  "project_type": "api-integration",
  "domain": "integration",
  "complexity": 7,
  "patterns": ["api-client", "error-handling", "config-loading"],
  "thinking_level": "Think Hard",
  "timeline_hint": null,
  "tech_stack": ["Stripe API", "webhooks"],
  "has_external_deps": true
}
```

### Example 3: Database Migration
**Spec excerpt:**
```
# PostgreSQL to Aurora Migration
Migrate production database from self-hosted PostgreSQL to AWS Aurora.
- Zero-downtime migration strategy
- Data validation before/after
- Rollback procedures
```

**Extracted metadata:**
```json
{
  "project_name": "PostgreSQL to Aurora Migration",
  "project_type": "data-migration",
  "domain": "data-architecture",
  "complexity": 8,
  "patterns": ["database-patterns", "error-handling"],
  "thinking_level": "Ultrathink",
  "timeline_hint": null,
  "tech_stack": ["PostgreSQL", "Aurora", "AWS"],
  "has_external_deps": true
}
```

## Classification Rules

**project_type:**
- `user-feature`: UI/UX, consumer-facing, mobile/web app features
- `api-integration`: External APIs, webhooks, third-party services
- `data-migration`: Database changes, data pipelines, ETL
- `infrastructure`: DevOps, deployment, monitoring
- `base`: General/mixed

**domain:**
- `consumer`: End-user facing features
- `integration`: API/service integration
- `data-architecture`: Database, data pipelines
- `physical-construction`: Physical/hardware projects
- `universal`: No specific domain

**complexity (1-10):**
- 1-3: Simple, well-understood, single component
- 4-6: Moderate, multiple components, some unknowns
- 7-8: Complex, external dependencies, security concerns
- 9-10: Critical systems, data migrations, compliance requirements

**thinking_level:**
- `Normal`: complexity 1-3, well-understood patterns
- `Think`: complexity 4-5, multiple domains
- `Think Hard`: complexity 6-7, security/integration concerns
- `Ultrathink`: complexity 8+, critical systems, migrations

**patterns** (from examples library):
- `api-client`: External API calls
- `error-handling`: Error boundaries, recovery
- `database-patterns`: Data access, transactions
- `config-loading`: Environment, secrets
- `test-fixtures`: Test data, mocks

## Your Task

Analyze the following specification and extract metadata in JSON format.

**Spec:**
```
{{SPEC_CONTENT}}
```

**Output only valid JSON matching this schema:**
```json
{
  "project_name": "string",
  "project_type": "user-feature|api-integration|data-migration|infrastructure|base",
  "domain": "consumer|integration|data-architecture|physical-construction|universal",
  "complexity": 1-10,
  "patterns": ["array", "of", "patterns"],
  "thinking_level": "Normal|Think|Think Hard|Ultrathink",
  "timeline_hint": "string or null",
  "tech_stack": ["array", "of", "technologies"],
  "has_external_deps": true|false
}
```
