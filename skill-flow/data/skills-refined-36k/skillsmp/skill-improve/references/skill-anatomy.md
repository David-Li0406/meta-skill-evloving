# skill anatomy

ideal structure, sizing, and quality signals for claude code skills.

## section order

skills follow a consistent structure. sections appear in this order:

| # | section | required | purpose |
|---|---------|----------|---------|
| 1 | frontmatter | yes | metadata: name, description with triggers |
| 2 | title + tagline | yes | one-line purpose statement |
| 3 | philosophy | recommended | principles table, quoted motto |
| 4 | when to use | yes | use/skip decision table |
| 5 | decision trees | yes | if/then control flow for common scenarios |
| 6 | concrete values | recommended | constants with sources |
| 7 | workflow | recommended | phased execution steps |
| 8 | tool integration | recommended | CLI commands with user's tools |
| 9 | anti-patterns | yes | pattern/problem/fix table |
| 10 | output contract | conditional | JSON schema (for chaining skills) |
| 11 | references | yes | links to reference files |

**optional sections** (position varies):
- modes (after decision trees, for multi-mode skills)
- lifecycle reporting (after workflow, for orchestration skills)
- error handling (after workflow, for complex skills)
- metaprompts (after references, for template-heavy skills)
- scripts (after references, for skills with scripts/)

## section sizing

| section | healthy | shallow | bloated |
|---------|---------|---------|---------|
| frontmatter | 3-5 lines | 2 lines (no triggers) | 10+ lines |
| title + tagline | 1-2 lines | missing tagline | 5+ lines |
| philosophy | 5-12 lines | 2 lines or missing | 20+ lines |
| when to use | 6-12 rows | 2 rows | 20+ rows |
| decision trees | 30-100 lines total | <15 lines | >150 lines |
| concrete values | 8-20 rows | 0-3 rows | 30+ rows |
| workflow | 40-120 lines | <20 lines | >200 lines |
| tool integration | 15-40 lines | 0-5 lines | >60 lines |
| anti-patterns | 6-12 rows | 0-3 rows | 20+ rows |
| output contract | 15-30 lines | stub or missing | >50 lines |
| references | 4-8 links | 0-2 links | >12 links |

**total SKILL.md targets by complexity:**

| complexity | line count | decision trees | references |
|------------|------------|----------------|------------|
| simple | 120-170 | 1-2 | 1-2 |
| medium | 170-240 | 3-5 | 2-4 |
| full-featured | 240-380 | 5-10 | 3-6 |
| orchestrator | 380-500 | 10-15 | 6-10 |

## section anatomy

### frontmatter

**healthy:**
```yaml
---
name: skill-name
description: This skill should be used when doing X. Triggers include "do X", "X this", "help with X", or when context suggests X is needed. Brief description of what it does.
---
```

**shallow:**
```yaml
---
name: skill-name
description: Does X.
---
```

**signals:**
- name matches folder name
- description starts with "This skill should be used when..."
- 3-6 trigger phrases in description
- description is 30-80 words

### title + tagline

**healthy:**
```markdown
# skill-name

one-line purpose statement. what problem it solves for whom.
```

**shallow:**
```markdown
# skill-name
```

**signals:**
- tagline is 10-20 words
- uses lowercase except acronyms
- no "This skill..." repetition from frontmatter

### philosophy

**healthy:**
```markdown
## philosophy

> "guiding principle in quotes"

| principle | application |
|-----------|-------------|
| evidence over vibes | every claim has a source |
| decision trees | express if/then logic |
| concrete values | cite constants with sources |
```

**shallow:**
```markdown
## philosophy

be thoughtful and thorough.
```

**signals:**
- quoted motto is memorable and actionable
- table has 4-7 principle rows
- principles map to observable skill behavior
- no vague "be good" platitudes

### when to use

**healthy:**
```markdown
## when to use

| use | skip |
|-----|------|
| user says "help with X" | task is simple one-liner |
| context shows X is needed | different skill handles it |
| periodic X audits | purely cosmetic changes |
| X identified gaps | deletion or deprecation |
```

**shallow:**
```markdown
## when to use

use when you need to do X. skip when you don't.
```

