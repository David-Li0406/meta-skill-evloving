---
name: nfr-assess
description: Use to assess non-functional requirements (security, performance, reliability, maintainability) through E2E integration testing patterns.
version: 1.0.0
---
<!-- Powered by PRISMâ„¢ System -->

# nfr-assess

E2E integration-focused NFR validation targeting the core four: security, performance, reliability, maintainability through real system testing.

## When to Use

- During QA gate review for story validation
- When assessing non-functional requirements
- When evaluating security, performance, reliability, or maintainability
- Before story completion to verify NFR compliance

## Quick Start

1. Provide story ID (e.g., "1.3")
2. Select NFRs to assess (default: security, performance, reliability, maintainability)
3. Run E2E integration tests for each selected NFR
4. Generate YAML block for gate file's `nfr_validation` section
5. Save markdown assessment to assessments folder

## Inputs

```yaml
required:
  - story_id: '{epic}.{story}' # e.g., "1.3"
  - story_path: `../core-config.yaml` for the `devStoryLocation`

optional:
  - architecture_refs: `../core-config.yaml` for the `architecture.architectureFile`
  - technical_preferences: `../core-config.yaml` for the `technicalPreferences`
  - acceptance_criteria: From story file
```

## Purpose

Assess non-functional requirements through E2E integration testing patterns and generate:

1. YAML block for the gate file's `nfr_validation` section with integration test evidence
2. Brief markdown assessment emphasizing real system validation saved to `qa.qaLocation/assessments/{epic}.{story}-nfr-{YYYYMMDD}.md`

## Process

### 0. Fail-safe for Missing Inputs

If story_path or story file can't be found:

- Still create assessment file with note: "Source story not found"
- Set all selected NFRs to CONCERNS with notes: "Target unknown / evidence missing"
- Continue with assessment to provide value

### 1. Elicit Scope

**Interactive mode:** Ask which NFRs to assess
**Non-interactive mode:** Default to core four (security, performance, reliability, maintainability)

```text
Which NFRs should I assess? (Enter numbers or press Enter for default)
[1] Security (default)
[2] Performance (default)
[3] Reliability (default)
[4] Maintainability (default)
[5] Usability
[6] Compatibility
[7] Portability
[8] Functional Suitability

> [Enter for 1-4]
```

### 2. Check for Thresholds

Look for NFR requirements in:

- Story acceptance criteria
- `docs/architecture/*.md` files
- `docs/technical-preferences.md`

**Interactive mode:** Ask for missing thresholds
**Non-interactive mode:** Mark as CONCERNS with "Target unknown"

```text
No performance requirements found. What's your target response time?
> 200ms for API calls

No security requirements found. Required auth method?
> JWT with refresh tokens
```

**Unknown targets policy:** If a target is missing and not provided, mark status as CONCERNS with notes: "Target unknown"

### 3. E2E Integration Assessment

For each selected NFR, prioritize integration test evidence:

- Are there integration tests validating the NFR?
- Can we measure it through real API calls?
- Is multi-tenant isolation properly tested?
- Are authentication/authorization flows validated end-to-end?

### 4. Generate Outputs

## Output 1: Gate YAML Block

Generate ONLY for NFRs actually assessed (no placeholders):

```yaml
# Gate YAML (copy/paste):
nfr_validation:
  _assessed: [security, performance, reliability, maintainability]
  security:
    status: CONCERNS
    notes: 'Auth endpoints tested but no rate limiting integration tests'
  performance:
    status: PASS
    notes: 'API response times < 200ms verified via integration tests with real DB'
  reliability:
    status: PASS
    notes: 'Health check endpoints and DB failover tested via containers'
  maintainability:
    status: CONCERNS
    notes: 'Integration test coverage at 65%, missing multi-tenant isolation tests'
```

## Deterministic Status Rules

- **FAIL**: Any selected NFR has critical gap or target clearly not met
- **CONCERNS**: No FAILs, but any NFR is unknown/partial/missing evidence
- **PASS**: All selected NFRs meet targets with evidence

## Quality Score Calculation

```
quality_score = 100
- 20 for each FAIL attribute
- 10 for each CONCERNS attribute
Floor at 0, ceiling at 100
```

If `technical-preferences.md` defines custom weights, use those instead.

## Output 2: Brief Assessment Report

**ALWAYS save to:** `qa.qaLocation/assessments/{epic}.{story}-nfr-{YYYYMMDD}.md`

