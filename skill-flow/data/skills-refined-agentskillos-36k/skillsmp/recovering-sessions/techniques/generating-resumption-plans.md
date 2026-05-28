# Generating Resumption Plans

Create actionable recovery reports with ready-to-execute Task() commands for resuming interrupted work.

## Recovery Report Structure

A complete recovery report includes:

1. **Header**: Timestamp, project path, session context
2. **Agent Status Summary**: Table of all agents with status
3. **Completed Work**: Inventory of verified deliverables
4. **Interrupted Tasks**: Details and resumption commands
5. **Failed Tasks**: Errors and remediation steps
6. **Recommended Actions**: Prioritized next steps

## Report Template

```markdown
# Session Recovery Report

**Generated**: {timestamp}
**Project**: {project_path}
**Session Duration**: {start_time} - {end_time}

## Quick Summary

| Status | Count |
|--------|-------|
| COMPLETE | X |
| IN_PROGRESS | Y |
| FAILED | Z |
| UNKNOWN | W |

## Agent Status Summary

| Agent ID | Task | Status | Files | Tests | Notes |
|----------|------|--------|-------|-------|-------|
| {id} | {task_name} | {status} | {count} | {results} | {notes} |

## Completed Work

### Successfully Verified Deliverables

- **TASK-X.1: {TaskName}**
  - Files: `path/to/file.ts`, `path/to/file.test.ts`
  - Tests: 17/17 passing
  - Coverage: 95%

## Interrupted Tasks

### TASK-X.2: {TaskName}

**Status**: IN_PROGRESS (crashed mid-execution)

**Last Known State**:
- Component scaffolding created
- Tests partially written
- Missing: accessibility, documentation

**Files Created** (need verification):
- `path/to/component.tsx` (exists, 2KB)
- `path/to/component.test.tsx` (exists, 1KB)

**Resumption Command**:
```
Task("ui-engineer-enhanced", "Complete TASK-X.2: {TaskName}

Last state: Component scaffolding exists, tests partial
Missing:
- Complete test coverage (currently 40%)
- Add accessibility attributes
- Add JSDoc documentation

Files to complete:
- path/to/component.tsx
- path/to/component.test.tsx

Follow project patterns from existing components.")
```

## Failed Tasks

### TASK-X.3: {TaskName}

**Status**: FAILED

**Error**:
```
TypeError: Cannot read property 'id' of undefined
at processData (path/to/file.ts:42)
```

**Root Cause**: Missing null check in data processing

**Remediation Command**:
```
Task("ui-engineer-enhanced", "Fix TASK-X.3: {TaskName}

Error: TypeError at processData - null check missing
Location: path/to/file.ts:42

Fix: Add null check before accessing 'id' property
Test: Ensure tests cover null/undefined input cases")
```

## Recommended Actions

### Immediate (Before Next Session)

1. [ ] Review and commit completed work
2. [ ] Update progress tracking
3. [ ] Resume highest-priority interrupted task

### Commit Command

```bash
git add path/to/verified/files
git commit -m "feat: recover work from interrupted session

Completed:
- TASK-X.1: TaskName (17 tests, 95% coverage)

Interrupted (to resume):
- TASK-X.2: TaskName (partial)

Failed (needs fix):
- TASK-X.3: TaskName (TypeError)

Recovered via session-recovery skill"
```

### Resume Commands (Priority Order)

1. Fix failed tasks first:
   ```
   Task("ui-engineer-enhanced", "Fix TASK-X.3...")
   ```

2. Then complete interrupted tasks:
   ```
   Task("ui-engineer-enhanced", "Complete TASK-X.2...")
   ```

## Prevention Notes

This session crashed due to: {crash_reason}

Recommendations for next session:
- Reduce parallel agent count from 6 to 3-4
- Add checkpoint after each task completion
- Use background execution with timeouts
```

## Building the Report

### Step 1: Collect Agent Analysis

From log analysis (see `./parsing-jsonl-logs.md`):

```javascript
const agentResults = [
  {
    id: 'a91845a',
    taskId: 'TASK-2.1',
    taskName: 'MatchAnalyzer',
    status: 'COMPLETE',
    filesCreated: ['src/analyzer.ts', 'src/analyzer.test.ts'],
    testResults: '33/33 passed',
    coverage: '97.67%'
  },
  {
    id: 'xyz1234',
    taskId: 'TASK-4.3',
    taskName: 'RatingDialog',
    status: 'IN_PROGRESS',
    filesCreated: ['src/RatingDialog.tsx'],
    testResults: null,
    lastError: null
  }
];
```

### Step 2: Verify On-Disk State

From verification (see `./verifying-on-disk-state.md`):

```javascript
const verificationResults = {
  verified: ['src/analyzer.ts', 'src/analyzer.test.ts'],
  missing: [],
  issues: []
};
```

### Step 3: Generate Status Summary

```javascript
function generateStatusSummary(agents) {
  const summary = {
    COMPLETE: 0,
    IN_PROGRESS: 0,
    FAILED: 0,
    UNKNOWN: 0
  };

  for (const agent of agents) {
    summary[agent.status]++;
  }

  return summary;
}
```

### Step 4: Generate Resumption Commands

```javascript
function generateResumptionCommand(task) {
  const agent = determineAgent(task);

  return `Task("${agent}", "${task.taskId}: ${task.taskName}

Last state: ${task.lastState}
Missing: ${task.missing.join(', ')}

Files to complete:
${task.files.map(f => `- ${f}`).join('\n')}

Follow project patterns from existing components.")`;
}

function determineAgent(task) {
  // Map task type to appropriate agent
  const agentMap = {
    'component': 'ui-engineer-enhanced',
    'api': 'python-backend-engineer',
    'schema': 'python-backend-engineer',
    'test': 'python-backend-engineer',
    'docs': 'documentation-writer'
  };

  return agentMap[task.type] || 'codebase-explorer';
}
```

### Step 5: Generate Commit Message

```javascript
function generateCommitMessage(completed, interrupted, failed) {
  return `feat: recover work from interrupted session

Completed:
${completed.map(t => `- ${t.taskId}: ${t.taskName}`).join('\n')}

Interrupted (to resume):
${interrupted.map(t => `- ${t.taskId}: ${t.taskName}`).join('\n')}

${failed.length ? `Failed (needs fix):\n${failed.map(t => `- ${t.taskId}: ${t.taskName}`).join('\n')}` : ''}

Recovered via session-recovery skill`;
}
```

## Full Report Generation Script

See `../scripts/generate-recovery-report.js` for complete implementation:

```bash
# Generate report for current project
node generate-recovery-report.js

# Generate report with specific time window
node generate-recovery-report.js --minutes 180

# Generate report with known agent IDs
node generate-recovery-report.js --agents a91845a,abec615
```

## Resumption Command Patterns

### UI Component Resumption

```
Task("ui-engineer-enhanced", "Complete {TaskId}: {ComponentName}

Current state:
- Component exists at: {filePath}
- Tests exist but incomplete

Missing:
- Full test coverage (currently {X}%)
- Accessibility attributes (aria-*)
- JSDoc documentation
- Storybook story

Project patterns:
- Use Radix UI primitives from @meaty/ui
- Follow existing component structure in src/components/
- Tests use vitest + testing-library")
```

### API Endpoint Resumption

```
Task("python-backend-engineer", "Complete {TaskId}: {EndpointName}

Current state:
- Router scaffolding at: {routerPath}
- Schema partially defined

Missing:
- Complete schema validation
- Service layer implementation
- Repository queries
- Integration tests

Project patterns:
- Follow layered architecture: router → service → repository
- Use Pydantic schemas in app/schemas/
- Tests in app/tests/test_{name}.py")
```

### Test Completion Resumption

```
Task("python-backend-engineer", "Complete tests for {TaskId}: {ModuleName}

Current state:
- Implementation complete at: {implPath}
- Test file exists but incomplete

Missing:
- Edge case tests
- Error path tests
- Integration tests
- Coverage goal: {targetCoverage}%

Current coverage: {currentCoverage}%

Test patterns:
- Use pytest fixtures
- Mock external dependencies
- Cover all public functions")
```

## Integration with Progress Tracking

After generating recovery report, update progress tracking:

```
Task("artifact-tracker", "Update {PRD} phase {N}:
- TASK-X.1: complete (recovered)
- TASK-X.2: in_progress (interrupted, resuming)
- TASK-X.3: blocked (error, needs fix)
- Add note: Recovered from session crash at {timestamp}")
```

## Recommended Actions Priority

Generate recommended actions in priority order:

1. **Critical**: Fix failed tasks that block others
2. **High**: Complete interrupted tasks near completion
3. **Medium**: Resume interrupted tasks with substantial work remaining
4. **Low**: Verify UNKNOWN status tasks

```javascript
function prioritizeActions(tasks) {
  return [
    ...tasks.filter(t => t.status === 'FAILED' && t.isBlocking),
    ...tasks.filter(t => t.status === 'FAILED' && !t.isBlocking),
    ...tasks.filter(t => t.status === 'IN_PROGRESS' && t.completionEstimate > 80),
    ...tasks.filter(t => t.status === 'IN_PROGRESS' && t.completionEstimate <= 80),
    ...tasks.filter(t => t.status === 'UNKNOWN')
  ];
}
```

## Report Output Options

### Markdown Report (Default)

For human review and documentation:

```bash
node generate-recovery-report.js > recovery-report.md
```

### JSON Report

For programmatic processing:

```bash
node generate-recovery-report.js --format json > recovery-report.json
```

### Console Summary

For quick overview:

```bash
node generate-recovery-report.js --summary
```

## Using the Template

The template at `../templates/recovery-report.md` provides:
- Complete structure with placeholders
- Example entries for each section
- Variable substitution markers

```bash
# Copy template and fill in
cp templates/recovery-report.md reports/recovery-$(date +%Y%m%d-%H%M%S).md
```

## Next Steps

After generating recovery report:

1. **Review with user** - Confirm status assessments
2. **Commit completed work** - Use generated commit message
3. **Update progress tracking** - Via artifact-tracking skill
4. **Execute resumption commands** - In priority order
5. **Monitor for similar issues** - Apply prevention patterns