**signals:**
- table format with use/skip columns
- 4-8 rows minimum
- specific triggers, not vague conditions
- anti-triggers prevent misfiring

### decision trees

**healthy:**
```markdown
## decision tree: scenario name

```
What should I do?
├── Condition A?
│   ├── Sub-condition A1?
│   │   └── Action A1
│   └── Sub-condition A2?
│       └── Action A2
├── Condition B?
│   └── Action B (with threshold N)
└── Default?
    └── Default action
```
```

**shallow:**
```markdown
## decision tree

consider your options and choose wisely.
```

**gold standard example (loop skill):**
```
What mode should I use?
├── Linear issue provided/detected?
│   ├── Issue ID in prompt → issue-mode
│   ├── git branch matches issue pattern → issue-mode
│   └── Path matches workspace → check for in-progress issues
├── Fresh repo with no context?
│   ├── No .loop.json → bootstrap-mode (Phase 0 first)
│   ├── .loop.json exists → task-mode with config
│   └── README/CONTRIBUTING exists → read first
├── Arbitrary task?
│   └── task-mode (pure autonomous execution)
└── Unclear?
    └── bootstrap-mode to gather context
```

**signals:**
- 3-15 decision trees covering common scenarios
- each tree has 3+ branches
- branches end in concrete actions
- default/fallback path always present
- thresholds and conditions are specific

**common decision tree types:**
- mode selection (what mode to use)
- routing (where to send task)
- validation (is output ready)
- scope (how deep to go)
- escalation (when to ask for help)
- tool selection (which tool to use)

### concrete values

**healthy:**
```markdown
## concrete values

| value | meaning | source |
|-------|---------|--------|
| pattern freshness: < 7 days | treat as fresh | `scripts/bootstrap.sh:42` |
| confidence threshold: >= 8 | proceed without asking | `references/routing.md` |
| reference depth: >= 50 lines | substantive content | skill-create validation |
| TOAST_DURATION: 4000ms | visible toast time | sonner/src/index.tsx:42 |
```

**shallow:**
```markdown
## values

- duration should be reasonable
- threshold depends on context
```

**signals:**
- table format with value/meaning/source columns
- 5-15 rows with specific numbers
- sources are file paths or URLs
- values are actionable, not ranges

### workflow

**healthy:**
```markdown
## workflow

### phase 1: name

brief description of phase goal.

```bash
# command with comment
command --flag value
```

output: what this phase produces

### phase 2: name

...
```

**shallow:**
```markdown
## workflow

1. do the thing
2. check the thing
3. done
```

**signals:**
- 3-7 phases with descriptive names
- each phase has goal, commands, output
- commands are real and runnable
- phases connect (output of N feeds N+1)
- graceful degradation noted for optional tools

### tool integration

**healthy:**
```markdown
## tool integration

```bash
# exploration
layer /path/to/project          # architecture overview
outline src/ --stats            # code structure

# validation
verify --format=summary         # run tests
copilot -p "validate X"    # external check

# documentation
ref_search_documentation "X"    # search docs
ref_read_url "https://..."      # read specific page
```
```

**shallow:**
```markdown
## tools

use appropriate tools.
```

**signals:**
- references user's actual tools (layer, outline, verify, etc.)
- commands are complete and runnable
- comments explain purpose
- 3+ distinct tool examples
- integrates with user's workflow from ~/AGENTS.md

### anti-patterns

**healthy:**
```markdown
## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| web-scrape only | misses implementation details | read source code |
| philosophy without action | no executable decisions | add decision tree |
| generic values | vague without source | cite exact constants |
| skip validation | no proof of quality | require pair review |
| fire-and-forget | progress invisible | update TodoWrite + commits |
```

**shallow:**
```markdown
## anti-patterns

don't do bad things.
```

**signals:**
- table format with pattern/problem/fix columns
- 5-12 rows with specific patterns
- fixes are concrete actions
- patterns are observable mistakes
- problems explain why it matters

### output contract

