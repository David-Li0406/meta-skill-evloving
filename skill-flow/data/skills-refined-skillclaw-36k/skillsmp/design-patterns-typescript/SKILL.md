---
name: design-patterns-typescript
description: TypeScript router to choose pattern and route to the next skill. Use when you need to choose pattern options or compare approaches for Adapter, Strategy, Factory Method, Abstract Factory, Builder, Prototype, Singleton, Command, Observer, Decorator, Facade, Bridge, Composite, Proxy, Flyweight, Iterator, State, Template Method, or Chain of Responsibility.
compatibility: Designed for Codex CLI / filesystem agents; works without script execution and does not require external tools.
metadata:
  author: codex
  version: 0.2.2
---

# Design Patterns TypeScript Router

## Goal

Route the user to the most suitable TypeScript design pattern skill quickly.
Keep recommendations minimal, align with existing architecture, and avoid over-abstraction.

## When to use (activation keywords)

Use when the user mentions or implies: choose pattern, router, TypeScript architecture, refactor, codebase structure, abstraction, extendability, plugin system, integration layer, data access, eventing, or commands.

## Inputs to ask for (max 3 questions)

Ask at most three:
1) What is the core change or pain (e.g., coupling, duplication, variation, integrations)?
2) What constraints matter most (e.g., existing architecture, testing, runtime, DI container)?
3) What is the smallest concrete example of the code or flow in question?

## Quick routing

Category routing:
- Creational: object creation complexity, variants, environment-based implementations.
- Structural: wrappers, composition, interface simplification, boundaries.
- Behavioral: algorithms, workflows/state, eventing, pipelines/handlers.

Common symptom -> pattern:
- Third-party API mismatch -> Adapter
- Many optional constructor params -> Builder
- Families of related objects -> Abstract Factory
- Too many `new` scattered -> Factory Method
- Need one shared instance -> Singleton
- Add logging/caching without touching core -> Decorator
- Simplify complex subsystem API -> Facade
- Treat tree nodes uniformly -> Composite
- Switch algorithms at runtime -> Strategy
- Pub/sub or event fan-out -> Observer
- Queue/undo/replay actions -> Command
- Handler pipeline or middleware -> Chain of Responsibility

## Handoff rule

Always output: Next skill: <pattern-name-kebab>-pattern-typescript

## Reference

See `references/pattern-selector.md` for the full catalog (definitions, signals, TypeScript notes).

## Output format

Recommendation: <Pattern>
Rationale:
- <1-3 short bullets>
Anti-signals:
- <1-3 short bullets>
Next skill: <pattern-name-kebab>-pattern-typescript
Minimal shape: <1-2 lines describing the smallest viable implementation>

## Guardrails

- Avoid cargo-cult patterns; default to the simplest refactor.
- Align with existing architecture and team conventions.
- Do not add abstractions unless they reduce coupling or improve testability.
- Keep scope tight; defer large rewrites.
