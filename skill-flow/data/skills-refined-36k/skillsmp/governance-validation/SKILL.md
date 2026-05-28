---
name: governance-validation
description: Validate governance constraints, CALM compliance, and architecture boundaries using spec-guard, flow-lint, and CALM validation. Use when checking if changes comply with SEA™ governance rules, enforcing invariants, or verifying architecture-as-code constraints before submitting PRs or generating code.
---

# Governance Validation Skill

Ensures proposed changes comply with SEA™ governance rules.

## Validation Checks

### 1. Spec Validation
```bash
just spec-guard
```
Validates all specification files:
- SDS YAML schema compliance
- SEA-DSL syntax validation
- Cross-reference integrity

### 2. Flow Lint
```bash
just flow-lint
```
Enforces CQRS annotation requirements on all Flows.

### 3. CALM Architecture
```bash
calm validate
```
Validates architecture definitions against CALM spec.

## Invariants Enforced

| ID | Invariant | Enforcement |
|----|-----------|-------------|
| INV-GOV-001 | Agents cannot self-approve privileged actions | SoD gate in CI |
| INV-GOV-002 | Breaking changes require R-AG approval | PR approval workflow |
| INV-GOV-003 | All privileged actions logged to audit trail | Audit event emission |

## When to Use

- Before submitting a PR with spec changes
- After generating code from specs
- During semantic debt review
- When changing governance policies

## Outputs

- Pass/fail status with specific violations
- Invariant IDs for failed checks
- Remediation suggestions

## Related Specs

- SDS-031: Authority & Ownership Boundaries
- SDS-035: Governance Invariants
- SDS-020: CI Semantic Gates
