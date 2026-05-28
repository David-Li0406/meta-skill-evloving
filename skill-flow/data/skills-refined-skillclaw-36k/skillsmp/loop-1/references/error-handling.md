# error handling

when things break during long-horizon work.

## test failures

**don't just fix the test. understand why.**

```bash
# get details
verify --json --failures-only | jq '.failures[0]'

# check what changed
outline --diff=HEAD~3

# trace the failure
outline --callers=failingFunction
```

**investigation flow**:
1. is the test correct? (testing right behavior)
2. is the implementation correct? (doing right thing)
3. is there a race condition or timing issue?
4. is there a missing mock or stub?
5. is there an environment issue?

**when to check in with user**:
- test reveals design ambiguity
- multiple valid fixes, unclear which is right
- test was passing before your changes, now failing

## type errors

**types reveal design issues. trace to root cause.**

```bash
# run type check
pnpm typecheck 2>&1 | head -50

# find the type definition
outline --search=TypeName src/
```

**common causes**:
- missing prop in component
- wrong return type from function
- incompatible library versions
- circular dependency

**when to check in with user**:
- type system is fighting the design
- need to add `any` or `as` cast to proceed
- fix requires changing public interface

## build failures

**usually config or deps, not code.**

```bash
# check for missing deps
pnpm install

# check for config issues
cat tsconfig.json | jq '.compilerOptions'

# check for import issues
pnpm build 2>&1 | grep -i error
```

**common causes**:
- missing dependency
- wrong import path
- incompatible module format (ESM vs CJS)
- environment variable not set

**when to check in with user**:
- need to install new dependency
- need to change build config
- unclear which package version to use

## lint errors

**usually auto-fixable. if not, understand why.**

```bash
# auto-fix what's fixable
pnpm lint --fix

# see what's left
pnpm lint
```

**when to check in with user**:
- lint rule conflicts with implementation need
- unclear if rule should be disabled
- pattern doesn't match existing codebase

## runtime errors

**when code runs but fails.**

```bash
# check logs
npx convex logs --prod --history 20

# trace the error
outline --callers=failingFunction
```

**investigation flow**:
1. reproduce locally
2. add logging to trace
3. check edge cases
4. check external dependencies (APIs, DB)

## blocked situations

**when you can't proceed without input.**

check in with user:
- explain what's blocking
- explain what you've tried
- provide options if you have them

```
blocked: can't determine auth strategy

tried:
- looked at existing auth code
- checked clerk docs
- reviewed similar patterns in arbor

options:
1. use middleware approach (like arbor)
2. use HOC approach (like old pattern)
3. need more context on requirements

which direction?
```

## recovery patterns

### rollback

```bash
# see what changed
git log --oneline -5
git diff HEAD~N

# rollback if needed
git reset --soft HEAD~N  # keep changes staged
git reset --hard HEAD~N  # discard changes
```

### stash and restart

```bash
# save current state
git stash push -m "work in progress on feature"

# start fresh
git checkout main

# restore later
git stash pop
```

### checkpoint commits

when unsure, commit what you have:

```bash
git commit -m "WIP: checkpoint before risky change"
```

can always squash later.

## error handling anti-patterns

- **fixing without understanding**: symptom vs root cause
- **silently working around**: hiding problems
- **giving up too early**: some problems just need time
- **not checking in when blocked**: spinning instead of asking
- **not preserving state**: losing work when resetting
