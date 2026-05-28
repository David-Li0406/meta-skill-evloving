---
name: quality-assurance
description: Quality Assurance skill for planning, executing, and improving testing across functional and non-functional dimensions. Use when creating test strategies, writing test plans/cases, defining quality gates, coordinating test execution, or triaging defects.
---

# Quality Assurance

A comprehensive QA skill for building and running effective quality programs: strategy, planning, test design, execution, automation, non-functional coverage, and continuous improvement.

## Quick Start

1. Clarify scope, risks, and release criteria.
2. Map test strategy: levels (unit/integration/E2E), types (functional, security, performance, UX), environments, and data.
3. Define quality gates in CI/CD (lint, SAST, tests, coverage, scanning).
4. Plan execution: owners, schedule, entry/exit criteria.
5. Track defects and readiness with metrics; iterate on gaps.

## Core Capabilities

### 1) Strategy & Planning
- Define objectives, scope, and risk-based priorities.
- Choose test types and levels; align to environments and data needs.
- Establish entry/exit criteria, Definition of Ready/Done, and release gates.
- Map dependencies (services, test data, accounts, flags).

### 2) Test Design
- Create test plans and charters (positive/negative, edge cases).
- Derive cases from requirements, flows, and risk areas.
- Apply heuristics (CRUD, boundaries, state transitions, error paths).
- Specify expected results, data, and observability hooks.

### 3) Functional Coverage
- Unit coverage for critical logic; integration for contracts/IO; E2E for happy/critical paths.
- Regression suites per component and smoke tests per deploy.
- Data variation: boundaries, locales, timezones, permissions, offline/latency.

### 4) Non-Functional Coverage
- Performance: baselines, load/stress/soak, SLO/SLA validation.
- Security: authZ/authN, input validation, dependency and secret scanning.
- Reliability: retries, idempotency, backoff, timeouts, circuit breakers.
- Accessibility/UX: WCAG basics (labels, focus, color contrast, keyboard).

### 5) Automation & Tooling
- CI gates: lint, unit/integration/E2E, coverage thresholds, SAST/DAST/SCA, secret scanning.
- Flake management: quarantine, retry budget, stability tracking.
- Test data: fixtures, factories, seeds, synthetic vs production-like data.
- Reporting: dashboards for pass rate, coverage, defect trends, MTTR/MTRR.

### 6) Defect Lifecycle & Readiness
- Triage: severity/priority, repro steps, environment, logs/traces.
- Root cause: code, test gap, environment, data, process.
- Exit criteria: critical defects fixed/waived, key scenarios passed, gates green.
- Post-release monitoring: error budgets, alerts, rollback/feature flag plans.

### 7) Quality Maintenance & Documentation
- Quality handbook: definition of ready/done, severity/priority matrix, gating rules, and escalation paths.
- Living test inventory: traceability from requirements/risks to suites (unit, integration, E2E, non-functional) with owners and status.
- Release/QA checklists: per environment and per release; include gating thresholds, data prep, observability checks, and rollback validation.
- Metrics & reports: coverage, pass rate, flake rate, defect density/escape rate, MTTR/MTRR; publish dashboards and retros.
- Knowledge base: known issues, mitigations, runbooks, and playbooks for incident/rollback/triage.

## Workflows

### Workflow: Build a QA Plan
1) Identify scope, risks, and success criteria.  
2) Choose levels and types of testing; map to environments and data.  
3) Define gates (CI checks, coverage thresholds, blocking severity).  
4) Assign owners, schedule, and communication cadence.  
5) Publish test cases/charters; set defect triage and reporting.  
6) Run, track metrics, and iterate on gaps.

### Workflow: Defect Triage
1) Verify and minimize repro steps; capture logs, traces, env, data.  
2) Classify severity/priority; tag area/owner.  
3) Assess impact and escape point; create fix/mitigation.  
4) Add regression coverage; update dashboards.

### Workflow: Release Readiness
1) Check gates: CI status, coverage thresholds, critical test suites, security scans.  
2) Review open defects vs exit criteria; confirm waivers/flags.  
3) Validate rollback/feature flags and monitoring in place.  
4) Communicate go/no-go with risks and mitigations.
