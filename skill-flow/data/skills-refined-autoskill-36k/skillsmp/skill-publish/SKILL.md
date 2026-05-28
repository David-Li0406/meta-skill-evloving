---
name: skill-publish
description: One-way sync from private skills to public versions. Triggers include "publish skills", "sync to public", "update public skills", or when private skills have changed.
---

# skill-publish

one-way transformation of private skills to portable public versions. strips private CLI dependencies, documents alternatives.

## philosophy

> "the decision tree is the skill; the CLI is convenience"

| principle | application |
|-----------|-------------|
| one-way flow | private → public only, never reverse |
| preserve decision trees | core methodology stays intact |
| document alternatives | private CLIs become optional enhancements |
| exclude personal | communication and orchestration skills stay private |
| minimal diff | only change what's necessary for portability |

## when to use

| use | skip |
|-----|------|
| private skill changed significantly | cosmetic edits only |
| new skill ready for sharing | skill still in development |
| periodic sync (monthly) | just synced recently |
| team member needs updated skill | skill is in excluded list |
| preparing for Claude Desktop upload | skill depends on local secrets |

## decision tree: include or exclude

```
Should this skill be published?
├── Personal communication skill? (imessage, slack)
│   └── EXCLUDE: contains personal voice/patterns
├── Heavy orchestration skill without portable bootstrap? (auto)
│   └── EXCLUDE: requires local agent infrastructure
├── External AI collaboration/orchestration skill? (pair, fanout, loop)
│   └── INCLUDE: note bash + copilot/codex requirements
├── Has private CLI as core dependency?
│   ├── CLI is enhancement only? → INCLUDE with alternatives
│   └── CLI is essential to function? → EXCLUDE
├── Contains secrets or API patterns?
│   └── EXCLUDE or redact
└── Default
    └── INCLUDE with transformation
```

## decision tree: transformation scope

```
How much transformation needed?
├── No private CLI references?
│   └── copy as-is (rare)
├── Only ## tool integration section?
│   └── light: convert to ## enhancements (optional)
├── CLI commands in workflow steps?
│   └── medium: add manual alternatives inline
├── CLI commands throughout?
│   └── heavy: systematic replacement + enhancements section
└── CLI is core to skill function?
    └── exclude from public
```

## decision tree: CLI categorization

```
What kind of CLI is this?
├── Private/local only?
│   ├── outline, layer, verify → manual code exploration
│   ├── trails → manual notes or omit
│   ├── linear → generic issue tracker patterns
│   ├── slack → generic messaging patterns
│   ├── agents, codex, copilot → omit or generalize
│   ├── prompts → inline the content or omit
│   └── messages → omit (personal)
├── Public CLI (available via package managers)?
│   ├── gh (GitHub CLI) → keep, widely available
│   ├── rg (ripgrep) → keep with grep alternative
│   ├── fd (fd-find) → keep with find alternative
│   └── jq → keep, widely available
├── Standard Unix?
│   └── keep: wc, grep, find, git, cat, stat, readlink
└── Unknown?
    └── check if installable, else provide alternative
```

## concrete values

| item | value | source |
|------|-------|--------|
| included skills | 18 | current public/ inventory |
| excluded skills | 3 | imessage, slack, auto |
| sync frequency | monthly or on significant change | convention |
| enhancements section | always last before references | structure convention |
| alternative format | `tool \| command \| alternative` table | readability |

## included skills

| skill | category | primary value |
|-------|----------|---------------|
| ask-deep | clarification | OARS questioning technique |
| emil-kowalski | design | animation principles |
| pr-audit | review | security/performance checklist |
| test-pilot | testing | coverage strategies |
| friction-analysis | analysis | DX bottleneck detection |
| context | continuity | handoff patterns |
| agent-docs-audit | docs | documentation accuracy |
| project-review | review | standards alignment |
| issue-context | enrichment | issue preparation |
| skill-compose | meta | skill orchestration |
| www-studio | design | marketing site craft |
| metaprompt-factory | meta | prompt engineering |
| skill-audit | meta | skill inventory |
| skill-create | meta | skill scaffolding |
| skill-improve | meta | skill enhancement |
| pair | collaboration | output contracts for external AI |
| fanout | analysis | multi-perspective parallel analysis |
| loop | orchestration | autonomous work with zero-context bootstrap |

