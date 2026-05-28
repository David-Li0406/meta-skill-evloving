---
name: issue-context
description: This skill should be used when enriching Linear issues with intelligent codebase context, architecture diagrams, and agent-ready prompts. Use for preparing issues for implementation, transforming vague tickets into rich specifications that coding agents can execute immediately.
---

# issue context enrichment

transform Linear issues from vague tickets into rich, context-aware specs. the trinity: `git` → `layer` → `outline` → `linear`.

## when to use

| use | skip |
|-----|------|
| preparing issue for implementation | issue already well-specified |
| adding codebase context to ticket | pure research (use `/map` or Explore) |
| creating agent-ready prompts | creating new issues (use `/linear`) |
| batch auditing issues | |

## philosophy

| principle | application |
|-----------|-------------|
| evidence-first | cite files you actually read, include file:line references |
| idempotent comments | tag comments with hidden markers and skip duplicates |
| minimal diagrams | 5-15 nodes, prune to issue-relevant paths |
| agent-ready | prompts include steps, constraints, and validation |
| graceful fallbacks | if a tool is missing, use rg/git/manual mapping |

## outputs (comment contract)

two Linear comments per issue, each with hidden markers:

- analysis: `<!-- issue-context:analysis -->`
- agent prompt: `<!-- issue-context:agent-prompt -->`

if markers already exist, update or add a short delta comment instead of reposting full blocks.

## decision tree: enrichment depth

```
How complex is the issue?
├── Simple (bug fix, single file)
│   ├── Phase 1: quick issue analysis
│   ├── Phase 2: git blame on specific file
│   ├── Skip: diagrams (not needed)
│   └── Output: minimal agent prompt
├── Moderate (feature, 2-5 files)
│   ├── All phases 1-5
│   ├── Phase 4: 1 architecture diagram
│   └── Output: full analysis + agent prompt
├── Complex (architecture, cross-cutting)
│   ├── All phases 1-5
│   ├── Phase 4: 2-3 diagrams (arch, flow, state)
│   └── Output: detailed analysis + rich agent prompt
└── Epic/Infrastructure
    ├── Fetch parent/child issues
    ├── All phases with extended git audit
    ├── Phase 4: system-level diagrams
    └── Output: comprehensive spec
```

## decision tree: diagram selection

```
What does the issue touch?
├── Data transformation
│   └── Sequence diagram (flow of data)
├── Component interaction
│   └── Flowchart (component boundaries)
├── State changes
│   └── State diagram (transitions)
├── System architecture
│   └── C4/layer diagram (dependencies)
├── API changes
│   └── Sequence + entity diagram
└── Multiple areas
    └── Combine relevant diagrams (max 3)
```

## decision tree: repo identification

```
How to find the repo?
├── Issue has file paths → Extract repo from path
├── Team prefix known
│   ├── ARB- → ~/Developer/arbor/arbor-xyz
│   ├── KUM- → ~/Developer/kumori/kumori-xyz
│   ├── SIP- → ~/Developer/spottedinprod/sip
│   └── etc. (see repo hints)
├── Description mentions repo → Use that
└── Unknown → Ask user before proceeding
```

## decision tree: prompt template selection

```
What kind of work?
├── Bugfix or regression
│   └── Bugfix template (minimal repro + suspected root)
├── Feature or enhancement
│   └── Feature template (acceptance criteria + integration points)
├── Refactor or cleanup
│   └── Refactor template (invariants + coverage plan)
└── Infra or migration
    └── Infra template (rollback + risk checklist)
```

## workflow

### phase 0: pre-flight

before starting:
1. `linear issue view ISSUE_ID --json` - capture title, description, state, labels
2. `linear comment list ISSUE_ID --json` - check for existing markers
3. check parent/sub issues - fetch parent for infra context
4. identify repo location (see repo hints below)
5. skip or delta-update if analysis already exists

### phase 1: issue analysis

```bash
linear issue view ISSUE-123
linear issue view ISSUE-123 --json | jq 'keys'
```

parse requirements, identify code areas, and extract constraints:
- acceptance criteria and success signals
- impacted users or systems
- unknowns that need clarification

for sub-issues, fetch parent for architecture context.

### phase 2: git audit

```bash
git log --oneline --since="4 weeks ago" --all -- relevant/path/
git log --oneline --grep="ISSUE_ID" --all
git blame relevant/file.ts
git show --stat COMMIT_HASH
outline --diff=HEAD~5
```

understand recent progress, who has context, related commits.

### phase 3: codebase mapping

```bash
rg -n "keyword|endpoint|component" src
rg -l "keyword|endpoint|component" src | outline -c --format=yaml
layer .
fd -e ts . src/relevant | outline -c --stats
outline --callers=functionName
```

find patterns, entry points, dependencies.

### phase 4: diagrams

create architecture and data flow diagrams in mermaid. keep 5-15 nodes each.
use layer for structure, then prune and annotate by hand.

### phase 5: generate comments

two comments:
1. **analysis + diagrams**: human-readable with visualizations
2. **agent prompt**: structured XML for coding agents

see [references/comment-templates.md](references/comment-templates.md).

