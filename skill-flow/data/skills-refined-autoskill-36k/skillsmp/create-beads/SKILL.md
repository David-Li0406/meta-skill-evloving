---
name: create-beads
description: Import a BEADS.md file into bd and set up dependencies. Use after /write-beads and /bead-review.
---

# Create Beads

Import a reviewed BEADS.md file into the bd issue tracker and configure all dependencies.

## When to use

Use after:
1. `/write-beads` has created the BEADS.md file
2. `/bead-review` has verified the beads are correct

## Workflow

### Step 0: Run schema validation (if validator exists)

Before importing, run the plan validator to ensure the BEADS.md file conforms to schema requirements:

```bash
pnpm validate:plans -- --path docs/plans/<project>
```

**If validation fails:** Fix the schema errors first, then re-run validation before proceeding.

**If no validator exists:** Skip to Step 1.

### Step 1: Validate the BEADS.md file

Confirm the file exists and has the required sections:
- Bead definitions (## ID: Title format)
- Dependency script (bash script with `bd dep add` commands; do not use `bd update --blocked-by`)

```bash
# Check file exists
ls docs/plans/<project>/BEADS.md

# Count beads (## headers that look like bead IDs)
grep -c "^## [A-Z]" docs/plans/<project>/BEADS.md
```

**Derive the project label** from the project folder name (e.g., `050_agent_planner_query_execution` → `050-query-execution` or similar short identifier).

### Step 2: Check for existing beads

Before creating, check if beads already exist to avoid duplicates:

```bash
bd list -l <project-label> --json 2>/dev/null | jq 'length'
```

If beads already exist, confirm with user before proceeding.

### Step 3: Create beads in bd

```bash
bd create -f docs/plans/<project>/BEADS.md
```

This creates all beads with their priority, type, description, and acceptance criteria.

**Expected output:**
```
✓ Created N issues from docs/plans/<project>/BEADS.md:
  project-xxxx: SETUP-01: Title [P0, task]
  project-yyyy: SETUP-02: Title [P0, task]
  ...
```

**Note:** `bd create -f` may not import labels from the markdown file. Labels must be added in Step 4.

### Step 4: Add project label to all beads

**This step is required.** After creation, add the project label to all beads so they can be filtered and managed as a group.

Capture the bead IDs from the `bd create` output, then add labels:

```bash
# Add project label to all created beads
for id in <space-separated-list-of-bead-ids>; do
  bd update "$id" --add-label <project-label>
done
```

**Important:** Use `--add-label` (not `--labels` or `--set-labels`) to add labels without removing existing ones.

### Step 5: Add dependencies

The dependency script in BEADS.md uses symbolic IDs (e.g., `SETUP-01`). Map these to actual bead IDs:

```bash
# Get bead ID mapping (run after labels are applied)
bd list -l <project-label> --json | jq -r '.[] | "\(.title | split(":")[0] | gsub(" "; "")): \(.id)"'
```

Then add each dependency using the actual IDs:

```bash
bd dep add <child-id> <parent-id>
# ... continue for all dependencies from BEADS.md script
```

### Step 6: Sync and verify

```bash
bd sync

# Check all beads were created with labels
bd list -l <project-label> --json | jq 'length'

# Check ready beads (no blockers)
bd ready -l <project-label>
```

### Step 7: Report

Summarize:
- Total beads created
- Project label applied
- Beads by phase/priority (P0/P1/P2/P3)
- Dependencies added
- Ready beads (no blocking dependencies)
- Any errors encountered

## Error Handling

### "No issues found in markdown file"
The BEADS.md uses wrong format. Beads must use `## ID: Title` format (H2), not `### ` or YAML blocks.

### "dependency target X not found"
Dependencies cannot reference symbolic IDs during creation. The dependency script must run AFTER beads are created with mapped IDs.

### "unknown flag: --labels"
Use `--add-label` instead of `--labels` when adding labels to beads.

### Duplicate beads
If beads already exist, `bd create -f` will create duplicates. Always check first with `bd list -l <project-label>`.

## Example Session

```
User: /create-beads docs/plans/050_agent_planner_query_execution/BEADS.md

Agent: I'll import the beads and set up dependencies.

Step 1: Validating BEADS.md...
Found 18 bead definitions.
Found dependency script with 20 dependencies.
Project label: 050-query-execution

Step 2: Checking for existing beads...
No existing beads with label 050-query-execution.

Step 3: Creating beads...
$ bd create -f docs/plans/050_agent_planner_query_execution/BEADS.md
✓ Created 18 issues

Step 4: Adding project label...
$ for id in auto_dash-xxx auto_dash-yyy ...; do bd update "$id" --add-label 050-query-execution; done
✓ Labels added to 18 beads

Step 5: Adding dependencies...
$ bd dep add auto_dash-poe auto_dash-hop  # CONFIG-01 depends on DEPS-01
$ bd dep add auto_dash-0tr auto_dash-hop  # ERRORS-01 depends on DEPS-01
... (18 more dependencies)
✓ Added 20 dependencies

Step 6: Syncing and verifying...
$ bd sync
$ bd list -l 050-query-execution --json | jq 'length'
18
$ bd ready -l 050-query-execution
Ready: DEPS-01

Step 7: Summary
- Total beads: 18
- Label: 050-query-execution
- P0: 3, P1: 6, P2: 6, P3: 3
- Dependencies: 20
- Ready to start: DEPS-01 (Add SingleStore Dependencies)

Done! Run `bd ready -l 050-query-execution` to see available work.
```
