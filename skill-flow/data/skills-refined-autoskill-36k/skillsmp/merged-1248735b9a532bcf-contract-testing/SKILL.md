---
name: contract-testing
description: Use this skill for consumer-driven contract testing of APIs, including REST, GraphQL, and event-driven systems, with a focus on schema validation and backward compatibility.
---

# Contract Testing

<default_to_action>
When testing API contracts or microservices:
1. DEFINE consumer expectations (what consumers actually need).
2. VERIFY provider fulfills contracts (Pact verification).
3. DETECT breaking changes before deployment (CI/CD integration).
4. VERSION APIs semantically (breaking = major bump).
5. MAINTAIN backward compatibility for supported versions.

**Quick Contract Testing Steps:**
- Consumer: Define expected request/response pairs.
- Provider: Verify against all consumer contracts.
- CI/CD: Block deploys that break contracts.
- Versioning: Document supported versions and deprecation.

**Critical Success Factors:**
- Consumers own the contract (they define what they need).
- Provider must pass all consumer contracts before deploy.
- Breaking changes require coordination, not surprise.
</default_to_action>

## Quick Reference Card

### When to Use
- Microservices communication
- Third-party API integrations
- Distributed team coordination
- Preventing breaking changes

### Consumer-Driven Contract Flow
```
Consumer → Defines Expectations → Contract
                    ↓
Provider → Verifies Contract → Pass/Fail
                    ↓
CI/CD → Blocks Breaking Changes
```

### Breaking vs Non-Breaking Changes
| Change Type | Breaking? | Semver |
|-------------|-----------|--------|
| Remove field | ✅ Yes | Major |
| Rename field | ✅ Yes | Major |
| Change type | ✅ Yes | Major |
| Add optional field | ❌ No | Minor |
| Add new endpoint | ❌ No | Minor |
| Bug fix | ❌ No | Patch |

### Tools
| Tool | Best For |
|------|----------|
| **Pact** | Consumer-driven contracts |
| **OpenAPI/Swagger** | API-first design |
| **JSON Schema** | Schema validation |
| **GraphQL** | Schema-first contracts |

---

## Contract Testing Types

### 1. Consumer-Driven Contracts (Pact)

```typescript
await contractTester.consumerDriven({
  consumer: '<consumer_name>',
  provider: '<provider_name>',
  contracts: '<path_to_contract>',
  verification: {
    providerBaseUrl: '<provider_base_url>',
    providerStates: '<provider_state_handlers>',
    publishResults: true
  }
});
```

### 2. Schema Validation

```typescript
await contractTester.validateSchema({
  type: 'openapi',
  schema: '<path_to_schema>',
  requests: '<actual_requests>',
  validation: {
    requestBody: true,
    responseBody: true,
    headers: true,
    statusCodes: true
  }
});
```

### 3. GraphQL Contract Testing

```typescript
await graphqlTester.testContracts({
  schema: '<path_to_graphql_schema>',
  operations: '<path_to_operations>',
  validation: {
    queryValidity: true,
    responseShapes: true,
    nullability: true,
    deprecations: true
  }
});
```

### 4. Event Contract Testing

```typescript
await contractTester.eventContracts({
  schema: '<path_to_event_schemas>',
  events: {
    '<event_name>': {
      schema: '<event_schema>',
      examples: ['<example_path>']
    }
  },
  compatibility: 'backward'
});
```

## Breaking Change Detection

```yaml
breaking_changes:
  always_breaking:
    - endpoint_removed
    - required_param_added
    - response_field_removed
    - type_changed

  potentially_breaking:
    - optional_param_removed
    - response_field_added
    - enum_value_removed

  non_breaking:
    - endpoint_added
    - optional_param_added
    - response_field_made_optional
    - documentation_changed
```

## CI/CD Integration

```yaml
contract_verification:
  consumer_side:
    - generate_contracts
    - publish_to_broker
    - can_i_deploy_check

  provider_side:
    - fetch_contracts_from_broker
    - verify_against_provider
    - publish_results

  pre_release:
    - check_breaking_changes
    - verify_all_consumers
    - update_compatibility_matrix
```

## Agent Coordination Hints

### Memory Namespace
```
aqe/contract-testing/
├── contracts/*           - Current contracts
├── breaking-changes/*    - Detected breaking changes
├── versioning/*          - Version compatibility matrix
└── verification-results/* - Provider verification history
```

### Fleet Coordination
```typescript
const contractFleet = await FleetManager.coordinate({
  strategy: 'contract-testing',
  agents: [
    'qe-api-contract-validator',  // Validation, breaking detection
    'qe-test-generator',          // Generate contract tests
    'qe-security-scanner'         // API security
  ],
  topology: 'sequential'
});
```

## Related Skills
- [api-testing-patterns](../api-testing-patterns/) - API testing strategies
- [shift-left-testing](../shift-left-testing/) - Early contract validation
- [cicd-pipeline-qe-orchestrator](../cicd-pipeline-qe-orchestrator/) - Pipeline integration

---

## Remember

**Consumers own the contract.** They define what they need; providers must fulfill it. Breaking changes require major version bumps and coordination. CI/CD blocks deploys that break contracts. Use Pact for consumer-driven, OpenAPI for API-first.

**With Agents:** Agents validate contracts, detect breaking changes with semver recommendations, and generate migration guides. Use agents to maintain contract compliance at scale.