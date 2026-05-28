---
name: requirement-clarification
description: Use this skill to resolve requirement ambiguities through structured questioning, ensuring clarity before development can proceed.
---

# Requirement Clarification

## ⚠️ CRITICAL RULES - READ FIRST

1. **SEARCH FIRST**: Always search `docs/reference/pm/` for related documents before asking questions.
2. **ONE QUESTION AT A TIME**: Max 5 questions per session.
3. **UPDATE DOCUMENTS**: After clarification, update the relevant story/version files.

## Language Configuration

Before generating any content, check `aico.json` in the project root for the `language` field to determine the output language. If not set, default to English.

## Process

1. **Scan context**: Check `docs/reference/pm/` for existing documentation.
2. **Identify ambiguities**: Categorize by type (scope, behavior, data, edge cases).
3. **Prioritize**: Sort by impact: scope > security > UX > technical.
4. **Ask ONE question at a time**: Max 5 questions per session.
5. **Provide recommendation**: Each question should have a recommended option with reasoning.
6. **Update docs**: Document each answer immediately.

## Question Format

```markdown
### Question [N]: [Topic]

**Context**: [Quote relevant requirement]

**Ambiguity**: [What's unclear]

**Options**:
| Option | Description | Implications |
|--------|-------------|--------------|
| A | [First option] | [Trade-offs] |
| B | [Second option] | [Trade-offs] |

**Recommended**: [Option] because [reasoning]
```

## Ambiguity Categories

| Category       | Focus                      |
| -------------- | -------------------------- |
| Scope          | What's included/excluded   |
| Behavior       | How feature should work    |
| Data           | What information is needed |
| Edge cases     | Unusual scenarios          |
| Error handling | Failure modes              |

## Key Rules

- ALWAYS ask ONE question per message, never batch.
- MUST provide recommended option with reasoning for each question.
- ALWAYS prioritize blocking issues (scope, security) over minor details.
- Max 5 questions per clarification session.

## Common Mistakes

- ❌ Ask all questions at once → ✅ One at a time.
- ❌ Open-ended questions → ✅ Multiple choice with recommendation.
- ❌ Low-impact questions → ✅ Focus on blocking issues first.