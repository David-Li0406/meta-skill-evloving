---
name: solid-enforcer
description: Enforce SOLID design principles during code generation, refactors, and code review (SRP/OCP/LSP/ISP/DIP). Use when changing architecture, introducing new abstractions, reducing coupling, eliminating type-switches, or reviewing PRs for maintainability.
compatibility: Cursor Agent Skills (~/.cursor/skills or .cursor/skills) and Agent Skills-compatible agents; optimized for TS/JS/Python repos.
metadata:
  author: janjaszczak
  version: "1.0"
---

# SOLID Enforcer (Generation + Review + Refactor)

## Purpose
Ensure produced or modified code adheres to SOLID, with designs that are extensible, testable, and maintainable. This skill is used both to:
1) **Generate** new code that is SOLID by construction, and
2) **Refactor/review** existing code to become more SOLID without breaking behavior.

## When to activate
Activate when the task includes any of:
- refactor / redesign / architecture changes
- “make it SOLID”, “clean up responsibilities”, “reduce coupling”
- adding extension points / plugin systems / strategies / policies
- replacing large conditionals or type switches
- improving testability, DI, interface boundaries, modularity
- PR review focused on design/maintainability

## Operating mode (must follow)
1) **Clarify (max 1–3 questions)** if requirements or constraints are ambiguous (behavioral invariants, extension expectations, performance constraints, public API stability).
2) **Plan first** for non-trivial changes:
   - identify files/modules to touch
   - state invariants and “must not change” behaviors
   - propose refactor steps with checkpoints (tests/typing/lint)
3) **Implement in small, verifiable steps**:
   - keep diffs tight
   - preserve stable logic
   - add/adjust tests as proof
4) **Prove correctness**:
   - add unit tests demonstrating contracts
   - run/describe the minimal commands to validate (tests, typecheck, lint)
5) **Return complete output**:
   - runnable files (or clear patches)
   - tests
   - short SOLID rationale (how SRP/OCP/LSP/ISP/DIP are satisfied)

---

## SOLID baseline constraints (always enforce)
- Prefer composition over inheritance unless full substitutability is guaranteed.
- Keep classes/modules small; if a unit grows rapidly, challenge responsibilities.
- Make dependencies explicit (constructor/params). Avoid `new` in business logic; use DI/factories.
- Return complete, runnable files and tests proving the contract.

---

## Principle checklists

### SRP — Single Responsibility
Pass if:
1) Each class/module has **one reason to change**.
2) Logging/validation/error-handling are **separated** from domain logic.
3) Methods do **one thing**; if a description needs “and/or”, split it.

Common fixes:
- Extract validation into validators/policies
- Extract I/O (HTTP/DB/files) into adapters/clients
- Split orchestration (use-case/service) from pure domain objects

### OCP — Open/Closed
Pass if:
1) New behaviors can be added by **adding new implementations**, not editing stable logic.
2) Replace type-based switches with **polymorphism** (strategy/decorator/handlers).

Common fixes:
- Strategy pattern: `Policy` / `Algorithm` interface + implementations
- Decorator: wrap behavior without editing core
- Registration/dispatch tables (map keys -> handlers) where appropriate

### LSP — Liskov Substitution
Pass if:
1) Subtypes preserve invariants.
2) No tighter preconditions / no looser postconditions.
3) No “noop/throw overrides” that violate expectations.

Common fixes:
- Split base interface into smaller role interfaces (often pairs with ISP)
- Prefer composition if inheritance requires exceptions
- Add contract tests for substitutability (same test suite for all impls)

### ISP — Interface Segregation
Pass if:
1) Interfaces are minimal and client-specific.
2) “Fat” interfaces are split; clients depend only on what they use.

Common fixes:
- Break one large interface into role interfaces
- Compose roles into larger façades only where needed

### DIP — Dependency Inversion
Pass if:
1) High-level modules depend on abstractions, not concretions.
2) Interfaces are defined near the clients (ports), implementations elsewhere (adapters).
3) Construction is pushed to the composition root; business logic receives dependencies.

Common fixes:
- Constructor/parameter injection
- Factories/providers passed in (not created inside domain logic)
- In TS: avoid importing concrete implementations into core domain/use-cases
- In Python: avoid instantiating clients inside use-case functions; inject them

---

## Refactor playbook (preferred approach)
1) Identify responsibilities and seams:
   - what is domain logic vs infrastructure vs orchestration?
2) Introduce abstractions only where they enable extension/testability:
   - define small interfaces (ports) at the boundary
3) Replace conditionals with strategies/handlers:
   - keep stable logic unchanged; move variability behind an interface
4) Push object creation outward:
   - create a composition root (factory/module) for wiring
5) Lock behavior with tests before/after:
   - contract tests for interfaces
   - regression tests for prior behavior

---

## Output contract (what to return)
Always return:
1) **Code + unit tests** that demonstrate the contract.
2) A **short rationale** explicitly answering:
   - SRP: what responsibilities were separated?
   - OCP: what is now extensible without edits to stable logic?
   - LSP: how substitutability is preserved (or why inheritance was avoided)?
   - ISP: how interfaces were slimmed/split?
   - DIP: what dependencies are injected and where is wiring done?
3) If relevant: a minimal example showing how to extend via a new implementation.

## Red flags (must call out and fix)
- Business logic instantiates concretes (`new`, direct client creation) rather than receiving deps.
- Large modules/classes growing in responsibilities.
- Type switches/if-chains driving behavior selection across the codebase.
- Inheritance hierarchies with special-case overrides or exceptions.

