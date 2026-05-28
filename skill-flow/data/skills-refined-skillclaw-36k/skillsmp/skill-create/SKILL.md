---
name: skill-create
description: This skill should be used when creating or refactoring Claude Code skills, guiding an interactive questionnaire, selecting an archetype (workflow/tool/domain), scaffolding from templates, and validating the result. Triggers include "create skill", "new skill", "scaffold skill", "bootstrap skill".
---

# skill scaffolder

guide claude through designing and scaffolding new skills with templates, questionnaires, and validation.

## philosophy

> "decisions first, prose second"

| principle | application |
|-----------|-------------|
| decision trees | choose archetype, size, and placement before writing |
| concrete thresholds | prefer explicit counts and gates over vague advice |
| scaffold then fill | generate structure first, then deepen |
| reusable prose | move repeatable text to prompts and link by alias |
| validate early | run introspect + validate after first pass |

## when to use

| use | skip |
|-----|------|
| bootstrapping a new skill | simple prompt tweaks or copy edits |
| re-scaffolding a skill with no structure | existing skill with depth issues (use skill-improve) |
| selecting archetype or template | one-line updates |
| validating skill quality before enabling | deletion or deprecation |

## decision tree: create vs improve

```
Is this a new skill?
├── No folder exists for this skill name → create
├── Existing SKILL.md < 80 lines and no references/ → create (re-scaffold)
├── Existing skill with references/ or > 80 lines → improve (skill-improve)
├── Change is < 20 lines and no structure changes → edit directly
└── unclear → run introspect-skill.sh for signal
```

## decision tree: archetype selection

```
What is the core purpose?
├── 3+ ordered steps or 2+ gates/checkpoints → workflow
├── deterministic input → output in <= 2 steps → tool
├── 3+ docs/policies or FAQ lookup → domain
├── 2+ archetypes apply → hybrid (pick primary + cross-links)
└── unclear → default workflow, document why
```

## decision tree: content placement

```
Where does this content belong?
├── SKILL.md (target 180-360 lines for mature skills)
│   ├── decision trees, workflow steps, validation gates
│   ├── short examples (<= 12 lines each)
│   └── tables with thresholds and tool callouts
├── references/ (>= 50 lines each)
│   ├── section > 25 lines or 3+ subtopics → reference
│   ├── checklists, rubrics, schemas → reference
│   └── reusable prose → prompts (link by alias)
├── scripts/ (executable helpers)
│   ├── command used 2+ times → script
│   ├── command > 120 chars or 3+ flags → script
│   └── multi-step pipelines → script
└── assets/ (static samples)
    ├── templates, example inputs/outputs, fixtures
    └── checklists used verbatim
```

## decision tree: skill complexity

```
How complex should the skill be?
├── Simple (120-170 lines)
│   ├── 1-2 references
│   ├── 0-1 scripts
│   └── single narrow purpose
├── Medium (170-240 lines)
│   ├── 2-4 references
│   ├── 1-2 scripts
│   └── 2-3 related operations
├── Full-featured (240-380 lines)
│   ├── 3-6 references
│   ├── 2-4 scripts
│   ├── multiple decision trees
│   └── cross-skill integration
└── Complexity signals
    ├── 6+ trigger phrases → medium+
    ├── 2+ archetypes apply → full-featured
    ├── 3+ external tools referenced → full-featured
    └── domain expertise required → full-featured
```

## decision tree: validation gates

```
Is the skill ready?
├── validate-skill.sh PASS with 0 warnings → ready
├── warnings present → fix then rerun
├── references < 50 lines or TODOs present → expand
├── missing tool examples (0) → add at least 2
└── missing anti-pattern fixes → add before finish
```

## concrete values (sourced)

| item | target | source |
|------|--------|--------|
| references depth | >= 50 lines each | `references/validation-rules.md` |
| script trigger | command used >= 2 times | `references/skill-patterns.md` |
| script trigger (complex) | > 120 chars or 3+ flags | `references/skill-patterns.md` |
| skill sizing | simple 120-170, medium 170-240, full 240-380 | `references/archetype-templates.md` |
| decision tree coverage | cover ~80% common scenarios | `references/skill-patterns.md` |
| tool example minimum | 2+ command examples | `references/validation-rules.md` |

## workflow

### 0. preflight (inventory)

- locate existing skill folder and templates
- if skill exists, run `./scripts/introspect-skill.sh` for signal
- output: skill brief stub (name, scope, archetype guess)

### 1. intake (questionnaire)

- use `references/questionnaire.md`
- capture triggers, anti-triggers, inputs/outputs, artifacts, validation
- output: filled skill brief

skill brief template:

| field | example |
|-------|---------|
| name | skill-create |
| triggers | "create skill", "scaffold skill" |
| archetype | workflow |
| complexity | full-featured |
| outputs | updated SKILL.md + references/ |

### 2. choose archetype + size

- use decision trees above
- confirm complexity tier and hybrid status
- output: archetype + sizing decision

