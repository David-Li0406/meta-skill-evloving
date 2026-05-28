# Explanation Template

**Purpose**: Deepen understanding by providing context, history, and perspective. User reads when reflecting.

**Key Characteristics**:
- Provides context, background, and history
- Makes connections to other concepts
- Discusses "why", not "how"
- Admits perspectives and alternatives
- Bounded to a single topic

## Structure

```markdown
# About [Subject]

[One sentence introducing what this is about]

## Background

[Historical context: why this matters, when it was introduced, or how it evolved]

Example: "Caching has been essential to web performance since the early 
days of the internet, when bandwidth was scarce. While bandwidth is 
cheaper now, caching remains critical because latency directly affects 
user experience."

## The core concept

[What is this fundamentally, without being instructional]

## [Aspect 1: Design consideration]

[Discuss why this was chosen, tradeoffs, alternatives]

Example: "We chose Event-Sourcing because it provides a complete audit 
trail. The tradeoff is that queries are more complex; traditional 
databases offer simpler queries but lose the ability to see historical state."

## [Aspect 2: Another consideration]

[Same approach: discuss why, tradeoffs, alternatives]

## Comparison to [related concept]

[How this relates to similar ideas]

Example: "Unlike traditional caching, which discards old data, Event 
Sourcing preserves the entire history. This is similar to a version 
control system like Git, where every change is recorded."

## Different perspectives

Some teams prefer [Approach A] because [reason]. This works well when 
[condition], but can be problematic when [condition].

Others prefer [Approach B] because [reason]. This is better suited for 
[situation], though it requires [tradeoff].

## Further reading

- **Learn it**: [Link to Tutorial]
- **Use it**: [Link to How-to Guide]
- **Details**: [Link to Reference]
```

## Language Patterns

Use these patterns consistently throughout your explanation:

| Pattern | Example |
|---------|---------|
| **The reason for X is because historically, Y** | "The reason we use semver is because it emerged from the open-source community's need for predictable versioning." |
| **W is better than Z, because** | "Immutability is better than shared state because it eliminates entire categories of race conditions." |
| **X in system Y is analogous to W in system Z** | "A microservice in our architecture is analogous to a module in traditional monoliths—isolated, focused, and independently deployable." |
| **Some prefer W because Z. This is good when** | "Some teams prefer GraphQL because it reduces over-fetching. This is beneficial when you have diverse client needs." |

## Key Principles to Remember

✓ **Make connections** — Relate to other concepts and contexts

✓ **Provide context** — Design decisions, history, constraints, tradeoffs

✓ **Talk about the subject** — Titles should work with "About…" prefix

✓ **Admit perspective** — Acknowledge limitations and alternatives

✓ **Weigh alternatives** — Show why one approach is chosen over others

✓ **Bound the discussion** — Don't absorb instructions or reference

✓ **Answer "why" questions** — Not "how" or "what"

## Example

See [examples.md](examples.md#example-4-explanation) for a complete working example: "About API rate limiting"