### phase 6: post to Linear

```bash
linear comment create -i ISSUE_ID -b "$ANALYSIS"
linear comment create -i ISSUE_ID -b "$AGENT_PROMPT"
```

verify posting and markers:
```bash
linear comment list ISSUE_ID --json | jq -r '.[].body' | rg "issue-context:"
```

## linear CLI integration details

**issue view and field extraction**

```bash
linear issue view $ISSUE_ID --json | jq 'keys'
linear issue view $ISSUE_ID --json | jq '{id, identifier, title, state: .state.name}'
linear issue view $ISSUE_ID --json | jq '{labels: [.labels[].name], assignee: .assignee.name}'
```

field names can vary by CLI version. always inspect `keys` first.

**comment idempotency**

```bash
# find existing issue-context comments
linear comment list $ISSUE_ID --json | jq -r '.[].body' | rg "issue-context:"
```

**issue URLs**

```
https://linear.app/$WORKSPACE_SLUG/issue/$ISSUE_ID
```

## codebase context gathering workflow

1. **extract keywords** from title/description (nouns, endpoints, UI surfaces).
2. **find entrypoints** with `rg` (routes, mutations, handlers, components).
3. **trace call chains** with `outline --callers/--callees` for key functions.
4. **map dependencies** with `layer` to identify which packages to touch.
5. **validate patterns** by opening files, capturing real examples and tests.

```bash
rg -n "keyword|endpoint" src
rg -l "keyword" src | outline -c --format=yaml
outline --callers=targetFunction src/**/*.ts
layer . --mode=packages --format=mermaid
```

## architecture diagram generation

workflow:
1. generate a base graph with `layer` or `outline --graph`.
2. prune to the 5-15 most relevant nodes.
3. rename nodes to match domain language from the issue.
4. annotate with direction and data types where useful.

```bash
layer . --mode=packages --format=mermaid > /tmp/arch.mmd
layer . --focus="packages/web" --depth=2 --format=mermaid > /tmp/web.mmd
outline --graph --format=mermaid src/**/*.ts > /tmp/callgraph.mmd
```

see [references/diagram-guide.md](references/diagram-guide.md) for templates.

## agent-ready prompt templates

use XML with CDATA for code. keep it actionable and unambiguous.

### template: bugfix (minimal)

```xml
<agent_prompt issue="ISSUE-ID" type="bugfix">
  <context>
    <summary>one-line description of the bug</summary>
    <repo>repo-name</repo>
  </context>
  <bug>
    <symptom>what breaks, where, for whom</symptom>
    <repro>steps to reproduce</repro>
    <suspected_root>file and function to inspect first</suspected_root>
  </bug>
  <files_to_modify>
    <file>path/to/file.ts</file>
  </files_to_modify>
  <validation>
    <test>verify --format=summary</test>
  </validation>
</agent_prompt>
```

### template: feature (full)

```xml
<agent_prompt issue="ISSUE-ID" type="feature">
  <context>
    <summary>one-line feature goal</summary>
    <repo>repo-name</repo>
  </context>
  <acceptance_criteria>
    <item>behavior or UI change required</item>
    <item>edge case to cover</item>
  </acceptance_criteria>
  <integration_points>
    <item file="path/to/entry.ts">where new behavior is wired</item>
  </integration_points>
  <existing_pattern file="path/to/pattern.ts" lines="12-40">
    <description>pattern to follow</description>
    <code_snippet><![CDATA[...]]></code_snippet>
  </existing_pattern>
  <implementation_steps>
    <step order="1" file="path/to/file.ts">add schema/logic</step>
    <step order="2" file="path/to/file.tsx">update UI</step>
  </implementation_steps>
  <validation>
    <test>verify --format=summary</test>
    <test>targeted test command</test>
  </validation>
</agent_prompt>
```

### template: refactor or infra

```xml
<agent_prompt issue="ISSUE-ID" type="refactor">
  <context>
    <summary>what is being refactored and why</summary>
  </context>
  <constraints>
    <invariant>behavior must not change</invariant>
    <invariant>performance baseline preserved</invariant>
  </constraints>
  <risk>
    <area>migration or data risk</area>
    <rollback>rollback plan or guard</rollback>
  </risk>
  <validation>
    <test>verify --format=summary</test>
  </validation>
</agent_prompt>
```

see [references/agent-prompt-templates.md](references/agent-prompt-templates.md) for full variants.

## quick start

```bash
# single issue
linear issue view ARB-123
# run phases 1-5, generate comments

# batch mode
linear issue list --team ARB --state "Todo" --assignee luke --json
# process each issue
```

## input recognition

| input | interpretation |
|-------|----------------|
| `ARB-123` or `SIP-364` | single issue ID |
| `--team ARB --state "Todo"` | filter/batch mode |
| `"fix auth bug"` | natural language search |
| linear URL | extract issue ID |

## tool integration

| tool | command | purpose |
|------|---------|---------|
| linear | `linear issue view`, `linear comment create` | issue management, comment posting |
| outline | `outline --callers`, `outline --callees` | AST-based codebase mapping (10-50x token savings) |
| layer | `layer . --format=mermaid` | dependency graphs, diagrams, cycle detection |
| git | `git log`, `git blame` | repo history, recent progress |
| rg | `rg -n "keyword"` | keyword search and file discovery |
| jq | `jq` | parse Linear JSON output |
| trails | `trails trail record` | enrichment history persistence |

