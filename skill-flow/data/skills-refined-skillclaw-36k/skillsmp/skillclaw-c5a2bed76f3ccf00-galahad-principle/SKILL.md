---
name: galahad-principle
description: Use this skill when you want to ensure high-quality code through rigorous testing, type safety, and coverage practices.
---

# Coding Agent Quality Rules (Galahad Principle)

Based on Jonathan Lange’s “The Galahad Principle”:  
https://jml.io/galahad-principle/

Core idea: **Getting to 100% yields disproportionate value**—especially **simplicity** and **trust**. When checks are truly “all green”, any new failure is a strong, unambiguous signal; “absence of evidence becomes evidence of absence”.

## Assess Before Applying

Before enforcing these rules strictly, understand the context:

1. **Read project conventions**: Check `tsconfig.json`, `pyproject.toml`, `.eslintrc`, `setup.cfg`, `mypy.ini` for existing standards.
2. **Gauge existing tech debt**: If the codebase already has many `any` types, don't block progress on fixing all of them.
3. **Match scope to task**: A quick bug fix ≠ a new feature ≠ a refactor.

When working in a codebase that doesn't meet these standards:
- **Don't make things worse**: No new type escapes, no new skipped tests.
- **Opportunistically improve**: Clean up what you touch.
- **Don't block the user's goal**: Pragmatic progress beats ideological purity.
- **Use code ratchets to improve over time**: Use the "code-ratchets" skill to improve patterns over time.

## Non-negotiables: Never Evade Feedback

Treat **type errors, test failures, pre-commit hooks, lint errors, and coverage warnings** as helpful feedback. Fix root causes.

### Absolutely Forbidden (unless the user explicitly orders it)
- **Type escapes / silencing**
  - TypeScript: `any`, sketchy `unknown` laundering, unchecked casts, `as any`, `@ts-ignore`, disabling strict mode.
  - Python: `# type: ignore`, `# pyright: ignore`, `cast()` without justification.
  - General: `noqa`, pragma comments to silence legitimate warnings.
- **Coverage gaming**
  - Ignoring/excluding lines/branches/files just to hit targets (e.g., `/* istanbul ignore */`, `# pragma: no cover`).

## Priorities

Type safety is part of correctness and **outranks tests**.

When tradeoffs exist, prioritize in this order:
1. **Type safety / soundness**
2. **Correctness + meaningful tests**
3. **Clarity / maintainability**
4. **Performance**
5. **Backwards compatibility** (lowest)

Breaking changes are acceptable when they improve verifiability and simplify the system.

## Default Workflow (when anything fails)

1. Read the failure output carefully.
2. Restate the real invariant being violated in plain English.
3. Fix the root cause (not the symptom).
4. Improve tests so the behavior is pinned and regressions get caught.
5. Refactor production code if needed to make it easy to type-check and validate.

### Run Checks in This Order
1. **Typecheck**
2. **Unit tests**
3. **Integration tests**
4. **Lint / pre-commit**
5. **Coverage**

Goal: a repo where “all green” is normal, and any new red is a loud, trustworthy signal.

## “Hard to Test” Means Refactor

If something is hard to test or hard to type:
- Treat it as a **design smell**.
- Refactor towards:
  - Smaller pure functions
  - Explicit data flow, minimal global state
  - Clear boundaries between logic and side effects
  - Typed domain models over stringly-typed blobs

## Mocks: Don’t Overuse