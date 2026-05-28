# linear-sync

Linear workspace mapping and issue synchronization.

## philosophy

> "the issue is the source of truth"

Linear issues define scope. sync state bidirectionally.

## workspace mapping

| path pattern | workspace | flag |
|--------------|-----------|------|
| ~/Developer/arbor/* | luke-labs | (default) |
| ~/Developer/koto/* | luke-labs | (default) |
| ~/Developer/kumori/* | luke-labs | (default) |
| ~/Developer/sine/* | luke-labs | (default) |
| ~/Developer/webs/* | luke-labs | (default) |
| */spottedinprod/* | spottedinprod | `--workspace spottedinprod` |

## team mapping

| workspace | teams |
|-----------|-------|
| luke-labs | ARB, KOT, KUM, SIN, WEB |
| spottedinprod | SIP |

## issue selection

### priority order

1. in-progress assigned to me
2. highest priority in current sprint
3. backlog by priority

```bash
# in-progress first
linear issue list --team ARB --state "In Progress" --assignee luke --json --quiet

# if empty, next priority
linear issue list --team ARB --state "Todo" --priority 1 --json --quiet | jq '.[0]'
```

### issue context

```bash
# full issue details
linear issue view ARB-456 --json --quiet | jq '{
  id: .identifier,
  title: .title,
  description: .description,
  state: .state.name,
  priority: .priority,
  labels: [.labels[].name],
  parent: .parent.identifier
}'
```

## state transitions

| from | to | when |
|------|-----|------|
| Todo | In Progress | starting work |
| In Progress | In Review | PR created |
| In Review | Done | PR merged |
| In Progress | Blocked | HIL needed |

```bash
# start work
linear issue edit ARB-456 --state "In Progress"

# PR ready
linear issue edit ARB-456 --state "In Review"

# blocked
linear issue edit ARB-456 --state "Blocked"
```

## progress comments

```bash
# add progress update
linear comment create -i ARB-456 -b "$(cat << 'EOF'
## Progress Update

**Phase:** Implementation
**Step:** 3/7

**Completed:**
- Created schema migration
- Added API endpoint

**Next:**
- Write tests
- Update UI

**Confidence:** 8/10
EOF
)"
```

## linking

### commits

```bash
# reference in commit
git commit -m "feat(ARB-456): add user profile endpoint"
```

### PRs

```bash
# reference in PR
gh pr create --title "feat(ARB-456): user profile" --body "Closes ARB-456"
```

### branches

```bash
# branch naming
git checkout -b feat/ARB-456-user-profile
```

## queries

### my issues

```bash
# current sprint
linear issue list --assignee luke --state "In Progress,Todo" --json --quiet

# by team
linear issue list --team ARB --assignee luke --json --quiet
```

### blocked issues

```bash
linear issue list --state "Blocked" --assignee luke --json --quiet
```

### recent activity

```bash
# comments on issue
linear comment list ARB-456 --json --quiet | jq '.[-3:]'
```

## automation patterns

### on loop start

```bash
# 1. find next issue
ISSUE=$(linear issue list --team ARB --state "In Progress" --assignee luke --json --quiet | jq -r '.[0].identifier')

# 2. if none, pick from todo
[ -z "$ISSUE" ] && ISSUE=$(linear issue list --team ARB --state "Todo" --priority 1 --json --quiet | jq -r '.[0].identifier')

# 3. start work
[ -n "$ISSUE" ] && linear issue edit $ISSUE --state "In Progress"
```

### on completion

```bash
# 1. create PR
PR_URL=$(gh pr create --title "feat($ISSUE): $TITLE" --body "Closes $ISSUE")

# 2. update Linear
linear issue edit $ISSUE --state "In Review"
linear comment create -i $ISSUE -b "PR created: $PR_URL"

# 3. notify
echo "PR ready: $ISSUE - $PR_URL" | slack dm send --user luke
```

### on block

```bash
# 1. update state
linear issue edit $ISSUE --state "Blocked"

# 2. add context
linear comment create -i $ISSUE -b "Blocked: $REASON. Full context: $GIST_URL"

# 3. notify
messages send luke "HIL needed: $ISSUE - $GIST_URL"
```

## anti-patterns

- **working without issue**: always have Linear context
- **silent progress**: update Linear regularly
- **wrong workspace**: check path mapping
- **stale state**: sync on each loop iteration
