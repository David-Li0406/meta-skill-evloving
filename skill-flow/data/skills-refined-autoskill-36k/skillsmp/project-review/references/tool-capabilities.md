# tool capabilities

full feature matrix for development tools. use for audit comparisons.

## outline

AST-based codebase exploration. 10-50x token savings vs reading files.

| feature | command | use case |
|---------|---------|----------|
| basic structure | `fd -e ts . src \| outline -c` | understand codebase |
| caller tracing | `outline --callers=funcName` | who uses this function? |
| callee tracing | `outline --callees=funcName` | what does this call? |
| dead code | `outline --unused` | find unused exports |
| complexity | `outline --complexity --min=15` | find complex functions |
| call graph | `outline --graph --format=mermaid` | visualize dependencies |
| diff mode | `outline --diff=HEAD~1` | structural changes |
| PR mode | `outline --pr=123` | review PR impact |
| stats | `outline --stats` | codebase dashboard |

**underutilized features:**
- `--unused` for cleanup sessions
- `--diff` for understanding recent changes
- `--pr` for code review

## layer

package/module dependency analysis.

| feature | command | use case |
|---------|---------|----------|
| package deps | `layer .` | monorepo architecture |
| file deps | `layer . --mode=files` | file-level analysis |
| cycle detection | `layer . --check-cycles` | find circular deps |
| focus | `layer . --focus=pkg --depth=2` | analyze specific area |
| dependents | `layer . --dependents=lib` | what depends on this? |
| mermaid | `layer . --format=mermaid` | generate diagrams |

**underutilized features:**
- `--check-cycles` before refactoring
- `--dependents` before removing code
- `--focus` for understanding specific packages

## verify

unified test runner adapter.

| feature | command | use case |
|---------|---------|----------|
| summary | `verify --format=summary` | quick check |
| failures only | `verify --json --failures-only` | CI/agent |
| coverage | `verify --coverage` | coverage report |
| changed files | `verify --changed` | fast CI |

## linear

issue tracking CLI.

| feature | command | use case |
|---------|---------|----------|
| view issue | `linear issue view ARB-123` | check issue details |
| list issues | `linear issue list --team ARB` | see team work |
| create issue | `linear issue create --team ARB` | file new issue |
| add comment | `linear comment create -i ARB-123` | update issue |
| workspace | `--workspace spottedinprod` | target workspace |

**workspaces:**
- luke-labs: ARB, KUM, KOT, SIN, WEB (default)
- spottedinprod: SIP team

## prompts

prompt template management.

| feature | command | use case |
|---------|---------|----------|
| export | `prompts commands export /map` | get prompt content |
| show | `prompts commands show /map` | raw (no expansion) |
| list | `prompts commands list` | available prompts |
| search | `prompts commands search "tdd"` | find prompts |

**key prompts:**
- `/prime` - full context for any task
- `/map` - fresh session codebase understanding
- `/tdd` - test-driven development guidance

## agents

plan management.

| feature | command | use case |
|---------|---------|----------|
| create plan | `agents plan --project X --title Y` | start planning |
| review | `agents review project/date-slug` | check plan |

## roles

persona management for coding agents.

| feature | command | use case |
|---------|---------|----------|
| list | `roles list` | see all roles |
| export | `roles export jony` | get role content |
| groups | `roles group list` | composed personas |

**key roles:**
- `jony` - design reviews, simplification
- `margaret` - reliability, safety-critical
- `bret` - future tooling, interaction design
- `dieter` - minimalism, systematic design

## slack

messaging and workflows.

| feature | command | use case |
|---------|---------|----------|
| dm | `echo "msg" \| slack dm send --user luke` | notify user |
| channel | `slack channel history -c general` | read channel |
| search | `slack search messages -q "keyword"` | find messages |
| workflow | `slack workflow run --file playbook.yaml` | run workflow |
| workspace | `-w saya` | target workspace |

## messages

iMessage sending.

| feature | command | use case |
|---------|---------|----------|
| send | `messages send luke "done"` | notify |
| read | `messages read --from luke` | context |

## format

output formatting for different targets.

| feature | command | use case |
|---------|---------|----------|
| slack | `echo "**bold**" \| format slack` | mrkdwn conversion |
| linear | `outline \| format linear` | issue formatting |

## pipe patterns

common combinations:

```bash
# exploration chain
layer . --format=json | jq -r '.layers.leaf[]' | xargs outline

# PR review
outline --pr=123 --format=text | slack dm send --user luke

# test notify
verify --format=summary | slack dm send --user luke

# code to linear
fd -e ts . src | outline -c | format linear | linear comment create -i X
```

## audit checklist

when auditing tool usage:

- [ ] outline: using --callers/--callees for tracing?
- [ ] outline: using --unused for cleanup?
- [ ] outline: using --diff/--pr for reviews?
- [ ] layer: running --check-cycles before refactors?
- [ ] verify: using --changed for fast CI?
- [ ] linear: referencing issues in commits?
- [ ] prompts: using /prime, /map, /tdd?
- [ ] roles: adopting personas for review?
