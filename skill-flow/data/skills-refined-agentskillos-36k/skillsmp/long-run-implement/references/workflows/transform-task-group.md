# Transform Task Group to PLAN.md

## Purpose
Convert a single task group from tasks.md into an executable PLAN.md file.

## Inputs
- `task_group`: Parsed task group object containing:
  - `number`: Task group number (e.g., "2")
  - `name`: Task group name (e.g., "API Endpoints")
  - `dependencies`: Array of dependency numbers (e.g., ["1"])
  - `subtasks`: Array of subtask objects
  - `acceptance_criteria`: Array of criteria strings
- `spec_path`: Path to spec folder
- `codebase_context`: Patterns inferred from codebase

## Workflow

### Step 1: Read Context Files
```
1. Read {spec_path}/spec.md for feature context
2. Read {spec_path}/planning/requirements.md if exists
3. Read {spec_path}/planning/visuals/ if exists
4. Extract:
   - Technical approach
   - Constraints and "do NOT" rules
   - File path patterns
   - Technology choices
```

### Step 2: Enrich Each Subtask
```
FOR each subtask in task_group.subtasks:
  1. Infer <files>:
     - Search codebase for similar patterns
     - Use spec.md hints
     - IF cannot infer: mark for clarification

  2. Generate <action>:
     - Merge subtask bullets into numbered steps
     - Add "what to avoid and WHY" from spec constraints
     - Reference existing patterns to follow

  3. Create <verify>:
     - From test-writing subtask (x.1) if exists
     - From acceptance criteria
     - Default: "npm test" or framework equivalent

  4. Define <done>:
     - Convert acceptance criteria to measurable form
     - Add specific success indicators
```

### Step 3: Validate Enrichment
```
FOR each subtask:
  Check required fields:
    - files: Must have at least one concrete path
    - action: Must have specific implementation steps
    - verify: Must be executable command
    - done: Must be measurable criteria

  IF any field is too vague:
    - Add to clarification_needed list
    - Mark field with placeholder

IF clarification_needed is not empty:
  - STOP transformation
  - Generate clarification request (see clarification-protocol.md)
  - Return { status: "needs_clarification", questions: [...] }
```

### Step 4: Merge Subtasks into Tasks
```
Merge related subtasks into logical tasks:
- Test-writing + implementation can be combined
- Keep task count to 2-4 per plan
- IF >4 tasks needed: split into multiple plans (NN-a, NN-b)

FOR each merged task:
  Generate XML task element:
    <task type="auto">
      <name>Task N: [Action-oriented name]</name>
      <files>[comma-separated paths]</files>
      <action>[numbered steps from merged subtasks]</action>
      <verify>[command]</verify>
      <done>[criteria]</done>
    </task>
```

### Step 5: Generate PLAN.md
```
1. Generate frontmatter:
   ---
   plan: {task_group.number}
   task_group: {task_group.name}
   claude_code_subagent: {from orchestration.yml or "general-purpose"}
   depends_on: {task_group.dependencies as JSON array}
   source_tasks: {subtask IDs as JSON array}
   ---

2. Generate <objective> from task_group context

3. Generate <context> with @file references

4. Generate <tasks> with merged task elements

5. Generate <verification> from acceptance criteria

6. Generate <success_criteria>

7. Generate <output> with SUMMARY.md path

8. Write to {spec_path}/.long-run/plans/{NN}-PLAN.md
```

### Step 6: Output
```
Return:
  - plan_path: path to generated PLAN.md
  - task_count: number of tasks in plan
  - dependencies: resolved dependency plan numbers
  - status: "generated" | "needs_clarification"
```

## Transformation Examples

### Input: Task Group
```markdown
#### Task Group 2: API Endpoints
**Dependencies:** Task Group 1

- [ ] 2.0 Complete API layer
  - [ ] 2.1 Write 2-8 focused tests
  - [ ] 2.2 Create controller
    - Actions: index, show, create
  - [ ] 2.3 Implement auth

**Acceptance Criteria:**
- All CRUD operations work
- Proper authorization enforced
```

### Output: PLAN.md
```xml
---
plan: 02
task_group: API Endpoints
depends_on: ["01"]
source_tasks: ["2.1", "2.2", "2.3"]
---

<objective>
Implement API layer with CRUD endpoints and authentication.

Purpose: Enable frontend to interact with data layer securely.
Output: REST endpoints with auth middleware.
</objective>

<context>
@agent-os/specs/[spec-name]/spec.md
@agent-os/specs/[spec-name]/planning/requirements.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Create API test suite and controller</name>
  <files>src/api/__tests__/resource.test.ts, src/api/resource/route.ts</files>
  <action>
1. Write 4-6 focused tests covering:
   - GET /resource returns list
   - POST /resource creates item with validation
   - Auth required for mutations

2. Create REST controller with actions: index, show, create
   - Use existing controller pattern
   - Return JSON with consistent shape {data, error, meta}
   - Do NOT use raw SQL - use ORM layer

3. Add auth middleware to mutation routes
   - Return 401 for missing/invalid token
   - Return 403 for insufficient permissions
  </action>
  <verify>npm test -- api/resource.test.ts</verify>
  <done>All tests pass, endpoints return correct status codes, auth enforced</done>
</task>

</tasks>

<verification>
- [ ] All API tests pass
- [ ] Endpoints return correct status codes
- [ ] Auth middleware properly enforced
</verification>

<success_criteria>
- CRUD operations functional
- Authorization working
- Tests passing
</success_criteria>

<output>
Create .long-run/summaries/02-SUMMARY.md
</output>
```
