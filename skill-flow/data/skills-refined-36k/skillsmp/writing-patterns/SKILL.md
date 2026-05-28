---
name: writing-patterns
description: "Use when documenting reusable code patterns, architectural approaches, or established solutions with keyword triggers and anti-patterns."
---

# Writing Patterns

## Overview

Patterns are reusable solutions to recurring problems. Good patterns have clear triggers, code examples, and known anti-patterns.

## When to Create

**Create a pattern when:**
- Solution applies to multiple projects
- Same approach discovered repeatedly
- Code pattern is non-obvious
- Anti-patterns should be avoided

**Don't create for:**
- One-time solutions
- Project-specific conventions
- Standard library usage (well-documented elsewhere)

## Structure Template

```markdown
---
name: pattern-name
keywords: [list, of, trigger, words]
category: [architecture | data | ui | testing | integration]
---

# Pattern Name

## Problem
[What problem this pattern solves]

## Solution
[Brief description of the approach]

## When to Use
[Trigger conditions]

## Code Example
[Working code with comments]

## Anti-Patterns
[What NOT to do and why]

## Related Patterns
[Links to complementary patterns]

## Version Notes
[Changes across versions/frameworks]
```

## Quality Checklist

- [ ] Problem clearly stated
- [ ] Solution is concise
- [ ] Keywords enable discovery
- [ ] Code example is complete and runnable
- [ ] Anti-patterns with explanations
- [ ] Category assigned for organization
- [ ] Version notes if framework-specific
- [ ] Under 100 lines (reference to files for complex examples)

## Testing Requirements

1. **Keyword test** - Search finds pattern via keywords
2. **Code test** - Example actually works
3. **Application test** - Agent applies pattern correctly
4. **Anti-pattern test** - Agent avoids documented pitfalls
5. **Version test** - Notes accurate for target versions

## Examples

**Good Pattern:**
```markdown
---
name: optimistic-updates
keywords: [optimistic, instant, ux, state, rollback]
category: ui
---

# Optimistic Updates

## Problem
User waits for server response before seeing UI change.

## Solution
Update UI immediately, rollback on error.

## When to Use
- Non-critical updates (likes, comments)
- Fast perceived performance needed
- Server usually succeeds

## Code Example
const [items, setItems] = useState(data);

async function addItem(newItem) {
  // Optimistic update
  setItems(prev => [...prev, newItem]);

  try {
    await api.create(newItem);
  } catch {
    // Rollback on failure
    setItems(prev => prev.filter(i => i.id !== newItem.id));
    toast.error('Failed to add');
  }
}

## Anti-Patterns
- Using for critical operations (payments)
- No rollback mechanism
- Complex state with dependencies

## Related Patterns
- error-boundaries
- loading-states
```

**Bad Pattern:**
```markdown
# Good Code

Write good code that works well.
```
(No problem, no example, no anti-patterns)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| No keywords | Add 3-5 trigger words |
| Incomplete example | Provide runnable code |
| Missing anti-patterns | Document what NOT to do |
| Too verbose | Keep under 100 lines |
| No category | Assign for organization |
| Outdated versions | Add version notes |
