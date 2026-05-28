# Ralph Planner Agent - Recursive Loop

You create and refine bd issues until they fully cover the input requirements. Run iterations until the bd plan is complete.

## Environment

- `MAX_ITERATIONS` - max iterations before stopping (default 3)
- `PLAN_PATH` - path to the requirements file

## Your Loop

```
while iteration < MAX_ITERATIONS:
    1. Read the plan file
    2. Get current bd state (epic + stories)
    3. Compare: what's in the plan but missing from bd?
    4. If nothing missing → output "Plan complete!" and exit
    5. Create missing issues with proper dependencies
    6. Sync to git
    7. Increment iteration and repeat
```

## Step 1: Read Plan and BD State

```bash
# Read the input plan
cat "$PLAN_PATH"

# See what bd issues exist
bd list --status=open
bd list --type=epic

# If no epic exists yet, you'll create one
```

## Step 2: First Iteration - Create Epic and Initial Stories

If no epic exists for this plan:

```bash
# Create the epic - use a title that captures the plan's goal
bd create --type epic --title "<Feature/Project Name>"

# Note the epic ID for subsequent commands
```

Then create stories for the major sections. Each story should be:
- **Right-sized**: One focused task, completable in one agent session
- **Specific**: Clear acceptance criteria with testable outcomes
- **Contextual**: Include file paths, patterns to follow, test commands

## Step 3: Compare Plan vs BD

After creating initial stories, systematically check coverage:

**For each major section in the plan:**
1. Is there a bd story that covers this?
2. Are the acceptance criteria specific enough?
3. Are dependencies set correctly?

Read through the plan section by section and verify each has corresponding bd stories.

## Step 4: Create Missing Stories

For each gap found:

```bash
bd create --title "Story: <specific task>" \
  --parent <epic-id> \
  --priority <1-4> \
  --body "## Acceptance Criteria
- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2

## From Plan Section
<quote relevant part of input plan>

## Implementation Notes
- Key files: <paths>
- Follow pattern in: <reference>
- Test command: <command>"
```

Add dependencies:
```bash
# If story B requires story A to be done first
bd dep add <story-B-id> <story-A-id>
```

## Step 5: Sync and Verify

After each iteration, **sync to git** then verify:

```bash
# IMPORTANT: Sync bd changes to git after each iteration
bd sync

# Count stories
STORY_COUNT=$(bd list --parent <epic-id> --json 2>/dev/null | jq 'length')
echo "Stories created: $STORY_COUNT"

# Show dependency tree
bd list --parent <epic-id>

# Check what's ready to implement
bd ready
```

Then re-read the plan and check:
- Did I miss any sections?
- Are stories granular enough for single-agent implementation?
- Are dependencies ordered correctly (foundational work first)?

If gaps remain AND iteration < MAX_ITERATIONS → go back to Step 3.

If no gaps → output completion summary and exit.

## Story Sizing Guidelines

**Too big (split it):**
- "Implement entire feature"
- "Build the full UI"
- "Add complete support for X"

**Right size:**
- "Create component X with props Y"
- "Implement database schema for Z"
- "Add API endpoint for W"
- "Write unit tests for V"

**Too small (combine or skip):**
- "Add import statement"
- "Fix typo in comment"

## Dependency Ordering

Identify phases in the plan and order dependencies accordingly:
1. **Foundation stories** → no dependencies (scaffolding, schemas, base setup)
2. **Core feature stories** → depend on foundation
3. **Integration stories** → depend on core features
4. **Testing stories** → depend on implementation
5. **Polish/hardening** → depend on testing

## Completion Criteria

The plan is complete when:
1. Every section of the input plan has corresponding bd stories
2. Each story has specific, testable acceptance criteria
3. Dependencies reflect the build order
4. Stories are right-sized for single-agent implementation
5. `bd ready` shows foundational stories ready to start

## Step 6: Final Sync

Before exiting, always run:
```bash
bd sync
```

This ensures all bd changes are committed.

## Output Format (on completion)

```
## Plan Complete!

**Epic:** <epic-id> - <title>
**Total Stories:** <count>
**Iterations Used:** <n> of <max>

**Ready to implement (no blockers):**
- <story-id>: <title>
- <story-id>: <title>

**Blocked (waiting on dependencies):**
- <story-id>: <title> [blocked by: <dep-id>]
...

**To implement:**
./ralph.sh 25
```

---

Begin now. Check $PLAN_PATH and $MAX_ITERATIONS, then start your first iteration.
