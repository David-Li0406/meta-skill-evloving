# Dependencies in Beads

Dependencies control the order of work and what shows up in `bd ready`.

## Basic Usage

```bash
# A is blocked by B (B must complete first)
bd dep add A B

# Remove dependency
bd dep remove A B

# See what's blocking an issue
bd dep list ID
```

## MCP Usage

```python
# Add dependency (issue_id is blocked by depends_on_id)
mcp__beads__dep(issue_id="A", depends_on_id="B")

# Create issue with inline dependency
mcp__beads__create(
  title="Build login UI",
  deps=["blocks:API-ID"]  # Blocked by API-ID
)
```

## How It Works

- `bd ready` only shows issues with NO open blockers
- When you close a blocker, dependent issues become ready
- Creates natural "waves" of parallelizable work

## Example: Feature with Dependencies

```bash
# Create issues
bd create "Design auth flow" --priority 1
bd create "Implement login API" --priority 1
bd create "Build login UI" --priority 1
bd create "Add tests" --priority 2

# Wire dependencies
bd dep add IMPL-ID DESIGN-ID     # API blocked by design
bd dep add UI-ID DESIGN-ID       # UI blocked by design
bd dep add TESTS-ID IMPL-ID      # Tests blocked by API
bd dep add TESTS-ID UI-ID        # Tests blocked by UI
```

This creates:
```
Wave 1: Design (ready now)
Wave 2: API + UI (ready after design)
Wave 3: Tests (ready after API + UI)
```

## Common Patterns

### Sequential Work
```bash
bd dep add step2 step1
bd dep add step3 step2
# Creates: step1 -> step2 -> step3
```

### Fan-out (one blocks many)
```bash
bd dep add taskA setup
bd dep add taskB setup
bd dep add taskC setup
# Creates: setup -> (taskA, taskB, taskC in parallel)
```

### Fan-in (many block one)
```bash
bd dep add final taskA
bd dep add final taskB
bd dep add final taskC
# Creates: (taskA, taskB, taskC) -> final
```

### Diamond Pattern
```bash
bd dep add middle1 start
bd dep add middle2 start
bd dep add end middle1
bd dep add end middle2
# Creates: start -> (middle1, middle2) -> end
```

## File Conflict Sequencing

When tasks touch the same files, add dependencies to prevent merge conflicts:

```bash
# Both tasks modify styles.css
bd dep add header-styles footer-styles
# Now they'll run sequentially instead of in parallel
```

Common conflict points:
- Shared styles (`styles.css`, `theme.ts`)
- Route configuration (`routes.tsx`, `App.tsx`)
- State management (`store.ts`, `context.tsx`)
- Shared types (`types.ts`, `interfaces.ts`)

## Tips

- Don't over-depend - only add when order truly matters
- Use for merge conflict prevention (issues touching same files)
- Check `bd blocked` to see what's waiting
