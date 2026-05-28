---
name: agent-md-refactor
description: Use this skill when you need to refactor bloated agent instruction files like AGENTS.md or CLAUDE.md to follow progressive disclosure principles, ensuring essential information is easily accessible while organizing the rest into linked documentation.
---

# Skill body

## Triggers

Use this skill when:
- "refactor my AGENTS.md" / "refactor my CLAUDE.md"
- "split my agent instructions"
- "organize my CLAUDE.md file"
- "my AGENTS.md is too long"
- "progressive disclosure for my instructions"
- "clean up my agent config"

## Quick Reference

| Phase | Action | Output |
|-------|--------|--------|
| 1. Analyze | Find contradictions | List of conflicts to resolve |
| 2. Extract | Identify essentials | Core instructions for root file |
| 3. Categorize | Group remaining instructions | Logical categories |
| 4. Structure | Create file hierarchy | Root + linked files |
| 5. Prune | Flag for deletion | Redundant/vague instructions |

## Process

### Phase 1: Find Contradictions

Identify any instructions that conflict with each other.

**Look for:**
- Contradictory style guidelines (e.g., "use semicolons" vs "no semicolons")
- Conflicting workflow instructions
- Incompatible tool preferences
- Mutually exclusive patterns

**For each contradiction found:**
```markdown
## Contradiction Found

**Instruction A:** [quote]
**Instruction B:** [quote]

**Question:** Which should take precedence, or should both be conditional?
```
Ask the user to resolve before proceeding.

### Phase 2: Identify the Essentials

Extract ONLY what belongs in the root agent file. The root should be minimal - information that applies to **every single task**.

**Essential content (keep in root):**
| Category | Example |
|----------|---------|
| Project description | One sentence: "A React dashboard for analytics" |
| Package manager | Only if not npm (e.g., "Uses pnpm") |
| Non-standard commands | Custom build/test/typecheck commands |
| Critical overrides | Things that MUST override defaults |
| Universal rules | Applies to 100% of tasks |

**NOT essential (move to linked files):**
- Language-specific conventions
- Testing guidelines
- Code style details
- Framework patterns
- Documentation standards
- Git workflow details

### Phase 3: Group the Rest

Organize remaining instructions into logical categories for linked files, ensuring clarity and ease of access.