```markdown
# NFR Assessment: {epic}.{story}

Date: {date}
Reviewer: Quinn

<!-- Note: Source story not found (if applicable) -->

## Summary

- Security: CONCERNS - Auth flows tested but missing rate limiting E2E tests
- Performance: PASS - <200ms verified via integration tests with real containers
- Reliability: PASS - Health checks and failover validated in test environment
- Maintainability: CONCERNS - Integration test coverage below target

## Critical Issues

1. **Missing rate limiting integration tests** (Security)
   - Risk: Auth endpoints vulnerable to brute force without E2E validation
   - Fix: Add integration tests that verify rate limiting behavior

2. **Insufficient multi-tenant isolation testing** (Maintainability)
   - Risk: Cross-tenant data leakage not validated
   - Fix: Add E2E tests that verify tenant isolation at API level

## Quick Wins

- Add rate limiting integration tests: ~3 hours
- Add multi-tenant isolation E2E tests: ~4 hours
- Add performance monitoring to existing integration tests: ~1 hour
```

## Output 3: Story Update Line

**End with this line for the review task to quote:**

```
NFR assessment: qa.qaLocation/assessments/{epic}.{story}-nfr-{YYYYMMDD}.md
```

## Output 4: Gate Integration Line

**Always print at the end:**

```
Gate NFR block ready â†’ paste into qa.qaLocation/gates/{epic}.{story}-{slug}.yml under nfr_validation
```

## Assessment Criteria

### Security

**PASS if:**

- Authentication/authorization E2E tested with real tokens
- Multi-tenant isolation validated via integration tests
- Input validation tested through API calls
- Secret management validated in containerized environment

**CONCERNS if:**

- Auth flows tested but missing rate limiting E2E tests
- Token validation tested but missing security headers validation
- Basic auth tested but missing authorization boundary tests

**FAIL if:**

- No authentication integration tests
- Multi-tenant data leakage in E2E tests
- Security vulnerabilities reproducible via integration tests

### Performance

**PASS if:**

- Response time targets verified via integration tests with real DB
- Performance measured through E2E API calls under load
- Database performance validated with real queries in containers
- Memory/CPU usage acceptable in integration test environment

**CONCERNS if:**

- Performance close to limits in integration tests
- Missing performance validation in multi-tenant scenarios
- No load testing of API endpoints

**FAIL if:**

- Response times exceed targets in integration tests
- Memory leaks detected in containerized test runs
- Database queries timeout in E2E tests

### Reliability

**PASS if:**

- Health check endpoints return correct status in integration tests
- Error handling validated through E2E failure scenarios
- Database failover/recovery tested in containerized environment
- Service resilience validated through integration tests

**CONCERNS if:**

- Health checks present but not comprehensively tested
- Some error scenarios not covered in E2E tests
- Database connection handling not fully validated

**FAIL if:**

- Health check endpoints fail in integration tests
- System crashes during E2E error simulation
- Database failures cause unrecoverable states in tests

### Maintainability

**PASS if:**

- Integration test coverage meets target (focus on E2E scenarios)
- Multi-tenant isolation properly tested
- API contract tests validate breaking changes
- Test environment closely mirrors production

**CONCERNS if:**

- Integration test coverage below target
- Missing multi-tenant test scenarios
- Some API endpoints not covered by E2E tests

**FAIL if:**

- No integration tests for critical paths
- Multi-tenant scenarios completely untested
- Test environment significantly different from production

## Quick Reference

### What to Check

```yaml
security:
  - Auth/authz E2E test coverage
  - Multi-tenant isolation tests
  - Token validation in real scenarios
  - Security headers validation
  - Rate limiting integration tests

performance:
  - API response time integration tests
  - Database performance with real queries
  - Load testing of endpoints
  - Container resource usage
  - Multi-tenant performance isolation

reliability:
  - Health check endpoint tests
  - Error handling E2E scenarios
  - Database failover tests
  - Service recovery tests
  - Container restart resilience

maintainability:
  - Integration test coverage %
  - Multi-tenant test scenarios
  - API contract test coverage
  - Test environment fidelity
  - E2E test maintenance burden
```

## Key Principles

- **E2E Integration First**: Prioritize NFR validation through real system testing over theoretical analysis
- **Container-based Validation**: Leverage containerized test environments that mirror production
- **Multi-tenant Focus**: Ensure NFR validation includes tenant isolation scenarios
- **API-level Testing**: Validate NFRs through actual HTTP calls, not mocked interfaces
- **Real Database Performance**: Use actual database queries and connections in performance validation
- **Gate-ready Evidence**: Provide concrete test evidence for gate decisions
- **Measurable Outcomes**: Focus on NFRs that can be measured through E2E tests

---

## E2E NFR Testing Patterns

### Security Testing Patterns

