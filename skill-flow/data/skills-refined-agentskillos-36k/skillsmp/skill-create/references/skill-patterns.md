# skill patterns and best practices

## core principles

| principle | pattern | why it matters |
|-----------|---------|----------------|
| decision trees first | pick archetype and size before writing | prevents mismatch and rework |
| explicit thresholds | use numbers for gates and sizing | reduces ambiguity |
| progressive disclosure | SKILL.md orchestrates, references hold depth | keeps top-level usable |
| tool integration | show real commands, not placeholders | makes skills executable |
| validation gates | run scripts until PASS | avoids shallow skills |

## decision tree patterns

- start with a single question and branching conditions
- include numeric thresholds (counts, limits, line targets)
- provide a default branch for unclear cases
- document hybrid choices explicitly

## concrete thresholds library

| item | target | use |
|------|--------|-----|
| trigger phrases | 3-6 | prevent overly broad skills |
| anti-triggers | 2-4 | avoid misuse |
| decision tree coverage | ~80% of common scenarios | depth signal |
| references depth | >= 50 lines each | avoid stub docs |
| script trigger | command used >= 2 times | reduce repetition |
| script trigger (complex) | > 120 chars or 3+ flags | avoid copy/paste errors |
| tool examples | 2+ commands | prove executability |
| simple size | 120-170 lines | narrow scope |
| medium size | 170-240 lines | multi-step scope |
| full size | 240-380 lines | complex or hybrid |

## tool integration patterns

| tool | use case | example |
|------|----------|---------|
| prompts | reusable prose or checklists | `prompts commands export /create-skill --json --quiet` |
| agents plan | record plan artifacts | `agents plan --project skills --title "create <skill>" --json --quiet` |
| rg | file discovery and lint | `rg -n "TODO" SKILL.md references` |
| validate-skill.sh | enforce structure | `./scripts/validate-skill.sh ~/.claude/skills/<skill>` |
| introspect-skill.sh | quick signal | `./scripts/introspect-skill.sh ~/.claude/skills/<skill>` |

## references hygiene

| check | pass condition | fix |
|-------|----------------|-----|
| every reference linked | all files in `references/` listed in SKILL.md | add missing links |
| no duplicated blocks | references contain deeper detail | move repeated text out of SKILL.md |
| no TODOs | placeholders removed | replace with content |
| skimmable structure | headings + short sections | add headers and tables |

## anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| vague trigger phrases | skill misfires or never runs | add 3-6 explicit phrases |
| prompt content embedded in SKILL.md | hard to reuse | move to prompts, link by alias |
| scripts missing | repeated commands copied | extract to scripts/ |
| no tool examples | skills feel theoretical | add 2+ command examples |
| validation skipped | quality unknown | run validation until PASS |

## examples

- workflow: deployments, code reviews, migrations
- tool: PDF split/merge, image transforms, API client invocations
- domain: schema guides, brand guidelines, policy playbooks