### 3. scaffold from template

```bash
./scripts/init-skill.sh <skill-name> --template workflow|tool|domain --path ~/.claude/skills
```

- confirm directory created and TODOs present
- output: scaffolded skill directory

### 4. author SKILL.md core

- update frontmatter with triggers and description
- fill when-to-use table
- add decision trees with thresholds
- add workflow steps with inputs/outputs
- add tool integration examples (2+)
- add anti-patterns table with fixes

### 5. deepen references

- expand each reference with thresholds, examples, and checklists
- ensure each reference is linked in `## references`
- keep each reference >= 50 lines

### 6. add scripts and assets

- create scripts for repeated commands and mark executable
- add assets for templates, examples, and checklists
- output: runnable helpers and static samples

### 7. validate and iterate

```bash
./scripts/introspect-skill.sh ~/.claude/skills/<skill-name>
./scripts/validate-skill.sh ~/.claude/skills/<skill-name>
```

- fix warnings (links, duplication, phrasing)
- rerun until PASS

### 8. finalize

- check line count vs complexity tier
- ensure references list is complete
- confirm voice rules and anti-pattern coverage

## tool integration

| tool | command | purpose |
|------|---------|---------|
| prompts | `prompts commands export /create-skill` | load creation prompt |
| agents | `agents plan --project skills` | plan skill creation |
| rg | `rg --files references` | discover reference files |
| trails | `trails trail record` | skill creation persistence |

### trails integration

persist skill creation for pattern analysis:

```bash
# record skill creation
trails trail record --agent claude --action completed \
  --task "skill-create: $SKILL_NAME - $ARCHETYPE" \
  --confidence $CONFIDENCE --json -q
```

**trails enables**:
- tracking skill creation patterns
- measuring archetype distribution
- correlating creation with audit scores

## tool integration examples

### prompt library

```bash
CONTENT=$(prompts commands export /create-skill --json --quiet | jq -r '.content')
```

### planning (optional)

```bash
agents plan --project skills --title "create <skill-name>" --json --quiet
```

### file discovery

```bash
rg --files references
rg -n "TODO|FIXME" SKILL.md references
```

### validation signals

```bash
./scripts/introspect-skill.sh ~/.claude/skills/<skill-name>
./scripts/validate-skill.sh ~/.claude/skills/<skill-name>
```

### codebase exploration (when skill targets a repo)

```bash
layer --check-cycles
outline --tree --stats
```

## templates

| archetype | location |
|-----------|----------|
| workflow | `assets/templates/workflow-skill/` |
| tool | `assets/templates/tool-skill/` |
| domain | `assets/templates/domain-skill/` |

## voice rules

- **lowercase headers** except acronyms (API, CLI)
- **tables over lists** for comparisons
- **terse content** - one line per bullet
- **no corporate speak** - "which feels right?" not "would you prefer..."
- **backticks for paths** - always `like/this.ts`

see imessage skill for gold standard.

## validation iteration

```
validate-skill.sh output:
├── PASS → skill ready for use
├── WARNING: missing reference links
│   └── Fix: add links in ## references section
├── WARNING: description not third-person
│   └── Fix: start with "This skill should be used when..."
├── WARNING: duplicate content detected
│   └── Fix: move duplicated lines to references/
└── FAIL: missing frontmatter
    └── Fix: add --- block with name/description
```

typical iteration:
1. `introspect-skill.sh` → quick assessment
2. address suggestions
3. `validate-skill.sh` → formal validation
4. fix warnings
5. repeat until PASS

manual gates (recommended):
- each reference >= 50 lines with examples
- 2+ tool integration commands present
- 3-6 trigger phrases in description
note: `introspect-skill.sh` warns above 200 lines; allow longer when full-featured.

## references

- [references/skill-patterns.md](references/skill-patterns.md) - best practices, thresholds, and anti-patterns
- [references/questionnaire.md](references/questionnaire.md) - intake prompts and skill brief template
- [references/validation-rules.md](references/validation-rules.md) - automated checks and manual gates
- [references/archetype-templates.md](references/archetype-templates.md) - template structure per archetype

## scripts

- [scripts/init-skill.sh](scripts/init-skill.sh) - scaffold from archetype template
- [scripts/validate-skill.sh](scripts/validate-skill.sh) - structural/quality checks
- [scripts/introspect-skill.sh](scripts/introspect-skill.sh) - quick assessment and suggestions

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| vague triggers | skill misfires or never activates | add 3-6 explicit trigger phrases |
| oversized SKILL.md | key info buried | move sections > 25 lines to references/ |
| missing tool examples | users cannot execute | add at least 2 command examples |
| no validation gate | quality unknown | run introspect + validate until PASS |
| mixing archetypes without label | unclear intent | choose primary, note hybrid in decision tree |
| references not linked | dead docs | link every reference in `## references` |
| scripts missing or not executable | repeated commands copy/pasted | add scripts and `chmod +x` |
| TODOs left behind | incomplete scaffold | replace or remove before validation |
