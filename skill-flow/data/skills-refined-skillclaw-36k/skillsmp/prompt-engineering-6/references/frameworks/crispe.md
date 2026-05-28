# CRISPE Framework

**C**apacity, **R**equirement, **I**nstructions, **S**pecifications, **P**urpose, **E**xamples

Best for creative/exploratory tasks needing flexibility.

## Template

```xml
<capacity>
[Role to assume]
[Expertise and perspective]
</capacity>

<requirement>
[What is needed - the core ask]
[Deliverable description]
</requirement>

<instructions>
[Step-by-step approach]
1. [First action]
2. [Second action]
3. [Third action]
</instructions>

<specifications>
[Constraints and boundaries]
- [Specification 1]
- [What to avoid]
</specifications>

<purpose>
[Why this matters]
[How it will be used]
</purpose>

<examples>
[Concrete samples if helpful]
[Show what good looks like]
</examples>
```

## Example

```xml
<capacity>
Senior product strategist with B2B SaaS experience.
Think in jobs-to-be-done and value propositions.
</capacity>

<requirement>
Generate 5 positioning statements for AI writing assistant.
Differentiate from Jasper, Copy.ai.
</requirement>

<instructions>
1. Identify unique capabilities (context-awareness, brand voice)
2. Map to customer pain points
3. Craft using: "For [audience], [product] is [category] that [benefit]"
4. Vary angle: speed, quality, consistency, cost
</instructions>

<specifications>
- Each under 50 words
- No superlatives ("best", "most powerful")
- Must be defensible/provable
- Target: Marketing teams 50-500 employees
</specifications>

<purpose>
A/B testing on landing pages.
Winner becomes homepage headline.
</purpose>

<examples>
Good: "For marketing teams drowning in content requests, Acme is the AI assistant that maintains brand voice because it learns from existing content."

Bad: "Acme is the best AI that writes better content faster."
</examples>
```

## When to Use

- Content ideation
- Brainstorming
- Creative tasks
- When flexibility matters more than structure

## When NOT to Use

- Well-defined technical tasks → Use COSTAR
- Complex multi-step workflows → Use 5C
