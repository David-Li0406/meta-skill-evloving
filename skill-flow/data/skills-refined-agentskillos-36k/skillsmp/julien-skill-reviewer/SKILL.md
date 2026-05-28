---
name: julien-skill-reviewer
description: "Review and improve skill quality. Use when: user asks to review skill, check skill quality, improve skill, or after creating a skill with skill-creator-pro."
license: Apache-2.0
metadata:
  author: "Julien"
  version: "2.0.0"
  category: "development"
triggers:
  - "review skill"
  - "check skill"
  - "improve skill"
  - "skill quality"
  - "audit skill"
  - "score skill"
  - "évaluer skill"
  - "vérifier skill"
  - "améliorer skill"
  - "qualité skill"
  - "auditer skill"
  - "revoir skill"
  - "relire skill"
  - "review my skill quality"
  - "check skill score"
  - "évaluer la qualité de la skill"
  - "améliorer ma skill"
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - Bash
---

# Skill Reviewer

Systematically evaluate and improve skill quality through scoring, refactoring, and iteration.

## When to Use

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-skill-reviewer" activated
```

- After creating a skill with skill-creator-pro
- When SKILL.md exceeds 500 lines
- Before packaging for distribution
- When quality score is unknown or low
- When skill feels bloated or has duplication

## Review Process

### Step 1: Read and Parse

```bash
# Read main file
Read skills/skill-name/SKILL.md

# Discover all resources
Glob skills/skill-name/**/*

