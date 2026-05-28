# Dependency Patterns for Task Decomposition

This reference provides detailed patterns for identifying and mapping dependencies between tasks extracted from specification documents.

## Dependency Types

### Hard Dependencies

A hard dependency exists when Task B **cannot start** until Task A is complete. The relationship is blocking and must be respected in execution order.

**Indicators of hard dependencies:**
- Task B requires output/artifacts from Task A
- Task B modifies code that Task A creates
- Task B tests functionality that Task A implements
- Task B extends an interface/API that Task A defines

**Examples:**
```
TASK-001: Create User model schema
TASK-002: Implement User CRUD operations  # Hard depends on TASK-001
TASK-003: Write User model unit tests     # Hard depends on TASK-001
```

### Soft Dependencies

A soft dependency exists when Task B **benefits from** Task A being complete but can proceed independently. These are "nice to have" orderings.

**Indicators of soft dependencies:**
- Task B could use patterns established by Task A
- Task B might need minor adjustments if started before Task A
- Task B is in the same domain/module as Task A
- Task B's implementation could inform Task A's design

**Examples:**
```
TASK-010: Implement login endpoint
TASK-011: Implement logout endpoint     # Soft depends on TASK-010 (shares auth patterns)
TASK-012: Implement password reset      # Soft depends on TASK-010 (similar flow)
```

### Resource Dependencies

A resource dependency exists when multiple tasks modify the same files, modules, or external services. These aren't blocking but require coordination.

**Indicators of resource dependencies:**
- Tasks modify the same file
- Tasks configure the same service
- Tasks share database tables
- Tasks use the same environment variables

**Examples:**
```
TASK-020: Add email field to User model
TASK-021: Add phone field to User model    # Resource depends (same model file)
TASK-022: Add user preferences table       # Resource depends (same migration system)
```

## Identifying Dependencies from Specifications

### Structural Analysis

Examine the specification structure to identify implicit dependencies:

1. **Hierarchical sections** often indicate hard dependencies
   - Parent feature must exist before child features
   - Foundation components before higher-level features

2. **Sequential descriptions** suggest execution order
   - "First... then... finally..." language
   - Numbered steps in requirements

3. **Cross-references** reveal relationships
   - "Uses the X from section Y"
   - "Extends the functionality described in..."

### Keyword Analysis

Look for dependency-indicating language:

**Hard dependency keywords:**
- "requires", "depends on", "after", "once X is complete"
- "uses", "consumes", "reads from", "writes to"
- "extends", "inherits", "implements"

**Soft dependency keywords:**
- "similar to", "like", "follows the pattern of"
- "related to", "in the same area as"
- "should be consistent with"

**Resource dependency keywords:**
- "also modifies", "shares", "both use"
- "same file", "same table", "same config"

### Technical Analysis

Identify dependencies from technical implications:

1. **Data model dependencies**
   - Create table → Create model → Create repository → Create service → Create API
   - Each layer depends on the previous

2. **API dependencies**
   - Define interface → Implement backend → Implement frontend
   - Tests depend on implementation

3. **Infrastructure dependencies**
   - Setup → Configuration → Implementation → Deployment
   - Later stages require earlier stages

## Dependency Graph Construction

### Building the Graph

1. **List all tasks as nodes**
2. **For each task, identify:**
   - What it produces (outputs)
   - What it consumes (inputs)
   - What files/resources it touches

3. **Create edges based on:**
   - Producer-consumer relationships (hard)
   - Pattern-following relationships (soft)
   - Shared resource relationships (resource)

### Detecting Cycles

Circular dependencies indicate specification issues:

```
TASK-A depends on TASK-B
TASK-B depends on TASK-C
TASK-C depends on TASK-A  # Cycle detected!
```

**Resolution strategies:**
1. Break the cycle by splitting a task
2. Identify the true dependency direction
3. Flag for human review/clarification

### Calculating Execution Phases

Group tasks into phases based on dependency depth:

**Phase 1**: Tasks with no hard dependencies (can start immediately)
**Phase 2**: Tasks whose hard dependencies are all in Phase 1
**Phase 3**: Tasks whose hard dependencies are all in Phase 1 or 2
...and so on.

```python
# Pseudocode for phase calculation
def calculate_phases(tasks, hard_deps):
    phases = []
    remaining = set(tasks)
    completed = set()

    while remaining:
        # Find tasks whose dependencies are all completed
        ready = [t for t in remaining
                 if all(d in completed for d in hard_deps[t])]

        if not ready:
            # Circular dependency detected
            raise CycleError(remaining)

        phases.append(ready)
        completed.update(ready)
        remaining -= set(ready)

    return phases
```

## Priority Calculation

### Dependency Depth Score

Tasks that unblock many others should be prioritized:

```
depth_score = count(tasks_that_depend_on_this_task)
```

Higher scores indicate more critical path tasks.

### Weighted Priority Formula

Combine factors for final priority:

```
priority_score = (
    dependency_depth * 3.0 +      # Most important
    risk_level * 2.0 +            # High risk = do early
    inverse_complexity * 1.0 +    # Simpler tasks first (quick wins)
    business_value * 2.5          # If specified in requirements
)
```

Map scores to priority levels:
- score >= 8.0: critical
- score >= 5.0: high
- score >= 2.5: medium
- score < 2.5: low

## Common Patterns

### Feature Implementation Pattern

```
1. Data Model (no deps)
2. Repository/Data Access (depends on 1)
3. Business Logic/Service (depends on 2)
4. API Endpoint (depends on 3)
5. Frontend Component (depends on 4)
6. Integration Tests (depends on 4, 5)
```

### CRUD Feature Pattern

```
1. Create operation (foundation)
2. Read operation (soft depends on 1 for test data)
3. Update operation (hard depends on 1)
4. Delete operation (hard depends on 1)
5. List/Search operation (soft depends on 1, 2)
```

### Configuration Pattern

```
1. Environment setup (no deps)
2. Configuration schema (depends on 1)
3. Configuration loading (depends on 2)
4. Feature using config (depends on 3)
```

## Best Practices

1. **Prefer explicit over implicit dependencies**
   - When in doubt, make the dependency explicit
   - Easier to relax than to add dependencies later

2. **Keep hard dependencies minimal**
   - Only mark as "hard" if truly blocking
   - Overuse of hard deps limits parallelization

3. **Document uncertainty**
   - If dependency type is unclear, note it
   - Flag for human review if significant

4. **Validate against specification**
   - Dependencies should trace back to requirements
   - No invented dependencies without basis

5. **Consider agent parallelization**
   - Goal is maximum parallel execution
   - Group independent tasks for concurrent work