see [references/cli-patterns.md](references/cli-patterns.md).

### trails integration

persist enrichment events for tracking and pattern analysis:

```bash
# record enrichment start
TRACE=$(trails trail record --agent claude --new-trace --action started \
  --task "issue-context: $ISSUE_ID" --json -q | jq -r '.trace_id')

# record enrichment completion
trails trail record --agent claude --trace-id $TRACE \
  --action completed --task "issue-context: $ISSUE_ID enriched" \
  --confidence $CONFIDENCE --json -q

# query enrichment history for an issue
trails trail replay --format json | jq '.[] | select(.task | contains("'$ISSUE_ID'"))'

# find all enrichments in last 7 days
trails trail replay --since 7d --format summary | grep "issue-context"
```

**trails enables**:
- tracking which issues were enriched
- measuring enrichment quality over time
- correlating enrichment with implementation success

## repo hints

| workspace | team | repos |
|-----------|------|-------|
| luke-labs | ARB | `~/Developer/arbor/arbor-xyz` |
| luke-labs | KUM | `~/Developer/kumori/kumori-xyz` |
| luke-labs | KOT | `~/Developer/koto/koto-xyz` |
| luke-labs | WEB | `~/Developer/webs/webs-xyz` |
| luke-labs | SIN | `~/Developer/sine/sine-xyz` |
| spottedinprod | SIP | `~/Developer/spottedinprod/sip` (web), `sip-api` (api) |

if repo unknown, check issue description for paths or ask.

## timing

| phase | duration |
|-------|----------|
| 0: pre-flight | 1-2 min |
| 1: issue analysis | 2-3 min |
| 2: git audit | 2-3 min |
| 3: codebase mapping | 3-5 min |
| 4: diagrams | 2-3 min |
| 5: comment gen | 2-3 min |
| 6: post | <1 min |
| **total** | ~15 min |

complex issues with multiple repos take longer.

## quality checklist

- [ ] URLs use workspace slug (not team prefix)
- [ ] git audit done - recent progress documented
- [ ] files actually read - patterns verified, not guessed
- [ ] diagrams digestible - 5-15 nodes each
- [ ] file paths correct - verified paths exist
- [ ] line numbers accurate - referenced after reading
- [ ] XML well-formed - valid structure, CDATA for code
- [ ] mermaid renders - tested syntax
- [ ] comment markers included and idempotent
- [ ] prompt includes acceptance criteria and validation commands
- [ ] open questions captured if blockers remain

## references

- [references/cli-patterns.md](references/cli-patterns.md) - command patterns
- [references/diagram-guide.md](references/diagram-guide.md) - mermaid templates
- [references/comment-templates.md](references/comment-templates.md) - output formats
- [references/agent-prompt-templates.md](references/agent-prompt-templates.md) - prompt variants
- [references/batch-mode.md](references/batch-mode.md) - processing multiple issues

## scripts

- [scripts/audit-issue.sh](scripts/audit-issue.sh) - fetch issue and detect context
- [scripts/post-comments.sh](scripts/post-comments.sh) - post comments to Linear

## concrete values (sourced)

| value | meaning | source |
|-------|---------|--------|
| diagram nodes: 5-15 | readable without overwhelming | `references/diagram-guide.md` (UX heuristic) |
| max diagrams per issue: 3 | avoid information overload | SKILL.md decision tree line 77 |
| git history window: 4 weeks | sufficient recent context | `references/cli-patterns.md:123,126,129,138` |
| outline diff range: HEAD~5 | reasonable recent commit window | SKILL.md workflow phase 2 |
| comments fetched limit: 20 | Linear CLI `--comments` default | `linear issue view --help` |
| issue list default limit: 30 | Linear CLI default | `linear issue list --help --limit` |
| git log head: 40 lines | quick scan without noise | `references/cli-patterns.md:123` |
| outline token savings: 10-50x | vs reading full files | `references/cli-patterns.md:7` |
| layer depth default: 1 | traversal hops for focus | `layer --help` (`-d, --depth`) |
| outline trace depth: 1-2 | callers of callers | `outline --help` (`--trace-depth`) |
| phase 0-6 total: ~15 min | typical enrichment time | SKILL.md timing table (heuristic) |
| comment marker: `<!-- issue-context:X -->` | idempotency tag format | SKILL.md outputs section |
| Linear URL format: `linear.app/$WORKSPACE_SLUG/issue/$ID` | correct URL structure | `references/cli-patterns.md:113-114` |

## anti-patterns

- **guessing file paths**: verify before citing
- **duplicate comments**: check existing first
- **massive diagrams**: target 5-15 nodes
- **skipping git audit**: recent context is critical
- **citing patterns blind**: read the file first
- **starting without repo**: identify location first
- **posting raw tool output**: curate and summarize
- **missing markers**: cannot dedupe or update
- **vague prompts**: include concrete steps and tests
