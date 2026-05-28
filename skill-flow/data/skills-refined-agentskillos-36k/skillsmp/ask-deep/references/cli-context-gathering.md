# CLI context gathering

patterns for using CLI tools to inform questions.

## before asking

gather context to avoid asking about discoverable things:

```bash
# understand architecture
layer .

# map relevant area
fd -e ts . src/relevant | outline -c

# recent changes
git log --oneline -10
outline --diff=HEAD~3

# find patterns
outline --search=patternName src/
```

## during conversation

when user mentions something, verify:

| user says | run |
|-----------|-----|
| "the auth module" | `outline --callers=authenticate src/auth/` |
| "like the reaction agent" | `fd -e ts . convex/agents \| outline -c --search=reaction` |
| "recent changes to X" | `outline --diff=HEAD~5 --search=X` |
| "related issues" | `linear issue list --team X --state "In Progress"` |
| "what we discussed" | `slack search "topic" --limit 10` |

report findings, then ask refined questions.

## tool → question mapping

### layer → architecture questions

```bash
layer .
```

informs:
- "should this live in package X or Y?"
- "which layer owns this responsibility?"
- "any cycle concerns?"

### outline → implementation questions

```bash
outline src/area/ --stats
outline --callers=functionName
outline --callees=functionName
```

informs:
- "who else uses this?"
- "what would break if we change this?"
- "which pattern should we follow?"

### git → context questions

```bash
git log --oneline -10 --all -- path/
git blame path/file.ts
outline --diff=HEAD~5
```

informs:
- "recent work on this area?"
- "who has context?"
- "what changed that might relate?"

### linear → coordination questions

```bash
linear issue list --team X --state "Todo"
linear issue view ISSUE-123
```

informs:
- "related work in progress?"
- "any blockers we should know about?"
- "who else is touching this?"

### slack → history questions

```bash
slack search "topic" --limit 20
slack dm history --user luke --limit 10
```

informs:
- "prior discussions about this?"
- "any decisions already made?"
- "context from earlier threads?"

## question enhancement

### before
```yaml
question: "where should this code live?"
options:
  - "src/utils"
  - "src/lib"
  - "new module"
```

### after running `layer .`
```yaml
question: "found 3 packages: core, utils, lib. where should this live?"
options:
  - label: "core (Recommended)"
    description: "depends on nothing, high-level abstractions"
  - label: "utils"
    description: "shared helpers, leaf node"
  - label: "lib"
    description: "external integrations, has dependencies"
```

### before
```yaml
question: "what pattern should we follow?"
options:
  - "new pattern"
  - "existing pattern"
```

### after running `outline --search=similar`
```yaml
question: "found existing pattern in auth/middleware.ts:45. should we follow it?"
options:
  - label: "yes, follow it (Recommended)"
    description: "consistent with established patterns"
  - label: "no, needs different approach"
    description: "explain why existing pattern doesn't fit"
  - label: "show me the code first"
    description: "need to see it before deciding"
```

## integration flow

1. user describes problem
2. run context tools
3. report findings briefly: "found X in path/to/file"
4. ask informed question with options shaped by findings
5. user answers
6. if answer mentions new thing, run more tools
7. repeat until synthesis

## anti-patterns

- **tool spam**: running every tool before any question
- **hiding findings**: not sharing what you discovered
- **asking anyway**: tool gave answer but still asking user
- **ignoring results**: findings don't influence question options
- **over-reporting**: dumping raw tool output instead of synthesis