**healthy:**
```markdown
## output contract

```json
{
  "mode": "consult | delegate | review",
  "status": "success | partial | blocked | failed",
  "summary": "50-200 words",
  "confidence": 8,
  "artifacts": [
    { "type": "file", "path": "path/to/file", "status": "created" }
  ],
  "sources": {
    "prompts": ["/tdd"],
    "files_read": ["src/auth.ts:10-50"]
  },
  "verification": {
    "tests_passed": true
  }
}
```
```

**shallow:**
```markdown
## output

returns a result.
```

**signals:**
- complete JSON schema with types
- required fields documented
- example values shown
- matches ~/.system/output-contract.md

### references

**healthy:**
```markdown
## references

- [references/evaluation-rubric.md](references/evaluation-rubric.md) - scoring criteria
- [references/research-patterns.md](references/research-patterns.md) - source methodology
- [references/artifact-examples.md](references/artifact-examples.md) - validation samples
```

**shallow:**
```markdown
## references

see references folder.
```

**signals:**
- each reference linked with markdown syntax
- brief description after link
- 3-8 references for full-featured skills
- all referenced files exist (no dead links)
- each reference file is >= 50 lines

## reference file anatomy

each reference should follow this structure:

```markdown
# reference-name

one-line purpose.

## section 1

content with tables, code blocks, examples.

## section 2

more detailed content.

## examples

concrete examples with good/bad comparisons.
```

**reference sizing:**
- minimum: 50 lines
- healthy: 80-150 lines
- deep: 150-300 lines

**reference types:**

| type | content | examples |
|------|---------|----------|
| rubric | scoring criteria with examples | evaluation-rubric.md |
| patterns | methodology with steps | research-patterns.md |
| templates | reusable prompts/schemas | prompt-templates.md |
| checklists | validation steps | security-checklist.md |
| examples | sample artifacts | artifact-examples.md |
| recipes | command sequences | cli-recipes.md |

## completeness checklist

### structure (must have)

- [ ] frontmatter with name and description (3-6 triggers)
- [ ] title + tagline (10-20 words)
- [ ] when to use table (4+ rows each column)
- [ ] at least 3 decision trees with branches
- [ ] anti-patterns table (5+ rows with fixes)
- [ ] references section with links

### depth (should have)

- [ ] philosophy with principles table (4-7 rows)
- [ ] concrete values table (5+ with sources)
- [ ] workflow with 3+ phases
- [ ] tool integration examples (3+ commands)
- [ ] each reference file >= 50 lines

### quality (health signals)

- [ ] decision trees have default paths
- [ ] values cite specific sources (file:line or URL)
- [ ] commands are runnable (not pseudocode)
- [ ] anti-pattern fixes are actionable
- [ ] no dead links in references
- [ ] no TODO/FIXME markers remaining
- [ ] voice follows conventions (lowercase, tables, terse)

### integration (for orchestration skills)

- [ ] output contract with JSON schema
- [ ] lifecycle reporting events
- [ ] pair skill integration patterns
- [ ] error handling decision tree
- [ ] graceful degradation for optional tools

## quick assessment

```
Skill: [name]
Date: [YYYY-MM-DD]

Structure:
- [ ] frontmatter complete
- [ ] when to use table
- [ ] decision trees (count: ___)
- [ ] anti-patterns table
- [ ] references linked

Depth:
- [ ] values sourced
- [ ] workflow phased
- [ ] tools integrated
- [ ] references substantive

Line count: ___
Complexity tier: [simple/medium/full/orchestrator]
Health: [healthy/needs-work/shallow]
```

## common gaps by skill type

| skill type | common gaps |
|------------|-------------|
| workflow | missing phases, no tool integration |
| tool | missing CLI examples, no error handling |
| domain | missing concrete values, vague decision trees |
| meta | missing self-application, circular validation |
| integration | missing error handling, no auth patterns |

## evolution path

```
shallow → functional → healthy → mature

shallow:
- 80-120 lines
- no decision trees
- generic values
- stubs for references

functional:
- 120-180 lines
- 1-2 decision trees
- some values with sources
- references exist but thin

healthy:
- 180-280 lines
- 3-5 decision trees
- values with sources
- references >= 50 lines each

mature:
- 280-400 lines
- 5-10 decision trees
- comprehensive values
- deep references
- external validation evidence
```
