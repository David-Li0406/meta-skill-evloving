# Philosophy of Effective Comments

Core principles from "A Philosophy of Software Design" by John Ousterhout.

## Why "Self-Documenting Code" Is a Myth

The claim that good code doesn't need comments is one of the most damaging misconceptions in software engineering.

**What code CAN express:**
- Structure and flow
- Data types and signatures
- Explicit logic and operations

**What code CANNOT express:**
- Why this approach was chosen over alternatives
- What high-level abstraction this code represents
- What invariants must be maintained
- What would break if you changed this
- What the designer was thinking

Code is **how**. Comments are **what** (at a higher level) and **why**.

## Comments Capture Designer Intent

When you write code, your mind holds crucial information:
- The mental model of the abstraction
- Considered alternatives and why they were rejected
- Assumptions about how the code will be used
- Edge cases that informed the design

**This information exists only in your head.** Without comments, it disappears when you move on. The next person (including future you) must reverse-engineer your thinking from the code alone—a lossy, error-prone process.

## Comments as a Design Tool

Write comments **before** implementing:

1. **Interface comments first** - Describe what the abstraction does before writing code
2. **Check your thinking** - If comments are awkward to write, the design may be flawed
3. **Then implement** - Write code that fulfills the documented contract
4. **Verify alignment** - Ensure implementation matches the documented intent

This approach:
- Forces clarity about what you're building
- Exposes design problems early
- Produces better abstractions
- Results in accurate comments naturally

## The Abstraction Principle

Comments operate at two levels:

### Interface Comments (Higher Abstraction)
For users of the code who don't need to read the implementation:
- Describe **what** the abstraction provides
- Hide implementation details
- Enable using the code without reading it

### Implementation Comments (Same Level, Different Information)
For maintainers who need to understand the code:
- Explain **why** the code works this way
- Highlight non-obvious logic
- Document constraints and gotchas

The key insight: **Interface comments abstract away the code; implementation comments annotate it.**

## Comments as Investment

Good comments pay dividends quickly:

| Investment | Return |
|------------|--------|
| 5 minutes writing interface comments | Hours saved by every future user |
| 2 minutes explaining "why" | Debug sessions avoided |
| 1 minute noting a constraint | Bugs prevented |

**The cost of poor comments:**
- Developers read code more than they write it
- Every person who touches the code pays the tax of understanding it
- Missing context leads to broken assumptions and bugs
- Maintenance becomes archaeology

Comments are not overhead. They are a **core deliverable** of software development.

## The Vocabulary Rule

A comment fails if it uses the same words as the code:

```python
# Bad: Uses the same words
# Increment the count
count += 1

# Good: Provides context at a higher level
# Track total requests for rate limiting
count += 1
```

Ask yourself: **Does this comment provide information not already expressed by the code?**

If you're struggling to write a comment without repeating the code, ask:
- Why does this code exist?
- What would someone need to know to modify this safely?
- What mental model should the reader have?
