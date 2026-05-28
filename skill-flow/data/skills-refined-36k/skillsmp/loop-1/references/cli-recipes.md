# cli-recipes

common outline, layer, and linear patterns for loop workflows.

## outline recipes

### codebase overview

```bash
# full structure (pipe from fd)
fd -e ts -e tsx . src | outline -c --format=yaml

# specific directory
fd -e ts . src/auth | outline -c --format=yaml

# with stats
fd -e ts . src | outline -c --stats
```

### function tracing

```bash
# who calls this?
outline --callers=handleAuth src/**/*.ts --format=yaml

# what does this call?
outline --callees=handleAuth src/**/*.ts --format=yaml

# full call graph
outline --graph src/auth/*.ts --format=mermaid
```

### complexity analysis

```bash
# find complex functions
outline --complexity --min-complexity=15 src/**/*.ts --format=yaml

# budget-constrained output
fd -e ts . src | outline -c --budget=500
```

### dead code

```bash
# unused exports
outline --unused src/**/*.ts --format=yaml
```

### PR review

```bash
# what changed structurally?
outline --pr=123 --format=yaml

# or by URL
outline --pr=https://github.com/owner/repo/pull/123

# diff between branches
outline --diff=main..feature --format=yaml
```

## layer recipes

### package structure

```bash
# monorepo overview
layer . --format=mermaid

# json for parsing
layer . --format=json --quiet
```

### cycle detection

```bash
# check for cycles
layer . --check-cycles

# if cycles found, details:
layer . --check-cycles --format=json | jq '.cycles'
```

### dependency analysis

```bash
# what depends on auth?
layer . --dependents="packages/auth" --format=mermaid

# focus on specific area
layer . --focus="packages/core" --depth=2 --format=mermaid
```

### file-level

```bash
# file dependencies (not packages)
layer . --mode=files --format=mermaid

# files only (no content)
layer . --mode=files --files-only
```

## linear recipes

### issue workflow

```bash
# view issue
linear issue view ARB-456 --json --quiet | jq '{id, title, state: .state.name}'

# list my issues
linear issue list --assignee luke --state "In Progress" --json --quiet

# update state
linear issue edit ARB-456 --state "In Review"
```

### comments

```bash
# add comment
linear comment create -i ARB-456 -b "Progress: completed step 3/7"

# list comments
linear comment list ARB-456 --json --quiet | jq '.[-3:]'
```

### workspace-aware

```bash
# spottedinprod workspace
linear issue view SIP-123 --workspace spottedinprod

# luke-labs (default)
linear issue list --team ARB
```

## combined patterns

### context gathering

```bash
# for copilot packet
{
  echo '{"codebase":'
  layer . --format=json --quiet
  echo ',"issue":'
  linear issue view ARB-456 --json --quiet
  echo '}'
} | jq -s '.[0] * .[1]'
```

### change analysis

```bash
# what files changed + their structure
git diff --name-only HEAD~1 | xargs outline -c --format=yaml
```

### pre-PR check

```bash
# structure diff
outline --diff=main --format=text

# cycles
layer . --check-cycles

# tests
verify --format=summary
```

### notify on changes

```bash
# structural changes to slack
outline --diff=HEAD~1 --format=text | slack dm send --user luke
```

## pipes

### outline → linear

```bash
# add codebase context to issue
fd -e ts . src/auth | outline -c --format=text | \
  format linear | \
  linear comment create -i ARB-456
```

### layer → copilot

```bash
# inject architecture into prompt
copilot -p --model gemini-3-pro "
Architecture: $(layer . --format=json --quiet)
Question: where should I add the new auth middleware?
"
```

### verify → slack

```bash
# test results to DM
verify --format=summary | slack dm send --user luke
```

## anti-patterns

- **raw grep over outline**: use outline for code structure
- **manual dep tracking**: use layer for dependencies
- **forgetting -c flag**: always cache outline results
- **prose over JSON**: use --format=json for parsing
- **ignoring workspace**: always specify for non-default
