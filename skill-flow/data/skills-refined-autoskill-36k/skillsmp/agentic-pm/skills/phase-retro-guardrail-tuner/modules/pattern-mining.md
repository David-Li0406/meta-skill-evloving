# Module: Pattern Mining (Evidence → Themes)

## Objective

Cluster phase execution issues into actionable patterns.

## Clustering dimensions

Analyze evidence across these dimensions:

### 1. Ambiguity
- Unclear acceptance criteria
- Missing non-goals
- Vague implementation notes
- Multiple interpretations possible

### 2. Missing prerequisites
- Wrong base branch
- Missing files or dependencies
- Contract drift from other tasks
- Environment assumptions

### 3. Testing gaps
- Vague testing requirements
- CI failures
- Missing test cases
- Coverage regressions

### 4. Integration pain
- Merge conflicts
- Sequencing errors
- Contract mismatches
- Dependencies not ready

### 5. Tooling issues
- Confusing git instructions
- Environment setup problems
- Build/CI configuration
- Documentation gaps

### 6. Scope creep
- "Helpful refactor" additions
- New dependencies introduced
- Untracked changes
- Expanded requirements

## Output format

For each pattern identified:

```markdown
### Pattern: <name>

**Frequency**: <# tasks impacted>

**Evidence**:
- TASK-XXX: "<quoted snippet>"
- TASK-YYY: "<quoted snippet>"

**Root cause hypothesis**:
<Why this keeps happening>

**Prevention strategy**:
<How to prevent in future>
```

## Severity classification

- **Critical**: Blocked tasks, required rework
- **High**: Significant delays, confusion
- **Medium**: Minor friction, workarounds found
- **Low**: Annoyances, small inefficiencies

## Pattern validation

A pattern is valid if:
- Appears in 2+ tasks
- Has clear evidence
- Root cause is identifiable
- Prevention is actionable
