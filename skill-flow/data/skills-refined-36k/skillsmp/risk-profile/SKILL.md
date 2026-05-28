---
name: risk-profile
version: 1.0.0
description: Use to assess and document risk factors for stories or features. Creates risk profiles with mitigation strategies.
---
<!-- Powered by PRISMâ„¢ Core -->

# risk-profile

Generate a comprehensive risk assessment matrix for a story implementation using probability × impact analysis.

## When to Use

- During story planning to identify potential risks
- When assessing story complexity before estimation
- When creating mitigation strategies for high-risk features
- As part of comprehensive story review

## Quick Start

1. Provide story ID and path
2. Identify risks across categories (TECH, SEC, PERF, DATA, BUS, OPS)
3. Rate each risk by probability and impact
4. Generate risk matrix with mitigation strategies
5. Document testing focus areas based on risk levels

## Inputs

```yaml
required:
  - story_id: '{epic}.{story}' # e.g., "1.3"
  - story_path: 'docs/stories/{epic}.{story}.*.md'
  - story_title: '{title}' # If missing, derive from story file H1
  - story_slug: '{slug}' # If missing, derive from title (lowercase, hyphenated)
```

## Purpose

Identify, assess, and prioritize risks in the story implementation. Provide risk mitigation strategies and testing focus areas based on risk levels.

## Risk Assessment Framework

### Risk Categories

**Category Prefixes:**

- `TECH`: Technical Risks
- `SEC`: Security Risks
- `PERF`: Performance Risks
- `DATA`: Data Risks
- `BUS`: Business Risks
- `OPS`: Operational Risks

**Priority Focus: E2E Integration-Testable Risks**

E2E integration tests provide the most effective risk mitigation for cross-system, multi-component, and real-world scenario risks. Prioritize risks that can be validated through complete user workflows and system interactions.

1. **Security Risks (SEC)** - *Critical Priority for E2E Testing*
   - **Authentication/authorization flaws** - Cross-service auth validation
   - **Multi-tenant data isolation breaches** - Tenant boundary enforcement
   - **API endpoint security vulnerabilities** - End-to-end request validation
   - **Session management across services** - Complete user session lifecycle
   - **Cross-tenant data leakage** - Data access boundary verification
   - **Service-to-service authentication failures** - Inter-service security
   - **Token validation and refresh cycles** - Complete auth workflows

2. **Data Risks (DATA)** - *High Priority for E2E Testing*
   - **Multi-tenant data isolation failures** - Critical tenant separation
   - **Cross-service data consistency issues** - Transaction boundaries
   - **Database connection pool exhaustion** - Multi-tenant load scenarios
   - **Data corruption during service integration** - End-to-end data integrity
   - **Backup/recovery in multi-tenant environments** - Tenant-specific recovery
   - **Data migration integrity across tenants** - Complete migration workflows

3. **Technical Risks (TECH)** - *High Priority for E2E Testing*
   - **Service integration failures** - Cross-service communication
   - **Container orchestration dependencies** - Infrastructure reliability
   - **Database connection management** - Multi-tenant connection handling
   - **API gateway and routing failures** - Request routing accuracy
   - **Service mesh communication breakdown** - Inter-service networking
   - **Configuration management across environments** - Environment parity
   - **Third-party service integration points** - External dependency reliability

4. **Operational Risks (OPS)** - *Medium Priority for E2E Testing*
   - **Deployment failures in containerized environments** - Complete deployment cycles
   - **Health check cascading failures** - System-wide health validation
   - **Multi-tenant monitoring blind spots** - Tenant-specific observability
   - **Service discovery and load balancing** - Traffic distribution accuracy
   - **Container resource allocation failures** - Resource management validation
   - **Backup and disaster recovery procedures** - Complete recovery workflows

5. **Performance Risks (PERF)** - *Medium Priority for E2E Testing*
   - **Cross-service response time cascading** - End-to-end latency
   - **Multi-tenant resource contention** - Tenant isolation performance
   - **Database connection pool bottlenecks** - Connection management under load
   - **API rate limiting effectiveness** - Traffic management validation
   - **Container resource scaling** - Auto-scaling behavior validation

6. **Business Risks (BUS)** - *Low Priority for E2E Testing*
   - **Complete user workflow failures** - Business process validation
   - **Feature integration breaking existing workflows** - Regression detection
   - **Multi-tenant feature availability** - Tenant-specific feature access
   - **Service degradation impact on user experience** - Business continuity

