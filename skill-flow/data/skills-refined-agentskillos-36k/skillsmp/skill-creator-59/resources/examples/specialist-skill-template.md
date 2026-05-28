# Specialist Skill Template

⚠️ **IMPORTANT: Most specialist work should use SUBAGENTS, not skills!**

For domain expertise (backend, frontend, security, QA, etc.), use:
```
Task(subagent_type="backend-engineer", prompt="...")
```

Subagents available in `.claude/agents/` directory. Only create a specialist SKILL if you have a specific reason to keep context in current agent.

---

## When to Use This Template (Rare)

Use this template when creating a skill that:
- Adds light domain guidance to current agent (not launching subprocess)
- Requires shared context with current conversation
- Is very lightweight (no complex multi-step work)

**Most specialist work should use subagents via Task tool instead.**

## Template Structure

```markdown
---
name: specialist-name
description: |
  [Domain] specialist for [area]. Use when [use case 1], [use case 2], or [use case 3]. Invoke when debugging "[error pattern 1]", "[error pattern 2]", "[error pattern 3]", or discussing [domain context], [architecture patterns], [technology decisions], or [implementation approach]. Handles [key responsibilities] with expertise in [technologies/patterns]. Keywords: [domain], [tech1], [tech2], [tech3], [pattern1], [pattern2], [tool1], [tool2]
tags: [specialist, [domain], [tech-stack], [area]]
allowed-tools:
  - mcp__serena__*
  - Bash([domain-cli]:*)
  - Read
  - Write
  - Edit
  - mcp__plugin_beads_beads__*
---

# Specialist Name

[Domain] expertise for [specific area] (<duration>).

## Purpose

[What domain this covers and what value the expertise provides]

**Expertise Areas:**
- [Area 1]
- [Area 2]
- [Area 3]
- [Area 4]

## When to Use This Skill

**Use when:**
- [Task pattern 1 requiring expertise]
- [Task pattern 2 requiring expertise]
- [Task pattern 3 requiring expertise]

**Trigger phrases:**
- "[domain task phrase 1]"
- "[domain task phrase 2]"
- "[domain task phrase 3]"

## Workflow

### 1. Analyze Request

[Understand scope, constraints, and requirements]

**Questions to answer:**
- What is the technical scope?
- What are the constraints? (performance, security, compatibility)
- What are the dependencies?
- What are the risks?

**Analysis pattern:**
```[language]
# How to analyze the request
```

### 2. Research Context

[Gather domain-specific information]

**A. Read Relevant Code**
```[language]
# Use Serena to understand existing implementation
```

**B. Check Related Issues**
```[language]
# Check Beads for related work
```

**C. Review Documentation**
```[language]
# Read domain-specific docs
```

### 3. Design Solution

[Apply domain expertise to design approach]

**Domain-Specific Considerations:**
- [Consideration 1]
- [Consideration 2]
- [Consideration 3]

**Pattern Selection:**
```[language]
# Which patterns to use and why
```

### 4. Execute with Expertise

[Implement using domain best practices]

**Step 1: [Implementation step]**
```[language]
# Code with domain patterns
```

**Step 2: [Implementation step]**
```[language]
# Code with domain patterns
```

**Step 3: [Implementation step]**
```[language]
# Code with domain patterns
```

### 5. Verify and Document

[Test and document domain-specific aspects]

**A. Test with Domain Knowledge**
```[language]
# Domain-specific testing
```

**B. Document Decisions**
```markdown
# Why this approach was chosen
# Trade-offs considered
# Future considerations
```

**C. Create Follow-up Issues**
```[language]
# Track discovered work in Beads
```

## Domain Knowledge

### [Topic Area 1]

[Key concepts, patterns, and practices]

**Best Practices:**
- [Practice 1]
- [Practice 2]
- [Practice 3]

**Common Pitfalls:**
- [Pitfall 1] → [How to avoid]
- [Pitfall 2] → [How to avoid]
- [Pitfall 3] → [How to avoid]

**Patterns:**
```[language]
# Example pattern implementation
```

### [Topic Area 2]

[Key concepts, patterns, and practices]

**Best Practices:**
- [Practice 1]
- [Practice 2]

**Patterns:**
```[language]
# Example pattern implementation
```

### [Topic Area 3]

[Key concepts, patterns, and practices]

**Best Practices:**
- [Practice 1]
- [Practice 2]

**Patterns:**
```[language]
# Example pattern implementation
```

## Integration Points

### With Beads

[How specialist tracks work in Beads]

**Pattern:**
```[language]
# Create feature issue
# Track discoveries
# Close on completion
```

### With Serena

[How specialist uses Serena for code operations]

**Pattern:**
```[language]
# Search existing implementations
# Navigate to relevant code
# Make domain-aware edits
```

### With [Domain Tools]

[How specialist uses domain-specific tools]

**Pattern:**
```[language]
# Use domain CLI/tools
```

## Decision Framework

### [Decision Type 1]

**When to choose approach A:**
- [Condition 1]
- [Condition 2]

**When to choose approach B:**
- [Condition 1]
- [Condition 2]

**Example:**
```[language]
if (condition):
    # Approach A
else:
    # Approach B
