---
name: coding-quality-principles
description: Use this skill to ensure high coding standards through tests, types, lints, and coverage.
---

# Coding Agent Quality Rules (Galahad Principle)

Based on Jonathan Lange’s “The Galahad Principle”:  
https://jml.io/galahad-principle/

Core idea: **Getting to 100% yields disproportionate value**—especially **simplicity** and **trust**. When checks are truly “all green”, any new failure is a strong, unambiguous signal; “absence of evidence becomes evidence of absence”.

## Assess Before Applying

Before enforcing these rules strictly, understand the context:

1. **Read project conventions**: Check configuration files (e.g., `tsconfig.json`, `pyproject.toml`, `.eslintrc`, `setup.cfg`, `mypy.ini`) for existing standards.
2. **Gauge existing tech debt**: If the codebase has many `any` types, prioritize progress over perfection.
3. **Match scope to task**: Differentiate between quick bug fixes, new features, and refactoring.

When working in a codebase that doesn't meet these standards:
- **Don't make things worse**: Avoid introducing new type escapes or skipped tests.
- **Opportunistically improve**: Clean up what you touch.
- **Don't block the user's goal**: Pragmatic progress beats ideological purity.
- **Use code ratchets to improve over time**: Gradually enhance patterns.

## Non-negotiables: Never Evade Feedback

Treat **type errors, test failures, pre-commit hooks, lint errors, and coverage warnings** as helpful feedback. Fix root causes.

### Absolutely Forbidden (unless explicitly ordered)
- **Type escapes / silencing**: Avoid using `any`, unchecked casts, or disabling strict mode.
- **Coverage gaming**: Do not ignore/exclude lines just to hit targets.
- **Faking results**: Skipping CI steps and claiming success is unacceptable.

### When User Requests Conflict with These Principles
1. **Comply, but note the tradeoff**: Inform the user of potential issues.
2. **Offer alternatives briefly**: Suggest better practices.
3. **Don't lecture**: Keep communication concise.

## Priorities

Type safety is part of correctness and **outranks tests**. When tradeoffs exist, prioritize in this order:
1. **Type safety / soundness**
2. **Correctness + meaningful tests**
3. **Clarity / maintainability**
4. **Performance**
5. **Backwards compatibility**

Breaking changes are acceptable when they improve verifiability and simplify the system, but:
- Flag breaking changes explicitly to the user.
- Prefer non-breaking improvements when effort is similar.

## Default Workflow (When Anything Fails)

1. **Read the failure output carefully.**
2. **Understand the context**: Investigate the original intent of the code.
3. **Restate the real invariant** being violated in plain English.
4. **Fix the root cause** (not the symptom).
5. **Improve tests** to catch regressions.
6. **Refactor production code** if needed for better type-checking.

### Run Checks in This Order
1. **Typecheck**
2. **Unit tests**
3. **Integration tests**
4. **Lint / pre-commit**
5. **Coverage**

Goal: A repository where “all green” is normal, and any new red is a loud, trustworthy signal.

## What Makes a Test Meaningful

✅ **Meaningful tests**:
- Test observable behavior from the caller's perspective.
- Would catch real regressions.
- Document intent and edge cases.

❌ **Not meaningful**:
- Test implementation details.
- Duplicate what the type checker verifies.
- Pass regardless of whether the code works.

## Coverage: Aim for Meaningful, Not Mechanical

- **Do**: Cover all business logic paths and edge cases.
- **Don't**: Chase 100% by testing trivial code.
- **Legitimate exclusions exist**: For platform-specific branches or debug-only code.

## Handling Flaky Tests

1. **Identify the source**: Determine if the flakiness is due to timing, race conditions, or external services.
2. **Fix the non-determinism**: Use techniques like injecting clocks or adding synchronization.
3. **If unfixable now**: Quarantine in a separate test suite.
4. **Never**: Mark as "expected flaky" in the main CI path.

## "Hard to Test" Means Refactor

If something is hard to test or type, treat it as a **design smell**. Refactor towards:
- Smaller pure functions.
- Explicit data flow, minimal global state.
- Clear boundaries between logic and side effects.

## Mocks: Use Sparingly and Explicitly

Avoid injecting mocks via monkeypatching. Instead, make functions operate in multiple environments by passing in substitutable operations explicitly.

### Examples

**TypeScript:**
```typescript
function processOrder(
  orderId: string,
  deps: { getTime: () => Date; getOrder: (id: string) => Order }
) {
  const now = deps.getTime();
  const order = deps.getOrder(orderId);
}
```

**Python:**
```python
def process_order(
    order_id: str,
    *,
    get_time: Callable[[], datetime] = datetime.now,
    get_order: Callable[[str], Order] = database.get_order,
) -> OrderResult:
    now = get_time()
    order = get_order(order_id)
```

## Summary: What "Good" Looks Like

- Types encode invariants; no “trust me” casts.
- Tests assert observable behavior.
- Coverage comes from exercising real behavior, not exclusions.
- If a thing can't be verified cleanly, refactor until it can.
- Progress beats perfection; aim to improve continuously.