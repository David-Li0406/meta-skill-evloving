# State Management

How to manage and persist state across workflow steps.

---

## Principles

1. **Explicit State**: Always document what state is available
2. **Immutable Core**: Core variables (task_id, flags) don't change
3. **Accumulated Results**: Each step adds to results, doesn't replace
4. **Handoff Pattern**: Each step declares what it receives and produces

---

## State Variable Types

### 1. Core Variables (Set in init, never change)

```yaml
# Set in step-00-init, persist unchanged
task_description: string # What to do
task_id: string # Unique identifier (e.g., "01-add-auth")
auto_mode: boolean # Skip confirmations
save_mode: boolean # Save outputs to files
output_dir: string # Path to output folder (if save_mode)
```

### 2. Flag Variables (Set in init, can be overridden)

```yaml
# Parsed from user flags
examine_mode: boolean # Run optional review
test_mode: boolean # Run optional tests
economy_mode: boolean # Use simplified approach
```

### 3. Accumulated Results (Grow across steps)

```yaml
# Each step adds to these
files_found: list # Step 1 finds files
patterns_identified: list # Step 1 finds patterns
plan_items: list # Step 2 creates plan
completed_tasks: list # Step 3 tracks progress
test_results: object # Step 4 records results
```

### 4. Step-Local Variables (Only exist in current step)

```yaml
# Temporary, not passed to next step
current_file: string # File being processed
loop_counter: integer # Iteration tracking
temp_results: list # Intermediate results
```

---

## Documenting State

### In SKILL.md

```markdown
<state_variables>
**Persist throughout all steps:**

| Variable             | Type    | Description                |
| -------------------- | ------- | -------------------------- |
| `{task_description}` | string  | What to implement          |
| `{task_id}`          | string  | Kebab-case identifier      |
| `{auto_mode}`        | boolean | Skip confirmations         |
| `{save_mode}`        | boolean | Save outputs               |
| `{output_dir}`       | string  | Output path (if save_mode) |

</state_variables>
```

### In Each Step

```markdown
<available_state>
From previous step:

| Variable             | Description                        |
| -------------------- | ---------------------------------- |
| `{task_description}` | What to implement                  |
| `{task_id}`          | Unique identifier                  |
| `{auto_mode}`        | Skip confirmations                 |
| `{files_found}`      | List of relevant files from step 1 |
| `{patterns}`         | Patterns identified in step 1      |

</available_state>
```

---

## State Handoff Patterns

### Pattern 1: Simple Handoff

Step 1 produces → Step 2 consumes:

```markdown
<!-- Step 1 output -->
<produces>
| Variable | Description |
|----------|-------------|
| `{files_found}` | Files related to task |
| `{patterns}` | Patterns in codebase |
</produces>

<!-- Step 2 input -->

<available_state>
From step-01-analyze:

| Variable        | Description           |
| --------------- | --------------------- |
| `{files_found}` | Files related to task |
| `{patterns}`    | Patterns in codebase  |

</available_state>
```

### Pattern 2: Accumulated State

Each step adds to growing state:

```markdown
<!-- Step 1 -->

Adds: {files_found}, {patterns}

<!-- Step 2 -->

Receives: {files_found}, {patterns}
Adds: {plan_items}

<!-- Step 3 -->

Receives: {files_found}, {patterns}, {plan_items}
Adds: {completed_tasks}

<!-- Step 4 -->

Receives: ALL of the above
Adds: {validation_results}
```

### Pattern 3: Conditional State

State that only exists if certain flags are set:

```markdown
<available_state>
From previous step:

**Always present:**
| `{task_description}` | What to implement |
| `{task_id}` | Unique identifier |

**If `{save_mode}` = true:**
| `{output_dir}` | Path to output folder |

**If `{test_mode}` = true:**
| `{test_results}` | Results from test runs |
</available_state>
```

---

## Persisting State to Files

When `save_mode` is true, persist state to files:

### 00-context.md Structure

````markdown
# Task: {task_id}

**Created:** {timestamp}
**Task:** {task_description}

## Configuration

| Flag      | Value   |
| --------- | ------- |
| auto_mode | {value} |
| save_mode | {value} |
| test_mode | {value} |

## Progress

| Step       | Status | Timestamp   |
| ---------- | ------ | ----------- |
| 00-init    | ✓      | {timestamp} |
| 01-analyze | ✓      | {timestamp} |
| 02-plan    | ⏳     | {timestamp} |

## Accumulated State

```yaml
files_found:
  - src/auth/login.ts
  - src/api/auth/route.ts

patterns:
  - name: "Route pattern"
    example: "src/api/users/route.ts"
```
````

````

### Reading State for Resume

```markdown
<check_resume>
**If resuming:**

1. Read `00-context.md`
2. Parse configuration section → restore flags
3. Parse progress table → find last completed step
4. Parse accumulated state → restore variables
5. Load next incomplete step
</check_resume>
````

---

## State Validation

Before using state, validate it exists:

```markdown
**Validate required state:**

IF {files_found} is empty:
→ Error: "Step 1 did not find any files. Cannot proceed."
→ Offer to re-run step 1

IF {plan_items} is empty:
→ Error: "No plan created. Cannot execute."
→ Return to step 2
```

---

## Anti-Patterns

❌ **Assuming state exists without checking**

```
# Bad: Will fail if files_found is undefined
For each file in {files_found}...
```

✅ **Always validate**

```
IF {files_found} exists AND length > 0:
    For each file in {files_found}...
ELSE:
    Handle missing state
```

❌ **Overwriting accumulated state**

```
# Bad: Loses previous step's results
{results} = step_3_results
```

✅ **Append to accumulated state**

```
# Good: Preserves previous results
{results}.step_3 = step_3_results
```

❌ **Hardcoding paths**

```
# Bad: Won't work in different projects
output_dir = "/Users/me/.claude/output/"
```

✅ **Use variables**

```
# Good: Works anywhere
output_dir = {project_root}/.claude/output/{workflow}/{task_id}/
```
