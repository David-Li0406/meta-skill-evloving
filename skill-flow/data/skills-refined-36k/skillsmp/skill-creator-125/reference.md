# Reference Guide


# Skill Creator

A meta-skill for creating optimized Agent skills through an interactive, guided workflow.

## Workflow

### Phase 1: Research (mandatory first step)

Before doing anything else:

1. Use the `general` subagent to fetch current best practices for skill creation
2. Explore existing skills in the agent's configuration directory for context and patterns
3. Best practices from the guide always take precedence over local patterns

Never skip this phase - it ensures skills are created with up-to-date patterns.

### Phase 2: Discovery

Ask the user directly to gather requirements. Ask about:

- Skill name and purpose
- When should the skill activate? (trigger conditions)
- What tools/capabilities does it need?
- Is this a single-file skill or does it need supporting files?

Never assume - always ask for clarification on ambiguous requirements.

### Phase 3: Interactive Design

Draft the initial skill structure, then iterate with the user:

1. **Determine skill structure** based on complexity:
   - Simple skills: Just `SKILL.md`
   - Complex skills: `SKILL.md` + `reference.md` + `cookbook/` directory

2. **Present draft to user** following recommended structure:
   - `SKILL.md`: Workflow and quick reference only
   - `reference.md`: Conceptual content (best practices, idioms, data structures, anti-patterns)
   - `cookbook/`: Practical recipes in Problem/Solution/Tip format

3. Present options to the user:
   - Description phrasing (which activates best?)
   - Workflow structure (linear vs branching?)
   - Tool restrictions (read-only? specific tools only?)
   - File organization (single file or multi-file structure?)

4. Ask: "Does this capture your intent? What would you change?"
5. Revise and repeat

**Exit conditions**: User says "stop", "finish", "done", or explicitly approves.

Be talkative and offer suggestions throughout. The goal is interactive refinement.

### Phase 4: Validation

Present a detailed checklist with pass/fail for each item:

**Core Requirements:**
- [ ] YAML frontmatter syntax valid
- [ ] Name matches directory name (kebab-case)
- [ ] Description includes activation triggers
- [ ] Description is specific, not vague
- [ ] Workflow is actionable and clear
- [ ] Tool restrictions considered (if applicable)

**Structure Requirements:**
- [ ] SKILL.md contains workflow and quick references only
- [ ] Conceptual content moved to reference.md (if applicable)
- [ ] Cookbook recipes follow Problem/Solution/Tip format (if applicable)
- [ ] Recipe code blocks specify language
- [ ] Supporting files organized appropriately

Ask the user to confirm any suggested improvements before applying.

### Phase 5: Context Management

For long-running or complex skill creation:

- Delegate heavy work to `general` subagent
- This preserves the main context window for continued interaction

## Key Behaviors

- **Always start with research**: Never skip the research phase
- **Ask, don't assume**: Ask the user directly - clarity over speed
- **Interactive by default**: Offer suggestions, ask for feedback, iterate on every draft
- **Progressive disclosure**: Keep SKILL.md focused, suggest supporting files when needed
- **Delegate heavy work**: Use `general` subagent for complex skills

## Quick Reference

### Recommended Skill Structure

**Simple skills** (single-purpose, minimal complexity):
```
skill-name/
└── SKILL.md
```

**Complex skills** (multiple concepts, lots of examples):
```
skill-name/
├── SKILL.md           # Workflow and quick references only
├── reference.md       # Conceptual content (best practices, idioms, anti-patterns)
└── cookbook/          # Practical recipes
    ├── basics.md
    ├── advanced.md
    └── troubleshooting.md
```

### When to Use reference.md vs cookbook/

**reference.md** - Conceptual understanding:
- Language idioms and patterns
- Data structures and type system concepts
- Best practices and anti-patterns
- Design principles
- Comparison tables (e.g., tool choices)

**cookbook/** - Practical recipes:
- Concrete code examples
- Step-by-step solutions to specific problems
- Common tasks and how to accomplish them
- Recipe format: Problem/Solution/Tip

### Cookbook Recipe Format

Each cookbook file should follow this structure:

```markdown
# [Topic] Cookbook

[Short description of what this cookbook covers]

---

## Recipe Name

**Problem**: What specific problem are you trying to solve?

**Solution**:
```lang
# Code example here
```

**Tip**: Helpful advice, gotchas, or best practices.

---

## Another Recipe

**Problem**: [Description]

**Solution**:
```lang
# Code
```

**Tip**: [Advice]

---
```

**Key elements**:
- Each recipe separated by `---` horizontal rule
- Code blocks must specify language (```python, ```rust, etc.)
- Tips should be actionable and specific
- Problem statements should be concrete, not abstract