## Risk Analysis Process

### 1. Risk Identification

For each category, identify specific risks with E2E testing focus:

```yaml
risk:
  id: 'SEC-001' # Use prefixes: SEC, PERF, DATA, BUS, OPS, TECH
  category: security
  title: 'Multi-tenant authentication boundary violation'
  description: 'Cross-tenant access possible through compromised auth tokens or session hijacking'
  affected_components:
    - 'Authentication Service'
    - 'API Gateway'
    - 'Tenant Context Resolution'
  detection_method: 'E2E testing with multi-tenant scenarios'
  e2e_testable: true
  integration_scope: 'cross-service'
```

**E2E Integration Testing Priority Examples:**

```yaml
# Critical E2E Risks
risk:
  id: 'DATA-001'
  title: 'Cross-tenant data leakage through shared services'
  e2e_validation: 'Complete tenant isolation workflows'
  test_scenarios:
    - 'Tenant A cannot access Tenant B data through any API endpoint'
    - 'Database connections properly isolated by tenant context'
    - 'Shared services maintain tenant boundaries'

risk:
  id: 'SEC-002'
  title: 'API endpoint authentication bypass'
  e2e_validation: 'End-to-end authentication workflows'
  test_scenarios:
    - 'Expired tokens properly rejected across all services'
    - 'Service-to-service auth maintained throughout request chain'
    - 'Token refresh cycles work across integrated services'

risk:
  id: 'TECH-001'
  title: 'Container orchestration dependency failure'
  e2e_validation: 'Full deployment and runtime scenarios'
  test_scenarios:
    - 'Service mesh communication under container restarts'
    - 'Database connections survive container scaling events'
    - 'Load balancing maintains service availability'
```

### 2. Risk Assessment

Evaluate each risk using probability Ã— impact:

**Probability Levels:**

- `High (3)`: Likely to occur (>70% chance)
- `Medium (2)`: Possible occurrence (30-70% chance)
- `Low (1)`: Unlikely to occur (<30% chance)

**Impact Levels:**

- `High (3)`: Severe consequences (data breach, system down, major financial loss)
- `Medium (2)`: Moderate consequences (degraded performance, minor data issues)
- `Low (1)`: Minor consequences (cosmetic issues, slight inconvenience)

### Risk Score = Probability Ã— Impact

- 9: Critical Risk (Red)
- 6: High Risk (Orange)
- 4: Medium Risk (Yellow)
- 2-3: Low Risk (Green)
- 1: Minimal Risk (Blue)

### 3. Risk Prioritization

Create risk matrix:

```markdown
## Risk Matrix

| Risk ID  | Description             | Probability | Impact     | Score | Priority |
| -------- | ----------------------- | ----------- | ---------- | ----- | -------- |
| SEC-001  | XSS vulnerability       | High (3)    | High (3)   | 9     | Critical |
| PERF-001 | Slow query on dashboard | Medium (2)  | Medium (2) | 4     | Medium   |
| DATA-001 | Backup failure          | Low (1)     | High (3)   | 3     | Low      |
```

### 4. Risk Mitigation Strategies

**E2E Integration Testing as Primary Mitigation**

For integration-testable risks, E2E tests provide the most comprehensive mitigation:

```yaml
mitigation:
  risk_id: 'SEC-001'
  strategy: 'preventive' # preventive|detective|corrective
  primary_mitigation: 'E2E Integration Testing'
  actions:
    - 'Implement comprehensive multi-tenant E2E test suites'
    - 'Add tenant boundary validation in all API endpoints'
    - 'Create cross-service authentication test scenarios'
    - 'Implement tenant context isolation verification'
  testing_requirements:
    - 'E2E multi-tenant isolation tests (CRITICAL)'
    - 'Cross-service authentication flow validation'
    - 'API endpoint security boundary testing'
    - 'Database connection tenant isolation verification'
    - 'Container orchestration failure recovery testing'
  e2e_coverage:
    - 'Complete tenant lifecycle workflows'
    - 'Authentication/authorization across all services'
    - 'Data isolation under various load conditions'
    - 'Service-to-service communication security'
  residual_risk: 'Low - E2E tests validate complete system behavior'
  owner: 'qa'
  timeline: 'Continuous - with every integration'
```

**E2E Testing Mitigation Priorities:**

1. **Critical Risks (Score 9)** - Must have comprehensive E2E coverage
   - Multi-tenant data isolation
   - Authentication/authorization flows
   - Service integration security
   - Container infrastructure dependencies

