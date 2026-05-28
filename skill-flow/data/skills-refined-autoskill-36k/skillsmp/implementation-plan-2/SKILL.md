---
name: implementation-plan
description: Generate a deterministic execution-ready implementation plan with local dev and CI/CD. Use after stack-selection confirms the chosen stack.
---

# Implementation Plan Generator

Produce a deterministic, execution-ready implementation plan including local dev runbook and CI/CD setup. **This skill does not execute** – it only generates the plan.

## Prerequisites

- Selected stack from **stack-selection**
- Architecture brief from **architecture-refinement**

## Plan Phases

The implementation plan covers 10 mandatory phases:

1. **Foundation** - Accounts, environments, regions, DNS
2. **Networking & Security** - IAM, secrets, network boundaries
3. **Data Layer** - Database provisioning, backups, migrations
4. **Local Development** - Local orchestration, dependencies, parity
5. **CI/CD Pipeline** - Build, test, deploy automation
6. **Application Delivery** - Scaffolding, runtime config
7. **Observability** - Logging, metrics, tracing, alerting
8. **Cost Controls** - Budgets, guardrails, tagging
9. **Reliability** - DR strategy, failover, RTO/RPO
10. **Hardening** - Security hardening, runbooks

The following phases have dedicated standalone skills that can also be invoked directly:

- **local-dev-plan** - Phase 4: Generate local development environment plans
  - "Create a local dev setup for React + PostgreSQL"
- **cicd-plan** - Phase 5: Generate CI/CD pipeline configurations
  - "Create GitHub Actions workflow for my app"

## Output Contract

```yaml
implementation_plan:
  plan_id: "<unique id>"
  created_at: "<ISO timestamp>"
  stack_id: "<reference>"

  assumptions:
    - "<assumption>"

  phases:
    - phase: 1
      name: "Foundation"
      goals: []
      steps:
        - id: "1.1"
          name: "<step name>"
          description: "<description>"
          outputs: []

    - phase: 2
      name: "Networking & Security Baseline"
      goals: []
      steps: []

    - phase: 3
      name: "Data Layer Setup"
      goals: []
      steps: []

    - phase: 4
      name: "Local Development Environment"
      goals: []
      steps: []

    - phase: 5
      name: "CI/CD Pipeline"
      goals: []
      steps: []

    - phase: 6
      name: "Application Delivery"
      goals: []
      steps: []

    - phase: 7
      name: "Observability"
      goals: []
      steps: []

    - phase: 8
      name: "Cost Controls"
      goals: []
      steps: []

    - phase: 9
      name: "Reliability Posture"
      goals: []
      steps: []

    - phase: 10
      name: "Hardening Checklist"
      goals: []
      steps: []

  summary:
    total_phases: 10
    total_steps: <count>
    critical_decisions: []
    risks:
      - risk: "<risk>"
        mitigation: "<mitigation>"
```

## Phase 1: Foundation

**Goals**: Set up cloud accounts, define environments, configure access

**Steps**:
- 1.1 Create Cloud Accounts/Projects
- 1.2 Define Environment Model (dev/staging/prod)
- 1.3 Configure Regions
- 1.4 Set Up DNS

## Phase 2: Networking & Security

**Goals**: Implement least-privilege, secrets management, network security

**Steps**:
- 2.1 Design IAM Model
- 2.2 Configure Secrets Management
- 2.3 Define Network Boundaries
- 2.4 Apply Security Policies

## Phase 3: Data Layer

**Goals**: Provision database, configure backups, establish migrations

**Steps**:
- 3.1 Provision Database
- 3.2 Configure Backups
- 3.3 Set Up Migrations
- 3.4 Configure HA/Replication (if required)

## Phase 4: Local Development

Use the **local-dev-plan** skill for detailed planning (can be invoked directly).

**Goals**: Enable full local development, minimize time-to-first-run

**Key outputs**:
- Local orchestration setup (docker-compose/k8s/hybrid/aspire)
- Dependencies runbook
- Seeding & migrations workflow
- Local secrets strategy
- Prod parity documentation

### Offline Considerations (when required)

If offline requirement is `transient` or higher, include:

- **Offline Storage Strategy**:
  - Technology selection (IndexedDB, SQLite WASM, localStorage)
  - Data model for offline access
  - Storage limits and quota handling

- **Sync Strategy**:
  - Background sync implementation
  - Conflict resolution approach (last-write-wins, merge, CRDT)
  - Retry and backoff policies

- **Failure Modes**:
  - Network detection and status handling
  - Graceful degradation patterns
  - User feedback during offline/sync states

- **Testing Offline Scenarios**:
  - Offline mode simulation in local dev
  - Sync conflict test cases
  - Data integrity verification

## Phase 5: CI/CD Pipeline

Use the **cicd-plan** skill for detailed planning (can be invoked directly).

**Goals**: Automate build/test/deploy, enforce quality gates

**Key outputs**:
- Repository structure
- Branching strategy
- CI pipeline (build, test, lint, security scan)
- CD pipeline per environment
- Rollback procedures

## Phase 6: Application Delivery

**Goals**: Scaffold application, configure runtime

**Steps**:
- 6.1 Application Scaffolding
- 6.2 Runtime Configuration
- 6.3 Environment Variable Contract
- 6.4 Deployment Topology

## Phase 7: Observability

**Goals**: Centralized logging, metrics, tracing, alerting

**Steps**:
- 7.1 Logging Setup
- 7.2 Metrics Setup
- 7.3 Dashboards
- 7.4 Tracing Setup
- 7.5 Alerting

## Phase 8: Cost Controls

**Goals**: Budget visibility, guardrails, attribution

**Steps**:
- 8.1 Budget Alerts
- 8.2 Cost Guardrails
- 8.3 Tagging Strategy

## Phase 9: Reliability

**Goals**: Meet availability target, implement DR

**Steps**:
- 9.1 DR Strategy
- 9.2 Failover Configuration
- 9.3 RTO/RPO Validation

## Phase 10: Hardening

**Goals**: Security hardening, operational readiness

**Steps**:
- 10.1 Security Hardening Checklist
- 10.2 Operational Runbooks
- 10.3 Operational Readiness Review

## Next Step

This plan is ready for execution. Consider invoking **skill-improvement** at end of flow to capture learnings.
