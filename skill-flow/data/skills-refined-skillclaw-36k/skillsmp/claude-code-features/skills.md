# Skills (Agent Skills)

**Trigger**: Claude auto-decides based on context

## Characteristics

- Progressive disclosure (loaded only when needed)
- Can consist of multiple files (SKILL.md + references)
- Shares main context

## Best For

- **Tool usage guides** (how to use specific tools/libraries)
- Domain-specific expertise & patterns
- Architecture guides
- API design patterns
- Security checklists

## Key Criteria

**"Knowledge not always needed, but should surface when relevant"**

- Putting it in AGENTS.md wastes context tokens
- But it's necessary for specific tasks
- Claude auto-loads when relevant

## Not Suitable For

- Standard procedures (→ Commands)
- Processing requiring independent context (→ Agents)
- Constraints that should always apply (→ Rules)