2. **High Risks (Score 6)** - Require targeted E2E scenarios
   - API endpoint security
   - Database connection management
   - Service mesh communication
   - Configuration management

3. **Medium/Low Risks** - Can use selective E2E validation
   - Performance degradation patterns
   - Monitoring and alerting effectiveness
   - Business workflow integrity

## Outputs

### Output 1: Gate YAML Block

Generate for pasting into gate file under `risk_summary`:

**Output rules:**

- Only include assessed risks; do not emit placeholders
- Sort risks by score (desc) when emitting highest and any tabular lists
- If no risks: totals all zeros, omit highest, keep recommendations arrays empty

```yaml
# risk_summary (paste into gate file):
risk_summary:
  totals:
    critical: X # score 9
    high: Y # score 6
    medium: Z # score 4
    low: W # score 2-3
  highest:
    id: SEC-001
    score: 9
    title: 'XSS on profile form'
  recommendations:
    must_fix:
      - 'Add input sanitization & CSP'
    monitor:
      - 'Add security alerts for auth endpoints'
```

### Output 2: Markdown Report

**Save to:** `qa.qaLocation/assessments/{epic}.{story}-risk-{YYYYMMDD}.md`

```markdown
# Risk Profile: Story {epic}.{story}

Date: {date}
Reviewer: Quinn (Test Architect)

## Executive Summary

- Total Risks Identified: X
- Critical Risks: Y
- High Risks: Z
- Risk Score: XX/100 (calculated)

## Critical Risks Requiring Immediate Attention

### 1. [ID]: Risk Title

**Score: 9 (Critical)**
**Probability**: High - Detailed reasoning
**Impact**: High - Potential consequences
**Mitigation**:

- Immediate action required
- Specific steps to take
  **Testing Focus**: Specific test scenarios needed

## Risk Distribution

### By Category

- Security: X risks (Y critical)
- Performance: X risks (Y critical)
- Data: X risks (Y critical)
- Business: X risks (Y critical)
- Operational: X risks (Y critical)

### By Component

- Frontend: X risks
- Backend: X risks
- Database: X risks
- Infrastructure: X risks

## Detailed Risk Register

[Full table of all risks with scores and mitigations]

## E2E Integration Risk-Based Testing Strategy

### Priority 1: Critical E2E Integration Tests

**Multi-Tenant Security & Data Isolation**
- Complete tenant lifecycle E2E scenarios (create, migrate, delete)
- Cross-tenant data access prevention validation
- Authentication/authorization boundary enforcement
- Service-to-service security under tenant context

**Container & Service Integration**
- Full deployment cycle with service dependencies
- Container orchestration failure and recovery
- Database connection management across scaling events
- Service mesh communication reliability

**Test Environment Requirements:**
- Multi-tenant test data isolation
- Container orchestration test infrastructure
- Service mesh configuration validation
- Database per-tenant provisioning

### Priority 2: High Risk E2E Integration Tests

**API Security & Service Communication**
- End-to-end API authentication flows
- Cross-service token validation and refresh
- API gateway routing and security enforcement
- Service discovery and load balancing validation

**Data Consistency & Transaction Management**
- Cross-service transaction integrity
- Database connection pool behavior under load
- Data migration workflows across tenant boundaries
- Backup/recovery procedures in multi-tenant environment

### Priority 3: Medium/Low Risk E2E Integration Tests

**Performance & Monitoring Integration**
- End-to-end response time monitoring
- Cross-service performance impact analysis
- Health check cascading validation
- Business workflow performance under load

**Operational Workflow Integration**
- Complete deployment and rollback procedures
- Monitoring and alerting integration validation
- Configuration management across environments
- Disaster recovery workflow testing

### E2E Test Coverage Metrics

**Critical Success Criteria:**
- 100% tenant isolation validation coverage
- 100% authentication/authorization flow coverage
- 100% service integration failure scenario coverage
- 95% container infrastructure dependency coverage

**Integration Test Types by Risk Category:**
- **SEC Risks**: Cross-service security validation, tenant boundary testing
- **DATA Risks**: Multi-tenant data isolation, cross-service consistency
- **TECH Risks**: Service integration, container orchestration, API gateway
- **OPS Risks**: Deployment workflows, monitoring integration, disaster recovery

## Risk Acceptance Criteria

### Must Fix Before Production

- All critical risks (score 9)
- High risks affecting security/data

### Can Deploy with Mitigation

- Medium risks with compensating controls
- Low risks with monitoring in place

### Accepted Risks

- Document any risks team accepts
- Include sign-off from appropriate authority

## Monitoring Requirements

Post-deployment monitoring for:

- Performance metrics for PERF risks
- Security alerts for SEC risks
- Error rates for operational risks
- Business KPIs for business risks

## Risk Review Triggers

Review and update risk profile when:

- Architecture changes significantly
- New integrations added
- Security vulnerabilities discovered
- Performance issues reported
- Regulatory requirements change
```

