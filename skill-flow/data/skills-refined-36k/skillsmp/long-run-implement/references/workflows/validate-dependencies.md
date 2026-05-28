# Validate Plan Dependencies

## Purpose
Check that all dependencies are satisfied before executing a plan.

## Inputs
- `plan_path`: Path to PLAN.md file
- `state_path`: Path to .long-run/ directory

## Workflow

### Step 1: Read Plan Dependencies
```
plan = read PLAN.md frontmatter
dependencies = plan.depends_on  # e.g., ["01", "03"]
```

### Step 2: Check Each Dependency
```
FOR each dep_id in dependencies:
  summary_path = {state_path}/summaries/{dep_id}-SUMMARY.md

  IF not exists(summary_path):
    Return {
      valid: false,
      missing: dep_id,
      reason: "Dependency plan not executed"
    }

  summary = read summary_path frontmatter
  status = summary.status
```

### Step 3: Validate Status
```
SWITCH status:
  CASE "completed":
    # OK - continue checking next dependency
    CONTINUE

  CASE "failed":
    Return {
      valid: false,
      blocked_by: dep_id,
      status: "failed",
      options: [
        { id: "skip", label: "Skip current plan (mark as skipped)" },
        { id: "retry", label: "Retry failed dependency first" },
        { id: "ignore", label: "Ignore failure and proceed anyway" }
      ]
    }

  CASE "partial":
    Return {
      valid: false,
      blocked_by: dep_id,
      status: "partial",
      options: [
        { id: "skip", label: "Skip current plan" },
        { id: "resume", label: "Resume partial dependency first" },
        { id: "ignore", label: "Proceed with partial dependency" }
      ]
    }

  CASE "skipped":
    Return {
      valid: false,
      blocked_by: dep_id,
      status: "skipped",
      reason: summary.reason,  # e.g., "needs-clarification"
      options: [
        { id: "cascade", label: "Skip current plan (cascade skip)" },
        { id: "clarify", label: "Provide clarification for skipped plan first" },
        { id: "ignore", label: "Ignore skip and proceed anyway (risky)" }
      ]
    }

  CASE "timeout":
    Return {
      valid: false,
      blocked_by: dep_id,
      status: "timeout",
      options: [
        { id: "skip", label: "Skip current plan" },
        { id: "retry", label: "Retry timed-out dependency" },
        { id: "ignore", label: "Proceed despite timeout" }
      ]
    }
```

### Step 4: All Dependencies Valid
```
IF all dependencies checked successfully:
  Return {
    valid: true,
    dependencies: dependencies,
    all_completed: true
  }
```

## Circular Dependency Detection

### Build Dependency Graph
```
FUNCTION build_graph(plans_directory):
  graph = {}

  FOR each plan_file in plans_directory:
    plan = read frontmatter
    graph[plan.plan] = plan.depends_on or []

  Return graph
```

### Detect Cycles
```
FUNCTION has_cycle(graph):
  visited = {}
  rec_stack = {}

  FUNCTION dfs(node):
    visited[node] = true
    rec_stack[node] = true

    FOR each neighbor in graph[node]:
      IF not visited[neighbor]:
        IF dfs(neighbor):
          Return true
      ELSE IF rec_stack[neighbor]:
        Return true

    rec_stack[node] = false
    Return false

  FOR each node in graph:
    IF not visited[node]:
      IF dfs(node):
        Return true

  Return false
```

### Report Cycle
```
IF cycle detected:
  cycle_path = trace_cycle(graph)
  Return {
    valid: false,
    reason: "circular_dependency",
    cycle: cycle_path,  # e.g., ["01", "02", "03", "01"]
    message: "Circular dependency detected: 01 → 02 → 03 → 01"
  }
```

## User Decision Handling

### Present Options
```
"Plan {plan_id} depends on Plan {dep_id} which {status_message}.

{options as numbered list}

Select option (1-N):"
```

### Handle Choice
```
SWITCH user_choice:
  CASE "skip":
    - Create skipped SUMMARY for current plan
    - Mark as "skipped" with reason "dependency-{status}"
    - Return to continue to next plan

  CASE "retry" | "resume":
    - Set current_plan to dependency
    - Restart execution from dependency

  CASE "ignore":
    - Log warning in STATE.md
    - Proceed with execution
    - Document risk in SUMMARY.md

  CASE "cascade":
    - Create skipped SUMMARY for current plan
    - reason: "cascade-from-{dep_id}"
    - Continue to next plan

  CASE "clarify":
    - Load clarification for skipped dependency
    - Present to user
    - On response, retry dependency transformation
```

## Output

```typescript
interface DependencyValidation {
  valid: boolean;
  missing?: string;
  blocked_by?: string;
  status?: "failed" | "partial" | "skipped" | "timeout";
  reason?: string;
  options?: Array<{ id: string; label: string }>;
  cycle?: string[];
}
```
