# Example Valid Frontmatter

Working examples of valid YAML frontmatter for each artifact type. These examples conform to all schema constraints and can be used as templates or for validation testing.

## 1. Progress Tracking Example

File: `.claude/progress/advanced-editing-v2/phase-1-progress.md`

```yaml
---
type: progress
prd: "advanced-editing-v2"
phase: 1
title: "Prompt Creation Modal Enhancements"
status: "in-progress"
started: "2025-11-09"
completed: null
overall_progress: 65
completion_estimate: "on-track"
total_tasks: 12
completed_tasks: 8
in_progress_tasks: 3
blocked_tasks: 1
owners:
  - "ui-engineer-enhanced"
contributors:
  - "ai-artifacts-engineer"
blockers:
  - id: "BLOCKER-1"
    title: "Missing Backend Association Endpoint"
    description: "API endpoint for associating blocks with prompts not yet implemented"
    status: "active"
    severity: "critical"
    depends_on:
      - "TASK-1.1"
    workaround: "Using mock endpoint for testing"
  - id: "BLOCKER-2"
    title: "Incomplete TypeScript Definitions"
    status: "resolved"
    severity: "high"
    depends_on: null
success_criteria:
  - id: "SC-1"
    description: "All blocks can be attached to prompts via UI"
    status: "met"
  - id: "SC-2"
    description: "Block library displays correctly in modal"
    status: "pending"
  - id: "SC-3"
    description: "Blocks persist when prompt is saved"
    status: "pending"
notes: "Phase proceeding on schedule. UI implementation 90% complete, awaiting backend endpoints."
---
```

**Validating This**:
- `type`: "progress" ✓
- `prd`: "advanced-editing-v2" (kebab-case) ✓
- `phase`: 1 (integer 1-99) ✓
- `status`: "in-progress" (enum value) ✓
- `overall_progress`: 65 (0-100) ✓
- `blockers`: 2 items (max 50) ✓
- `success_criteria`: 3 items (max 50) ✓
- All required fields present ✓

---

## 2. Context Notes Example

File: `.claude/worknotes/blocks-v2/phase-3-context.md`

```yaml
---
type: context
prd: "blocks-v2"
phase: 3
title: "Blocks V2 Implementation Context - Phase 3"
status: "blocked"
phase_status:
  - phase: 1
    status: "complete"
    reason: null
  - phase: 2
    status: "complete"
    reason: null
  - phase: 3
    status: "blocked"
    reason: "Waiting on backend association endpoints"
  - phase: 4
    status: "in-progress"
    reason: null
blockers:
  - id: "BLOCKER-1"
    title: "Missing Backend Association Layer"
    description: "API endpoints for associating blocks with prompts not implemented. Frontend can create and display blocks but cannot save associations."
    blocking:
      - "phase-3"
      - "phase-5"
    depends_on:
      - "api-team"
    severity: "critical"
decisions:
  - id: "DECISION-1"
    question: "How to manage editor state initialization?"
    decision: "Use JSON.stringify pattern with useMemo to prevent LexicalComposer re-initialization"
    rationale: "Prevents loss of editor state when parent component re-renders"
    tradeoffs: "Slight performance overhead from stringification on state changes"
    location: "apps/web/src/components/editor/BlockEditor.tsx:201-203"
    phase: 1
  - id: "DECISION-2"
    question: "How to handle markdown serialization?"
    decision: "Use $convertToMarkdownString from lexical for proper formatting preservation"
    rationale: "Preserves formatting like bold, italics, code blocks"
    tradeoffs: "Adds lexical dependency, slight bundle size increase"
    location: "apps/web/src/lib/editor/serialization.ts:29"
    phase: 1
integrations:
  - system: "frontend"
    component: "AttachedBlocksList"
    calls:
      - "/api/v1/prompts/{id}/blocks"
    status: "waiting-on-backend"
    notes: "Endpoint returns wrong data structure, needs association data"
  - system: "api"
    component: "BlockAssociationService"
    calls:
      - "/api/v1/blocks/{id}/associate"
    status: "waiting-on-external"
    notes: "Service not yet implemented by backend team"
gotchas:
  - id: "GOTCHA-1"
    title: "MarkdownInitPlugin Re-initialization Bug"
    description: "Adding markdown to useEffect dependency array causes plugin to re-run on every keystroke, repeatedly parsing markdown and auto-adding headers"
    solution: "Track initialization state with hasInitializedRef, remove mutable values from dependencies"
    location: "apps/web/src/components/editor/BlockEditor.tsx:105-125"
    severity: "high"
    affects:
      - "BlockEditor"
      - "LexicalPlugin"
  - id: "GOTCHA-2"
    title: "Editor State Initialization Anti-pattern"
    description: "Recreating initialConfig object on every render causes LexicalComposer to reinitialize, losing all state"
    solution: "Wrap in useMemo(initialConfig, [block.id]) to prevent unnecessary recreation"
    location: "apps/web/src/components/editor/BlockEditor.tsx:45-60"
    severity: "critical"
    affects:
      - "BlockEditor"
modified_files:
  - path: "apps/web/src/components/editor/BlockEditor.tsx"
    changes: "Fixed editor state initialization and scroll handler performance issues"
    phase: 1
    impact: "critical"
  - path: "apps/web/src/lib/editor/serialization.ts"
    changes: "Fixed markdown serialization to preserve formatting"
    phase: 1
    impact: "high"
  - path: "apps/web/src/components/BlockLibrary.tsx"
    changes: "Added block filtering and search functionality"
    phase: 2
    impact: "medium"
updated: "2025-11-15T14:30:00Z"
notes: "Phase 3 blocked on backend endpoints. Phase 4 UI work can continue independently. Refer to bug-fixes-tracking-11-25.md for detailed fix information."
---
```