## Risk Scoring Algorithm

Calculate overall story risk score:

```text
Base Score = 100
For each risk:
  - Critical (9): Deduct 20 points
  - High (6): Deduct 10 points
  - Medium (4): Deduct 5 points
  - Low (2-3): Deduct 2 points

Minimum score = 0 (extremely risky)
Maximum score = 100 (minimal risk)
```

## E2E Integration Risk-Based Recommendations

Based on risk profile with E2E integration testing focus:

1. **E2E Testing Priority**
   - **Critical Path**: Multi-tenant isolation and authentication flows first
   - **Service Integration**: Cross-service communication and container orchestration
   - **Data Integrity**: Database isolation and transaction consistency
   - **Security Boundaries**: API endpoint protection and tenant context enforcement

2. **Integration Development Focus**
   - **Multi-Tenant Architecture**: Tenant context propagation across services
   - **Service Mesh Security**: Inter-service authentication and authorization
   - **Container Dependencies**: Infrastructure reliability and scaling behavior  
   - **API Gateway Configuration**: Request routing and security enforcement

3. **Deployment Strategy for Integration Risks**
   - **Phased Multi-Tenant Rollout**: Validate tenant isolation at each phase
   - **Service-by-Service Deployment**: Maintain integration integrity
   - **Container Blue-Green Deployment**: Ensure zero-downtime service availability
   - **Database Migration Validation**: Verify tenant data integrity during updates

4. **Integration Monitoring Setup**
   - **Cross-Service Metrics**: Request tracing, authentication success rates
   - **Tenant Isolation Alerts**: Cross-tenant access attempts, data leakage
   - **Container Health Dashboards**: Service availability, resource utilization
   - **Database Connection Monitoring**: Per-tenant connection health, isolation metrics

5. **E2E Test Environment Requirements**
   - **Multi-Tenant Test Infrastructure**: Isolated tenant environments
   - **Service Mesh Test Configuration**: Container orchestration platform
   - **Database Per-Tenant Setup**: Complete data isolation validation
   - **Authentication Service Integration**: Full identity provider connectivity

## Integration with Quality Gates

**Deterministic gate mapping:**

- Any risk with score â‰¥ 9 â†’ Gate = FAIL (unless waived)
- Else if any score â‰¥ 6 â†’ Gate = CONCERNS
- Else â†’ Gate = PASS
- Unmitigated risks â†’ Document in gate

### Output 3: Story Hook Line

**Print this line for review task to quote:**

```text
Risk profile: qa.qaLocation/assessments/{epic}.{story}-risk-{YYYYMMDD}.md
```

## Key Principles

**E2E Integration Risk Assessment Focus:**

- **Prioritize Integration-Testable Risks**: Focus on risks best validated through complete system workflows
- **Multi-Tenant Security First**: Tenant isolation and cross-tenant security as highest priority
- **Service Integration Validation**: Cross-service communication and dependency risks as critical
- **Container Infrastructure Dependencies**: Infrastructure reliability risks require E2E validation
- **Authentication/Authorization Flows**: Complete auth workflows across all service boundaries
- **Database Multi-Tenancy**: Data isolation and connection management under realistic load
- **API Gateway Security**: End-to-end request routing and security enforcement validation

**Risk Assessment Process:**
- Identify risks early with E2E testing capability in mind
- Use consistent probability Ã— impact scoring with integration complexity weighting
- Provide E2E test-focused mitigation strategies as primary approach
- Link risks to specific E2E integration test scenarios and coverage requirements
- Track residual risk after comprehensive E2E integration testing
- Update risk profile as system integration complexity evolves

**E2E Testing as Risk Mitigation:**
- E2E integration tests provide highest confidence for cross-system risks
- Multi-tenant scenarios validate most critical security and data isolation risks  
- Service integration testing catches risks that unit/component tests cannot detect
- Container orchestration testing validates infrastructure dependency risks
- Complete workflow testing ensures business continuity under failure conditions

