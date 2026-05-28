---
name: julien-skill-creator
description: "Create or update Claude Code skills. Use when: user wants to create a skill, add a new skill, update skill, or mentions SKILL.md. Includes Skill Chaining documentation."
license: Apache-2.0
metadata:
  author: "Julien (based on Anthropic skill-creator)"
  version: "2.0.0"
  category: "development"
triggers:
  - "SKILL.md"
  - "skill.md"
  - "create skill"
  - "new skill"
  - "add skill"
  - "build skill"
  - "skill template"
  - "write skill"
  - "créer skill"
  - "nouvelle skill"
  - "ajouter skill"
  - "construire skill"
  - "écrire skill"
  - "créer une skill"
  - "faire une skill"
  - "développer une skill"
  - "create a new skill"
  - "build custom skill"
  - "skill development"
---

# Skill Creator

Enhanced guidance for creating effective skills with proper structure and documentation.

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-skill-creator" activated
```

## Core Principles

### Concise is Key

Context window is shared. Only add what Claude doesn't already know. Challenge each piece: "Does this justify its token cost?"

### Progressive Disclosure (3 Levels)

1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (**< 500 lines**)
3. **Bundled resources** - As needed by Claude

### Skill Structure

```
skill-name/
├── SKILL.md (required, < 500 lines)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/      - Executable code
    ├── references/   - Documentation loaded on-demand
    └── assets/       - Output resources (templates, images)
```

**Key rules:**
- References must be **one level deep** from SKILL.md
- Files > 100 lines need **table of contents** at top
- Use **forward slashes** only (not Windows backslashes)
- No extraneous files (README.md, CHANGELOG.md, etc.)

### Naming & Description

See [references/naming-conventions.md](references/naming-conventions.md) for full guidelines.

**Quick rules:**
- Name: max 64 chars, lowercase + hyphens, gerund form preferred (`processing-pdfs`)
- Description: max 1024 chars, **third person**, include "what + when to use"

## Skill Creation Process

### Step 1: Understand with Examples

Ask clarifying questions:
- "What functionality should this skill support?"
- "Give examples of how it would be used"
- "What should trigger this skill?"

### Step 2: Choose Destination

**ALWAYS ask the user where to place the skill:**

| Destination | Path | Use Case |
|-------------|------|----------|
| **Local (projet)** | `.claude/skills/` | Skill spécifique à ce projet uniquement |
| **Marketplace** | `~/.../Claude Code MarketPlace/skills/` | Skill réutilisable, à partager/sync |

**Questions to ask:**
- "Cette skill est-elle spécifique à ce projet ou réutilisable ailleurs?"
- "Voulez-vous la partager via le marketplace?"

**Naming convention by destination:**
- Local: simple name (`my-project-deploy`)
- Marketplace: prefixed (`julien-{category}-{name}`)

### Step 3: Plan Reusable Contents

For each example, identify:
- Scripts needed (deterministic/repeated code)
- References needed (schemas, docs, policies)
- Assets needed (templates, images)

### Step 4: Initialize Skill

**For Local (project):**
```bash
mkdir -p .claude/skills/<skill-name>
# Or copy template
cp -r ~/.claude/skills/julien-skill-creator/assets/template-skill/ .claude/skills/<skill-name>/
```

**For Marketplace:**
```bash
# Use marketplace path
MARKETPLACE="$HOME/OneDrive/Coding/_Projets de code/2025.11 Claude Code MarketPlace"
mkdir -p "$MARKETPLACE/skills/<skill-name>"
# Or use init script
python "$MARKETPLACE/scripts/init_skill.py" <skill-name> --path "$MARKETPLACE/skills/"
```

### Step 5: Edit the Skill

#### YAML Frontmatter

**Required Fields:**

```yaml
---
name: skill-name                      # Required: max 64 chars, lowercase + hyphens
description: What it does and when to use it  # Required: max 1024 chars, third person
---
```

**Optional Fields**:

See [references/yaml-frontmatter-guide.md](references/yaml-frontmatter-guide.md) for complete documentation on all optional fields.

**Quick Reference - When to Use Each Field:**

| Field | Use Case |
|-------|----------|
| `version` | Always (recommended for hot-reload tracking) |
| `license` | Always (Apache-2.0, MIT, or proprietary) |
| `allowed-tools` | Security-sensitive operations (restrict tool access) |
| `user-invocable: false` | Internal helper skills (not in /slash menu) |
| `disable-model-invocation: true` | Manual-only destructive operations |
| `mode: true` | Mode commands (modify Claude's global behavior) |
| `context: fork` | Isolated execution in subagent (exploration, research) |
| `agent` | Specify agent type (Explore, Plan, Bash) |
| `model` | Cost optimization (haiku for exploration, opus for complex) |
| `hooks` | Lifecycle automation (lint on write, cleanup on stop) |
| `triggers` | **ALWAYS** for marketplace (10-20 natural language triggers) |
| `metadata` | Organization, attribution, categorization |

> **Note**: `triggers` is our marketplace extension, not official Anthropic. Official approach uses keywords in `description`.

#### Body Instructions

Write using **imperative form** (verb-first). Reference bundled resources clearly.

#### Document Skill Chaining (Critical)

Add Skill Chaining section at end. See [references/skill-chaining-template.md](references/skill-chaining-template.md) for complete template.

Required subsections:
1. Skills Required Before
2. Input Expected
3. Output Produced
4. Compatible Skills After
5. Called By
6. Tools Used
7. Visual Workflow
8. Usage Example

### Step 6: Add Activation Announcement (REQUIRED)

**Every skill MUST announce its activation for observability.**

Add this instruction at the beginning of the skill's execution section:

```markdown
## Observability