```

### [Decision Type 2]

**Trade-offs:**
| Approach | Pros | Cons | Use When |
|----------|------|------|----------|
| [A] | [Pro 1, Pro 2] | [Con 1] | [Condition] |
| [B] | [Pro 1] | [Con 1, Con 2] | [Condition] |

## Best Practices

### Do

✅ [Domain-specific best practice 1]
✅ [Domain-specific best practice 2]
✅ [Domain-specific best practice 3]
✅ [Domain-specific best practice 4]
✅ [Domain-specific best practice 5]

### Don't

❌ [Domain-specific anti-pattern 1]
❌ [Domain-specific anti-pattern 2]
❌ [Domain-specific anti-pattern 3]
❌ [Domain-specific anti-pattern 4]

## What This Skill Does

✅ [Domain capability 1]
✅ [Domain capability 2]
✅ [Domain capability 3]
✅ [Domain capability 4]
✅ [Domain capability 5]

## What This Skill DOESN'T Do

❌ [Out of domain 1]
❌ [Out of domain 2]
❌ [Out of domain 3]
❌ [Out of domain 4]

## Examples

### Example 1: [Common Task]

```
User: "[domain task request]"

AI analyzes:
- [Analysis point 1]
- [Analysis point 2]
- [Decision made]

AI executes:
1. [Step with domain expertise]
2. [Step with domain expertise]
3. [Step with domain expertise]

Result:
✅ [Outcome with domain quality]
```

### Example 2: [Complex Task with Trade-offs]

```
User: "[complex task request]"

AI asks: "[clarifying question about trade-offs]"
User: "[preference]"

AI applies expertise:
1. [Chosen approach based on user preference]
2. [Domain-specific implementation]
3. [Verification with domain knowledge]

Result:
✅ [High-quality domain solution]
ℹ️ [Documented trade-offs and rationale]
```

### Example 3: [Edge Case]

```
User: "[edge case task]"

AI recognizes: "[domain-specific edge case pattern]"

AI execution:
1. [Special handling for edge case]
2. [Domain expertise prevents common mistake]
3. [Robust solution]

Result:
✅ [Handled correctly with expertise]
⚠️ [Warning about edge case for future reference]
```

## Troubleshooting

### [Domain-Specific Problem 1]

**Symptom:** [Description]

**Domain Analysis:** [Why this happens in this domain]

**Solution:**
```[language]
# Domain-specific fix
```

### [Domain-Specific Problem 2]

**Symptom:** [Description]

**Domain Analysis:** [Why this happens]

**Solution:**
```[language]
# Domain-specific fix
```

## Related Skills

- **[skill-1]**: [How domains interact]
- **[skill-2]**: [How domains interact]
- **[skill-3]**: [When to use which specialist]

## Reference Materials

**Read for domain context:**
- `resources/[domain]/[topic].md` - [Description]
- `resources/[domain]/patterns.md` - [Description]
- External: [Official docs URL]

**Domain authorities:**
- [Authoritative source 1]
- [Authoritative source 2]
- [Authoritative source 3]

---

**Last Updated:** [Date]
**Skill Type:** Specialist
**Domain:** [Domain name]
**Average Duration:** Variable
**Related Docs:**
- [Domain documentation]
- [Pattern references]
```

## Specialist Skill Checklist

When creating a specialist skill, ensure:

- [ ] Domain clearly defined and scoped
- [ ] Expertise areas documented
- [ ] Decision frameworks provided
- [ ] Best practices listed
- [ ] Common pitfalls documented
- [ ] Domain-specific patterns included
- [ ] Trade-off analysis for key decisions
- [ ] Examples show domain expertise
- [ ] Integration with standard tools (Beads/Serena)
- [ ] Reference materials linked
- [ ] Troubleshooting covers domain-specific issues

## Common Specialist Patterns

### Analyze-Design-Execute Pattern

```
1. Analyze request with domain lens
2. Design solution using domain patterns
3. Execute with domain best practices
4. Verify with domain tests
5. Document domain decisions
```

**Use for:** Most specialist tasks

### Research-Compare-Recommend Pattern

```
1. Research multiple domain approaches
2. Compare trade-offs
3. Recommend based on context
4. Get user confirmation if significant trade-offs
5. Execute recommended approach
```

**Use for:** Tasks with multiple valid approaches

### Diagnose-Fix-Prevent Pattern

```
1. Diagnose with domain knowledge
2. Fix root cause (not symptom)
3. Add safeguards to prevent recurrence
4. Document for team knowledge
```

**Use for:** Bug fixes, security issues, performance problems

## Domain Knowledge Documentation

### Structure

```markdown
## Domain Knowledge

### [Subtopic 1]
**Core concepts:** [Explanation]
**Best practices:** [List]
**Patterns:** [Code examples]
**Pitfalls:** [What to avoid]

### [Subtopic 2]
...
```

### What to Include

- **Core concepts:** Essential domain knowledge
- **Best practices:** Proven approaches
- **Patterns:** Reusable code/design patterns
- **Pitfalls:** Common mistakes and how to avoid
- **Trade-offs:** When to use what approach
- **Decision trees:** How to choose between options

## Real Examples

### backend-engineer

**Domain:** FastAPI backend development
**Expertise:**
- API design (REST, GraphQL)
- Database operations (Supabase, migrations)
- Data validation (Pydantic)
- Testing (pytest, fixtures)
**Pattern:** Analyze-Design-Execute

### security-engineer

**Domain:** Security and compliance
**Expertise:**
- Authentication/authorization
- Data encryption
- Input validation
- OWASP top 10
- Compliance (SOX, PCI-DSS, GDPR)
**Pattern:** Diagnose-Fix-Prevent

### frontend-engineer

**Domain:** React frontend development
**Expertise:**
- Component architecture
- State management
- TypeScript types
- UI/UX patterns (Material-UI)
- Testing (Jest, RTL)
**Pattern:** Analyze-Design-Execute

---

**Related:**
- resources/skill-types.md - Skill type details
- resources/v3-philosophy.md - V3 principles
- ../../agents/backend-engineer.md - Example subagent (use Task tool, not skills, for specialist work)