## excluded skills

| skill | reason |
|-------|--------|
| imessage | personal communication patterns |
| slack | workspace-specific, requires tokens |
| auto | requires local agent infrastructure (no portable bootstrap) |

## workflow

### phase 1: inventory

```bash
# list private skills
ls ~/Developer/skills/*/SKILL.md

# list current public skills
ls ~/Developer/skills/public/*/SKILL.md

# find skills needing sync (modified after public version)
for skill in ~/Developer/skills/*/SKILL.md; do
  name=$(basename $(dirname "$skill"))
  # skip public dir itself
  [ "$name" = "public" ] && continue
  public="$HOME/Developer/skills/public/${name}/SKILL.md"
  if [ -f "$public" ]; then
    if [ "$skill" -nt "$public" ]; then
      echo "needs sync: $name"
    fi
  fi
done
```

### phase 2: assess each skill

for each skill needing sync:

1. check exclusion list
2. identify CLI dependencies
3. determine transformation scope
4. note sections requiring changes

### phase 3: transform

transformation checklist:

- [ ] update frontmatter description (remove private tool mentions)
- [ ] replace private CLI commands with manual alternatives
- [ ] convert `## tool integration` to `## enhancements (optional)`
- [ ] add alternatives table for each private CLI
- [ ] preserve all decision trees unchanged
- [ ] preserve all concrete values unchanged
- [ ] preserve all anti-patterns unchanged

### phase 4: write public version

```bash
# create skill folder
mkdir -p ~/Developer/skills/public/{skill-name}

# write SKILL.md (proper skill structure)
# ~/Developer/skills/public/{skill-name}/SKILL.md
```

### phase 5: verify

verification checklist:

- [ ] decision trees intact and actionable
- [ ] no broken references to private tools
- [ ] enhancements section has alternatives for each tool
- [ ] frontmatter name matches filename
- [ ] no personal/private patterns leaked

## transformation patterns

### tool integration → enhancements

before (private):
```markdown
## tool integration

| tool | command | purpose |
|------|---------|---------|
| layer | `layer .` | understand architecture |
| outline | `outline --callers=X` | trace dependencies |
| trails | `trails trail record` | persist context |
```

after (public):
```markdown
## enhancements (optional)

These CLI tools provide automation but are not required:

| tool | command | alternative |
|------|---------|-------------|
| layer | `layer .` | Read package.json files, trace imports manually |
| outline | `outline --callers=X` | Use grep to find function references |
| trails | `trails trail record` | Manual notes |
```

### inline CLI references

before:
```markdown
### phase 1: explore
```bash
layer .                    # architecture
outline --callers=X src/   # dependencies
```
```

after:
```markdown
### phase 1: explore
```bash
# understand architecture
# - read package.json for dependencies
# - check directory structure

# trace dependencies
# - grep for function/import references
# - or use IDE "find references"
```
```

### workflow commands

before:
```markdown
```bash
verify --format=summary    # run tests
linear issue view ARB-123  # get context
```
```

after:
```markdown
```bash
# run tests using your test runner
npm test
# or: pnpm test, yarn test, pytest, etc.

# get issue context from your issue tracker
# check the issue description and comments
```
```

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| reverse sync | public changes lost | always private → public |
| include non-portable orchestration | broken without infrastructure | exclude auto (has no portable bootstrap) |
| strip decision trees | removes core value | preserve all decision trees |
| vague alternatives | "use something else" | specific alternative commands |
| include secrets | security risk | redact or exclude |
| sync too often | churn | monthly or significant changes |
| forget enhancements | users can't enhance | always add section |

## quality checklist

before committing public version:

- [ ] all decision trees preserved
- [ ] all concrete values preserved
- [ ] all anti-patterns preserved
- [ ] no private CLI commands without alternatives
- [ ] enhancements section present (if any tools referenced)
- [ ] frontmatter description updated
- [ ] no personal patterns (voice, accounts, secrets)
- [ ] skill is self-contained and actionable

## references

- [../public/README.md](../public/README.md) - public skills documentation