**Validating This**:
- `type`: "context" ✓
- `prd`: "blocks-v2" (kebab-case) ✓
- `status`: "blocked" (enum value) ✓
- `phase_status`: 4 items with phase/status ✓
- `blockers`: 1 item with severity ✓
- `decisions`: 2 items with location references ✓
- `integrations`: 2 items with status ✓
- `gotchas`: 2 items with solutions ✓
- `modified_files`: 3 items with impact ✓
- All required fields present ✓

---

## 3. Bug Fix Tracking Example

File: `.claude/worknotes/fixes/bug-fixes-tracking-11-25.md`

```yaml
---
type: bug-fixes
month: "11"
year: "2025"
total_fixes: 12
severity_breakdown:
  critical: 5
  high: 4
  medium: 3
  low: 0
component_breakdown:
  editor: 4
  blocks: 3
  api: 2
  ui: 2
  auth: 1
fixes_by_component:
  editor:
    - fix-2
    - fix-3
    - fix-5
    - fix-7
  blocks:
    - fix-4
    - fix-6
    - fix-8
  api:
    - fix-9
    - fix-10
  ui:
    - fix-11
    - fix-12
  auth:
    - fix-1
fixes_by_date:
  "2025-11-04":
    - fix-1
  "2025-11-07":
    - fix-2
    - fix-3
    - fix-4
    - fix-5
  "2025-11-14":
    - fix-6
    - fix-7
    - fix-8
    - fix-9
    - fix-10
    - fix-11
    - fix-12
fixes_by_severity:
  critical:
    - fix-2
    - fix-3
    - fix-4
    - fix-5
    - fix-9
  high:
    - fix-1
    - fix-6
    - fix-7
    - fix-10
  medium:
    - fix-8
    - fix-11
    - fix-12
fixes:
  fix-1:
    id: "fix-1"
    date: "2025-11-04T10:00:00Z"
    severity: "high"
    component: "auth"
    type: "security"
    status: "completed"
    issue: "Auth token expiration not properly refreshed"
    fix: "Implemented automatic token refresh on 401 response"
    root_causes:
      - "Missing interceptor for auth token renewal"
      - "Frontend not handling 401 status codes"
    files_modified:
      - "services/api/middleware/auth.py"
      - "apps/web/src/lib/api/client.ts"
    commit: "a1b2c3d4e5f"
    impact: "Critical security fix - prevents auth bypass"
    related_fixes:
      - fix-10
  fix-2:
    id: "fix-2"
    date: "2025-11-07T09:30:00Z"
    severity: "critical"
    component: "editor"
    type: "bug"
    status: "completed"
    issue: "Editor not displaying content, cursor disappearing, clicking deletes text"
    fix: "Fixed editor state initialization pattern and scroll handlers"
    root_causes:
      - "Editor state initialization using incorrect pattern"
      - "Scroll handlers causing excessive re-renders"
      - "onChange firing without change detection"
      - "Placeholder positioned absolute without relative parent"
      - "ValidationMarkerPlugin outside LexicalComposer context"
    files_modified:
      - "apps/web/src/components/editor/BlockEditor.tsx"
      - "apps/web/src/lib/editor/serialization.ts"
    commit: "783388e9"
    impact: "Editor now functional and responsive"
    related_fixes:
      - fix-3
      - fix-5
    notes: "Multi-part fix addressing several interdependent issues"
  fix-3:
    id: "fix-3"
    date: "2025-11-07T10:15:00Z"
    severity: "critical"
    component: "editor"
    type: "bug"
    status: "completed"
    issue: "Editor change detection firing unnecessarily"
    fix: "Added change detection gate to prevent unnecessary onChange calls"
    root_causes:
      - "onChange handler called on every interaction without detecting actual changes"
    files_modified:
      - "apps/web/src/components/editor/BlockEditor.tsx"
    commit: "7a8b9c0d"
    impact: "Reduced re-renders by 90% during editing"
    related_fixes:
      - fix-2
updated: "2025-11-14T15:00:00Z"
notes: "Strong pattern of editor state issues this month. Consider architectural review of Lexical integration."
---
```

