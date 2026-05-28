# TDD Rationales

Extended discussion of why the order matters and responses to common objections.

## The Core Insight

TDD isn't about testing. It's about **design feedback**.

When you write the test first, the test tells you:

- Is this API awkward to use?
- Are there too many dependencies?
- Is the scope too large?

Tests written after can't give this feedback - the design is already locked in.

## Why Test-First Order Matters

### "I'll write tests after to verify it works"

Tests written after code pass immediately. Passing immediately proves nothing:

- **Might test wrong thing** - You test what you built, not what was required
- **Might test implementation, not behavior** - Tests become brittle, break on refactor
- **Might miss forgotten edge cases** - You only test what you remember
- **Never saw it catch the bug** - No proof the test actually tests anything

Test-first forces seeing the test fail, proving it actually tests something.

**The proof is in the failure.** A test that never failed never proved it could catch anything.

### "I already manually tested all the edge cases"

Manual testing is ad-hoc:

- **No record of what was tested** - Can't prove coverage
- **Can't re-run when code changes** - Must manually re-test everything
- **Easy to forget cases under pressure** - "Ship it" mindset skips edge cases
- **"It worked when I tried it" ≠ comprehensive** - Happy path bias

Automated tests are systematic. They run the same way every time. They catch regressions immediately.

**Manual testing is discovery. Automated testing is verification.**

### "Deleting X hours of work is wasteful"

Sunk cost fallacy. The time is already gone. The choice now:

- **Delete and rewrite with TDD** (X more hours, high confidence)
- **Keep it and add tests after** (30 min, low confidence, likely bugs)

The "waste" is keeping code that can't be trusted.

**Working code without real tests is technical debt.** You'll pay interest on it forever in:

- Debugging time
- Fear of refactoring
- Regression bugs
- Production incidents

### "TDD is dogmatic, being pragmatic means adapting"

TDD IS pragmatic:

- **Finds bugs before commit** - Faster than debugging after deploy
- **Prevents regressions** - Tests catch breaks immediately
- **Documents behavior** - Tests show how to use code
- **Enables refactoring** - Change freely, tests catch breaks

"Pragmatic" shortcuts = debugging in production = slower delivery.

**The most pragmatic thing you can do is write the test first.**

### "Tests after achieve the same goals - it's spirit not ritual"

No. Tests-after answer "What does this do?" Tests-first answer "What should this do?"

Tests-after are biased by the implementation:

- **Testing what was built, not what's required** - Confirmation bias
- **Verifying remembered edge cases, not discovered ones** - Survivorship bias

Tests-first force edge case discovery before implementing. You design the interface, then implement it.

**30 minutes of tests after ≠ TDD.** You get coverage numbers, but lose proof the tests work.

### "Keep as reference, write tests first"

You'll adapt it. That's testing after. Delete means delete.

The "reference" code biases your thinking:

- **You'll match the test to the code** instead of matching code to the test
- **You'll skip edge cases the reference missed**
- **You'll replicate bugs in the reference**

**Fresh implementation from tests is the only way to be sure.**

### "Need to explore first"

Fine. Exploration is valuable. But then:

1. **Throw away exploration**
2. **Start fresh with TDD**

Exploration code is prototype code. It's not production code. Don't ship it.

**The exploration taught you what to build. Now build it right.**

## Good vs Bad Tests

| Quality          | Good                        | Bad                                                 |
| ---------------- | --------------------------- | --------------------------------------------------- |
| **Minimal**      | One thing per test          | `test('validates email and domain and whitespace')` |
| **Clear**        | Name describes behavior     | `test('test1')`                                     |
| **Shows intent** | Demonstrates desired API    | Obscures what code should do                        |
| **Real code**    | Tests actual implementation | Tests mock behavior                                 |

### What makes a test name good?

A good test name is a specification:

```typescript
// Good: Describes behavior
test("rejects email without @ symbol", () => {});
test("accepts valid email with subdomain", () => {});
test("returns error message for empty input", () => {});

// Bad: Describes implementation or is vague
test("test email validation", () => {});
test("email test", () => {});
test("it works", () => {});
```

**If you can't name it clearly, you don't understand what you're testing.**

## The Economics of TDD

| Scenario                  | Time Investment | Bug Discovery     | Refactoring Safety |
| ------------------------- | --------------- | ----------------- | ------------------ |
| No tests                  | 0 hours         | Production        | Dangerous          |
| Tests after               | 2 hours         | Sometimes staging | Risky              |
| TDD                       | 3 hours         | Development       | Safe               |

The extra hour of TDD saves:

- **4+ hours of debugging** when bugs surface later
- **Unlimited hours** of fear when refactoring
- **Customer trust** when bugs don't reach production

## Final Rule

```text
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without explicit permission.