**First**: At the start of execution, display:
```
🔧 Skill "your-skill-name" activated
```
```

This:
- Confirms which skill is running
- Provides feedback to users
- Contourns Issue #4084 (hooks can't display in UI)

### Step 7: Package Skill

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Validates then creates `.skill` file.

### Step 8: Add Semantic Routing Triggers

Add triggers to YAML frontmatter for automatic skill suggestion:

```yaml
---
name: your-skill-name
description: What it does. Use when [specific triggers].
triggers:
  - "excel"
  - "créer un fichier excel"
  - "ajouter des formules"
---
```

#### Trigger Writing Methodology

**Golden Rule**: Write triggers as users naturally speak, not technical jargon.

| Bad (Technical) | Good (Natural Language) |
|-----------------|------------------------|
| `xlsx manipulation` | `créer un fichier excel` |
| `git repository sync` | `mettre à jour le serveur` |
| `docker container` | `lancer le site` |
| `pdf extraction` | `lire ce pdf` |

**3 Categories of Triggers (include all 3):**

1. **Keywords** (1-2 words): Core concepts users mention
   - `excel`, `pdf`, `docker`, `skill`

2. **Action Phrases** (3-5 words): What users want to DO
   - `créer un fichier excel`
   - `traduire ces sous-titres`
   - `déployer sur le serveur`

3. **Problem Phrases**: How users describe their PROBLEM
   - `mon site ne marche plus`
   - `je veux automatiser`
   - `comment faire pour...`

**Bilingual Coverage:**
- Always include French AND English variants
- French first (primary user language), then English

**Quantity Guidelines:**
- Minimum: 5 triggers
- Optimal: 10-20 triggers
- Maximum: 50 triggers (diminishing returns)

**Test Your Triggers:**
```bash
python scripts/benchmark-semantic-router.py "votre phrase test"
```

### Step 9: Iterate with Self-Assessment

**Never fix everything at once.** Each iteration focuses on ONE improvement.

1. Score against quality rubric (see [references/quality-rubric.md](references/quality-rubric.md))
2. Identify top 3-5 gaps
3. Fix ONE dimension per iteration
4. Re-score until average ≥ 3.5/5

## Reference Files

| File | Content |
|------|---------|
| [references/quality-rubric.md](references/quality-rubric.md) | 11-dimension scoring (1-5 scale) |
| [references/skill-chaining-template.md](references/skill-chaining-template.md) | Complete chaining documentation format |
| [references/naming-conventions.md](references/naming-conventions.md) | Official Anthropic naming rules |
| [references/advanced-patterns.md](references/advanced-patterns.md) | Feedback loops, plan-validate-execute, templates |
| [references/final-checklist.md](references/final-checklist.md) | Pre-distribution verification checklist |

## Degrees of Freedom

Match specificity to task fragility:

| Freedom | When to Use | Example |
|---------|-------------|---------|
| **High** | Multiple valid approaches | Code review guidelines |
| **Medium** | Preferred pattern exists | Scripts with parameters |
| **Low** | Fragile/critical operations | Database migrations |

## What NOT to Include

- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md
- User-facing documentation
- Setup/testing procedures
- Any auxiliary context about creation process

## Security & Portability

### Security Checklist

- ✓ No hardcoded credentials (passwords, API keys, tokens)
- ✓ Sensitive data in `.env` file
- ✓ `.env` added to `.gitignore`
- ✓ Instructions use environment variables (`$VAR` or `source .env`)
- ✓ Use `allowed-tools` to restrict tool access for sensitive operations
- ✓ Set `disable-model-invocation: true` for admin-only/destructive skills
- ✓ Add `version` field for hot-reload tracking (Claude Code v2.1.0+)

### Portability Checklist

- ✓ Use relative paths (`.env`, `./scripts/`) instead of absolute paths
- ✓ Use `~/.claude/skills/` for user paths, not hardcoded home directories
- ✓ Avoid platform-specific paths (e.g., `C:\Users\...` in examples)
- ✓ Use forward slashes only (not Windows backslashes)

## Anti-Patterns to Avoid

❌ Description >200 chars (breaks progressive disclosure)
❌ Content >300 lines (too much detail)
❌ Duplicates existing docs (should reference instead)
❌ Development notes in content (timestamps, changelog)
❌ Generic/vague description (doesn't explain when to use)
❌ Second-person language ("you should...")
❌ Information in both SKILL.md and references files
❌ Hardcoded credentials (passwords, API keys, database credentials, tokens)
❌ Sensitive data in code examples (use placeholders or `.env` variables)
❌ Absolute paths in examples (`/home/user/...`, `C:\Users\...`)
❌ Platform-specific paths (Windows-only or Unix-only examples)

## Skill Chaining

### Skills Required Before
- None (entry point skill for skill creation)

### Input Expected
- User request to create/improve a skill
- Domain knowledge or examples from user
- Optional: existing skill to improve

### Output Produced
- **Format**: Complete skill directory with SKILL.md + resources
- **Side effects**: Creates files in specified path
- **Duration**: 10-30 minutes depending on complexity

### Compatible Skills After
**Recommandés:**
- **julien-dev-tools-skill-reviewer**: Review and score the created skill

### Called By
- Direct user invocation: "Create a skill for X"
- Skill improvement workflows

### Tools Used
- `Read` (usage: read existing skills, templates)
- `Write` (usage: create SKILL.md, references)
- `Bash` (usage: run init_skill.py, package_skill.py)
- `Edit` (usage: modify existing skills)

### Visual Workflow

```
User: "Create skill for X"
    ↓
[THIS SKILL]
    ├─► Step 1: Gather examples
    ├─► Step 2: Plan resources
    ├─► Step 3: Initialize structure
    ├─► Step 4: Write SKILL.md + refs
    ├─► Step 5: Package
    ├─► Step 6: Add semantic triggers
    └─► Step 7: Iterate
    ↓
skill-name.skill created
    ↓
[Optional] skill-reviewer for quality check
```

### Usage Example

**Scenario**: Create deployment skill for VPS

**Command**: "Create a skill for deploying to my Hostinger VPS"

**Result**:
- `hostinger-deployment/SKILL.md` created
- `hostinger-deployment/references/` with server docs
- `hostinger-deployment/scripts/` with deploy scripts
- Packaged as `hostinger-deployment.skill`