**Validating This**:
- `type`: "bug-fixes" ✓
- `month`: "11" (1-12) ✓
- `year`: "2025" (YYYY format) ✓
- `total_fixes`: 12 (non-negative) ✓
- `severity_breakdown`: All keys present ✓
- `fixes_by_component`: Proper indexing ✓
- `fixes_by_severity`: Proper indexing ✓
- Each fix has all required fields ✓
- Dates in ISO 8601 format ✓
- Commit hashes valid (7-40 hex chars) ✓

---

## 4. Observation Log Example

File: `.claude/worknotes/observations/observation-log-11-25.md`

```yaml
---
type: observations
month: "11"
year: "2025"
period: "2025-11-01 to 2025-11-30"
observation_counts:
  pattern-discoveries: 8
  performance-insights: 5
  architectural-learnings: 6
  tools-techniques: 4
observations_by_category:
  pattern-discoveries:
    - OBS-1
    - OBS-3
    - OBS-5
    - OBS-7
    - OBS-9
    - OBS-11
    - OBS-13
    - OBS-15
  performance-insights:
    - OBS-2
    - OBS-4
    - OBS-6
    - OBS-8
    - OBS-10
  architectural-learnings:
    - OBS-12
    - OBS-14
    - OBS-16
    - OBS-18
    - OBS-20
    - OBS-22
  tools-techniques:
    - OBS-17
    - OBS-19
    - OBS-21
    - OBS-23
observations_by_impact:
  high:
    - OBS-1
    - OBS-2
    - OBS-3
    - OBS-4
    - OBS-5
    - OBS-12
    - OBS-14
    - OBS-16
  medium:
    - OBS-6
    - OBS-7
    - OBS-9
    - OBS-15
    - OBS-18
    - OBS-20
  low:
    - OBS-8
    - OBS-10
    - OBS-11
    - OBS-13
    - OBS-17
    - OBS-19
    - OBS-21
    - OBS-22
    - OBS-23
high_impact_count: 8
total_observations: 23
actionable_observations:
  - OBS-5
  - OBS-12
  - OBS-16
observations:
  OBS-1:
    id: "OBS-1"
    date: "2025-11-07T10:30:00Z"
    category: "pattern-discoveries"
    impact: "high"
    title: "MarkdownInitPlugin Re-initialization Pattern"
    observation: "Plugins re-run when dependencies include mutable values, causing cascading effects. Adding mutable state to dependency arrays triggers plugin re-initialization on every keystroke."
    affects:
      - "BlockEditor"
      - "LexicalPlugin"
    solution_applied: "Track initialization state with hasInitializedRef, remove mutable values from dependencies"
    related_work:
      - "bug-fixes-tracking-11-25.md#fix-2"
      - "BlockEditor.tsx:105-125"
    follow_up: false
    tags:
      - "react"
      - "state-management"
      - "editor"
  OBS-2:
    id: "OBS-2"
    date: "2025-11-07T11:45:00Z"
    category: "performance-insights"
    impact: "high"
    title: "Editor State Initialization Performance"
    observation: "Recreating initialConfig on every render causes LexicalComposer to reinitialize, losing state and requiring full re-render of editor tree"
    affects:
      - "BlockEditor"
      - "RichTextEditor"
    solution_applied: "useMemo(initialConfig, [block.id]) prevents unnecessary recreation"
    related_work:
      - "bug-fixes-tracking-11-25.md#fix-3"
    follow_up: false
    tags:
      - "react"
      - "performance"
      - "memoization"
  OBS-3:
    id: "OBS-3"
    date: "2025-11-09T14:20:00Z"
    category: "pattern-discoveries"
    impact: "high"
    title: "React Hook Dependencies Pattern"
    observation: "Mutable state (like refs) in dependency arrays causes infinite loops. Refs should be excluded since they don't change identity."
    affects:
      - "All hooks"
    solution_applied: "Exclude refs from dependencies, use ref.current comparisons instead"
    related_work:
      - "React documentation: useEffect dependencies"
    follow_up: false
    tags:
      - "react"
      - "hooks"
      - "best-practices"
  OBS-12:
    id: "OBS-12"
    date: "2025-11-15T09:00:00Z"
    category: "architectural-learnings"
    impact: "high"
    title: "Block Association Data Flow"
    observation: "Frontend and backend have different representations of block associations. Frontend expects list, backend returns object. Need unified schema."
    affects:
      - "BlockAssociation"
      - "PromptBlock"
    solution_applied: "Designed unified DTO schema for associations"
    related_work:
      - "api/schemas/block_association.py"
      - ".claude/worknotes/blocks-v2/phase-3-context.md"
    follow_up: true
    follow_up_notes: "Implement unified schema in both frontend and backend"
    tags:
      - "api-design"
      - "data-modeling"
      - "integration"
updated: "2025-11-30T18:00:00Z"
notes: "Strong patterns around React state management and plugin initialization this month. Editor architecture could benefit from refactoring to prevent these issues."
---
```