# Check line count
wc -l skills/skill-name/SKILL.md
```

Parse YAML frontmatter and validate all fields. See [references/yaml-validation.md](references/yaml-validation.md) for complete field specifications.

### Step 2: Score Against Rubric

Evaluate 11 dimensions (1-5 scale). See [references/quality-rubric.md](references/quality-rubric.md) for detailed criteria.

| Dimension | Check |
|-----------|-------|
| Clarity | Clear steps, no ambiguity |
| Completeness | All scenarios covered |
| Discoverability | Good name + description |
| Context Efficiency | **< 500 lines**, refs used |
| Actionability | Concrete, copy-paste ready |
| Resource Organization | Proper scripts/refs/assets |
| Examples | Concrete, realistic |
| Skill Chaining | I/O/Dependencies documented |
| Error Handling | Troubleshooting provided |
| **Trigger Quality** | Natural language, bilingual, 10-20 triggers |
| **Observability** | Announces activation, clear output markers |

### Step 2.5: Auto-Fix Mode (Optional)

Before manual review, optionally run auto-fix for common issues.

**Ask user:**
```
🔧 Auto-fix mode available:
A) Run safe auto-fixes (non-destructive)
B) Interactive fix (approve each change)
C) Skip auto-fix, manual review only
```

**Safe Auto-Fixes** (automatic, no approval):
1. Add missing YAML fields (`version: 1.0.0`, `license: Apache-2.0`)
2. Convert Windows paths (`\` → `/`)
3. Generate TOC for files > 100 lines
4. Warn if triggers < 5

**Interactive Auto-Fixes** (require approval):
1. Detect hardcoded credentials → suggest `.env`
2. Split files > 500 lines → suggest `references/`
3. Check description quality → suggest "what + when" format

**Execution:**
```bash
# Run auto-fix script (integrated)
python skills/julien-skill-reviewer/scripts/auto-fix.py path/to/skill/ --mode safe
python skills/julien-skill-reviewer/scripts/auto-fix.py path/to/skill/ --mode interactive
python skills/julien-skill-reviewer/scripts/auto-fix.py path/to/skill/ --dry-run
```

**Safety:**
- Always creates backup: `SKILL.md.backup-YYYYMMDD-HHMMSS`
- Dry-run mode available for preview
- All changes logged to console

### Step 3: Calculate Score

```
Average = Sum of 11 scores / 11
```

| Score | Status |
|-------|--------|
| 1.0-2.4 | Needs major rework |
| 2.5-3.4 | Functional, needs improvement |
| 3.5-4.4 | Good, minor refinements |
| 4.5-5.0 | Excellent, production ready |

**Minimum for production**: 3.5/5, no dimension < 3/5

### Step 4: Identify Issues

For each dimension < 4/5, document with line references.
See [references/refactoring-templates.md](references/refactoring-templates.md) for issue format.

### Step 5: Suggest Refactoring

Create prioritized plan:
- **Priority 1**: Critical (must fix)
- **Priority 2**: High impact
- **Priority 3**: Polish

See [references/dry-patterns.md](references/dry-patterns.md) for common patterns.

### Step 6: Execute (with approval)

Ask user before changes:
```
A) Show detailed plan
B) Execute Priority 1 automatically
C) Walk through one-by-one
D) Focus on specific dimension
```

### Step 7: Re-evaluate

After refactoring:
1. Re-read modified files
2. Re-score all 11 dimensions
3. Compare before/after
4. Report improvement

### Step 8: Iterate if Needed

If score < 3.5/5, continue iterations.
**Safety limit**: Max 5 iterations.

## Key Validation Checks

See [references/validation-checks.md](references/validation-checks.md) for complete list.

### Required Fields

| Check | Requirement |
|-------|-------------|
| `name` | ≤ 64 chars, lowercase + hyphens only |
| `description` | Third person, ≤ 1024 chars, includes trigger keywords |

### Structure Checks

| Check | Requirement |
|-------|-------------|
| Line count | SKILL.md < 500 lines |
| Paths | Forward slashes only (not Windows backslashes) |
| References | One level deep from SKILL.md |
| Long files | TOC if > 100 lines |
| No duplicates | Content in one place only |

### Optional Fields

| Field | Validation |
|-------|------------|
| `version` | Semantic versioning (X.Y.Z) |
| `license` | Valid SPDX identifier (Apache-2.0, MIT, etc.) |
| `allowed-tools` | Only valid tool names (Read, Write, Edit, Bash, etc.) |
| `user-invocable` | Boolean only (true/false) |
| `disable-model-invocation` | Boolean only (true/false) |
| `mode` | Boolean only (`true` for mode commands, NOT interactive/batch/autonomous) |
| `context` | `fork` only (for isolated subagent execution) |
| `agent` | Valid agent type (Explore, Plan, Bash) |
| `model` | Valid model (haiku, sonnet, opus, or full model ID) |
| `hooks` | Correct syntax: `event`, `matcher`, `command`, optional `once` |
| `triggers` | 5-50 natural language phrases (marketplace extension) |

## Reference Files

| File | Content |
|------|---------|
| [references/quality-rubric.md](references/quality-rubric.md) | 11-dimension scoring details |
| [references/dry-patterns.md](references/dry-patterns.md) | DRY violations and fixes |
| [references/refactoring-templates.md](references/refactoring-templates.md) | Report and plan templates |
| [references/validation-checks.md](references/validation-checks.md) | Automated and manual checks |
| [references/yaml-validation.md](references/yaml-validation.md) | YAML frontmatter field validation |

## Quality Assurance Checklist

Before marking production-ready:

### Score Requirements
- [ ] Average score ≥ 3.5/5
- [ ] No dimension < 3/5

### Structure Requirements
- [ ] SKILL.md ≤ 500 lines
- [ ] Proper progressive disclosure
- [ ] No DRY violations
- [ ] Skill Chaining documented
- [ ] Examples are concrete
- [ ] Error handling documented
- [ ] All references linked from SKILL.md

### YAML Frontmatter Validation
- [ ] `name`: max 64 chars, lowercase + hyphens only
- [ ] `description`: non-empty, max 1024 chars, includes trigger keywords
- [ ] `version`: follows semantic versioning (X.Y.Z) if present
- [ ] `license`: valid SPDX identifier if present (Apache-2.0, MIT)
- [ ] `allowed-tools`: contains only valid tool names if present
- [ ] `mode`: is boolean (`true`/`false`) if present, NOT string
- [ ] `context`: is `fork` if present
- [ ] `agent`: is valid type (Explore, Plan, Bash) if present
- [ ] `model`: is valid (haiku, sonnet, opus, or full ID) if present
- [ ] `hooks`: uses correct syntax with `matcher` and `command` if present
- [ ] YAML syntax is valid (no parse errors)

### Marketplace Requirements
- [ ] **Triggers**: 10-20 natural language phrases in frontmatter
- [ ] **Observability**: Skill announces activation at start

## Skill Chaining

### Skills Required Before
- **julien-dev-tools-skill-creator-pro** (optionnel): If reviewing newly created skill

### Input Expected
- Path to skill directory with SKILL.md
- Skill must have valid YAML frontmatter

### Output Produced
- **Format**: Review report in markdown
- **Side effects**:
  - May create `references/` directory
  - May create new .md files
  - May modify SKILL.md (with approval)
  - Creates backup: `SKILL.md.backup-YYYYMMDD-HHMMSS`
- **Duration**: 5-10 minutes (3-5 iterations)

### Compatible Skills After
**Recommandés** (if score ≥ 3.5/5):
- Package script from skill-creator-pro
- **julien-workflow-sync-personal-skills**: Deploy to ~/.claude/skills/

### Called By
- **julien-dev-tools-skill-creator-pro**: After Step 4, before packaging
- Direct invocation: "Review my skill X"

### Tools Used
- `Read` (usage: read SKILL.md, references/)
- `Glob` (usage: discover skill files)
- `Grep` (usage: search patterns, word count)
- `Edit` (usage: refactor SKILL.md)
- `Write` (usage: create references/*.md)
- `Bash` (usage: wc -l, backup files)

### Visual Workflow

```
User: "Review skills/my-skill"
    ↓
[THIS SKILL]
    ├─► Read SKILL.md + refs
    ├─► Score 9 dimensions
    ├─► Identify issues
    └─► Generate report
    ↓
Score < 3.5/5?
    YES → Refactor → Re-evaluate → Iterate
    NO  → Production ready ✅
    ↓
[Next steps]
    ├─► package_skill.py
    └─► sync-personal-skills
```

### Usage Example

**Scenario**: Review deployment skill

**Command**: "Review the skill at skills/deployment-manager/"

**Result**:
- Initial score: 2.8/5
- Issues: DRY violation, bloated SKILL.md (6000 words), missing chaining
- After 3 iterations: 4.3/5
- SKILL.md: 6000 → 2500 words
- Created: references/api-reference.md, references/examples.md
- Status: Production ready
