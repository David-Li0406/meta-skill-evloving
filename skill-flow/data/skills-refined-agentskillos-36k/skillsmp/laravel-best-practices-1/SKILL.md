---
name: laravel-best-practices
description: Enforce Laravel Best Practices when generating code, reviewing code, and writing tests (SRP, skinny controllers, FormRequests, service/action classes, DRY, Eloquent/Collections, Blade query avoidance, eager loading, chunking).
metadata:
  installed_path: .codex/skills/laravel-best-practices
  outputs:
    - review (findings + patch outline)
    - generate (file plan + code)
    - tests (test matrix + starter tests)
---

## Purpose
This skill guides an AI coding agent to:
1) generate Laravel code aligned with established best practices,
2) review Laravel code (or diffs) and propose refactors aligned to those practices,
3) propose and scaffold tests (Pest preferred; PHPUnit supported).

## Use when
- Implementing or refactoring controllers, FormRequests, service/action classes, jobs, events/listeners, policies, observers
- Reviewing PRs, diffs, or entire files in a Laravel application
- Designing maintainable application layering and test strategy

## Rulebook
Use **references/rulebook.json** as the source of truth for:
- rule ids
- detection signals
- recommended refactor patterns
- expected outputs

When you flag an issue, always include:
- rule_id
- evidence (file + line numbers or excerpt)
- minimal refactor steps first
- test impact plan

## Core principles (high-level)
- **Single Responsibility**: one reason to change per class; one main concern per method.
- **Thin controllers**: controllers orchestrate; business logic lives elsewhere.
- **Validation in FormRequests**: move validation and authorization there.
- **Business logic in services/actions**: extract workflows into testable units.
- **DRY**: centralize repeated logic (Eloquent scopes, value objects/DTOs, helpers).
- **Prefer Eloquent + Collections**: use expressive domain modeling where practical.
- **No queries in Blade**: views must not query the database; eager load to avoid N+1.
- **Chunk/stream large datasets**: avoid loading large tables into memory.

## Workflow: Review
When asked to review code:
1) Identify the layer (Controller, Request, Model, Service/Action, Blade, etc.).
2) Apply rules from rulebook.json; emit findings with rule ids.
3) Provide a patch outline (what files to create/change) and a test plan.

### Recommended output (JSON)
Return a JSON object:
- summary: score, counts
- findings[]: rule_id, severity, evidence, rationale, recommendations, patch outline
- tests: a short matrix or list of impacted tests

## Workflow: Generate code
When asked to implement a feature:
1) Propose file layout first (Controller + FormRequest + Service/Action + Model scopes, etc.).
2) Generate code using Laravel idioms: dependency injection, FormRequests, policies, resources.
3) Include a minimal test plan (Feature + Unit tests).

## Workflow: Generate tests
Prefer Pest if repository uses Pest (presence of pestphp/pest in composer.json); otherwise PHPUnit.
- FormRequest validation/authorization
- Service/action business rules (unit)
- Feature tests for endpoints (happy path + validation + authz)
- Mock external systems (HTTP, queues, notifications) as needed