```csharp
// Authentication/Authorization E2E Tests
[Fact]
public async Task Endpoint_WithoutAuthentication_ShouldReturnUnauthorized()
{
    var client = application.GetHttpClient();
    client.DefaultRequestHeaders.Authorization = null;
    
    var response = await client.GetAsync("/api/protected-endpoint");
    
    response.StatusCode.ShouldBe(HttpStatusCode.Unauthorized);
}

// Multi-tenant Isolation Tests
[Fact]
public async Task Endpoint_ShouldNotLeakDataBetweenTenants()
{
    var client = application.GetHttpClient();
    var tenant1Data = await CreateTenantSpecificData(tenant1Id);
    var tenant2Token = await GetTenantToken(tenant2Id);
    
    client.DefaultRequestHeaders.Authorization = 
        new AuthenticationHeaderValue("Bearer", tenant2Token);
    var response = await client.GetAsync($"/api/tenant-data/{tenant1Data.Id}");
    
    response.StatusCode.ShouldBe(HttpStatusCode.Forbidden);
}
```

### Performance Testing Patterns

```csharp
// API Response Time Validation
[Fact]
public async Task Endpoint_ShouldMeetPerformanceTarget()
{
    var client = application.GetHttpClient();
    // Warm-up request to eliminate cold-start effects
    await client.GetAsync("/api/endpoint");
    
    var stopwatch = Stopwatch.StartNew();
    var response = await client.GetAsync("/api/endpoint");
    stopwatch.Stop();
    
    response.StatusCode.ShouldBe(HttpStatusCode.OK);
    stopwatch.ElapsedMilliseconds.ShouldBeLessThan(200);
}

// Database Performance with Real Queries
[Fact]
public async Task DatabaseQuery_ShouldPerformWithinLimits()
{
    var dbContext = await application.GetRequiredService<TenantDbContext>();
    
    var stopwatch = Stopwatch.StartNew();
    var results = await dbContext.LargeTable
        .Where(x => x.IndexedField == "value")
        .ToListAsync();
    stopwatch.Stop();
    
    stopwatch.ElapsedMilliseconds.ShouldBeLessThan(100);
}
```

### Reliability Testing Patterns

```csharp
// Health Check Validation
[Fact]
public async Task HealthCheck_ShouldReportCorrectStatus()
{
    var client = application.GetHttpClient();
    var response = await client.GetAsync("/health/tenant-id");
    
    response.StatusCode.ShouldBe(HttpStatusCode.OK);
    var content = await response.Content.ReadAsStringAsync();
    content.ShouldContain("Healthy");
}

// Database Connection Resilience
[Fact]
public async Task Service_ShouldHandleDatabaseFailure()
{
    var resolver = await application.GetRequiredService<IDbContextResolver>();
    var connected = await resolver.ConnectToTenant(tenantId);
    
    connected.ShouldBeTrue();
    // Simulate DB connection issues and verify graceful handling
}
```

### Container-based Testing Setup

```csharp
// TestContainers for Real Database Integration
public class DatabaseFixture : IAsyncLifetime
{
    private readonly MsSqlContainer container = new MsSqlBuilder().Build();
    
    public string ConnectionString => container.GetConnectionString();
    
    public Task InitializeAsync() => container.StartAsync();
    public Task DisposeAsync() => container.DisposeAsync().AsTask();
}

// Application Factory with Real Dependencies
public class TestApplicationFactory : WebApplicationFactory<Program>
{
    private readonly DatabaseFixture databaseFixture;
    
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureTestServices(services =>
        {
            // Use real database connection from TestContainer
            services.AddDbContext<TenantDbContext>(options =>
                options.UseSqlServer(databaseFixture.ConnectionString));
        });
    }
}
```

---

## Appendix: ISO 25010 Reference

<details>
<summary>Full ISO 25010 Quality Model (click to expand)</summary>

### All 8 Quality Characteristics

1. **Functional Suitability**: Completeness, correctness, appropriateness
2. **Performance Efficiency**: Time behavior, resource use, capacity
3. **Compatibility**: Co-existence, interoperability
4. **Usability**: Learnability, operability, accessibility
5. **Reliability**: Maturity, availability, fault tolerance
6. **Security**: Confidentiality, integrity, authenticity
7. **Maintainability**: Modularity, reusability, testability
8. **Portability**: Adaptability, installability

Use these when assessing beyond the core four.

</details>

<details>
<summary>Example: E2E Performance Validation (click to expand)</summary>

```yaml
performance_integration_testing:
  api_response_times:
    endpoint_auth: 45ms (target: <100ms)
    endpoint_tenant_data: 180ms (target: <200ms)
    endpoint_health_check: 25ms (target: <50ms)
  database_performance:
    tenant_connection_time: 15ms
    query_large_table: 85ms (with proper indexes)
    multi_tenant_isolation_overhead: 5ms
  container_performance:
    memory_usage: 245MB (target: <500MB)
    cpu_usage: 15% (target: <50%)
    startup_time: 3.2s (target: <5s)
  load_testing_results:
    concurrent_users: 50 (passed)
    max_throughput: 150 rps
    error_rate_under_load: 0.1%
```

</details>