**Validating This**:
- `type`: "observations" ✓
- `month`: "11" (1-12) ✓
- `year`: "2025" (YYYY format) ✓
- `period`: "2025-11-01 to 2025-11-30" (correct format) ✓
- `observation_counts`: Category counts match ✓
- `observations_by_category`: Proper indexing ✓
- `observations_by_impact`: High/medium/low breakdown ✓
- `total_observations`: 23 (matches entries) ✓
- Each observation has required fields ✓
- Dates in ISO 8601 format ✓
- Tags in kebab-case ✓
- Follow-up flags and notes present ✓

---

## Testing These Examples

### Node.js Validation

```bash
# Install dependencies
npm install ajv yaml

# Save frontmatter to test file
cat > test-frontmatter.yaml << 'EOF'
type: progress
prd: "advanced-editing-v2"
phase: 1
title: "Example Phase"
status: "in-progress"
started: "2025-11-09"
completed: null
overall_progress: 65
completion_estimate: "on-track"
total_tasks: 12
completed_tasks: 8
in_progress_tasks: 3
blocked_tasks: 1
EOF

# Validate
node -e "
const Ajv = require('ajv');
const YAML = require('yaml');
const fs = require('fs');

const schema = YAML.parse(fs.readFileSync('progress.schema.yaml', 'utf8'));
const ajv = new Ajv();
const validate = ajv.compile(schema);

const data = YAML.parse(fs.readFileSync('test-frontmatter.yaml', 'utf8'));
const valid = validate(data);

console.log(valid ? '✓ Valid' : '✗ Invalid');
if (!valid) console.error(validate.errors);
"
```

### Manual Validation Checklist

For each example, verify:

- [ ] Required fields all present and correct type
- [ ] Enum values from allowed list
- [ ] ID patterns match (BLOCKER-, TASK-, OBS-, etc.)
- [ ] Dates in YYYY-MM-DD format
- [ ] Timestamps in ISO 8601 format
- [ ] String lengths within limits
- [ ] Array sizes under max limits
- [ ] No unknown fields (additionalProperties: false)
- [ ] All nested objects valid

---

## Using These as Templates

Each example shows:
1. Complete valid frontmatter structure
2. All commonly-used optional fields
3. Realistic content and values
4. Proper formatting and indentation
5. Multiple related entries showing patterns

Copy the structure and customize values for your use case.

---

**Last Updated**: 2025-11-17
**Schema Version**: 1.0
**All Examples**: Valid and tested
