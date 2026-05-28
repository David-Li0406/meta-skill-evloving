---
name: skill-foundry
description: Create and validate portable Agent Skills. Use when authoring new skills, validating existing skills, or learning skill best practices. Guides through structure, portability, and progressive disclosure.
license: MIT
metadata:
  version: "2.0"
  author: ubod
  portability: universal
---

# Skill Foundry

Expert guidance for creating portable Agent Skills.

## When to Use

- Creating a new skill from scratch
- Validating an existing skill
- Understanding skill anatomy and best practices
- Improving skill descriptions or structure
- Converting single-agent skills to universal format

## Quick Commands

```bash
# Validate a skill
python scripts/validate.py path/to/skill/

# Scaffold a new skill
python scripts/scaffold.py my-skill-name

# Validate all skills in workspace (if Ubod install.sh provides this)
../../scripts/validate-all.sh
```

## Creating a New Skill

### Option 1: Quick Start (5 Minutes)

See [references/QUICK_START.md](references/QUICK_START.md) for a 5-minute tutorial.

**Summary:**
1. Create directory: `mkdir -p .github/skills/my-skill`
2. Copy template or use scaffold script
3. Fill in name, description, commands, process
4. Test immediately
5. Iterate based on usage

### Option 2: Via Scaffold Script

```bash
python scripts/scaffold.py my-skill \
  --description "Does X when Y. Use when Z."
```

### Option 3: Manual Creation

1. Copy `templates/SKILL.template.md` or `examples/hello-world/SKILL.md`
2. Fill in frontmatter (name, description)
3. Write body sections (When to Use, Commands, Process, Examples, Boundaries)
4. Validate: `python scripts/validate.py my-skill/`
5. Test with Claude
6. Refine based on behavior

## Skill Anatomy

See [references/SKILL_ANATOMY.md](references/SKILL_ANATOMY.md) for deep dive on:
- Progressive disclosure (Level 1/2/3 loading)
- Frontmatter standards
- Directory structure
- Token efficiency

### Minimal Structure

A skill needs only `SKILL.md`:

```
.github/skills/<skill-name>/
└── SKILL.md
```

### Complete Structure

```
.github/skills/<skill-name>/
├── SKILL.md              # Required: frontmatter + instructions
├── scripts/              # Optional: executable helpers
├── references/           # Optional: detailed docs (loaded on-demand)
├── templates/            # Optional: starter files
└── assets/               # Optional: images, data files
```

## Writing SKILL.md

### Frontmatter (YAML)

Use only standard fields for portability:

```yaml
---
name: my-skill-name
description: What this skill does and when to use it. Be specific about triggers.
license: MIT
requirements: Python 3.9+, pytest
metadata:
  version: "1.0"
  author: your-name
---
```

**Required fields:**
- `name`: Lowercase, hyphens only, ≤64 characters
- `description`: ≤1024 characters, include both "what" and "when"

**Optional standard fields:**
- `license`: License name or bundled file reference
- `requirements`: Environment hints (≤500 chars)
- `metadata`: Arbitrary key-value pairs (for tool-specific extensions)

**Do NOT use at root level** (breaks portability):
- `allowed-tools` (Claude-only)
- `model` (Claude-only)
- `hooks` (Claude-only)
- `context` (Claude-only)

If you need tool-specific features, put them in `metadata` namespace:

```yaml
metadata:
  claude-code:
    allowed-tools: Read, Grep, Glob
```

### Body (Markdown)

Recommended sections:

```markdown
# Skill Name

## When to Use
- Specific trigger condition 1
- Specific trigger condition 2

## Commands
- `command --flag arg`
- `another-command --option`

## Process
1. Step one with details
2. Step two with details
3. Step three with details

## Examples

### Example 1: Task X
[Input/output example]

### Example 2: Task Y
[Input/output example]

## Boundaries

✅ **Always do:**
- Action 1
- Action 2

⚠️ **Ask first:**
- Action that needs confirmation
- Potentially destructive action

🚫 **Never do:**
- Forbidden action 1
- Forbidden action 2
```

### Referencing Files

Use relative paths from skill root:

```markdown
See [API documentation](references/API.md) for details.

Run validation:
```bash
python scripts/validate.py input.json
```
```

Claude will load referenced files on-demand.

## Best Practices

Key principles (see [references/BEST_PRACTICES.md](references/BEST_PRACTICES.md)):

1. **Great descriptions** = what + when  
   - "Does X. Use when Y or when user mentions Z."
2. **Keep SKILL.md lean** (< 500 lines / 5000 tokens)  
   - Move detailed content to `references/`
3. **Deep content in references/** (loaded on-demand)  
   - API docs, schemas, examples
4. **Executable commands** (with flags)  
   - `npm test --coverage`, not just "run tests"
5. **Concrete examples** (code > prose)  
   - Show ✅ good and ❌ bad patterns
6. **Set boundaries** (always/ask/never)  
   - See [references/AGENT_PATTERNS.md](references/AGENT_PATTERNS.md)

### Progressive Disclosure

Skills load in three levels:

1. **Level 1 (Discovery)** - Only `name` and `description` (always in context)
2. **Level 2 (Activation)** - Full SKILL.md body (when skill is relevant)
3. **Level 3 (Deep Dive)** - `references/`, `scripts/` (on-demand)

**Design implication**: Optimize description (always loaded), keep SKILL.md focused (sometimes loaded), move details to references (rarely loaded).

See [references/SKILL_ANATOMY.md](references/SKILL_ANATOMY.md) for details.

## Validation Checklist

Before deploying a skill:

- [ ] `name` is lowercase, hyphens, ≤64 chars
- [ ] `description` includes what AND when (≤1024 chars)
- [ ] Body under 500 lines / 5000 tokens
- [ ] Commands are executable (include flags and args)
- [ ] Examples included (concrete input/output)
- [ ] Boundaries set (✅ always / ⚠️ ask / 🚫 never)
- [ ] Passes validation: `python scripts/validate.py my-skill/`
- [ ] Tested with Claude on real tasks
- [ ] Works across VS Code and Claude Code

## Validation Script

The validator checks:

1. **Required fields**: `name` and `description` present
2. **Name format**: Lowercase, hyphens, no spaces, ≤64 chars
3. **Description length**: ≤1024 characters
4. **Non-portable fields**: Warns if tool-specific fields at root
5. **YAML syntax**: Valid frontmatter structure

Run validation:

```bash
python scripts/validate.py path/to/SKILL.md
```

## Resources

All resources are in the `references/` directory:

- **[QUICK_START.md](references/QUICK_START.md)** - Create your first skill in 5 minutes
- **[BEST_PRACTICES.md](references/BEST_PRACTICES.md)** - Distilled from Anthropic docs
- **[AGENT_PATTERNS.md](references/AGENT_PATTERNS.md)** - Lessons from 2500+ agents
- **[PORTABILITY.md](references/PORTABILITY.md)** - Cross-platform compatibility
- **[SKILL_ANATOMY.md](references/SKILL_ANATOMY.md)** - Structure and loading

## Examples

- **[hello-world](../examples/hello-world/)** - Minimal working example
- **See also**: Real-world examples in your workspace's `.github/skills/` directory

## Templates

See [templates/SKILL.template.md](templates/SKILL.template.md) for a starter template.
